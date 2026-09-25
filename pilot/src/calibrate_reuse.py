"""Measure the checking/application seam on a synthetic known control, not discovery."""
import argparse
from collections import Counter
import copy
import json
from pathlib import Path
import resource
from checker import check
from model import Arena, encoded, start
from reuse import Library, compile_template
from run_smoke import measured
from solver import Solver


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    arena = Arena(3, 4)
    state = start('8/8/8/8/2k5/8/K7/1R6 w - - 0 1', arena)
    solver = Solver(arena)
    root, search = measured(lambda: solver.solve(state, 4))
    proof, emit = measured(lambda: solver.certificate(root))
    audit, verification = measured(lambda: check(proof, state, arena, 4, expected=True))
    template, construction = measured(lambda: compile_template(proof, state, arena, 4))
    payload, serialization = measured(lambda: encoded([template]))
    library, loading = measured(lambda: Library(json.loads(payload)))
    stats = Counter()
    concrete, application = measured(lambda: library.lookup(state, arena, 4, stats))
    assert concrete is not None
    bad = copy.deepcopy(template)
    bad['nodes'][bad['root']]['used'] = 99
    rejected = Counter()
    failed, failed_cost = measured(lambda: Library([bad]).lookup(state, arena, 4, rejected))
    assert failed is None
    report = {'scope': 'known synthetic control only; no donor/evaluation discovery',
              'fen': state.board.fen(), 'arena': arena.spec(), 'plies': 4,
              'baseline_search': search, 'baseline_counts': dict(solver.stats),
              'proof_emit': emit, 'verification': dict(verification, audit=audit),
              'template_construction': construction, 'library_serialization': serialization,
              'library_loading_and_index': loading, 'application_including_checker': application,
              'application_counts': dict(stats), 'deliberate_rejection': failed_cost,
              'rejection_counts': dict(rejected), 'serialized_library_bytes': len(payload.encode()),
              'process_peak_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
              'status': 'PASS'}
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({'status': 'PASS', 'library_bytes': report['serialized_library_bytes'],
                      'application_counts': dict(stats), 'rejection_counts': dict(rejected)}))


if __name__ == '__main__':
    main()
