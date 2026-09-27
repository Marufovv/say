"""Explicit browser-camera frame inference; frames are not saved or used for training."""
import threading,time
import cv2
import numpy as np
from .detector import Detector
from .scene import ROOT

_lock=threading.Lock()
_detector=None

def infer_jpeg(data):
    global _detector
    # Browser sends a bounded 640px JPEG. Reject unreasonable compressed image dimensions
    # before OpenCV allocates its decoded image.
    if len(data)>1024*1024:raise ValueError('Kadr hajmi 1 MB dan oshmasin.')
    if not data.startswith(b'\xff\xd8'):raise ValueError('JPEG kadr yuboring.')
    i=2;dimensions=None
    while i+4<len(data):
        if data[i]!=255:break
        marker=data[i+1];i+=2
        length=int.from_bytes(data[i:i+2],'big')
        if length<2:break
        if marker in (0xc0,0xc1,0xc2):
            dimensions=(int.from_bytes(data[i+3:i+5],'big'),int.from_bytes(data[i+5:i+7],'big'));break
        i+=length
    if not dimensions or min(dimensions)<=0 or max(dimensions)>1920:raise ValueError('Kadr tomonlari 1920 pikseldan oshmasin.')
    frame=cv2.imdecode(np.frombuffer(data,np.uint8),cv2.IMREAD_COLOR)
    if frame is None:raise ValueError('Kadr o‘qilmadi.')
    if not _lock.acquire(blocking=False):raise RuntimeError('Kamera tahlili band.')
    try:
        if _detector is None:_detector=Detector(ROOT/'weights/yolox_s.onnx',.45)
        start=time.perf_counter();objects=_detector.detect(frame)
        return {'objects':objects,'latency_ms':round((time.perf_counter()-start)*1000),'width':frame.shape[1],'height':frame.shape[0],'mode':'objects_only'}
    finally:_lock.release()
