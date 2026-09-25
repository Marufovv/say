"""Local-first WIUT CV application. Bind to 127.0.0.1 by default."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import json,os,time,uuid,threading,shutil
import cv2
from fastapi import FastAPI,UploadFile,File,HTTPException,Request
from fastapi.responses import FileResponse,JSONResponse,Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel,Field
from src.scene import ROOT,load_scene,validate_scene,capabilities,SUPPORTED
from src.pipeline import analyze,video_metadata,official_prediction
from src.events import OFFICIAL_CLASSES
from src.compliance import BOUNDARIES,validate_annotations

DATA=Path(os.getenv('YUKSAVA_DATA_DIR',str(ROOT/'.local')));VIDEOS=DATA/'videos';JOBS=DATA/'jobs'
for p in (VIDEOS,JOBS):p.mkdir(parents=True,exist_ok=True)
from src.bootstrap import restore_demo
restore_demo(ROOT,DATA)
MAX_BYTES=8*1024*1024*1024
app=FastAPI(title='Yuksava — WIUT CV',docs_url='/api/docs')
app.mount('/static',StaticFiles(directory=ROOT/'web'),name='static')
executor=ThreadPoolExecutor(max_workers=1)
jobs={};cancels={};state_lock=threading.Lock()
for p in JOBS.glob('*/status.json'):
    try:
        j=json.loads(p.read_text())
        if j['status'] in ('queued','running'):j.update(status='error',message='Server qayta ishga tushdi. Tahlilni qayta boshlang.')
        jobs[j['id']]=j
    except (ValueError,KeyError,OSError):pass

def atomic_json(path,data):
    tmp=path.with_suffix('.tmp');tmp.write_text(json.dumps(data,ensure_ascii=False));tmp.replace(path)

def video_dir(vid):
    if len(vid)!=32 or any(c not in '0123456789abcdef' for c in vid):raise HTTPException(404,'Video topilmadi.')
    p=VIDEOS/vid
    if not (p/'meta.json').exists():raise HTTPException(404,'Video topilmadi.')
    return p

def get_job(jid):
    if jid not in jobs:raise HTTPException(404,'Tahlil topilmadi.')
    return jobs[jid]

@app.middleware('http')
async def same_origin(request:Request,call_next):
    # Protect local write endpoints against cross-site browser requests.
    if request.url.path=='/api/videos' and request.method=='POST':
        length=request.headers.get('content-length')
        if length and length.isdigit() and int(length)>MAX_BYTES+1024*1024:
            return JSONResponse({'detail':'Video hajmi 8 GB dan oshmasin.'},status_code=413)
    origin=request.headers.get('origin')
    if request.method in ('POST','PUT','DELETE') and origin:
        from urllib.parse import urlparse
        if urlparse(origin).netloc!=request.headers.get('host'):return JSONResponse({'detail':'Boshqa saytdan so‘rovga ruxsat yo‘q.'},status_code=403)
    return await call_next(request)

@app.get('/')
def index():return FileResponse(ROOT/'web/index.html')

@app.get('/api/health')
def health():
    scene=load_scene()
    return {'ready':(ROOT/'weights/yolox_s.onnx').exists(),'model':'YOLOX-S','scene':scene,'enabled':capabilities(scene),'supported':SUPPORTED,'classes':OFFICIAL_CLASSES,'max_upload_mb':8192,'max_upload_seconds':None,'product':'Yuksava'}

@app.put('/api/scene')
async def save_scene(request:Request):
    try:scene=validate_scene(await request.json())
    except (ValueError,TypeError,KeyError) as e:raise HTTPException(422,str(e))
    atomic_json(ROOT/'configs/scene.json',scene)
    return {'scene':scene,'enabled':capabilities(scene)}

@app.get('/api/videos')
def list_videos():
    rows=[]
    for p in VIDEOS.glob('*/meta.json'):
        try:rows.append(json.loads(p.read_text()))
        except (OSError,ValueError):pass
    return sorted(rows,key=lambda r:r['created'],reverse=True)

@app.post('/api/videos')
async def upload(file:UploadFile=File(...)):
    name=Path(file.filename or 'video.mp4').name
    if not name.lower().endswith('.mp4'):raise HTTPException(415,'Faqat .mp4 fayl qabul qilinadi.')
    vid=uuid.uuid4().hex;p=VIDEOS/vid;p.mkdir();size=0
    try:
        with (p/'video.mp4').open('wb') as f:
            while chunk:=await file.read(1024*1024):
                size+=len(chunk)
                if size>MAX_BYTES:raise HTTPException(413,'Video hajmi 8 GB dan oshmasin.')
                f.write(chunk)
        meta=video_metadata(p/'video.mp4')
        cap=cv2.VideoCapture(str(p/'video.mp4'));ok,frame=cap.read();cap.release()
        if not ok:raise ValueError('Birinchi kadr o‘qilmadi.')
        if frame.shape[1]>1280:frame=cv2.resize(frame,(1280,round(frame.shape[0]*1280/frame.shape[1])))
        cv2.imwrite(str(p/'poster.jpg'),frame)
        row={**meta,'id':vid,'name':name,'bytes':size,'created':time.time()};atomic_json(p/'meta.json',row)
        return row
    except HTTPException:shutil.rmtree(p);raise
    except Exception as e:
        shutil.rmtree(p);raise HTTPException(422,str(e))
    finally:await file.close()

@app.get('/api/videos/{vid}/media')
def media(vid:str):return FileResponse(video_dir(vid)/'video.mp4',media_type='video/mp4')

@app.get('/api/videos/{vid}/poster')
def poster(vid:str):return FileResponse(video_dir(vid)/'poster.jpg',media_type='image/jpeg')

@app.get('/api/videos/{vid}/frame')
def frame(vid:str,t:float=0):
    p=video_dir(vid);meta=json.loads((p/'meta.json').read_text())
    if t<0 or t>=meta['duration']:raise HTTPException(422,'Video vaqti noto‘g‘ri.')
    cap=cv2.VideoCapture(str(p/'video.mp4'));cap.set(cv2.CAP_PROP_POS_MSEC,t*1000);ok,f=cap.read();cap.release()
    if not ok:raise HTTPException(422,'Kadr o‘qilmadi.')
    if f.shape[1]>1280:f=cv2.resize(f,(1280,round(f.shape[0]*1280/f.shape[1])))
    return Response(cv2.imencode('.jpg',f)[1].tobytes(),media_type='image/jpeg')

@app.get('/api/videos/{vid}/scene')
def video_scene(vid:str):
    from src.alignment import align_scene
    p=video_dir(vid)
    if (p/'scene.json').exists():scene=validate_scene(json.loads((p/'scene.json').read_text()));alignment={'status':'saved_for_video'}
    else:
        cap=cv2.VideoCapture(str(p/'video.mp4'));ok,f=cap.read();cap.release()
        if not ok:raise HTTPException(422,'Kadr o‘qilmadi.')
        scene,alignment=align_scene(load_scene(),f)
    return {'scene':scene,'enabled':capabilities(scene),'alignment':alignment}

@app.put('/api/videos/{vid}/scene')
async def save_video_scene(vid:str,request:Request):
    p=video_dir(vid)
    try:scene=validate_scene(await request.json())
    except (ValueError,TypeError,KeyError) as e:raise HTTPException(422,str(e))
    scene['alignment_required']=False;atomic_json(p/'scene.json',scene)
    return {'scene':scene,'enabled':capabilities(scene)}

class StartJob(BaseModel):
    video_id:str
    scene:dict|None=None
    team:str=Field(default='unnamed-team',max_length=100)

@app.post('/api/jobs')
def start_job(body:StartJob):
    video=video_dir(body.video_id);meta=json.loads((video/'meta.json').read_text())
    if not (ROOT/'weights/yolox_s.onnx').exists():raise HTTPException(503,'Model og‘irligi topilmadi.')
    try:scene=validate_scene(body.scene) if body.scene is not None else video_scene(body.video_id)['scene']
    except (ValueError,TypeError,KeyError) as e:raise HTTPException(422,str(e))
    with state_lock:
        if sum(j['status'] in ('queued','running') for j in jobs.values())>=3:raise HTTPException(429,'Navbat band. Avvalgi tahlil tugashini kuting.')
        jid=uuid.uuid4().hex;(JOBS/jid).mkdir();cancels[jid]=threading.Event()
        jobs[jid]={'id':jid,'video_id':body.video_id,'name':meta['name'],'status':'queued','progress':0,'message':'Navbatda','created':time.time()}
        atomic_json(JOBS/jid/'status.json',jobs[jid]);executor.submit(worker,jid,video,scene,body.team)
    return dict(jobs[jid])

def worker(jid,video,scene,team):
    def progress(p,message,stats):jobs[jid].update(progress=p,message=message,stats=stats)
    try:
        if cancels[jid].is_set():raise InterruptedError('Tahlil bekor qilindi.')
        jobs[jid]['status']='running'
        result=analyze(video/'video.mp4',scene,progress,cancels[jid])
        heat=result.pop('_heatmap',None)
        if heat:(JOBS/jid/'heatmap.jpg').write_bytes(heat)
        result['meta']['video_id']=jobs[jid]['name']
        atomic_json(JOBS/jid/'result.json',result)
        atomic_json(JOBS/jid/'predictions.json',official_prediction(result,jobs[jid]['name'],team))
        jobs[jid].update(status='done',progress=1,message='Tahlil tayyor',events=len(result['events']))
    except InterruptedError:jobs[jid].update(status='cancelled',message='Tahlil bekor qilindi.')
    except Exception as e:
        jobs[jid].update(status='error',message=str(e))
        import traceback
        (JOBS/jid/'error.log').write_text(traceback.format_exc())
    finally:atomic_json(JOBS/jid/'status.json',jobs[jid]);cancels.pop(jid,None)

@app.get('/api/jobs')
def list_jobs():return sorted((dict(j) for j in jobs.values()),key=lambda j:j['created'],reverse=True)

@app.get('/api/jobs/{jid}')
def job(jid:str):return dict(get_job(jid))

@app.post('/api/jobs/{jid}/cancel')
def cancel(jid:str):
    get_job(jid)
    if jid in cancels:cancels[jid].set()
    return {'ok':True}

@app.get('/api/jobs/{jid}/{asset}')
def result_asset(jid:str,asset:str):
    j=get_job(jid)
    if asset not in ('result.json','predictions.json','heatmap.jpg'):raise HTTPException(404,'Fayl topilmadi.')
    p=JOBS/jid/asset
    if j['status']!='done' or not p.exists():raise HTTPException(409,'Natija hali tayyor emas.')
    return FileResponse(p,filename=asset if asset=='predictions.json' else None)

@app.get('/api/specification')
def specification():
    return {'events':[dict(label=l,name=n,start=s,end=e,automatic=l in SUPPORTED) for l,n,s,e in BOUNDARIES],
            'scoring':{'part_a':'Macro F1; tIoU 0.3 / 0.5 / 0.7','model':'0.7 A + 0.3 B; accident yo‘q bo‘lsa M=A','elimination':'0.60 M + 0.25 sayt + 0.15 kod'},
            'limits':{'gpu':'T4 sinfi, 16 GB','cpu':8,'ram_gb':32,'weights_gb':5,'runtime':'A+B ≤ 3 × video davomiyligi','python':'>=3.10'},
            'camera_description_available':(ROOT/'samples/camera.md').exists()}

@app.get('/api/videos/{vid}/annotations')
def annotations(vid:str):
    p=video_dir(vid)/'annotations.json'
    return json.loads(p.read_text()) if p.exists() else {'events':[],'reviewed':False,'source':'human_review'}

class AnnotationBody(BaseModel):
    events:list
    reviewed:bool=False

@app.put('/api/videos/{vid}/annotations')
def save_annotations(vid:str,body:AnnotationBody):
    p=video_dir(vid);meta=json.loads((p/'meta.json').read_text())
    try:events=validate_annotations(body.events,meta['duration'])
    except (ValueError,TypeError) as e:raise HTTPException(422,str(e))
    data={'events':events,'reviewed':body.reviewed,'source':'human_review','updated':time.time()}
    atomic_json(p/'annotations.json',data);return data

@app.get('/api/videos/{vid}/ground-truth')
def ground_truth(vid:str):
    p=video_dir(vid);meta=json.loads((p/'meta.json').read_text());a=annotations(vid)
    if not a['reviewed']:raise HTTPException(409,'Avval butun videoni tekshirib, annotatsiyani tasdiqlang.')
    return {meta['name']:{'duration':meta['duration'],'events':a['events']}}

@app.get('/api/jobs/{jid}/score/review')
def score_review(jid:str):
    from evaluate import validate,evaluate
    j=get_job(jid)
    if j['status']!='done':raise HTTPException(409,'Tahlil hali tugamadi.')
    gt=ground_truth(j['video_id']);pred=json.loads((JOBS/jid/'predictions.json').read_text())
    errors,warnings=validate(pred,gt)
    if errors:raise HTTPException(422,errors)
    return {'report':evaluate(gt,pred,per_video=True),'warnings':warnings,'scope':'Shu videoning foydalanuvchi annotatsiyasi; hidden test natijasi emas.'}

@app.post('/api/camera/frame')
async def camera_frame(request:Request):
    from src.live import infer_jpeg
    from starlette.concurrency import run_in_threadpool
    data=bytearray()
    async for chunk in request.stream():
        data.extend(chunk)
        if len(data)>1024*1024:raise HTTPException(413,'Kadr hajmi 1 MB dan oshmasin.')
    try:return await run_in_threadpool(infer_jpeg,bytes(data))
    except ValueError as e:raise HTTPException(422,str(e))
    except RuntimeError as e:raise HTTPException(429,str(e))

@app.get('/api/project')
def project():
    p=DATA/'project.json'
    if not p.exists():p=ROOT/'configs/project.json'
    data=json.loads(p.read_text()) if p.exists() else {'team':'','members':[],'repository':'','website':'','weights_url':'','revision':''}
    return {**data,'editable':os.getenv('YUKSAVA_READ_ONLY_SETTINGS','0')!='1'}

@app.get('/api/documents/{name}')
def documents(name:str):
    files={'task':ROOT/'docs/task.pdf','report':ROOT/'docs/TECHNICAL_REPORT_UZ.md'}
    p=files.get(name)
    if p is None or not p.exists():raise HTTPException(404,'Hujjat topilmadi.')
    return FileResponse(p,filename=p.name)

@app.put('/api/project')
async def save_project(request:Request):
    from urllib.parse import urlparse
    if os.getenv('YUKSAVA_READ_ONLY_SETTINGS','0')=='1':raise HTTPException(403,'Public saytda jamoa tahriri yopiq. Repositorydagi configs/project.json ni yangilang.')
    data=await request.json()
    if not isinstance(data,dict):raise HTTPException(422,'JSON obyekt kerak.')
    out={k:str(data.get(k,''))[:500] for k in ['team','repository','website','weights_url','revision']}
    for k in ['repository','website','weights_url']:
        if out[k] and (urlparse(out[k]).scheme not in ['http','https'] or not urlparse(out[k]).netloc):raise HTTPException(422,'Havola http yoki https bilan boshlansin.')
    members=data.get('members',[])
    if not isinstance(members,list) or len(members)>3 or any(not isinstance(m,dict) for m in members):raise HTTPException(422,'Jamoada 3 tagacha a’zo kiriting.')
    out['members']=[{k:str(m.get(k,'')).strip()[:200] for k in ['name','role','email','portfolio']} for m in members]
    import re
    if any(m['email'] and not re.fullmatch(r'[^\s@]+@[^\s@]+\.[^\s@]+',m['email']) for m in out['members']):raise HTTPException(422,'Email manzilini tekshiring.')
    atomic_json(DATA/'project.json',out);return out

if __name__=='__main__':
    import uvicorn
    uvicorn.run(app,host='127.0.0.1',port=int(os.getenv('PORT','8765')))
