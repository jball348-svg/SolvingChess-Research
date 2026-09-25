"""Read-only reconciliation/checking of RP2 evidence; never generates a cohort.

Added after evaluation for reporting. It does not alter experimental machinery.
"""
import argparse
from collections import Counter
import json
from pathlib import Path
import statistics
import subprocess
from model import Arena, encoded, query_state, sha, start
from checker import check
import reuse
from rp2_support import geometry_id, state_at, subproof
from rp2 import ROOT, file_hash, verify_contract, write_json


def stats(values):
    return dict(median=statistics.median(values), min=min(values), max=max(values), repeats=values)


def read(path):
    return json.loads(Path(path).read_text())


def phase_sum(report):
    phases = {}
    for name in ['contract_cost','freeze_load','library_load_and_index','shared_query_generation',
                 'candidate_enumeration','all_candidates','library_storage',
                 'table_storage_accounting','table_memory_accounting','library_memory_accounting']:
        if name in report:
            phases[name] = report[name]
    for name in ['load','search','proof_emit','serialize','proof_load','verification','certificate_storage']:
        phases[name] = {unit:sum(row.get(name,{}).get(unit,0) for row in report['rows'])
                        for unit in ['cpu_s','wall_s']}
    return phases


def stable(report):
    return dict(queries=report['query_sha256'],
                certificates=[(r['query_id'],r['result'],r['certificate_sha256']) for r in report['rows']],
                search={k:v for k,v in report['search_counts'].items() if not k.endswith('_s')},
                events=report['event_counts'], work=report['total_inside_process']['work'],
                checking={k:v for k,v in report['total_inside_process']['checking'].items() if not k.endswith('_s')})


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--input',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--transfer-certificate',type=Path,required=True)
    a = p.parse_args()
    verify_contract()
    freeze = read(a.input/'donor-freeze.json')
    for path,digest in {**freeze['evidence_files'],**freeze['driver_sources']}.items():
        assert file_hash(ROOT/path) == digest, path
    summary = dict(schema=1, acquisition_verdict='BOUNDED_POSITIVE', r1_economic_verdict='NO_ADVANTAGE',
                   cumulative_benefit='NOT_TESTED', arms={}, carry_forward={},
                   publication=read(a.input/'publication.json'))
    checked, answer_vectors = set(), set()
    all_reports, all_envelopes = [], []
    for arm in 'BCFG':
        evaluations = [read(a.input/f'evaluate-{i}-{arm}/report.json') for i in [1,2,3]]
        envelopes = [read(a.input/f'evaluate-{i}-{arm}/envelope.json') for i in [1,2,3]]
        acquisitions = [] if arm == 'B' else [read(a.input/f'acquire-{i}-{arm}/report.json') for i in [1,2,3]]
        acquisition_envelopes = [] if arm == 'B' else [read(a.input/f'acquire-{i}-{arm}/envelope.json') for i in [1,2,3]]
        assert len({encoded(stable(r)) for r in evaluations}) == 1, arm+' evaluation work changed'
        if acquisitions:
            assert len({encoded(stable(r)) for r in acquisitions}) == 1, arm+' acquisition work changed'
        for report in evaluations+acquisitions:
            assert report['status'] == 'COMPLETE'
            for row in report['rows']:
                cert = read(ROOT/row['certificate_path'])
                assert sha(cert['proof']) == row['certificate_sha256']
                if row['certificate_sha256'] not in checked:
                    arena = Arena(**cert['proof']['arena'])
                    check(cert['proof'],query_state(cert['query'],arena),arena,cert['plies'],expected=row['result'])
                    checked.add(row['certificate_sha256'])
        for report in evaluations:
            assert len(report['queries']) == 16
            answer_vectors.add(tuple((r['query_id'],r['result']) for r in report['rows']))
        for env in envelopes+acquisition_envelopes:
            assert env['returncode'] == 0 and env['status'] == 'COMPLETED'
        all_reports += evaluations+acquisitions
        all_envelopes += envelopes+acquisition_envelopes
        r = evaluations[0]
        item = dict(outcomes=r['outcomes'], stable=stable(r),
                    acquisition={}, evaluation={}, first_use_given_environment={}, amortized_per_query={},
                    phase_costs={}, library_bytes=r['library_serialized_bytes'],
                    library_python_bytes=r['library_python_bytes'], table_bytes=r['table_serialized_bytes'],
                    table_python_bytes=r['table_python_bytes'],
                    peak_rss_kib=stats([e['child_peak_rss_kib'] for e in envelopes]),
                    terminal_and_horizon_table_leaves=r['table_leaf_reasons'])
        summary['carry_forward'][arm] = []
        for i, (report,env) in enumerate(zip(evaluations,envelopes)):
            acq = acquisition_envelopes[i] if acquisition_envelopes else dict(cpu_s=0,wall_s=0)
            summary['carry_forward'][arm].append(dict(repeat=i+1,
                donor_acquisition={u:acq[u] for u in ['cpu_s','wall_s']},
                evaluated_r1={u:env[u] for u in ['cpu_s','wall_s']},
                total_through_r1={u:acq[u]+env[u] for u in ['cpu_s','wall_s']},
                fresh_expansions=report['search_counts']['expanded_states']+
                                 (acquisitions[i]['search_counts']['expanded_states'] if acquisitions else 0)))
        for unit in ['cpu_s','wall_s']:
            item['evaluation'][unit] = stats([e[unit] for e in envelopes])
            item['acquisition'][unit] = stats([e[unit] for e in acquisition_envelopes]) if acquisitions else stats([0]*3)
            totals = [c['total_through_r1'][unit] for c in summary['carry_forward'][arm]]
            item['first_use_given_environment'][unit] = stats(totals)
            item['amortized_per_query'][unit] = stats([v/16 for v in totals])
        # Disjoint primary columns; nested application/checking is labelled only.
        for phase in phase_sum(r):
            item['phase_costs'][phase] = {unit:stats([phase_sum(x)[phase][unit] for x in evaluations])
                                         for unit in ['cpu_s','wall_s']}
        item['application_inside_search'] = {unit:stats([sum(row['application_in_search'][unit] for row in x['rows'])
                                                          for x in evaluations]) for unit in ['cpu_s','wall_s']}
        item['fallback_residual'] = {unit:stats([sum(row['fallback_residual'][unit] for row in x['rows'])
                                                   for x in evaluations]) for unit in ['cpu_s','wall_s']}
        item['envelope_residual'] = {unit:stats([env[unit]-sum(v[unit] for v in phase_sum(rep).values())
                                               for env,rep in zip(envelopes,evaluations)]) for unit in ['cpu_s','wall_s']}
        assert all(v >= -1e-6 for q in item['envelope_residual'].values() for v in q['repeats'])
        item['query_cost_by_outcome'] = {}
        for outcome in [True,False]:
            item['query_cost_by_outcome'][str(outcome).lower()] = {unit:stats([
                sum(row.get(phase,{}).get(unit,0) for row in rep['rows'] if row['result']==outcome
                    for phase in ['load','search','proof_emit','serialize','proof_load','verification','certificate_storage'])
                for rep in evaluations]) for unit in ['cpu_s','wall_s']}
        summary['arms'][arm] = item
    assert len(answer_vectors) == 1
    summary['root_certificate_rechecks'] = len(checked)
    summary['root_answers_identical_all_twelve_runs'] = True
    summary['matched_coverage'] = '16/16 for B/C/F/G in all repeats; 5 true, 11 false, 0 unknown'
    summary['donor'] = {}
    library = read(a.input/'acquire-1-F/library.json')
    entries = library['entries']
    assert len({e['geometry_id'] for e in entries}) == len(entries) == 8
    fixture = start('8/8/8/8/2k5/8/K7/1R6 w - - 0 1',Arena(3,4))
    assert geometry_id(fixture) not in {e['geometry_id'] for e in entries}
    object_rows = []
    for entry in entries:
        prov = entry['provenance']
        cert = read(a.input/'acquire-1-F/certificates'/(prov['query_id']+'.json'))
        concrete = subproof(cert['proof'],prov['node_id'])
        assert sha(concrete) == prov['subproof_sha256']
        state, depth = state_at(concrete,concrete['root'])
        assert reuse.compile_template(concrete,state,Arena(3,4),depth) == entry['template']
        assert geometry_id(state) == entry['geometry_id']
        object_rows.append(dict(id=entry['id'],geometry_id=entry['geometry_id'],
                               nodes=len(concrete['nodes']),plies=entry['template']['plies'],
                               maximum_branching=max(len(n['edges']) for n in concrete['nodes'].values()),
                               donor_query=prov['query_id']))
    summary['donor'] = dict(objects=object_rows, fixture_geometry_overlap=False, distinct_geometries=8,
                             actual_object_bytes=(a.input/'acquire-1-F/library.json').stat().st_size)
    cache = read(a.input/'acquire-1-C/library.json')
    for entry in cache['entries']:
        state,depth = state_at(entry['proof'],entry['proof']['root'])
        assert reuse.cache_geometry(state,Arena(3,4),depth) == entry['key']
        check(entry['proof'],state,Arena(3,4),depth)
    summary['generic_cache_witnesses_rechecked'] = len(cache['entries'])
    events = [json.loads(s) for s in (a.input/'evaluate-1-F/events.jsonl').read_text().splitlines()]
    summary['application_failures_per_proof_run'] = dict(Counter(e.get('reason',e['status']) for e in events if e['status']!='ACCEPTED'))
    successes = [e for e in events if e['status']=='ACCEPTED']
    assert len(successes) == 1
    event = successes[0]
    spec,fen,depth,_,_ = json.loads(event['state_key'])
    arena,query = Arena(**spec),dict(fen=fen+' 0 1',moves=[])
    template = next(e['template'] for e in entries if e['id']==event['template'])
    proof,audit = reuse.instantiate(template,query_state(query,arena),arena,depth,event['matrix'])
    assert sha(proof)==event['proof_sha256']
    write_json(a.transfer_certificate,dict(query=query,plies=depth,proof=proof))
    report = read(a.input/'evaluate-1-F/report.json')
    final_roots = [r['query_id'] for r in report['rows']
        if any(n['state_key']==event['state_key'] for n in read(ROOT/r['certificate_path'])['proof']['nodes'].values())]
    summary['transfer'] = dict(distinct_objects=1,successful_applications_per_run=1,checked_nodes=audit['checked_nodes'],
                              checked_edges=audit['checked_edges'],template=event['template'],
                              donor_arena=library['entries'][0]['provenance']['donor_arena'],recipient_arena=spec,
                              retained_in_final_root_certificates=final_roots,
                              source_query=[r['query_id'] for r in report['rows'] if r['search_counts'].get('proof_hits')],
                              certificate_path=str(a.transfer_certificate),proof_sha256=sha(proof))
    setup1,setup2 = [read(a.input/'preflight'/name) for name in ['rp2-setup.json','rp2-setup-venv.json']]
    setup = dict(cpu_s=setup1['child_cpu_s']+setup2['cpu_s'],wall_s=setup1['wall_s']+setup2['wall_s'])
    summary['shared_environment_setup_once'] = dict(setup, note='Both observed installations retained; first installation was lost across session environment reset. Not multiplied by repeats or queries.')
    for arm,item in summary['arms'].items():
        item['first_use_including_observed_setup'] = {u:stats([v+setup[u] for v in item['first_use_given_environment'][u]['repeats']]) for u in ['cpu_s','wall_s']}
    summary['actual_all_repetition_envelopes'] = {u:sum(e[u] for e in all_envelopes) for u in ['cpu_s','wall_s']}
    summary['actual_preflight_envelopes'] = {u:sum(read(path)[u] for path in (a.input/'preflight').glob('rp2-checks*.json')) for u in ['cpu_s','wall_s']}
    summary['observed_experiment_plus_setup_and_checks'] = {u:summary['actual_all_repetition_envelopes'][u]+setup[u]+summary['actual_preflight_envelopes'][u] for u in ['cpu_s','wall_s']}
    summary['human_llm_design_tokens_cost'] = 'unavailable, not zero'
    summary['publication_and_manual_shell_overhead'] = 'not fully metered; not included in automated solver economics'
    summary['generated_data_bytes_before_summary'] = sum(path.stat().st_size for path in a.input.rglob('*') if path.is_file())
    for arm in 'CFG':
        item,base = summary['arms'][arm],summary['arms']['B']
        reduction = 1-item['stable']['search']['expanded_states']/base['stable']['search']['expanded_states']
        gates = dict(expansion_reduction=reduction, expansions_at_least_25_percent=reduction>=.25)
        for unit in ['cpu_s','wall_s']:
            candidate,baseline = item['first_use_given_environment'][unit],base['first_use_given_environment'][unit]
            gates[unit] = dict(ratio=candidate['median']/baseline['median'],
                saving=baseline['median']-candidate['median'],
                relative_margin=candidate['median']<=.75*baseline['median'],
                absolute_margin=baseline['median']-candidate['median']>=.05,
                separated_repeats=candidate['max']<baseline['min'])
        item['practical_advantage_gates_vs_B'] = gates
    write_json(a.output,summary)
    print(json.dumps(dict(output=str(a.output),verdict=summary['acquisition_verdict'],
                          transfer=summary['transfer'],matched_coverage=summary['matched_coverage'],
                          checked_root_certificates=len(checked),actual_cpu=summary['observed_experiment_plus_setup_and_checks']['cpu_s'])))


if __name__ == '__main__':
    main()
