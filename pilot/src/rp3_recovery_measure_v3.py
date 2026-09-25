"""Immutable-generation fresh-process limits/envelope, with atomic durable envelope storage."""
import argparse
import json
import os
from pathlib import Path
import resource
import signal
import subprocess
import time
from measure import limits
from rp3_durable_v3 import write_json


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('command', nargs=argparse.REMAINDER)
    a = p.parse_args()
    command = a.command[1:] if a.command and a.command[0] == '--' else a.command
    if not command or a.output.exists():
        p.error('command required; refusing existing envelope')
    start = time.perf_counter()
    process = subprocess.Popen(command, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               preexec_fn=limits, start_new_session=True)
    try:
        stdout, stderr = process.communicate(timeout=600)
        code, status = process.returncode, 'COMPLETED'
    except subprocess.TimeoutExpired:
        os.killpg(process.pid, signal.SIGKILL)
        stdout, stderr = process.communicate()
        code, status = None, 'WALL_LIMIT'
    usage = resource.getrusage(resource.RUSAGE_CHILDREN)
    report = dict(command=command, status=status, returncode=code,
                  wall_s=time.perf_counter()-start, cpu_s=usage.ru_utime+usage.ru_stime,
                  child_peak_rss_kib=usage.ru_maxrss, stdout=stdout, stderr=stderr)
    write_json(a.output, report)
    print(json.dumps(report))
    raise SystemExit(code if code is not None else 124)


if __name__ == '__main__':
    main()
