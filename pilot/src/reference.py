"""Complete development-arena layer DP; additional reference, not the primary baseline."""
import itertools
import chess
from model import advance, legal, repetition_key, start, terminal


def full_arena(arena, plies):
    if arena.history:
        raise ValueError('board-only reference does not quotient histories')
    squares = [s for s in chess.SQUARES if arena.contains(s)]
    graph = {}
    edges = 0
    for wk, rook, bk in itertools.permutations(squares, 3):
        for turn in (chess.WHITE, chess.BLACK):
            b = chess.Board(None)
            for sq, piece in ((wk, 'K'), (rook, 'R'), (bk, 'k')):
                b.set_piece_at(sq, chess.Piece.from_symbol(piece))
            b.turn = turn
            if not b.is_valid():
                continue
            state = start(b.fen(), arena)
            moves = legal(state, arena)
            end = terminal(state, arena, moves)
            children = [repetition_key(advance(state, m, arena).board) for m in moves]
            graph[repetition_key(b)] = (turn, None if end is None else end[0], children)
            edges += len(children)
    truth = {k: end is True for k, (_, end, _) in graph.items()}
    scans = 0
    for _ in range(plies):
        after = {}
        for k, (turn, end, children) in graph.items():
            if end is not None:
                after[k] = end
                continue
            # All exits are capture of White's only rook: exact bare-king failure.
            values = [truth.get(c, False) for c in children]
            scans += len(children)
            after[k] = any(values) if turn else all(values)
        truth = after
    return truth, {'states': len(graph), 'graph_edges': edges, 'layer_edge_scans': scans,
                   'plies': plies, 'white_bounded_mates': sum(truth.values())}
