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
| G14 | Can slow history reduce probe cost without making the prior dictate truth? | hybrid `100%` accurate at `1.3` probes pre-shift; stale prior stays correct at temporary `1.9` probes; fixed-prior accuracy falls to `10%` | **Positive.** Slow history can compile search order; fast evidence owns truth. |
| G15 | Do FAST + MEDIUM + SLOW compose under a stale passive key? | `288` episodes: ALWAYS_ACTIVE `492` probes; FAST+MEDIUM `166`; FAST+MEDIUM+SLOW `138`, all robust routes `100%`; full system detects remap on first post-shift episode; cache without invalidation falls to `33.3%` post-shift | **Positive engineering composition.** Medium memory amortizes identification, slow history trims the residual cost, fast contradiction re-grounds stale keys. |
| G16 | What if operator drift is completely silent under ordinary behavior? | NO_AUDIT: `0` detections and `280` stale episodes; AUDIT_EVERY_EPISODE: `319` audits and `0` stale; 16-step periodic schedules with equal `20`-audit budgets average `82.5` stale episodes (best `56`, worst `109`); SLOW_HAZARD also spends `20` audits and has `52` stale episodes, but after the true hazard doubles it skips one intermediate operator generation (`max jump = 2`) | **Hard evidence-cost boundary + partial scheduling win.** Silent drift is not detectable for free. Learned hazard improves audit economics while its timing statistics hold, but loses its guarantee after hazard shift and can miss a change event. |

## After sixteen attacks

The computational architecture has become clearer precisely because the philosophical shortcuts keep failing:

```text
SLOW
history of causes / change statistics
   -> choose probe order and audit timing

MEDIUM
poke-confirmed context -> causal identity
   -> cheap reusable prediction

FAST
current evidence
   -> active identification / re-grounding
```

The discipline is now stronger than after G15:

> **Slow history may schedule evidence. Medium memory may reuse evidence. Neither may invent evidence.**

G16 removes G15's convenient free cache audit. The ordinary control consequence is exactly the same string, `OK`, under every hidden operator generation. The only operation that contains information about the current generation is an explicit paid audit.

That creates a hard stopping line:

```text
normal consequence under operator A = OK
normal consequence under operator B = OK

no audit
  -> no observation differs
  -> no change detector has evidence
```

The deterministic receipt is:

```text
320 episodes
11 hidden operator changes
normal observation identical across all generations

NO_AUDIT
  paid audits: 0
  detected changes: 0
  stale hidden-identity episodes: 280

AUDIT_EVERY_EPISODE
  paid audits: 319
  stale episodes: 0

ORACLE_CHANGE_POINT
  paid audits: 11
  stale episodes: 0
  (benchmark only: knows the hidden change times)

PERIODIC_16
  every phase offset evaluated
  each schedule forced to the same 20-audit budget
  mean stale episodes: 82.5
  best offset: 56
  worst offset: 109
  every operator generation separately observed

SLOW_HAZARD
  paid audits: 20
  stale episodes: 52
  stale before hazard-rate change: 0
  stale after hazard-rate change: 52
  detected audit events: 10
  one audit jumps generation 6 -> 8
```

The slow scheduler starts with a previously learned 40-episode change interval. While that remains true, it places audits near the expected boundary and gets **zero stale dwell**. A fair 16-step periodic schedule with unknown phase averages `30` stale episodes over the same early regime.

Then the environment changes from a 40-episode to a 20-episode change interval. The slow scheduler has no magical way to know that. Its post-shift stale dwell becomes `52`, almost exactly the periodic ensemble's `52.5` average. Worse, one pair of operator changes occurs between audits, so the observer updates directly from generation 6 to generation 8 and never separately observes generation 7.

That is an important negative result. Lower stale dwell is not the same thing as complete change-event capture.

So G16 earns two statements at once:

> **When drift is silent under normal behavior, cache invalidation has an irreducible evidence cost.**

and

> **A learned hazard can allocate a fixed audit budget better in a familiar regime, but it is a prior over change timing, not a guarantee.**

This is ordinary inspection scheduling / change detection. That is the correct description.

## What survived from the original PokeAQuale idea

```text
passive state can alias cause
intervention can reveal cause
stable causal identity can be cached
cached identity can become stale
contradiction can re-ground it when contradiction is observable
silent drift requires paid audit
slow history can reduce evidence cost but cannot abolish it
exact operational equivalence remains a stopping line
```

What still has not been earned:

```text
operational identity -> quale
causal bottleneck    -> SELF
homeostasis          -> intrinsic valence
survival             -> represented objective
behavior             -> unique reward
fitness / reward     -> felt experience
```

## Gate 17 preregistration — combine learned hazard with a hard audit safety bound

G16 reveals a concrete engineering defect in the pure slow-hazard scheduler: it minimizes stale dwell well, but after the hazard changes it leaves a long enough audit gap to skip an entire intermediate operator generation.

The next test should ask whether the natural composition is:

```text
SLOW statistical hazard
  -> spend audits where changes are expected

PLUS

HARD maximum audit gap
  -> never let historical confidence suppress evidence forever
```

Compare on the same silent-drift world:

```text
1. HAZARD ONLY
   cheap, adaptive, can miss events

2. PERIODIC ONLY
   phase-blind safety cadence

3. HAZARD + MAX-GAP SAFETY FLOOR
   historical targeting, but no audit gap may exceed a fixed bound

4. AUDIT EVERY EPISODE
   expensive ceiling

5. ORACLE
   benchmark only
```

Required measurements:

- paid audits;
- stale hidden-identity episodes;
- number of operator generations separately observed;
- maximum generation jump at detection;
- maximum audit gap;
- pre/post hazard-shift performance;
- Pareto comparison against periodic schedules with similar audit budgets.

Kill conditions:

- if the hybrid still skips generations despite a gap shorter than the minimum change interval, the implementation is wrong;
- if a periodic schedule at comparable audit cost matches both stale dwell and event capture, the learned hazard adds nothing;
- if the safety floor consumes so many audits that historical scheduling no longer matters, the composition is ornamental;
- there is still no free guarantee against changes faster than the enforced audit bound.

The narrow target is:

> **Statistical expectations can optimize where evidence is purchased, while a hard evidence budget bound prevents confidence from becoming permanent blindness.**

That is a useful bounded-observer design principle independent of the original qualia framing.

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
