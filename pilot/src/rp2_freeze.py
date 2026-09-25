"""Validate acquisition identities and prepare the pre-evaluation freeze manifest."""
import argparse
import json
from pathlib import Path
import subprocess
from rp2 import ROOT, RP1, file_hash, verify_contract, write_json


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--input', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    if list(a.input.glob('evaluate-*')):
        raise ValueError('cannot prepare a donor freeze after evaluation in this directory')
    verify_contract()
    # Audit the actual commit too, rather than trusting only the manifest text.
    manifest = json.loads((ROOT/'pilot/evidence/source-manifest.json').read_text())
    for path in manifest['files']:
        assert subprocess.check_output(['git','show',RP1+':'+path]) == (ROOT/path).read_bytes(), path
    sources = ['pilot/src/rp2.py', 'pilot/src/rp2_support.py', 'pilot/src/rp2_campaign.py',
               'pilot/src/rp2_freeze.py', 'pilot/tests/test_rp2.py']
    freeze = dict(schema=1, rp1_freeze=RP1,
                  checkout_before_rp2=subprocess.check_output(['git','rev-parse','HEAD'], text=True).strip(),
                  driver_sources={path:file_hash(ROOT/path) for path in sources}, acquisitions={},
                  reserved_execution={name:False for name in ['r1','r2','r3','r4','counterplay','history']})
    identities, objects, cache = set(), set(), set()
    for repeat in range(1,4):
        for arm in ['C','F','G']:
            directory = a.input/f'acquire-{repeat}-{arm}'
            report = json.loads((directory/'report.json').read_text())
            envelope = json.loads((directory/'envelope.json').read_text())
            assert report['status'] == 'COMPLETE' and envelope['returncode'] == 0
            assert len(report['queries']) == 24
            assert sum(q['fen'].split()[1] == 'w' for q in report['queries']) == 12
            identities.add(tuple((r['query_id'],r['certificate_sha256']) for r in report['rows']))
            (cache if arm == 'C' else objects).add(report['library_sha256'])
            for row in report['rows']:
                record = json.loads((ROOT/row['certificate_path']).read_text())
                from model import sha
                assert sha(record['proof']) == row['certificate_sha256']
            assert file_hash(ROOT/report['library_path']) == report['library_sha256']
            freeze['acquisitions'][f'{repeat}-{arm}'] = {k:report[k] for k in
                ['library_path','library_sha256','library_serialized_bytes','object_ids','query_sha256']}
    assert len(identities) == len(objects) == len(cache) == 1, 'nonreproducible donor construction'
    freeze['identity_checks'] = dict(donor_certificates_identical_across_nine_runs=True,
                                    proof_libraries_identical_across_six_runs=True,
                                    cache_libraries_identical_across_three_runs=True)
    freeze['evidence_files'] = {str(path.relative_to(ROOT)):file_hash(path)
        for path in sorted(a.input.resolve().rglob('*')) if path.is_file() and path != a.output.resolve()}
    write_json(a.output, freeze)
    print(json.dumps(dict(output=str(a.output), proof_library_sha256=next(iter(objects)),
                          geometry_cache_sha256=next(iter(cache)), checks=freeze['identity_checks'])))


if __name__ == '__main__':
    main()
