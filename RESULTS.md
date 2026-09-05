# Executed gates — what survived, what died

Every gate is a finite / synthetic mechanism test. None is evidence of consciousness or subjective experience.

| gate | attacker / question | result | status |
|---|---|---|---|
| G0–G13 | invariance, memory, SELF, value and selection attacks | see git history / earlier ledger | The philosophical vocabulary repeatedly shrank to ordinary operational, causal and learning mechanisms. |
| G14 | Can slow history reduce probe cost without dictating truth? | hybrid `100%` accurate at `1.3` probes pre-shift; stale prior remains correct at temporary `1.9`; prior-only falls to `10%` | **Positive.** Slow history can optimize search order; fast evidence owns truth. |
| G15 | Do FAST + MEDIUM + SLOW compose under stale passive keys? | `288` episodes: ALWAYS_ACTIVE `492` probes; FAST+MEDIUM `166`; FAST+MEDIUM+SLOW `138`, all robust routes `100%`; un-audited cache falls to `33.3%` post-shift | **Positive engineering composition.** Cache causal identities, order probes historically, re-ground on contradiction. |
| G16 | What if drift is silent under ordinary behavior? | NO_AUDIT: `280` stale episodes; periodic-16 / 20-audit ensemble mean `82.5`; learned hazard / 20 audits `52`, but skips one intermediate operator generation after hazard doubles | **Hard evidence-cost boundary.** Silent drift requires purchased evidence; hazard scheduling helps but is not a guarantee. |
| G17 | Can a hard maximum audit gap repair the learned hazard's missed-generation failure? | HAZARD_ONLY: `20` audits, `52` stale, max generation jump `2`; HAZARD+MAX_GAP16: `31` audits, `24` stale, all `11` generations detected separately, max jump `1`; periodic-10 phase ensemble near the same budget averages `31.9` audits and `49.5` stale, but a perfectly aligned periodic phase achieves `0` stale | **Positive with an explicit caveat.** A safety floor repairs the skipped-generation failure and improves the phase-averaged cost/staleness tradeoff, but a lucky periodic schedule can still beat it. The guarantee exists only because the constructed fastest change interval (`20`) exceeds the declared max audit gap (`16`). |

## After seventeen attacks

The useful architecture is now straightforward:

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

SAFETY FLOOR
maximum evidence-free interval
   -> bounds how long confidence can suppress checking
```

The principle has sharpened again:

> **Statistical expectations can optimize where evidence is purchased. A hard audit bound can limit blindness. Neither is a substitute for evidence, and the bound is only as good as the environmental assumption behind it.**

G17 uses the same silent-drift world as G16. The hidden operator changes every 40 episodes initially, then every 20. Ordinary behavior remains exactly `OK`; only a paid audit reveals operator generation.

The pure learned-hazard scheduler reproduces G16:

```text
HAZARD ONLY
  paid audits            20
  stale identity episodes 52
  detected generations    10 / 11
  maximum generation jump 2
  maximum audit gap       30
```

Adding a hard 16-episode maximum gap gives:

```text
HAZARD + MAX_GAP16
  paid audits             31
  stale identity episodes 24
  detected generations    11 / 11
  maximum generation jump 1
  maximum audit gap       16
```

So the safety constraint costs `11` extra audits and removes `28` stale episodes while repairing the skipped-generation failure.

The fair periodic attacker matters. G17 sweeps every phase offset for fixed intervals `8..16`, not one convenient cadence. Interval `10` is nearest the hybrid's audit budget:

```text
PERIODIC_10, all phase offsets
  mean audits 31.9
  mean stale  49.5
  every phase captures every generation separately
```

The hybrid therefore beats the **phase-averaged** periodic-10 schedule with slightly fewer audits (`31 < 31.9`) and roughly half the stale dwell (`24 < 49.5`). But one periodic-10 phase happens to land exactly on every hidden change and gets `0` stale episodes. That attacker stays in the result deliberately: this toy does not establish universal optimality.

The earned result is only:

> **A learned hazard and a hard evidence-frequency floor can complement each other: the prior improves where audits are spent, while the floor prevents long confidence-induced blind intervals.**

The guarantee is conditional. Here `MAX_GAP=16` is shorter than the world's fastest hidden change interval `20`. That assumption is doing real work.

## Gate 18 preregistration — attack the assumed safety bound

The obvious loophole is now the bound itself.

Inject an adversarial burst in which two or more silent operator changes occur inside one allowed 16-episode audit gap. Keep the ordinary observation identical. Compare:

```text
1. FIXED MAX-GAP16
2. HAZARD + MAX-GAP16
3. ESCALATING AUDITOR
   if an audit reveals generation jump > 1,
   temporarily shorten its maximum gap
4. AUDIT EVERY EPISODE
5. ORACLE
```

Mandatory distinctions:

- **current identity recovery**: after the next audit, can the observer become correct about the present operator?
- **event reconstruction**: can it know how many unseen intermediate generations occurred?

Kill / stopping conditions:

- no method may reconstruct an unobserved intermediate operator trajectory when multiple trajectories produce the same two audited endpoints;
- a fixed audit bound cannot guarantee complete event capture if the world may change faster than that bound;
- an adaptive auditor may reduce *future* misses after discovering a jump, but it cannot retroactively recover information never observed;
- if retrospective side information is added, count it as new evidence rather than memory magic.

The narrow target is:

> **Evidence-frequency guarantees require a justified bound on hidden change rate. Violate that bound and an observer may recover the current state at its next audit while permanently losing the exact path taken between audits.**

That is likely the natural stopping point for this audit thread.

## Current stopping lines

```text
causal structure      != semantic origin
causal role           != privileged SELF
future affordance     != valence
behavior              != unique reward
survival selection    != represented objective
represented objective != phenomenology
unobserved history    != reconstructable fact without additional evidence
```
