"""Assemble an app for hosting from either the flat or six-folder upload layout.
Copies only; never changes the uploaded originals. Run in a separate build directory.
"""
from pathlib import Path
import argparse,shutil

def prepare(source,target):
    source=Path(source).resolve();target=Path(target).resolve()
    if target==source or source in target.parents:raise ValueError('Target must be outside the source tree.')
    if target.exists() and any(target.iterdir()):raise ValueError('Target must be empty.')
    target.mkdir(parents=True,exist_ok=True)
    base=source/'01_Dastur' if (source/'01_Dastur/app.py').exists() else source
    shutil.copytree(base,target,dirs_exist_ok=True,ignore=shutil.ignore_patterns('.git','.local','.venv','__pycache__','.env'))
    for group,sub in [('02_Hisobotlar','docs'),('03_Natijalar','demo'),('04_Videolar','samples'),('05_Model_1','weights'),('06_Model_2','weights')]:
        p=source/group/sub
        if p.exists():shutil.copytree(p,target/sub,dirs_exist_ok=True)
    required=['app.py','requirements.txt','scripts/serve.py','configs/project.json','web/index.html','weights/download.py']
    missing=[p for p in required if not (target/p).exists()]
    if missing:raise ValueError('Missing uploaded files: '+', '.join(missing))
    print('Application assembled:',target)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('source');p.add_argument('target');a=p.parse_args();prepare(a.source,a.target)
