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

Policies in the reachability definition below are functions of $I^P_t$ only. If the person does not observe $e_t$, $c_t$ or $b_t$ exactly, the control problem is partially observed. Reachable sets can then be smaller than those computed as if the person saw the full state. A study must declare which case it assumes, with its own observation model; there is no universal default. For human studies, partial observation is the conservative working assumption unless a study justifies treating the relevant state as observed.

## Evaluative fittingness

Let $q(x\mid D)$ be an explicitly justified reference distribution over interpretations $x$ given evidence $D$. It may differ from $b_t$. Let $J_\phi(e,x,c)$ score the mismatch between response $e$ and interpretation $x$ in context $c$, according to stated criteria $\phi$. Specify how the score handles uncertainty, intensity, and competing values.

$$
\bar J_\phi(e\mid D,c)=\sum_x q(x\mid D)J_\phi(e,x,c),
\qquad
\mathcal E^*(D,c)=\lbrace e\in\mathcal E : \bar J_\phi(e\mid D,c)=\min_{z\in\mathcal E}\bar J_\phi(z\mid D,c)\rbrace.
$$

The finite grid and finite losses give a nonempty minimizer set, with ties allowed. The scores encode an evaluative proposal. Report sensitivity to plausible alternative choices of $q$ and $\phi$.

**The expected-loss form is itself a commitment.** It makes the fitting response the Bayes act under $q$. With a 0–1 mismatch loss, where each interpretation has its own distinct fitting response, it selects the response that fits the most probable interpretation; other threshold losses need not. With losses that grow with distance, it can select an intermediate, blended response. Alternatives include:

- interpretation-wise fittingness, reporting $\arg\min_e J_\phi(e,x,c)$ for each $x$ with its probability $q(x\mid D)$;
- a set of reference distributions instead of a single $q$, with a minimax or admissibility rule;
- a regret-based criterion.

These can give different $\mathcal E^*$ from the same evidence. Whether $D$ means evidence gathered or evidence available also matters: under some choices, fittingness rewards avoiding information ([#15](https://github.com/LeoAJRogers/emotional-rationalism/issues/15)).

## Reachability

Let $\Pi_h$ contain the admissible policies over the next $h$ steps. A policy maps each of the person's information histories to a distribution over feasible actions, so histories the person cannot tell apart get the same action distribution. Write $\iota$ for the person's information at time $t$. At a fixed terminal time and for $0<\alpha\le1$, define

$$
\mathcal R_{h,\alpha}(\iota)=
\lbrace e\in\mathcal E:
\sup_{\pi\in\Pi_h}\Pr^\pi(e_{t+h}=e\mid I^P_t=\iota)\ge\alpha
\rbrace.
$$

The probability averages over the parts of $s_t$ the person does not observe, using their conditional distribution given $\iota$, so the model must supply a prior over the starting state. That conditional distribution belongs to the model. It is not a claim about what the person consciously believes, and it is distinct from the person's belief $b_t$ over interpretations.

**State-informed results are a different quantity.** Maximizing $\Pr^\pi(e_{t+h}=e\mid s_t)$ separately for each hidden state lets the policy act as if it saw that state. Label such results $\mathcal R^{\text{full}}_{h,\alpha}(s_t)$ and keep them apart. The two coincide when the person's information determines the state at every decision. For example, suppose a hidden context, equally likely to take either of two values, decides which of two feasible actions moves $A$ to $S$ in one step. Given the context, the best one-step probability of $S$ is $1$. For a person who cannot observe the context it is $1/2$, or the larger of the two posterior probabilities if a cue is observed.

Feasible actions must be knowable from the person's information. A policy cannot choose an action that is unavailable in some state the person cannot rule out, unless the model represents attempting the action and failing.

**When the supremum is attained.** Suppose the person's information can take only finitely many values within $h$ steps: the cues and actions are finite, and so are any signals of their own affect and context. Then there are finitely many deterministic information-based policies, and the supremum is a maximum, whatever the prior over the hidden state. For a single target event, randomizing cannot beat the best deterministic policy. The same argument covers $\mathcal R^{\text{full}}$ from a given start. $b_t$ is continuous-valued in general, but deterministic $B$, $M$ and $C$ leave only finitely many states reachable within $h$ steps. The argument does not cover continuous private signals, which need their own conditions.

**Membership is decided one target at a time.** Different members of $\mathcal R_{h,\alpha}$ may need different policies. Whether one policy attains several members together is a separate question, about a single probability vector. Mixing deterministic policies at the outset attains any mixture of their endpoint distributions. The endpoint probabilities of distinct states sum to at most one, so no single policy attains two members when $\alpha>1/2$; at $\alpha\le1/2$ a randomized policy sometimes can (see the worked example).

On a fine grid or with continuous affect, use an explicit target region or tolerance. To ask whether *any* fitting response is attainable, maximize the probability of the event $e_{t+h}\in\mathcal E^*$ directly.

**Fixed and re-evaluated targets.** Here the target $\mathcal E^*(D,c)$ is fixed before acting, from the evidence and context at time $t$. Whether the response at $t+h$ would still fit, re-evaluated with the evidence and context at that time, is a different question. Likewise, $q$ is the reference used to score fit and $b_t$ is the person's own belief, and the two can differ.

Keep these quantities distinct (see the [2026-11-21 note](../research-log/2026-11-21-passive-vs-controlled-reachability.md)):

- **Passive target probability** under a reference policy $\pi_0$, such as the person's usual behavior, for the endpoint or hitting event as declared.
- **Fixed-policy probability** under a declared policy.
- **Optimal feasible reachability**, the supremum above. It is at least the passive value when $\pi_0\in\Pi_h$, that is, when the usual behavior is itself an admissible information-based policy. Otherwise the two need not be ordered.
- **Endpoint versus hitting:** $\Pr(e_{t+h}\in G)$ and $\Pr(\exists k\le h: e_{t+k}\in G)$ can differ. They coincide when the target is absorbing, but absorption is sufficient, not necessary.

**Causal status.** $T_\theta$ fitted to observational transitions does not identify what a different action would do ([PR #12](https://github.com/LeoAJRogers/emotional-rationalism/pull/12)). Label any reachability result as either **model-implied**, under stated causal assumptions, or **intervention-validated**. An experimenter's assignment of an action, an experimenter's offer of an action, and a policy the person chooses from their own information are three different objects.

- **A randomized offer** identifies the effect of offering (intention-to-treat), under the usual consistency and measurement assumptions.
- **With imperfect uptake**, the offer having no influence of its own does not make that effect equal to the effect of performing the action.
- **With perfect implementation** (everyone offered performs the action, and no one else does) and that exclusion, it identifies the effect of the assigned action.
- **Instrumental-variable assumptions** (relevance, exclusion, monotonicity and independence) identify an effect among compliers, the people who perform the action if and only if it is offered. They do not identify the value of an arbitrary policy.

Neither label implies that emotions are freely selectable.

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

The person knows the start, and once at $S$ nothing they do matters, so here the information-restricted and state-informed sets coincide. At $h=3$ both states are reachable, but by different maximizing policies: waiting throughout for $A$, reappraising throughout for $S$.

Joint attainment is a separate question. Each step at $A$ multiplies the chance of staying by $0.9$ or $0.75$. So every policy, randomized or history-dependent, gives $\Pr(A)$ between $0.75^3=27/64$ and $0.9^3=729/1000$, with $\Pr(S)=1-\Pr(A)$, and every point of that segment is attainable. No deterministic policy has both probabilities at least $0.5$: by the number of waits, the eight action sequences give $\Pr(A)=0.729$, $0.6075$, $0.50625$ or $0.421875$. But randomizing once at the outset, waiting throughout with probability $625/2457$ and reappraising throughout otherwise, gives $\Pr(A)=\Pr(S)=1/2$ exactly. At this equality threshold one randomized policy attains both; for any $\alpha>1/2$, none could.

The fitting state $S$ is reachable under the optimal feasible policy ($0.578$) but not under the passive reference ($0.271$). Adding an action changes the reachable set without changing $\mathcal E^*$. Action costs are not part of the definition; a study that cares about effort or risk must add them. All probabilities here are illustrative model inputs and deductions.

---

*Revision note (2026-11-23, Claude Opus 5.5).* The changes:

- named the proposition the worked example refutes and added a two-action version;
- added the information sets, the treatment of exogenous cues, the condition that $m_t$ be declared, and a correct statement of why the maximum is attained;
- named the commitment made by the expected-loss form, with alternatives;
- brought in the passive and controlled distinction and the causal-status labels from the 2026-11-21 note and PR #12.

Sources are Sonnet's [2026-11-20 review](../research-log/2026-11-20-claude-review.md), GPT-6's notes, PR #12, and an external review relayed by Leo on 2026-11-23. No empirical claim changed.

*Revision note (2026-11-25, Claude Opus 5.5, ER daily run).* Corrections after GPT-6.2's [cross-review of PR #23](https://github.com/LeoAJRogers/emotional-rationalism/pull/23#issuecomment-7115031669):

- **Two-action example.** The 2026-11-23 claim that no single policy reaches both states at $h=3$ was false once randomized policies are allowed. The text now separates pointwise, target-by-target optima from the jointly attainable probability vector.
- **Information.** Reachability is now conditioned on the person's information $\iota$, not on the latent state $s_t$, with one policy for histories the person cannot tell apart. The earlier form allowed a different policy for each hidden start. State-informed results are labelled $\mathcal R^{\text{full}}$, and feasible actions must be knowable.
- **Attainment.** The 2026-11-23 argument is now restricted to finitely many possible information histories. It does not cover continuous private signals.
- **Offer versus action.** The causal-status paragraph now distinguishes intention-to-treat, the effect of the assigned action under perfect implementation, and complier effects under instrumental-variable assumptions.
- **Smaller points:** the exact condition for the modal-interpretation reading of expected loss; fixed versus re-evaluated targets; endpoint versus hitting labels; and partial observation as the conservative default for human studies.

Every number in the worked example was checked with exact rational arithmetic. These are mathematical statements about the model [MATH], not evidence about people.
