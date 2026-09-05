# Executed gates — what survived, what died

The purpose of this ledger is to prevent the philosophical vocabulary from outrunning the executable result.

Every gate below is a finite / synthetic mechanism test. None is evidence that the tested system is conscious or that the operational object is identical to phenomenal experience.

| gate | attacker / question | result | status of the idea |
|---|---|---|---|
| G0 | Can raw code relabeling destroy the candidate? Does action identity matter? | raw-code cross-embodiment identity `0%`; action-bound poke identity `100%`; passive and unordered-response attackers `50%` | An action-conditioned response geometry can be coordinate-invariant in this toy, and action→response binding matters. |
| G1 | Does adding actions change the world partition while world + passive sensor stay fixed? | operational classes `1 → 2 → 4 → 8` as actions are added | The quotient is embodiment/action-repertoire relative by construction. |
| G2 | Are passive, one-step, or unordered response statistics enough? | all three attackers `50%`; ordered two-step predictive profile `100%` | Multi-step action-conditioned history can contain distinctions erased by cheaper summaries. This is predictive-state territory, not a qualia result. |
| G3 | Does efference distinguish SELF from a matched WORLD event? | sensory-only / unordered bag `50%`; bound command→consequence lag `100%`; perfect external mimic remains `50%` even with full supplied transcript | Efference can add causal attribution only when the causal stories differ operationally. Perfect mimics are an explicit stopping line. |
| G4 | Can remembered counterfactuals by themselves make an exactly aliased present state immediately identifiable? | no-memory `40` pokes; remembered relation library still `40`; ordinary stable-key lookup only `8`; stale unversioned lookup after key remap `0%` accuracy | **Negative.** Memory does not manufacture missing current evidence. |
| G5 | Can active discovery be compiled into later zero-poke perception, and is special machinery needed? | poke-labelled passive compiler `100%`, `0` test pokes after `384` calibration pokes; ordinary supervised centroid on same targets is identical; old compiler after representation remap `0%`, active poke route stays `100%` | Active identification can teach an immediate shortcut, but ordinary supervised distillation fully explains it here. |
| G6 | Can complete action-conditioned structure settle a globally inverted / permuted quality labelling? | six-state ring has **6** zero-error action-preserving cross-agent isomorphisms; actual hidden shift is only one of them; one extra external anchor collapses ambiguity to `1` map | **Stopping line.** Relational intervention geometry fixes structure, not an absolute semantic origin when nontrivial automorphisms remain. |
| G7 | Can two differently encoded agents align qualities across embodiments? What if passive geometry is a false friend? | honest passive metric + affine alignment: `100%` with zero residual; deliberately reattached but still perfectly isometric passive geometry: `0%` semantic correspondence with zero residual; transition-only leaves `6` exact maps; shared three-action consequence profile recovers `100%` true correspondence | Interventions are **not always needed**. Passive relational geometry wins when causally honest, but beautiful passive structure can be exactly wrong. |
| G8 | Is an endogenous homeostatic / body consequence intrinsically stronger than an equally informative external marker? | body effect + transitions leaves exactly `1` true map; a matched external beacon with the same pattern also leaves exactly `1` true map | **Negative on privilege.** Homeostatic consequence can break symmetry, but symmetry-breaking alone is ordinary information. |
| G9 | If BODY and BEACON are perfectly correlated, can the agent identify which one changes its future ability to act and sense? | passive/current/history attackers `50%`; decoupling interventions identify the causal driver at `100%`; BODY changes future actions, sensors and reachability while BEACON does not; exact external causal clone restores `50%` internal/external identifiability | **Positive but ordinary.** This is intervention-based system identification. |
| G10 | Does a hand-labelled SELF factor buy anything beyond generic causal abstraction? | passive shortcut fails correlation reversal; hand-labelled SELF transfers `100%`; generic no-SELF causal bottleneck also transfers `100%` after `3` calibration interventions at the same model size; external REMOTE driver is discovered just as well | **SELF loses as a computational primitive here.** The useful object is a reusable causal sufficient statistic. |
| G11 | Does causal control of future affordances define `good` and `bad`? | same dynamics: empowerment/viability choose `PRESERVE`; task reward/reversed viability choose `COLLAPSE`; utility inversion flips policy; generic planner matches all | **Hard negative on intrinsic valence from dynamics alone.** Causal structure determines consequence; an objective determines value. |
| G12 | Can a unique objective be recovered from complete optimal behavior? | BASE, potential-shaped BASE, and a distinct ALTERNATE all explain the same optimal policy; one off-policy B-vs-C preference query removes ALTERNATE, but BASE and SHAPED remain numerically different while preserving every supplied complete-path preference and optimal choice | **Hard negative on unique value origin from behavior.** Behavior constrains a reward equivalence class. Extra preference evidence can shrink it, but policy/preference-equivalent reward transformations remain. |

## The hypothesis after twelve attacks

The executable story is now:

```text
active intervention
 -> predictive / causal identity
 -> cheap learned shortcuts while stable
 -> re-grounding when shortcuts break
 -> discover variables controlling future affordances
 -> compress them into transferable causal bottlenecks
 -> plan only relative to an objective
 -> infer at most an equivalence class of objectives from behavior
```

The strongest computational claim presently earned is:

> **A bounded agent can use intervention-conditioned futures to discover transferable causal sufficient statistics for future action/sensing possibilities. Those statistics can support objective-relative planning, and behavior can provide evidence about an objective.**

The stopping lines are stronger:

```text
causal structure != semantic origin
causal role      != SELF
future affordance!= valence
behavior         != unique reward
```

> **Causal structure gives consequence; an objective gives value; behavior need not reveal a unique objective.**

Nothing so far requires privileged SELF vocabulary, intrinsic inside/outside semantics, canonical valence, or phenomenology.

## Gate 12 result — value has its own equivalence class

The decision process has one meaningful choice at `START`:

```text
A -> SA -> T
B -> SB -> T
C -> SC -> T
```

All complete paths share the same start and terminal state.

Three reward models are supplied. `BASE` ranks the paths `A > B > C`. `ALTERNATE` ranks them `A > C > B`, so it has the same optimal action but disagrees about off-policy preference. `SHAPED` is generated from BASE by

```text
r'(s,a,s') = r(s,a,s') + gamma * Phi(s') - Phi(s)
```

and changes the numerical immediate rewards substantially.

Yet all three reward models explain the complete demonstrated optimal policy: choose `A`. Behavior alone therefore leaves three candidates.

An extra preference query asks whether the agent prefers the complete B-path or C-path. The answer `B` removes ALTERNATE. That is useful evidence, but it was *new evidence*.

BASE and SHAPED survive together. Because every compared path has the same start and terminal state, the shaping terms telescope to the same constant offset. Their numerical reward tables differ, but every supplied pairwise complete-path preference and the optimal policy are identical.

So Gate 12 earns:

> **Choice can constrain value without identifying a unique numerical value function. Operationally equivalent rewards form another quotient.**

This is standard inverse-reward ambiguity, not a claim about felt valence.

There is now an interesting symmetry with G6:

```text
G6: semantic labels can vary under an operational automorphism.
G12: reward labels can vary under a policy/preference-preserving transformation.
```

In both cases the correct answer is an equivalence class unless extra evidence breaks it.

## Gate 13 preregistration — can selection masquerade as an intrinsic objective?

Another escape route is evolution:

> perhaps survival itself supplies the value function.

But population filtering can produce survival-oriented behavior without any within-agent reward representation.

Construct two mechanisms that produce the same observed mature behavior:

```text
A. EXPLICIT PLANNER
   agent evaluates viability and chooses PRESERVE

B. SELECTION ONLY
   inherited fixed controllers have no reward or learning
   some choose PRESERVE, some COLLAPSE
   environment removes the COLLAPSE lineages
   mature population therefore chooses PRESERVE
```

Mandatory tests:

- match the mature action distribution between explicit-planner and selection-only populations;
- verify selection-only individuals contain no reward/utility update machinery;
- reverse the survival mapping experimentally;
- an explicit planner with access to the new consequences should change policy immediately, while hereditary selection should initially retain its old controller distribution and change only through differential survival/reproduction;
- if only the selected mature snapshot is observed, do not infer an internal viability objective;
- no evolutionary fitness quantity is to be called felt valence.

The narrow result worth earning is:

> **Selection can make a population look as if it values viability even when no individual controller represents viability as an objective; intervention on the selection regime and temporal response can distinguish the mechanisms.**

That would fence off one more common slide: evolutionary function is not automatically within-agent value, and within-agent value is not automatically experience.

## Current philosophical boundary

The repo can investigate agent-relative distinguishability, causal anchoring, transferable causal state, self-maintaining control, objective-relative planning, and reward identifiability. It cannot infer that any of these structures feel like anything.

G6: if an automorphism preserves every available action-conditioned relation, no hidden semantic origin can be recovered.

G10: if generic causal abstraction reproduces the SELF-labelled computation, the result belongs to causal representation learning, not privileged selfhood.

G11: fixed dynamics support opposite preferences under different objectives, so preserving future options is not a canonical good.

G12: even complete optimal behavior and added preference evidence can leave numerically distinct reward functions operationally equivalent.

These are not temporary missing features. They are part of the current theory's definition.
