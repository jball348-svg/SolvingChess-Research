"""RP1 rectangular chess laboratory, not an implementation of unrestricted chess."""
from dataclasses import dataclass
from collections import Counter
import hashlib
import json
import chess

WORK = Counter()


def encoded(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'))


def sha(obj):
    return hashlib.sha256(encoded(obj).encode()).hexdigest()


@dataclass(frozen=True)
class Arena:
    width: int
    height: int
    history: bool = False

    def __post_init__(self):
        if not (3 <= self.width <= 8 and 3 <= self.height <= 8):
            raise ValueError('unsupported rectangle')

    def contains(self, square):
        return chess.square_file(square) < self.width and chess.square_rank(square) < self.height

    def spec(self):
        return {'width': self.width, 'height': self.height, 'history': self.history}


def repetition_key(board):
    # Rights are absent in this experiment; retain them defensively in the key.
    return ' '.join(board.fen(en_passant='legal').split()[:4])


@dataclass
class State:
    board: chess.Board
    counts: dict


def start(fen, arena):
    board = chess.Board(fen)
    if not board.is_valid() or board.castling_rights or board.ep_square is not None:
        raise ValueError('invalid root or unsupported special rights')
    if any(not arena.contains(s) for s in board.piece_map()):
        raise ValueError('piece outside rectangle')
    return State(board, {repetition_key(board): 1} if arena.history else {})


def legal(state, arena):
    moves = [m for m in state.board.legal_moves if arena.contains(m.to_square)]
    WORK['move_generation_calls'] += 1
    WORK['legal_edges_generated'] += len(moves)
    return moves


def advance(state, move, arena):
    WORK['transitions'] += 1
    board = state.board.copy(stack=False)
    board.push(move)
    counts = state.counts.copy() if arena.history else {}
    if arena.history:
        key = repetition_key(board)
        counts[key] = counts.get(key, 0) + 1
    return State(board, counts)


def terminal(state, arena, moves):
    """Return (White forces bounded mate?, reason), or None before the horizon."""
    b = state.board
    if not moves:
        return (b.turn == chess.BLACK and b.is_check(), 'mate' if b.is_check() else 'stalemate')
    # A bare White king cannot check a legally separated opposing king.
    if b.occupied_co[chess.WHITE] == b.kings & b.occupied_co[chess.WHITE]:
        return False, 'bare_white_king'
    if arena.history:
        n = state.counts[repetition_key(b)]
        if b.halfmove_clock >= 150 or n >= 5:
            return False, 'automatic_draw'
        if b.turn == chess.BLACK:
            if b.halfmove_clock >= 100 or n >= 3:
                return False, 'claim_now'
            for m in moves:
                child = advance(state, m, arena)
                if child.board.halfmove_clock >= 100 or child.counts[repetition_key(child.board)] >= 3:
                    return False, 'claim_by_move'
    return None


def key(state, arena, remaining):
    WORK['state_keys'] += 1
    return encoded([arena.spec(), repetition_key(state.board), remaining,
                    state.board.halfmove_clock if arena.history else None,
                    sorted(state.counts.items()) if arena.history else None])


def query_state(query, arena):
    state = start(query['fen'], arena)
    for uci in query.get('moves', []):
        moves = legal(state, arena)
        end = terminal(state, arena, moves)
        # Optional Black claims need not have been taken along a supplied history.
        if end is not None and end[1] not in ('claim_now', 'claim_by_move'):
            raise ValueError('history continues after a compulsory terminal')
        move = chess.Move.from_uci(uci)
        if move not in moves:
            raise ValueError('illegal supplied history')
        state = advance(state, move, arena)
    return state
