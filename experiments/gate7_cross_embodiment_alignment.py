#!/usr/bin/env python3
"""Gate 7 — Cross-embodiment alignment with honest and misleading passive geometry.

Question
--------
Can two agents with different raw sensors align operational qualities without a raw
coordinate map?

The gate has two conditions over the same six-state physical ring and the same
hidden cross-agent state relabeling.

HONEST PASSIVE GEOMETRY
    Agent B's passive feature cloud is an isometric coordinate transform of Agent
    A's cloud under the true physical correspondence.  A strong passive metric / 
    affine alignment attacker should solve the correspondence with no pokes.

MISLEADING PASSIVE GEOMETRY
    Agent B has the same beautiful isometric feature geometry, but it is attached
    to the *wrong physical states* by a cyclic shift.  Passive metric and affine
    alignment are therefore confidently exact but semantically wrong.  The shared
    action-conditioned consequence profile remains attached to the physical state
    and recovers the true correspondence.

A transition-only attacker is also included.  The physical dynamics are a symmetric
ring, so named-action transition structure alone admits six equally valid rotations.

This gate does NOT show that interventions are universally needed.  In the honest
condition, passive geometry wins for free.  It only shows the narrower case where
cross-agent passive geometry can itself be a false friend and shared causal
consequences provide the missing anchor.

Constructed finite-state / linear-algebra sanity check; no phenomenology claim.
"""

from __future__ import annotations

import itertools
import json
import math
import random
from typing import Dict, Iterable, List, Sequence, Tuple


N = 6
DIM = 4
ACTIONS = (0, 1, 2)  # three reversible diagnostic consequence channels
MOVE_ACTIONS = ("CW", "CCW", "STAY")

# Arbitrary internal relabeling from A labels / physical states to B labels.
ACTUAL_MAP = (2, 5, 1, 4, 0, 3)
INV_ACTUAL = tuple(ACTUAL_MAP.index(i) for i in range(N))

Vector = Tuple[float, ...]
Permutation = Tuple[int, ...]


def physical_transition(q: int, action: str) -> int:
    if action == "CW":
        return (q + 1) % N
    if action == "CCW":
        return (q - 1) % N
    if action == "STAY":
        return q
    raise ValueError(action)


def b_transition(b_label: int, action: str) -> int:
    physical = INV_ACTUAL[b_label]
    return ACTUAL_MAP[physical_transition(physical, action)]


def consequence_profile(physical_state: int) -> Tuple[int, int, int]:
    # Three shared binary intervention consequences.  These are operational
    # outcomes, not a hidden semantic class label.
    return tuple((physical_state >> bit) & 1 for bit in range(3))  # type: ignore[return-value]


def a_profile(a_label: int) -> Tuple[int, int, int]:
    return consequence_profile(a_label)


def b_profile(b_label: int) -> Tuple[int, int, int]:
    return consequence_profile(INV_ACTUAL[b_label])


def make_a_codes() -> Dict[int, Vector]:
    rng = random.Random(7102026)
    return {q: tuple(rng.gauss(0.0, 2.0) for _ in range(DIM)) for q in range(N)}


def sensor_transform(x: Vector) -> Vector:
    # Exact Euclidean isometry: coordinate permutation plus sign flips.
    order = (2, 0, 3, 1)
    signs = (1.0, -1.0, 1.0, -1.0)
    return tuple(signs[d] * x[order[d]] for d in range(DIM))


def make_b_codes(a_codes: Dict[int, Vector], misleading: bool) -> Dict[int, Vector]:
    out: Dict[int, Vector] = {}
    for physical in range(N):
        source_physical = (physical + 1) % N if misleading else physical
        out[ACTUAL_MAP[physical]] = sensor_transform(a_codes[source_physical])
    return out


def sqdist(a: Sequence[float], b: Sequence[float]) -> float:
    return sum((x - y) ** 2 for x, y in zip(a, b))


def pairwise_distance_alignment_error(
    a_codes: Dict[int, Vector], b_codes: Dict[int, Vector], mapping: Sequence[int]
) -> float:
    err = 0.0
    for i in range(N):
        for j in range(i + 1, N):
            da = math.sqrt(sqdist(a_codes[i], a_codes[j]))
            db = math.sqrt(sqdist(b_codes[mapping[i]], b_codes[mapping[j]]))
            err += (da - db) ** 2
    return err


def best_metric_alignment(a_codes: Dict[int, Vector], b_codes: Dict[int, Vector]) -> Tuple[Permutation, float, int]:
    scored = []
    for perm in itertools.permutations(range(N)):
        scored.append((pairwise_distance_alignment_error(a_codes, b_codes, perm), perm))
    best_error = min(error for error, _ in scored)
    tol = max(1e-10, best_error + 1e-9)
    best = [perm for error, perm in scored if error <= tol]
    return best[0], best_error, len(best)


def solve_linear(matrix: List[List[float]], rhs: List[float]) -> List[float]:
    n = len(rhs)
    aug = [row[:] + [rhs[i]] for i, row in enumerate(matrix)]
    for col in range(n):
        pivot = max(range(col, n), key=lambda r: abs(aug[r][col]))
        aug[col], aug[pivot] = aug[pivot], aug[col]
        if abs(aug[col][col]) < 1e-12:
            aug[col][col] += 1e-9
        scale = aug[col][col]
        aug[col] = [v / scale for v in aug[col]]
        for row in range(n):
            if row == col:
                continue
            factor = aug[row][col]
            if factor == 0.0:
                continue
            aug[row] = [a - factor * b for a, b in zip(aug[row], aug[col])]
    return [aug[i][-1] for i in range(n)]


def affine_fit_residual(
    a_codes: Dict[int, Vector], b_codes: Dict[int, Vector], mapping: Sequence[int]
) -> float:
    # Fit y = W [x, 1] by ridge-stabilized least squares for a proposed unpaired
    # correspondence. Searching over permutations makes this a strong passive
    # linear-alignment attacker for the tiny toy.
    x_rows = [list(a_codes[i]) + [1.0] for i in range(N)]
    y_rows = [list(b_codes[mapping[i]]) for i in range(N)]
    p = DIM + 1

    xtx = [[0.0 for _ in range(p)] for _ in range(p)]
    for x in x_rows:
        for i in range(p):
            for j in range(p):
                xtx[i][j] += x[i] * x[j]
    for i in range(p):
        xtx[i][i] += 1e-10

    coefficients: List[List[float]] = []
    for out_dim in range(DIM):
        xty = [sum(x_rows[r][i] * y_rows[r][out_dim] for r in range(N)) for i in range(p)]
        coefficients.append(solve_linear(xtx, xty))

    residual = 0.0
    for x, y in zip(x_rows, y_rows):
        pred = [sum(coefficients[d][i] * x[i] for i in range(p)) for d in range(DIM)]
        residual += sqdist(pred, y)
    return residual


def best_affine_alignment(a_codes: Dict[int, Vector], b_codes: Dict[int, Vector]) -> Tuple[Permutation, float, int]:
    scored = []
    for perm in itertools.permutations(range(N)):
        scored.append((affine_fit_residual(a_codes, b_codes, perm), perm))
    best_error = min(error for error, _ in scored)
    tolerance = best_error + 1e-7
    best = [perm for error, perm in scored if error <= tolerance]
    return best[0], best_error, len(best)


def transition_isomorphisms() -> Tuple[Permutation, ...]:
    valid = []
    for perm in itertools.permutations(range(N)):
        ok = True
        for a_state in range(N):
            for action in MOVE_ACTIONS:
                if perm[physical_transition(a_state, action)] != b_transition(perm[a_state], action):
                    ok = False
                    break
            if not ok:
                break
        if ok:
            valid.append(perm)
    return tuple(valid)


def action_profile_alignment() -> Permutation:
    mapping = []
    for a_state in range(N):
        target = a_profile(a_state)
        matches = [b_state for b_state in range(N) if b_profile(b_state) == target]
        if len(matches) != 1:
            raise AssertionError((a_state, target, matches))
        mapping.append(matches[0])
    return tuple(mapping)


def mapping_accuracy(mapping: Sequence[int]) -> float:
    return sum(mapping[i] == ACTUAL_MAP[i] for i in range(N)) / N


def expected_misleading_passive_map() -> Permutation:
    # B label ACTUAL_MAP[q] carries transformed passive code from A state q+1.
    # Therefore A state i is passively aligned to the B label of physical i-1.
    return tuple(ACTUAL_MAP[(i - 1) % N] for i in range(N))


def profile_class_count(n_actions: int) -> int:
    prefixes = {a_profile(q)[:n_actions] for q in range(N)}
    return len(prefixes)


def run_condition(name: str, a_codes: Dict[int, Vector], b_codes: Dict[int, Vector]) -> dict:
    metric_map, metric_error, metric_ties = best_metric_alignment(a_codes, b_codes)
    affine_map, affine_error, affine_ties = best_affine_alignment(a_codes, b_codes)
    return {
        "condition": name,
        "passive_metric_alignment": {
            "mapping": list(metric_map),
            "semantic_correspondence_accuracy": mapping_accuracy(metric_map),
            "residual": metric_error,
            "zeroish_best_maps": metric_ties,
        },
        "passive_affine_alignment": {
            "mapping": list(affine_map),
            "semantic_correspondence_accuracy": mapping_accuracy(affine_map),
            "residual": affine_error,
            "zeroish_best_maps": affine_ties,
        },
    }


def main() -> None:
    a_codes = make_a_codes()
    b_honest = make_b_codes(a_codes, misleading=False)
    b_misleading = make_b_codes(a_codes, misleading=True)

    honest = run_condition("HONEST_PASSIVE_GEOMETRY", a_codes, b_honest)
    misleading = run_condition("MISLEADING_PASSIVE_GEOMETRY", a_codes, b_misleading)

    transition_maps = transition_isomorphisms()
    causal_map = action_profile_alignment()
    expected_wrong = expected_misleading_passive_map()

    result = {
        "gate": "G7_CROSS_EMBODIMENT_ALIGNMENT",
        "n_states": N,
        "passive_dimension": DIM,
        "true_hidden_cross_embodiment_map": list(ACTUAL_MAP),
        "honest_condition": honest,
        "misleading_condition": misleading,
        "transition_only_attacker": {
            "zero_error_isomorphisms": len(transition_maps),
            "true_map_is_among_them": ACTUAL_MAP in transition_maps,
            "chance_of_selecting_true_map_without_extra_anchor": 1.0 / len(transition_maps),
        },
        "action_conditioned_consequence_alignment": {
            "mapping": list(causal_map),
            "semantic_correspondence_accuracy": mapping_accuracy(causal_map),
            "operational_classes_with_1_2_3_actions": [
                profile_class_count(1),
                profile_class_count(2),
                profile_class_count(3),
            ],
        },
        "expected_misleading_passive_map": list(expected_wrong),
        "classification": (
            "PASSIVE_GEOMETRY_CAN_ALIGN_EMBODIMENTS_FOR_FREE_WHEN_ITS_STRUCTURE_IS_"
            "SEMANTICALLY_HONEST_BUT_CAN_BE_EXACTLY_AND_CONFIDENTLY_WRONG_WHEN_"
            "GEOMETRY_IS_REATTACHED_TO_DIFFERENT_CAUSES_WHILE_SHARED_ACTION_"
            "CONSEQUENCES_RECOVER_THE_CAUSAL_CORRESPONDENCE"
        ),
        "claim_boundary": (
            "Constructed cross-embodiment sanity result. It does not show that action "
            "is always necessary: the honest passive condition is solved exactly by "
            "metric and affine attackers. It shows only that passive relational geometry "
            "can itself be an isomorphic false friend, while shared intervention outcomes "
            "can act as extra causal anchors. Those shared action/outcome semantics are "
            "themselves an assumption and do not establish phenomenology."
        ),
    }

    # Honest passive geometry: boring passive attackers should win exactly.
    assert tuple(honest["passive_metric_alignment"]["mapping"]) == ACTUAL_MAP, result
    assert honest["passive_metric_alignment"]["semantic_correspondence_accuracy"] == 1.0, result
    assert honest["passive_metric_alignment"]["residual"] < 1e-12, result
    assert tuple(honest["passive_affine_alignment"]["mapping"]) == ACTUAL_MAP, result
    assert honest["passive_affine_alignment"]["semantic_correspondence_accuracy"] == 1.0, result
    assert honest["passive_affine_alignment"]["residual"] < 1e-8, result

    # Misleading passive geometry: same elegant geometry, wrong physical attachment.
    assert tuple(misleading["passive_metric_alignment"]["mapping"]) == expected_wrong, result
    assert misleading["passive_metric_alignment"]["semantic_correspondence_accuracy"] == 0.0, result
    assert misleading["passive_metric_alignment"]["residual"] < 1e-12, result
    assert tuple(misleading["passive_affine_alignment"]["mapping"]) == expected_wrong, result
    assert misleading["passive_affine_alignment"]["semantic_correspondence_accuracy"] == 0.0, result
    assert misleading["passive_affine_alignment"]["residual"] < 1e-8, result

    assert len(transition_maps) == N, result
    assert ACTUAL_MAP in transition_maps, result
    assert causal_map == ACTUAL_MAP, result
    assert mapping_accuracy(causal_map) == 1.0, result
    assert [profile_class_count(k) for k in (1, 2, 3)] == [2, 4, 6], result

    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
