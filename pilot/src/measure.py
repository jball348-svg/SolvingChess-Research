"""One process envelope, including interpreter startup, failures and timeouts."""
import argparse
import json
import os
from pathlib import Path
import resource
import signal
import subprocess
import time


def limits():
    capacity = 8*1024**3
    p = Path('/sys/fs/cgroup/memory.max')
    if p.exists() and p.read_text().strip().isdigit():
        used = Path('/sys/fs/cgroup/memory.current')
        capacity = min(capacity, int(p.read_text())-(int(used.read_text()) if used.exists() else 0))
    info = Path('/proc/meminfo')
    if info.exists():
        available = next(int(line.split()[1])*1024 for line in info.read_text().splitlines() if line.startswith('MemAvailable:'))
        capacity = min(capacity, available)
    memory = capacity//2
    hard = resource.getrlimit(resource.RLIMIT_AS)[1]
    if hard != resource.RLIM_INFINITY:
        memory = min(memory, hard)
    resource.setrlimit(resource.RLIMIT_AS, (memory, memory))
    resource.setrlimit(resource.RLIMIT_CPU, (300, 301))
    resource.setrlimit(resource.RLIMIT_FSIZE, (64*1024**2, 64*1024**2))
    if hasattr(os, 'sched_getaffinity'):
        os.sched_setaffinity(0, {min(os.sched_getaffinity(0))})


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('command', nargs=argparse.REMAINDER)
    a = p.parse_args()
    command = a.command[1:] if a.command and a.command[0] == '--' else a.command
    if not command:
        p.error('missing command')
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
    report = {'command': command, 'status': status, 'returncode': code,
              'wall_s': time.perf_counter()-start, 'cpu_s': usage.ru_utime+usage.ru_stime,
              'child_peak_rss_kib': usage.ru_maxrss, 'stdout': stdout, 'stderr': stderr}
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report))
    raise SystemExit(code if code is not None else 124)


if __name__ == '__main__':
    main()
