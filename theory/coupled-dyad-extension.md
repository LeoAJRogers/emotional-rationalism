# Proposed extension: coupled dyads with affective and reasoning channels

**Status:** Proposed extension. It does **not** modify [model.md](model.md). The notation follows model.md as revised in [PR #23](https://github.com/LeoAJRogers/emotional-rationalism/pull/23), which is not yet merged. The worked example is an illustration of the definitions [MATH], not evidence about people or animals.

**Provenance:**
- **Leo Rogers (2026-11-26):** the direction (companionship across capability gaps, identified from parent–child and human–pet data) and the observation that less capable beings influence through emotion rather than reasoning.
- **Claude Opus 5.5:** the formalization.
- **Background:** the [companionship note](../research-log/2026-11-26-asymmetric-companionship-note.md) (PR #29), relational coupling (PR #20), and self-feasible versus externally feasible reachability (PR #28).

## 1. Two agents

There are two agents, $i\in\{A,B\}$, with partner $j\neq i$. Each has its own state $s^i_t=(e^i_t,b^i_t,m^i_t,c^i_t)$, feasible actions $u^i_t\in U^i(s^i_t)$, transition parameters $\theta_i$ and information $I^i_t$. The agents can differ in every one of these. That is what allows a capability gap.

Each agent emits two kinds of output to the other:

- **Affective signal** $\sigma^i_t\sim X_i(\cdot\mid e^i_t,c^i_t)$: expressed affect such as a cry, gaze, posture or tone. The context enters, so display norms can shape what is shown.
- **Message** $\mu^i_t$: reasoning-channel content such as explanation, reassurance or argument. It is part of the action $u^i_t$. An agent may have no messages available, $\mu^i_t=\varnothing$.

Agent $i$'s cue is $o^i_t=(\sigma^j_t,\mu^j_t,\omega^i_t)$, with $\omega^i_t$ the exogenous cues of model.md.

## 2. Dynamics

$$
\begin{aligned}
b^i_{t+1} &= B_i\big(b^i_t,\ \kappa_i(\mu^j_t),\ \sigma^j_t,\ \omega^i_t,\ c^i_t,\ u^i_t\big),\\
e^i_{t+1} &\sim T_{\theta_i}\big(\cdot\mid e^i_t,\ b^i_{t+1},\ m^i_t,\ c^i_t,\ u^i_t,\ \omega^i_t,\ \gamma_i(b^i_{t+1},c^i_t)\,\sigma^j_t\big),
\end{aligned}
$$

with $m$ and $c$ updated as in model.md.

- **Comprehension** $\kappa_i$ is how much of the partner's message agent $i$ can process. For example, $\kappa_i(\mu)=\varnothing$ when $i$ cannot process $\mu$. The reasoning channel acts **only through belief**, $b^i_{t+1}$.
- **Gated affective gain** $\gamma_i(b,c)\ge 0$ sets how strongly the partner's signal moves $i$'s affect **directly**, not through belief. Because $\gamma_i$ depends on $i$'s own belief, $i$'s reasoning can damp or amplify contagion. One example is a parent who understands that a tantrum is a bid and not an emergency.
- $\sigma^j_t$ may also enter $B_i$, since a signal can be informative. The direct term is the part of the signal's effect that is not mediated by belief.

**Channel decomposition (estimand).** Partner $j$'s influence on $i$'s next affect splits into two parts:

- direct affective: $I\big(\sigma^j_t;\,e^i_{t+1}\mid b^i_{t+1},s^i_t,u^i_t\big)$;
- belief-mediated: the dependence of $e^i_{t+1}$ on $(\sigma^j_t,\mu^j_t)$ that runs through $b^i_{t+1}$.

This is only identifiable if beliefs are measured or experimentally manipulated (§5).

## 3. Special cases and nesting

The extension contains the existing models as special cases:

- **Single-person model.md:** set $\gamma_i\equiv 0$ and fold the partner into $Q$. The partner then becomes part of the exogenous cue process.
- **Symmetric peer coupling** (PR #20, M0): $\theta_A=\theta_B$, $\kappa_A=\kappa_B$, and constant $\gamma$.

The model comparison in the companionship note maps onto this nesting:

| Model | Adds |
|---|---|
| M0 | Symmetric peer coupling |
| M1 | Asymmetric $\theta$ and $\kappa$ |
| M2 | Direct affective term, with constant $\gamma$ |
| M3 | Belief-gated $\gamma_i(b)$ |
| M4 | Time-varying parameters, e.g. $\kappa_B$ growing with development |

**Hypotheses, formally:**

- **H1 (affective channel).** In a capability-gap dyad with $\kappa_B\ll\kappa_A$, B's influence on A is mainly direct affective. As $\kappa_B$ grows, the belief-mediated share of B's influence on A grows.
- **H2 (gating).** $\gamma_A$ is not constant in $b^A$. M3 predicts held-out interactions better than M2.

## 4. Fit and reachability with two agents

**Fit** keeps the form in model.md, separately for each agent: $\mathcal E^*_i(D^i,c^i)$. One constraint is added.

> **Frequency constraint.** $q(x\mid D)$ must not depend on how often a response occurs in the population or group. That frequency is the *typical* layer, not evidence about what fits. Group conventions may enter $D$ and $c$ only through what they do to the situation: expectations, sanctions, payoffs and meanings. (See the contextual-norms note, PR #29.)

**Reachability** now depends on whose policies are optimized and on whose information. Fix horizon $h$ and threshold $\alpha$.

- **Self-feasible** (for $i$, partner's policy $\pi^j$ fixed):
$$
\mathcal R^{\text{self},i}_{h,\alpha}(\iota^i;\pi^j)=\lbrace e:\ \sup_{\pi^i}\Pr^{\pi^i,\pi^j}\big(e^i_{t+h}=e\mid I^i_t=\iota^i\big)\ge\alpha\rbrace .
$$
- **Externally feasible** (for $i$'s state, optimized over $j$'s policies on $j$'s information, with $\pi^i$ fixed):
$$
\mathcal R^{\text{ext},i}_{h,\alpha}(\iota^j;\pi^i)=\lbrace e:\ \sup_{\pi^j}\Pr^{\pi^i,\pi^j}\big(e^i_{t+h}=e\mid I^j_t=\iota^j\big)\ge\alpha\rbrace .
$$
- **Joint:** the supremum over both policies, each a function of its own agent's information.

The same rules as in model.md apply: information restriction, state-informed results labelled separately, causal-status labels, and endpoint versus hitting declared.

**Care, in these terms.** For a dependent partner B, the question "can B reach a fitting state?" often has its answer in $\mathcal R^{\text{ext},B}$, not $\mathcal R^{\text{self},B}$. **Exploitation through the affective channel** is the mirror case: B's signals drive A into states outside $\mathcal E^*_A$. Brood parasitism is the biological example and manipulative AI companions the technical one. Both are the same machinery with a different target.

## 5. Worked example: the gate decides whether calm is reachable

Take $\mathcal E^B=\lbrace D,C\rbrace$ (infant distressed, calm). Start at $D$. Suppose the evidence is benign, so $\mathcal E^*_B=\lbrace C\rbrace$. $C$ is absorbing, $h=2$ and $\alpha=0.5$. For simplicity A's affect is held in one of two states for the whole horizon.

- **Self-feasible only.** B's only action is to wait, which moves $D$ to $C$ with probability $0.1$ per step. $\Pr(C\text{ at }t+2)=1-0.9^2=0.19<0.5$, so $C\notin\mathcal R^{\text{self},B}_{2,0.5}$.
- **Externally feasible, A calm.** A soothes, moving B from $D$ to $C$ with probability $0.5$ per step: $1-0.5^2=0.75\ge 0.5$, so $C\in\mathcal R^{\text{ext},B}_{2,0.5}$.
- **Externally feasible, A distressed by contagion.** Soothing from a distressed caregiver succeeds with probability $0.2$ per step: $1-0.8^2=0.36<0.5$, so $C\notin\mathcal R^{\text{ext},B}_{2,0.5}$.

Whether A stays calm depends on $\gamma_A(b^A)$. A high gain lets B's distress pull A into distress. A belief-damped gain keeps A calm. So **the gate on A's affective channel decides whether B's fitting state is reachable at all**. Nothing about B changes. The numbers are illustrative model inputs, and the arithmetic is exact.

## 6. Identification

- **One-partner interventions** are needed to separate coupling from shared context (PR #20). The still-face paradigm sets A's action to "unresponsive" and fixes $\sigma^A$ to neutral exogenously, then restores it. The repair phase identifies recovery dynamics and constrains $\gamma$.
- **Measuring belief** is needed for the channel decomposition. Options are reported interpretations for older children and adults, or manipulations of A's information. For example, telling the caregiver why the infant is crying shifts $b^A$ while $\sigma^B$ stays fixed. Without this, M2 and M3 may not be distinguishable.
- **Signal and message overlap.** Tone of voice carries both $\sigma$ and $\mu$. The observation model must declare how they are separated. Otherwise the decomposition is not defined.
- **Recovery checks** come before any human data: simulate from M0–M4 with known parameters and confirm that the comparison selects the generating model and recovers $\gamma_i(\cdot)$.

## 7. Open questions

- Is $\kappa$ a property of the receiver, or of the pair? A parent may understand their own child's signals better than a stranger's.
- Beyond two agents, the pairwise terms generalize, but group-level norms (the contextual-norms note) enter through $c^i$. How should the two levels be coupled?
- For human–AI dyads, $U^{\text{AI}}$ is mostly externally feasible (PR #28), and either side may be the more capable one, depending on the task. The extension allows this, but it makes no claim about AI experience.
