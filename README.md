# PokeAQuale

**Billiards of the soul.**

This repo started from a speculative question about whether an agent-relative geometry of action-conditioned consequences might be a useful computational analogue for qualitative identity.

After **19 executable gates (G0–G18)**, the result is narrower and more useful:

> **PokeAQuale is now an executable study of a bounded causal observer: how an agent can buy interventions when passive evidence is insufficient, cache causally confirmed identities, use slow history to make future inquiry cheaper, and re-ground itself when the world changes.**

It is **not** evidence of consciousness, a solution to the hard problem, or an executable bridge to subjective experience.

See [`RESULTS.md`](RESULTS.md) for the gate ledger and exact stopping lines.

## What survived

The compact architecture is:

```text
SLOW
historical cause / change statistics
   -> order probes and target audits

MEDIUM
poke-confirmed causal cache
   -> reuse expensive evidence

FAST
current intervention evidence
   -> identify / re-ground

SAFETY POLICY
maximum evidence-free interval / audit budget
   -> trade evidence cost against stale-state risk
```

The governing rule after G18 is:

> **Use history to decide where evidence is worth buying, use memory to amortize evidence already bought, and use current intervention to re-ground when necessary. Never promote a prior, cache, or safety assumption into evidence it did not observe.**

That places the repo squarely near active sensing, system identification, sequential testing, predictive-state representations, bisimulation, adaptive monitoring and cache invalidation.

## The original operational object

Passive perception gives an observation

```text
o_t = H(x_t)
```

while an intervention gives an action-conditioned consequence

```text
a_t -> x_{t+1} -> o_{t+1}.
```

Two states are operationally equivalent for a particular observer when every available intervention predicts the same relevant future observations:

```text
x ~ x'
iff
P(o_{t+tau} | do(a), x) = P(o_{t+tau} | do(a), x')
for all available a, tau.
```

That makes the observer inhabit an action-repertoire-relative quotient `X / ~` rather than requiring access to raw physical state.

The early repo treated this as a **computational qualia candidate** worth attacking. The gates did attack it. What survived is the operational / causal machinery; the stronger qualia interpretation did not earn an executable bridge.

## What the gates established

The full ledger is in [`RESULTS.md`](RESULTS.md). The later sequence is the clearest summary:

- **G14:** slow empirical priors reduce paid probe cost while fast interventions preserve correctness after distribution shift.
- **G15:** FAST + MEDIUM + SLOW compose: causal caching supplies the large amortization win; historical probe ordering trims the remaining cost; contradiction re-grounds stale keys.
- **G16:** when operator drift is silent under ordinary behavior, cache invalidation has an irreducible evidence cost.
- **G17:** a learned change hazard plus a hard maximum audit gap can improve the phase-averaged cost/staleness tradeoff, but the guarantee depends on the assumed change-rate bound.
- **G18:** violate that bound and two physically different hidden histories can produce exactly the same complete evidence transcript. The observer can recover the **current** operator at its next audit while the exact unobserved path remains non-identifiable.

The final G18 distinction is important:

```text
CURRENT IDENTITY
  can be repaired by new evidence

UNOBSERVED PATH
  cannot be reconstructed when multiple paths
  produce the same available evidence
```

## Stopping lines earned by the attacks

```text
causal structure      != semantic origin
causal role           != privileged SELF
future affordance     != intrinsic valence
behavior              != unique reward
survival selection    != represented objective
represented objective != phenomenology
unobserved history    != reconstructable fact without added evidence
```

These are not TODO items disguised as results. They are part of the current theory boundary.

## Run the experiments

The repo uses the Python standard library. Individual gates can be run directly, for example:

```bash
python experiments/gate15_three_timescale_observer.py
python experiments/gate16_silent_drift_audit_cost.py
python experiments/gate17_hazard_plus_safety_floor.py
python experiments/gate18_unknown_change_bound.py
```

GitHub Actions runs the complete G0–G18 sequence on Python 3.12.

## Lineage

This repo is downstream of several related experiments:

- [ReadWrite](https://github.com/anttiluode/ReadWrite) — intervention as an additional sense when passive states alias.
- [AlternativeNeuron](https://github.com/anttiluode/AlternativeNeuron) — active poke, medium memory, efference and coordinate-invariant dynamical objects.
- [GeometricNeuronV24](https://github.com/anttiluode/GeometricNeuronV24) — paid addressed sensing, information-gain probe selection and persistent WRITE.
- [RajoitustenHierarkia](https://github.com/anttiluode/RajoitustenHierarkia) — prediction → action/efference → consequence → residual → targeted diagnosis.
- [WidePresent](https://github.com/anttiluode/WidePresent) — ordered history can be necessary to disambiguate a current state.
- [AuditedEpistemicCache](https://github.com/anttiluode/AuditedEpistemicCache) — purchased consequences become expectations that can be reused, audited and invalidated.

See [`PRIOR_ART.md`](PRIOR_ART.md) for the repo's prior-art fence.

## Where to go next

There is deliberately no preregistered **Gate 19** merely to continue the sequence. A next branch should earn its existence by adding either a genuinely new mechanism or a real application.

The obvious engineering descendants are:

```text
active fault diagnosis
adaptive monitoring
sensor scheduling
audited caches
change detection
bounded system identification
fast / medium / slow observers
```

The consciousness question remains open outside what these programs establish.

**Billiards of the soul** remains the repo name because the originating intuition was about touching a world and receiving its rebound. The executable result is simpler: sometimes the rebound contains information you cannot get by looking, and sometimes no amount of memory can replace a rebound you never measured.
