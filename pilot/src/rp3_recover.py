"""Recover a lost final checkpoint from ORIGINAL ledgers; never rerun acquisition.

Keep original bytes. No timing or work count is copied from a different repeat.
Only this named RP3 reporting interruption is handled.
"""
from collections import Counter
from pathlib import Path
import json
from model import sha
from rp2 import ROOT,file_hash,write_json
from rp3 import read
from rp2_support import breadth_first


def main():
    root=ROOT/'pilot/evidence/rp3'
    d=root/'acquire-r2-primary-1-G'
    original=d/'report-checkpoint-before-recovery.json'
    if original.exists():raise ValueError('recovery already performed')
    original.write_bytes((d/'report.json').read_bytes())
    r=read(original);env=read(d/'envelope.json');completion=json.loads(env['stdout'].strip())
    assert env['returncode']==0 and completion['status']=='COMPLETE'
    assert len(r['rows'])==24 and all(x['status']=='EXACT' for x in r['rows'])
    for row in r['rows']:
        assert sha(read(ROOT/row['certificate_path'])['proof'])==row['certificate_sha256']
    library=read(d/'library.json')
    assert file_hash(d/'library.json')==file_hash(root/'acquire-r2-primary-2-G/library.json')==file_hash(root/'acquire-r2-primary-3-G/library.json')
    events=[json.loads(s) for s in (d/'events.jsonl').read_text().splitlines()]
    counts=Counter()
    for row in r['rows']:counts.update(row['search_counts'])
    r.update(status=completion['status'],outcomes=completion['outcomes'],
        total_inside_process=completion['total_inside_process'],search_counts=dict(counts),
        event_counts=dict(Counter(e['kind']+':'+e['status'] for e in events)),
        events_path=str((d/'events.jsonl').relative_to(ROOT)),
        table_entries=r['rows'][-1]['table_entries'],library_settled_obligations=0,library_hits=[],
        library_path=str((d/'library.json').relative_to(ROOT)),library_sha256=file_hash(d/'library.json'),
        library_serialized_bytes=(d/'library.json').stat().st_size,object_ids=[e['id'] for e in library['entries']],
        candidate_attempts=len(events),initial_entries=16,accepted_entries=len(library['entries']),
        new_entries=sum(e['status']=='ACCEPTED' for e in events),
        process_peak_rss_kib=env['child_peak_rss_kib'])
    note=dict(original_checkpoint_sha256=file_hash(original),original_envelope_sha256=file_hash(d/'envelope.json'),
        finding='Final report checkpoint unavailable although original process envelope records successful completion. Filesystem cause undetermined.',
        reconstructed_from='Original process stdout, original 24 per-query rows/certificates, original candidate events and original final library; no replay.',
        unavailable=['aggregate candidate/enumeration phase intervals','library storage/memory-accounting intervals',
                     'table storage/memory-accounting intervals','table serialized/Python bytes and terminal leaf tally','library Python bytes'],
        accounting='Full original CPU/wall envelope and process-wide work/check counters retained. Missing phase intervals remain inside explicitly unallocated envelope residual; never zero or refunded.',
        repetition_identity='All 24 root certificates, all 19 candidate identities/statuses and final 24-object library match repeats 2/3; no costs imported from them.')
    r['report_recovery']=note
    write_json(d/'report.json',r)
    write_json(root/'recovery.json',dict(note,restored_report_sha256=file_hash(d/'report.json'),
        frozen_experimental_source_unchanged=True,no_acquisition_or_evaluation_repeated=True))
    print(json.dumps(note))


if __name__=='__main__':main()
