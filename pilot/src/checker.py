"""Certificate traversal independent of the search implementation.

Shares model.py and python-chess, so this is not an independent chess rules proof.
Checks both positive AND/OR strategies and dual certificates of bounded failure.
"""
import chess
from model import advance, key, legal, terminal


def check(proof, state, arena, remaining, expected=None):
    if proof.get('schema') != 1 or proof.get('arena') != arena.spec():
        raise ValueError('certificate semantic domain mismatch')
    seen = {}
    counts = {'checked_nodes': 0, 'checked_edges': 0, 'generated_edges': 0}

    def visit(identifier, position, depth):
        k = key(position, arena, depth)
        if identifier in seen:
            if seen[identifier] != k:
                raise ValueError('invalid state/history merge or circular witness')
            return proof['nodes'][identifier]['result']
        node = proof['nodes'][identifier]
        if type(node['result']) is not bool or node['remaining'] != depth or node['state_key'] != k:
            raise ValueError('invalid state, history or progress witness')
        seen[identifier] = k
        counts['checked_nodes'] += 1
        moves = {m.uci(): m for m in legal(position, arena)}
        counts['generated_edges'] += len(moves)
        end = terminal(position, arena, list(moves.values()))
        if end is None and depth == 0:
            end = (False, 'horizon')
        if end is not None:
            if node['result'] != end[0] or node['leaf'] != end[1] or node['edges']:
                raise ValueError('false terminal/target')
            return node['result']
        if node['leaf'] is not None:
            raise ValueError('false target at nonterminal')
        edges = node['edges']
        labels = [m for m, _ in edges]
        if len(labels) != len(set(labels)) or not set(labels).issubset(moves):
            raise ValueError('duplicate or illegal move')
        # OR-true / AND-false choose a witness; OR-false / AND-true need all replies.
        existential = node['result'] == (position.board.turn == chess.WHITE)
        if existential:
            if len(edges) != 1:
                raise ValueError('missing admitted choice')
        elif set(labels) != set(moves):
            raise ValueError('missing legal reply')
        for uci, child in edges:
            counts['checked_edges'] += 1
            if visit(child, advance(position, moves[uci], arena), depth-1) != node['result']:
                raise ValueError('false Bellman witness')
        return node['result']

    value = visit(proof['root'], state, remaining)
    if len(seen) != len(proof['nodes']):
        raise ValueError('unreachable certificate baggage')
    if expected is not None and value != expected:
        raise ValueError('wrong proposition')
    return dict(counts, result=value)


if __name__ == '__main__':
    import argparse
    import json
    from pathlib import Path
    from model import Arena, query_state
    p = argparse.ArgumentParser()
    p.add_argument('certificate', type=Path)
    a = p.parse_args()
    record = json.loads(a.certificate.read_text())
    arena = Arena(**record['proof']['arena'])
    print(json.dumps(check(record['proof'], query_state(record['query'], arena), arena, record['plies'])))
