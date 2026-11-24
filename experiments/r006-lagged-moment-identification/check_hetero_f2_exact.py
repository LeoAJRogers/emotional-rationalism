"""Code licence: MIT. Independent check of GPT-6.2's heterogeneous-F2 aggregation counterexample (ER #13).
Direct Wick enumeration over every ordered pair of disjoint lag-1 pairs (no S1/S2 shortcut).
Exact rational arithmetic. Design: 6 independent days x 10 beeps, r = (1/2)^lag within day."""
from fractions import Fraction as F
from itertools import product

M0 = [[5,4,3],[4,4,4],[3,4,5]]
def perm(M, p):  # relabel items: new item i is old item p[i]
    return [[M[p[i]][p[j]] for j in range(3)] for i in range(3)]
classes = [perm(M0, p) for p in ((0,1,2),(1,2,0),(2,0,1))]
beeps = [(d,b) for d in range(6) for b in range(10)]
pairs = [((d,b+1),(d,b)) for d in range(6) for b in range(9)]
def r(s,t):
    return F(1,2)**abs(s[1]-t[1]) if s[0]==t[0] else F(0)
def EP_pair(M, pi, e, pj, f):
    """E[P_pi[e] * P_pj[f]] for disjoint pairs, P_pi[j,l] = (x_j,t x_l,t' + x_l,t x_j,t')/2.
    Cov(x_j,s, x_l,t) = M[j][l] r(s,t) for s != t (common-rate rank structure)."""
    (t,tp),(u,up) = pi,pj
    (j,l),(k,m) = e,f
    def four(a,sa,b,sb,c,sc,d,sd):  # Wick: E[x_a,sa x_b,sb x_c,sc x_d,sd]
        C = lambda i,si,k_,sk: M[i][k_]*r(si,sk)
        return C(a,sa,b,sb)*C(c,sc,d,sd)+C(a,sa,c,sc)*C(b,sb,d,sd)+C(a,sa,d,sd)*C(b,sb,c,sc)
    tot = F(0)
    for (a,b) in ((j,l),(l,j)):
        for (c,d) in ((k,m),(m,k)):
            tot += four(a,t,b,tp,c,u,d,up)
    return tot/4
G=[F(0)]*3; Q=[F(0)]*3; n=0
for pi,pj in product(pairs, repeat=2):
    if len({*pi,*pj})<4: continue
    n+=1
    for M in classes:
        for j in range(3):
            k,l=[x for x in range(3) if x!=j]
            U1 = EP_pair(M,pi,(j,j),pj,(k,l)); U2 = EP_pair(M,pi,(j,k),pj,(j,l))
            G[j]+=U1-U2; Q[j]+=U2
print("ordered disjoint pair-pairs:", n)
print("aggregate E[g_j] (x n):", [str(g) for g in G])
print("aggregate ratios:", [float(g/q) for g,q in zip(G,Q)])
# per-class item excess of M itself and E3a identity
for M in classes:
    g=[M[j][j]*M[k][l]-M[j][k]*M[j][l] for j,(k,l) in zip(range(3),((1,2),(0,2),(0,1)))]
    det = (M[0][0]*(M[1][1]*M[2][2]-M[1][2]**2)-M[0][1]*(M[0][1]*M[2][2]-M[1][2]*M[0][2])
           +M[0][2]*(M[0][1]*M[1][2]-M[1][1]*M[0][2]))
    print("class g:", g, "product:", g[0]*g[1]*g[2], "det(M):", det)
