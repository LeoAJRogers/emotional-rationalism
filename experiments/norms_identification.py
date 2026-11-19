"""Synthetic social-norm identification demonstration (NOT empirical psychology).

Two simulated agents interact; one community norm influences the context they
experience. All latent states and norm coordinates are known by experimenter.
Requires numpy. Run: python norms_identification.py
"""
import json
import numpy as np

PARAMS = {
    'affiliative': (.60, .18, .10, .16),
    'territorial': (.60, .18, .10, .16),
    'different': (.25, .48, -.10, .07),
}
NORM_CENTERS = {
    'affiliative': (.78, .88),
    'territorial': (-.78, -.88),
    'different': (.78, .88),
}


def simulate(group, seed, episodes=500, steps=8):
    """Generated columns: z, partner z, cue, cue*descriptive, cue*injunctive, next z."""
    rng = np.random.default_rng(seed)
    rows=[]
    rho, gamma, beta_desc, beta_inj = PARAMS[group]
    desc0, inj0 = NORM_CENTERS[group]
    for ep in range(episodes):
        # Intentional within-population norm variation for estimability.
        desc = np.clip(desc0 + rng.normal(0,.22),-1,1)
        inj = np.clip(inj0 + rng.normal(0,.22),-1,1)
        z = rng.normal(0,.17,2)
        for t in range(steps):
            cue = rng.choice([-1.,1.], size=2)
            next_z = rho*z + gamma*z[::-1] + beta_desc*cue*desc + beta_inj*cue*inj + rng.normal(0,.025,2)
            for i in range(2):
                rows.append([z[i],z[1-i],cue[i],cue[i]*desc,cue[i]*inj,next_z[i]])
            z = next_z
    return np.asarray(rows)


def design(rows, model):
    if model=='raw': return np.column_stack([np.ones(len(rows)),rows[:,[0,1,2]]])
    if model=='norm': return np.column_stack([np.ones(len(rows)),rows[:,[0,1,3,4]]])
    raise ValueError(model)


def fit(rows, model):
    X=design(rows,model)
    coeff=np.linalg.lstsq(X,rows[:,-1],rcond=None)[0]
    return coeff


def rmse(rows, coeff, model):
    return float(np.sqrt(np.mean((rows[:,-1]-design(rows,model)@coeff)**2)))


def main():
    training=np.concatenate([simulate('affiliative',11,500),simulate('territorial',22,500)])
    evals={g:simulate(g,800+i,160) for i,g in enumerate(PARAMS)}
    raw=fit(training,'raw')
    norm=fit(training,'norm')
    # Separate population-specific transition after local calibration.
    local=fit(simulate('different',99,125),'norm')
    results={
        'status':'Synthetic method test only; fixed hand-designed parameters; latent states and independently measured norms available to estimator',
        'training_rows':len(training),
        'test_rows_by_group':{g:len(v) for g,v in evals.items()},
        'fitted_shared_coefficients':{'raw':[round(float(x),5) for x in raw],'norm':[round(float(x),5) for x in norm]},
        'true_shared_coefficients':{'intercept':0.,'persistence':.60,'partner_feedback':.18,'descriptive_cue':.10,'injunctive_cue':.16},
        'heldout_RMSE':{g:{'raw_pooled':round(rmse(rows,raw,'raw'),5),'norm_conditioned_shared':round(rmse(rows,norm,'norm'),5), **({'calibrated_population_specific':round(rmse(rows,local,'norm'),5)} if g=='different' else {})} for g,rows in evals.items()},
        'calibrated_different_coefficients':[round(float(x),5) for x in local],
    }
    assert results['heldout_RMSE']['affiliative']['norm_conditioned_shared'] < results['heldout_RMSE']['affiliative']['raw_pooled']
    assert results['heldout_RMSE']['territorial']['norm_conditioned_shared'] < results['heldout_RMSE']['territorial']['raw_pooled']
    assert results['heldout_RMSE']['different']['calibrated_population_specific'] < results['heldout_RMSE']['different']['norm_conditioned_shared']
    print(json.dumps(results,indent=2))


if __name__=='__main__': main()
