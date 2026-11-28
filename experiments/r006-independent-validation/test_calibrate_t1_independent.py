"""Synthetic-only parity checks for the independent R-006 T1 implementation."""
import numpy as np
import calibrate_t1_independent as m


def brute_person(y):
    mask=np.isfinite(y).all(-1)
    n=mask.sum()
    xx=np.where(mask[...,None],y,0)
    mu=xx.sum((0,1))/n
    x=(xx-mu)*mask[...,None]
    s=np.sqrt(((x*x).sum((0,1))/n).mean())
    x=x/s
    pp=[]
    for d in range(m.D):
        for b in range(1,m.B):
            if mask[d,b] and mask[d,b-1]:
                v=.5*(np.outer(x[d,b],x[d,b-1])+np.outer(x[d,b-1],x[d,b]))
                pp.append(((d,b),(d,b-1),v))
    us=np.zeros((3,3,3,3))
    n_pairs=0
    for a in pp:
        for b in pp:
            if {a[0],a[1]}.isdisjoint({b[0],b[1]}):
                us+=np.einsum('ij,kl->ijkl',a[2],b[2]);n_pairs+=1
    us/=n_pairs
    g=[];q=[]
    for j,kl in enumerate(((1,2),(0,2),(0,1))):
        k,l=kl
        g.append(us[j,j,k,l]-us[j,k,j,l]);q.append(us[j,k,j,l])
    return np.array(g),np.array(q)


def main():
    rng=np.random.default_rng(420)
    Y=rng.normal(size=(m.M,m.D,m.B,m.J))
    Y[rng.random((m.M,m.D,m.B))<.20]=np.nan
    g,q,cnt,keep,ok=m.estimate(Y,cor=False)
    gb,qb=brute_person(Y[0])
    assert np.allclose(g[0],gb,atol=1e-12), (g[0],gb)
    assert np.allclose(q[0],qb,atol=1e-12), (q[0],qb)
    # Severe floor and partially empty persons must yield a finite aggregate.
    Z=m.sim(np.random.default_rng(102), 'N3h')
    out=m.run(Z,cor=True,nboot=29,seed=17)
    assert all(np.isfinite(out[k]) for k in ('t1','lo','hi')),out
    print('PASS independent disjoint-pair algebra against explicit enumeration')
    print('PASS ordinal-corrected T1 finite under severe floor scenario')

if __name__=='__main__':main()
