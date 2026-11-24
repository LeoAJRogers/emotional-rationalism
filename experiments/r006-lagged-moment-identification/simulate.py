"""Synthetic worlds for the R-006 bench (DESIGN.md section 6). Code licence: MIT.

Item order: cheerful, relaxed (PA); worried, fearful, sad (NA).
Grid per person-period: 6 days x 10 beeps; nominal gap 1 between beeps, 7 overnight.
"""
import numpy as np
from scipy.special import expit, logit, ndtri

N_PERSONS, N_PERIODS, N_DAYS, N_BEEPS = 127, 2, 6, 10
LAM = np.array([0.70, 0.60, 0.70, 0.70, 0.65])
PHI = 0.55
RHO_PN = -0.45
COMPLETENESS = (0.77, 0.70)
CONCENTRATION = 8.0
THRESH = np.array([0.0, 0.6, 1.2, 1.8, 2.4, 3.0])
SD_PERSON_MEAN, SD_PERIOD_SHIFT = 0.8, 0.3
NA_ITEMS, PA_ITEMS = (2, 3, 4), (0, 1)

BASE = dict(
    persistence="blocks",     # 'blocks' (PA, NA factors), 'bipolar', 'two_timescale'
    item_excess=0.0,          # target T1_j for item AR residuals (rho = 0.6)
    rho_item=0.6,
    f2_phi=None,              # second NA factor rate (None = absent)
    f2_load=(0.30, 0.00, -0.30),
    f2_hetero=False,          # R-006b: person p gets f2_load cyclically shifted by p % 3 (no extra RNG draws)
    load_sd=0.0,              # person-specific loading log-SD
    day_load_sd=0.0,          # person-item-day loading log-SD
    phi_logit_sd=0.0,         # person-specific inertia (logit scale SD)
    method=0.0,               # white-noise method factor loading on worried, fearful
    mnar=0.0,                 # missingness slope on the NA factor
    anchor=0.0,               # response anchoring weight
    ordinal=False,
    floors=(0.45, 0.65, 0.50),
)


def world(**kw):
    cfg = dict(BASE)
    cfg.update(kw)
    return cfg


N8 = dict(load_sd=0.3, phi_logit_sd=0.5, ordinal=True, floors=(0.45, 0.65, 0.50), mnar=0.6)
WORLDS = {
    "W0": world(),
    "W0b": world(persistence="bipolar"),
    "W1s": world(item_excess=0.25),
    "W1w": world(item_excess=0.10),
    "W2s": world(f2_phi=0.85),
    "W2f": world(f2_phi=0.20),
    "W2e": world(f2_phi=0.55),
    "W3": world(persistence="two_timescale"),
    "N1": world(load_sd=0.3),
    "N2": world(phi_logit_sd=0.5),
    "N3": world(ordinal=True),
    "N3h": world(ordinal=True, floors=(0.75, 0.75, 0.75)),
    "N4": world(method=0.35),
    "N5": world(mnar=0.6),
    "N6": world(day_load_sd=0.3),
    "N7": world(anchor=0.15),
    "N8": world(**N8),
    "N9": world(**dict(N8, load_sd=0.5)),
    "W1s+N8": world(**N8, item_excess=0.25),
    "W1w+N8": world(**N8, item_excess=0.10),
    "W2s+N8": world(**N8, f2_phi=0.85),
    "W2e+N8": world(**N8, f2_phi=0.55),
}


def gaps():
    g = np.ones(N_DAYS * N_BEEPS - 1)
    g[N_BEEPS - 1::N_BEEPS] = 7.0
    return g


def ar_paths(phi, n, rng, T=N_DAYS * N_BEEPS):
    """Stationary unit-variance AR(1) paths on the nominal grid; phi scalar or (n,)."""
    phi = np.broadcast_to(np.asarray(phi, float), (n,))
    g = gaps()
    x = np.empty((n, T))
    x[:, 0] = rng.standard_normal(n)
    for t in range(T - 1):
        c = phi ** g[t]
        x[:, t + 1] = c * x[:, t] + np.sqrt(1 - c ** 2) * rng.standard_normal(n)
    return x


def var_paths(phi, gamma, n, rng, T=N_DAYS * N_BEEPS):
    """Bivariate VAR(1) with Phi = phi*I and stationary covariance gamma."""
    phi = np.broadcast_to(np.asarray(phi, float), (n,))
    L = np.linalg.cholesky(gamma)
    g = gaps()
    x = np.empty((n, T, 2))
    x[:, 0] = rng.standard_normal((n, 2)) @ L.T
    for t in range(T - 1):
        c = (phi ** g[t])[:, None]
        x[:, t + 1] = c * x[:, t] + np.sqrt(1 - c ** 2) * (rng.standard_normal((n, 2)) @ L.T)
    return x


def simulate(cfg, seed, n_persons=N_PERSONS, return_latent=False):
    rng = np.random.default_rng(seed)
    MP = n_persons * N_PERIODS
    T = N_DAYS * N_BEEPS
    person = np.repeat(np.arange(n_persons), N_PERIODS)
    period = np.tile(np.arange(N_PERIODS), n_persons)

    # person-level parameters (shared by both periods)
    phi_p = PHI * np.ones(n_persons)
    if cfg["phi_logit_sd"] > 0:
        phi_p = expit(logit(PHI) + cfg["phi_logit_sd"] * rng.standard_normal(n_persons))
    phi = phi_p[person]
    lam = np.tile(LAM, (MP, 1))
    if cfg["load_sd"] > 0:
        lam_p = LAM * np.exp(cfg["load_sd"] * rng.standard_normal((n_persons, 5)))
        lam = lam_p[person]
    lam = np.repeat(lam[:, None, :], T, 1)                     # (MP,T,5)
    if cfg["day_load_sd"] > 0:
        dl = np.exp(cfg["day_load_sd"] * rng.standard_normal((MP, N_DAYS, 5)))
        lam = lam * np.repeat(dl, N_BEEPS, 1)

    # shared factors (MP,T)
    if cfg["persistence"] == "blocks":
        f = var_paths(phi, np.array([[1, RHO_PN], [RHO_PN, 1]]), MP, rng)
        fPA, fNA = f[..., 0], f[..., 1]
    elif cfg["persistence"] == "bipolar":
        om = -RHO_PN
        V = ar_paths(phi, MP, rng)
        mP, mN = rng.standard_normal((MP, T)), rng.standard_normal((MP, T))
        fPA = np.sqrt(om) * V + np.sqrt(1 - om) * mP
        fNA = -np.sqrt(om) * V + np.sqrt(1 - om) * mN
    elif cfg["persistence"] == "two_timescale":
        fPA = ar_paths(phi, MP, rng)
        fNA = np.sqrt(0.6) * ar_paths(0.35, MP, rng) + np.sqrt(0.4) * ar_paths(0.90, MP, rng)
    else:
        raise ValueError(cfg["persistence"])
    F = np.stack([fPA, fPA, fNA, fNA, fNA], -1)                # (MP,T,5)
    latent = lam * F

    theta = 1.0 - LAM ** 2
    # item-specific AR residuals
    if cfg["item_excess"] > 0:
        rho = cfg["rho_item"]
        s = cfg["item_excess"] * PHI * LAM ** 2 / rho
        theta = theta - s
        u = np.stack([ar_paths(rho, MP, rng) for _ in range(5)], -1) * np.sqrt(s)
        latent = latent + u
    # second NA factor
    if cfg["f2_phi"] is not None:
        b = np.zeros(5)
        b[list(NA_ITEMS)] = cfg["f2_load"]
        if cfg.get("f2_hetero", False):
            # R-006b heterogeneous F2: which NA item has the negative excess varies by person class.
            bp = np.zeros((n_persons, 5))
            for c in range(3):
                bp[np.arange(n_persons) % 3 == c, 2:5] = np.roll(np.asarray(cfg["f2_load"], float), c)
            b = bp[person][:, None, :]                          # (MP,1,5)
        theta = theta - b ** 2
        eta2 = ar_paths(cfg["f2_phi"], MP, rng)
        latent = latent + eta2[..., None] * b
    # white-noise method factor on worried, fearful
    if cfg["method"] > 0:
        mvec = np.zeros(5)
        mvec[[2, 3]] = cfg["method"]
        theta = theta - mvec ** 2
        latent = latent + rng.standard_normal((MP, T))[..., None] * mvec
    assert np.all(theta > 0), theta
    ystar = latent + rng.standard_normal((MP, T, 5)) * np.sqrt(theta)

    # missingness
    a, b_ = np.array(COMPLETENESS)[period] * CONCENTRATION, (1 - np.array(COMPLETENESS)[period]) * CONCENTRATION
    pi = rng.beta(a, b_)
    lp = logit(np.clip(pi, 1e-6, 1 - 1e-6))[:, None] - cfg["mnar"] * fNA
    obs = rng.random((MP, T)) < expit(lp)

    # response anchoring (latent scale, within day, to the previous answered beep)
    if cfg["anchor"] > 0:
        aw = cfg["anchor"]
        resp = ystar.copy()
        for d in range(N_DAYS):
            last = None
            have = np.zeros(MP, bool)
            for bb in range(N_BEEPS):
                t = d * N_BEEPS + bb
                if last is not None:
                    blend = (1 - aw) * ystar[:, t] + aw * last
                    resp[:, t] = np.where(have[:, None], blend, ystar[:, t])
                upd = obs[:, t]
                last = np.where(upd[:, None], resp[:, t], last if last is not None else resp[:, t])
                have |= upd
        ystar = resp

    # observation
    if cfg["ordinal"]:
        tot_sd = np.sqrt(1 + SD_PERSON_MEAN ** 2 + SD_PERIOD_SHIFT ** 2)
        m = np.full(5, 1.8)
        m[list(NA_ITEMS)] = -ndtri(np.array(cfg["floors"])) * tot_sd
        mu_p = m + SD_PERSON_MEAN * rng.standard_normal((n_persons, 5))
        mu = mu_p[person] + SD_PERIOD_SHIFT * rng.standard_normal((MP, 5))
        z = ystar + mu[:, None, :]
        y = 1.0 + (z[..., None] > THRESH).sum(-1)
    else:
        y = ystar
    y = np.where(obs[..., None], y, np.nan)
    Y = y.reshape(MP, N_DAYS, N_BEEPS, 5)
    if return_latent:
        return Y, person, dict(fNA=fNA.reshape(MP, N_DAYS, N_BEEPS), obs=obs)
    return Y, person
