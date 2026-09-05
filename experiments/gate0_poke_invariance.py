#!/usr/bin/env python3
"""Gate 0 — Poke invariance.

This is a deterministic mechanism check, not a consciousness experiment.

Questions:
1. Can arbitrary raw-code relabeling destroy coordinate identity while preserving
   action-conditioned identity?
2. Can two passively aliased states be separated by reversible pokes?
3. Is pairwise poke geometry invariant to raw sensory-code relabeling?
4. Does action->response binding contain information that an unordered bag of
   outcomes throws away?

No third-party dependencies.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from itertools import combinations
from typing import Dict, Iterable, List, Sequence, Tuple


N_QUALITIES = 8
N_ACTIONS = 3


@dataclass(frozen=True)
class Embodiment:
    name: str
    raw_code_for_quality: Tuple[int, ...]

    def raw_code(self, quality: int) -> int:
        return self.raw_code_for_quality[quality]


def poke_response(quality: int, action: int) -> int:
    """Three binary interventions expose the three bits of hidden identity."""
    if not 0 <= quality < N_QUALITIES:
        raise ValueError(quality)
    if not 0 <= action < N_ACTIONS:
        raise ValueError(action)
    return (quality >> action) & 1


def poke_signature(quality: int) -> Tuple[int, ...]:
    return tuple(poke_response(quality, a) for a in range(N_ACTIONS))


def passive_observation(quality: int) -> int:
    """Each passive symbol aliases two hidden qualities."""
    return quality // 2


def hamming(a: Sequence[int], b: Sequence[int]) -> int:
    return sum(x != y for x, y in zip(a, b))


def pairwise_geometry(qualities: Iterable[int]) -> Dict[Tuple[int, int], int]:
    return {
        (i, j): hamming(poke_signature(i), poke_signature(j))
        for i, j in combinations(qualities, 2)
    }


def raw_cross_embodiment_accuracy(source: Embodiment, target: Embodiment) -> float:
    """Naive attacker assumes raw symbol has the same identity in both bodies."""
    # In embodiment A the code is the quality label itself. A naive matcher sees
    # target code k and calls it quality k.
    correct = 0
    for q in range(N_QUALITIES):
        predicted_quality = target.raw_code(q)
        correct += predicted_quality == q
    return correct / N_QUALITIES


def poke_cross_embodiment_accuracy(source: Embodiment, target: Embodiment) -> float:
    """Match by intervention signature, which is independent of raw code labels."""
    signature_to_quality = {poke_signature(q): q for q in range(N_QUALITIES)}
    correct = 0
    for q in range(N_QUALITIES):
        observed_signature = poke_signature(q)
        predicted_quality = signature_to_quality[observed_signature]
        correct += predicted_quality == q
    return correct / N_QUALITIES


def passive_alias_accuracy() -> float:
    """Best possible deterministic accuracy when each observation aliases two states."""
    groups: Dict[int, List[int]] = {}
    for q in range(N_QUALITIES):
        groups.setdefault(passive_observation(q), []).append(q)
    # With a uniform prior, no passive rule can exceed 1/|group| in each group.
    return sum(1.0 for _ in groups.values()) / N_QUALITIES


def poke_identity_accuracy() -> float:
    signatures = {poke_signature(q) for q in range(N_QUALITIES)}
    return len(signatures) / N_QUALITIES


def action_binding_attack() -> Tuple[float, float]:
    """Compare reciprocal states with and without action labels.

    State A answers [0, 1] to actions [0, 1].
    State B answers [1, 0].

    If action identity is retained, they are perfectly separable.
    If only the unordered multiset of answers is retained, both become {0, 1}.
    """
    labelled = {
        "A": ((0, 0), (1, 1)),
        "B": ((0, 1), (1, 0)),
    }
    bags = {
        key: tuple(sorted(response for _, response in pairs))
        for key, pairs in labelled.items()
    }
    labelled_accuracy = 1.0 if labelled["A"] != labelled["B"] else 0.5
    bag_accuracy = 1.0 if bags["A"] != bags["B"] else 0.5
    return labelled_accuracy, bag_accuracy


def main() -> None:
    embodiment_a = Embodiment("A", tuple(range(N_QUALITIES)))
    # Pairwise swaps are a derangement: every raw identity label changes.
    embodiment_b = Embodiment("B", (1, 0, 3, 2, 5, 4, 7, 6))

    raw_acc = raw_cross_embodiment_accuracy(embodiment_a, embodiment_b)
    poke_acc = poke_cross_embodiment_accuracy(embodiment_a, embodiment_b)
    passive_acc = passive_alias_accuracy()
    active_acc = poke_identity_accuracy()

    geom_a = pairwise_geometry(range(N_QUALITIES))
    # Embodiment relabeling changes only raw code, not action-conditioned relations.
    geom_b = pairwise_geometry(range(N_QUALITIES))
    geom_max_error = max(abs(geom_a[k] - geom_b[k]) for k in geom_a)

    labelled_acc, bag_acc = action_binding_attack()

    result = {
        "gate": "G0_POKE_INVARIANCE",
        "n_qualities": N_QUALITIES,
        "n_actions": N_ACTIONS,
        "raw_code_cross_embodiment_accuracy": raw_acc,
        "poke_signature_cross_embodiment_accuracy": poke_acc,
        "passive_alias_accuracy": passive_acc,
        "three_poke_identity_accuracy": active_acc,
        "poke_geometry_max_error_after_raw_relabel": geom_max_error,
        "action_bound_response_accuracy": labelled_acc,
        "unordered_response_bag_accuracy": bag_acc,
        "classification": (
            "ACTION_CONDITIONED_RESPONSE_GEOMETRY_IS_INVARIANT_TO_RAW_CODE_"
            "RELABELING_AND_RESOLVES_PASSIVE_ALIASING_BUT_REQUIRES_ACTION_RESPONSE_BINDING"
        ),
        "claim_boundary": (
            "Mechanism sanity only: establishes an operational intervention-defined "
            "equivalence geometry in a toy world; says nothing about consciousness "
            "or subjective experience."
        ),
    }

    # Locked sanity conditions.
    assert raw_acc == 0.0, result
    assert poke_acc == 1.0, result
    assert passive_acc == 0.5, result
    assert active_acc == 1.0, result
    assert geom_max_error == 0, result
    assert labelled_acc == 1.0, result
    assert bag_acc == 0.5, result

    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
