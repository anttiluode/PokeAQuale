# Executed gates — what survived, what died

The purpose of this ledger is to prevent the philosophical vocabulary from outrunning the executable result. Every gate is a finite / synthetic mechanism test. None is evidence of consciousness or subjective experience.

| gate | attacker / question | result | status |
|---|---|---|---|
| G0 | Does raw-code relabeling destroy identity? | raw code `0%`; action-bound poke identity `100%` | Action-conditioned response geometry can be coordinate-invariant. |
| G1 | Does action repertoire change operational state? | classes `1 → 2 → 4 → 8` | Operational quotient is embodiment-relative. |
| G2 | Are passive / one-step / unordered summaries enough? | all `50%`; ordered two-step profile `100%` | Temporal counterfactual structure matters. |
| G3 | Does efference create a SELF distinction? | bound lag `100%`; perfect external mimic still `50%` | Causal attribution only when causal stories differ. |
| G4 | Can memory manufacture missing present evidence? | relation memory still needs `40` pokes; stable key lookup needs `8` | **No.** Memory needs a current handle. |
| G5 | Can active discovery become zero-poke recognition? | compiled route `100%`; ordinary supervised learner identical | Useful distillation, no special machinery. |
| G6 | Can relational structure settle an inverted spectrum? | `6` exact isomorphisms; external anchor reduces to `1` | **Stopping line.** No absolute semantic origin from preserved relations. |
| G7 | Can passive geometry align embodiments? | honest geometry `100%`; exact false-friend geometry `0%` causal correspondence | Geometry can align or confidently mislead. |
| G8 | Is homeostasis privileged over matched external information? | BODY and BEACON break symmetry equally | **No privilege from naming/location.** |
| G9 | Which correlated variable changes future affordances? | passive `50%`; decoupling intervention `100%`; external causal clone restores location ambiguity | Standard causal identification. |
| G10 | Does labelled SELF beat generic causal abstraction? | both `100%`; generic model pays `3` interventions and finds same bottleneck | **SELF adds no computational primitive here.** |
| G11 | Does affordance preservation define good/bad? | same dynamics support opposite policies under different objectives | **No canonical valence from causal structure.** |
| G12 | Can behavior reveal unique reward? | policy + preference evidence still leaves BASE and shaped BASE equivalent | **Reward is identified only up to an equivalence class.** |
| G13 | Can selection look like within-agent preference? | equilibrium snapshot identical; survival-map reversal reveals immediate planner adaptation vs one-generation selection lag | **Yes.** Fitness filtering is not a represented objective. |
| G14 | Can slow history reduce probe cost without making the prior dictate truth? | pre-shift: hybrid `100%` accuracy at `1.3` probes vs uniform active `1.667`; stale prior immediately after shift stays `100%` accurate but costs `1.9` probes while fixed-prior-only accuracy falls to `10%`; after slow update hybrid returns to `1.3`, matching oracle order | **Positive.** Slow history can compile search order; fast interventions preserve correctness under shift. Ordinary sequential testing explains the mechanism. |

## After fourteen attacks

The project has converged on a computational architecture considerably more defensible than the original qualia language:

```text
slow history
   -> prior / probe ordering

medium stable representation
   -> cheap prediction / cache

fast current interaction
   -> intervene when needed
   -> identify current causal state
   -> override stale prior or cache
```

The important principle is:

> **The prior may choose which question is cheap to ask first. Evidence still chooses the answer.**

G14 makes that concrete. Before the distribution shift, a historical prior `V1 > V0 > V2` reduces expected intervention cost from the uniform active searcher's `5/3 ≈ 1.667` probes to `1.3`, with perfect identification. When the world abruptly becomes V2-dominant, the stale hybrid remains perfectly correct because contradiction triggers further probing; it merely becomes temporarily more expensive at `1.9` probes. A prior-only guesser costs nothing but collapses to `10%` accuracy. Updating the slow prior to the new distribution restores the hybrid to `1.3` probes, equal to the oracle ordering.

So the useful result is not mysterious:

> **Slow experience can compile an intervention policy that makes recurrent causal identification cheaper, while fast counterfactual testing preserves adaptability when the world changes.**

This is sequential testing / active diagnosis. That mundane description is a strength, because it connects directly to the bounded-observer line elsewhere in the repos.

## What survived from the original PokeAQuale idea

A fairly coherent core survived the attacks:

```text
1. passive representations can alias or mislead;
2. intervention can expose hidden causal distinctions;
3. action-conditioned futures give an operational identity;
4. stable identities can be compiled into cheaper predictors;
5. those predictors need invalidation / re-grounding under drift;
6. slow statistics can optimize the order and cost of future interventions;
7. exact operational equivalence remains a stopping line.
```

What did **not** survive as earned claims:

```text
operational identity -> quale
causal bottleneck    -> SELF
homeostasis          -> intrinsic valence
survival             -> represented objective
behavior             -> unique reward
fitness / reward     -> felt experience
```

The repo has therefore become more useful while becoming less of a consciousness theory.

## Gate 15 preregistration — put the three timescales in one observer

G14 tests only the slow-prior / fast-probe pair. Gate 15 should combine the pieces into one end-to-end bounded observer and see whether they actually compose.

World:

```text
persistent epochs
  -> passive context usually predicts the causal driver
  -> occasional abrupt remap / operator shift
  -> same passive key can become stale
```

Observer:

```text
FAST
  active causal probes when uncertainty / prediction error is high

MEDIUM
  cache passive-context -> poke-confirmed causal identity

SLOW
  empirical prior over likely drivers / useful probe order
```

Attackers:

```text
ALWAYS ACTIVE
  robust, expensive

CACHE ONLY
  cheap, catastrophically stale after remap

PRIOR ONLY
  cheapest, guesses dominant cause

FAST + MEDIUM
  learns shortcuts but has no optimized probe ordering

FAST + MEDIUM + SLOW
  full three-timescale observer
```

Required measurements:

- causal-identification accuracy;
- interventions per episode;
- errors in the first episodes after remap;
- time / probes to detect drift;
- cache invalidations;
- steady-state cost;
- cumulative cost over long stable epochs plus shifts.

Kill conditions:

- if `FAST + MEDIUM + SLOW` does not beat `FAST + MEDIUM` in cumulative probe cost at equal accuracy, the slow layer is ornamental;
- if it cannot beat `ALWAYS ACTIVE` over stable epochs, compilation is useless;
- if stale cache causes unobserved wrong answers, uncertainty/change detection is inadequate;
- if a standard adaptive diagnosis/cache-invalidation account explains the whole result, that is the correct description.

The narrow target is:

> **A bounded observer can amortize expensive causal identification across recurrent experience without surrendering the ability to re-ground itself after its cheap representation becomes stale.**

That is an engineering claim worth keeping even if the repo is eventually renamed.

## Current stopping lines

```text
causal structure      != semantic origin
causal role           != privileged SELF
future affordance     != valence
behavior              != unique reward
survival selection    != represented objective
represented objective != phenomenology
```

PokeAQuale can study the machinery on the left. It currently has no executable bridge across the final `!=` signs.
