import unittest,sys
from pathlib import Path
from datetime import datetime,timezone
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
import build_epg as b
class GuideTests(unittest.TestCase):
 def setUp(self):self.now=datetime(2026,11,1,12,tzinfo=timezone.utc)
 def test_timezone_and_exact_mapping_exclude_unknown_and_stale(self):
  xml=b'<tv><programme channel="right" start="20261101170000 +0530" stop="20261101183000 +0530"><title>Real show</title></programme><programme channel="other" start="20261101120000 +0000" stop="20261101130000 +0000"><title>Wrong channel</title></programme><programme channel="right" start="20261030000000 +0000" stop="20261030010000 +0000"><title>Stale</title></programme></tv>'
  ps=b.source_programmes(xml,{'right':['target']},self.now);self.assertEqual(1,len(ps));self.assertEqual('target',ps[0].get('channel'));self.assertEqual('Real show',ps[0].findtext('title'))
 def test_empty_schedule_cannot_replace_good_guide(self):
  cfg={'channels':{'target':{'name':'One','source':'source','source_channel':'right'}}}
  with self.assertRaises(ValueError):b.build(cfg,lambda url:b'<tv/>',self.now)
 def test_no_fake_programmes_and_deterministic_gzip(self):
  cfg={'channels':{'target':{'name':'One','source':'source','source_channel':'right'}}};xml=b'<tv><programme channel="right" start="20261101120000 +0000" stop="20261101130000 +0000"><title>Actual title</title></programme></tv>'
  first,counts=b.build(cfg,lambda url:xml,self.now);second,_=b.build(cfg,lambda url:xml,self.now);self.assertEqual(first,second);self.assertEqual({'target':1},counts)
 def test_dtd_and_bad_xml_are_rejected(self):
  for xml in [b'<!DOCTYPE tv><tv/>',b'<tv><programme>']:
   with self.assertRaises(Exception):b.source_programmes(xml,{},self.now)
if __name__=='__main__':unittest.main()
