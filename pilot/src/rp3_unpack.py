"""Verify and materialize compact RP3 raw evidence for read-only reconciliation."""
import hashlib
import json
from pathlib import Path
import tarfile

ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'pilot/evidence/rp3'


def digest(data):return hashlib.sha256(data).hexdigest()


def main():
    index=json.loads((BASE/'raw-index.json').read_text())
    archive=BASE/'raw-evidence.tar.gz'
    assert digest(archive.read_bytes())==index['archive_sha256'],'archive identity'
    with tarfile.open(archive,'r:gz') as bundle:
        assert {m.name for m in bundle.getmembers()}==set(index['members']),'member set'
        for member in bundle.getmembers():
            assert member.isfile() and not member.issym() and not member.islnk()
            path=(ROOT/member.name).resolve()
            assert path.is_relative_to(BASE.resolve()) and path.parent!=BASE.resolve()
            assert member.name.startswith(('pilot/evidence/rp3/acquire-','pilot/evidence/rp3/evaluate-'))
            data=bundle.extractfile(member).read();record=index['members'][member.name]
            assert len(data)==record['bytes'] and digest(data)==record['sha256'],member.name
            if path.exists():assert path.read_bytes()==data,'refusing overwrite '+member.name
            else:
                path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
    print(json.dumps(dict(verified_members=len(index['members']),raw_bytes=sum(x['bytes'] for x in index['members'].values()))))


if __name__=='__main__':main()
