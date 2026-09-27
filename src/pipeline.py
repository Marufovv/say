from pathlib import Path
from collections import Counter
import hashlib,json,time,threading
import cv2
import numpy as np
from .detector import Detector
from .tracking import Tracker
from .events import EventEngine
from .scene import ROOT,load_scene,validate_scene,capabilities
from .alignment import align_scene

_detector=None
_detector_conf=None
_lock=threading.Lock()

def video_metadata(path):
    cap=cv2.VideoCapture(str(path))
    try:
        if not cap.isOpened():raise ValueError('Video ochilmadi. Yaroqli MP4 fayl tanlang.')
        fps=float(cap.get(cv2.CAP_PROP_FPS));n=int(cap.get(cv2.CAP_PROP_FRAME_COUNT));w=int(cap.get(cv2.CAP_PROP_FRAME_WIDTH));h=int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        if not np.isfinite(fps) or fps<=0 or n<=0 or w<=0 or h<=0:raise ValueError('Video metadata noto‘g‘ri yoki fayl buzilgan.')
        return {'fps':fps,'n_frames':n,'width':w,'height':h,'duration':n/fps,'video_id':Path(path).name}
    finally:cap.release()

def analyze(path,scene=None,progress=None,cancel=None,collect=True):
    global _detector,_detector_conf
    scene=validate_scene(scene) if scene is not None else load_scene()
    meta=video_metadata(path);begin=time.perf_counter();stride=max(1,round(meta['fps']/scene['analysis_fps']))
    with _lock:
        if _detector is None or _detector_conf!=scene['confidence']:
            if progress:progress(0,'Model yuklanmoqda',{})
            _detector=Detector(ROOT/'weights/yolox_s.onnx',scene['confidence']);_detector_conf=scene['confidence']
        alignment={'status':'not_requested'}
        if scene.get('alignment_required'):
            preview=cv2.VideoCapture(str(path));ok,first_frame=preview.read();preview.release()
            if not ok:raise ValueError('Kamera mosligini tekshirish uchun birinchi kadr o‘qilmadi.')
            scene,alignment=align_scene(scene,first_frame)
        tracker=Tracker(max_gap=max(.8,2*stride/meta['fps']));engine=EventEngine(scene)
        cap=cv2.VideoCapture(str(path));idx=0;records=[];series=[];counts=Counter();seen=set();heat=np.zeros((72,128),np.float32);first=None
        try:
            while cap.grab():
                if cancel and cancel.is_set():raise InterruptedError('Tahlil bekor qilindi.')
                if idx%stride==0:
                    ok,frame=cap.retrieve()
                    if not ok:raise ValueError(f'{idx}-kadrni o‘qib bo‘lmadi.')
                    if first is None:first=frame.copy()
                    t=idx/meta['fps'];detections=_detector.detect(frame);tracks=tracker.update(detections,t);engine.update(tracks,t)
                    current=Counter(tr.label for tr in tracks)
                    for tr in tracks:
                        if tr.id not in seen:counts[tr.label]+=1;seen.add(tr.id)
                        x,y=tr.point;heat[min(71,int(y*72)),min(127,int(x*128))]+=1
                    if collect:
                        records.append({'t':round(t,4),'objects':[tr.json() for tr in tracks]})
                        series.append({'t':round(t,3),'count':len(tracks),'vehicles':sum(n for k,n in current.items() if k in {'car','truck','bus','motorcycle','bicycle'}),'people':current.get('person',0)})
                    if progress:progress(min(.99,idx/meta['n_frames']),'Video tahlil qilinmoqda',{'frame':idx,'objects':len(seen),'elapsed':round(time.perf_counter()-begin,1)})
                idx+=1
        finally:cap.release()
        if idx==0:raise ValueError('Videoda o‘qiladigan kadr topilmadi.')
        if abs(idx-meta['n_frames'])>max(2,meta['fps']*.1):
            raise ValueError(f'Video to‘liq o‘qilmadi: {idx}/{meta["n_frames"]} kadr. Qisman natija chiqarilmadi.')
        duration=idx/meta['fps'];events=engine.finish(duration);elapsed=time.perf_counter()-begin
        warnings=[]
        if alignment['status']=='rejected':warnings.append(alignment['reason']+' Hodisa qoidalari o‘chirildi.')
        if not scene['verified']:warnings.append('Sahna tasdiqlanmagan: obyektlar tahlil qilindi, hodisa qoidalari o‘chirilgan.')
        if elapsed>3*duration:warnings.append('Ushbu qurilmada 3× vaqt chegarasi oshdi. Rasmiy harness bu videoni bo‘sh natija deb oladi.')
        warnings.append('Hodisa qoidalari evristik; natijalar inson tekshiruvini talab qiladi. Part B nol baseline.')
        result={'meta':{**meta,'decoded_frames':idx,'duration':duration},'events':events,'event_details':engine.details,
                'frames':records,'series':series,'track_counts':dict(counts),'unique_tracks':len(seen),
                'runtime_sec':round(elapsed,3),'runtime_ratio':round(elapsed/duration,3),'sample_stride':stride,
                'enabled_classes':[k for k,v in capabilities(scene).items() if v],
                'warnings':warnings,'scene':scene,'alignment':alignment,'part_b':'zero_baseline','model':'YOLOX-S / OpenCV Zoo',
                'model_sha256':model_hash()}
        if collect and first is not None:
            small=cv2.resize(first,(640,int(first.shape[0]*640/first.shape[1])))
            colored=cv2.applyColorMap(cv2.normalize(cv2.GaussianBlur(heat,(7,7),0),None,0,255,cv2.NORM_MINMAX).astype(np.uint8),cv2.COLORMAP_TURBO)
            colored=cv2.resize(colored,(small.shape[1],small.shape[0]))
            overlay=cv2.addWeighted(small,.65,colored,.35,0) if heat.max()>0 else small
            result['_heatmap']=cv2.imencode('.jpg',overlay)[1].tobytes()
        if progress:progress(1,'Tayyor',{'frame':idx,'objects':len(seen),'elapsed':round(elapsed,1)})
        return result

_hash=None
def model_hash():
    global _hash
    if _hash is None:
        p=ROOT/'weights/yolox_s.onnx';_hash=hashlib.sha256(p.read_bytes()).hexdigest()
    return _hash

def official_prediction(result,name,team='unnamed-team'):
    meta=result['meta']
    return {'team':team,'videos':{name:{'events':result['events'],'risk':[[round(i/meta['fps'],4),0.0] for i in range(meta['decoded_frames'])]}}}
