"""Scene-gated temporal rules. Pixel geometry is NOT calibrated speed/contact evidence."""
import math
import cv2
import numpy as np
from .detector import VEHICLES, ANIMALS
from .scene import capabilities

OFFICIAL_CLASSES=['accident','near_miss','red_light','wrong_way','illegal_u_turn','stopped_vehicle','jaywalking','failure_to_yield','illegal_turn','solid_line_crossing','stop_line','congestion','road_obstacle','fire_smoke']

def inside(point,polygon):
    return bool(polygon) and cv2.pointPolygonTest(np.asarray(polygon,dtype=np.float32),tuple(map(float,point)),False)>=0

def merge_segments(events,duration):
    out=[]
    for label in OFFICIAL_CLASSES:
        rows=sorted((max(0,float(s)),min(duration,float(e))) for s,e,l in events if l==label and math.isfinite(s) and math.isfinite(e))
        merged=[]
        for s,e in rows:
            if e<=s:continue
            if merged and s<=merged[-1][1]+1e-8:merged[-1][1]=max(merged[-1][1],e)
            else:merged.append([s,e])
        for s,e in merged:
            # Millisecond quantization compatible with the unchanged harness.
            a,b=round(s,3),round(e,3)
            b=min(b,math.floor(duration*1000)/1000)
            if a<b:out.append([a,b,label])
    return sorted(out)

class EventEngine:
    def __init__(self,scene):
        self.scene=scene;self.enabled=capabilities(scene);self.active={};self.finished=[];self.details=[]
    def update(self,tracks,t):
        flags={};s=self.scene
        def on_road(point):return inside(point,s['road']) and not any(inside(point,p) for p in s.get('exclusions',[]))
        vehicles=[tr for tr in tracks if tr.label in VEHICLES and tr.hits>=3 and on_road(tr.point)]
        pedestrians=[tr for tr in tracks if tr.label=='person' and tr.hits>=3]
        def flag(label,key,start=None,reason=''):
            if self.enabled.get(label):flags[(label,str(key))]=(t if start is None else start,reason)
        for tr in vehicles:
            queued=any(inside(tr.point,p) for p in s['queue_zones'])
            if not queued and t-tr.stationary_since>=10:
                flag('stopped_vehicle',tr.id,tr.stationary_since,'Qatnovdagi iz kamida 10 soniya harakatsiz; navbat zonasidan tashqarida.')
            for i,lane in enumerate(s['lanes']):
                key=str(i)
                if inside(tr.point,lane['polygon']):
                    tr.lane_enter.setdefault(key,t)
                    vx,vy=tr.velocity();dx,dy=lane['direction'];dot=(vx*dx+vy*dy)/math.hypot(dx,dy)
                    if dot < -0.005 or ('wrong_way',f'{tr.id}:{i}') in self.active:flag('wrong_way',f'{tr.id}:{i}',tr.lane_enter[key],'Iz tasdiqlangan yo‘lak yo‘nalishiga qarshi harakat qilmoqda.')
                else:tr.lane_enter.pop(key,None)
            for i,crossing in enumerate(s['crossings']):
                if inside(tr.point,crossing):
                    ck=f'crossing:{i}';tr.lane_enter.setdefault(ck,t)
                    moving=math.hypot(*tr.velocity())>.002
                    if (moving and any(inside(p.point,crossing) for p in pedestrians)) or ('failure_to_yield',f'{tr.id}:{i}') in self.active:
                        flag('failure_to_yield',f'{tr.id}:{i}',tr.lane_enter[ck],reason='Transport va piyoda crossing hududida bir vaqtning o‘zida qayd etildi; inson ko‘rigi kerak.')
                else:tr.lane_enter.pop(f'crossing:{i}',None)
        for tr in pedestrians:
            if on_road(tr.point) and not any(inside(tr.point,p) for p in s['crossings']):
                flag('jaywalking',tr.id,reason='Piyoda qatnov hududida, belgilangan crossinglardan tashqarida.')
        for tr in tracks:
            if tr.hits>=3 and tr.label in ANIMALS and on_road(tr.point):
                flag('road_obstacle',tr.id,reason='Qatnov hududida hayvon aniqlandi. Boshqa turdagi to‘siqlar bu modelda qo‘llab-quvvatlanmaydi.')
        groups={l['group'] for l in s['lanes']}
        for group in groups:
            lanes=[l for l in s['lanes'] if l['group']==group]
            queues=[[tr for tr in vehicles if inside(tr.point,l['polygon'])] for l in lanes]
            if queues and all(len(q)>=2 and all(math.hypot(*tr.velocity())<.003 and tr.hits>=5 for tr in q) for q in queues):
                flag('congestion',group,reason='Yo‘nalishning barcha belgilangan yo‘laklarida kamida 2 ta sekin/harakatsiz iz.')
        for key in list(self.active):
            if key not in flags:self._close(key,t)
        for key,(start,reason) in flags.items():
            if key not in self.active:self.active[key]={'start':start,'last':t,'reason':reason}
            else:self.active[key]['last']=t
    def _close(self,key,end):
        a=self.active.pop(key);label,object_id=key
        if end>a['start']:
            self.finished.append([a['start'],end,label]);self.details.append({'start':round(a['start'],3),'end':round(end,3),'label':label,'track':object_id,'evidence':a['reason'],'review_required':True})
    def finish(self,duration):
        for key in list(self.active):self._close(key,duration)
        return merge_segments(self.finished,duration)
