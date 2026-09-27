"""Restore the four supplied excerpts and their measured results on a fresh install."""
import json,shutil

def restore_demo(root,data):
    seed=root/'demo'
    if not seed.exists():return
    for p in (seed/'videos').glob('*/meta.json'):
        meta=json.loads(p.read_text());out=data/'videos'/p.parent.name
        if (out/'meta.json').exists():continue
        sample=root/'samples/excerpts'/meta['name']
        if not sample.exists():continue
        out.mkdir(parents=True,exist_ok=True)
        shutil.copy2(sample,out/'video.mp4');shutil.copy2(p.parent/'poster.jpg',out/'poster.jpg')
        shutil.copy2(p,out/'meta.json')
    for p in (seed/'jobs').glob('*/status.json'):
        out=data/'jobs'/p.parent.name
        if not out.exists():shutil.copytree(p.parent,out)
