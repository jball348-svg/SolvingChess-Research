"""Cumulative admission controls; synthetic records, no benchmark generation."""
import copy
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from rp3 import admission, CAP

class RP3Checks(unittest.TestCase):
    def test_new_quota_preserves_inherited_first_witness_and_checks_duplicates(self):
        old=[dict(id=str(i),template='first') for i in range(8)]
        lib=dict(entries=copy.deepcopy(old));seen=set(range(8))
        self.assertEqual(admission(lib,dict(id='replacement'),0,seen,3,8,False),'DUPLICATE')
        for i in range(8,16):
            self.assertEqual(admission(lib,dict(id=str(i)),i,seen,3,8,False),'ACCEPTED')
        self.assertEqual(lib['entries'][:8],old)
        self.assertEqual(admission(lib,dict(id='17'),17,seen,3,8,False),'GEOMETRY_CAP')
        self.assertEqual(admission(lib,dict(id='15-alt'),15,seen,3,8,False),'DUPLICATE')

    def test_storage_rejection_does_not_evict_or_poison_seen(self):
        lib=dict(entries=[dict(id='old')]);seen={'old'}
        self.assertEqual(admission(lib,dict(id='big',payload='x'*CAP),'big',seen,1,1,True),'BYTE_CAP')
        self.assertEqual(lib['entries'],[dict(id='old')]);self.assertNotIn('big',seen)
        self.assertEqual(admission(lib,dict(id='small'),'small',seen,3000,1,True),'ACCEPTED')
        self.assertEqual(admission(lib,dict(id='nodes'),'nodes',seen,2049,1,False),'NODE_CAP')

if __name__=='__main__':unittest.main()
