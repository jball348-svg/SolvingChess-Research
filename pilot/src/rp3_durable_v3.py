"""RP3-MR1 immutable-generation persistence and completeness checks; no chess or search changes."""
from collections import Counter
import hashlib
import json
import math
import os
import uuid
from pathlib import Path


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read(path):
    return json.loads(Path(path).read_text())


def sync_directory(path):
    fd = os.open(path, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    data = (json.dumps(value, sort_keys=True, separators=(',', ':'))+'\n').encode()
    if len(data) > 64*1024**2:
        raise ValueError('64 MiB file limit')
    # Use a process-unique temporary name.  The first recovery run used one
    # fixed ``*.pending`` name; this version makes each generation independently
    # durable and verifies the bytes that are visible after replacement.
    temporary = path.with_name('.'+path.name+'.'+str(os.getpid())+'.'+uuid.uuid4().hex+'.pending')
    try:
        with temporary.open('xb') as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
        os.replace(temporary, path)
        sync_directory(path.parent)
        visible = path.read_bytes()
        if visible != data:
            raise IOError('post-replace readback mismatch: '+str(path))
    finally:
        try:
            temporary.unlink()
        except FileNotFoundError:
            pass
    return len(data)


def validate(directory, expected=None, marker=True):
    directory = Path(directory)
    r = read(directory/'report.json')
    final_path = directory/'report.final.json'
    if final_path.exists():
        assert final_path.read_bytes() == (directory/'report.json').read_bytes(), 'final report link mismatch'
    assert r['status'] in ('COMPLETE', 'LIMIT'), 'missing final status'
    queries = r['queries']; rows = r['rows']
    if expected is not None:
        assert len(queries) == expected, 'wrong query count'
    assert len(rows) == len(queries), 'incomplete measurement rows'
    assert [x['query_id'] for x in rows] == [q['id'] for q in queries], 'query ordering'
    counts = Counter()
    files = {}
    for q, row in zip(queries, rows):
        assert row['status'] in ('EXACT', 'UNKNOWN/LIMIT')
        for key in ('search_counts', 'application_in_search', 'fallback_residual', 'unresolved_frontier'):
            assert key in row, 'incomplete query '+key
        counts.update(row['search_counts'])
        if row['status'] == 'EXACT':
            for key in ('load','search','proof_emit','serialize','proof_load','verification','certificate_storage'):
                assert all(u in row[key] for u in ('cpu_s','wall_s')), 'missing phase '+key
            path = directory/'certificates'/(q['id']+'.json')
            cert = read(path)
            assert cert['query'] == q
            raw = json.dumps(cert['proof'], sort_keys=True, separators=(',', ':')).encode()
            assert hashlib.sha256(raw).hexdigest() == row['certificate_sha256']
            files[str(path.relative_to(directory))] = digest(path)
    final = Counter(r['search_counts'])
    assert set(counts) == set(final), 'missing final search counters'
    assert all(math.isclose(counts[k], final[k], rel_tol=1e-12, abs_tol=1e-12)
               if k.endswith('_s') else counts[k] == final[k] for k in counts), 'final search counters differ from rows'
    events = [json.loads(s) for s in (directory/'events.jsonl').read_text().splitlines()]
    ec = Counter(e['kind']+':'+e['status'] for e in events)
    assert ec == Counter(r['event_counts']), 'incomplete event tail'
    if r['mode'] == 'acquire':
        assert len(events) == r['candidate_attempts']
        assert digest(directory/'library.json') == r['library_sha256']
        lib = read(directory/'library.json')
        assert [e['id'] for e in lib['entries']] == r['object_ids']
        files['library.json'] = digest(directory/'library.json')
    else:
        assert sum(e['status'] == 'ACCEPTED' for e in events) == r['library_settled_obligations']
    for key in ('total_inside_process','outcomes','table_entries','table_serialized_bytes','table_leaf_reasons'):
        assert key in r, 'missing final '+key
    if r.get('experiment') in ('RP3-MR1', 'RP3-MR1-FINAL', 'RP3-MR1-V3'):
        journal = [json.loads(s) for s in (directory/'rows.jsonl').read_text().splitlines()]
        assert journal == rows, 'query journal mismatch'
        files['rows.jsonl'] = digest(directory/'rows.jsonl')
    files.update({'report.json':digest(directory/'report.json'), 'events.jsonl':digest(directory/'events.jsonl')})
    if final_path.exists(): files['report.final.json'] = digest(final_path)
    if marker:
        m = read(directory/'completion.json')
        assert m['files'] == files and m['rows'] == len(rows) and m['events'] == len(events), 'completion digest mismatch'
    return dict(rows=len(rows), events=len(events), files=files)
