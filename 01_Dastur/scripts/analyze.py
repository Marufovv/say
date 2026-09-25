#!/usr/bin/env python3
"""Local EDA + detections for full-size videos; no demo upload/duration cap."""
import sys,argparse,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from src.pipeline import analyze,official_prediction
from src.scene import load_scene
p=argparse.ArgumentParser();p.add_argument('video');p.add_argument('--scene');p.add_argument('--out',default='analysis');p.add_argument('--team',default='unnamed-team');args=p.parse_args()
out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
last=[-1]
def progress(value,message,stats):
    percent=int(value*100)
    if percent!=last[0]:print(f'{percent:3}% {message}',flush=True);last[0]=percent
result=analyze(args.video,load_scene(args.scene),progress=progress)
heat=result.pop('_heatmap',None)
if heat:(out/'heatmap.jpg').write_bytes(heat)
(out/'result.json').write_text(json.dumps(result,ensure_ascii=False))
(out/'predictions.json').write_text(json.dumps(official_prediction(result,Path(args.video).name,args.team),ensure_ascii=False))
print(f'Tayyor: {out.resolve()}. {len(result["events"])} hodisa; {result["unique_tracks"]} iz; {result["runtime_sec"]} s.')
