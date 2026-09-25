"""Serial RP2 repetition runner. Acquisition and evaluation are separate commands."""
import argparse
import json
from pathlib import Path
import subprocess
import sys


def main():
    p = argparse.ArgumentParser()
    p.add_argument('phase', choices=['acquire', 'evaluate'])
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--freeze', type=Path)
    p.add_argument('--freeze-commit')
    a = p.parse_args()
    if a.phase == 'evaluate' and (not a.freeze or not a.freeze_commit):
        p.error('evaluation requires the previously published freeze')
    a.output.mkdir(parents=True, exist_ok=True)
    sequence = []
    cpu = 0.0
    arms = ['B', 'C', 'F', 'G']
    for repeat in range(1, 4):
        order = arms[repeat-1:]+arms[:repeat-1]
        for arm in order:
            if a.phase == 'acquire' and arm == 'B':
                continue
            label = f'{a.phase}-{repeat}-{arm}'
            directory = a.output/label
            if directory.exists():
                raise RuntimeError('refusing to overwrite an existing run: '+str(directory))
            command = [sys.executable, 'pilot/src/measure.py', '--output', str(directory/'envelope.json'),
                       '--', sys.executable, 'pilot/src/rp2.py', a.phase, '--arm', arm,
                       '--repeat', str(repeat), '--output', str(directory/'report.json')]
            if a.phase == 'evaluate':
                command += ['--freeze', str(a.freeze), '--freeze-commit', a.freeze_commit]
            process = subprocess.run(command, text=True, capture_output=True)
            envelope = json.loads((directory/'envelope.json').read_text())
            cpu += envelope['cpu_s']
            sequence.append(dict(label=label, command=command, returncode=process.returncode,
                                 cpu_s=envelope['cpu_s'], wall_s=envelope['wall_s']))
            (a.output/(a.phase+'-sequence.json')).write_text(json.dumps(sequence, indent=2)+'\n')
            print(json.dumps(sequence[-1]), flush=True)
            if process.returncode:
                print(envelope.get('stderr', ''), file=sys.stderr)
                raise SystemExit(process.returncode)
            if cpu > 4*3600:
                raise RuntimeError('part CPU budget exhausted')


if __name__ == '__main__':
    main()
