"""Read-only reconciliation of the BLOCKED RP3 record; never generates or solves.

Missing original measurements stay missing. No repeat supplies another's costs.
"""
import argparse
from collections import Counter
import json
from pathlib import Path
from checker import check
from model import Arena, query_state, sha, encoded, start
import reuse
from rp2 import ROOT, file_hash, verify_contract, write_json
from rp2_summary import stats, phase_sum
from rp2_support import geometry_id, state_at, subproof
from rp3 import read

UNITS=('cpu_s','wall_s')


def known_phases(report):
    phases=phase_sum(report)
    if 'inherited_library_load' in report:phases['inherited_library_load']=report['inherited_library_load']
    return phases


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--input',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--witnesses',type=Path,required=True)
    a=p.parse_args();a.input=a.input.resolve();a.witnesses=a.witnesses.resolve()
    verify_contract()
    frozen=read(a.input/'source-freeze.json')
    for path,digest in {**frozen['driver_sources'],**frozen['inherited_rp2_files']}.items():
        assert file_hash(ROOT/path)==digest,path
    for path,digest in read(a.input/'freeze-after-r1.json')['evidence_files'].items():
        assert file_hash(ROOT/path)==digest,path
    recovery=read(a.input/'recovery.json')
    for path,digest in recovery['operational_sources'].items():assert file_hash(ROOT/path)==digest,path
    old=read(ROOT/'pilot/evidence/rp2/summary.json')
    seq=read(a.input/'sequence.json')
    assert len(seq)==24 and len({e['label'] for e in seq})==24
    assert not list(a.input.glob('evaluate-r3-*')) and not list(a.input.glob('evaluate-r4-*'))
    out=dict(schema=1,part='RP3',verdict='BLOCKED',
        reason='Original evaluate-r2-primary-3-F/report.json stops after 14 queries and lacks final search counters; original envelope and 16 certificates survive. Cannot reconstruct missing per-query costs/work from original data.',
        first_checkpoint_recovery=recovery,groups={},prefixes={},updates={},applications={},
        inherited_carry_forward=old['carry_forward'],
        controls=dict(r3='NOT_RUN',r4='NOT_RUN'),
        r3_r4_evaluation='NOT_RUN',counterplay_history_anchor='NOT_GENERATED_OR_INSPECTED',
        cumulative_benefit='NOT_MEASURED',break_even='No observed R1/R2 break-even; R3/R4 unavailable.',
        human_llm_cost='unavailable, not zero',artifact_loss={},source_checks='all inherited RP1/RP2 and frozen RP3 source hashes match')
    groups={};certs={};checked=set();vectors=set();event_checks={}
    for entry in seq:
        d=a.input/entry['label'];r=read(d/'report.json');e=read(d/'envelope.json')
        assert e['returncode']==entry['returncode']==0 and e['status']=='COMPLETED'
        for u in UNITS:assert e[u]==entry[u]
        completion=json.loads(e['stdout'].strip());assert completion['status']=='COMPLETE'
        name=f"{r['mode']}-{r['rung']}-{r['arm']}"
        events=[json.loads(line) for line in (d/'events.jsonl').read_text().splitlines()]
        event_checks.setdefault(name,set()).add(encoded([{k:v for k,v in x.items() if k!='cost'} for x in events]))
        rows={x['query_id']:x for x in r['rows']};answers=[]
        for query in r['queries']:
            path=d/'certificates'/(query['id']+'.json');cert=read(path)
            assert cert['query']==query
            digest=sha(cert['proof']);certs[digest]=cert
            arena=Arena(**cert['proof']['arena'])
            result=cert['proof']['nodes'][cert['proof']['root']]['result']
            if query['id'] in rows:
                row=rows[query['id']];assert row['certificate_sha256']==digest and row['result']==result
            if digest not in checked:
                check(cert['proof'],query_state(query,arena),arena,cert['plies'],expected=result);checked.add(digest)
            answers.append((query['id'],result,digest))
        assert Counter('true' if v else 'false' for _,v,_ in answers)==completion['outcomes']
        if r['mode']=='evaluate':vectors.add(tuple((q,v) for q,v,_ in answers))
        if r.get('status')!='COMPLETE':
            assert d.name=='evaluate-r2-primary-3-F'
            out['artifact_loss']=dict(path=str((d/'report.json').relative_to(ROOT)),sha256=file_hash(d/'report.json'),
                preserved_measurement_rows=len(r['rows']),required_rows=len(r['queries']),
                missing_query_measurement_ids=[q['id'] for q in r['queries'] if q['id'] not in rows],
                full_original_envelope={u:e[u] for u in UNITS},complete_stdout_work=completion['total_inside_process'],
                all_16_certificates_present_and_checked=True,
                missing='Last two per-query phase/work rows; final search-count totals; table storage/memory/tally; library-hit attribution. No values copied from another repeat.')
        known=known_phases(r)
        groups.setdefault(name,[]).append(dict(report=r,envelope=e,directory=d,completion=completion,
            events=events,answers=answers,known_phase_costs=known,
            unallocated_envelope_cost={u:e[u]-sum(x[u] for x in known.values()) for u in UNITS}))
    assert len(vectors)==1
    for name,runs in groups.items():
        runs.sort(key=lambda x:x['report']['repeat'])
        assert [x['report']['repeat'] for x in runs]==[1,2,3]
        assert len({encoded(x['answers']) for x in runs})==1,name+' certificates differ'
        if name!='evaluate-r2-F':assert len(event_checks[name])==1,name+' event decisions differ'
        else:
            out['artifact_loss']['preserved_application_events']=len(runs[2]['events'])
            out['artifact_loss']['complete_other_repeats_application_events']=[len(x['events']) for x in runs[:2]]
            out['artifact_loss']['application_ledger_also_incomplete']=True
        assert len({encoded(x['completion']['total_inside_process']['work']) for x in runs})==1
        x=runs[0];r=x['report']
        out['groups'][name]=dict(outcomes=x['completion']['outcomes'],certified_queries=len(x['answers']),
            solver_unknowns=0,timeouts=0,process_failures=0,
            cost={u:stats([x['envelope'][u] for x in runs]) for u in UNITS},
            peak_rss_kib=stats([x['envelope']['child_peak_rss_kib'] for x in runs]),
            event_counts=dict(Counter(e['kind']+':'+e['status'] for e in x['events'])),
            search_counts_by_repeat=[x['report'].get('search_counts') for x in runs],
            complete_work=x['completion']['total_inside_process']['work'],
            complete_check_counts={k:v for k,v in x['completion']['total_inside_process']['checking'].items() if not k.endswith('_s')},
            known_phase_costs_by_repeat=[x['known_phase_costs'] for x in runs],
            unallocated_envelope_cost_by_repeat=[x['unallocated_envelope_cost'] for x in runs],
            application_in_search_by_repeat=[None if len(x['report']['rows'])!=len(x['answers']) else
                {u:sum(row['application_in_search'][u] for row in x['report']['rows']) for u in UNITS} for x in runs],
            fallback_residual_by_repeat=[None if len(x['report']['rows'])!=len(x['answers']) else
                {u:sum(row['fallback_residual'][u] for row in x['report']['rows']) for u in UNITS} for x in runs],
            library_serialized_bytes=r.get('library_serialized_bytes'),library_python_bytes=r.get('library_python_bytes'),
            table_bytes_by_repeat=[x['report'].get('table_serialized_bytes') for x in runs],
            table_python_bytes_by_repeat=[x['report'].get('table_python_bytes') for x in runs],
            terminal_horizon_leaves_by_repeat=[x['report'].get('table_leaf_reasons') for x in runs],
            query_certificates_identical_across_repeats=True,candidate_application_events_identical_across_repeats=len(event_checks[name])==1,
            event_counts_by_repeat=[dict(Counter(e['kind']+':'+e['status'] for e in x['events'])) for x in runs])
    # Library growth and first-witness preservation; all actual bytes retained.
    donor=read(ROOT/'pilot/evidence/rp2/acquire-1-F/library.json')
    previous={'G':donor,'C':read(ROOT/'pilot/evidence/rp2/acquire-1-C/library.json')}
    objects={e['id']:e for e in donor['entries']};cache_checked=set()
    for rung in ['r1','r2']:
        out['updates'][rung]={}
        for arm in 'CG':
            runs=groups[f'acquire-{rung}-{arm}'];libraries=[read(x['directory']/'library.json') for x in runs]
            hashes=[file_hash(x['directory']/'library.json') for x in runs];assert len(set(hashes))==1
            lib=libraries[0];initial=len(previous[arm]['entries']);assert lib['entries'][:initial]==previous[arm]['entries']
            added=lib['entries'][initial:]
            assert (runs[0]['directory']/'library.json').stat().st_size<=1024**2
            if arm=='G':
                assert len(added)<=8 and len({e['geometry_id'] for e in lib['entries']})==len(lib['entries'])
                for e in added:
                    pr=e['provenance'];proof=certs[pr['certificate_sha256']]['proof'];concrete=subproof(proof,pr['node_id'])
                    state,depth=state_at(concrete,concrete['root']);assert sha(concrete)==pr['subproof_sha256']
                    assert reuse.compile_template(concrete,state,Arena(**pr['donor_arena']),depth)==e['template']
                    assert geometry_id(state)==e['geometry_id'];objects[e['id']]=e
            else:
                for e in added:
                    state,depth=state_at(e['proof'],e['proof']['root']);arena=Arena(**e['proof']['arena'])
                    assert reuse.cache_geometry(state,arena,depth)==e['key'];check(e['proof'],state,arena,depth);cache_checked.add(e['id'])
            out['updates'][rung][arm]=dict(initial=initial,new=len(added),total=len(lib['entries']),
                library_sha256=hashes[0],library_bytes=(runs[0]['directory']/'library.json').stat().st_size,
                accepted_ids=[e['id'] for e in added],candidate_counts=out['groups'][f'acquire-{rung}-{arm}']['event_counts'],
                acquisition_cost=out['groups'][f'acquire-{rung}-{arm}']['cost'],
                first_usable_prefix='r2' if rung=='r1' else 'r3_not_evaluated')
            previous[arm]=lib
    # Reconstruct original successful applications; identify exact final sub-DAGs.
    def normalized(proof):
        return {n['state_key']:[n['result'],n['remaining'],n['leaf'],sorted((m,proof['nodes'][c]['state_key']) for m,c in n['edges'])] for n in proof['nodes'].values()}
    witnesses=set()
    for arm in 'BCFG':
        x=groups['evaluate-r2-'+arm][0];events=x['events'];accepted=[e for e in events if e['status']=='ACCEPTED']
        applications=[]
        for event in accepted:
            if 'template' not in event:continue
            spec,fen,depth,_,_=json.loads(event['state_key']);arena=Arena(**spec)
            query=dict(fen=fen+' 0 1',moves=[])
            proof,audit=reuse.instantiate(objects[event['template']]['template'],query_state(query,arena),arena,depth,event['matrix'])
            digest=sha(proof);assert digest==event['proof_sha256']
            path=a.witnesses/(digest+'.json');write_json(path,dict(query=query,plies=depth,proof=proof));witnesses.add(digest)
            retained=[]
            for q,_,h in x['answers']:
                final=certs[h]['proof']
                for identifier,node in final['nodes'].items():
                    if node['state_key']==event['state_key'] and normalized(subproof(final,identifier))==normalized(proof):retained.append(q)
            applications.append(dict(object_id=event['template'],proof_sha256=digest,state_key=event['state_key'],
                donor_arena=objects[event['template']]['provenance']['donor_arena'],retained_in_final_roots=retained,
                witness_path=str(path.relative_to(ROOT))))
        out['applications'][arm]=dict(internal_successes=len(accepted),
            failures=dict(Counter(e.get('reason',e['status']) for e in events if e['status']!='ACCEPTED')),
            applications=applications,distinct_objects=sorted({e['object_id'] for e in applications}),
            final_root_certificates=sorted({q for e in applications for q in e['retained_in_final_roots']}),
            objects_in_final_certificates=sorted({e['object_id'] for e in applications if e['retained_in_final_roots']}))
    setup=old['shared_environment_setup_once']
    for k in [1,2]:
        out['prefixes'][f'r{k}']={}
        for arm in 'BCFG':
            reps=[]
            for i in [1,2,3]:
                carried=old['carry_forward'][arm][i-1]
                total=carried['total_through_r1'].copy();evaluated=carried['evaluated_r1'].copy();acquisition=carried['donor_acquisition'].copy()
                expansions=carried['fresh_expansions'];loss=False
                if k==2:
                    run=groups['evaluate-r2-'+arm][i-1]
                    for u in UNITS:total[u]+=run['envelope'][u];evaluated[u]+=run['envelope'][u]
                    if 'search_counts' in run['report']:expansions+=run['report']['search_counts'].get('expanded_states',0)
                    else:loss=True
                    if arm in 'CG':
                        update=groups['acquire-r1-'+arm][i-1]
                        for u in UNITS:total[u]+=update['envelope'][u];acquisition[u]+=update['envelope'][u]
                        expansions+=update['report']['search_counts']['expanded_states']
                reps.append(dict(repeat=i,total=total,evaluation=evaluated,acquisition=acquisition,
                    fresh_expansions=None if loss else expansions,expansion_measurement_missing=loss))
            out['prefixes'][f'r{k}'][arm]=dict(cumulative={u:stats([r['total'][u] for r in reps]) for u in UNITS},
                including_shared_setup_once={u:stats([r['total'][u]+setup[u] for r in reps]) for u in UNITS},
                amortized_per_query={u:stats([r['total'][u]/(16*k) for r in reps]) for u in UNITS},
                raw_evaluation={u:stats([r['evaluation'][u] for r in reps]) for u in UNITS},
                charged_acquisition={u:stats([r['acquisition'][u] for r in reps]) for u in UNITS},
                matched_certified_queries=16*k,outcomes=dict(true=5+(6 if k==2 else 0),false=11+(10 if k==2 else 0),unknown=0),
                repetitions=reps)
    out['prefixes'].update(r3=None,r4=None)
    out['unusable_r2_update_expense']={arm:out['groups']['acquire-r2-'+arm]['cost'] for arm in 'CG'}
    out['shared_environment_setup_once']=setup
    out['actual_rp3_process_envelopes']={u:sum(e[u] for e in seq) for u in UNITS}
    out['actual_rp3_preflight_envelopes']={u:sum(read(p)[u] for p in (a.input/'preflight').glob('*.json')) for u in UNITS}
    out['original_rp2_total_including_reconciliation']={u:old['observed_experiment_plus_setup_and_checks'][u]+read(ROOT/'pilot/evidence/rp2/summary-check-envelope.json')[u] for u in UNITS}
    out['measured_total_before_this_audit']={u:sum(out[k][u] for k in ['actual_rp3_process_envelopes','actual_rp3_preflight_envelopes','original_rp2_total_including_reconciliation']) for u in UNITS}
    out['audit_counts']=dict(root_certificates=len(checked),new_proof_objects=len(objects)-8,new_cache_witnesses=len(cache_checked),application_witnesses=len(witnesses))
    out['data_bytes_before_summary']=sum(p.stat().st_size for p in a.input.rglob('*') if p.is_file())
    out['max_file_bytes']=max(p.stat().st_size for p in a.input.rglob('*') if p.is_file())
    out['unmetered']='Human/LLM, shell and publication/orchestration overhead unavailable; not zero. This read-only audit has a separate envelope.'
    write_json(a.output,out)
    print(json.dumps(dict(verdict=out['verdict'],artifact_loss=out['artifact_loss'],audit_counts=out['audit_counts'],
        actual_rp3_cpu=out['actual_rp3_process_envelopes']['cpu_s'])))


if __name__=='__main__':main()
