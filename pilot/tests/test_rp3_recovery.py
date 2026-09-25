"""Persistence fault controls and a known RP1 fixture; no reserved generator."""
import contextlib
import copy
import io
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
import reuse
import rp2
import rp3
from model import Arena, sha
from rp2_summary import stable
from rp3_durable import read, write_json, validate
from rp3_durable_v2 import write_json as write_json_v2
from rp3_recovery_run import Run


class RecoveryChecks(unittest.TestCase):
    def test_atomic_failure_preserves_previous_record(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'report.json';write_json(path,{'version':1})
            with patch('rp3_durable.os.replace',side_effect=OSError('injected interruption')):
                with self.assertRaises(OSError):write_json(path,{'version':2})
            self.assertEqual(read(path),{'version':1})

    def test_v2_writer_readback_and_unique_temporary(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'report.json'
            write_json_v2(path,{'version':1})
            write_json_v2(path,{'version':2,'rows':[1,2,3]})
            self.assertEqual(path.read_text(), '{"rows":[1,2,3],"version":2}\n')
            self.assertEqual(list(Path(d).glob('*.pending')), [])
            self.assertEqual(list(Path(d).glob('.*.pending')), [])

    def test_same_known_fixture_and_detect_missing_measurements(self):
        original_check=reuse.check
        query=dict(id='rp1-known-fixture',fen='8/8/8/8/2k5/8/K7/1R6 w - - 0 1',moves=[])
        arena=Arena(3,4)
        try:
            with tempfile.TemporaryDirectory(dir=rp2.ROOT/'pilot/.work') as d:
                reports=[]
                for name,cls in [('frozen',rp3.Run),('durable',Run)]:
                    directory=Path(d)/name
                    args=SimpleNamespace(mode='evaluate',arm='B',repeat=1,rung='r2',diagnostic='primary',
                        output=directory/'report.json',freeze=rp2.ROOT/'pilot/evidence/rp2/donor-freeze.json',
                        source_freeze=rp2.ROOT/'pilot/evidence/rp3/source-freeze.json')
                    with contextlib.ExitStack() as stack:
                        if name=='durable':
                            stack.enter_context(patch.object(rp2,'write_json',write_json))
                            stack.enter_context(patch.object(rp3,'write_json',write_json))
                        run=cls(args)
                        run.report.update(queries=[query],query_sha256=sha([query]),arena=arena.spec(),plies=6)
                        run.solve_queries(arena,[query])
                        with contextlib.redirect_stdout(io.StringIO()):run.finish()
                        reports.append(run.report)
                self.assertEqual(stable(reports[0]),stable(reports[1]))
                validate(directory,1)
                intact=read(directory/'report.json')
                damaged=copy.deepcopy(intact);damaged['rows']=[]
                write_json(directory/'report.json',damaged)
                with self.assertRaisesRegex(AssertionError,'incomplete measurement'):validate(directory,1)
                damaged=copy.deepcopy(intact);damaged.pop('search_counts')
                write_json(directory/'report.json',damaged)
                with self.assertRaises(KeyError):validate(directory,1)
                damaged=copy.deepcopy(intact);damaged['event_counts']={'application:ACCEPTED':1}
                write_json(directory/'report.json',damaged)
                with self.assertRaisesRegex(AssertionError,'event tail'):validate(directory,1)
                write_json(directory/'report.json',intact)
                (directory/'rows.jsonl').write_text('')
                with self.assertRaisesRegex(AssertionError,'journal'):validate(directory,1)
        finally:
            reuse.check=original_check


if __name__=='__main__':unittest.main()
