# Affect-dependent belief update: exact illustration

**Status:** candidate, illustrative [MATH, SIM]. No human data, no fitted parameters, no registered predictions. The research note is [2026-11-27-affect-dependent-belief-update](../../research-log/2026-11-27-affect-dependent-belief-update.md).

## Run

```bash
python3 model.py           # prints every table in RESULTS.md, then runs the assertions
python3 model.py --check   # assertions only
```

Standard library only (`fractions`). Runtime is about 2 s. Every probability is an exact rational, and the assertions check the claims the note relies on. [RESULTS.md](RESULTS.md) is the script's own output. Regenerate it rather than editing it by hand.

## Model in one paragraph

The state is $(e,k)$, with affect $e\in\lbrace S,A\rbrace$ (low or high alarm) and threat credence $k/N$, where $N=4$. Each step runs in this order: the person chooses an action in {none, correct, reinforce} from $(e,k)$, which declares full self-observation; a cue arrives; belief updates through a kernel that may depend on $e$; then $e'=A$ with probability $\rho[e=A]+(1-\rho)k'/N$. The fitting response is stipulated as $S$, as in `theory/model.md`.

| Spec | Interpretation of the ambiguous cue | Capacity $\omega$ (S, A) | $\rho$ |
| --- | --- | --- | --- |
| B0 (original model, nested) | down 1/2 in both states | 1/2, 1/2 | 1/2 |
| E1 | S: down 1/2. A: up 1/2, down 0 | 1/2, 1/2 | 1/2 |
| E2 | as E1 | 1/2, 1/4 | 1/2 |
| E3 | as E1 | 1/2, 0 | 1/2 |
| C1 (capacity only) | as B0 | 1/2, 1/4 | 1/2 |
| R9 (slow-affect rival) | as B0 | 1/2, 1/2 | 9/10 |

"Correct" moves $k$ toward the reference (benign) reading with probability $\omega(e)$. "Reinforce" moves it toward the affect-congruent reading. A threat cue raises $k$ by one in any state. In B0 the script checks exactly that "reinforce" is an $e$-indexed choice between two $e$-independent actions, so it is a selection effect there and B0 stays nested.

## Limitations

The model is a toy with 10 states, one cue type, no action costs and hand-picked parameters. Full self-observation is declared, and partial observation can only shrink reachable sets. The two-equilibrium cases need an exact zero (down = 0 in A). The note treats that as a knife-edge, not a finding.
