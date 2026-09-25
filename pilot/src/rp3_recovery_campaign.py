"""Bounded RP3-MR1 schedule. Existing measurements are never overwritten."""
import argparse
import datetime
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import time
from rp2 import ROOT, file_hash, verify_contract
from rp2_summary import stable
from rp3 import read, checked_library
from rp3_durable import write_json, validate

OLD = ROOT/'pilot/evidence/rp3'
DONOR = ROOT/'pilot/evidence/rp2/donor-freeze.json'
SOURCES = ['pilot/src/rp3_durable.py','pilot/src/rp3_recovery_run.py',
           'pilot/src/rp3_recovery_measure.py','pilot/src/rp3_recovery_campaign.py',
           'pilot/tests/test_rp3_recovery.py','pilot/RP3_RECOVERY.md']
ORDERS = ['BCFG','CFGB','FGBC']


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def freeze_update(base, rung, source, parent, output):
    update = dict(schema=1, experiment='RP3-MR1', rung=rung,
                  usable_at={'r2':'r3','r3':'r4'}[rung], frozen_utc=now(),
                  source_freeze_sha256=file_hash(source), parent_freeze_sha256=file_hash(parent),
                  acquisitions={}, evidence_files={})
    information = set()
    for arm in 'CG':
        identities = set(); work = set()
        previous = checked_library(read(parent)['acquisitions']['1-'+arm])
        for repeat in [1,2,3]:
            d = base/f'acquire-{rung}-primary-{repeat}-{arm}'
            r = read(d/'report.json'); e = read(d/'envelope.json')
            assert e['returncode'] == 0 and r['status'] == 'COMPLETE'
            assert len(r['queries']) == len(r['rows']) == 24
            assert len((d/'events.jsonl').read_text().splitlines()) == r['candidate_attempts']
            lib = checked_library(r)
            assert lib['entries'][:len(previous['entries'])] == previous['entries']
            assert len(lib['entries'])-len(previous['entries']) <= (8 if arm == 'G' else 1000000)
            assert (d/'library.json').stat().st_size <= 1024**2
            information.add(tuple((x['query_id'],x['certificate_sha256']) for x in r['rows']))
            identities.add(r['library_sha256']); work.add(json.dumps(stable(r),sort_keys=True))
            update['acquisitions'][f'{repeat}-{arm}'] = {k:r[k] for k in
                ['library_path','library_sha256','library_serialized_bytes','object_ids','query_sha256','initial_entries','new_entries']}
            for p in sorted(d.rglob('*')):
                if p.is_file(): update['evidence_files'][str(p.relative_to(ROOT))] = file_hash(p)
        assert len(identities) == len(work) == 1, 'nonreproducible update '+arm
    assert len(information) == 1, 'C/G training information differs'
    if output.exists():
        old = read(output)
        assert {k:v for k,v in old.items() if k!='frozen_utc'} == {k:v for k,v in update.items() if k!='frozen_utc'}
    else:
        write_json(output,update)
    print(json.dumps(dict(freeze=str(output.relative_to(ROOT)),sha256=file_hash(output),
                         objects={a:len(update['acquisitions']['1-'+a]['object_ids']) for a in 'CG'})),flush=True)


def prepare(output):
    verify_contract()
    old = read(OLD/'source-freeze.json')
    for p,h in {**old['driver_sources'],**old['inherited_rp2_files']}.items():
        assert file_hash(ROOT/p) == h,p
    for p,h in read(OLD/'freeze-after-r1.json')['evidence_files'].items():
        assert file_hash(ROOT/p) == h,p
    assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip() == '6c37c4765d204362d16a2647625521e0fc6f740d'
    frozen = dict(old, experiment='RP3-MR1', frozen_utc=now(),
                  original_source_freeze_sha256=file_hash(OLD/'source-freeze.json'),
                  amendment_sha256=file_hash(ROOT/'pilot/RP3_RECOVERY.md'),
                  driver_sources={**old['driver_sources'],**{p:file_hash(ROOT/p) for p in SOURCES}},
                  original_record_commit='6c37c4765d204362d16a2647625521e0fc6f740d',
                  original_local_commit='d1f75fff5a28c92921f889fa4ca87d566fba467d',
                  original_raw_archive_sha256=file_hash(OLD/'raw-evidence.tar.gz'),
                  recovery_environment=dict(python=sys.version,executable=sys.executable,platform=platform.platform(),
                      cpu=next(l.split(':',1)[1].strip() for l in Path('/proc/cpuinfo').read_text().splitlines() if l.startswith('model name')),
                      affinity=sorted(os.sched_getaffinity(0)),memory_max=Path('/sys/fs/cgroup/memory.max').read_text().strip(),
                      cpu_max=Path('/sys/fs/cgroup/cpu.max').read_text().strip(),
                      package_access='Preserved pinned chess through PYTHONPATH; no new installation',
                      limitation='New executable path and I/O safeguards; previous host load unavailable. R1 and original acquisitions retained without timing normalization.'),
                  measurement_access=dict(r2='previously inspected; balanced replacement',r3='not yet generated',r4='not yet generated',counterplay_history='inaccessible'))
    source = output/'source-freeze.json'
    if source.exists(): raise ValueError('freeze exists')
    write_json(source,frozen)
    freeze_update(OLD,'r2',source,OLD/'freeze-after-r1.json',output/'freeze-after-r2.json')


def run(output, source, commit):
    frozen = read(source)
    assert subprocess.check_output(['git','show',commit+':'+str(source.relative_to(ROOT))]) == source.read_bytes()
    for p,h in {**frozen['driver_sources'],**frozen['inherited_rp2_files']}.items():
        assert file_hash(ROOT/p)==h,p
    assert file_hash(OLD/'raw-evidence.tar.gz') == frozen['original_raw_archive_sha256']
    for p,h in read(output/'freeze-after-r2.json')['evidence_files'].items():
        assert file_hash(ROOT/p)==h,p
    seqpath = output/'sequence.json'
    sequence = read(seqpath) if seqpath.exists() else []
    before_cpu, before_wall = time.process_time(), time.perf_counter()
    new_entries = []
    old_cpu = sum(e['cpu_s'] for e in read(OLD/'sequence.json'))
    current = OLD/'freeze-after-r1.json'

    def execute(mode,rung,arm,repeat,diagnostic='primary'):
        label=f'{mode}-{rung}-{diagnostic}-{repeat}-{arm}'; directory=output/label
        if directory.exists():
            matches=[x for x in sequence if x['label']==label]
            assert len(matches)==1, 'unrecorded directory; preserve and stop'
            validate(directory,24 if mode=='acquire' else 16)
            env=read(directory/'envelope.json')
            assert env['returncode']==matches[0]['returncode']==0
            assert all(env[u]==matches[0][u] for u in ['cpu_s','wall_s'])
            return
        command=[sys.executable,'pilot/src/rp3_recovery_measure.py','--output',str(directory/'envelope.json'),'--',
                 sys.executable,'pilot/src/rp3_recovery_run.py',mode,'--rung',rung,'--arm',arm,
                 '--repeat',str(repeat),'--diagnostic',diagnostic,'--output',str(directory/'report.json'),
                 '--freeze',str(current),'--source-freeze',str(source)]
        proc=subprocess.run(command,text=True,capture_output=True)
        env=read(directory/'envelope.json')
        entry=dict(label=label,command=command,returncode=proc.returncode,cpu_s=env['cpu_s'],wall_s=env['wall_s'],recorded_utc=now())
        sequence.append(entry);new_entries.append(entry);write_json(seqpath,sequence)
        print(json.dumps(entry),flush=True)
        if proc.returncode: raise RuntimeError('Recorded failure; no selective rerun: '+label+' '+env['stderr'][-1500:])
        validate(directory,24 if mode=='acquire' else 16)
        if old_cpu+sum(e['cpu_s'] for e in sequence)>4*3600: raise RuntimeError('RP3 CPU budget exhausted')
        if sum(p.stat().st_size for p in (ROOT/'pilot/evidence').rglob('*') if p.is_file())>1024**3: raise RuntimeError('disk budget exhausted')

    try:
        for repeat,order in enumerate(ORDERS,1):
            for arm in order: execute('evaluate','r2',arm,repeat)
        current=output/'freeze-after-r2.json'
        for rung in ['r3','r4']:
            for repeat,order in enumerate(ORDERS,1):
                for arm in order:execute('evaluate',rung,arm,repeat)
            for repeat in [1,2,3]:execute('evaluate',rung,'G',repeat,'ablation')
            for repeat,order in enumerate(ORDERS,1):
                for arm in order:execute('evaluate',rung,arm,repeat,'reverse')
            if rung=='r3':
                for repeat,order in enumerate(ORDERS,1):
                    for arm in order:
                        if arm in 'CG':execute('acquire',rung,arm,repeat)
                freeze_update(output,'r3',source,current,output/'freeze-after-r3.json')
                current=output/'freeze-after-r3.json'
        write_json(output/'execution-complete.json',dict(experiment='RP3-MR1',status='COMPLETE',processes=len(sequence),
                   final_freeze=str(current.relative_to(ROOT)),source_commit=commit,finished_utc=now()))
    finally:
        overhead=output/'orchestration.json'
        previous=read(overhead) if overhead.exists() else []
        previous.append(dict(cpu_s=time.process_time()-before_cpu,
            wall_s=max(0,time.perf_counter()-before_wall-sum(e['wall_s'] for e in new_entries)),
            note='Parent CPU and elapsed-wall residual only; child envelopes counted separately',new_processes=len(new_entries)))
        write_json(overhead,previous)


def main():
    p=argparse.ArgumentParser();p.add_argument('mode',choices=['prepare','run'])
    p.add_argument('--output',type=Path,required=True);p.add_argument('--commit')
    a=p.parse_args();a.output=a.output.resolve()
    if a.mode=='prepare':prepare(a.output)
    else:
        if not a.commit:p.error('published source commit required')
        run(a.output,a.output/'source-freeze.json',a.commit)


if __name__=='__main__':main()
