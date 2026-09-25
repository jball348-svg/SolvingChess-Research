"""RP3 scheduling adapter; all RP1/RP2 mathematical and measurement code is frozen."""
import argparse
import json
from pathlib import Path
import reuse
from model import encoded, sha
from rp2 import Run as RP2Run, ROOT, RP1, CAP, file_hash, write_json
from rp2_support import (ProofLibrary, GeometryCache, breadth_first, deep_bytes,
                         geometry_id, state_at, subproof)

DONOR = '2736e3cf00e0696520c3d8fe1203f28087ed3db6'
PUBLICATION = '984b427eb4054c7eb11968b4f871a1e4f73d5836'


def read(path):
    return json.loads(Path(path).read_text())


def checked_library(record):
    path = ROOT/record['library_path']
    if file_hash(path) != record['library_sha256']:
        raise ValueError('library identity mismatch: '+str(path))
    return read(path)


def admission(library, entry, identity, seen, nodes, initial, cache):
    # Same RP2 ordering, extended only to the frozen per-update/total quotas.
    if identity in seen:
        return 'DUPLICATE'
    if not cache and nodes > 2048:
        return 'NODE_CAP'
    if not cache and (len(library['entries'])-initial >= 8 or len(library['entries']) >= 64):
        return 'GEOMETRY_CAP'
    if len((encoded(dict(library, entries=library['entries']+[entry]))+'\n').encode()) > CAP:
        return 'BYTE_CAP'
    seen.add(identity)
    library['entries'].append(entry)
    return 'ACCEPTED'


class Run(RP2Run):
    def __init__(self, args):
        super().__init__(args)
        self.report.update(part='RP3', rung=args.rung, diagnostic=args.diagnostic,
                           donor_freeze_commit=DONOR, rp2_publication_commit=PUBLICATION)
        def load_freeze():
            frozen = read(args.source_freeze)
            for path, digest in frozen['driver_sources'].items():
                if file_hash(ROOT/path) != digest:
                    raise ValueError('RP3 source changed after freeze: '+path)
            return read(args.freeze)
        self.freeze, self.report['freeze_load'] = self.meter.run(load_freeze)
        self.report['source_freeze_sha256'] = file_hash(args.source_freeze)
        self.report['input_freeze_sha256'] = file_hash(args.freeze)

    def input_record(self):
        arm = 'F' if self.args.diagnostic == 'ablation' else self.args.arm
        if arm == 'F':
            return read(ROOT/'pilot/evidence/rp2/donor-freeze.json')['acquisitions'][f'{self.args.repeat}-F']
        return self.freeze['acquisitions'][f'{self.args.repeat}-{arm}']

    def evaluate(self):
        library = None
        if self.args.arm != 'B':
            record = self.input_record()
            def load():
                data = checked_library(record)
                obj = (GeometryCache(data['entries'], self.meter, self.emit) if self.args.arm == 'C'
                       else ProofLibrary([e['template'] for e in data['entries']], self.meter, self.emit))
                return obj, data
            (library, data), self.report['library_load_and_index'] = self.meter.run(load)
            self.report.update(library_serialized_bytes=(ROOT/record['library_path']).stat().st_size,
                               library_identity=record['library_sha256'], library_path=record['library_path'])
            self.report['library_python_bytes'], self.report['library_memory_accounting'] = self.meter.run(
                lambda: deep_bytes([data, library.index]))
        else:
            self.report.update(library_serialized_bytes=0, library_python_bytes=0)
        arena, queries = self.queries(self.args.rung, 'test', 8)
        if self.args.diagnostic == 'reverse':
            queries = list(reversed(queries))
            self.report.update(queries=queries, query_sha256=sha(queries))
            self.checkpoint()
        self.solve_queries(arena, queries, library)

    def acquire(self):
        record = self.input_record()
        library, self.report['inherited_library_load'] = self.meter.run(lambda: checked_library(record))
        self.report['inherited_library_identity'] = record['library_sha256']
        initial = len(library['entries'])
        arena, queries = self.queries(self.args.rung, 'train', 12)
        proofs = self.solve_queries(arena, queries)
        seen = {e['key'] if self.args.arm == 'C' else e['geometry_id'] for e in library['entries']}
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
                    event['status'] = admission(library, entry, identity, seen, len(concrete['nodes']), initial, self.args.arm == 'C')
                except ValueError as exc:
                    event.update(status='REJECTED', reason=str(exc))
                event['cost'] = self.meter.elapsed(snap)
                self.emit(event)
        self.report['all_candidates'] = self.meter.elapsed(candidates)
        self.report.update(candidate_attempts=attempted, skipped_terminal_roots=skipped,
                           accepted_entries=len(library['entries']), initial_entries=initial,
                           new_entries=len(library['entries'])-initial)
        path = self.directory/'library.json'
        self.report['library_serialized_bytes'], self.report['library_storage'] = self.meter.run(lambda: write_json(path, library))
        self.report['library_sha256'] = file_hash(path)
        self.report['library_path'] = str(path.relative_to(ROOT))
        self.report['object_ids'] = [e['id'] for e in library['entries']]
        self.report['library_python_bytes'], self.report['library_memory_accounting'] = self.meter.run(lambda: deep_bytes(library))
        assert self.report['library_serialized_bytes'] <= CAP


def main():
    p = argparse.ArgumentParser()
    p.add_argument('mode', choices=['acquire', 'evaluate'])
    p.add_argument('--rung', choices=['r1', 'r2', 'r3', 'r4'], required=True)
    p.add_argument('--arm', choices=list('BCFG'), required=True)
    p.add_argument('--repeat', type=int, choices=[1,2,3], required=True)
    p.add_argument('--diagnostic', choices=['primary','ablation','reverse'], default='primary')
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--freeze', type=Path, required=True)
    p.add_argument('--source-freeze', type=Path, required=True)
    a = p.parse_args()
    if a.mode == 'acquire' and (a.arm not in 'CG' or a.rung == 'r4' or a.diagnostic != 'primary'):
        p.error('only R1/R2/R3 C/G training is authorized')
    if a.mode == 'evaluate' and (a.rung == 'r1' or
            (a.diagnostic != 'primary' and a.rung not in ['r3','r4']) or
            (a.diagnostic == 'ablation' and a.arm != 'G')):
        p.error('invalid RP3 evaluation/control')
    a.output = a.output.resolve()
    if a.output.exists():
        p.error('refusing to overwrite recorded run')
    from measure import limits
    limits()
    run = Run(a)
    try:
        getattr(run, a.mode)()
        run.finish()
    except Exception as exc:
        run.report.update(status='BLOCKED', error=type(exc).__name__+': '+str(exc),
                          partial_cost=run.meter.elapsed(run.begin))
        run.checkpoint()
        raise


if __name__ == '__main__':
    main()
