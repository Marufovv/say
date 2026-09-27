import json,math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SUPPORTED=['stopped_vehicle','jaywalking','wrong_way','failure_to_yield','congestion','road_obstacle']

def validate_scene(s):
    if not isinstance(s,dict):raise ValueError('Sahna sozlamasi JSON obyekt bo‘lishi kerak.')
    flags=['verified','crossings_complete','queue_zones_complete','lane_coverage_complete','alignment_required']
    if any(not isinstance(s.get(k,False),bool) for k in flags):raise ValueError('Tasdiqlash maydonlari true/false bo‘lsin.')
    out={k:s.get(k,False) for k in flags}
    def polygon(p):
        if not isinstance(p,list) or not 3<=len(p)<=80:raise ValueError('Zona 3–80 nuqtadan iborat bo‘lsin.')
        pts=[]
        for q in p:
            if not isinstance(q,list) or len(q)!=2:raise ValueError('Nuqta [x,y] bo‘lsin.')
            if any(isinstance(v,bool) or not isinstance(v,(int,float)) or not math.isfinite(v) or not 0<=v<=1 for v in q):raise ValueError('Koordinatalar 0–1 oralig‘ida bo‘lsin.')
            pts.append([float(q[0]),float(q[1])])
        area=abs(sum(pts[i][0]*pts[(i+1)%len(pts)][1]-pts[(i+1)%len(pts)][0]*pts[i][1] for i in range(len(pts))))/2
        if area<0.00001:raise ValueError('Zona yuzasi juda kichik.')
        return pts
    out['road']=polygon(s['road']) if s.get('road') else []
    for name in ['crossings','queue_zones','exclusions']:
        ps=s.get(name,[])
        if not isinstance(ps,list) or len(ps)>30:raise ValueError('Zonalar ro‘yxati noto‘g‘ri.')
        out[name]=[polygon(p) for p in ps]
    lanes=s.get('lanes',[])
    if not isinstance(lanes,list) or len(lanes)>30:raise ValueError('Yo‘laklar ro‘yxati noto‘g‘ri.')
    out['lanes']=[]
    for i,l in enumerate(lanes):
        if not isinstance(l,dict):raise ValueError('Yo‘lak JSON obyekt bo‘lsin.')
        d=l.get('direction',[])
        if not isinstance(d,list) or len(d)!=2 or any(isinstance(v,bool) or not isinstance(v,(int,float)) or not math.isfinite(v) or abs(v)>2 for v in d) or math.hypot(*d)<0.001:raise ValueError('Yo‘lakning ruxsat etilgan yo‘nalishini belgilang.')
        out['lanes'].append({'polygon':polygon(l['polygon']),'direction':d,'group':str(l.get('group','1'))[:30],'name':str(l.get('name',f'Yo‘lak {i+1}'))[:60]})
    for key,default,low,high in [('analysis_fps',5,1,10),('confidence',.45,.2,.9)]:
        v=s.get(key,default)
        if isinstance(v,bool) or not isinstance(v,(int,float)) or not math.isfinite(v):raise ValueError('Sozlama sonlari finite bo‘lsin.')
        out[key]=max(low,min(high,float(v)))
    out['source_note']=str(s.get('source_note',''))[:1000]
    return out

def load_scene(path=None):
    return validate_scene(json.loads(Path(path or ROOT/'configs/scene.json').read_text()))

def capabilities(scene):
    road=bool(scene['verified'] and scene['road'])
    enabled={
        'stopped_vehicle':road and scene['queue_zones_complete'],
        'jaywalking':road and scene['crossings_complete'],
        'wrong_way':road and bool(scene['lanes']),
        'failure_to_yield':road and bool(scene['crossings']),
        'road_obstacle':road,
        'congestion':road and scene['lane_coverage_complete'] and bool(scene['lanes'])}
    return enabled
