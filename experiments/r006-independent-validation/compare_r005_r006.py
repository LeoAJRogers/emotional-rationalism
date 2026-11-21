"""Synthetic-only, independent R-005/R-006 comparison.

No human-data files read. External packages: NumPy only.

R-005 D2: average same-item lag-2 covariance minus cross-item lag-2
covariance, divided by lag-1 off-diagonal covariance, pooled over people.
R-006 T1: within-person-period disjoint-pair U-statistic of lag-1 item excess,
pooled with lag-pair weights; raw linear/no jackknife or ordinal correction.
The latter is an algebraic screen, *not* a substitute for the registered bench.
"""
from __future__ import annotations
import argparse, json
import numpy as np

N = 127
PER = 2
D = 6
B = 10
BASE = np.array([.7, .7, .65])
PHI = .55


def ar_sim(rng, n, days=6, beeps=10):
    f = np.zeros((n, days, beeps))
    f[:,0,0] = rng.normal(size=n)
    for d in range(days):
        for b in range(beeps):
            if d == 0 and b == 0:
                continue
            c = PHI ** (7 if b == 0 else 1)
            last = f[:, d-1, beeps-1] if b == 0 else f[:, d, b-1]
            f[:,d,b] = c*last+np.sqrt(1-c*c)*rng.normal(size=n)
    return f


def data(rng, loading_sd=0.3):
    n = N * PER
    f = ar_sim(rng,n)
    lam_person = BASE * np.exp(loading_sd*rng.normal(size=(N,3)))
    lam = np.repeat(lam_person,PER,axis=0)
    y=lam[:,None,None,:]*f[:,:,:,None]+np.sqrt(1-BASE**2)*rng.normal(size=(n,D,B,3))
    pi=rng.beta(np.array([.77,.70]*N)*8,(1-np.array([.77,.70]*N))*8)
    obs=rng.random((n,D,B))<pi[:,None,None]
    y[~obs] = np.nan
    return y


def r005(y):
    z=y-np.nanmean(y,axis=(1,2),keepdims=True)
    def c(k,diagonal):
        a=z[:,:,k:,:];b=z[:,:,:B-k,:]
        valid=np.isfinite(a).all(axis=-1)&np.isfinite(b).all(axis=-1)
        vals=np.einsum('...i,...j->...ij',a,b)
        if diagonal:
            per=np.trace(vals,axis1=-2,axis2=-1)/3
        else:
            per=(vals.sum(axis=(-1,-2))-np.trace(vals,axis1=-2,axis2=-1))/6
        return np.nansum(np.where(valid,per,0))/valid.sum()
    c1=c(1,False);c2cross=c(2,False);c2same=c(2,True)
    return (c2same-c2cross)/c1


def r006_raw(y):
    # Disjoint-pair U aggregation, within each individual period.
    pnum=pden=0.0
    for yy in y:
        x=yy-np.nanmean(yy,axis=(0,1),keepdims=True)
        s=np.sqrt(np.nanmean(np.nanvar(x,axis=(0,1))))
        if not np.isfinite(s) or s<1e-9:continue
        x=x/s
        aa=[];bb=[];pp=[]
        for d in range(D):
            for t in range(1,B):
                if np.isfinite(x[d,t,:]).all() and np.isfinite(x[d,t-1,:]).all():
                    a=x[d,t];b=x[d,t-1]
                    pp.append((np.outer(a,b)+np.outer(b,a))/2)
                    aa.append((d,t));bb.append((d,t-1))
        n=len(pp)
        if n<8:continue
        a=np.array(aa);b=np.array(bb)
        disjoint=~(((a[:,None,:]==a[None,:,:]).all(-1)) | ((a[:,None,:]==b[None,:,:]).all(-1)) |
                   ((b[:,None,:]==a[None,:,:]).all(-1)) | ((b[:,None,:]==b[None,:,:]).all(-1)))
        norm=disjoint.sum()
        if norm<=0:continue
        P=np.array(pp)
        u=lambda e,f: np.einsum('u,uv,v->',P[:,e[0],e[1]],disjoint,P[:,f[0],f[1]])/norm
        g=q=0.0
        for j in range(3):
            k,l=[x for x in range(3) if x!=j]
            g+=u((j,j),(k,l))-u((j,k),(j,l))
            q+=u((j,k),(j,l))
        pnum+=n*g
        pden+=n*q
    return pnum/pden


def run(reps=48,seed=20261121):
    out={}
    for sd in (0.0, 0.3):
        vals=[]
        for rep in range(reps):
            rng=np.random.default_rng(seed+rep+int(sd*100000))
            y=data(rng,loading_sd=sd)
            vals.append((r005(y),r006_raw(y)))
        x=np.array(vals)
        out[f"log_sd_{sd}"]={"reps":reps,
            "r005_D2_mean":float(x[:,0].mean()),"r005_D2_q025_q975":np.quantile(x[:,0],[.025,.975]).tolist(),
            "r006_raw_T1_mean":float(x[:,1].mean()),"r006_raw_T1_q025_q975":np.quantile(x[:,1],[.025,.975]).tolist(),
            "r005_D2_positive_fraction":float((x[:,0]>0).mean()),"r006_raw_T1_positive_fraction":float((x[:,1]>0).mean())}
    return out

if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--reps',type=int,default=48);args=a.parse_args()
    print(json.dumps(run(args.reps),indent=2))
