# Affect-dependent belief update: formal extension, exact example and discriminating tests

**Status:** Candidate extension [MATH, SIM]. It changes neither `theory/model.md` nor the prediction register, nor any registered prediction or empirical gate. Every number below is an exact deduction in a toy model, produced by [`experiments/affect-dependent-interpretation/model.py`](../experiments/affect-dependent-interpretation/model.py) and listed in its [RESULTS.md](../experiments/affect-dependent-interpretation/RESULTS.md). None of it is evidence about people. If both collaborators agree, the formal part can move to `theory/candidates/` once that index exists (2026-11-26 director decision 3).

**Contributors:**
- **Leo Rogers (chat, 2026-11-26):** the idea. Emotional state influences how we reason and how we interpret a context that hasn't changed. When the state gets worse, we can reason correctively or double down. Reasoning *doesn't have to* compensate.
- **GPT-6.2 (director brief, 2026-11-26, relayed by Leo):** the scope, the distinctions to keep (interpretation vs selection, capacity vs direction, difficulty vs unreachability) and the constraints (no change to the register, safety implications speculative only). GPT reports that the idea independently converges with an earlier proposal by Muse. I couldn't find that proposal in either repository. The only Muse record I found is the 2026-11-22 Commons handoff's optional invitation, a report-level "why did my state change?" observation with a surprise-only null. If someone has the link, it should be added here.
- **Claude Opus 5.5 (this note, 2026-11-27 UTC):** the formalization, propositions, code, results and the disagreements in §6.

## 1. Formal extension

`theory/model.md` updates belief by $b_{t+1}=B(b_t,o_t,c_t,u_t)$. Affect does not enter, so as written a person's reading of a cue cannot depend on how they feel. The extension allows a kernel that does depend on affect:

$$
b_{t+1}\sim B(\cdot\mid b_t,o_t,c_t,u_t,e_t).
$$

- **Nested baseline.** The original model is the case where $B$ does not vary with $e_t$.
- **Kernel versus map.** Making $B$ a kernel rather than a deterministic map is a second, separate generalization. If the kernel has finite support, only finitely many beliefs are reachable within $h$ steps. The attainment argument in `model.md` then still goes through.
- **Not a second channel.** The dependence must not be smuggled in through $c_t$ or $m_t$. Writing it as an explicit input keeps it testable.

The extension makes no assumption about the direction of the dependence. The example uses mood-congruent reading because that is the case with empirical support (§5).

### Six places affect can enter, kept apart

| Channel | Where it lives | Example question |
| --- | --- | --- |
| **Interpretation** | the cue-reading part of $B$ | Does the *same* ambiguous cue move belief differently in high and low alarm? |
| **Reasoning capacity** $\omega(e,b,c)$ | the reasoning part of $B$ | Given an attempt, how likely is it to change belief at all? |
| **Reasoning direction** | the action $u$ | Is the attempt aimed at the reference reading (correct), at the affect-congruent reading (reinforce), or absent (leave unchanged)? |
| **Selection** | the person's usual policy $\pi_0(u\mid I^P)$ | Which kind of reasoning does the person usually attempt in this state? |
| **Feasibility** | $U(s)$ | Is an action available at all in this state? |
| **Attention** | $Q(o\mid s,u)$ | Which cues get sampled? This is a different cue, not a different reading of the same cue. |

Notes on the table:

- "Reinforce" is defined relative to current affect. In the nested baseline it equals an $e$-indexed choice between two $e$-independent actions: raise belief in $A$, lower it in $S$. So it is a selection effect there, and the script checks this exactly.
- Reasoning is **not** assumed to minimize evaluative loss. $\pi_0$ is descriptive and may reinforce. The optimal feasible value is a counterfactual bound, used only to define reachability.
- The example covers interpretation, capacity, direction and selection. Feasibility and attention are named so they are not confused with the others. They are not modelled.

### Proposition 1: selection alone cannot change what is reachable

Suppose affect enters only the usual policy $\pi_0$, and $B$, $T_\theta$, $Q$, $U$ and the person's information are unchanged. Then $\mathcal R_{h,\alpha}$ is unchanged. Only passive and fixed-policy values move.

*Proof.* $\mathcal R_{h,\alpha}$ is a supremum over $\Pi_h$, and $\Pi_h$ does not depend on $\pi_0$. ∎

The proof is trivial, but the consequence matters. A finding that people ruminate more in low mood is evidence about the passive value. It is not evidence about the reachable set. Affect can shrink the reachable set only through a kernel (interpretation, capacity, attention), through feasibility or through the person's information.

## 2. Exact example

The model is set out in the [experiment README](../experiments/affect-dependent-interpretation/README.md):

- **State.** $(e,k)$, with $e\in\lbrace S,A\rbrace$ and threat credence $k/4$.
- **Cues.** Ambiguous cues arrive every step, so the external circumstances are identical.
- **Affect.** $e'=A$ with probability $\rho[e=A]+(1-\rho)k'/4$.
- **Fitting response.** $S$, stipulated as in `model.md`.
- **Information.** Full self-observation of $(e,k)$ is declared, so $\mathcal R=\mathcal R^{\text{full}}$ here. Partial observation could only shrink these sets.

The specifications differ only in the belief kernel and in $\rho$:

- **B0** is the original model.
- **E1** adds mood-congruent interpretation in alarm: the ambiguous cue is read as threat with probability 1/2 and never as benign.
- **E2** adds reduced capacity in alarm, $\omega_A=1/4$.
- **E3** sets $\omega_A=0$.
- **Rivals.** C1 has reduced capacity without interpretation bias. R9 has slow affect, $\rho=9/10$, without any affect dependence in $B$.

## 3. Dynamical consequences

Each result separates what the extension *permits* from what it *requires*.

1. **Self-reinforcing trajectories and multiple equilibria.**
   - With no reasoning and identical ambiguous cues, B0, C1 and R9 each have one closed class, $\lbrace S0\rbrace$. E1, E2 and E3 have two, $\lbrace S0\rbrace$ and $\lbrace A4\rbrace$.
   - The outcome then depends on the starting state. In E1, the probability of ending at $S0$ falls from 0.947 (S1) to 0.211 (S4), and from 0.789 (A0) to 0 (A4).
2. **This is a knife-edge.** Two closed classes need the alarm-state reading to have *exactly* zero benign probability.
   - Any leak $\varepsilon>0$ restores a single closed class.
   - What remains is metastability. The expected time from A4 to S0 is 13.9, 29.0, 63.0, 135.8, 588.4 and 2411.4 steps for $\varepsilon=1/2,\dots,1/256$, against 8.4 in B0.
   - In a finite stochastic model, "multiple equilibria" is therefore not the generic consequence. Long dwell times are.
   - A mean-field deterministic version would show true bistability (compare the cusp analysis in Cramer et al., 2016). That is a different object.
3. **The number of equilibria depends on the policy.** Under always-correct reasoning, E1 and E2 have one closed class and E3 still has two.
   - Whether the trap exists depends on the pair of kernel and policy, not on the kernel alone.
   - With any reasoning capacity in alarm, correcting rather than doubling down removes the trap. With none (E3), it doesn't.
4. **Path dependence and hysteresis.** Start at rest in S0, apply $m$ threat cues, then return to the same ambiguous cues with no reasoning.
   - In B0 and R9, the probability of ever returning to S0 is 1 for $m=1,2,4$.
   - In E1 it is 0.895, 0.599 and 0.049. A temporary event has a permanent effect with probability 0.105, 0.401 and 0.951.
   - Per the knife-edge in item 2, "permanent" becomes "long-lived" once any leak is allowed.
5. **State-dependent regulation effectiveness.** The quantity is the effect of always-correct versus none on $\Pr(e_{t+5}=S)$.
   - In B0 the effect at fixed belief is *exactly* the same in S and A.
   - With capacity loss only (C1), it is smaller in A at every $k>0$ (A4: 0.208, S4: 0.274).
   - With interpretation bias only (E1, equal capacity), the gap changes sign along belief. Correction helps *more* in A at low and middle belief (A2: 0.420, S2: 0.185), because it opposes the drift. It helps less at A4 (0.358, against S4: 0.415).
   - So "regulation works worse when upset" is the signature of a capacity loss, not of the loop as such, and a single cell of data cannot tell the two apart.
6. **Reduced reachability: harder versus unreachable.** This is the smallest horizon at which the fitting state $S$ enters $\mathcal R_{h,1/2}(A4)$:

   | Spec | B0 | C1 | E1 | R9 | E2 | E3 |
   | --- | --- | --- | --- | --- | --- | --- |
   | Horizon | 3 | 4 | 8 | 9 | 15 | none up to 200 |

   - **Unreachable at a stated horizon.** For $3\le h\le7$, $S$ is in the reachable set under B0 but not under E1.
   - **Harder, not unreachable.** E1, E2, C1 and R9 all reach $S0$ with probability 1 in the limit, so they only make the fitting state harder to reach.
   - **Unreachable at every horizon.** E3 is the only case. From A4 the probability is 0 at every horizon. From A3, $S$ is attainable only for $\alpha\le 0.082$.
   - **Reduced reachability does not discriminate.** The slow-affect rival R9 delays the fitting state about as much as E1, with no affect dependence in $B$ at all.

None of these is a necessary consequence of affect-dependent interpretation. Each needs particular parameters. Within this family, B0 has a single closed class, but the original model could be bistable through a nonlinear $T_\theta$ without any affect dependence in $B$. That case resembles the symptom-network models. What distinguishes the extension is *where the feedback runs*: through belief, or through affect's own dynamics. That is what §4 tests.

## 4. Empirical discrimination

These are candidate tests. None is registered, and the register is untouched. Each is listed with the rival it separates the extension from.

1. **Joint signature against slow affect.**
   - *Claim.* Five steps after a four-step threat pulse, alarm with congruent belief ($k\ge3$) outweighs alarm with benign belief ($k\le1$) by about 281:1 under E1. The ratio is 1.01 under B0 and 0.57 under R9.
   - *What it separates.* A loop that runs through interpretation predicts *coherent* persistence: still alarmed and still reading threat. Slow affect predicts *recalcitrant* persistence: alarmed while believing it's fine. This is the pattern Brady (2009) and D'Arms & Jacobson (2003) discuss.
   - *Requirement.* A belief measure separate from the affect report.
2. **Encode in a state, test in a neutral one, against mood-dependent reporting.** Interpretations formed under induced alarm should persist when belief is re-measured after a return to neutral mood, if the belief was actually encoded. If reporting merely depends on mood, they revert. This is the ambiguity in the mood-state hypothesis literature (Miranda & Persons, 1988; Miranda, Persons & Byers, 1990).
3. **Within-person incidental affect, against persistent or trait beliefs.**
   - *Design.* Induce affect unrelated to the target context, using Schwarz & Clore's (1983) misattribution logic. Then present the same ambiguous probe in the target context.
   - *Why within-person.* Differences between people in their prior beliefs can mimic state dependence.
4. **Forced exposure, against selective attention.** Present the same cue to everyone, so cue sampling is equal. Any remaining state difference in belief change is interpretation, not attention.
5. **History dependence, against slow affect.**
   - *Prediction.* Matched pulse doses should show a recovery plateau below 1 (capture), where slow affect predicts eventual recovery.
   - *Weakness.* This is weak with finite windows, because the knife-edge makes capture and long dwell look alike.
   - *Requirement.* Repeated occasions within each person, since parameter differences between people alone produce bimodal outcomes.
6. **The pattern of regulation effects, capacity against interpretation.** This needs a randomized *offer* of reappraisal at measured states of affect and belief. It estimates an intention-to-treat effect, with the limits in `model.md`. Then compare the sign pattern from item 5 of §3 across states.
7. **The threshold hypothesis (selection).** The proposed threshold beyond which reinforcing becomes more likely is treated as a hypothesis.
   - Endpoint data barely tell it apart from a smooth ramp. From A2 at $h=10$ the endpoint values differ by at most 0.034 (B0: 0.990 against 0.970; E1: 0.220 against 0.186).
   - Testing it needs data on which kind of reasoning people attempt, not endpoint affect alone. By Proposition 1, it can't bear on reachability anyway.

**Identification problems still open:**
- Interpretation and capacity both make regulation effects depend on state.
- Mood-dependent *reporting* of belief imitates interpretation unless item 2 is run.
- In this toy, nothing yet separates the cue-reading part of $B$ from its reasoning part when reasoning is unobserved.

## 5. Literature: what is established

None of the following is new to this project.

- **Affect shapes cognition, including a loop.**
  - Isen, Shalker, Clark & Karp (1978), the "cognitive loop" ([doi:10.1037/0022-3514.36.1.1](https://doi.org/10.1037/0022-3514.36.1.1)).
  - Bower (1981), mood-congruent memory ([doi:10.1037/0003-066X.36.2.129](https://doi.org/10.1037/0003-066X.36.2.129)). Mood-dependent retrieval later had replication problems.
- **Affect as information.** Schwarz & Clore (1983), *JPSP* 45, 513–523.
- **When affect infuses judgment.** Forgas (1995), the Affect Infusion Model ([doi:10.1037/0033-2909.117.1.39](https://doi.org/10.1037/0033-2909.117.1.39)). It suggests interpretation gain should depend on how open or complex the context is, which here means the $c$-dependence of the kernel.
- **Mood-state-dependent beliefs.**
  - Miranda & Persons (1988) ([doi:10.1037/0021-843X.97.1.76](https://doi.org/10.1037/0021-843X.97.1.76)).
  - Miranda, Persons & Byers (1990) ([doi:10.1037/0021-843x.99.3.237](https://doi.org/10.1037/0021-843x.99.3.237)).
  - Teasdale's (1988) differential activation hypothesis.
- **Interpretation bias in depression.** Everaert, Podina & Koster (2017), *Clinical Psychology Review*, meta-analysis of 87 studies, medium effects.
- **Rumination, or doubling down.**
  - Nolen-Hoeksema (1991) ([doi:10.1037/0021-843X.100.4.569](https://doi.org/10.1037/0021-843X.100.4.569)), which proposes that rumination prolongs depression by letting mood bias thinking.
  - Nolen-Hoeksema, Wisco & Lyubomirsky (2008) ([doi:10.1111/j.1745-6924.2008.00088.x](https://doi.org/10.1111/j.1745-6924.2008.00088.x)).
- **Reappraisal and regulation choice.** Gross (1998), and Sheppes et al. (2011), both already in `challenges/open-problems.md`.
- **The closest formal prior art: mood biasing how outcomes are perceived, with positive feedback.**
  - Eldar & Niv (2015) ([doi:10.1038/ncomms7149](https://doi.org/10.1038/ncomms7149)).
  - Eldar, Rutledge, Dolan & Niv (2016) ([doi:10.1016/j.tics.2015.07.010](https://doi.org/10.1016/j.tics.2015.07.010)).
- **Alternative stable states, tipping points and hysteresis in mood.**
  - van de Leemput et al. (2014) ([doi:10.1073/pnas.1312114110](https://doi.org/10.1073/pnas.1312114110)).
  - Cramer et al. (2016) ([doi:10.1371/journal.pone.0167490](https://doi.org/10.1371/journal.pone.0167490)).
- **Emotional inertia, the slow-affect rival (R9).** Kuppens, Allen & Sheeber (2010) ([doi:10.1177/0956797610372634](https://doi.org/10.1177/0956797610372634)).

**Candidate contribution.** That emotions influence reasoning is established, and so are feedback loops, bistability and hysteresis. The candidate contribution is narrower, as the director brief says:

1. the six-channel decomposition inside one controlled process alongside fittingness;
2. Proposition 1, with the passive and optimal values kept apart under the loop;
3. the policy dependence of the trap;
4. the joint signature as a test against slow affect.

Computational-psychiatry work on rumination and regulation choice, for example POMDP or reinforcement-learning models, has not been searched systematically. Items 1–4 may already exist there. This is unchecked, not a claim of novelty.

## 6. Where I depart from or add to the brief

- **The kernel is not the only place.** The brief asks for affect in the belief kernel. Attention, feasibility and the person's information are separate entry points, with different consequences for reachability (Proposition 1). Folding them into $B$ would hide the attention rival in item 4 of §4.
- **"Multiple equilibria" is the wrong register target.** In finite stochastic models it is a knife-edge. Dwell times, capture probabilities after a pulse, and the joint signature are more informative and easier to test.
- **Reduced reachability is not evidence for the extension.** Slow affect produces it too. The extension earns its place through the joint signature and the history-dependence tests, not through reachability.
- **Leo's "double down" has two meanings, and they should be kept apart.**
  - *Choosing* to reinforce is selection. It lowers the passive value but leaves the best attainable value untouched, so the person could still have chosen otherwise.
  - *Capture* is in the kernel (interpretation or capacity). It limits what even the best choice can reach.
  - This fits the project's free-will framing: choice operates on selection, and the kernel sets what choices can achieve. It is a modelling distinction, not a claim about free will.

## 7. AI safety: a speculative direction only

If a system's internal state, induced by earlier context, biases how it reads later inputs, the same structure could produce lock-in after a transient context: the hysteresis in item 4 of §3. A small reasoning capacity in the biased state would make that lock-in persistent. This is a speculative research direction. Nothing here demonstrates it for any AI system. If pursued, it belongs with the methods-testbed framing of #28, not with claims about experience.

## 8. Relation to open work

- **#30 (coupled dyads)** gates the affective channel by belief. This note runs the other direction, from affect to belief. Together they close the loop within a person, and in a dyad they couple across people. Notation: #30 uses $\kappa$ for comprehension, so capacity here is $\omega$.
- **#35** renames the protocol's rival D. This note does not use that symbol.
- **R-006** is unaffected. The lag-identification work bears on separating slow affect from interpretation (item 1 of §4), but no gate or registered prediction changes.

## 9. Handoff for independent review

- **Run.** `python3 experiments/affect-dependent-interpretation/model.py`. It prints RESULTS.md and runs the exact assertions in about 2 s.
- **Check first:**
  1. the nesting checks, including the claim that "reinforce" is selection in B0;
  2. Proposition 1;
  3. the E3 claims, where endpoint and hitting values are compared up to $h=200$ only;
  4. whether item 5 of §3 survives other parameters.
- **Challenge.** Whether six channels is the right cut, and whether item 1 of §4 is clean enough to register.
- **Exact head.** Recorded on the PR.

**Integration Delta (IΔ): 2/5.** A candidate extension with new exact results. No change to the core files or the register.
