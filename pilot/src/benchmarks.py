"""Prospectively fixed generators. Importing does not enumerate or solve a benchmark."""
import heapq
import itertools
import chess
from model import Arena, advance, encoded, legal, sha, start, terminal

SEED = 'RP1-2026-09-25-v1'
HORIZON = 6
DOMAINS = {'dev': (3, 4), 'r1': (3, 5), 'r2': (4, 5), 'r3': (4, 6), 'r4': (5, 6),
           'counterplay': (5, 6), 'history': (4, 5)}


def positions(arena, pawn=False):
    squares = [s for s in chess.SQUARES if arena.contains(s)]
    for wk, rook, bk in itertools.permutations(squares, 3):
        pawns = [s for s in squares if s not in (wk, rook, bk) and 1 <= chess.square_rank(s) < arena.height-1] if pawn else [None]
        for ps in pawns:
            for turn in (chess.WHITE, chess.BLACK):
                b = chess.Board(None)
                for square, piece in ((wk, 'K'), (rook, 'R'), (bk, 'k')):
                    b.set_piece_at(square, chess.Piece.from_symbol(piece))
                if ps is not None:
                    b.set_piece_at(ps, chess.Piece.from_symbol('p'))
                b.turn = turn
                if not b.is_valid():
                    continue
                state = start(b.fen(), arena)
                if terminal(state, arena, legal(state, arena)) is not None:
                    continue
                yield {'fen': b.fen(), 'moves': []}


def partition(query):
    # Disjoint roles within each arena; rejection never depends on bounded truth.
    value = int(sha([SEED, 'partition', query])[:8], 16) % 8
    return 'smoke' if value == 0 else 'test' if value == 1 else 'train'


def cohort(name, role, per_side=8):
    """Reservoir via smallest fixed SHA priorities; no outcomes consulted."""
    arena = Arena(*DOMAINS[name], history=name == 'history')
    if name == 'history':
        raise ValueError('use history_cohort for explicit histories')
    picked = []
    for turn in ('w', 'b'):
        eligible = (q for q in positions(arena, pawn=name == 'counterplay')
                    if q['fen'].split()[1] == turn and partition(q) == role)
        order = lambda q: sha([SEED, name, role, q])
        selected = heapq.nsmallest(per_side, eligible, key=order)
        if len(selected) != per_side:
            raise ValueError('insufficient query population')
        picked.extend(selected)
    picked.sort(key=lambda q: sha([SEED, name, role, q]))
    return arena, [dict(q, id=sha([name, role, q])[:16]) for q in picked]


def history_cohort():
    # Fixed, outcome-blind 16-query stress: 4 clocks 0, 4 clocks 98,
    # 4 one-cycle histories, 4 two-cycle histories. Board placements may overlap
    # main r2; these are paired history stresses, not unseen board claims.
    base_arena, roots = cohort('r2', 'test')
    arena = Arena(*DOMAINS['history'], history=True)
    out = []
    for clock in (0, 98):
        for q in roots[:4]:
            parts = q['fen'].split()
            parts[4] = str(clock)
            item = {'fen': ' '.join(parts), 'moves': []}
            out.append(dict(item, id=sha(['history', item])[:16]))
    cycles = []
    # Enumeration is legal-move generation, not evaluation; run only in RP4.
    candidates = sorted(positions(base_arena), key=lambda q: sha([SEED, 'cycles', q]))
    for q in candidates:
        state = start(q['fen'], base_arena)
        target = state.board.board_fen(), state.board.turn

        def cycle(s, path):
            if len(path) == 4:
                return path if (s.board.board_fen(), s.board.turn) == target else None
            if terminal(s, base_arena, legal(s, base_arena)) is not None:
                return None
            for m in sorted(legal(s, base_arena), key=lambda m: m.uci()):
                if s.board.is_capture(m):
                    continue
                found = cycle(advance(s, m, base_arena), path+[m.uci()])
                if found is not None:
                    return found
            return None

        path = cycle(state, [])
        if path:
            cycles.append((q, path))
        if len(cycles) == 4:
            break
    if len(cycles) != 4:
        raise ValueError('four legal cycle anchors unavailable')
    for count in (1, 2):
        for q, path in cycles:
            item = {'fen': q['fen'], 'moves': path*count}
            out.append(dict(item, id=sha(['history', item])[:16]))
    return arena, out
