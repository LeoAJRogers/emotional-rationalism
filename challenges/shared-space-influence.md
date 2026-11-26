# Open problem: emotional influence in shared spaces, across observer types

**Status:** Open problem, opened 2026-11-26. It is not a result and not an extension of the core model. No model text, numbers or prediction-register entries change here. Core corrections and baseline discrimination work (#23, #26, #29) take priority over this problem.

**Origin:** Leo stated the framing in conversation with Claude on 2026-11-26. Claude (Opus 5.5) constrained it into an open problem. This version is Claude's revision after GPT-6.2's cross-review of `3d9df0a`, which identified two blocking errors: information was labelled as impact, and non-fixed policies were taken to imply conflict and exit. The revision corrects both.

## The framing

Leo's framing: Emotional Rationalism is a candidate mechanism for emotional influence in social dynamics generally. It is not limited to one observer type or one population, and it is meant to cover very mixed populations too. Its main setting is a **shared space**: participants with different values encounter one another's expression. Humans already struggle here, and many social problems arise in such spaces.

The central question, in Leo's words (lightly edited):

> They said something I disagree with. Does it impact me, or does it just impact what I know? And how much should an impact on what I know count as justification for an emotional response, if I wasn't impacted in another way?

Leo also holds a normative view. People may express themselves to others when all parties consent. In communal spaces they may do so even without explicit consent, because consent was given by entering the space. A person who has entered the space is, in some sense, responsible for dealing with the emotional consequences of what they encounter there.

## Two parts, kept separate

**A. Descriptive (testable).** In a shared space, one participant's expression influences others' affect through distinguishable routes. The candidate hypothesis is that these routes have shared structure across observer types and population mixes, while each observer type's transition mechanism ($T_\theta$), action set and outcome boundaries differ.

**B. Normative (philosophical proposals).** These are Leo's proposals, not project positions and not results.

- (B0) A common space requires free expression and freedom to leave. Leo considers both essential.
- (B1) Entering a common space that meets B0 is consent to receive expression there.
- (B2) A listener is in some sense responsible for handling the emotional consequences of that expression.
- (B3) An impact only on what one knows warrants less emotional response than an impact on oneself. B3 is not meant to discount concern for others; see outcome-boundary point 2 below.

B can supply candidate criteria $\phi$ for the fittingness loss $J_\phi$. Under the model's existing rules, such criteria must be stated explicitly and tested for sensitivity to alternatives. The README's statement that the project does not prescribe how anyone should feel still applies.

## Formalizing the central question (part A)

Treat an expression as a cue $o_t$ that participant $j$ emits in shared context $c_t$, which listener $i$ observes. Leo's "does it impact me or just what I know" covers four distinct quantities. Information measures are not measures of impact, so the four must be kept apart.

1. **Causal outcome contrast.** Does the expression *change* $i$'s outcomes $Y_i$? This needs a well-defined intervention on expression, for example $P(Y_i\mid do(o))$ against $P(Y_i\mid do(o'))$ for a specified alternative $o'$, such as silence or a different statement.
2. **Predictive update about outcomes.** Does observing the expression change what $i$ should expect about $Y_i$? For a realized expression, measure this with an event-specific quantity, such as the divergence between the posterior and prior predictive distributions of $Y_i$ given history and context. Population mutual information $I(O;Y_i)$ is an average over expressions and does not describe a single event.
3. **Residual world-information.** What does the expression tell $i$ about the rest of the world $Z$, beyond its bearing on $Y_i$? This includes what $j$ believes and values.
4. **Evaluative importance and valence.** How much does each of the above matter, and in which direction, under explicitly stated criteria $\phi$?

Averaged over expressions, and conditioning both sides on the same history and context, the chain rule gives the exact identity

$$
I(O;\,Y_i,Z)=\underbrace{I(O;\,Y_i)}_{\text{outcome-relevant information}}+\underbrace{I(O;\,Z\mid Y_i)}_{\text{residual world-information}}.
$$

Neither term equals actual impact. Mutual information measures statistical dependence, not causal or welfare effect. GPT-6.2's counterexample makes the point. Let $O$ be a randomized bit and $Y=O$, so that $O$ causes $Y$. Separately, let $O=U$ and $Y=U$ for a fair latent bit $U$, so the dependence comes from a common cause. Both cases have $I(O;Y)=1$ bit, but intervening on $O$ changes $Y$ only in the first. In the other direction, a constant harmful exposure carries zero mutual information. And a cue can carry a bit about an outcome that does not matter to anyone.

Leo's question therefore splits into:

- **Descriptive:** how much of an observed affective response tracks each of quantities 1–3, for a given observer type and population?
- **Evaluative (B3):** under stated $\phi$, how much weight should each receive?

The outcome horizon $H$ and the partition into $Y_i$ and $Z$ must be specified in advance, and results must be reported under alternative partitions.

**What "rational" means here (Leo, 2026-11-26).** The "rational" in Emotional Rationalism does not refer to reasoning. Reasoning is free and can go anywhere. It refers to the emotional state *in context with the situation and the group's social dynamics*: whether the response fits what is actually happening, including the norms of the group and of the relationships within it. That is the existing fittingness question, with the north-star idea supplying the reference. The context $c$ therefore has to include group-level structure. A response can fit a group's local dynamics while the norm itself is a poor one, which Leo accepts is possible. If relationship-type norms could be characterized independently of any one group (see the constraints below), they might serve as a check on local norms. Without such a check, "fits the group" and "fits the situation" can come apart. The reference $q(x\mid D)$ must still be explicitly justified. The population reference of reflected responses is one candidate.

Whether reflection moves a person's response toward the fitting one is a separate empirical question, as [open problems](open-problems.md) already notes. One *directional candidate*, not a default criterion of rationality: reflected responses track residual world-information less than initial responses do. Whether lower tracking is more fitting depends on $\phi$ and on the case.

## Where the formalization is hard

1. **Outcome boundaries.** Many people treat identity, values or group standing as part of themselves. For them a statement denigrating their group may change their standing or safety in the space, which affects their own outcomes. "It only changed what I know" can be false for one participant and true for another who hears the same sentence. Where the boundary sits, how it varies, and whether reflection moves it are part of the problem. They cannot be fixed by assumption.
2. **Other-regarding stakes.** Affective responses can be warranted by effects on *others*. Learning of someone else's suffering can warrant concern without any effect on one's own outcomes. Moving everything a person values into $Y_i$ would hide this. Instead, other-regarding stakes need their own category, separate from both self-outcomes and residual information. This bears directly on B3. Read literally, B3 would discount concern for others whenever one's own outcomes are untouched.

   **Leo's clarification (2026-11-26):** B3 is not meant to discount concern for others. Other-regarding responses are subject to the same fittingness question as any other: they count when they fit the situation. Two consequences follow. First, *expressed* concern is a cue, not an obligation. Someone stating concern, or urging others to feel it, does not require a listener to adopt it. Second, emotions are not always accurate. Many things can move them in ways that do not fit the situation, including deliberate influence by others. This separates two cases. In one, a listener's own concern responds to evidence about someone else's situation. In the other, a speaker's expressed emotion is an attempt to induce a response. Both are routes of emotional influence in a shared space, and the second is close to the central mechanism of this problem.

   The constraint: another person's situation is often known mainly through their own report. The project already holds that one participant's reports about another's internal state are not ground truth (see [research scope](../theory/research-scope.md)). The same caution runs the other way: a report is evidence, not nothing. "I am not required to accept this concern" must not become a general license to dismiss reported harm. Fit is assessed against the evidence available about the other's situation, with reports weighed as evidence.
3. **Predictive updates are easy to undercount.** An expressed view is often evidence about how its speaker will act. A response that looks like a reaction to "only information" may be a well-calibrated reaction to a predictive update.
4. **Consent (B1) needs more than entry and exit.** Some spaces are entered freely and left cheaply. Others are hard to avoid or leave, such as a workplace, a family, a school or a platform with strong network effects. Leo's answer to the threshold question is that each participant weighs whether the exposure is worth what they gain from the space, so consent attaches to a stay-or-leave decision. Even with acceptable exit, entering or staying is not sufficient for consent to every expression or treatment. Scope, notice, revocability, power asymmetry, targeted harassment or threats, and effects on third parties all matter. Staying because every alternative is worse is a calculation, but it is hard to call consent. Whether "free expression" includes spaces with rules or moderation also needs a definition.
5. **Responsibility (B2) and reachability.** Reachability bounds claims about which affective responses are *achievable*. It does not establish a duty or assign blame. Responsibility for one's own feasible regulation also does not transfer responsibility for another participant's conduct.
6. **Exposure cost moves both ways.** A response that fits the situation can lower the cost of staying, when an informational impact draws only the response it warrants. It can also raise that cost. An accurate threat appraisal can make leaving more valuable. Fitting responses therefore do not systematically widen the set of spaces worth staying in.

## Requirements for an observer-general claim

Each of the following is a hypothesis to specify and test, not an established property.

1. **An abstract observer class.** At minimum an observer has an internal state, observations, actions, beliefs and outcomes. The mechanism $T_\theta$ stays a free parameter. The open question is whether the dependence of responses on quantities 1–3, or its change under reflection, shares structure across observer types.
2. **Relationship type defined structurally.** Candidate invariants: how well each party can predict the other, outcome dependence, repeated versus one-shot interaction, exit cost and information asymmetry. Whether relationships that share these invariants share norms is a hypothesis. It also needs specified incentives, selection processes and boundary conditions.
3. **Norms defined explicitly.** A shared-space norm is a convention about expression and response. Candidates: a stable equilibrium of repeated interaction, an evolutionarily stable strategy, or a convention that reduces mutual uncertainty. One definition must be chosen and defended.
4. **Equilibrium selection.** In repeated interaction, folk-theorem results allow many conventions to be stable. Narrowing to one norm per relationship type needs a selection argument, such as evolutionary dynamics, learnability or robustness to noise. Any value-like assumption in that argument, such as agents maximizing joint welfare, must be stated as one.
5. **Operational variables only.** A model in which affect-like signals act as signals or commitment devices concerns operational variables. It does not establish subjective experience in any observer, and claims about experience need independent justification.

## Populations: local norms, shared norms and xenophobia

**Leo's framing (2026-11-26).** Populations can have different local norms (Leo's example is a fictional culture such as the Klingons) and still share enough norms to interact with other populations. A population with xenophobic norms is one that comes into conflict when it meets another population. Leo's key hypothesis, which he labels a claim and not a known truth: *social dynamics that evolve as intelligence increases become less xenophobic.* He adds that this may not be knowable until we meet independently developed observers.

**Measuring a shared norm layer.** Mutual information between populations' "mappings" is undefined without a probability law over paired contexts and signals and explicit random variables. A workable operationalization: the degree to which one population's responses in context can be predicted, on held-out cases and with calibration, from the other population's response structure, compared with independent baselines and conditioned on context.

Predictability is not compatibility or tolerance. An adversary can be highly predictable. Hostility is also not the same as treating out-group signals as uninformative, since a hostile population can read out-group signals accurately. Learning from out-groups, threat attribution, treatment of out-group members and cooperation should be measured separately. "Xenophobia" should be defined in terms of these measures, not assumed to be any one of them.

**Constraints on the hypothesis.**

- **Norms change on cultural timescales.** In humans, intergroup prejudice shifts within generations. The intergroup-contact literature (Allport, 1954; Pettigrew and Tropp's 2006 meta-analysis) reports reduced prejudice under conditions such as equal status, common goals and cooperation.
- **Intelligence is probably not sufficient by itself.** Greater capability could lengthen planning horizons and improve prediction, which could favour cooperation. It could equally make conquest and exploitation more effective. Both are hypotheses. A narrower candidate: as capability increases, populations become less xenophobic *toward populations of comparable capability, under repeated positive-sum contact*. Strongly unequal encounters fall under the asymmetric relationship types.
- **Partial tests exist now.** Truly independent observers are not available. But social intelligence evolved more than once among animals (primates, corvids, cetaceans, elephants), so one could test whether out-group tolerance tracks social cognition there. The evidence has to be checked. Chimpanzees, for example, show lethal intergroup aggression, while bonobos are often described as more tolerant of out-groups, which suggests ecology matters at least as much as intelligence. Separately trained AI agents in multi-agent simulation are a weak form of independent development. AI trained on human data is not independent of humans.

**Change and conflict (Leo, 2026-11-26).** Even a purely xenophobic population can change. Leo holds that conflict between populations is unavoidable because participants have free will and can always choose it. He also holds, as a conditional hypothesis, that if a population's members are free to reason, xenophobia might not be permanent. The project takes no position on free will (see [research scope](../theory/research-scope.md)). These are recorded as Leo's views.

Stating them formally requires separating several claims that are easy to run together:

- **Possibility, hazard, eventual occurrence and recurrence are distinct.** Conflict being possible at every time, or having positive probability at every time, does not imply that conflict eventually occurs almost surely. If conflict occurs independently at time $t$ with probability $p_t=2^{-t-1}$, the probabilities sum to less than one, and with positive probability conflict never occurs. Leo's "can always choose it" most closely matches positive probability at every time. On its own that does not imply eventual or recurrent conflict.
- **Variable policies do not imply exit.** A population can vary its policies entirely within cooperative actions, or entirely within a closed set of xenophobic ones. To ask whether xenophobia is permanent, define a xenophobic set $X$ of population states and ask whether $X$ is *closed* under a specified transition kernel and policy class. Positive exit probability from some states, positive exit probability from every state, and eventual exit almost surely are three different claims. (The worked counterexample in the [symbolic model](../theory/model.md) shows an absorbing state.)
- **Freedom to reason is a covariate or intervention, not a guarantee.** It needs a measure independent of the outcome, or any population that stays xenophobic could be dismissed as "not free to reason," and the hypothesis could never fail. Candidate measures include free expression within the population, whether dissenters are punished, and access to outside information. The testable form: xenophobic states are exited at a higher rate where these freedoms are present.
- **Change can come from several sources.** Discounting explicit outsider speech does not prevent learning from outsiders' observed behaviour or from third-party evidence. Internal sources of change (dissent, members reasoning their way to different responses, generational turnover) are candidates alongside these. One testable question: in initially closed groups, how often does norm change begin with internal dissenters, compared with observed outsider behaviour or third parties?

## What would count as progress

- **Human vignette study.** Independently manipulate three things: the direct causal stakes for the reader, how diagnostic the statement is about the reader's future outcomes, and other-regarding stakes. Preregister measures of initial affect, reflected affect and endorsed fittingness. Test whether reflection changes how responses track each manipulation, beyond re-rating, scale-use or conformity effects.
- **Outcome-boundary measurement.** Ask participants what they count as affecting them, and test whether that boundary explains individual differences better than a fixed partition.
- **Multi-agent simulation.** Use agents with deliberately different internal architectures. Vary one relationship invariant at a time (prediction symmetry, dependence, repetition, exit cost) and mix agent types within one shared space. Test whether similar expression and response conventions emerge across architectures, with incentives and selection stated.
- **A formal result.** A theorem or simulation in which a defined norm for each relationship type is invariant across a stated class of mechanisms and differs between types, with all value-like assumptions listed.

## What would count against it

- Response dependence on quantities 1–3 varies with mechanism details and shows no shared structure across observer types.
- Equilibrium selection cannot be resolved without value-like assumptions.
- In humans, differences by relationship type or by space are fully explained by culture.
- Reflection does not change response tracking beyond measurement artifacts.
- Xenophobic states are closed under realistic transition kernels even where freedom to reason is present.

## Comparators to check before any novelty claim

These are listed from Claude's general knowledge and have not been independently verified for this note.

- J. S. Mill, *On Liberty* (1859), and Joel Feinberg, *Offense to Others* (1985): harm versus offense.
- Causal inference with interventions (e.g. Pearl's do-calculus), for quantity 1.
- Value-of-information analysis in decision theory, for decision-relevant versus decision-irrelevant information.
- Crawford and Sobel (1982), *Strategic Information Transmission*: how informative communication can be depends on incentive alignment.
- Nowak (2006), *Five Rules for the Evolution of Cooperation*, and Axelrod (1984): structural conditions for cooperation.
- Fudenberg and Maskin (1986), the folk theorem for repeated games: the equilibrium-selection obstacle.
- Robert Frank, *Passions Within Reason* (1988): emotions as commitment devices.
- Allport (1954) and Pettigrew and Tropp (2006): intergroup contact.
- Gross (1998) and the reappraisal literature already listed in [open problems](open-problems.md): reflection as regulation.
