"""Bounded RP3-MR1 final rerun. Existing attempt-1 measurements are never overwritten."""
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
from rp3_durable_v2 import write_json, validate

OLD = ROOT/'pilot/evidence/rp3'
FIRST = ROOT/'pilot/evidence/rp3-recovery'
ORDERS = ['BCFG', 'CFGB', 'FGBC']


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def freeze_update(base, rung, source, parent, output):
    update = dict(schema=1, experiment='RP3-MR1-FINAL', rung=rung,
                  usable_at={'r2': 'r3', 'r3': 'r4'}[rung], frozen_utc=now(),
                  source_freeze_sha256=file_hash(source), parent_freeze_sha256=file_hash(parent),
                  acquisitions={}, evidence_files={})
    information = set()
    for arm in 'CG':
        identities = set(); work = set()
        previous = checked_library(read(parent)['acquisitions']['1-'+arm])
        for repeat in [1, 2, 3]:
            d = base/f'acquire-{rung}-primary-{repeat}-{arm}'
            r = read(d/'report.json'); e = read(d/'envelope.json')
            assert e['returncode'] == 0 and r['status'] == 'COMPLETE'
            assert len(r['queries']) == len(r['rows']) == 24
            assert len((d/'events.jsonl').read_text().splitlines()) == r['candidate_attempts']
            lib = checked_library(r)
            assert lib['entries'][:len(previous['entries'])] == previous['entries']
            assert len(lib['entries'])-len(previous['entries']) <= (8 if arm == 'G' else 1000000)
            assert (d/'library.json').stat().st_size <= 1024**2
            information.add(tuple((x['query_id'], x['certificate_sha256']) for x in r['rows']))
            identities.add(r['library_sha256']); work.add(json.dumps(stable(r), sort_keys=True))
            update['acquisitions'][f'{repeat}-{arm}'] = {k: r[k] for k in
                ['library_path', 'library_sha256', 'library_serialized_bytes', 'object_ids',
                 'query_sha256', 'initial_entries', 'new_entries']}
            for p in sorted(d.rglob('*')):
                if p.is_file():
                    update['evidence_files'][str(p.relative_to(ROOT))] = file_hash(p)
        assert len(identities) == len(work) == 1, 'nonreproducible update '+arm
    assert len(information) == 1, 'C/G training information differs'
    if output.exists():
        old = read(output)
        assert {k: v for k, v in old.items() if k != 'frozen_utc'} == {
            k: v for k, v in update.items() if k != 'frozen_utc'}
    else:
        write_json(output, update)
    print(json.dumps(dict(freeze=str(output.relative_to(ROOT)), sha256=file_hash(output),
                          objects={a: len(update['acquisitions']['1-'+a]['object_ids']) for a in 'CG'})),
          flush=True)


def inherit_r2(output, source):
    parent = FIRST/'freeze-after-r2.json'
    prior = read(parent)
    evidence = {str(parent.relative_to(ROOT)): file_hash(parent)}
    for record in prior['acquisitions'].values():
        path = ROOT/record['library_path']
        assert file_hash(path) == record['library_sha256']
        evidence[record['library_path']] = file_hash(path)
    frozen = dict(schema=1, experiment='RP3-MR1-FINAL', rung='r2', usable_at='r3',
                  frozen_utc=now(), source_freeze_sha256=file_hash(source),
                  parent_freeze_sha256=file_hash(parent),
                  first_attempt_freeze_sha256=file_hash(FIRST/'freeze-after-r2.json'),
                  acquisitions=prior['acquisitions'], evidence_files=evidence)
    write_json(output, frozen)


def prepare(output):
    verify_contract()
    output.mkdir(parents=True, exist_ok=True)
    old = read(OLD/'source-freeze.json')
    for path, digest in {**old['driver_sources'], **old['inherited_rp2_files']}.items():
        assert file_hash(ROOT/path) == digest, path
    for path, digest in read(OLD/'freeze-after-r1.json')['evidence_files'].items():
        assert file_hash(ROOT/path) == digest, path
    first_source = FIRST/'source-freeze.json'
    first_execution = FIRST/'execution-complete.json'
    assert first_source.exists() and first_execution.exists()
    sources = [
        'pilot/src/rp3_durable_v2.py', 'pilot/src/rp3_recovery_run_v2.py',
        'pilot/src/rp3_recovery_measure_v2.py', 'pilot/src/rp3_recovery_campaign_v2.py',
        'pilot/tests/test_rp3_recovery.py', 'pilot/RP3_RECOVERY.md',
        'pilot/RP3_RECOVERY_V2.md']
    frozen = dict(old, experiment='RP3-MR1-FINAL', frozen_utc=now(),
                  original_source_freeze_sha256=file_hash(OLD/'source-freeze.json'),
                  first_attempt_source_freeze_sha256=file_hash(first_source),
                  first_attempt_execution_sha256=file_hash(first_execution),
                  amendment_sha256=file_hash(ROOT/'pilot/RP3_RECOVERY.md'),
                  rerun_amendment_sha256=file_hash(ROOT/'pilot/RP3_RECOVERY_V2.md'),
                  driver_sources={**old['driver_sources'], **{p: file_hash(ROOT/p) for p in sources}},
                  original_record_commit='6c37c4765d204362d16a2647625521e0fc6f740d',
                  original_local_commit='d1f75fff5a28c92921f889fa4ca87d566fba467d',
                  first_attempt_local_commit='6eaca9a',
                  original_raw_archive_sha256=file_hash(OLD/'raw-evidence.tar.gz'),
                  recovery_environment=dict(
                      python=sys.version, executable=sys.executable,
                      platform=platform.platform(),
                      cpu=next(l.split(':', 1)[1].strip() for l in Path('/proc/cpuinfo').read_text().splitlines()
                               if l.startswith('model name')),
                      affinity=sorted(os.sched_getaffinity(0)),
                      memory_max=Path('/sys/fs/cgroup/memory.max').read_text().strip(),
                      cpu_max=Path('/sys/fs/cgroup/cpu.max').read_text().strip(),
                      package_access='Preserved pinned chess through PYTHONPATH; no new installation',
                      limitation='New executable path and I/O safeguards; previous host load unavailable. '
                                 'R1 and original acquisitions retained without timing normalization.'),
                  measurement_access=dict(r2='previously inspected; balanced replacement rerun',
                                          r3='final rerun', r4='final rerun',
                                          counterplay_history='inaccessible'))
    source = output/'source-freeze.json'
    if source.exists():
        raise ValueError('freeze exists')
    write_json(source, frozen)
    inherit_r2(output/'freeze-after-r2.json', source)


def run(output, source, commit):
    frozen = read(source)
    assert subprocess.check_output(['git', 'show', commit+':'+str(source.relative_to(ROOT))],
                                   cwd=ROOT) == source.read_bytes()
    for path, digest in {**frozen['driver_sources'], **frozen['inherited_rp2_files']}.items():
        assert file_hash(ROOT/path) == digest, path
    assert file_hash(OLD/'raw-evidence.tar.gz') == frozen['original_raw_archive_sha256']
    for path, digest in read(output/'freeze-after-r2.json')['evidence_files'].items():
        assert file_hash(ROOT/path) == digest, path
    seqpath = output/'sequence.json'
    sequence = read(seqpath) if seqpath.exists() else []
    before_cpu, before_wall = time.process_time(), time.perf_counter()
    new_entries = []
    old_cpu = sum(e['cpu_s'] for e in read(OLD/'sequence.json'))
    first_cpu = sum(e['cpu_s'] for e in read(FIRST/'sequence.json')) if (FIRST/'sequence.json').exists() else 0
    current = output/'freeze-after-r2.json'

    def execute(mode, rung, arm, repeat, diagnostic='primary'):
        label = f'{mode}-{rung}-{diagnostic}-{repeat}-{arm}'
        directory = output/label
        if directory.exists():
            matches = [x for x in sequence if x['label'] == label]
            assert len(matches) == 1, 'unrecorded directory; preserve and stop'
            validate(directory, 24 if mode == 'acquire' else 16)
            env = read(directory/'envelope.json')
            assert env['returncode'] == matches[0]['returncode'] == 0
            assert all(env[u] == matches[0][u] for u in ['cpu_s', 'wall_s'])
            return
        command = [sys.executable, str(ROOT/'pilot/src/rp3_recovery_measure_v2.py'),
                   '--output', str(directory/'envelope.json'), '--', sys.executable,
                   str(ROOT/'pilot/src/rp3_recovery_run_v2.py'), mode, '--rung', rung,
                   '--arm', arm, '--repeat', str(repeat), '--diagnostic', diagnostic,
                   '--output', str(directory/'report.json'), '--freeze', str(current),
                   '--source-freeze', str(source)]
        proc = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
        env = read(directory/'envelope.json')
        entry = dict(label=label, command=command, returncode=proc.returncode,
                     cpu_s=env['cpu_s'], wall_s=env['wall_s'], recorded_utc=now())
        sequence.append(entry); new_entries.append(entry); write_json(seqpath, sequence)
        print(json.dumps(entry), flush=True)
        if proc.returncode:
            raise RuntimeError('Recorded failure; no selective rerun: '+label+' '+env['stderr'][-1500:])
        validate(directory, 24 if mode == 'acquire' else 16)
        if old_cpu + first_cpu + sum(e['cpu_s'] for e in sequence) > 4*3600:
            raise RuntimeError('RP3 CPU budget exhausted')
        if sum(p.stat().st_size for p in (ROOT/'pilot/evidence').rglob('*') if p.is_file()) > 1024**3:
            raise RuntimeError('disk budget exhausted')

    try:
        for repeat, order in enumerate(ORDERS, 1):
            for arm in order:
                execute('evaluate', 'r2', arm, repeat)
        for repeat, order in enumerate(ORDERS, 1):
            for arm in order:
                execute('evaluate', 'r3', arm, repeat)
        for repeat in [1, 2, 3]:
            execute('evaluate', 'r3', 'G', repeat, 'ablation')
        for repeat, order in enumerate(ORDERS, 1):
            for arm in order:
                execute('evaluate', 'r3', arm, repeat, 'reverse')
        for repeat, order in enumerate(ORDERS, 1):
            for arm in order:
                if arm in 'CG':
                    execute('acquire', 'r3', arm, repeat)
        freeze_update(output, 'r3', source, current, output/'freeze-after-r3.json')
        current = output/'freeze-after-r3.json'
        for repeat, order in enumerate(ORDERS, 1):
            for arm in order:
                execute('evaluate', 'r4', arm, repeat)
        for repeat in [1, 2, 3]:
            execute('evaluate', 'r4', 'G', repeat, 'ablation')
        for repeat, order in enumerate(ORDERS, 1):
            for arm in order:
                execute('evaluate', 'r4', arm, repeat, 'reverse')
        write_json(output/'execution-complete.json', dict(
            experiment='RP3-MR1-FINAL', status='COMPLETE', processes=len(sequence),
            final_freeze=str(current.relative_to(ROOT)), source_commit=commit, finished_utc=now()))
    finally:
        overhead = output/'orchestration.json'
        previous = read(overhead) if overhead.exists() else []
        previous.append(dict(cpu_s=time.process_time()-before_cpu,
                             wall_s=max(0, time.perf_counter()-before_wall-
                                       sum(e['wall_s'] for e in new_entries)),
                             note='Parent CPU and elapsed-wall residual only; child envelopes counted separately',
                             new_processes=len(new_entries)))
        write_json(overhead, previous)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['prepare', 'run'])
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--commit')
    args = parser.parse_args()
    args.output = args.output.resolve()
    if args.mode == 'prepare':
        prepare(args.output)
    else:
        if not args.commit:
            parser.error('published source commit required')
        run(args.output, args.output/'source-freeze.json', args.commit)


if __name__ == '__main__':
    main()
