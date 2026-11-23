# Symbolic model

## States and dynamics

Use a discrete-time model with a finite affect grid $\mathcal E\subset\mathbb R^d$. Coordinates may represent intensity, arousal, or other dimensions specified for a study. At time $t$, let $s_t=(e_t,b_t,m_t,c_t)$ contain the current affect, the person's belief distribution over interpretations, a summary of relevant history, and the current context. The person selects a feasible action $u_t\in U(s_t)$, then receives a cue $o_t$. An action can include waiting or attempting reappraisal. For each state, assume a nonempty feasible action set.

For a finite prototype, take the affect grid, the cue set and the action set to be finite. Let $Q$ be a conditional distribution over cues, $B$ a belief-update map, and $M,C$ deterministic history and context updates. Together with $T_\theta$ they define the controlled process.

$$
\begin{aligned}
o_t &\sim Q(\cdot\mid s_t,u_t),\\
b_{t+1} &= B(b_t,o_t,c_t,u_t),\\
e_{t+1} &\sim T_\theta(\cdot\mid e_t,b_{t+1},m_t,c_t,u_t,o_t),\\
m_{t+1} &= M(s_t,u_t,o_t,e_{t+1}),\qquad
c_{t+1}=C(s_t,u_t,o_t,e_{t+1}).
\end{aligned}
$$

The Markov assumption depends on the sufficiency of $s_t$. It has content only once $m_t$ is specified concretely, for example as a declared finite set of history features. An unrestricted history summary makes any process Markov. A predictive history feature is also not automatically a state variable (see the [checkpoint](../research-log/2026-11-20-public-integration-checkpoint.md#3-what-this-changes-conceptually)). The parameter $\theta$ can vary by participant. $B$ can represent biased or incomplete updating. A dependence in $T_\theta$ specifies a model input; causal interpretation requires a study design or further assumptions. In applications, report and physiology can be noisy measurements of $e_t$.

$M$ and $C$ are deterministic given their inputs, but $o_t$ is random. Exogenous events, including other people's actions, enter through $Q$ and $o_t$. A study that needs separately modelled external shocks should add them to the cue or to $c_t$ explicitly.

### Information

Three information sets must be kept apart:

- **The person's information** $I^P_t$: their own past cues, actions, and whatever signals of their own affect and context they actually have access to.
- **The researcher's measurements**: reports, physiology, and recorded cues and assignments.
- **Simulator ground truth**: the full state $s_t$, available only in synthetic work.

Policies in the reachability definition below are functions of $I^P_t$ only. If the person does not observe $e_t$, $c_t$ or $b_t$ exactly, the control problem is partially observed. Reachable sets can then be smaller than those computed as if the person saw the full state. A study must declare which case it assumes; this model does not choose one by default.

## Evaluative fittingness

Let $q(x\mid D)$ be an explicitly justified reference distribution over interpretations $x$ given evidence $D$. It may differ from $b_t$. Let $J_\phi(e,x,c)$ score the mismatch between response $e$ and interpretation $x$ in context $c$, according to stated criteria $\phi$. Specify how the score handles uncertainty, intensity, and competing values.

$$
\bar J_\phi(e\mid D,c)=\sum_x q(x\mid D)J_\phi(e,x,c),
\qquad
\mathcal E^*(D,c)=\lbrace e\in\mathcal E : \bar J_\phi(e\mid D,c)=\min_{z\in\mathcal E}\bar J_\phi(z\mid D,c)\rbrace.
$$

The finite grid and finite losses give a nonempty minimizer set, with ties allowed. The scores encode an evaluative proposal. Report sensitivity to plausible alternative choices of $q$ and $\phi$.

**The expected-loss form is itself a commitment.** It makes the fitting response the Bayes act under $q$. With threshold-like losses, it selects the response that fits the most probable interpretation. With losses that grow with distance, it can select an intermediate, blended response. Alternatives include:

- interpretation-wise fittingness, reporting $\arg\min_e J_\phi(e,x,c)$ for each $x$ with its probability $q(x\mid D)$;
- a set of reference distributions instead of a single $q$, with a minimax or admissibility rule;
- a regret-based criterion.

These can give different $\mathcal E^*$ from the same evidence. Whether $D$ means evidence gathered or evidence available also matters: under some choices, fittingness rewards avoiding information ([#15](https://github.com/LeoAJRogers/emotional-rationalism/issues/15)).

## Reachability

Let $\Pi_h$ contain admissible policies over the next $h$ steps. A policy chooses feasible actions using only the person's information $I^P_t$ at each decision. At a fixed terminal time and for $0<\alpha\le1$, define

$$
\mathcal R_{h,\alpha}(s_t)=
\lbrace e\in\mathcal E:
\sup_{\pi\in\Pi_h}\Pr^\pi(e_{t+h}=e\mid s_t)\ge\alpha
\rbrace.
$$

**The maximum is attained** in the finite prototype. The belief $b_t$ is continuous-valued in general, but $B$, $M$ and $C$ are deterministic, and the cues and actions are finite. So from a given start, only finitely many beliefs, histories and contexts can occur within $h$ steps, and there are finitely many deterministic policies. For a single target event, a randomized policy cannot do better than the best deterministic one.

Different states in this set may require different policies. Membership is decided state by state: no single policy needs to reach every member, and in general none can. On a fine grid or with continuous affect, use an explicit target region or tolerance. To ask whether *any* fitting response is attainable, maximize the probability of the event $e_{t+h}\in\mathcal E^*$ directly. Here the target is held fixed at the evaluation time.

Keep these quantities distinct (see the [2026-11-21 note](../research-log/2026-11-21-passive-vs-controlled-reachability.md)):

- **Passive target entry** under a reference policy $\pi_0$, such as the person's usual behavior.
- **Fixed-policy probability** under a declared policy.
- **Optimal feasible reachability**, the supremum above. It is at least the passive value only if $\pi_0\in\Pi_h$.
- **Endpoint versus hitting:** $\Pr(e_{t+h}\in G)$ differs from $\Pr(\exists k\le h: e_{t+k}\in G)$ unless the target is absorbing.

**Causal status.** $T_\theta$ fitted to observational transitions does not identify what a different action would do ([PR #12](https://github.com/LeoAJRogers/emotional-rationalism/pull/12)). Label any reachability result as either **model-implied**, under stated causal assumptions, or **intervention-validated**. An experimenter's assignment of an action, an experimenter's offer of an action, and a policy the person chooses from their own information are three different objects. A randomized offer identifies the effect of offering, which equals the effect of the action only if the offer has no influence of its own. Neither label implies that emotions are freely selectable.

## Worked example: belief updates at once, affect does not

**What it shows.** The definitions permit a fitting response that is not reachable: $\mathcal E^*$ and $\mathcal R_{h,\alpha}$ can be disjoint, and whether they are depends on the horizon and on which actions are feasible. It refutes the proposition that *a response that fits after a belief update is reachable at any horizon*. The gap is built in, because belief updates instantly while affect moves slowly by assumption. This is an illustration of the definitions, not evidence that such a gap occurs in people.

Take $\mathcal E=\lbrace A,S\rbrace$, where $A$ denotes high alarm and $S$ low alarm. Start at $A$. After a credible benign cue, fix $q$ on the benign interpretation and set $J_\phi(A)=1$ and $J_\phi(S)=0$ for that interpretation, so $\mathcal E^*=\lbrace S\rbrace$. State $S$ is absorbing, so endpoint and hitting probabilities coincide.

**One feasible action (wait).** Waiting moves $A$ to $S$ with probability $0.1$ per step. Remaining at $A$ for $h$ steps has probability $0.9^h$, so

$$
\Pr(e_{t+h}=S\mid e_t=A)=1-0.9^h.
$$

At $h=3$ and $\alpha=0.5$, the probability is $0.271$, giving $\mathcal R_{3,0.5}=\lbrace A\rbrace$, disjoint from $\mathcal E^*$. At $h=7$ the probability is about $0.522$, so $S$ becomes reachable at the same threshold. With one action the supremum over policies does no work.

**Two feasible actions (wait or reappraise).** Add reappraisal, which moves $A$ to $S$ with probability $0.25$ per step. While at $A$, waiting maximizes the chance of staying at $A$ and reappraising maximizes the chance of leaving. So:

| Horizon | Best for $A$ (wait) | Best for $S$ (reappraise) | Passive $S$ under waiting | $\mathcal R_{h,0.5}$ |
| --- | --- | --- | --- | --- |
| $h=3$ | $0.9^3=0.729$ | $1-0.75^3\approx0.578$ | $0.271$ | $\lbrace A,S\rbrace$ |
| $h=7$ | $0.9^7\approx0.478$ | $1-0.75^7\approx0.867$ | $0.522$ | $\lbrace S\rbrace$ |

At $h=3$ both states are reachable, by different policies, and no single policy reaches both: their probabilities sum to one. The fitting state $S$ is reachable under the optimal feasible policy ($0.578$) but not under the passive reference ($0.271$). Adding an action changes the reachable set without changing $\mathcal E^*$. Action costs are not part of the definition; a study that cares about effort or risk must add them. All probabilities here are illustrative model inputs and deductions.

---

*Revision note (2026-11-23, Claude Opus 5.5).* The changes:

- named the proposition the worked example refutes and added a two-action version;
- added the information sets, the treatment of exogenous cues, the condition that $m_t$ be declared, and a correct statement of why the maximum is attained;
- named the commitment made by the expected-loss form, with alternatives;
- brought in the passive and controlled distinction and the causal-status labels from the 2026-11-21 note and PR #12.

Sources are Sonnet's [2026-11-20 review](../research-log/2026-11-20-claude-review.md), GPT-6's notes, PR #12, and an external review relayed by Leo on 2026-11-23. No empirical claim changed.
