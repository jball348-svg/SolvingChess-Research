"""Serial, bounded RP3 continuation; freezes each update before the next test."""
import argparse
import datetime
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
from rp2 import ROOT, RP1, file_hash, verify_contract, write_json
from rp2_summary import stable
from rp3 import DONOR, PUBLICATION, read, checked_library

SOURCES = ['pilot/src/rp3.py', 'pilot/src/rp3_campaign.py', 'pilot/tests/test_rp3.py']


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def preflight(output):
    verify_contract()
    manifest = read(ROOT/'pilot/evidence/source-manifest.json')
    for path in manifest['files']:
        assert subprocess.check_output(['git','show',RP1+':'+path]) == (ROOT/path).read_bytes(), path
    assert subprocess.check_output(['git','rev-parse','HEAD:archive/pre-reboot-2026-09-25'], text=True).strip() == manifest['archive_tree']
    donor = read(ROOT/'pilot/evidence/rp2/donor-freeze.json')
    for path,digest in {**donor['driver_sources'],**donor['evidence_files']}.items():
        assert file_hash(ROOT/path) == digest, path
    for path in ['pilot/evidence/rp2/donor-freeze.json','pilot/evidence/rp2/publication.json','pilot/evidence/rp2/summary.json']:
        assert subprocess.check_output(['git','show',PUBLICATION+':'+path]) == (ROOT/path).read_bytes(), path
    assert read(ROOT/'pilot/evidence/rp2/publication.json')['donor_freeze_commit'] == DONOR
    assert subprocess.check_output(['git','rev-parse',DONOR+'^{tree}'],text=True).strip() == read(ROOT/'pilot/evidence/rp2/publication.json')['tree']
    for record in donor['acquisitions'].values(): checked_library(record)
    old = read(ROOT/'pilot/evidence/rp2/evaluate-1-B/report.json')
    result = dict(schema=1, frozen_utc=now(), rp1=RP1, donor=DONOR, rp2_publication=PUBLICATION,
        driver_sources={**donor['driver_sources'],**{p:file_hash(ROOT/p) for p in SOURCES}},
        inherited_rp2_files={str(p.relative_to(ROOT)):file_hash(p) for p in sorted((ROOT/'pilot/evidence/rp2').rglob('*')) if p.is_file()},
        environment=dict(python=sys.version, executable=sys.executable, platform=platform.platform(),
            cpu=next(l.split(':',1)[1].strip() for l in Path('/proc/cpuinfo').read_text().splitlines() if l.startswith('model name')),
            affinity=sorted(os.sched_getaffinity(0)), memory_max=Path('/sys/fs/cgroup/memory.max').read_text().strip(),
            cpu_max=Path('/sys/fs/cgroup/cpu.max').read_text().strip(),
            same_python_and_platform_as_rp2=sys.version==old['python'] and platform.platform()==old['platform'],
            setup='Existing RP2 virtualenv reused; no installation. RP2 CPU model/load were not recorded; identical host speed cannot be established.'),
        decisions=dict(sequence='R1 training; freeze; R2 test; R2 training; freeze; R3 test/controls; R3 training; freeze; R4 test/controls; stop',
            repeats=3, primary_orders=['BCFG','CFGB','FGBC'], acquisition_orders=['CG','CG','GC'],
            controls='At R3 and R4: three G donor-only ablation repetitions, then one reverse-order sequence with three rotating B/C/F/G repetitions.',
            cache='Fresh ordinary table per training/evaluation cohort; warm within its queries. Training always library-free baseline, identical C/G information source.',
            accounting='Pair repetition i with inherited RP2 ledger i; one acquisition per modeled use. Controls separate actual expense; ablation retains all G acquisition costs.',
            reverse_prefix='Substitute reverse R3/R4 evaluation only at those rungs, retain R1/R2 and every acquisition. Also report each reversed rung.',
            expansion_gate='Report both evaluation-only and acquisition-inclusive fresh fallback expansions; require the cumulative inclusive gate.',
            human_llm_intervention='Implementation of RP3 schedule/instrumentation only, before new outcomes; costs unavailable, not zero.'),
        reserved_execution={k:False for k in ['r1_training','r2','r3','r4','counterplay','history']})
    write_json(output,result)
    print(json.dumps(dict(source_freeze=str(output),sha256=file_hash(output),environment=result['environment'])))


def campaign(output, source):
    frozen = read(source)
    for path,digest in frozen['driver_sources'].items(): assert file_hash(ROOT/path)==digest,path
    for path,digest in frozen['inherited_rp2_files'].items(): assert file_hash(ROOT/path)==digest,path
    sequence, cpu = [], 0.0
    current = ROOT/'pilot/evidence/rp2/donor-freeze.json'
    def execute(mode,rung,arm,repeat,diagnostic='primary'):
        nonlocal cpu
        label=f'{mode}-{rung}-{diagnostic}-{repeat}-{arm}'
        directory=output/label
        if directory.exists(): raise ValueError('refusing overwrite '+str(directory))
        command=[sys.executable,'pilot/src/measure.py','--output',str(directory/'envelope.json'),'--',
                 sys.executable,'pilot/src/rp3.py',mode,'--rung',rung,'--arm',arm,'--repeat',str(repeat),
                 '--diagnostic',diagnostic,'--output',str(directory/'report.json'),
                 '--freeze',str(current),'--source-freeze',str(source)]
        process=subprocess.run(command,text=True,capture_output=True)
        env=read(directory/'envelope.json');cpu+=env['cpu_s']
        sequence.append(dict(label=label,command=command,returncode=process.returncode,
            cpu_s=env['cpu_s'],wall_s=env['wall_s'],recorded_utc=now()))
        write_json(output/'sequence.json',sequence)
        print(json.dumps(sequence[-1]),flush=True)
        if cpu>4*3600: raise RuntimeError('RP3 CPU budget exhausted; expenses retained')
        if process.returncode:
            # A process exhaustion remains a measured UNKNOWN; no selective rerun.
            # Cannot silently publish a partial, unreproducible acquisition library.
            if mode=='acquire' or read(directory/'report.json').get('status')=='BLOCKED':
                raise RuntimeError('BLOCKED: '+label+'; '+env.get('stderr','')[-1500:])
        if sum(p.stat().st_size for p in output.rglob('*') if p.is_file())>1024**3:
            raise RuntimeError('RP3 disk budget exhausted')
    for previous,next_rung in [('r1','r2'),('r2','r3'),('r3','r4')]:
        for repeat,order in enumerate(['BCFG','CFGB','FGBC'],1):
            for arm in order:
                if arm in 'CG':execute('acquire',previous,arm,repeat)
        update=dict(schema=1,rung=previous,usable_at=next_rung,frozen_utc=now(),
            source_freeze_sha256=file_hash(source),parent_freeze_sha256=file_hash(current),acquisitions={},
            evidence_files={})
        information=set()
        for arm in 'CG':
            identities=set();work=set()
            for repeat in [1,2,3]:
                directory=output/f'acquire-{previous}-primary-{repeat}-{arm}'
                r=read(directory/'report.json')
                assert r['status']=='COMPLETE'
                information.add(tuple((x['query_id'],x['certificate_sha256']) for x in r['rows']))
                identities.add(r['library_sha256']);work.add(json.dumps(stable(r),sort_keys=True))
                update['acquisitions'][f'{repeat}-{arm}']={k:r[k] for k in ['library_path','library_sha256','library_serialized_bytes','object_ids','query_sha256','initial_entries','new_entries']}
                for path in directory.rglob('*'):
                    if path.is_file():update['evidence_files'][str(path.relative_to(ROOT))]=file_hash(path)
            assert len(identities)==len(work)==1,'nonreproducible update '+arm
        assert len(information)==1,'C/G training information differs'
        current=output/f'freeze-after-{previous}.json'
        write_json(current,update)
        print(json.dumps(dict(freeze=str(current),sha256=file_hash(current),objects={a:len(update['acquisitions']['1-'+a]['object_ids']) for a in 'CG'})),flush=True)
        for repeat,order in enumerate(['BCFG','CFGB','FGBC'],1):
            for arm in order:execute('evaluate',next_rung,arm,repeat)
        if next_rung in ['r3','r4']:
            for repeat in [1,2,3]:execute('evaluate',next_rung,'G',repeat,'ablation')
            for repeat,order in enumerate(['BCFG','CFGB','FGBC'],1):
                for arm in order:execute('evaluate',next_rung,arm,repeat,'reverse')
    print(json.dumps(dict(status='RP3_EXECUTION_COMPLETE',processes=len(sequence),actual_cpu_s=cpu,final_freeze=str(current))))


def main():
    p=argparse.ArgumentParser()
    p.add_argument('mode',choices=['preflight','run'])
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--source-freeze',type=Path)
    a=p.parse_args();a.output=a.output.resolve()
    if a.mode=='preflight':
        if a.output.exists():p.error('freeze already exists')
        preflight(a.output)
    else:
        if not a.source_freeze:p.error('need source freeze')
        campaign(a.output,a.source_freeze.resolve())


if __name__=='__main__':main()
