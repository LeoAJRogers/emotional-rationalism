"""Independent, targeted R-006 T1 synthetic calibration (NO HUMAN DATA).

Reimplements disjoint-pair U, leave-one-day-out jackknife, bootstrap,
and 20-term Hermite ordinal correction using vectorized NumPy/SciPy.
NOT a reproduction of Claude's 22-world Part A benchmark.
"""
import argparse, json
from math import factorial
import numpy as np
from scipy.special import ndtri, expit, logit, eval_hermitenorm

M = 254
N = 127
D = 6
B = 10
J = 3
K = 20
LAM = np.array([.7,.7,.65])
PAIR = [(0,0),(0,1),(0,2),(1,1),(1,2),(2,2)]
FIDX = [((0,0),(1,2)),((1,1),(0,2)),((2,2),(0,1))]
EIDX = {p:i for i,p in enumerate(PAIR)}
EIDX.update({(j,i):e for (i,j),e in list(EIDX.items())})
INDICES=[(EIDX[a],EIDX[b],EIDX[(j,k)],EIDX[(j,l)]) for j,((a,b),(k,l)) in enumerate([])] # unused
GQIDX = [(EIDX[(j,j)],EIDX[tuple(k_l)],EIDX[(j,k_l[0])],EIDX[(j,k_l[1])])
         for j,k_l in enumerate([(1,2),(0,2),(0,1)])]


def phi_path(rng, phi, size=M):
    phi=np.broadcast_to(np.asarray(phi,float),(size,))
    f=np.empty((size,D*B))
    f[:,0]=rng.standard_normal(size)
    for t in range(1,D*B):
        p=phi**(7 if t%B==0 else 1)
        f[:,t]=p*f[:,t-1]+np.sqrt(1-p*p)*rng.standard_normal(size)
    return f.reshape(size,D,B)


def sim(rng,world):
    load_sd=(.3 if world in ('N8','W1s+N8','W1w+N8') else 0)
    phisd=(.5 if world in ('N8','W1s+N8','W1w+N8') else 0)
    mnar=(.6 if world in ('N8','W1s+N8','W1w+N8') else 0)
    ordinal=world not in ('W0','N6','N7')
    floors=(.75,.75,.75) if world=='N3h' else (.45,.65,.50)
    phi=np.full(N,.55) if phisd==0 else expit(logit(.55)+phisd*rng.standard_normal(N))
    phi=np.repeat(phi,2)
    lam=np.tile(LAM,(M,1)) if load_sd==0 else np.repeat(LAM*np.exp(load_sd*rng.standard_normal((N,J))),2,axis=0)
    f=phi_path(rng,phi)
    signal=f[...,None]*lam[:,None,None,:]
    if world=='N6':
        signal*=np.exp(.3*rng.standard_normal((M,D,J)))[:,:,None,:]
    target=(.25 if world=='W1s+N8' else .10 if world=='W1w+N8' else 0)
    s=target*.55*LAM**2/.6
    if target:
        for j in range(J):
            signal[...,j] += np.sqrt(s[j])*phi_path(rng,.6)
    theta=1-LAM**2-s
    ystar=signal+np.sqrt(theta)*rng.standard_normal((M,D,B,J))
    period=np.tile([0,1],N)
    means=np.array([.77,.70])[period]
    pi=rng.beta(means*8,(1-means)*8)
    pr=expit(logit(np.clip(pi,1e-6,1-1e-6))[:,None,None]-mnar*f)
    obs=rng.random((M,D,B))<pr
    if world=='N7':
        resp=ystar.copy()
        for d in range(D):
            have=np.zeros(M,bool)
            last=np.zeros((M,J))
            for b in range(B):
                if b>0:
                    resp[:,d,b,:]=np.where(have[:,None],.85*ystar[:,d,b,:]+.15*last,ystar[:,d,b,:])
                upd=obs[:,d,b]
                last=np.where(upd[:,None],resp[:,d,b,:],last)
                have|=upd
        ystar=resp
    if ordinal:
        tot_sd=np.sqrt(1+(.8)**2+(.3)**2)
        meanitem=-ndtri(np.array(floors))*tot_sd
        mu_p=meanitem+.8*rng.standard_normal((N,J))
        mu=np.repeat(mu_p,2,axis=0)+.3*rng.standard_normal((M,J))
        z=ystar+mu[:,None,None,:]
        y=1+(z[...,None]>np.array([0,.6,1.2,1.8,2.4,3.0])).sum(-1)
    else:
        y=ystar
    return np.where(obs[...,None],y,np.nan)


def correction(P,valid,X,s):
    n=valid.sum((1,2))
    C=P.sum((1,2))/np.maximum(n[:,None],1)
    m,j,d,b=X.shape[0],X.shape[-1],X.shape[1],X.shape[2]
    obs=np.isfinite(X[...,0]);nobs=obs.sum((1,2)).astype(float)
    x=np.nan_to_num(X,nan=0.0)
    f=np.stack([( (x<=c)&obs[...,None]).sum((1,2))/np.maximum(nobs[:,None],1) for c in range(1,7)],axis=-1)
    inside=(f>0)&(f<1)
    tau=ndtri(np.clip(f,1e-12,1-1e-12))
    dens=np.exp(-tau*tau/2)/np.sqrt(2*np.pi)
    s_safe=np.where(np.isfinite(s)&(s>1e-12),s,1.0)
    a=np.stack([(dens*eval_hermitenorm(k,tau)*inside).sum(-1)/s_safe[:,None] for k in range(K)],axis=-1)
    jj,ll=np.array(PAIR).T
    fact=np.array([factorial(k) for k in range(1,K+1)],float)
    coef=a[:,jj,:]*a[:,ll,:]/fact[None,None,:]
    ns=np.arange(1,K+1)
    c1=coef[:,:,0];okay=c1>1e-12
    r=np.clip(C/np.where(okay,c1,1),-.95,.95)
    for it in range(40):
        power=r[...,None]**(ns-1)
        fun=r*(coef*power).sum(-1)-C
        deriv=(ns*coef*power).sum(-1)
        update=np.where(okay&(deriv>1e-12),fun/np.where(deriv>1e-12,deriv,1),0)
        rr=np.clip(r-update,-.99,.99)
        if np.max(np.abs(rr-r))<1e-13:break
        r=rr
    r=np.where(okay,r,0)
    corr=(coef[:,:,1:]*(r[...,None]**ns[1:])).sum(-1)
    return P-corr[:,None,None,:]*valid[...,None]


def estimate(Y,ordinal=False,drop_day=None,cor=False):
    yy=Y.copy()
    if drop_day is not None: yy[:,drop_day,:,:]=np.nan
    mask=np.isfinite(yy).all(-1)
    nobs=mask.sum((1,2))
    X=np.where(np.isfinite(yy), yy,0)
    mean=(X*mask[...,None]).sum((1,2))/np.maximum(nobs[:,None],1)
    Xc=(X-mean[:,None,None,:])*mask[...,None]
    s=np.sqrt(((Xc**2).sum((1,2))/np.maximum(nobs[:,None],1)).mean(-1))
    good=np.isfinite(s)&(s>1e-12)
    xx=Xc/np.where(good,s,1)[:,None,None,None]
    valid=np.zeros((M,D,B),bool)
    valid[:,:,1:]=mask[:,:,1:]&mask[:,:,:-1]
    jj,ll=np.array(PAIR).T
    P=np.zeros((M,D,B,len(PAIR)))
    P[:,:,1:,:]=.5*(xx[:,:,1:,jj]*xx[:,:,:-1,ll]+xx[:,:,1:,ll]*xx[:,:,:-1,jj])
    P*=valid[...,None]
    if cor:P=correction(P,valid,yy,s)
    S=P.sum((1,2));cnt=valid.sum((1,2))
    ov=np.zeros((M,len(PAIR),len(PAIR)))
    n_over=np.zeros(M)
    for shift in [-1,0,1]:
        if shift>=0:
            a,b=P[:,:,:B-shift,:],P[:,:,shift:,:]
            va,vb=valid[:,:,:B-shift],valid[:,:,shift:]
        else:
            a,b=P[:,:,-shift:,:],P[:,:,:B+shift,:]
            va,vb=valid[:,:,-shift:],valid[:,:,:B+shift]
        ov+=np.einsum('mdte,mdtf->mef',a,b)
        n_over+=(va&vb).sum((1,2))
    den=cnt*cnt-n_over
    u=(S[:,:,None]*S[:,None,:]-ov)/np.maximum(den[:,None,None],1)
    gs=np.stack([u[:,a,b]-u[:,c,d] for a,b,c,d in GQIDX],axis=1)
    qs=np.stack([u[:,c,d] for a,b,c,d in GQIDX],axis=1)
    ok=(nobs>=15)&(cnt>=8)&(mask.any(-1).sum(-1)>=3)&(den>0)&good
    return gs,qs,cnt,ok,good&(den>0)


def run(Y, cor=False, nboot=199, seed=0):
    gs,qs,cnt,keep,_=estimate(Y,drop_day=None,cor=cor)
    Dcount=np.isfinite(Y).all(-1).any(-1).sum(-1)
    gj,qj=gs.copy(),qs.copy();fallback=0
    allgs=[];allqs=[];allok=[]
    for d in range(D):
        g,q,n,ok,version_ok=estimate(Y,drop_day=d,cor=cor)
        allgs.append(g);allqs.append(q);allok.append(version_ok)
    allgs=np.array(allgs);allqs=np.array(allqs);allok=np.array(allok)
    observedday=np.isfinite(Y).all(-1).any(-1).T
    valid_l=(allok|~observedday).all(axis=0)
    valid_l&=keep
    fallback=int((keep&~valid_l).sum())
    weights=observedday[:,:,None]
    avg_g=(allgs*weights).sum(axis=0)/np.maximum(Dcount[:,None],1)
    avg_q=(allqs*weights).sum(axis=0)/np.maximum(Dcount[:,None],1)
    gj=np.where(valid_l[:,None],Dcount[:,None]*gs-(Dcount[:,None]-1)*avg_g,gs)
    qj=np.where(valid_l[:,None],Dcount[:,None]*qs-(Dcount[:,None]-1)*avg_q,qs)
    npers=127
    wg=(cnt[:,None]*gj).sum(-1).reshape(npers,2)
    wq=(cnt[:,None]*qj).sum(-1).reshape(npers,2)
    wg=(wg*keep.reshape(npers,2)).sum(-1)
    wq=(wq*keep.reshape(npers,2)).sum(-1)
    val=wg.sum()/wq.sum()
    rng=np.random.default_rng(seed)
    counts=rng.multinomial(npers,np.full(npers,1/npers),size=nboot)
    boot=(counts@wg)/(counts@wq)
    lo,hi=np.quantile(boot,[.025,.975])
    return {'t1':float(val),'lo':float(lo),'hi':float(hi),'fire':bool(lo>0),'used':int(keep.sum()),'fallback':fallback}


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--reps',type=int,default=20)
    p.add_argument('--worlds',nargs='+',default=['W0','N3','N3h','N8','W1s+N8'])
    p.add_argument('--boot',type=int,default=199)
    p.add_argument('--start',type=int,default=0)
    p.add_argument('--output',default='r006_targeted_bench.json')
    a=p.parse_args();out={}
    world_order=['W0','N3','N3h','N8','W1s+N8','W1w+N8','N6','N7']
    for world in a.worlds:
        wi=world_order.index(world)
        arr=[]
        import time
        ti=time.time()
        for rr in range(a.start,a.start+a.reps):
            seed=100000*(wi+1)+rr
            y=sim(np.random.default_rng(seed),world)
            c=world not in ('W0','N6','N7')
            z=run(y,cor=c,seed=rr,nboot=a.boot)
            if c:
                linear=run(y,cor=False,seed=rr,nboot=a.boot)
                z['lin_t1']=linear['t1']
                z['lin_fire']=linear['fire']
            arr.append(z)
            if (rr+1)%10==0:print(world,rr+1,'elapsed',round(time.time()-ti,1),'fire',sum(x['fire'] for x in arr),flush=True)
        out[world]={'n':a.reps,'start':a.start,'mean_T1':float(np.mean([x['t1'] for x in arr])),
            'sd_T1':float(np.std([x['t1'] for x in arr],ddof=1)),
            'fire_rate':float(np.mean([x['fire'] for x in arr])),
            'mean_used':float(np.mean([x['used'] for x in arr])),
            'mean_jk_fallback':float(np.mean([x['fallback'] for x in arr])),
            'lin_mean_T1':float(np.mean([x.get('lin_t1',float('nan')) for x in arr])) if world!='W0' else None,
            'lin_fire_rate':float(np.mean([x.get('lin_fire',False) for x in arr])) if world!='W0' else None,
            'first_5':arr[:5]}
        print(world,out[world]['fire_rate'],out[world]['mean_T1'],flush=True)
    with open(a.output,'w') as f:json.dump(out,f,indent=2)
if __name__=='__main__': main()
