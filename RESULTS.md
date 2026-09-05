# Executed gates — what survived, what died

Every gate is a finite / synthetic mechanism test. None is evidence of consciousness or subjective experience.

| gate | attacker / question | result | status |
|---|---|---|---|
| G0–G13 | invariance, memory, SELF, value and selection attacks | see git history / earlier ledger | The philosophical vocabulary repeatedly shrank to ordinary operational, causal and learning mechanisms. |
| G14 | Can slow history reduce probe cost without dictating truth? | hybrid `100%` accurate at `1.3` probes pre-shift; stale prior remains correct at temporary `1.9`; prior-only falls to `10%` | **Positive.** Slow history can optimize search order; fast evidence owns truth. |
| G15 | Do FAST + MEDIUM + SLOW compose under stale passive keys? | `288` episodes: ALWAYS_ACTIVE `492` probes; FAST+MEDIUM `166`; FAST+MEDIUM+SLOW `138`, all robust routes `100%`; un-audited cache falls to `33.3%` post-shift | **Positive engineering composition.** Cache causal identities, order probes historically, re-ground on contradiction. |
| G16 | What if drift is silent under ordinary behavior? | NO_AUDIT: `280` stale episodes; periodic-16 / 20-audit ensemble mean `82.5`; learned hazard / 20 audits `52`, but skips one intermediate generation after hazard doubles | **Hard evidence-cost boundary.** Silent drift requires purchased evidence; hazard scheduling helps but is not a guarantee. |
| G17 | Can a hard maximum audit gap repair the learned hazard's missed-generation failure? | HAZARD_ONLY: `20` audits, `52` stale, max jump `2`; HAZARD+MAX_GAP16: `31` audits, `24` stale, all `11` generations captured, max jump `1`; periodic-10 near-budget phase ensemble averages `31.9` audits / `49.5` stale, but a perfectly aligned phase gets `0` stale | **Positive with a conditional guarantee.** The safety floor works because the world's fastest change interval (`20`) exceeds the audit bound (`16`). |
| G18 | What if the world changes more than once inside the declared audit bound? | actual hidden burst `C→A` at `t=100`, `A→B` at `106`; alternate world has only direct `C→B` at `106`. FIXED16 and the tested escalating observer receive **identical complete audit transcripts in both worlds**. FIXED16: `10` audits, `50` stale episodes, `4` endpoint-change detections. ESCALATING: `22` audits, `20` stale, `6` endpoint detections. Both recover current `B` at `t=112`; neither can identify whether intermediate `A` occurred. | **Stopping line.** Faster auditing after a surprise improves future tracking but cannot reconstruct unobserved history. A maximum audit gap guarantees event capture only if a valid upper bound on hidden change rate is supplied. |

## Where the project landed

The useful architecture is now:

```text
SLOW
historical cause / change statistics
   -> order probes and target audits

MEDIUM
poke-confirmed causal cache
   -> reuse expensive evidence

FAST
current paid evidence
   -> identify / re-ground

SAFETY POLICY
maximum evidence-free interval / audit budget
   -> trades cost against stale-state risk
```

The surviving design rule is:

> **Use history to decide where evidence is worth buying, use memory to amortize evidence already bought, and use current intervention to re-ground when necessary. Never promote a prior, cache, or safety assumption into evidence it did not observe.**

That is a bounded causal observer. It is ordinary system identification, active diagnosis, caching, change detection and sequential decision machinery composed under explicit observation costs.

## Gate 18 — current state can be recovered while the path is lost

G17 looked reassuring because `MAX_GAP=16` was shorter than the world's fastest hidden change interval `20`. G18 violates that assumption deliberately.

The normal channel remains completely silent:

```text
ordinary observation = OK
```

for every hidden operator state.

The bounded observer audits at:

```text
... 80, 96, 112, 128 ...
```

but the actual world does this inside one gap:

```text
t=96 audit: C

t=100: C -> A
t=106: A -> B

t=112 audit: B
```

Now construct a second world:

```text
t=96 audit: C

t=106: C -> B

t=112 audit: B
```

The worlds differ physically: in one, state `A` exists from `t=100..105`; in the other it never occurs. Yet every ordinary observation and every audit taken by FIXED16 is identical.

The escalating observer does not help retroactively. Its first evidence of any change arrives at `t=112`, so its complete transcript is also identical in the two worlds. It then shortens its future gap from `16` to `4`, reducing stale current-state time from `50` to `20` episodes over the full run and increasing endpoint detections from `4` to `6`. That is useful adaptation. But the missing `A` episode has already disappeared behind the observation boundary.

So two questions must stay separate:

```text
CURRENT IDENTITY
  What operator is active now?
  -> can be repaired at the next informative audit.

HIDDEN PATH
  Exactly what happened between the last two audits?
  -> not identifiable when distinct paths induce the same evidence transcript.
```

The oracle and audit-every baselines confirm the obvious cost side: auditing every episode uses `175` paid audits and leaves zero stale dwell; an oracle that knows the seven actual change times uses seven audits and also leaves zero stale dwell. Neither is available to a bounded observer for free.

The Gate 18 result is therefore not an algorithm win. It is a boundary:

> **Evidence-frequency guarantees require assumptions about how fast the hidden world can change. If those assumptions fail, later evidence can restore the present without restoring an unobserved past.**

This closes the audit / cache-invalidation thread cleanly.

## What survived from the original PokeAQuale idea

```text
passive state can alias cause
intervention can expose causal distinctions
ordered action-conditioned futures can define operational identity
stable causal identities can be compiled into cheaper predictors
cached identities need re-grounding under drift
slow history can reduce evidence cost
silent drift requires explicit auditing
safety bounds only work under stated environmental assumptions
exact operational equivalence remains a stopping line
```

What did not survive as earned claims:

```text
operational identity -> quale
causal bottleneck    -> privileged SELF
homeostasis          -> intrinsic valence
survival             -> represented objective
behavior             -> unique reward
fitness / reward     -> felt experience
```

And G18 adds a general epistemic stopping line:

```text
unobserved history != reconstructable fact without additional evidence
```

## Current status

There is no need for Gate 19 just to make the number larger. G0–G18 have already turned the original speculative question into a useful, falsifiable architecture and mapped several places where the inference must stop.

A future branch should only reopen the gate sequence for a genuinely new mechanism or a real-data application. The natural engineering descendants are active diagnosis, adaptive monitoring, audited caches, bounded system identification and multiscale observers.

The consciousness question remains open outside what this executable repo has established.
