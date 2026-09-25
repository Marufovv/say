"""One-time download from official OpenCV Zoo; no inference-time network use."""
from pathlib import Path
import hashlib,urllib.request
URL='https://media.githubusercontent.com/media/opencv/opencv_zoo/main/models/object_detection_yolox/object_detection_yolox_2022nov.onnx'
SHA256='c5c2d13e59ae883e6af3b45daea64af4833a4951c92d116ec270d9ddbe998063'
p=Path(__file__).parent/'yolox_s.onnx'
if p.exists() and hashlib.sha256(p.read_bytes()).hexdigest()==SHA256:
    print('YOLOX-S tayyor; checksum mos.');raise SystemExit(0)
tmp=p.with_suffix('.partial')
try:
    parts=[p.parent/'yolox_s.part01',p.parent/'yolox_s.part02']
    if all(part.exists() for part in parts):
        with tmp.open('wb') as f:
            for part in parts:
                with part.open('rb') as source:
                    while chunk:=source.read(1024*1024):f.write(chunk)
    else:
        with urllib.request.urlopen(URL,timeout=120) as response,tmp.open('wb') as f:
            while chunk:=response.read(1024*1024):f.write(chunk)
    if hashlib.sha256(tmp.read_bytes()).hexdigest()!=SHA256:raise RuntimeError('Checksum mos kelmadi; model o‘rnatilmadi.')
    tmp.replace(p);print('YOLOX-S yuklandi va checksum tekshirildi.')
finally:
    if tmp.exists():tmp.unlink()
