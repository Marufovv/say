"""YOLOX-S ONNX adapter. Decode/preprocess follows OpenCV Zoo YOLOX (Apache-2.0).
Locally authored adapter: normalized boxes, road-user filtering, classwise NMS.
No network access during inference. See weights/LICENSE-YOLOX.txt and NOTICE.md.
"""
from pathlib import Path
import cv2
import numpy as np

NAMES = {0:'person',1:'bicycle',2:'car',3:'motorcycle',5:'bus',7:'truck',9:'traffic_light',15:'cat',16:'dog',17:'horse',18:'sheep',19:'cow'}
VEHICLES = {'bicycle','car','motorcycle','bus','truck'}
ANIMALS = {'cat','dog','horse','sheep','cow'}

class Detector:
    def __init__(self, weights: str | Path, confidence=0.45):
        p=Path(weights)
        if not p.exists():
            raise FileNotFoundError('Model topilmadi. Avval weights/download.sh ni ishga tushiring.')
        cv2.setNumThreads(4)
        self.net=cv2.dnn.readNetFromONNX(str(p))
        self.confidence=float(confidence)
        grids=[]; strides=[]
        for s in (8,16,32):
            x,y=np.meshgrid(np.arange(640//s),np.arange(640//s))
            g=np.stack((x,y),axis=-1).reshape(-1,2)
            grids.append(g);strides.append(np.full((len(g),1),s))
        self.grid=np.concatenate(grids);self.strides=np.concatenate(strides)

    def detect(self, frame):
        h,w=frame.shape[:2];scale=min(640/w,640/h)
        resized=cv2.resize(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB),(int(w*scale),int(h*scale)))
        padded=np.full((640,640,3),114,dtype=np.float32)
        padded[:resized.shape[0],:resized.shape[1]]=resized
        self.net.setInput(padded.transpose(2,0,1)[None])
        raw=self.net.forward()[0].copy()
        raw[:,:2]=(raw[:,:2]+self.grid)*self.strides
        raw[:,2:4]=np.exp(np.clip(raw[:,2:4],-20,20))*self.strides
        scores=raw[:,4,None]*raw[:,5:];labels=scores.argmax(1);conf=scores.max(1)
        selected=np.where((conf>=self.confidence)&np.isin(labels,list(NAMES)))[0]
        boxes=np.column_stack((raw[:,0]-raw[:,2]/2,raw[:,1]-raw[:,3]/2,raw[:,2],raw[:,3]))
        result=[]
        for cls in sorted(set(labels[selected].tolist())):
            ids=selected[labels[selected]==cls]
            keep=cv2.dnn.NMSBoxes(boxes[ids].tolist(),conf[ids].tolist(),self.confidence,0.5)
            for k in np.asarray(keep).reshape(-1):
                i=ids[int(k)];x,y,bw,bh=boxes[i]/scale
                b=[max(0,float(x/w)),max(0,float(y/h)),min(1,float((x+bw)/w)),min(1,float((y+bh)/h))]
                if b[2]>b[0] and b[3]>b[1]:
                    result.append({'box':b,'label':NAMES[cls],'confidence':round(float(conf[i]),4)})
        return sorted(result,key=lambda d:(d['label'],d['box'][0],d['box'][1]))
