"""Frozen RP1 seam for spatial proof skeletons. No library is learned by this module.

Only previously checked positive KRK proofs may be compiled. A template carries
the root geometry and an entire decreasing-depth proof tree/DAG, not an answer.
Every application is concretized and checked again, including all opponent moves.
"""
import chess
from checker import check
from model import advance, encoded, key, legal, sha

TRANSFORMS = ((1, 0, 0, 1), (-1, 0, 0, 1), (1, 0, 0, -1), (-1, 0, 0, -1),
              (0, 1, 1, 0), (0, -1, 1, 0), (0, 1, -1, 0), (0, -1, -1, 0))


def transform(xy, matrix):
    x, y = xy
    a, b, c, d = matrix
    return a*x+b*y, c*x+d*y


def offset(square, origin):
    return chess.square_file(square)-chess.square_file(origin), chess.square_rank(square)-chess.square_rank(origin)


def is_krk(board):
    return sorted(p.symbol() for p in board.piece_map().values()) == ['K', 'R', 'k']


def shape(board, matrix=TRANSFORMS[0]):
    origin = board.king(chess.BLACK)
    return sorted([[p.symbol(), *transform(offset(s, origin), matrix)] for s, p in board.piece_map().items()])


def compile_template(proof, state, arena, remaining):
    check(proof, state, arena, remaining, expected=True)
    if arena.history or not is_krk(state.board):
        raise ValueError('donor templates are restricted KRK proofs only')
    origin = state.board.king(chess.BLACK)
    variants = []
    for matrix in TRANSFORMS:
        nodes = {}
        for identifier, node in proof['nodes'].items():
            edges = []
            for uci, child in node['edges']:
                m = chess.Move.from_uci(uci)
                edges.append([list(transform(offset(m.from_square, origin), matrix)),
                              list(transform(offset(m.to_square, origin), matrix)), child])
            nodes[identifier] = {'used': remaining-node['remaining'], 'leaf': node['leaf'], 'edges': edges}
        variants.append({'schema': 1, 'shape': shape(state.board, matrix), 'turn': state.board.turn,
                         'plies': max(n['used'] for n in nodes.values()), 'root': proof['root'], 'nodes': nodes})
    # Geometry identity is separate from witness identity; RP2 deduplicates shapes.
    template = min(variants, key=encoded)
    template['id'] = sha(template)
    return template


def instantiate(template, state, arena, remaining, matrix):
    if remaining < template['plies'] or not is_krk(state.board) or state.board.turn != template['turn']:
        raise ValueError('root material/turn/depth guard')
    wanted = sorted([[p, *transform((x, y), matrix)] for p, x, y in template['shape']])
    if shape(state.board) != wanted:
        raise ValueError('root geometry guard')
    origin = state.board.king(chess.BLACK)
    nodes = {}

    def square(xy):
        x, y = transform(xy, matrix)
        x += chess.square_file(origin)
        y += chess.square_rank(origin)
        if not (0 <= x < 8 and 0 <= y < 8):
            raise ValueError('template leaves physical board')
        return chess.square(x, y)

    def visit(identifier, position, depth):
        k = key(position, arena, depth)
        if identifier in nodes:
            if nodes[identifier]['state_key'] != k:
                raise ValueError('history/state alias')
            return
        source = template['nodes'][identifier]
        if source['used'] != remaining-depth:
            raise ValueError('template progress')
        node = {'state_key': k, 'remaining': depth, 'result': True, 'leaf': source['leaf'], 'edges': []}
        nodes[identifier] = node
        permitted = legal(position, arena)
        for a, b, child in source['edges']:
            move = chess.Move(square(a), square(b))
            if move not in permitted:
                raise ValueError('template move not admitted')
            node['edges'].append([move.uci(), child])
            visit(child, advance(position, move, arena), depth-1)

    visit(template['root'], state, remaining)
    proof = {'schema': 1, 'arena': arena.spec(), 'root': template['root'], 'nodes': nodes}
    return proof, check(proof, state, arena, remaining, expected=True)


class Library:
    def __init__(self, templates=()):
        self.templates = sorted(templates, key=lambda t: t['id'])
        self.index = {}
        for template in self.templates:
            for matrix in TRANSFORMS:
                geometry = sorted([[p, *transform((x, y), matrix)] for p, x, y in template['shape']])
                self.index.setdefault((encoded(geometry), template['turn']), []).append((template, matrix))

    def lookup(self, state, arena, remaining, stats):
        if not is_krk(state.board):
            return None
        stats['template_index_probes'] += 1
        for template, matrix in self.index.get((encoded(shape(state.board)), state.board.turn), []):
            if remaining < template['plies']:
                continue
            stats['template_attempts'] += 1
            try:
                proof, audit = instantiate(template, state, arena, remaining, matrix)
            except ValueError:
                stats['template_rejections'] += 1
                continue
            stats['application_checked_nodes'] += audit['checked_nodes']
            stats['application_checked_edges'] += audit['checked_edges']
            return proof
        return None


def cache_geometry(state, arena, remaining):
    """Generic cache control must retain the whole arena, not just root geometry.

    Histories use their exact key. D4 is sound only for pawn-free KRK here.
    """
    if arena.history or not is_krk(state.board):
        return key(state, arena, remaining)
    origin = state.board.king(chess.BLACK)
    domains = []
    for matrix in TRANSFORMS:
        squares = sorted(transform(offset(s, origin), matrix) for s in chess.SQUARES if arena.contains(s))
        domains.append(encoded([shape(state.board, matrix), squares, state.board.turn, remaining]))
    return min(domains)
