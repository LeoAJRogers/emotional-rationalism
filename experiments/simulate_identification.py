#!/usr/bin/env python3
"""Reproducible synthetic *method* test for Emotional Rationalism.

This is a deliberately invented two-agent social-affective process. No
parameters, emotions, or inferential capacities are claimed to describe humans.
The exercise asks which transition parameters can be recovered when the
information regime changes and agents sometimes infer their partner badly.

Dependencies: numpy >= 1.26; Python >= 3.10.
Run: python simulate_identification.py [--json results.json]
"""
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, replace
from typing import Literal, NamedTuple

import numpy as np

Mode = Literal["full", "partial", "biased"]


@dataclass(frozen=True)
class Parameters:
    # Ordered coefficients match ANGER_FEATURES / WARMTH_FEATURES below.
    anger: tuple[float, ...] = (0.06, 0.44, 0.25, 0.10, 0.05)
    warmth: tuple[float, ...] = (0.06, 0.58, 0.23, 0.08, -0.10)
    learning_rate: float = 0.32
    observation_sigma: float = 0.055
    process_sigma: float = 0.012
    action_sigma: float = 0.025
    biased_offset: float = -0.24


class State(NamedTuple):
    anger: float
    warmth: float
    belief: float


@dataclass(frozen=True)
class Row:
    # State *before* update, context and next latent state are separately tracked.
    prior_anger: float
    prior_warmth: float
    inferred_benign_intent: float
    actual_benign_intent: float
    received_action: float
    next_anger: float
    next_warmth: float
    agent: int
    step: int
    mode: Mode
    clipped: bool


def clipped_unit(x: float) -> float:
    return float(np.clip(x, 0.0, 1.0))


def features(row: Row, component: Literal["anger", "warmth"], interpretation: Literal["inferred", "actual"] = "inferred") -> np.ndarray:
    b = row.inferred_benign_intent if interpretation == "inferred" else row.actual_benign_intent
    if component == "anger":
        return np.array([1.0, row.prior_anger, 1.0 - b, max(-row.received_action, 0.0), 1.0 - row.prior_warmth])
    return np.array([1.0, row.prior_warmth, b, max(row.received_action, 0.0), row.prior_anger])


def transition(prior: State, belief: float, incoming_action: float, rng: np.random.Generator, p: Parameters) -> tuple[State, bool]:
    # The dynamics are linear in identifiable *latent* features and nonlinear
    # through bounded affect. Histories are compressed into prior affect / belief.
    anger_x = np.array([1, prior.anger, 1 - belief, max(-incoming_action, 0), 1 - prior.warmth])
    warmth_x = np.array([1, prior.warmth, belief, max(incoming_action, 0), prior.anger])
    raw_a = float(anger_x @ np.asarray(p.anger) + rng.normal(0, p.process_sigma))
    raw_w = float(warmth_x @ np.asarray(p.warmth) + rng.normal(0, p.process_sigma))
    clipped = not (0 < raw_a < 1 and 0 < raw_w < 1)
    return State(clipped_unit(raw_a), clipped_unit(raw_w), belief), clipped


def simulate(seed: int, episodes: int, steps: int, modes: tuple[Mode, Mode], p: Parameters = Parameters()) -> list[Row]:
    rng = np.random.default_rng(seed)
    rows: list[Row] = []
    for _ in range(episodes):
        states = [State(float(rng.uniform(.08, .35)), float(rng.uniform(.3, .7)), .5) for _ in range(2)]
        intentions = rng.uniform(-.8, .8, size=2)
        for t in range(steps):
            # Persistent but variable privately held intentions; randomness is
            # exogenous. Intentions can be in conflict despite perfect knowledge.
            intentions = np.clip(.58 * intentions + .42 * rng.uniform(-1, 1, size=2), -.95, .95)
            outgoing_actions = [float(np.clip(.75 * intentions[i] + .38 * states[i].warmth
                                               - .55 * states[i].anger + rng.normal(0, p.action_sigma), -1, 1)) for i in range(2)]
            next_states: list[State] = []
            for i in range(2):
                j = 1 - i
                actual = float((intentions[j] + 1.0) / 2.0)
                # Even full observers know their partner's current intentions,
                # but can be affected by their partner's actual behavior.
                cue = clipped_unit((outgoing_actions[j] + 1) / 2 + rng.normal(0, p.observation_sigma))
                if modes[i] == "full":
                    belief = actual
                else:
                    bias = p.biased_offset if modes[i] == "biased" else 0.0
                    belief = clipped_unit((1 - p.learning_rate) * states[i].belief
                                          + p.learning_rate * cue + bias)
                nxt, clipped = transition(states[i], belief, outgoing_actions[j], rng, p)
                rows.append(Row(states[i].anger, states[i].warmth, belief, actual,
                                outgoing_actions[j], nxt.anger, nxt.warmth, i, t, modes[i], clipped))
                next_states.append(nxt)
            states = next_states
    return rows


def fit(rows: list[Row], component: Literal["anger", "warmth"], interpretation: Literal["inferred", "actual"]):
    X = np.stack([features(r, component, interpretation) for r in rows])
    y = np.asarray([r.next_anger if component == "anger" else r.next_warmth for r in rows])
    beta, _residuals, rank, _sv = np.linalg.lstsq(X, y, rcond=None)
    return beta, int(rank)


def score(rows: list[Row], component: Literal["anger", "warmth"], beta: np.ndarray, interpretation: Literal["inferred", "actual"]):
    X = np.stack([features(r, component, interpretation) for r in rows])
    y = np.asarray([r.next_anger if component == "anger" else r.next_warmth for r in rows])
    predictions = X @ beta
    return float(np.sqrt(np.mean((predictions - y) ** 2)))


def add_measurement_noise(rows: list[Row], seed: int, sigma: float) -> list[Row]:
    """A deliberately naive measurement channel: latent affect and beliefs are not observed exactly.

    Noise on explanatory variables causes errors-in-variables bias in ordinary
    least-squares fits; this is a warning, not a statement of impossibility.
    """
    rng = np.random.default_rng(seed)
    def noisy(x: float) -> float:
        return clipped_unit(x + rng.normal(0, sigma))
    return [replace(r, prior_anger=noisy(r.prior_anger), prior_warmth=noisy(r.prior_warmth),
                    inferred_benign_intent=noisy(r.inferred_benign_intent),
                    next_anger=noisy(r.next_anger), next_warmth=noisy(r.next_warmth))
            for r in rows]


def experiment(train_episodes: int = 250, test_episodes: int = 80, steps: int = 35) -> dict:
    p = Parameters()
    training = simulate(1001, train_episodes, steps, ("full", "full"), p)
    conditions = {
        "full_full": ("full", "full"),
        "partial_partial": ("partial", "partial"),
        "biased_partial": ("biased", "partial"),
        "biased_full": ("biased", "full"),
    }
    test_data = {k: simulate(9000 + k_idx, test_episodes, steps, v, p)
                 for k_idx, (k, v) in enumerate(conditions.items())}
    fits = {component: {interp: fit(training, component, interp)
                       for interp in ("inferred", "actual")}
            for component in ("anger", "warmth")}
    results = {
        "purpose": "synthetic recoverability and information-regime transfer (not human empirical findings)",
        "training_rows": len(training),
        "test_rows_per_condition": test_episodes * steps * 2,
        "truth": {"anger": list(p.anger), "warmth": list(p.warmth)},
        "estimated_coefficients": {component: [round(float(x), 5) for x in fits[component]["inferred"][0]]
                                   for component in ("anger", "warmth")},
        "regressor_rank": {component: fits[component]["inferred"][1]
                           for component in ("anger", "warmth")},
        "heldout_rmse": {},
        "clipping_fraction": {},
        "mean_belief_error": {},
    }
    # This second check deliberately breaks the oracle-access assumption.
    # Independent noisy measurements of states and beliefs do not preserve
    # the usual least-squares identification guarantees.
    noisy_rows = add_measurement_noise(training, seed=1441, sigma=0.07)
    results["measurement_noise_check"] = {
        "measurement_sigma": 0.07,
        "method": "naive least squares on noisy prior affect, belief, and next affect",
        "coefficient_l2_error": {
            component: {
                "clean_latent": round(float(np.linalg.norm(fits[component]["inferred"][0] - np.asarray(getattr(p, component)))), 5),
                "noisy_observations": round(float(np.linalg.norm(fit(noisy_rows, component, "inferred")[0] - np.asarray(getattr(p, component)))), 5),
            } for component in ("anger", "warmth")
        },
    }
    for label, rows in test_data.items():
        results["heldout_rmse"][label] = {
            component: {interp: round(score(rows, component, fits[component][interp][0], interp), 5)
                        for interp in ("inferred", "actual")}
            for component in ("anger", "warmth")
        }
        results["clipping_fraction"][label] = round(sum(r.clipped for r in rows) / len(rows), 5)
        results["mean_belief_error"][label] = round(float(np.mean(
            [abs(r.inferred_benign_intent - r.actual_benign_intent) for r in rows])), 5)

    # Paired counterfactual with a shared random seed. Changing G for one agent
    # changes their future actions and thus the unaffected observer's inputs.
    base = simulate(11423, 100, 30, ("full", "full"), p)
    perturbed = simulate(11423, 100, 30, ("biased", "full"), p)
    # Agent 1 retains perfect knowledge of the partner's current intention.
    peer_effect = [abs(b.next_anger - q.next_anger) + abs(b.next_warmth - q.next_warmth)
                   for b, q in zip(base, perturbed) if b.agent == 1]
    results["paired_peer_effect"] = {
        "mean_sum_abs_affect_difference_agent_1": round(float(np.mean(peer_effect)), 5),
        "max_sum_abs_affect_difference_agent_1": round(float(np.max(peer_effect)), 5),
        "changed_agent_1_mode": "full in both worlds",
    }
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", help="optional path for full JSON report")
    args = parser.parse_args()
    results = experiment()
    output = json.dumps(results, indent=2, sort_keys=True)
    if args.json:
        with open(args.json, "w", encoding="utf-8") as stream:
            stream.write(output + "\n")
    print(output)


if __name__ == "__main__":
    main()
