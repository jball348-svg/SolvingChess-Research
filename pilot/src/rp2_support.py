"""RP2 measurement/comparator adapters. RP1 mathematical source remains unchanged."""
from collections import Counter, deque
import json
import sys
import time
import chess
import checker
import reuse
from model import WORK, Arena, State, advance, encoded, key, query_state, sha, start


def delta(after, before):
    return {k: v-before.get(k, 0) for k, v in after.items() if v != before.get(k, 0)}


class Meter:
    def __init__(self):
        self.audits = Counter()

    def snapshot(self):
        return time.process_time(), time.perf_counter(), WORK.copy(), self.audits.copy()

    def elapsed(self, snap):
        cpu, wall, work, audits = snap
        return dict(cpu_s=time.process_time()-cpu, wall_s=time.perf_counter()-wall,
                    work=delta(WORK, work), checking=delta(self.audits, audits))

    def run(self, fn):
        snap = self.snapshot()
        try:
            result = fn()
        except Exception as exc:
            exc.measurement = self.elapsed(snap)
            raise
        return result, self.elapsed(snap)

    def check(self, *args, **kwargs):
        """Observe the unmodified checker, including its counters on rejection.

        The exception traceback exposes the checker's local counts. No labels,
        control flow, acceptance condition or move generator are changed.
        """
        cpu, wall = time.process_time(), time.perf_counter()
        counts = {}
        self.audits['calls'] += 1
        try:
            counts = checker.check(*args, **kwargs)
            self.audits['accepted'] += 1
            return counts
        except Exception as exc:
            self.audits['rejected'] += 1
            tb = exc.__traceback__
            while tb:
                if tb.tb_frame.f_code is checker.check.__code__:
                    counts = tb.tb_frame.f_locals.get('counts', {})
                    break
                tb = tb.tb_next
            raise
        finally:
            for name in ('checked_nodes', 'checked_edges', 'generated_edges'):
                self.audits[name] += counts.get(name, 0)
            self.audits['cpu_s'] += time.process_time()-cpu
            self.audits['wall_s'] += time.perf_counter()-wall


def state_at(proof, identifier):
    spec, fen, remaining, clock, counts = json.loads(proof['nodes'][identifier]['state_key'])
    arena = Arena(**spec)
    state = start(fen+' '+str(clock or 0)+' 1', arena)
    if arena.history:
        state.counts = dict(counts)
    return state, remaining


def breadth_first(proof):
    queue, seen = deque([proof['root']]), set()
    while queue:
        identifier = queue.popleft()
        if identifier in seen:
            continue
        seen.add(identifier)
        yield identifier
        queue.extend(c for _, c in sorted(proof['nodes'][identifier]['edges']))


def subproof(proof, root):
    nodes, queue = {}, [root]
    while queue:
        identifier = queue.pop()
        if identifier in nodes:
            continue
        node = proof['nodes'][identifier]
        nodes[identifier] = node
        queue.extend(c for _, c in node['edges'])
    return dict(schema=1, arena=proof['arena'], root=root, nodes=nodes)


def geometry_id(state):
    return sha([min((reuse.shape(state.board, m) for m in reuse.TRANSFORMS), key=encoded),
                state.board.turn])


def deep_bytes(value):
    seen = set()
    def visit(item):
        if id(item) in seen:
            return 0
        seen.add(id(item))
        total = sys.getsizeof(item)
        if isinstance(item, dict):
            total += sum(visit(k)+visit(v) for k, v in item.items())
        elif isinstance(item, (list, tuple, set)):
            total += sum(visit(v) for v in item)
        return total
    return visit(value)


class ProofLibrary(reuse.Library):
    """Frozen Library.lookup ordering, with a ledger for every failed guard.

    The frozen implementation silently skips too-deep templates; these skips
    are observed but still return exactly the same witness (or None).
    """
    def __init__(self, templates, meter, emit):
        super().__init__(templates)
        self.meter, self.emit = meter, emit
        self.cost = Counter()
        self.work = Counter()
        self.audit = Counter()
        self.hits = []

    def lookup(self, state, arena, remaining, stats):
        snap = self.meter.snapshot()
        try:
            return self._lookup(state, arena, remaining, stats)
        finally:
            cost = self.meter.elapsed(snap)
            for k in ('cpu_s', 'wall_s'):
                self.cost[k] += cost[k]
            self.work.update(cost['work'])
            self.audit.update(cost['checking'])

    def _lookup(self, state, arena, remaining, stats):
        if not reuse.is_krk(state.board):
            stats['material_lookup_skips'] += 1
            return None
        stats['template_index_probes'] += 1
        candidates = self.index.get((encoded(reuse.shape(state.board)), state.board.turn), [])
        if not candidates:
            stats['template_index_misses'] += 1
        for template, matrix in candidates:
            event = dict(kind='application', template=template['id'], matrix=matrix,
                         state_key=key(state, arena, remaining))
            if remaining < template['plies']:
                stats['template_depth_rejections'] += 1
                event.update(status='DEPTH_GUARD', required=template['plies'])
                self.emit(event)
                continue
            stats['template_attempts'] += 1
            try:
                (proof, audit), event['cost'] = self.meter.run(
                    lambda: reuse.instantiate(template, state, arena, remaining, matrix))
            except ValueError as exc:
                stats['template_rejections'] += 1
                event.update(status='REJECTED', reason=str(exc), cost=exc.measurement)
                self.emit(event)
                continue
            stats['application_checked_nodes'] += audit['checked_nodes']
            stats['application_checked_edges'] += audit['checked_edges']
            event.update(status='ACCEPTED', audit=audit, proof_sha256=sha(proof))
            self.hits.append(dict(template=template['id'], state_key=event['state_key'],
                                  proof_sha256=sha(proof), nodes=len(proof['nodes'])))
            self.emit(event)
            return proof
        return None


def domain_shape(state, arena, matrix):
    origin = state.board.king(chess.BLACK)
    return sorted(reuse.transform(reuse.offset(s, origin), matrix)
                  for s in chess.SQUARES if arena.contains(s))


def cache_instantiate(entry, state, arena, remaining, check):
    """Transform a complete extensional witness, including negative certificates.

    A full-domain match is required. No proof-template boundary relaxation is
    used. Non-KRK/history entries can serve only their original exact state key.
    """
    proof = entry['proof']
    donor, depth = state_at(proof, proof['root'])
    donor_arena = Arena(**proof['arena'])
    if remaining != depth:
        raise ValueError('cache depth mismatch')
    if arena.history or not reuse.is_krk(state.board) or not reuse.is_krk(donor.board):
        if key(state, arena, remaining) != proof['nodes'][proof['root']]['state_key']:
            raise ValueError('exact cache guard')
        return proof, check(proof, state, arena, remaining)
    matrices = [m for m in reuse.TRANSFORMS
                if reuse.shape(donor.board, m) == reuse.shape(state.board)
                and domain_shape(donor, donor_arena, m) == domain_shape(state, arena, reuse.TRANSFORMS[0])]
    if donor.board.turn != state.board.turn or not matrices:
        raise ValueError('cache full-domain guard')
    matrix = matrices[0]
    origin, target = donor.board.king(chess.BLACK), state.board.king(chess.BLACK)
    def square(s):
        x, y = reuse.transform(reuse.offset(s, origin), matrix)
        x += chess.square_file(target)
        y += chess.square_rank(target)
        if not (0 <= x < 8 and 0 <= y < 8):
            raise ValueError('cache transform outside board')
        return chess.square(x, y)
    nodes = {}
    for identifier, node in proof['nodes'].items():
        old, d = state_at(proof, identifier)
        board = chess.Board(None)
        for s, piece in old.board.piece_map().items():
            board.set_piece_at(square(s), piece)
        board.turn = old.board.turn
        position = State(board, {})
        edges = []
        for uci, child in node['edges']:
            move = chess.Move.from_uci(uci)
            edges.append([chess.Move(square(move.from_square), square(move.to_square)).uci(), child])
        nodes[identifier] = dict(node, state_key=key(position, arena, d), edges=edges)
    output = dict(schema=1, arena=arena.spec(), root=proof['root'], nodes=nodes)
    return output, check(output, state, arena, remaining)


class GeometryCache:
    def __init__(self, entries, meter, emit):
        self.entries = entries
        self.index = {entry['key']: entry for entry in entries}
        self.meter, self.emit = meter, emit
        self.cost, self.work, self.audit = Counter(), Counter(), Counter()
        self.hits = []

    def lookup(self, state, arena, remaining, stats):
        snap = self.meter.snapshot()
        try:
            stats['geometry_cache_probes'] += 1
            entry = self.index.get(reuse.cache_geometry(state, arena, remaining))
            if entry is None:
                stats['geometry_cache_misses'] += 1
                return None
            event = dict(kind='cache_application', state_key=key(state, arena, remaining),
                         entry=entry['id'])
            try:
                (proof, audit), event['cost'] = self.meter.run(
                    lambda: cache_instantiate(entry, state, arena, remaining, self.meter.check))
            except ValueError as exc:
                stats['geometry_cache_rejections'] += 1
                event.update(status='REJECTED', reason=str(exc), cost=exc.measurement)
                self.emit(event)
                return None
            event.update(status='ACCEPTED', audit=audit)
            self.emit(event)
            self.hits.append(dict(entry=entry['id'], state_key=event['state_key']))
            return proof
        finally:
            cost = self.meter.elapsed(snap)
            for k in ('cpu_s', 'wall_s'):
                self.cost[k] += cost[k]
            self.work.update(cost['work'])
            self.audit.update(cost['checking'])


def unresolved_stack(exc):
    """Retain the active DFS path and every pending sibling if a limit occurs."""
    out, tb = [], exc.__traceback__
    while tb:
        f = tb.tb_frame
        if f.f_code.co_name == 'solve' and 'state' in f.f_locals:
            v = f.f_locals
            out.append(dict(fen=v['state'].board.fen(), remaining=v['remaining'],
                            state_key=v.get('k'),
                            ordered_moves=[m.uci() for m in v.get('moves', [])],
                            active_move=v['m'].uci() if 'm' in v else None,
                            completed_edges=v.get('edges', [])))
        tb = tb.tb_next
    return out
