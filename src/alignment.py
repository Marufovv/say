"""Conservative camera alignment against the supplied sample reference frame."""
import cv2
import numpy as np
from .scene import ROOT

def align_scene(scene,frame):
    if not scene.get('alignment_required'):return scene,{'status':'not_requested'}
    def reject(reason):return {**scene,'verified':False},{'status':'rejected','reason':reason}
    ref=cv2.imread(str(ROOT/'configs/reference.jpg'))
    if ref is None:return reject('Kamera moslash uchun reference.jpg topilmadi.')
    target=cv2.resize(frame,(960,540));ref=cv2.resize(ref,(960,540))
    orb=cv2.SIFT_create(nfeatures=3000)
    clahe=cv2.createCLAHE(2.0,(8,8))
    # Static pavement/buildings dominate. RANSAC discards moving objects.
    a,da=orb.detectAndCompute(clahe.apply(cv2.cvtColor(ref,cv2.COLOR_BGR2GRAY)),None)
    b,db=orb.detectAndCompute(clahe.apply(cv2.cvtColor(target,cv2.COLOR_BGR2GRAY)),None)
    if da is None or db is None:return reject('Kamerani solishtirish uchun belgilar kam.')
    pairs=cv2.BFMatcher(cv2.NORM_L2).knnMatch(da,db,k=2)
    matches=[p[0] for p in pairs if len(p)==2 and p[0].distance<.7*p[1].distance]
    if len(matches)<40:return reject('Video tasdiqlangan kameraga mos kelmadi.')
    p=np.float32([a[m.queryIdx].pt for m in matches]);q=np.float32([b[m.trainIdx].pt for m in matches])
    cv2.setRNGSeed(0);H,mask=cv2.findHomography(p,q,cv2.RANSAC,3.0)
    if H is None:return reject('Kamera siljishini aniqlab bo‘lmadi.')
    inliers=mask.ravel().astype(bool);ratio=float(inliers.mean())
    if inliers.sum()<30 or ratio<.55:return reject('Kamera mosligi ishonchsiz.')
    # Restrict to small changes of the same camera; not arbitrary homographies.
    corners=np.float32([[0,0],[960,0],[960,540],[0,540]])
    transformed=cv2.perspectiveTransform(corners[None],H)[0]
    if not np.isfinite(transformed).all() or np.max(np.linalg.norm(transformed-corners,axis=1))>120:return reject('Rakurs juda o‘zgargan; zonalarni qayta belgilang.')
    if np.ptp(p[inliers,0])<300 or np.ptp(p[inliers,1])<180:return reject('Mos belgilar tasvirning kichik qismida to‘plangan.')
    def poly(points):
        if not points:return []
        px=np.float32(points)*[960,540]
        return np.clip(cv2.perspectiveTransform(px.astype(np.float32)[None],H)[0]/[960,540],0,1).tolist()
    out={**scene,'road':poly(scene['road'])}
    for key in ['crossings','queue_zones','exclusions']:out[key]=[poly(z) for z in scene.get(key,[])]
    # Direction vectors must transform with their lane's centre, too.
    out['lanes']=[]
    for lane in scene['lanes']:
        centre=np.mean(lane['polygon'],axis=0);end=centre+np.asarray(lane['direction'])*.1
        mapped=cv2.perspectiveTransform((np.float32([centre,end])*[960,540]).astype(np.float32)[None],H)[0]/[960,540]
        out['lanes'].append({**lane,'polygon':poly(lane['polygon']),'direction':((mapped[1]-mapped[0])*10).tolist()})
    out['alignment_required']=False
    return out,{'status':'matched','matches':len(matches),'inliers':int(inliers.sum()),'inlier_ratio':round(ratio,3)}
