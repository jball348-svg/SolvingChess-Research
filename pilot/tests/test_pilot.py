"""Soundness and seam controls only; no reserved discovery/evaluation queries."""
import copy
import json
from pathlib import Path
import sys
import unittest
from collections import Counter
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
import chess
from model import Arena, advance, key, legal, query_state, start, terminal
from solver import Solver
from checker import check
from reuse import Library, cache_geometry, compile_template, instantiate, TRANSFORMS


class PilotChecks(unittest.TestCase):
    def setUp(self):
        self.arena = Arena(3, 4)
        self.state = start('8/8/8/8/2k5/8/K7/1R6 w - - 0 1', self.arena)
        self.solver = Solver(self.arena)
        root = self.solver.solve(self.state, 4)
        self.proof = self.solver.certificate(root)

    def test_known_move_generation(self):
        # Standard initial-position perft 1/2, underlying rules dependency control.
        b = chess.Board()
        self.assertEqual(len(list(b.legal_moves)), 20)
        count = 0
        for m in list(b.legal_moves):
            b.push(m)
            count += len(list(b.legal_moves))
            b.pop()
        self.assertEqual(count, 400)
        self.assertTrue(all(self.arena.contains(m.to_square) for m in legal(self.state, self.arena)))

    def test_positive_and_warm_cache(self):
        self.assertTrue(check(self.proof, self.state, self.arena, 4)['result'])
        before = self.solver.stats['expanded_states']
        self.solver.solve(self.state, 4)
        self.assertEqual(before, self.solver.stats['expanded_states'])

    def test_dual_bounded_failure(self):
        root = self.solver.solve(self.state, 1)
        proof = self.solver.certificate(root)
        self.assertFalse(check(proof, self.state, self.arena, 1)['result'])
        self.assertEqual(len(proof['nodes'][proof['root']]['edges']), len(legal(self.state, self.arena)))

    def test_missing_opponent_reply_rejected(self):
        # Already observed development smoke fixture; two legal Black replies.
        state = start('8/8/8/8/8/KRk5/8/8 b - - 0 1', self.arena)
        solver = Solver(self.arena)
        proof = solver.certificate(solver.solve(state, 6))
        check(proof, state, self.arena, 6, expected=True)
        candidates = [n for n in proof['nodes'].values() if len(n['edges']) >= 2]
        self.assertTrue(candidates, 'control must contain a nontrivial all-reply obligation')
        candidates[0]['edges'].pop()
        with self.assertRaises(ValueError):
            check(proof, state, self.arena, 6)

    def test_false_target_rejected(self):
        proof = copy.deepcopy(self.proof)
        root = proof['nodes'][proof['root']]
        root.update(leaf='mate', edges=[])
        with self.assertRaises(ValueError):
            check(proof, self.state, self.arena, 4)

    def test_progress_and_cycle_rejected(self):
        proof = copy.deepcopy(self.proof)
        proof['nodes'][proof['root']]['remaining'] += 1
        with self.assertRaises(ValueError):
            check(proof, self.state, self.arena, 4)
        proof = copy.deepcopy(self.proof)
        proof['nodes'][proof['root']]['edges'][0][1] = proof['root']
        with self.assertRaises(ValueError):
            check(proof, self.state, self.arena, 4)

    def test_clock_and_history_identity(self):
        arena = Arena(8, 8, True)
        clean = start('8/8/8/8/8/8/8/QK1k4 b - - 0 1', arena)
        clock = start('8/8/8/8/8/8/8/QK1k4 b - - 100 1', arena)
        self.assertIsNone(terminal(clean, arena, legal(clean, arena)))
        self.assertEqual(terminal(clock, arena, legal(clock, arena)), (False, 'claim_now'))
        self.assertNotEqual(key(clean, arena, 6), key(clock, arena, 6))
        intended = start('8/8/8/8/8/8/8/QK1k4 b - - 99 1', arena)
        self.assertEqual(terminal(intended, arena, legal(intended, arena)), (False, 'claim_by_move'))

    def test_legal_repetition_history(self):
        arena = Arena(3, 4, True)
        q = {'fen': '8/8/8/8/2k5/8/8/KR6 w - - 0 1',
             'moves': ['b1b2', 'c4c3', 'b2b1', 'c3c4']*4}
        state = query_state(q, arena)
        self.assertEqual(terminal(state, arena, legal(state, arena)), (False, 'automatic_draw'))
        broken = dict(q, moves=q['moves']+['b1b2'])
        with self.assertRaises(ValueError):
            query_state(broken, arena)

    def test_history_quotient_rejected(self):
        arena = Arena(3, 4, True)
        state = start(self.state.board.fen(), arena)
        with self.assertRaises(ValueError):
            check(self.proof, state, arena, 4)
        solver = Solver(arena)
        proof = solver.certificate(solver.solve(state, 4))
        state.counts[next(iter(state.counts))] += 1
        with self.assertRaises(ValueError):
            check(proof, state, arena, 4)

    def test_mate_precedes_automatic_clock_draw(self):
        arena = Arena(8, 8, True)
        state = start('7k/5Q2/7K/8/8/8/8/8 w - - 149 1', arena)
        move = chess.Move.from_uci('f7g7')
        self.assertIn(move, legal(state, arena))
        child = advance(state, move, arena)
        self.assertEqual(child.board.halfmove_clock, 150)
        self.assertEqual(terminal(child, arena, legal(child, arena)), (True, 'mate'))

    def test_lower_material_capture(self):
        state = start('8/8/8/8/2k5/1R6/8/K7 b - - 0 1', self.arena)
        move = chess.Move.from_uci('c4b3')
        self.assertIn(move, legal(state, self.arena))
        child = advance(state, move, self.arena)
        self.assertEqual(terminal(child, self.arena, legal(child, self.arena)), (False, 'bare_white_king'))

    def test_template_seam_known_control_only(self):
        template = compile_template(self.proof, self.state, self.arena, 4)
        library = Library([template])
        solver = Solver(self.arena, library=library)
        proof = solver.certificate(solver.solve(self.state, 4))
        self.assertTrue(check(proof, self.state, self.arena, 4)['result'])
        self.assertEqual(solver.stats['proof_hits'], 1)
        self.assertEqual(solver.stats['expanded_states'], 0)
        # Use the actual proof height, so a proof found under a larger horizon
        # remains usable after a capture has spent some of the query's budget.
        short = Solver(self.arena, library=library)
        root = short.solve(self.state, template['plies'])
        self.assertTrue(check(short.certificate(root), self.state, self.arena, template['plies'])['result'])
        self.assertEqual(short.stats['proof_hits'], 1)
        # Corrupt rank data must never become a cacheable answer.
        corrupt = copy.deepcopy(template)
        corrupt['nodes'][corrupt['root']]['used'] = 99
        bad = Library([corrupt])
        stats = Counter()
        self.assertIsNone(bad.lookup(self.state, self.arena, 4, stats))
        self.assertGreater(stats['template_rejections'], 0)

    def test_cache_keeps_domain(self):
        self.assertNotEqual(cache_geometry(self.state, self.arena, 4),
                            cache_geometry(self.state, Arena(4, 4), 4))

    def test_illegal_history_and_rights_rejected(self):
        with self.assertRaises(ValueError):
            start(chess.STARTING_FEN, Arena(8, 8))
        with self.assertRaises(ValueError):
            query_state({'fen': self.state.board.fen(), 'moves': ['b1h8']}, self.arena)


if __name__ == '__main__':
    unittest.main()
