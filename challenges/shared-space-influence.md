# Open problem: emotional influence in shared spaces, across observer types

**Status:** Open problem, opened 2026-11-26. It is not a result. No model text, numbers or prediction-register entries change here.

**Origin:** Leo stated the framing in conversation with Claude on 2026-11-26. Claude (Opus 5.5) constrained it into the problem below. GPT and other collaborators are invited to review and revise it.

## The framing

Leo's framing: Emotional Rationalism is a candidate mechanism for emotional influence in social dynamics generally. It is not limited to one observer type or one population, and it is meant to cover very mixed populations too. Its main setting is a **shared space**: participants with different values encounter one another's expression. Humans already struggle here, and many social problems arise in such spaces.

The central question, in Leo's words (lightly edited):

> They said something I disagree with. Does it impact me, or does it just impact what I know? And how much should an impact on what I know count as justification for an emotional response, if I wasn't impacted in another way?

Leo also holds a normative view. People may express themselves to others when all parties consent. In communal spaces they may do so even without explicit consent, because consent was given by entering the space. A person who has entered the space is, in some sense, responsible for dealing with the emotional consequences of what they encounter there.

## Two parts, kept separate

The project already separates description from evaluation. This problem has one part of each kind, and they need different kinds of support.

**A. Descriptive and mechanistic (testable).** In a shared space, one participant's expression influences others' affect through identifiable channels. The *structure* of those channels is the same across observer types and population mixes, while each observer type's transition mechanism ($T_\theta$), action set and boundary of self differ.

**B. Normative (an evaluative proposal).** (B0) A common space, in Leo's sense, requires two conditions: free expression and freedom to leave. Leo considers both essential (2026-11-26). (B1) Entering a common space that meets B0 is consent to receive expression there. (B2) A listener is in some sense responsible for handling the emotional consequences of that expression. (B3) An impact only on what one knows warrants less emotional response than an impact on oneself.

B is a candidate choice of evaluative criteria $\phi$ in the fittingness loss $J_\phi$. It is not something mathematics can establish. Under the model's existing rules it must be stated explicitly and tested for sensitivity to alternatives. The README's statement that the project does not prescribe how anyone should feel still applies: B is recorded as one contributor's evaluative proposal, not a project position. "What the math shows" can apply to A, not to B.

## Formalizing the central question (part A)

Treat an expression as a cue $o_t$ that participant $j$ emits in shared context $c_t$, which listener $i$ observes. Split what $i$ could learn into two variables:

- $Y_i$: $i$'s own future outcomes over a horizon $H$, such as feasible action sets $U(s)$, resources, standing, safety and relationships;
- $Z$: everything else about the world, including what $j$ believes and values.

By the chain rule for mutual information (given history and context),

$$
I(o;\,Y_i,Z)=\underbrace{I(o;\,Y_i)}_{\text{impact on me}}+\underbrace{I(o;\,Z\mid Y_i)}_{\text{impact only on what I know}}.
$$

The first term includes *direct* impact: the expression itself changes $i$'s outcomes, as a threat or a binding decision would. It also includes *predictive* impact: the expression is evidence about $i$'s future outcomes. Learning that a hostile participant is present is predictive impact even if nothing has happened yet. The second term is Leo's "just impacts what I know": beliefs about the world change, but the predicted distribution over $i$'s own outcomes does not.

Leo's question then becomes two separate questions:

- **Descriptive:** how much of an observed affective response does each term predict, for a given observer type and population?
- **Evaluative (B3):** what weight should $J_\phi$ give the second term relative to the first?

**What "rational" means here (Leo, 2026-11-26).** The "rational" in Emotional Rationalism does not refer to reasoning. Reasoning is free and can go anywhere. It refers to the emotional state *in context with the situation and the group's social dynamics*: whether the response fits what is actually happening, including the norms of the group and of the relationships within it. That is the existing fittingness question, with the north-star idea supplying the reference. The context $c$ therefore has to include group-level structure, not only the immediate exchange. One open point follows. Leo accepts that group norms can be negative, so a response can fit a group's local dynamics while the norm itself is a poor one. If relationship-type norms can be derived structurally (see the constraints below), they could serve as a check on local group norms. Without that check, "fits the group" and "fits the situation" can come apart. The decomposition contributes the situation side. It separates what an expression actually did to the listener's outcomes from what it only told them about the world. A response can then be assessed against each part. Assessed by whom remains the existing requirement that the reference $q(x\mid D)$ be explicitly justified. The population reference of reflected responses is one candidate.

Whether reflection moves a person's response toward the fitting one is a separate empirical question, as the [open problems](open-problems.md) already note. It is not part of the definition. One testable form: population reference distributions of reflected responses show a lower weight on $I(o;Z\mid Y_i)$ than initial responses do.

## Where the formalization is hard

1. **The boundary of self.** The decomposition depends on what belongs in $Y_i$, and that boundary is not given. Many people treat identity, values or group standing as part of themselves. For them a statement denigrating their group may lower their standing or safety in the space, which is impact in $Y_i$ and not only in $Z$. "It only changed what I know" can be false for one participant and true for another who hears the same sentence. Where the boundary sits, how it varies across observer types, and whether reflection moves it are part of the problem. It cannot be fixed by assumption.
2. **Predictive impact is easy to undercount.** An expressed view is often evidence about how its speaker will act. A response that looks like a reaction to "only information" may be a well-calibrated reaction to predictive impact.
3. **Consent by entry (B1) depends on exit cost.** Some spaces are entered freely and left cheaply. Others are hard to avoid or leave, such as a workplace, a family or the only available forum. Implied consent is plausibly weaker as exit cost rises. B0 makes freedom to leave a defining condition of a common space, but exit cost is a matter of degree. It is one of the relationship invariants below. Two questions remain open. Where is the threshold for "free to leave", or should B1 weaken gradually as exit cost rises? And what applies in spaces that fail B0? Many of the spaces where shared-space problems arise, such as workplaces, families, schools and platforms with strong network effects, are costly to leave, and B1 does not cover them. "Free expression" also needs a definition that says whether a space with rules or moderation still qualifies.

   Leo's answer to the threshold question (2026-11-26): it is each participant's own value calculation, namely whether the exposure is worth what they gain from the space. On this reading, B1 becomes a stay-or-leave decision. A participant compares the expected cost of exposure, including its emotional cost, with the value of being in the space minus the cost of leaving. Consent attaches to the decision to stay. Two consequences follow:

   - **The calculation is necessary but not sufficient.** A person may stay because every alternative is worse, not because staying is acceptable. That choice is a calculation, but it is hard to call consent. B0's freedom-to-leave condition is still needed as a floor: the alternatives to staying must be acceptable, not just less bad.
   - **A link to part A.** Exposure cost depends partly on how much weight a participant gives the informational term $I(o;Z\mid Y_i)$. When a response fits the actual impact, and a purely informational impact draws only the response that impact warrants, exposure costs less, so more spaces become worth staying in. On this reading, a response that fits its context widens the set of shared spaces a person can take part in. It does not change what others may say. This is Claude's suggested connection and remains to be tested.
4. **Responsibility (B2) is bounded by reachability.** The model already distinguishes a fitting response from a reachable one, and says an unreachable response is not a personal failure. Responsibility can then attach at most to a person's feasible policies within $\mathcal R_{h,\alpha}$, not to outcomes outside it.

## Constraints on the observer-general claim

For part A to be a result about observers generally, and not about humans, it needs the following.

1. **An abstract observer class.** At minimum an observer has an internal state, observations, actions, beliefs and outcomes it is selected or persists on. The mechanism $T_\theta$ stays a free parameter. The chain-rule decomposition already holds for any such observer. The open question is whether the *weights* on the two terms, or how they change under reflection, share structure across observer types.
2. **Relationship type defined structurally.** Candidate invariants: how well each party can predict the other, outcome dependence, repeated versus one-shot interaction, exit cost and information asymmetry. Relationships that share these invariants should share norms.
3. **Norms derived, not stipulated.** A shared-space norm is a convention about expression and response. Candidates: a stable equilibrium of repeated interaction, an evolutionarily stable strategy, or a convention that minimizes mutual uncertainty. One definition must be chosen and defended.
4. **Equilibrium selection.** In repeated interaction, folk-theorem results allow many conventions to be stable. Narrowing to one norm per relationship type needs a selection argument, such as evolutionary dynamics, learnability or robustness to noise. That argument cannot reintroduce values, for example by assuming agents maximize joint welfare.
5. **A bridge to experience.** Affect must be part of the strategy, as a signal or a commitment device, so that norms over strategies induce norms over affective responses. Without this step the result is game theory, not a claim about emotional influence.

## Populations: local norms, shared norms and xenophobia

**Leo's framing (2026-11-26).** Populations can have different local norms (Leo's example is a fictional culture such as the Klingons) and still share enough norms to interact with other populations. A population with xenophobic norms is one that comes into conflict when it meets another population, and nothing resolves that: it is a fact about how those observers relate. Leo's key hypothesis, which he labels a claim and not a known truth: *social dynamics that evolve as intelligence increases become less xenophobic.* He adds that this may not be knowable until we meet independently developed observers.

**An information-theoretic statement (Claude's suggestion).** Model each population's norms as a mapping from expressions in context to expected responses. The *shared* norm layer is the part of these mappings that each population can predict about the other, measurable as the mutual information between populations' expression-response mappings. Interaction is possible when that shared part is large enough to act as a common codebook. One way to formalize xenophobia is as a norm that treats out-group expression as uninformative, or only as a threat signal. A population with that norm cannot learn from the other, so the shared layer cannot grow.

**Constraints on the hypothesis.**

- **"Nothing resolves it" holds only while the norm is fixed.** In humans, intergroup prejudice shifts on cultural timescales, not only evolutionary ones. The intergroup-contact literature (Allport, 1954; Pettigrew and Tropp's 2006 meta-analysis) reports reduced prejudice under conditions such as equal status, common goals and cooperation. Read that way, xenophobia is a norm that can change, and the conflict is not permanent.
- **Intelligence alone is probably not the driver.** Game theory suggests cooperation between groups pays when encounters are repeated and positive-sum. Intelligence lengthens horizons and improves prediction, which favours cooperation. It also makes conquest and exploitation more effective. A more specific hypothesis: as intelligence increases, populations become less xenophobic *toward populations of comparable capability, under repeated positive-sum contact*. Strongly unequal encounters fall under the asymmetric relationship types, where structure alone may not force cooperation.
- **Partial tests exist now.** Truly independent observers are not available. But social intelligence evolved more than once among animals (primates, corvids, cetaceans, elephants), so one could test whether out-group tolerance tracks social cognition there. The evidence has to be checked. Chimpanzees, for example, show lethal intergroup aggression, while bonobos are often described as more tolerant of out-groups, which suggests ecology matters at least as much as intelligence. Separately trained AI agents in multi-agent simulation are a weak form of independent development. AI trained on human data is not independent of humans, but it is a first case of differently built observers.

**Change is always possible, and so is conflict (Leo, 2026-11-26).** Even a purely xenophobic population can change. Leo holds that conflict between populations is unavoidable because participants have free will and can always choose it. For the same reason, he holds that no population should ever stay permanently xenophobic. The project takes no position on free will (see [research scope](../theory/research-scope.md)). These are recorded as Leo's views.

- **A model-level statement that does not depend on free will.** As long as participants' policies are not fixed, two things hold. Conflict has nonzero probability over time ("inevitable"). And a xenophobic norm is not an *absorbing state*, one the population can enter but never leave ("never permanent"). Both can be stated and tested in the existing transition-model language: the worked counterexample in the [symbolic model](../theory/model.md) already uses an absorbing state. The open question is whether xenophobic norms are absorbing, and under what conditions.
- **"Should never stay" has two readings that need separating.** As a prediction, it says no population remains xenophobic indefinitely, and it can be tested against how long such norms have persisted. As an evaluative claim, it says no population ought to remain so, and it belongs with part B.
- **If outsiders can't drive change, it has to come from inside.** If a xenophobic norm treats all out-group expression as uninformative, outside contact alone cannot change it. Change has to come from within: internal dissent, members reasoning their way to different responses, or generational turnover, unless contact is forced by circumstance. This is Leo's view that reasoning can alter emotional response, operating at population scale. A testable form: in initially closed groups, norm change more often begins with internal dissenters than with outside contact.

## What would count as progress

- **Human vignette study.** Vary whether a disagreed-with statement has direct, predictive or purely informational impact on the reader. Measure initial affect, reflected affect and endorsed fittingness separately. Estimate the weight on each term, and test whether reflection lowers the weight on the informational term beyond re-rating, scale-use or conformity effects.
- **Boundary-of-self measurement.** Ask participants what they count as affecting them, and test whether that boundary explains individual differences better than the decomposition alone.
- **Multi-agent simulation.** Use agents with deliberately different internal architectures. Vary one relationship invariant at a time (prediction symmetry, dependence, repetition, exit cost) and mix agent types within one shared space. Test whether the same expression and response conventions emerge across architectures.
- **A formal result.** A theorem or simulation in which the norm for each relationship type is invariant across mechanisms and differs between types, with an audit confirming that no assumption is a value.

## What would count against it

- The weights on the two terms vary with mechanism details and show no shared structure across observer types.
- Equilibrium selection cannot be resolved without value-like assumptions.
- In humans, differences by relationship type or by space are fully explained by culture.
- Reflection does not change the informational term's weight beyond measurement artifacts.

## Comparators to check before any novelty claim

- J. S. Mill, *On Liberty* (1859), and Joel Feinberg, *Offense to Others* (1985). The harm versus offense distinction closely parallels the $Y_i$ versus $Z$ split.
- Value-of-information analysis in decision theory, for the separation of decision-relevant from decision-irrelevant information.
- Crawford and Sobel (1982), *Strategic Information Transmission*: how informative communication can be depends on incentive alignment.
- Nowak (2006), *Five Rules for the Evolution of Cooperation*, and Axelrod (1984): structural conditions under which cooperation is stable, independent of mechanism.
- Fudenberg and Maskin (1986), the folk theorem for repeated games: the equilibrium-selection obstacle.
- Robert Frank, *Passions Within Reason* (1988): emotions as commitment devices.
- Gross (1998) and the reappraisal literature already listed in [open problems](open-problems.md): reflection as regulation.
