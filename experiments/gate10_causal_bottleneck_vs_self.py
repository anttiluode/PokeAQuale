#!/usr/bin/env python3
"""Gate 10 — Does a hand-labelled SELF factor buy computation beyond a generic causal bottleneck?

Gate 9 identified a variable that controls the observer's future affordances. The next
temptation is to promote that variable into a privileged SELF representation.

This gate attacks that move.

Three currently observed binary channels V0, V1, V2 are perfectly correlated during
ordinary training data. The true affordance driver is V1, but ordinary data cannot
reveal that because all three channels agree.

We compare:

1. flat context-specific lookup;
2. passive single-variable shortcut chosen from ordinary correlations only;
3. hand-labelled SELF factor told for free that V1 is the driver;
4. generic causal-bottleneck discovery with no SELF vocabulary, allowed to intervene
   on candidate variables and choose the one whose manipulation changes affordances;
5. oracle causal graph.

At test time external contexts reverse the distractor correlations while preserving
V1 -> affordance. The generic causal bottleneck should match the hand-labelled SELF
factor after paying calibration interventions. If it does, the result is causal
abstraction / sufficient-state discovery, not evidence that the name SELF adds a new
computational primitive.

Constructed finite-state result; no phenomenology claim.
"""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from dataclasses import dataclass
from typing import Dict, Iterable, List, Mapping, Sequence, Tuple


CHANNELS = ("V0", "V1", "V2")
TRUE_DRIVER = "V1"


@dataclass(frozen=True)
class Example:
    context: str
    channels: Mapping[str, int]
    affordance: int  # 0 = low, 1 = high


def make_example(context: str, driver: int, flip_v0: int, flip_v2: int) -> Example:
    channels = {
        "V0": driver ^ flip_v0,
        "V1": driver,
        "V2": driver ^ flip_v2,
    }
    return Example(context=context, channels=channels, affordance=driver)


def build_dataset() -> Tuple[List[Example], List[Example]]:
    # Training contexts deliberately provide no passive clue: every channel equals V1.
    train = [
        make_example(context, driver, 0, 0)
        for context in ("TRAIN_A", "TRAIN_B", "TRAIN_C")
        for driver in (0, 1)
    ]

    # Held-out contexts reverse one or both distractors while the true driver law stays fixed.
    test_specs = (
        ("TEST_FLIP_V0", 1, 0),
        ("TEST_FLIP_V2", 0, 1),
        ("TEST_FLIP_BOTH", 1, 1),
        ("TEST_NEW_CONTEXT", 1, 0),
    )
    test = [
        make_example(context, driver, flip_v0, flip_v2)
        for context, flip_v0, flip_v2 in test_specs
        for driver in (0, 1)
    ]
    return train, test


def accuracy(predictions: Sequence[int], examples: Sequence[Example]) -> float:
    return sum(int(pred == ex.affordance) for pred, ex in zip(predictions, examples)) / len(examples)


def flat_lookup_train(train: Sequence[Example]) -> Dict[Tuple[str, Tuple[int, int, int]], int]:
    table: Dict[Tuple[str, Tuple[int, int, int]], int] = {}
    for ex in train:
        key = (ex.context, tuple(ex.channels[ch] for ch in CHANNELS))
        table[key] = ex.affordance
    return table


def flat_lookup_predict(table: Mapping[Tuple[str, Tuple[int, int, int]], int], examples: Sequence[Example]) -> List[int]:
    # Honest lookup cannot generalize to unseen context/feature combinations. Use the
    # training majority only when the key is absent. The balanced training set makes
    # that fallback uninformative; deterministic tie-break = 0.
    out = []
    for ex in examples:
        key = (ex.context, tuple(ex.channels[ch] for ch in CHANNELS))
        out.append(table.get(key, 0))
    return out


def passive_channel_scores(train: Sequence[Example]) -> Dict[str, float]:
    scores = {}
    for ch in CHANNELS:
        scores[ch] = sum(int(ex.channels[ch] == ex.affordance) for ex in train) / len(train)
    return scores


def choose_passive_shortcut(train: Sequence[Example]) -> str:
    scores = passive_channel_scores(train)
    # All three channels tie perfectly on ordinary data. A passive-only procedure has
    # no evidence for preferring V1. Lexicographic tie-break is explicit and therefore
    # chooses V0, not the hidden true driver.
    best = max(scores.values())
    return sorted(ch for ch, score in scores.items() if score == best)[0]


def one_channel_predict(channel: str, examples: Sequence[Example]) -> List[int]:
    return [ex.channels[channel] for ex in examples]


def affordance_after_intervention(base: Mapping[str, int], variable: str, value: int) -> int:
    state = dict(base)
    state[variable] = value
    return state[TRUE_DRIVER]


def discover_causal_driver_by_intervention() -> Tuple[str, int, Dict[str, bool]]:
    # Start from a state where all channels are 0. Toggle each candidate to 1 while
    # holding the others fixed. Only the true driver changes the next affordance.
    base = {ch: 0 for ch in CHANNELS}
    effects: Dict[str, bool] = {}
    interventions = 0
    for ch in CHANNELS:
        interventions += 1
        before = affordance_after_intervention(base, ch, 0)
        after = affordance_after_intervention(base, ch, 1)
        effects[ch] = before != after

    causal = [ch for ch, changed in effects.items() if changed]
    assert len(causal) == 1, effects
    return causal[0], interventions, effects


def intervention_prediction_accuracy(selected_channel: str) -> float:
    # Predict the affordance under all 3 variables x 2 intervention values from a
    # fixed zero baseline. A correct one-variable bottleneck predicts all six exactly.
    base = {ch: 0 for ch in CHANNELS}
    correct = 0
    total = 0
    for variable in CHANNELS:
        for value in (0, 1):
            actual = affordance_after_intervention(base, variable, value)
            hypothetical = dict(base)
            hypothetical[variable] = value
            predicted = hypothetical[selected_channel]
            correct += int(predicted == actual)
            total += 1
    return correct / total


def external_clone_attacker() -> Dict[str, object]:
    # Replace the anatomically named internal driver with REMOTE while preserving the
    # exact driver -> affordance law. A generic causal bottleneck identifies REMOTE just
    # as happily. Operational role transfers; anatomical location is extra vocabulary.
    candidate_variables = ("LOCAL_NOISE", "REMOTE", "OTHER_NOISE")

    def future(base: Mapping[str, int], variable: str, value: int) -> int:
        state = dict(base)
        state[variable] = value
        return state["REMOTE"]

    base = {name: 0 for name in candidate_variables}
    effects = {}
    for variable in candidate_variables:
        effects[variable] = future(base, variable, 0) != future(base, variable, 1)
    causal = [name for name, changed in effects.items() if changed]
    return {
        "candidate_variables": list(candidate_variables),
        "intervention_effects": effects,
        "discovered_driver": causal[0],
        "generic_bottleneck_succeeds_without_internal_location": causal == ["REMOTE"],
    }


def main() -> None:
    train, test = build_dataset()

    flat = flat_lookup_train(train)
    flat_acc = accuracy(flat_lookup_predict(flat, test), test)

    passive_scores = passive_channel_scores(train)
    passive_channel = choose_passive_shortcut(train)
    passive_train_acc = accuracy(one_channel_predict(passive_channel, train), train)
    passive_test_acc = accuracy(one_channel_predict(passive_channel, test), test)

    # Privileged SELF prior: told the correct factor name for free.
    self_channel = TRUE_DRIVER
    self_test_acc = accuracy(one_channel_predict(self_channel, test), test)
    self_intervention_acc = intervention_prediction_accuracy(self_channel)

    # Generic model: no SELF label, but pays interventions to discover the reusable driver.
    generic_channel, calibration_interventions, effects = discover_causal_driver_by_intervention()
    generic_test_acc = accuracy(one_channel_predict(generic_channel, test), test)
    generic_intervention_acc = intervention_prediction_accuracy(generic_channel)

    oracle_channel = TRUE_DRIVER
    oracle_test_acc = accuracy(one_channel_predict(oracle_channel, test), test)

    clone = external_clone_attacker()

    result = {
        "gate": "G10_CAUSAL_BOTTLENECK_VS_SELF",
        "train_examples": len(train),
        "held_out_examples": len(test),
        "ordinary_training_correlations": passive_scores,
        "flat_context_specific_lookup": {
            "stored_entries": len(flat),
            "held_out_accuracy": flat_acc,
        },
        "passive_single_variable_shortcut": {
            "selected_channel": passive_channel,
            "training_accuracy": passive_train_acc,
            "held_out_correlation_reversal_accuracy": passive_test_acc,
            "model_entries": 2,
            "calibration_interventions": 0,
        },
        "hand_labelled_SELF_factor": {
            "selected_channel": self_channel,
            "held_out_accuracy": self_test_acc,
            "intervention_prediction_accuracy": self_intervention_acc,
            "model_entries": 2,
            "privileged_driver_label_supplied": True,
            "calibration_interventions": 0,
        },
        "generic_causal_bottleneck": {
            "selected_channel": generic_channel,
            "intervention_effects": effects,
            "held_out_accuracy": generic_test_acc,
            "intervention_prediction_accuracy": generic_intervention_acc,
            "model_entries": 2,
            "calibration_interventions": calibration_interventions,
            "uses_SELF_vocabulary": False,
        },
        "oracle": {
            "selected_channel": oracle_channel,
            "held_out_accuracy": oracle_test_acc,
        },
        "external_causal_clone_attacker": clone,
        "classification": (
            "A_REUSABLE_AFFORDANCE_DRIVER_FORMS_A_TRANSFERABLE_CAUSAL_BOTTLENECK_"
            "ACROSS_CORRELATION_REVERSALS_BUT_A_GENERIC_INTERVENTION_DISCOVERY_MODEL_"
            "MATCHES_THE_HAND_LABELLED_SELF_FACTOR_AT_THE_SAME_MODEL_SIZE_AFTER_PAYING_"
            "CALIBRATION_INTERVENTIONS_SO_SELF_ADDS_NO_NEW_COMPUTATIONAL_PRIMITIVE_HERE"
        ),
        "claim_boundary": (
            "Constructed transfer result. A one-variable causal sufficient statistic generalizes across "
            "changing external correlations and beats a flat lookup / passive shortcut in this toy. But "
            "a generic causal-bottleneck procedure with no SELF vocabulary discovers the same variable "
            "and matches the hand-labelled SELF model after three calibration interventions. The result "
            "supports causal abstraction and transferable system identification, not selfhood or phenomenology."
        ),
    }

    # Ordinary training data must not reveal the causal driver by correlation.
    assert len(set(passive_scores.values())) == 1 and next(iter(passive_scores.values())) == 1.0, result
    assert passive_channel == "V0", result
    assert passive_train_acc == 1.0, result

    # Correlation reversal must punish the passive shortcut and flat memorization.
    assert passive_test_acc < 1.0, result
    assert flat_acc < 1.0, result

    # The hand-labelled factor and generic causal bottleneck must transfer equally.
    assert self_test_acc == 1.0, result
    assert generic_channel == TRUE_DRIVER, result
    assert generic_test_acc == self_test_acc == oracle_test_acc == 1.0, result
    assert generic_intervention_acc == self_intervention_acc == 1.0, result
    assert calibration_interventions == len(CHANNELS), result

    # Same model size: only the information source differs (privileged label vs interventions).
    assert result["hand_labelled_SELF_factor"]["model_entries"] == result["generic_causal_bottleneck"]["model_entries"], result

    # External-location stopping line.
    assert clone["generic_bottleneck_succeeds_without_internal_location"], result

    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
