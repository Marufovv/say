import unittest,sys,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from src.compliance import validate_annotations,BOUNDARIES
from src.scene import validate_scene
from src.events import OFFICIAL_CLASSES,EventEngine
from src.live import infer_jpeg
from evaluate import validate
from test_rules import scene,tr,ROAD

class Compliance(unittest.TestCase):
    def test_all_official_boundaries_and_export(self):
        self.assertEqual([r[0] for r in BOUNDARIES],OFFICIAL_CLASSES)
        events=validate_annotations([[0,1,c] for c in OFFICIAL_CLASSES],2)
        self.assertEqual(validate({'team':'test','videos':{'test.mp4':{'events':events,'risk':[]}}})[0],[])
    def test_review_rejects_bad_bounds_and_labels(self):
        for row in [[0,3,'accident'],[1,1,'accident'],[True,1,'accident'],[0,float('inf'),'accident'],[float('nan'),1,'accident'],[0,1,'speeding']]:
            with self.assertRaises(ValueError):validate_annotations([row],2)
    def test_same_class_union_different_class_overlap(self):
        self.assertEqual(validate_annotations([[0,1,'accident'],[.5,2,'accident'],[.5,1,'near_miss']],2),[[0.0,2.0,'accident'],[.5,1.0,'near_miss']])
    def test_islands_not_jaywalking(self):
        e=EventEngine(scene(exclusions=[ROAD]));e.update([tr(1,'person',.3,.4,1)],1);self.assertEqual(e.finish(2),[])
    def test_strict_scene_flags_numbers(self):
        for s in [{'verified':'false'},{'analysis_fps':float('nan')},{'confidence':True}]:
            with self.assertRaises(ValueError):validate_scene(s)
    def test_camera_rejects_non_jpeg_and_oversized_input(self):
        for data in [b'not a jpeg',b'x'*(1024*1024+1)]:
            with self.assertRaises(ValueError):infer_jpeg(data)

if __name__=='__main__':unittest.main()
