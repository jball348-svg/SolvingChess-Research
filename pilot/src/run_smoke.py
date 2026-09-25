"""RP1-only calibration command. Does not generate later evaluation cohorts."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import platform
import resource
import sys
import time
import chess
from benchmarks import cohort, HORIZON
from checker import check
from model import WORK, encoded, query_state, repetition_key
from reference import full_arena
from solver import Limit, Solver


def measured(call):
    before = WORK.copy()
    cpu = time.process_time()
    wall = time.perf_counter()
    try:
        value = call()
    except Exception as exc:
        exc.measurement = {'cpu_s': time.process_time()-cpu, 'wall_s': time.perf_counter()-wall,
                           'work': dict(WORK-before)}
        raise
    return value, {'cpu_s': time.process_time()-cpu, 'wall_s': time.perf_counter()-wall,
                   'work': dict(WORK-before)}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--certificate', type=Path)
    a = p.parse_args()
    # Enforce process ceilings in addition to the measured search deadline.
    from measure import limits
    limits()
    begin = time.perf_counter()
    cpu_begin = time.process_time()
    (arena, queries), generation = measured(lambda: cohort('dev', 'smoke', per_side=4))
    (truth, reference_summary), reference_cost = measured(lambda: full_arena(arena, HORIZON))
    report = {'schema': 1, 'scope': 'RP1-development-only', 'python': sys.version,
              'chess': chess.__version__, 'platform': platform.platform(), 'arena': arena.spec(),
              'plies': HORIZON, 'query_sha256': hashlib.sha256(encoded(queries).encode()).hexdigest(),
              'queries': queries, 'shared_query_generation': generation,
              'full_arena_reference': dict(reference_summary, cost=reference_cost),
              'unrun_phases': ['discovery', 'dependency_construction', 'template_application', 'engine_calls'],
              'rows': []}
    solver = Solver(arena)
    witness_written = False
    for pass_name in ('cold_sequence', 'warm_repeat'):
        for q in queries:
            row = {'query_id': q['id'], 'pass': pass_name}
            report['rows'].append(row)
            state, row['load'] = measured(lambda: query_state(q, arena))
            before = solver.stats.copy()
            try:
                root, row['search'] = measured(lambda: solver.solve(state, HORIZON))
                proof, row['proof_emit'] = measured(lambda: solver.certificate(root))
                payload, row['serialize'] = measured(lambda: encoded(proof).encode())
                loaded, row['proof_load'] = measured(lambda: json.loads(payload))
                audit, row['verification'] = measured(lambda: check(loaded, state, arena, HORIZON))
                row['verification'].update(audit)
                assert audit['result'] == truth[repetition_key(state.board)], 'DP/search discrepancy'
                row.update(status='EXACT', result=audit['result'], certificate_bytes=len(payload),
                           certificate_sha256=hashlib.sha256(payload).hexdigest())
                if a.certificate and audit['result'] and not witness_written:
                    a.certificate.parent.mkdir(parents=True, exist_ok=True)
                    a.certificate.write_text(json.dumps({'query': q, 'plies': HORIZON, 'proof': loaded}, indent=2)+'\n')
                    witness_written = True
            except Limit as exc:
                row.update(status='LIMIT', reason=str(exc), failed_phase_cost=exc.measurement)
            row['search_counts'] = dict(solver.stats-before)
            row['table_entries'] = len(solver.table)
            # Incremental durable row checkpoint, including unsuccessful queries.
            a.output.parent.mkdir(parents=True, exist_ok=True)
            a.output.write_text(json.dumps(report, indent=2)+'\n')
    table_bytes, byte_cost = measured(solver.serialized_table_bytes)
    report['table_serialized_bytes'] = table_bytes
    report['table_byte_measurement'] = byte_cost
    report['total_wall_s'] = time.perf_counter()-begin
    report['total_cpu_s'] = time.process_time()-cpu_begin
    report['process_peak_rss_kib'] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    report['status'] = 'PASS' if all(r['status'] == 'EXACT' for r in report['rows']) else 'LIMIT'
    a.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({k: report[k] for k in ['status', 'total_cpu_s', 'total_wall_s', 'process_peak_rss_kib', 'table_serialized_bytes']}))


if __name__ == '__main__':
    main()
