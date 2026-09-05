#!/usr/bin/env python3
"""Gate 5 — Active discovery can become immediate perception, but here it is distillation.

Gate 4 established a negative boundary: remembering a counterfactual response does
not remove exact current aliasing by itself.  Something in the current passive path
must become more informative.

This gate gives the passive path learnable structure and asks whether repeated
poke-confirmed distinctions can be compiled into a zero-poke predictor.

Setup
-----
- 8 operational qualities are defined by their 3-bit reversible poke signatures.
- Passive observations are arbitrary 6-D embodiment-specific feature clouds.
- During a calibration/development phase the system pays three pokes per sample to
  discover the operational signature; no hidden semantic label is needed.
- A slow compiler distills those discovered signatures into passive centroids.

Attackers / boundaries
----------------------
1. In the same embodiment, the compiled passive path should identify held-out
   samples with no test-time pokes.
2. An ordinary supervised centroid classifier given the *same poke-derived targets*
   must match it exactly.  If so, no special "structural qualia" mechanism has been
   earned; this is ordinary distillation / representation learning.
3. A new embodiment arbitrarily remaps passive feature prototypes while preserving
   the poke signatures.  The old passive compiler should fail, while active
   counterfactual identification remains exact.  Recompiling in the new generation
   restores immediate recognition.

Constructed toy result; no consciousness or phenomenology claim.
"""

from __future__ import annotations

import json
import random
from typing import Dict, Iterable, List, Sequence, Tuple


N_QUALITIES = 8
DIM = 6
N_TRAIN_PER_QUALITY = 16
N_TEST_PER_QUALITY = 64
POKES_PER_ACTIVE_IDENTIFICATION = 3
NOISE_SD = 0.45

Vector = Tuple[float, ...]
Example = Tuple[Vector, Tuple[int, int, int]]


def poke_signature(quality: int) -> Tuple[int, int, int]:
    return tuple((quality >> bit) & 1 for bit in range(3))  # type: ignore[return-value]


def quality_from_signature(signature: Sequence[int]) -> int:
    return sum(int(bit) << i for i, bit in enumerate(signature))


def make_prototypes() -> Dict[int, Vector]:
    rng = random.Random(20260905)
    return {
        q: tuple(rng.gauss(0.0, 3.0) for _ in range(DIM))
        for q in range(N_QUALITIES)
    }


def remap_prototypes(prototypes: Dict[int, Vector]) -> Dict[int, Vector]:
    # Same set of raw feature prototypes, but their assignment to operational
    # qualities shifts.  The counterfactual poke signature itself is unchanged.
    return {q: prototypes[(q + 1) % N_QUALITIES] for q in range(N_QUALITIES)}


def sample_dataset(
    prototypes: Dict[int, Vector],
    *,
    seed: int,
    n_per_quality: int,
) -> List[Tuple[Vector, int]]:
    rng = random.Random(seed)
    out: List[Tuple[Vector, int]] = []
    for q in range(N_QUALITIES):
        for _ in range(n_per_quality):
            x = tuple(
                prototypes[q][d] + rng.gauss(0.0, NOISE_SD)
                for d in range(DIM)
            )
            out.append((x, q))
    return out


def actively_label(dataset: Iterable[Tuple[Vector, int]]) -> Tuple[List[Example], int]:
    labelled: List[Example] = []
    pokes = 0
    for x, quality in dataset:
        # The "teacher" is not a hidden semantic class label.  It is the result of
        # issuing all three reversible diagnostic pokes.
        signature = poke_signature(quality)
        pokes += POKES_PER_ACTIVE_IDENTIFICATION
        labelled.append((x, signature))
    return labelled, pokes


def train_centroids(labelled: Iterable[Example]) -> Dict[Tuple[int, int, int], Vector]:
    sums: Dict[Tuple[int, int, int], List[float]] = {}
    counts: Dict[Tuple[int, int, int], int] = {}
    for x, signature in labelled:
        if signature not in sums:
            sums[signature] = [0.0] * DIM
            counts[signature] = 0
        counts[signature] += 1
        for d, value in enumerate(x):
            sums[signature][d] += value
    return {
        signature: tuple(v / counts[signature] for v in total)
        for signature, total in sums.items()
    }


def squared_distance(a: Sequence[float], b: Sequence[float]) -> float:
    return sum((x - y) ** 2 for x, y in zip(a, b))


def predict_signature(centroids: Dict[Tuple[int, int, int], Vector], x: Vector) -> Tuple[int, int, int]:
    return min(centroids, key=lambda s: squared_distance(x, centroids[s]))


def passive_accuracy(
    centroids: Dict[Tuple[int, int, int], Vector],
    dataset: Iterable[Tuple[Vector, int]],
) -> float:
    data = list(dataset)
    correct = 0
    for x, quality in data:
        pred_signature = predict_signature(centroids, x)
        correct += quality_from_signature(pred_signature) == quality
    return correct / len(data)


def active_accuracy(dataset: Iterable[Tuple[Vector, int]]) -> Tuple[float, int]:
    data = list(dataset)
    correct = 0
    pokes = 0
    for _x, quality in data:
        signature = poke_signature(quality)
        pokes += POKES_PER_ACTIVE_IDENTIFICATION
        pred = quality_from_signature(signature)
        correct += pred == quality
    return correct / len(data), pokes


def main() -> None:
    prototypes_a = make_prototypes()
    prototypes_b = remap_prototypes(prototypes_a)

    train_a = sample_dataset(prototypes_a, seed=1, n_per_quality=N_TRAIN_PER_QUALITY)
    test_a = sample_dataset(prototypes_a, seed=2, n_per_quality=N_TEST_PER_QUALITY)
    train_b = sample_dataset(prototypes_b, seed=3, n_per_quality=N_TRAIN_PER_QUALITY)
    test_b = sample_dataset(prototypes_b, seed=4, n_per_quality=N_TEST_PER_QUALITY)

    labelled_a, train_a_pokes = actively_label(train_a)
    compiled_a = train_centroids(labelled_a)

    # "Slow structural compiler" and boring supervised attacker receive exactly the
    # same x -> poke-signature examples.  In this gate they are intentionally the
    # same estimator; the point is to deny special credit when ordinary distillation
    # already explains the result.
    boring_supervised_a = train_centroids(labelled_a)

    stable_compiled_acc = passive_accuracy(compiled_a, test_a)
    boring_attacker_acc = passive_accuracy(boring_supervised_a, test_a)
    active_a_acc, active_a_test_pokes = active_accuracy(test_a)

    old_compiler_on_b_acc = passive_accuracy(compiled_a, test_b)
    active_b_acc, active_b_test_pokes = active_accuracy(test_b)

    labelled_b, train_b_pokes = actively_label(train_b)
    compiled_b = train_centroids(labelled_b)
    fresh_compiler_b_acc = passive_accuracy(compiled_b, test_b)

    total_test_examples = len(test_a)
    active_always_total_pokes_same_generation = train_a_pokes + active_a_test_pokes
    compile_then_passive_total_pokes_same_generation = train_a_pokes

    result = {
        "gate": "G5_ACTIVE_TO_IMMEDIATE_DISTILLATION",
        "n_qualities": N_QUALITIES,
        "passive_dimension": DIM,
        "train_examples": len(train_a),
        "test_examples": total_test_examples,
        "pokes_per_active_identification": POKES_PER_ACTIVE_IDENTIFICATION,
        "same_embodiment": {
            "active_every_test_example": {
                "accuracy": active_a_acc,
                "test_paid_pokes": active_a_test_pokes,
            },
            "poke_labelled_compiler": {
                "accuracy": stable_compiled_acc,
                "calibration_paid_pokes": train_a_pokes,
                "test_paid_pokes": 0,
            },
            "ordinary_supervised_centroid_same_targets": {
                "accuracy": boring_attacker_acc,
                "predictions_identical_to_compiler": boring_attacker_acc == stable_compiled_acc,
            },
            "total_poke_reduction_after_training_vs_active_always": (
                1.0
                - compile_then_passive_total_pokes_same_generation
                / active_always_total_pokes_same_generation
            ),
        },
        "new_embodiment_generation": {
            "old_passive_compiler_accuracy": old_compiler_on_b_acc,
            "active_counterfactual_accuracy": active_b_acc,
            "active_counterfactual_test_paid_pokes": active_b_test_pokes,
            "fresh_recompiled_passive_accuracy": fresh_compiler_b_acc,
            "fresh_recompile_calibration_paid_pokes": train_b_pokes,
            "fresh_recompile_test_paid_pokes": 0,
        },
        "classification": (
            "POKE_CONFIRMED_DISTINCTIONS_CAN_BE_DISTILLED_INTO_ZERO_POKE_PASSIVE_"
            "RECOGNITION_BUT_AN_ORDINARY_SUPERVISED_CLASSIFIER_MATCHES_EXACTLY_AND_"
            "THE_SHORTCUT_IS_REPRESENTATION_GENERATION_SPECIFIC"
        ),
        "claim_boundary": (
            "Constructed distillation result. It demonstrates a computational route from "
            "active identification to later immediate recognition, but here that route is "
            "fully explained by ordinary supervised learning on poke-derived targets. The "
            "active counterfactual signature is more invariant across embodiment remapping, "
            "while the passive shortcut is cheaper and more brittle. No phenomenology is inferred."
        ),
    }

    assert train_a_pokes == N_QUALITIES * N_TRAIN_PER_QUALITY * 3, result
    assert stable_compiled_acc == 1.0, result
    assert boring_attacker_acc == stable_compiled_acc, result
    assert active_a_acc == 1.0, result
    assert old_compiler_on_b_acc == 0.0, result
    assert active_b_acc == 1.0, result
    assert fresh_compiler_b_acc == 1.0, result
    assert result["same_embodiment"]["total_poke_reduction_after_training_vs_active_always"] == 0.8, result

    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
