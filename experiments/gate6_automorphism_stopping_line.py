#!/usr/bin/env python3
"""Gate 6 — Inverted-spectrum / automorphism stopping line.

This gate does not try to "solve" the inverted spectrum.  It makes the limitation
of an intervention-defined quality space executable.

Two embodiments live on the same six-state cyclic operational world.  They have the
same named actions and exactly the same action-conditioned transition structure,
but embodiment B globally rotates the arbitrary internal quality labels by three.
Thus corresponding physical states have different raw quality labels.

The ring has six action-preserving rotational automorphisms.  Complete operational
transition data therefore cannot determine which rotation is the privileged
cross-agent semantic correspondence.  The actual hidden correspondence is one of
six equally structure-preserving maps.  A single externally supplied anchor breaks
the symmetry, but that anchor is extra information rather than something recovered
from the quality geometry itself.

This is the intended stopping line of PokeAQuale: if a philosophical inversion
preserves the complete action-conditioned structure made available to the theory,
the framework must call the systems operationally isomorphic and abstain from
claiming a further hidden phenomenal fact.

Constructed finite-state result; no consciousness claim.
"""

from __future__ import annotations

import itertools
import json
from typing import Dict, Iterable, Sequence, Tuple


N = 6
ACTIONS = ("CW", "CCW", "STAY")
INVERSION_SHIFT = 3


def transition(label: int, action: str) -> int:
    if action == "CW":
        return (label + 1) % N
    if action == "CCW":
        return (label - 1) % N
    if action == "STAY":
        return label
    raise ValueError(action)


def a_label(physical_state: int) -> int:
    return physical_state


def b_label(physical_state: int) -> int:
    return (physical_state + INVERSION_SHIFT) % N


def actual_cross_embodiment_map(a_raw_label: int) -> int:
    # Hidden construction map, deliberately unavailable to the operational matcher.
    return (a_raw_label + INVERSION_SHIFT) % N


def is_action_preserving_isomorphism(permutation: Sequence[int]) -> bool:
    """Does phi(T(s,a)) == T(phi(s),a) for every state and named action?"""
    for state in range(N):
        for action in ACTIONS:
            left = permutation[transition(state, action)]
            right = transition(permutation[state], action)
            if left != right:
                return False
    return True


def all_operational_isomorphisms() -> Tuple[Tuple[int, ...], ...]:
    return tuple(
        perm
        for perm in itertools.permutations(range(N))
        if is_action_preserving_isomorphism(perm)
    )


def obeys_anchor(permutation: Sequence[int], a_state: int, b_state: int) -> bool:
    return permutation[a_state] == b_state


def rollout(start: int, actions: Iterable[str]) -> Tuple[int, ...]:
    state = start
    observations = [state]
    for action in actions:
        state = transition(state, action)
        observations.append(state)
    return tuple(observations)


def mapped_rollout(
    a_start: int,
    actions: Sequence[str],
    mapping: Sequence[int],
) -> Tuple[int, ...]:
    return tuple(mapping[label] for label in rollout(a_start, actions))


def main() -> None:
    actual_map = tuple(actual_cross_embodiment_map(i) for i in range(N))
    identity = tuple(range(N))
    isomorphisms = all_operational_isomorphisms()

    # Across corresponding physical states the arbitrary internal labels disagree
    # everywhere under this half-cycle shift.
    raw_matches = sum(
        a_label(physical) == b_label(physical)
        for physical in range(N)
    )
    raw_label_correspondence_accuracy = raw_matches / N

    # Every zero-error operational alignment is a ring rotation.  The hidden actual
    # mapping is present, but complete action-conditioned structure cannot select it.
    actual_is_operationally_valid = actual_map in isomorphisms
    identity_is_operationally_valid = identity in isomorphisms

    # A test battery verifies that the actual hidden map carries complete A
    # trajectories to the corresponding B-labelled trajectories exactly.
    probe_sequences = (
        (),
        ("CW",),
        ("CCW",),
        ("CW", "CW"),
        ("CW", "CCW", "STAY", "CW"),
        ("CCW", "CCW", "CW", "STAY", "CW"),
    )
    max_actual_mapping_mismatches = 0
    for physical_start in range(N):
        for actions in probe_sequences:
            a_start = a_label(physical_start)
            b_start = b_label(physical_start)
            a_mapped = mapped_rollout(a_start, actions, actual_map)
            b_trace = rollout(b_start, actions)
            mismatches = sum(x != y for x, y in zip(a_mapped, b_trace))
            max_actual_mapping_mismatches = max(max_actual_mapping_mismatches, mismatches)

    anchor_a = 0
    anchor_b = actual_cross_embodiment_map(anchor_a)
    anchored_isomorphisms = tuple(
        perm
        for perm in isomorphisms
        if obeys_anchor(perm, anchor_a, anchor_b)
    )

    result = {
        "gate": "G6_AUTOMORPHISM_STOPPING_LINE",
        "n_operational_states": N,
        "actions": list(ACTIONS),
        "hidden_internal_label_shift": INVERSION_SHIFT,
        "raw_label_correspondence_accuracy_on_same_physical_states": raw_label_correspondence_accuracy,
        "complete_action_conditioned_structure": {
            "zero_error_cross_agent_isomorphisms": len(isomorphisms),
            "isomorphisms": [list(p) for p in isomorphisms],
            "actual_hidden_correspondence_is_one_valid_isomorphism": actual_is_operationally_valid,
            "literal_identity_map_is_also_one_valid_isomorphism": identity_is_operationally_valid,
            "max_trace_mismatches_under_actual_mapping": max_actual_mapping_mismatches,
            "chance_of_selecting_actual_hidden_mapping_from_symmetric_isomorphisms": 1.0 / len(isomorphisms),
        },
        "one_external_anchor": {
            "anchor": {"agent_a_label": anchor_a, "agent_b_label": anchor_b},
            "remaining_zero_error_isomorphisms": len(anchored_isomorphisms),
            "remaining_map": list(anchored_isomorphisms[0]) if anchored_isomorphisms else None,
        },
        "classification": (
            "GLOBAL_INTERNAL_LABEL_AUTOMORPHISMS_THAT_PRESERVE_COMPLETE_ACTION_"
            "CONDITIONED_STRUCTURE_ARE_OPERATIONALLY_UNIDENTIFIABLE_UNTIL_EXTRA_"
            "ANCHOR_INFORMATION_IS_SUPPLIED"
        ),
        "claim_boundary": (
            "Constructed symmetry result. The action-conditioned quality geometry fixes "
            "relational structure but not an absolute semantic origin when the structure "
            "has nontrivial automorphisms. PokeAQuale therefore cannot detect a secret "
            "inverted spectrum that preserves all supplied operational relations, and it "
            "does not infer phenomenology from operational isomorphism."
        ),
    }

    assert raw_label_correspondence_accuracy == 0.0, result
    assert len(isomorphisms) == N, result
    assert actual_is_operationally_valid, result
    assert identity_is_operationally_valid, result
    assert max_actual_mapping_mismatches == 0, result
    assert len(anchored_isomorphisms) == 1, result
    assert anchored_isomorphisms[0] == actual_map, result

    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
