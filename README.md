# PokeAQuale

**Billiards of the soul.**

This repo takes one narrow idea seriously enough to attack it:

> **The poke itself is probably not a quale. A better computational candidate is the agent-relative geometry of what could happen under the agent's own interventions, together with the binding that says _I issued this action and this consequence followed_.**

This is **not a claim that the code is conscious**, not a solution to the hard problem, and not a claim that sensorimotor theories of qualia are new. The broad philosophical territory is old and directly occupied. The purpose here is to turn one version of it into an executable object with invariance tests and kill conditions.

## The candidate

Passive perception gives an observation

```text
o_t = H(x_t)
```

A poke gives an action-conditioned consequence

```text
a_t -> x_{t+1} -> o_{t+1}
```

If the system also retains the efference relation

```text
I issued a_t -> this consequence followed
```

then its state can be characterized not only by what it currently sees, but by the family of futures available under its own interventions.

Define the **poke profile** of state `x` as

```text
Q(x) = { P(o_{t+tau} | do(a), x) : a in A, tau in T }
```

Two hidden states are operationally equivalent for this agent when every available intervention predicts the same future observations:

```text
x ~ x'
iff
P(o_{t+tau} | do(a), x) = P(o_{t+tau} | do(a), x')
for all available a, tau.
```

The agent therefore does not need to identify raw physical state `x`. It can inhabit the quotient

```text
X / ~
```

where states are grouped by the distinctions this particular sensing-and-action repertoire can actually make.

That quotient is the first **computational qualia candidate** in this repo.

The deliberately cautious claim is:

> If qualitative identity has a computational structure at all, an agent-relative action-conditioned predictive equivalence class is a better candidate than a raw feature code, neuron ID, frequency label, or frozen latent vector.

## Why the poke matters

Two states can be passively identical:

```text
H(x1) = H(x2)
```

and still differ under action:

```text
H(F(x1, a)) != H(F(x2, a)).
```

The action has exposed a distinction absent from the passive stream. This is the precise sense in which an actuator can become a sense organ.

The deeper point is not merely information gain. The action creates an **egocentric causal relation**:

```text
my command
   |
   v
expected consequence
   |
   v
actual consequence
   |
   v
structured difference
```

That is a plausible computational ingredient of **for-me-ness**: not a metaphysical Self, but an internally privileged causal origin around which perceptual distinctions can be organized.

## Poke Invariance Test

A serious candidate should survive arbitrary implementation relabeling.

We therefore ask two opposite questions.

### A. Different code, same counterfactual world

Give two embodiments different raw internal codes while preserving the same action-response structure.

Prediction:

```text
raw-code identity fails
poke geometry survives
```

If the candidate depends on the neuron number / latent coordinate / arbitrary symbol, kill it.

### B. Same passive appearance, different counterfactual world

Give two hidden states the same passive observation but different consequences under one or more interventions.

Prediction:

```text
passive identity fails
poke geometry separates them
```

If passive appearance alone captures everything the poke representation learns, kill the extra machinery.

## Gate 0 — executable sanity check

`experiments/gate0_poke_invariance.py` is intentionally tiny and deterministic. It checks four things:

1. **raw-code relabeling** can destroy coordinate identity while leaving poke identity exact;
2. **passive aliasing** can leave two states indistinguishable while three reversible pokes identify them exactly;
3. the pairwise **response geometry** is unchanged by arbitrary sensory-code relabeling;
4. if action identity is discarded, reciprocal response patterns collapse — binding the consequence to the issued action matters.

This is only a mechanism sanity check. It earns vocabulary, not consciousness.

Run:

```bash
python experiments/gate0_poke_invariance.py
```

## The strongest version of the thought

A quale candidate is not

```text
RED = neuron 1847
RED = latent [0.2, -0.7, ...]
RED = 37 Hz
```

but something closer to

```text
RED = its location in the agent's learned web of
      action-conditioned possible consequences,
      similarities, transitions, memories and affordances.
```

This is history dependent. Let

```text
Q_t = Q(x_t, m_t, theta_t)
```

where

- `x_t` is fast current state,
- `m_t` is medium history / expectation,
- `theta_t` is slower structure that determines which distinctions are easy, costly or even available.

Then a computational "moment" is not a frozen feature vector. It is a cross-section through:

```text
what is happening
+
what I can do to it
+
what I expect my actions to do
+
what happened before
+
which distinctions my slower structure has learned to preserve
```

Repeated active interrogation may eventually be compiled into structure. What initially required

```text
look -> poke -> compare -> poke again -> confirm
```

can later become

```text
I see it.
```

That is one possible route from active discovery to perceptual immediacy without pretending that immediacy proves phenomenology.

## Direct collision with prior art

The broad idea is **not new**. O'Regan & Noë's sensorimotor contingency theory explicitly argues that qualitative character depends on laws linking action and sensory change. Predictive-state representations describe state by action-conditional predictions. Bisimulation groups states by behaviorally relevant action-conditioned futures. Contemporary quality-space / structural approaches study phenomenal character relationally rather than as isolated labels.

So the research question here is narrower:

> **Can we build a rigorous intervention-defined quality space that is invariant to irrelevant implementation coordinates, depends on owned action-consequence binding, survives strong passive and representation attackers, and composes with memory and slow operator change?**

See [`PRIOR_ART.md`](PRIOR_ART.md).

## Lineage in these repos

This repo is downstream of several already-executed ideas rather than a fresh philosophical bolt from nowhere:

- [ReadWrite](https://github.com/anttiluode/ReadWrite) — passive ambiguity can sometimes be resolved only by a state-dependent write/intervention: actuator as sense organ.
- [AlternativeNeuron](https://github.com/anttiluode/AlternativeNeuron) — active poke, medium memory, self/world attribution, efference, coordinate-invariant dynamical objects.
- [GeometricNeuronV24](https://github.com/anttiluode/GeometricNeuronV24) — paid addressed sensing, information-gain poke selection and persistent WRITE.
- [RajoitustenHierarkia](https://github.com/anttiluode/RajoitustenHierarkia) — prediction -> action/efference -> consequence -> residual -> targeted diagnosis.
- [WidePresent](https://github.com/anttiluode/WidePresent) — ordered history can be part of current state; a frozen instant can alias moving states.
- [PresentMoment](https://github.com/anttiluode/PresentMoment) — current state can physically contain multiscale residues of previous interaction.
- [AuditedEpistemicCache](https://github.com/anttiluode/AuditedEpistemicCache) — purchased consequences become expectations that can be reused, audited and invalidated.

The progression is:

```text
passive state
   -> active distinction
   -> owned action/consequence
   -> remembered counterfactual relation
   -> coordinate-invariant predictive object
   -> slow compilation into future perceptual structure
```

## Kill conditions

This repo should become less interesting if any of these happen:

- a passive representation with equal information reproduces every claimed distinction;
- the candidate changes under arbitrary internal relabeling that preserves action-conditioned futures;
- an unordered bag of sensory consequences performs as well as correctly bound action->consequence pairs;
- simple predictive-state / bisimulation machinery already captures every useful result with no extra constraint;
- efference is unnecessary once fair controls are included;
- the proposed geometry predicts no behavioral or learning consequence beyond ordinary state estimation;
- a claimed "qualia" result is only a classifier accuracy result in fancy language.

## Stopping line

Even a perfect result here would establish, at most, a **computational structure with properties we might want from a qualia candidate**:

- perspectival anchoring,
- counterfactual depth,
- discrimination by action,
- invariance to arbitrary coordinate relabeling,
- history dependence,
- agent-relative equivalence classes.

It would **not** explain why any of that should feel like anything.

That explanatory gap stays open.

The repo is allowed to end there.

**Billiards of the soul: not because the billiard balls are conscious, but because touching the world and receiving the rebound may be part of what gives a perceptual world its agent-relative shape.**
