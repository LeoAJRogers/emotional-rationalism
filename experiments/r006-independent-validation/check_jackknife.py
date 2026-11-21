"""Synthetic-only R-006 T1 day-jackknife audit, independent implementation.

Requires compare_r005_r006.py and NumPy in this directory.
This is NOT the registered R-006 Part A or ordinal/CI calibration.
"""
import numpy as np
from compare_r005_r006 import data, r005, D, B


def gq_one(yy, drop_day=None):
    y=yy.copy()
    if drop_day is not None:y[drop_day,:,:]=np.nan
    if np.isfinite(y).all(-1).sum()<4:return None
    x=y-np.nanmean(y,axis=(0,1),keepdims=True)
    s=np.sqrt(np.nanmean(np.nanvar(x,axis=(0,1))))
    if not np.isfinite(s) or s<=1e-9:return None
    x=x/s
    aa=[]; bb=[];pp=[]
    for d in range(D):
        for t in range(1,B):
            if np.isfinite(x[d,t,:]).all() and np.isfinite(x[d,t-1,:]).all():
                a=x[d,t];b=x[d,t-1]
                pp.append((np.outer(a,b)+np.outer(b,a))/2)
                aa.append((d,t));bb.append((d,t-1))
    n=len(pp)
    if n<2:return None
    a=np.array(aa);b=np.array(bb)
    ok=~(((a[:,None,:]==a[None,:,:]).all(-1)) | ((a[:,None,:]==b[None,:,:]).all(-1)) |
        ((b[:,None,:]==a[None,:,:]).all(-1)) | ((b[:,None,:]==b[None,:,:]).all(-1)))
    norm=ok.sum()
    if norm==0:return None
    P=np.array(pp)
    def u(e,f):
        return np.einsum('u,uv,v->',P[:,e[0],e[1]],ok,P[:,f[0],f[1]])/norm
    gs=[]; qs=[]
    for j in range(3):
        k,l=[x for x in range(3) if x!=j]
        gs.append(u((j,j),(k,l))-u((j,k),(j,l)))
        qs.append(u((j,k),(j,l)))
    return np.array(gs),np.array(qs),n


def r006_jk(y):
    raw_num=raw_den=jk_num=jk_den=0.
    used=0; fallback=0
    for pp in y:
        full=gq_one(pp)
        if full is None:continue
        g,q,n=full
        loo=[gq_one(pp,i) for i in range(D)]
        obs=np.isfinite(pp).all(-1).any(-1)
        nday=obs.sum()
        if nday<3:continue
        if any(loo[i] is None for i in range(D) if obs[i]):
            fallback+=1
            gj,qj=g,q
        else:
            lg=np.array([loo[i][0] for i in range(D) if obs[i]])
            lq=np.array([loo[i][1] for i in range(D) if obs[i]])
            gj=nday*g-(nday-1)*lg.mean(axis=0)
            qj=nday*q-(nday-1)*lq.mean(axis=0)
        raw_num+=n*sum(g);raw_den+=n*sum(q)
        jk_num+=n*sum(gj);jk_den+=n*sum(qj)
        used+=1
    return raw_num/raw_den, jk_num/jk_den,used,fallback


def go(reps=12, sds=(0.,.3,.5)):
    for sd in sds:
        vals=[]
        for r in range(reps):
            yy=data(np.random.default_rng(20261121+r+int(sd*100000)),sd)
            vals.append((r005(yy), *r006_jk(yy)))
        x=np.asarray(vals)
        print('sd',sd, 'reps',reps, 'R005',x[:,0].mean(),
              'R006raw',x[:,1].mean(),'R006jk',x[:,2].mean(),
              'q025,975 jk',np.quantile(x[:,2],[.025,.975]),
              'used_mean',x[:,3].mean(),'fallback_mean',x[:,4].mean(),flush=True)


if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--reps',type=int,default=12);a=ap.parse_args()
    go(a.reps)
