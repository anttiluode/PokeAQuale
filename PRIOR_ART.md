# Prior art map — where PokeAQuale is already occupied

The first rule of this repo is that the broad idea is **not ours**.

The sentence

> qualitative character may depend on lawful relations between action and sensory consequence

lands directly inside established sensorimotor / enactive theories of perception.

The useful work here, if any, is to make one narrow version explicit enough to execute, attack and compare with boring computational controls.

---

## 1. Sensorimotor contingency theory — the closest philosophical ancestor

**J. Kevin O'Regan & Alva Noë (2001), _A sensorimotor account of vision and visual consciousness_. Behavioral and Brain Sciences 24(5):939–973.**

DOI: https://doi.org/10.1017/S0140525X01000115

This is the direct collision. They argue that seeing is a mode of active exploration and that perceptual quality depends on the structure of laws linking movement/action to sensory change — the **sensorimotor contingencies**.

This means PokeAQuale must **not** claim novelty for:

- action being constitutive of perception;
- different sensory qualities being related to different action/sensation laws;
- the idea that visual experience is temporally extended active engagement rather than a static inner picture;
- the suggestion that color quality can be understood partly through sensorimotor dependencies.

The strongest surviving distinction in this repo is computational:

> represent those contingencies explicitly as an action-conditioned predictive object, quotient states by intervention indistinguishability, then test invariance, efference binding, memory and structural compilation.

That may still turn out to be only a re-expression of old ideas.

A useful later exposition is:

**J. Kevin O'Regan (2011), _Why Red Doesn't Sound Like a Bell: Understanding the Feel of Consciousness_.**

In the color discussion, qualitative feel is again tied to the laws characterizing current sensorimotor interaction.

---

## 2. Predictive state representations — state as action-conditioned futures

**Michael L. Littman, Richard S. Sutton & Satinder Singh (2001), _Predictive Representations of State_. NeurIPS.**

Paper: https://proceedings.neurips.cc/paper/2001/file/1e4d36177d71bbb3558e43af9577d70e-Paper.pdf

Predictive-state representations describe dynamical state using multi-step **action-conditional predictions of future observations** rather than requiring an inaccessible latent-state description.

This is mathematically very close to the PokeAQuale object

```text
Q(x) = { P(future observation | action sequence, x) }
```

Therefore:

- action-conditioned prediction is not novel;
- describing hidden state by test outcomes is not novel;
- learning a sufficient predictive state from histories is not novel.

PokeAQuale asks a different question: whether that kind of predictive equivalence is a useful **candidate structure for perceptual quality** once agent-relative action, efference and invariance are included.

That philosophical identification is a hypothesis, not a theorem.

---

## 3. Bisimulation — quotienting away irrelevant implementation details

Bisimulation and related behavioral-equivalence ideas identify states when their behavior under actions is equivalent in the ways relevant to future dynamics/reward.

A modern machine-learning example is:

**Amy Zhang et al. (2021), _Learning Invariant Representations for Reinforcement Learning without Reconstruction / Deep Bisimulation for Control_. ICLR 2021.**

OpenReview: https://openreview.net/forum?id=H1lBz2VtDr

The key lesson for this repo is old and strong:

> two physically or visually different states can deserve the same representation when their action-conditioned consequences are behaviorally equivalent.

That is exactly why arbitrary raw-code relabeling is a mandatory attacker here.

PokeAQuale therefore must not advertise

```text
x ~ x' when actions cannot behaviorally distinguish them
```

as a new mathematical invention.

The candidate contribution is the **qualia-facing use of this constraint plus explicit tests of owned intervention, history and perceptual invariance**.

---

## 4. Quality spaces and structural approaches to phenomenal character

A separate literature asks whether phenomenal qualities are identified by their **relations to other possible qualities**, often represented as similarity / quality spaces.

Useful recent reviews include:

**Johannes Kleiner (2024), _Towards a structural turn in consciousness science_. Consciousness and Cognition 119:103653.**

DOI: https://doi.org/10.1016/j.concog.2024.103653

and

**Quality space computations for consciousness (2024), Trends in Cognitive Sciences.**

The common idea is that qualitative character may have relational structure rather than being exhausted by isolated intrinsic labels.

An older stronger structuralist proposal is:

**Kristjan Loorits (2014), _Structural qualia: a solution to the hard problem of consciousness_. Frontiers in Psychology 5:237.**

DOI: https://doi.org/10.3389/fpsyg.2014.00237

PokeAQuale does **not** inherit the claim that structuralism solves the hard problem.

The useful contact is narrower:

```text
ordinary quality space:
    relation among sensory qualities

PokeAQuale space:
    relation among action-conditioned predictive profiles
```

The latter is agent- and embodiment-relative by construction.

---

## 5. IIT qualia geometry — nearby vocabulary, different commitment

**Balduzzi & Tononi (2009), _Qualia: The Geometry of Integrated Information_. PLOS Computational Biology 5(8):e1000462.**

DOI: https://doi.org/10.1371/journal.pcbi.1000462

IIT uses a high-dimensional cause/effect repertoire and a geometric object in "qualia space" to characterize quality.

PokeAQuale should keep a hard distinction:

- we are **not** computing integrated information;
- we do **not** infer consciousness from causal structure;
- our object is explicitly defined relative to the actions and observations available to an agent;
- our tests are operational invariance and discriminability tests, not IIT axioms/postulates.

The overlap is that both take relational/counterfactual structure seriously.

---

## 6. Efference copy / action-based perception

Action-based perception theories emphasize that organisms use a copy of outgoing motor commands to predict self-generated sensory changes and distinguish them from external change.

A useful overview is the Stanford Encyclopedia of Philosophy entry:

https://plato.stanford.edu/entries/action-perception/

For this repo, the important computational distinction is:

```text
response after action
```

versus

```text
response known to belong to action a that I issued
```

If the action label can be discarded without changing anything, the proposed perspectival role of efference has failed.

This is why Gate 0 includes an action-response binding attacker, and later gates should separate:

- self-issued action;
- externally imposed matched perturbation;
- action known only after the fact;
- action identity removed or shuffled.

---

# What could still be worth doing

The interesting gap is **not** "nobody thought action could matter to qualia."

They did.

The useful research program is:

```text
1. define an explicit action-conditioned predictive quality object;
2. quotient away raw implementation coordinates;
3. attack it with passive representations and static latent geometry;
4. require action->response binding rather than an unordered outcome bag;
5. add memory: previous pokes alter later predictions and available distinctions;
6. add slow structural learning: repeated verified relations become cheaper / immediate;
7. test whether the resulting geometry predicts anything beyond ordinary PSR/bisimulation state estimation;
8. stop if it does not.
```

The strongest honest description today is therefore:

> **PokeAQuale is an executable meeting point between sensorimotor contingency theory, predictive-state / behavioral-equivalence mathematics, and structural quality-space ideas.**

Whether that meeting point produces anything scientifically new is an empirical question for the repo.

It does not get novelty credit merely for putting the words together.
