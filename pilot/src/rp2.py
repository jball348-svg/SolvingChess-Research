"""Bounded RP2 only: donor acquisition or the reserved R1 evaluation.

Run through measure.py. No R1 training, later rung or held-out variant is exposed.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import platform
import resource
import sys
import time
import chess
import reuse
from benchmarks import cohort, HORIZON
from model import WORK, encoded, query_state, sha
from solver import Solver, Limit
from rp2_support import (Meter, ProofLibrary, GeometryCache, breadth_first, deep_bytes,
                         delta, geometry_id, state_at, subproof, unresolved_stack)

ROOT = Path(__file__).resolve().parents[2]
RP1 = 'ccf3a1c18ac9f92250bb94576a9d3f010fab80f3'
CAP = 1024**2


def file_hash(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = encoded(value)+'\n'
    if len(payload.encode()) > 64*1024**2:
        raise Limit('64 MiB file limit')
    path.write_text(payload)
    return len(payload.encode())


def verify_contract():
    manifest = json.loads((ROOT/'pilot/evidence/source-manifest.json').read_text())
    for path, record in manifest['files'].items():
        full = ROOT/path
        if full.stat().st_size != record['bytes'] or file_hash(full) != record['sha256']:
            raise ValueError('RP1 source manifest mismatch: '+path)
    if chess.__version__ != manifest['dependency']['chess_version'] or file_hash(chess.__file__) != manifest['dependency']['chess_core_sha256']:
        raise ValueError('pinned chess dependency mismatch')
    return dict(rp1_freeze=RP1, source_files=len(manifest['files']), chess=chess.__version__,
                chess_core_sha256=file_hash(chess.__file__))


def ordinary_counts(solver):
    leaves = Counter(n['leaf'] for n in solver.table.values() if n['leaf'])
    return dict(table_entries=len(solver.table), table_leaf_reasons=dict(leaves),
                search_counts=dict(solver.stats))


class Run:
    def __init__(self, args):
        self.args, self.meter = args, Meter()
        # Observability only: reuse's calls still execute the frozen checker.
        reuse.check = self.meter.check
        self.begin = self.meter.snapshot()
        self.directory = args.output.parent
        self.directory.mkdir(parents=True, exist_ok=True)
        self.events = (self.directory/'events.jsonl').open('w')
        self.event_counts = Counter()
        self.report = dict(schema=1, part='RP2', mode=args.mode, arm=args.arm, repeat=args.repeat,
                           rp1_freeze=RP1, python=sys.version, platform=platform.platform(),
                           rows=[], engine_calls=0, complete_arena_solves=0,
                           human_llm_cost='unavailable, not zero',
                           memory_limit_bytes=resource.getrlimit(resource.RLIMIT_AS)[0],
                           cpu_limit_seconds=resource.getrlimit(resource.RLIMIT_CPU)[0])
        self.report['contract'], self.report['contract_cost'] = self.meter.run(verify_contract)

    def emit(self, event):
        self.events.write(encoded(event)+'\n')
        self.events.flush()
        self.event_counts[(event['kind'], event['status'])] += 1

    def checkpoint(self):
        write_json(self.args.output, self.report)

    def queries(self, name, role, per_side):
        (arena, queries), cost = self.meter.run(lambda: cohort(name, role, per_side))
        self.report.update(arena=arena.spec(), plies=HORIZON, queries=queries,
                           query_sha256=sha(queries), shared_query_generation=cost,
                           complete_sampling_scan=True)
        self.checkpoint()
        return arena, queries

    def solve_queries(self, arena, queries, library=None):
        solver = Solver(arena, library=library)
        proofs = []
        for query in queries:
            row = dict(query_id=query['id'])
            self.report['rows'].append(row)
            state, row['load'] = self.meter.run(lambda: query_state(query, arena))
            before = solver.stats.copy()
            app_before = library.cost.copy() if library else Counter()
            work_before = library.work.copy() if library else Counter()
            audit_before = library.audit.copy() if library else Counter()
            try:
                root, row['search'] = self.meter.run(lambda: solver.solve(state, HORIZON))
                proof, row['proof_emit'] = self.meter.run(lambda: solver.certificate(root))
                payload, row['serialize'] = self.meter.run(lambda: encoded(proof))
                loaded, row['proof_load'] = self.meter.run(lambda: json.loads(payload))
                audit, row['verification'] = self.meter.run(lambda: self.meter.check(loaded, state, arena, HORIZON))
                row.update(status='EXACT', result=audit['result'], audit=audit,
                           certificate_sha256=sha(loaded), certificate_bytes=len(payload.encode()))
                certificate = dict(query=query, plies=HORIZON, proof=loaded)
                path = self.directory/'certificates'/(query['id']+'.json')
                _, row['certificate_storage'] = self.meter.run(lambda: write_json(path, certificate))
                row['certificate_path'] = str(path.relative_to(ROOT))
                proofs.append((query, loaded))
            except Limit as exc:
                row.update(status='UNKNOWN/LIMIT', reason=str(exc), failed_phase_cost=exc.measurement,
                           unresolved_frontier=unresolved_stack(exc))
            row['search_counts'] = delta(solver.stats, before)
            row['table_entries'] = len(solver.table)
            app = delta(library.cost, app_before) if library else {}
            row['application_in_search'] = dict(cpu_s=app.get('cpu_s', 0), wall_s=app.get('wall_s', 0),
                    work=delta(library.work, work_before) if library else {},
                    checking=delta(library.audit, audit_before) if library else {})
            search = row.get('search', row.get('failed_phase_cost', {}))
            row['fallback_residual'] = {unit: search.get(unit, 0)-app.get(unit, 0)
                                        for unit in ('cpu_s', 'wall_s')}
            row['fallback_residual']['work'] = delta(search.get('work', {}), row['application_in_search']['work'])
            row.setdefault('unresolved_frontier', [])
            self.checkpoint()
        self.report.update(ordinary_counts(solver))
        self.report['table_serialized_bytes'], self.report['table_storage_accounting'] = self.meter.run(solver.serialized_table_bytes)
        self.report['table_python_bytes'], self.report['table_memory_accounting'] = self.meter.run(lambda: deep_bytes(solver.table))
        self.report['outcomes'] = dict(Counter('true' if r.get('result') is True else 'false' if r.get('result') is False
                                             else 'unknown' for r in self.report['rows']))
        self.report['library_settled_obligations'] = solver.stats.get('proof_hits', 0)
        self.report['library_hits'] = library.hits if library else []
        return proofs

    def acquire(self):
        arena, queries = self.queries('dev', 'train', 12)
        proofs = self.solve_queries(arena, queries)
        library = dict(schema=1, kind='geometry_cache' if self.args.arm == 'C' else 'proof_templates',
                       rp1_freeze=RP1, donor_query_sha256=self.report['query_sha256'], entries=[])
        seen = set()
        enumerated, enumer_cost = self.meter.run(lambda: [(q, p, list(breadth_first(p))) for q, p in proofs
                if self.args.arm == 'C' or p['nodes'][p['root']]['result']])
        self.report['candidate_enumeration'] = enumer_cost
        self.report['subproof_nodes_scanned'] = sum(len(ids) for _, _, ids in enumerated)
        candidates = self.meter.snapshot()
        attempted, skipped = 0, 0
        for query, proof, identifiers in enumerated:
            if self.args.arm != 'C' and not proof['nodes'][proof['root']]['result']:
                continue
            scheduled = 0
            for identifier in identifiers:
                if self.args.arm != 'C' and proof['nodes'][identifier]['leaf'] is not None:
                    skipped += 1
                    continue
                if self.args.arm != 'C' and scheduled == 32:
                    break
                scheduled += 1
                attempted += 1
                event = dict(kind='candidate', query_id=query['id'], node_id=identifier, ordinal=scheduled,
                             donor_certificate_sha256=sha(proof))
                snap = self.meter.snapshot()
                concrete = subproof(proof, identifier)
                state, remaining = state_at(concrete, identifier)
                provenance = dict(query_id=query['id'], node_id=identifier,
                                  certificate_sha256=sha(proof), subproof_sha256=sha(concrete),
                                  donor_arena=arena.spec(), remaining=remaining,
                                  state_key=concrete['nodes'][identifier]['state_key'])
                try:
                    if self.args.arm == 'C':
                        self.meter.check(concrete, state, arena, remaining)
                        identity = reuse.cache_geometry(state, arena, remaining)
                        entry = dict(id=sha(identity), key=identity, proof=concrete, provenance=provenance)
                    else:
                        template = reuse.compile_template(concrete, state, arena, remaining)
                        identity = geometry_id(state)
                        entry = dict(id=template['id'], geometry_id=identity, template=template, provenance=provenance)
                    event.update(identity=sha(identity) if self.args.arm == 'C' else identity,
                                 object_id=entry['id'], nodes=len(concrete['nodes']))
                    # Compile/check even when duplicate or over cap: none of
                    # these already-scheduled candidates becomes free work.
                    if identity in seen:
                        event['status'] = 'DUPLICATE'
                    elif self.args.arm != 'C' and len(concrete['nodes']) > 2048:
                        event['status'] = 'NODE_CAP'
                    elif self.args.arm != 'C' and len(library['entries']) >= 8:
                        event['status'] = 'GEOMETRY_CAP'
                    elif len((encoded(dict(library, entries=library['entries']+[entry]))+'\n').encode()) > CAP:
                        event['status'] = 'BYTE_CAP'
                    else:
                        seen.add(identity)
                        library['entries'].append(entry)
                        event['status'] = 'ACCEPTED'
                except ValueError as exc:
                    event.update(status='REJECTED', reason=str(exc))
                event['cost'] = self.meter.elapsed(snap)
                self.emit(event)
        self.report['all_candidates'] = self.meter.elapsed(candidates)
        self.report.update(candidate_attempts=attempted, skipped_terminal_roots=skipped,
                           accepted_entries=len(library['entries']))
        path = self.directory/'library.json'
        self.report['library_serialized_bytes'], self.report['library_storage'] = self.meter.run(lambda: write_json(path, library))
        self.report['library_sha256'] = file_hash(path)
        self.report['library_path'] = str(path.relative_to(ROOT))
        self.report['object_ids'] = [e['id'] for e in library['entries']]
        self.report['library_python_bytes'], self.report['library_memory_accounting'] = self.meter.run(lambda: deep_bytes(library))
        assert self.report['library_serialized_bytes'] <= CAP

    def evaluate(self):
        if not self.args.freeze or not self.args.freeze_commit:
            raise ValueError('R1 requires a published donor freeze and its commit')
        def load_freeze():
            freeze = json.loads(self.args.freeze.read_text())
            for path, digest in freeze['driver_sources'].items():
                if file_hash(ROOT/path) != digest:
                    raise ValueError('driver changed after donor freeze: '+path)
            return freeze
        freeze, self.report['freeze_load'] = self.meter.run(load_freeze)
        self.report.update(donor_freeze_commit=self.args.freeze_commit, donor_freeze_sha256=file_hash(self.args.freeze))
        library = None
        if self.args.arm != 'B':
            record = freeze['acquisitions'][str(self.args.repeat)+'-'+self.args.arm]
            def load():
                path = ROOT/record['library_path']
                if file_hash(path) != record['library_sha256']:
                    raise ValueError('donor library identity mismatch')
                data = json.loads(path.read_text())
                if self.args.arm == 'C':
                    obj = GeometryCache(data['entries'], self.meter, self.emit)
                else:
                    obj = ProofLibrary([e['template'] for e in data['entries']], self.meter, self.emit)
                return obj, data
            (library, data), self.report['library_load_and_index'] = self.meter.run(load)
            self.report['library_serialized_bytes'] = (ROOT/record['library_path']).stat().st_size
            self.report['library_identity'] = record['library_sha256']
            self.report['library_python_bytes'], self.report['library_memory_accounting'] = self.meter.run(
                lambda: deep_bytes([data, library.index]))
        else:
            self.report.update(library_serialized_bytes=0, library_python_bytes=0)
        arena, queries = self.queries('r1', 'test', 8)
        self.solve_queries(arena, queries, library)

    def finish(self):
        self.events.close()
        self.report['event_counts'] = {kind+':'+status: n for (kind, status), n in self.event_counts.items()}
        self.report['total_inside_process'] = self.meter.elapsed(self.begin)
        self.report['process_peak_rss_kib'] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        self.report['status'] = 'COMPLETE' if all(r['status'] == 'EXACT' for r in self.report['rows']) else 'LIMIT'
        self.report['events_path'] = str((self.directory/'events.jsonl').relative_to(ROOT))
        self.checkpoint()
        total = sum(p.stat().st_size for p in self.directory.parent.rglob('*') if p.is_file())
        if total > 1024**3:
            raise Limit('1 GiB part disk limit')
        print(encoded({k:self.report[k] for k in ('mode','arm','repeat','status','outcomes','total_inside_process')}))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['acquire', 'evaluate'])
    parser.add_argument('--arm', choices=['B', 'C', 'F', 'G'], required=True)
    parser.add_argument('--repeat', type=int, choices=[1,2,3], required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--freeze', type=Path)
    parser.add_argument('--freeze-commit')
    args = parser.parse_args()
    args.output = args.output.resolve()
    if args.mode == 'acquire' and args.arm == 'B':
        parser.error('B has no acquisition')
    from measure import limits
    limits()
    run = Run(args)
    try:
        getattr(run, args.mode)()
        run.finish()
    except Exception as exc:
        run.report.update(status='BLOCKED', error=type(exc).__name__+': '+str(exc))
        run.report['partial_cost'] = run.meter.elapsed(run.begin)
        run.checkpoint()
        raise


if __name__ == '__main__':
    main()
