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
| G14 | Can slow history reduce probe cost without making the prior dictate truth? | pre-shift: hybrid `100%` accuracy at `1.3` probes vs uniform active `1.667`; stale prior immediately after shift stays `100%` accurate but costs `1.9` probes while fixed-prior-only accuracy falls to `10%`; after slow update hybrid returns to `1.3`, matching oracle order | **Positive.** Slow history can compile search order; fast interventions preserve correctness under shift. |
| G15 | Do FAST + MEDIUM + SLOW actually compose under a stale passive key? | over `288` episodes: ALWAYS_ACTIVE `492` probes; FAST+MEDIUM `166`; FAST+MEDIUM+SLOW `138`, all robust routes `100%` accurate; full system detects remap on first post-shift episode and invalidates `2` hot stale cache entries; CACHE_NO_INVALIDATION falls to `33.3%` accuracy in the first and last post-shift cycles; PRIOR_ONLY falls from `87.5%` pre-shift to `4.17%` post-shift | **Positive engineering composition.** Medium audited caching amortizes repeated identification; slow history cuts the remaining probe bill by `28` probes (`16.9%`) at equal perfect accuracy; fast contradiction-triggered probing prevents stale cache hits from becoming final errors. |

## After fifteen attacks

The project has converged on a bounded causal observer:

```text
SLOW
historical frequencies / hazard estimates
   -> choose which expensive question is worth asking first

MEDIUM
poke-confirmed context -> causal identity
   -> cheap reusable prediction

FAST
current consequence / contradiction
   -> active re-grounding when the cheap route fails
```

The crucial discipline is now:

> **Slow history may choose search economics. Medium memory may cache an answer. Current evidence still owns truth.**

G15 makes the three layers coexist in one deterministic toy instead of testing them pairwise.

The world has ten persistent context keys and a four-slot LRU cache. Two contexts are hot and recur constantly; the others create cold misses. During a long stable epoch, context predicts the causal driver. Then the operator remaps while the passive context names stay exactly the same.

The full observer behaves like this:

```text
cache hit
  -> try cached causal identity
  -> ordinary task consequence agrees
       -> zero extra diagnostic probes

cache hit
  -> ordinary consequence contradicts expectation
       -> invalidate stale entry
       -> FAST probes remaining hypotheses
       -> rewrite MEDIUM cache

cache miss
  -> SLOW orders candidate probes
  -> FAST identifies current cause
  -> MEDIUM stores it
```

That yields the deterministic receipt:

```text
288 total episodes

ALWAYS_ACTIVE
  accuracy: 100%
  paid diagnostic probes: 492

FAST + MEDIUM
  accuracy: 100%
  paid diagnostic probes: 166

FAST + MEDIUM + SLOW
  accuracy: 100%
  paid diagnostic probes: 138
  saving vs FAST+MEDIUM: 28 probes = 16.9%
  first drift invalidation: first post-shift episode
  stale hot entries repaired: 2

CACHE_NO_INVALIDATION
  post-shift first-cycle accuracy: 33.3%
  post-shift last-cycle accuracy: 33.3%
  wrong final answers in each 24-episode post cycle: 16

PRIOR_ONLY
  pre-shift accuracy: 87.5%
  post-shift accuracy: 4.17%
```

In the final post-shift steady cycle, the probe bill is:

```text
ALWAYS_ACTIVE          42 / 24 episodes
FAST + MEDIUM          12 / 24
FAST + MEDIUM + SLOW   11 / 24
```

So MEDIUM supplies the large amortization win and SLOW supplies a smaller but real optimization at equal perfect final causal accuracy.

The full mechanism is ordinary adaptive diagnosis, audited caching and sequential search. That is the correct description.

## What survived from the original PokeAQuale idea

```text
1. passive representations can alias or mislead;
2. intervention can expose hidden causal distinctions;
3. action-conditioned futures give an operational identity;
4. stable identities can be compiled into cheaper predictors;
5. compiled predictors require evidence-based invalidation under drift;
6. slow statistics can optimize probe order without becoming truth;
7. fast intervention can re-ground a stale representation;
8. exact operational equivalence remains a stopping line.
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

The repo is now substantially more useful as architecture and substantially weaker as a consciousness theory. That is the direction the tests forced.

## Gate 16 preregistration — remove the free audit signal

G15 contains an important convenience that must be attacked immediately: the ordinary task consequence tells the observer when its cached causal prediction is wrong.

That means stale cache entries are **audited for free by normal behavior**.

Real systems are not always that kind. An operator can drift while the currently chosen action continues to produce the same immediate observation. The hidden causal identity may have changed even though the cheap control loop looks normal.

Gate 16 should therefore construct **silent drift**:

```text
before shift:
  cached identity A
  ordinary action -> immediate consequence OK

after shift:
  hidden causal identity B
  same ordinary action -> same immediate consequence OK

only an explicit audit / alternative intervention
reveals A != B
```

Attackers:

```text
NO AUDIT
  trust the cache while ordinary behavior looks normal

AUDIT EVERY EPISODE
  guaranteed rapid detection, maximal diagnostic cost

PERIODIC AUDIT
  fixed audit interval

SLOW-HAZARD AUDIT + FAST RE-GROUNDING
  historical change rate determines audit frequency;
  a positive audit triggers full active identification

ORACLE CHANGE POINT
  benchmark only
```

Required measurements:

- paid audits / probes;
- stale-cache dwell time after silent remap;
- number of episodes carrying the wrong hidden causal identity before detection;
- first-detection latency;
- cumulative diagnostic cost;
- cost-vs-staleness frontier;
- performance when the true drift hazard changes.

Kill / stopping conditions:

- if `NO AUDIT` detects a truly silent remap, the setup leaked change information;
- no non-oracle method may claim guaranteed immediate detection without paying for evidence;
- if slow hazard estimates do not beat a fair periodic schedule on the cost/staleness tradeoff, the slow audit scheduler is ornamental;
- if two operators are identical under every available normal consequence and every available audit, they are operationally equivalent and the test must stop there.

The narrow target is:

> **Cache invalidation has an irreducible evidence cost when drift is silent under normal behavior; learned change statistics may reduce that cost by scheduling audits, but cannot eliminate the identifiability boundary.**

This would close a loophole in G15 rather than merely adding another feature.

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
