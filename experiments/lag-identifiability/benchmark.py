"""Synthetic structural identifiability test. Requires numpy; no human data."""
import numpy as np

KINDS = ("affect", "belief", "report")

def trajectory(kind, cue, rho):
    b = np.zeros(len(cue)); z = np.zeros(len(cue)); y = np.zeros(len(cue))
    for t in range(len(cue)):
        b[t] = rho * (b[t-1] if t else 0) + (1-rho)*cue[t] if kind == "belief" else cue[t]
        z[t] = rho * (z[t-1] if t else 0) + (1-rho)*b[t] if kind == "affect" else b[t]
        y[t] = rho * (y[t-1] if t else 0) + (1-rho)*z[t] if kind == "report" else z[t]
    return np.stack([b,z,y],axis=1)

def winners(fits, rtol=1e-9):
    """All candidates tied with the best held-out score. An exact tie is an observational
    equivalence on this sample, not evidence for the first-listed candidate."""
    fits=np.asarray(fits); best=fits.min()
    return np.flatnonzero(fits <= best + rtol*max(1.0, abs(best)))

def experiment(seed=20261122, reps=30, n=240):
    print("numpy", np.__version__, "(Generator streams can differ across NumPy versions)")
    rng=np.random.default_rng(seed)
    for stride in (1,4):
        for channels in ((2,), (0,2), (0,1,2)):
            counts=np.zeros((3,3),dtype=int); unique_ok=unique_wrong=tied=0
            for true_idx,kind in enumerate(KINDS):
                for _ in range(reps):
                    cue=np.repeat(rng.choice([-1.,1.],size=(n+11)//12),12)[:n]
                    observed=trajectory(kind,cue,.78)+rng.normal(0,.12,(n,3))
                    sample=np.arange(n)%stride==0
                    train=sample & (np.arange(n)<int(.65*n))
                    test=sample & ~train
                    fits=[]
                    for candidate in KINDS:
                        best=(float("inf"),None)
                        for rho in np.linspace(.05,.95,91):
                            pred=trajectory(candidate,cue,rho)
                            loss=np.mean((pred[train][:,channels]-observed[train][:,channels])**2)
                            if loss<best[0]: best=(loss,pred)
                        held=np.mean((best[1][test][:,channels]-observed[test][:,channels])**2)
                        fits.append(held)
                    counts[true_idx,int(np.argmin(fits))]+=1
                    w=winners(fits)
                    if len(w)>1: tied+=1
                    elif w[0]==true_idx: unique_ok+=1
                    else: unique_wrong+=1
            print("stride",stride,"channels",channels,"rows=true cols=pred",KINDS)
            print(counts,"accuracy",np.trace(counts)/counts.sum())
            print("  tie-aware: unique correct",unique_ok,"| unique wrong",unique_wrong,
                  "| exact ties",tied,"(argmin above gives every tie to the first-listed kind)")

if __name__=="__main__":
    experiment()
