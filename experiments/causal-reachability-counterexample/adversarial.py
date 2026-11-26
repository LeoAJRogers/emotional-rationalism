"""Adversarial test of imperfect adherence and direct encouragement effects."""
from random import Random

N = 100000

def sample(model, seed=31, n=N, assignment=False, adherence=1., direct=0.):
    r = Random(seed)
    rows = []
    for _ in range(n):
        h = r.randrange(2)
        z = r.randrange(2) if assignment else h
        a = z if r.random() < adherence else h
        y = a if model == 'action' else h
        if r.random() < direct:
            y = z
        rows.append((h, z, a, y))
    return rows

def mean(xs):
    return sum(xs) / len(xs)

def stats(rows):
    return {
        'itt': mean([y for h,z,a,y in rows if z == 1]) - mean([y for h,z,a,y in rows if z == 0]),
        'naive': mean([y for h,z,a,y in rows if a == 1]) - mean([y for h,z,a,y in rows if a == 0]),
        'first_stage': mean([a for h,z,a,y in rows if z == 1]) - mean([a for h,z,a,y in rows if z == 0])
    }

def main():
    print('model,assigned,adherence,direct,ITT,observed_contrast,first_stage')
    conditions = [('action',False,1,0), ('readiness',False,1,0),
                  ('action',True,.7,0), ('readiness',True,.7,0),
                  ('readiness',True,.7,.3)]
    for model, assigned, adherence, direct in conditions:
        s = stats(sample(model, assignment=assigned, adherence=adherence, direct=direct))
        print(f"{model},{assigned},{adherence},{direct},{s['itt']:.4f},{s['naive']:.4f},{s['first_stage']:.4f}")
        if not assigned: assert abs(s['naive'] - 1) < .001
        if assigned and model == 'action': assert .68 < s['itt'] < .72
        if assigned and model == 'readiness' and direct == 0: assert abs(s['itt']) < .02
        if assigned and direct > 0: assert s['itt'] > .25
    print('PASS')

if __name__ == '__main__':
    main()
