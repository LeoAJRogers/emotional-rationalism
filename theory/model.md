# Symbolic model

## States and dynamics

Use a discrete-time model with a finite affect grid $\mathcal E\subset\mathbb R^d$. Coordinates may represent intensity, arousal, or other dimensions specified for a study. At time $t$, let $s_t=(e_t,b_t,m_t,c_t)$ contain the current affect, the person's belief distribution over interpretations, a summary of relevant history, and the current context. The person selects a feasible action $u_t\in U(s_t)$, then receives a cue $o_t$. An action can include waiting or attempting reappraisal. For each state, assume a nonempty feasible action set.

For a finite-state prototype, let $Q$ be a conditional distribution over cues, $B$ a belief-update map, and $M,C$ deterministic history and context updates. Together with $T_\theta$ they define the controlled process.

$$
\begin{aligned}
o_t &\sim Q(\cdot\mid s_t,u_t),\\
b_{t+1} &= B(b_t,o_t,c_t,u_t),\\
e_{t+1} &\sim T_\theta(\cdot\mid e_t,b_{t+1},m_t,c_t,u_t,o_t),\\
m_{t+1} &= M(s_t,u_t,o_t,e_{t+1}),\qquad
c_{t+1}=C(s_t,u_t,o_t,e_{t+1}).
\end{aligned}
$$

The Markov assumption depends on the sufficiency of $s_t$. The parameter $\theta$ can vary by participant. $B$ can represent biased or incomplete updating. A dependence in $T_\theta$ specifies a model input; causal interpretation requires a study design or further assumptions. In applications, report and physiology can be noisy measurements of $e_t$.

## Evaluative fittingness

Let $q(x\mid D)$ be an explicitly justified reference distribution over interpretations $x$ given evidence $D$. It may differ from $b_t$. Let $J_\phi(e,x,c)$ score the mismatch between response $e$ and interpretation $x$ in context $c$, according to stated criteria $\phi$. Specify how the score handles uncertainty, intensity, and competing values.

$$
\bar J_\phi(e\mid D,c)=\sum_x q(x\mid D)J_\phi(e,x,c),
\qquad
\mathcal E^*(D,c)=\operatorname*{arg\,min}_{e\in\mathcal E}\bar J_\phi(e\mid D,c).
$$

The finite grid and finite losses give a nonempty minimizer set, with ties allowed. The scores encode an evaluative proposal. Report sensitivity to plausible alternative choices of $q$ and $\phi$.

## Reachability

Let $\Pi_h$ contain admissible policies over the next $h$ steps. A policy chooses feasible actions using only the information available to the person at each decision. At a fixed terminal time and for $0<\alpha\le1$, define

$$
\mathcal R_{h,\alpha}(s_t)=
\left\lbracee\in\mathcal E:
\sup_{\pi\in\Pi_h}\Pr^\pi(e_{t+h}=e\mid s_t)\ge\alpha
\right\rbrace.
$$

For finite observation and action spaces and a finite horizon, the maximum is attained. Different states in this set may require different policies. On a fine grid or with continuous affect, use an explicit target region or tolerance. To ask whether *any* fitting response is attainable, maximize the probability of the event $e_{t+h}\in\mathcal E^*$ directly. Here the target is held fixed at the evaluation time.

## Worked counterexample

Take $\mathcal E=\lbraceA,S\rbrace$, where $A$ denotes high alarm and $S$ low alarm. Start at $A$. After a credible benign cue, fix $q$ on the benign interpretation and set $J_\phi(A)=1$ and $J_\phi(S)=0$ for that interpretation. The only feasible action has probability $0.1$ of moving from $A$ to $S$ per step. State $S$ is absorbing.

Remaining at $A$ for $h$ steps has probability $0.9^h$ by the transition rule, so

$$
\Pr(e_{t+h}=S\mid e_t=A)=1-0.9^h.
$$

At $h=3$ and $\alpha=0.5$, the probability is $0.271$, giving $\mathcal E^*=\lbraceS\rbrace$ and $\mathcal R_{3,0.5}=\lbraceA\rbrace$. At $h=7$ the probability is about $0.522$, so $S$ becomes reachable at the same threshold. These probabilities are illustrative model inputs and deductions.
