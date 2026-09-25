"""New RP1 implementation: exact bounded AND/OR search with a warm transposition table."""
from collections import Counter
import time
import chess
from model import advance, encoded, key, legal, terminal


class Limit(Exception):
    pass


class Solver:
    def __init__(self, arena, max_nodes=500_000, wall_seconds=120, library=None):
        self.arena = arena
        self.max_nodes = max_nodes
        self.deadline = time.perf_counter() + wall_seconds
        self.table = {}
        self.stats = Counter()
        self.library = library

    def solve(self, state, remaining):
        self.stats['calls'] += 1
        if time.perf_counter() > self.deadline:
            raise Limit('wall budget')
        k = key(state, self.arena, remaining)
        if k in self.table:
            self.stats['cache_hits'] += 1
            return k
        if len(self.table) >= self.max_nodes:
            raise Limit('table budget')
        self.stats['fresh_states'] += 1
        moves = legal(state, self.arena)
        self.stats['generated_edges'] += len(moves)
        end = terminal(state, self.arena, moves)
        if end is not None:
            return self.save(k, remaining, end[0], [], end[1])
        if remaining == 0:
            return self.save(k, remaining, False, [], 'horizon')
        # Optional proof lookup must return a checked concrete DAG, never a label.
        if self.library is not None:
            t = time.perf_counter()
            witness = self.library.lookup(state, self.arena, remaining, self.stats)
            self.stats['application_wall_s'] += time.perf_counter() - t
            if witness is not None:
                self.import_proof(witness)
                self.stats['proof_hits'] += 1
                return k
        self.stats['expanded_states'] += 1
        b = state.board
        # Conventional tactical ordering, shared by every arm; tie break is UCI.
        moves.sort(key=lambda m: (not b.is_capture(m), not b.gives_check(m), m.uci()))
        is_or = b.turn == chess.WHITE
        result = not is_or
        edges = []
        for m in moves:
            self.stats['examined_edges'] += 1
            ck = self.solve(advance(state, m, self.arena), remaining-1)
            value = self.table[ck]['result']
            edges.append([m.uci(), ck])
            if value == is_or:
                result = value
                edges = [[m.uci(), ck]]
                break
        return self.save(k, remaining, result, edges, None)

    def save(self, k, remaining, result, edges, leaf):
        if len(self.table) >= self.max_nodes:
            raise Limit('table budget')
        self.table[k] = {'remaining': remaining, 'result': result, 'edges': edges, 'leaf': leaf}
        return k

    def certificate(self, root):
        nodes = {}
        indices = {}

        def visit(k):
            if k in indices:
                return indices[k]
            identifier = str(len(indices))
            indices[k] = identifier
            node = self.table[k]
            edges = [[m, visit(child)] for m, child in node['edges']]
            nodes[identifier] = dict(node, edges=edges, state_key=k)
            return identifier

        rid = visit(root)
        return {'schema': 1, 'arena': self.arena.spec(), 'root': rid, 'nodes': nodes}

    def import_proof(self, proof):
        if len(self.table) + len(proof['nodes']) > self.max_nodes:
            raise Limit('table budget during proof import')
        for n in proof['nodes'].values():
            self.table[n['state_key']] = {k: v for k, v in n.items() if k != 'state_key'}
            self.table[n['state_key']]['edges'] = [[m, proof['nodes'][c]['state_key']] for m, c in n['edges']]

    def serialized_table_bytes(self):
        return len(encoded(self.table).encode())
