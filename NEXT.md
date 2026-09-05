# NEXT — from poke profile to an agent-relative quality space

Gate 0 only proves that a toy action-response fingerprint can survive raw-code relabeling and resolve passive aliasing. That is deliberately trivial.

The next gates should attack the **candidate structure**, not try to make a toy look conscious.

---

## Mathematical object

Let an agent have action repertoire `A`, observation channel `O`, history `h`, and horizon `H`.

Define an action-conditioned predictive profile

```text
Q_A(h) = {
    P(o_{t+1:t+H} | do(a_{t:t+H-1}), h)
    for action sequences from A
}
```

Define operational equivalence

```text
h ~_A h'
iff
all available action sequences induce the same future-observation distributions.
```

A natural pseudometric is

```text
d_A(h, h') = sup_over_action_sequences D(
    P(future observations | do(actions), h),
    P(future observations | do(actions), h')
)
```

for some declared divergence `D`.

`d_A = 0` means the states may be physically different but are **indistinguishable to this agent under its current embodiment**.

This is predictive-state / behavioral-equivalence mathematics. The hypothesis is only that such a geometry is a useful computational candidate for qualitative structure.

---

## Gate 1 — embodiment refines the quotient

### Question

If the external world and passive sensor are unchanged but the agent gains a new reversible action, does its operational state space become finer?

If

```text
A_small subset A_large
```

then every distinction available to `A_small` is also available to `A_large`, while the larger repertoire may expose new ones.

Therefore the equivalence relation should refine monotonically:

```text
x ~_A_large x'  =>  x ~_A_small x'
```

but not necessarily the reverse.

### Why this matters

This makes "quality space" explicitly **embodiment-relative**.

Two agents can occupy the same physical environment with the same passive sensor and still partition that world differently because one can perform interventions the other cannot.

This is a computational version of the intuition behind different sensorimotor worlds across organisms. It is not evidence that either agent experiences anything.

### Attacker

A passive hidden-state ID must not leak into the representation. If passive sensing already separates the states, the gate says nothing about action.

---

## Gate 2 — same one-step statistics, different multi-step counterfactuals

Gate 0 is too easy because single pokes expose bits directly.

Construct states with:

```text
same passive observation
same marginal response histogram
same one-step response distribution
```

but different **ordered multi-step action-conditioned futures**.

Compare:

1. passive feature model;
2. unordered response histogram;
3. one-step action-response model;
4. finite predictive-state profile;
5. oracle hidden state.

The candidate only earns something if ordered counterfactual structure adds information that the cheaper attackers genuinely lack.

---

## Gate 3 — owned poke versus matched external perturbation

Repeat the same sensory consequence in two causal stories:

```text
SELF:   I issued action a -> consequence c
WORLD:  matched external perturbation -> same consequence c
```

Without action provenance/efference, the transcript should be observationally equivalent.

With efference, the system can attribute the event to an internally privileged causal source.

This gate **must not** be sold as discovering a Self. The narrow result would be:

> efference creates causal attribution unavailable in the sensory stream alone.

This substantially overlaps existing action-perception theory and earlier `AlternativeNeuron` results. It remains here because ownership is required by the PokeAQuale candidate.

---

## Gate 4 — cached counterfactuals: active discovery becomes cheap perception

Connect to `AuditedEpistemicCache`.

First encounter:

```text
ambiguous passive state
 -> buy poke
 -> observe rebound
 -> store action/consequence claim
```

Later recurrence:

```text
cheap cue + remembered response model
 -> avoid some pokes
 -> occasionally audit
```

Measure:

```text
paid interventions
identification accuracy
stale reuse
false merge / false split
```

Attackers:

- no memory;
- ordinary lookup cache;
- learned passive classifier;
- predictive-state cache;
- proposed relational memory.

If a boring lookup does everything, call it a lookup.

---

## Gate 5 — compilation into structure

This is the important old-repo connection.

Repeatedly useful, causally confirmed distinctions should be allowed to alter a slower operator under a fixed resource budget.

Then ask whether a distinction that originally required active interrogation becomes available with fewer or no explicit probes.

Compare:

```text
A. external lookup table
B. static learned classifier
C. fast memory only
D. slow structural compilation
E. oracle
```

The hypothesis is not "plasticity creates qualia."

It is:

> repeated verified sensorimotor relations can be compiled into the machinery that makes later perception immediate.

If the static classifier is equally good and cheap, structural compilation has not earned special status.

---

## Gate 6 — the inverted-spectrum / automorphism attacker

This repo should face the philosophical symmetry problem directly.

Suppose two agents differ by a global permutation of internal quality labels, while **every action-conditioned predictive relation is preserved**.

Then this framework must say:

```text
the two systems are operationally isomorphic
under the current observation/action vocabulary.
```

It cannot discover an extra fact saying "their qualia are secretly inverted" because no such fact exists in the operational data supplied to the theory.

That is not a bug to hide. It is the theory's stopping line.

If a philosophical inverted spectrum preserves the entire causal/behavioral structure, PokeAQuale cannot settle it.

---

## Gate 7 — sensory substitution / cross-embodiment alignment

Give two agents radically different raw sensors but a learnable common structure of action-conditioned world consequences.

Ask whether their predictive geometries can be aligned without a raw coordinate map.

Attackers:

- raw feature matching;
- passive temporal matching;
- CCA / linear alignment;
- transition-only alignment;
- action-conditioned predictive alignment;
- oracle correspondence.

If a simple linear/passive alignment solves the problem, no deeper intervention geometry is needed.

---

## What success would and would not mean

A successful ladder could support:

```text
agent-relative perceptual distinctions
are naturally represented by
invariants of action-conditioned predictive structure.
```

It could also support a developmental/computational story:

```text
actively discovered counterfactual relation
 -> remembered relation
 -> audited recurrence
 -> slow compilation
 -> apparently immediate perceptual distinction
```

It would still not establish:

```text
this structure feels like something
```

The hard problem remains outside the gate ladder.

**The repo is about finding the strongest computational object that survives before that gap — and then stopping at the gap instead of naming it away.**
