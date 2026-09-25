#!/usr/bin/env python3
"""Register a local supplied sample without modifying its source; optionally run real inference."""
import argparse,hashlib,json,os,sys,time,uuid
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import cv2
from src.scene import ROOT
from src.pipeline import video_metadata,analyze,official_prediction

def run():
    p=argparse.ArgumentParser();p.add_argument('video',type=Path);p.add_argument('--excerpt',action='store_true');p.add_argument('--analyze',action='store_true');p.add_argument('--team',default='unnamed-team');args=p.parse_args()
    source=args.video.resolve();meta=video_metadata(source);vid=uuid.uuid5(uuid.NAMESPACE_URL,str(source)).hex
    folder=ROOT/'.local/videos'/vid;folder.mkdir(parents=True,exist_ok=True)
    target=folder/'video.mp4'
    if not target.exists():target.symlink_to(source)
    cap=cv2.VideoCapture(str(source));ok,f=cap.read();cap.release()
    if not ok:raise ValueError('Birinchi kadr o‘qilmadi.')
    cv2.imwrite(str(folder/'poster.jpg'),cv2.resize(f,(1280,round(f.shape[0]*1280/f.shape[1]))))
    sha=hashlib.file_digest(source.open('rb'),'sha256').hexdigest()
    row={**meta,'id':vid,'name':source.name,'bytes':source.stat().st_size,'created':time.time(),'source':'provided_sample_excerpt' if args.excerpt else 'provided_sample','sha256':sha}
    (folder/'meta.json').write_text(json.dumps(row,ensure_ascii=False));print(json.dumps(row),flush=True)
    if args.analyze:
        jid=uuid.uuid4().hex;out=ROOT/'.local/jobs'/jid;out.mkdir()
        status={'id':jid,'video_id':vid,'name':source.name,'created':time.time(),'status':'running','progress':0,'message':'Haqiqiy video tahlili'}
        (out/'status.json').write_text(json.dumps(status))
        try:
            result=analyze(source);heat=result.pop('_heatmap',None)
            if heat:(out/'heatmap.jpg').write_bytes(heat)
            result['meta']['video_id']=source.name
            (out/'result.json').write_text(json.dumps(result,ensure_ascii=False))
            (out/'predictions.json').write_text(json.dumps(official_prediction(result,source.name,args.team)))
            status.update(status='done',progress=1,message='Tahlil tayyor',events=len(result['events']))
            print(json.dumps({k:result[k] for k in ['events','unique_tracks','runtime_sec','runtime_ratio','alignment']}),flush=True)
        except Exception as e:
            status.update(status='error',message=str(e));raise
        finally:(out/'status.json').write_text(json.dumps(status,ensure_ascii=False))
if __name__=='__main__':run()
