"""Deterministic greedy IoU/position tracker. IDs are estimates, not identities."""
from collections import deque
from dataclasses import dataclass, field
import math

def iou(a,b):
    area=max(0,min(a[2],b[2])-max(a[0],b[0]))*max(0,min(a[3],b[3])-max(a[1],b[1]))
    union=(a[2]-a[0])*(a[3]-a[1])+(b[2]-b[0])*(b[3]-b[1])-area
    return area/union if union>0 else 0

def foot(b): return ((b[0]+b[2])/2,b[3])

@dataclass
class Track:
    id:int
    label:str
    box:list
    confidence:float
    first:float
    last:float
    hits:int=1
    history:deque=field(default_factory=lambda:deque(maxlen=100))
    stationary_since:float=0
    anchor:tuple=(0,0)
    lane_enter:dict=field(default_factory=dict)

    @property
    def point(self):return foot(self.box)
    def velocity(self):
        if len(self.history)<2:return (0.0,0.0)
        recent=[x for x in self.history if self.last-x[0]<=1.5]
        old=recent[0];new=recent[-1];dt=new[0]-old[0]
        if dt<0.3:return (0.0,0.0)
        return ((new[1]-old[1])/dt,(new[2]-old[2])/dt)
    def update(self,det,t):
        self.box=det['box'];self.confidence=det['confidence'];self.last=t;self.hits+=1
        x,y=self.point;self.history.append((t,x,y))
        tolerance=max(0.0025,(self.box[3]-self.box[1])*0.045)
        if math.dist((x,y),self.anchor)>tolerance:
            self.stationary_since=t;self.anchor=(x,y)
    def json(self):
        return {'id':self.id,'label':self.label,'box':[round(x,5) for x in self.box],
                'confidence':self.confidence,'point':list(self.point),
                'trail':[[round(x,5),round(y,5)] for _,x,y in list(self.history)[-35:]]}

class Tracker:
    def __init__(self,max_gap=0.8):self.tracks={};self.next_id=1;self.max_gap=max_gap
    def update(self,detections,t):
        self.tracks={i:tr for i,tr in self.tracks.items() if t-tr.last<=self.max_gap}
        pairs=[]
        for i,tr in self.tracks.items():
            for j,d in enumerate(detections):
                if tr.label!=d['label']:continue
                overlap=iou(tr.box,d['box']);dist=math.dist(tr.point,foot(d['box']))
                gate=max(0.025,(tr.box[3]-tr.box[1])*0.6)
                if overlap>0.12 or dist<gate:pairs.append((overlap+max(0,1-dist/gate)*0.25,i,j))
        used_t=set();used_d=set();active=[]
        for _,i,j in sorted(pairs,reverse=True):
            if i in used_t or j in used_d:continue
            tr=self.tracks[i];tr.update(detections[j],t);active.append(tr);used_t.add(i);used_d.add(j)
        for j,d in enumerate(detections):
            if j in used_d:continue
            i=self.next_id;self.next_id+=1;p=foot(d['box'])
            tr=Track(i,d['label'],d['box'],d['confidence'],t,t,stationary_since=t,anchor=p)
            tr.history.append((t,*p));self.tracks[i]=tr;active.append(tr)
        return sorted(active,key=lambda tr:tr.id)
