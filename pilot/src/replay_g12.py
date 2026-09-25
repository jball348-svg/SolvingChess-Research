"""Replay frozen source in an isolated directory; never execute in the archive."""
import argparse
import hashlib
import json
import pathlib
import platform
import resource
import subprocess
import tempfile
import time
import zipfile

ROOT = pathlib.Path(__file__).resolve().parents[2]
BUNDLE = ROOT / 'archive/pre-reboot-2026-09-25/legacy/originals/G12_Final_Rules_Reference_Bundle.zip'
EXPECTED = '7641e0f8a4e621efb90b75cd3ce99b44e96c07a2f3541114611126a076d5695c'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=pathlib.Path, required=True)
    args = parser.parse_args()
    assert digest(BUNDLE.read_bytes()) == EXPECTED
    report = {'bundle_sha256': EXPECTED,
              'source_commit': '3eba1a0c60e8ffca63a85763d176e1da9f904141',
              'platform': platform.platform(), 'steps': []}
    with tempfile.TemporaryDirectory(prefix='rp1-g12-') as tmp:
        work = pathlib.Path(tmp)
        with zipfile.ZipFile(BUNDLE) as z:
            z.extractall(work / 'frozen')
        (work / 'replayed').mkdir()
        report['source_sha256'] = {n: digest((work/'frozen'/n).read_bytes())
                                  for n in ['g12_suite.cpp', 'g12_verifier.cpp']}
        for source, executable in [('g12_suite.cpp', 'producer'), ('g12_verifier.cpp', 'verifier')]:
            command = ['g++', '-O3', '-std=c++20', str(work/'frozen'/source), '-o', str(work/executable)]
            run(command, work, report)
        run([str(work/'producer'), str(work/'replayed')], work, report)
        run([str(work/'verifier'), str(work/'replayed')], work, report)
        report['artifacts'] = {}
        for path in sorted((work/'replayed').iterdir()):
            data = path.read_bytes()
            identical = data == (work/'frozen'/path.name).read_bytes()
            report['artifacts'][path.name] = {'bytes': len(data), 'sha256': digest(data), 'matches_frozen': identical}
            assert identical, path.name
        report['arena'] = json.loads((work/'replayed/G12_Arena_Ledger.json').read_text())
        report['verification'] = json.loads((work/'replayed/G12_Verification_Ledger.json').read_text())
        report['history_controls'] = json.loads((work/'replayed/G12_History_Rules_Ledger.json').read_text())
    report['verdict'] = 'PASS'
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'verdict': report['verdict'], 'output': str(args.output), 'steps': report['steps']}))


def run(command, work, report):
    before = resource.getrusage(resource.RUSAGE_CHILDREN)
    start = time.perf_counter()
    proc = subprocess.run(command, capture_output=True, text=True, timeout=600)
    after = resource.getrusage(resource.RUSAGE_CHILDREN)
    report['steps'].append({'command': [s.replace(str(work), '$WORK') for s in command],
                            'wall_s': time.perf_counter()-start,
                            'cpu_s': after.ru_utime+after.ru_stime-before.ru_utime-before.ru_stime,
                            'cumulative_child_peak_rss_kib': after.ru_maxrss,
                            'returncode': proc.returncode, 'stdout': proc.stdout, 'stderr': proc.stderr})
    if proc.returncode:
        raise RuntimeError(report['steps'][-1])


if __name__ == '__main__':
    main()
