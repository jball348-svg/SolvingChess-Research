"""New wiring controls use existing RP1 fixtures only; no reserved cohorts."""
from collections import Counter
import copy
import sys
from pathlib import Path
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'src'))
import checker
import reuse
from model import Arena, sha, start
from solver import Solver
from rp2_support import (Meter, ProofLibrary, GeometryCache, breadth_first,
                         cache_instantiate, geometry_id, state_at, subproof)


class RP2Checks(unittest.TestCase):
    def setUp(self):
        self.arena = Arena(3, 4)
        self.state = start('8/8/8/8/2k5/8/K7/1R6 w - - 0 1', self.arena)
        self.meter = Meter()
        self.original_check = reuse.check
        reuse.check = self.meter.check
        self.solver = Solver(self.arena)
        self.proof = self.solver.certificate(self.solver.solve(self.state, 4))

    def tearDown(self):
        reuse.check = self.original_check

    def test_instrumented_library_same_witness(self):
        template = reuse.compile_template(self.proof, self.state, self.arena, 4)
        plain = reuse.Library([template]).lookup(self.state, self.arena, 4, Counter())
        events = []
        observed = ProofLibrary([template], self.meter, events.append)
        measured = observed.lookup(self.state, self.arena, 4, Counter())
        self.assertEqual(plain, measured)
        self.assertGreaterEqual(observed.cost['cpu_s'], 0)  # May quantize to zero.
        self.assertGreater(observed.cost['wall_s'], 0)
        self.assertEqual(events[-1]['status'], 'ACCEPTED')
        observed.lookup(self.state, self.arena, 0, Counter())
        self.assertEqual(events[-1]['status'], 'DEPTH_GUARD')

    def test_failed_checker_work_retained(self):
        proof = copy.deepcopy(self.proof)
        proof['nodes'][proof['root']].update(leaf='mate', edges=[])
        with self.assertRaises(ValueError):
            self.meter.check(proof, self.state, self.arena, 4)
        self.assertEqual(self.meter.audits['rejected'], 1)
        self.assertGreater(self.meter.audits['checked_nodes'], 0)
        self.assertGreater(self.meter.audits['generated_edges'], 0)

    def test_bfs_subproofs_check(self):
        for identifier in breadth_first(self.proof):
            concrete = subproof(self.proof, identifier)
            state, depth = state_at(concrete, identifier)
            self.assertTrue(checker.check(concrete, state, self.arena, depth)['result'])

    def test_generic_cache_both_truths_and_symmetry(self):
        reflected = start('8/8/8/8/k7/8/2K5/1R6 w - - 0 1', self.arena)
        self.assertEqual(geometry_id(self.state), geometry_id(reflected))
        for depth, expected in ((4, True), (1, False)):
            proof = self.solver.certificate(self.solver.solve(self.state, depth))
            entry = dict(id=sha(proof), key=reuse.cache_geometry(self.state, self.arena, depth), proof=proof)
            cache = GeometryCache([entry], self.meter, lambda e: None)
            for state in (self.state, reflected):
                result = cache.lookup(state, self.arena, depth, Counter())
                self.assertIsNotNone(result)
                self.assertEqual(checker.check(result, state, self.arena, depth)['result'], expected)
            self.assertIsNone(cache.lookup(self.state, Arena(3, 5), depth, Counter()))
            damaged = copy.deepcopy(entry)
            damaged['proof']['nodes'][proof['root']]['remaining'] += 1
            with self.assertRaises(ValueError):
                cache_instantiate(damaged, reflected, self.arena, depth, self.meter.check)


if __name__ == '__main__':
    unittest.main()
