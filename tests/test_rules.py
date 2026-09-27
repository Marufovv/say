import unittest,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from src.events import EventEngine,merge_segments,OFFICIAL_CLASSES
from src.scene import validate_scene
from src.tracking import Track,Tracker
from solution import RiskEstimator
from evaluate import validate

ROAD=[[0,0],[1,0],[1,1],[0,1]]
def scene(**kw):return validate_scene(dict(verified=True,road=ROAD,crossings=[],queue_zones=[],lanes=[],crossings_complete=True,queue_zones_complete=True,lane_coverage_complete=False,**kw)) if not kw else validate_scene({**scene(),**kw})
def tr(i,label,x,y,t,old=None,stationary=0):
    v=Track(i,label,[x-.04,y-.1,x+.04,y],.9,0,t,hits=20,stationary_since=stationary,anchor=(x,y))
    v.history.extend([(t-1,*(old or (x,y))),(t,x,y)]);return v

class Rules(unittest.TestCase):
    def test_scene_guard(self):
        e=EventEngine(scene(verified=False));e.update([tr(1,'person',.3,.4,1)],1);self.assertEqual(e.finish(2),[])
    def test_stationary_10s_backdated_and_queue_excluded(self):
        e=EventEngine(scene());e.update([tr(1,'car',.3,.4,9)],9);self.assertEqual(e.active,{})
        e.update([tr(1,'car',.3,.4,10)],10);self.assertEqual(e.finish(11),[[0.0,11.0,'stopped_vehicle']])
        e=EventEngine(scene(queue_zones=[ROAD]));e.update([tr(1,'car',.3,.4,11)],11);self.assertEqual(e.finish(12),[])
    def test_crossing_excludes_jaywalking(self):
        e=EventEngine(scene(crossings=[ROAD]));e.update([tr(1,'person',.3,.4,1)],1);self.assertEqual(e.finish(2),[])
    def test_jaywalking(self):
        e=EventEngine(scene());e.update([tr(1,'person',.3,.4,1)],1);self.assertEqual(e.finish(2),[[1.0,2.0,'jaywalking']])
    def test_wrong_way(self):
        e=EventEngine(scene(lanes=[{'polygon':ROAD,'direction':[1,0]}]));e.update([tr(1,'car',.3,.4,1,old=(.4,.4),stationary=1)],1)
        self.assertEqual(e.finish(2),[[1.0,2.0,'wrong_way']])
    def test_yield_requires_movement_and_persists_until_exit(self):
        s=scene(crossings=[ROAD]);e=EventEngine(s)
        e.update([tr(1,'car',.3,.4,1,stationary=1),tr(2,'person',.3,.5,1)],1);self.assertFalse(e.active)
        car=tr(1,'car',.4,.4,2,old=(.3,.4),stationary=2);e.update([car,tr(2,'person',.3,.5,2)],2)
        e.update([car],3);self.assertTrue(any(k[0]=='failure_to_yield' for k in e.active))
    def test_obstacle_animal(self):
        e=EventEngine(scene());e.update([tr(1,'dog',.3,.4,1)],1);self.assertEqual(e.finish(2),[[1.0,2.0,'road_obstacle']])
    def test_congestion_all_lanes_required(self):
        lane={'polygon':ROAD,'direction':[1,0]};s=scene(lanes=[lane],lane_coverage_complete=True,queue_zones_complete=False)
        e=EventEngine(s);e.update([tr(1,'car',.3,.4,1),tr(2,'truck',.6,.5,1)],1);self.assertEqual(e.finish(2),[[1.0,2.0,'congestion']])
    def test_union_no_global_min_duration(self):
        a=merge_segments([[1,2,'accident'],[1.5,3,'accident'],[4,4.2,'near_miss']],5)
        self.assertEqual(a,[[1.0,3.0,'accident'],[4.0,4.2,'near_miss']])
        self.assertEqual(validate({'videos':{'a.mp4':{'events':a,'risk':[]}}})[0],[])
    def test_track_determinism(self):
        rows=[]
        for _ in range(2):
            tracker=Tracker();ids=[]
            for i in range(10):ids.append([t.id for t in tracker.update([{'box':[.1+i*.001,.1,.2+i*.001,.2],'label':'car','confidence':.9}],i*.2)])
            rows.append(ids)
        self.assertEqual(rows[0],rows[1]);self.assertEqual(set(x[0] for x in rows[0]),{1})
    def test_risk_prefix_and_reset(self):
        r=RiskEstimator();r.reset({'video_id':'a'});a=[r.step(None,i) for i in range(5)]
        r.reset({'video_id':'b'});b=[r.step(None,i) for i in range(10)];self.assertEqual(a,b[:5]);self.assertEqual(a,[0.]*5)
    def test_invalid_scene(self):
        with self.assertRaises(ValueError):scene(road=[[0,0],[1,1],[2,0]])
        with self.assertRaises(ValueError):scene(lanes=[{'polygon':ROAD,'direction':[0,0]}])

if __name__=='__main__':unittest.main()
