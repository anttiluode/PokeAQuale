#!/usr/bin/env python3
"""Gate 8 — Does endogenous homeostatic consequence provide a privileged anchor?

Gate 7 ended with a cheat: the two agents shared action names and consequence
semantics.  A tempting next move is to say that consequences to the organism itself
(homeostasis, damage, energy, future action capacity) are a more intrinsic source of
"for-me-ness" than an experimenter-provided label.

This gate attacks that move before granting it special status.

World
-----
Six operational states form a symmetric ring.  Agent B arbitrarily relabels those
states.  Transition structure alone therefore admits six exact cross-agent maps.

BODY CHANNEL
    Contact with a state changes an internal action-capacity budget by a
    state-dependent amount.  The pattern contains repeated values, so body effect
    alone does not uniquely label all states.  Combined with ring relations it
    breaks the rotational symmetry and recovers one cross-agent map.

MATCHED EXTERNAL CHANNEL
    An exogenous beacon carries exactly the same state-dependent pattern but does
    *not* modify the agent.  It supplies the same alignment information and breaks
    the symmetry equally well.

Therefore homeostasis can be an endogenous causal anchor, but mere symmetry
breaking does not make it mathematically privileged: an equally informative
external asymmetry does the same alignment work.

A stronger future claim would have to exploit the fact that body consequence
changes future control / viability, not merely the fact that it adds another
observable state label.

Constructed finite-state result; no phenomenology claim.
"""

from __future__ import annotations

import itertools
import json
from typing import Dict, Sequence, Tuple


N = 6
MOVE_ACTIONS = ("CW", "CCW", "STAY")
ACTUAL_MAP = (2, 5, 1, 4, 0, 3)
INV_ACTUAL = tuple(ACTUAL_MAP.index(i) for i in range(N))

# Deliberately repeated values; no state gets a unique "homeostatic label" for free.
# The cyclic arrangement itself is asymmetric.
BODY_DELTA = (0, -1, 0, 1, -1, -2)
EXTERNAL_BEACON = BODY_DELTA

Permutation = Tuple[int, ...]


def transition_a(state: int, action: str) -> int:
    if action == "CW":
        return (state + 1) % N
    if action == "CCW":
        return (state - 1) % N
    if action == "STAY":
        return state
    raise ValueError(action)


def transition_b(label: int, action: str) -> int:
    physical = INV_ACTUAL[label]
    next_physical = transition_a(physical, action)
    return ACTUAL_MAP[next_physical]


def body_a(state: int) -> int:
    return BODY_DELTA[state]


def body_b(label: int) -> int:
    return BODY_DELTA[INV_ACTUAL[label]]


def beacon_a(state: int) -> int:
    return EXTERNAL_BEACON[state]


def beacon_b(label: int) -> int:
    return EXTERNAL_BEACON[INV_ACTUAL[label]]


def preserves_transitions(mapping: Sequence[int]) -> bool:
    for a_state in range(N):
        for action in MOVE_ACTIONS:
            if mapping[transition_a(a_state, action)] != transition_b(mapping[a_state], action):
                return False
    return True


def preserves_channel(mapping: Sequence[int], channel_a, channel_b) -> bool:
    return all(channel_a(a_state) == channel_b(mapping[a_state]) for a_state in range(N))


def valid_maps(channel_a=None, channel_b=None) -> Tuple[Permutation, ...]:
    out = []
    for perm in itertools.permutations(range(N)):
        if not preserves_transitions(perm):
            continue
        if channel_a is not None and not preserves_channel(perm, channel_a, channel_b):
            continue
        out.append(perm)
    return tuple(out)


def channel_class_count(channel) -> int:
    return len({channel(s) for s in range(N)})


def simulate_capacity(start_capacity: int, state: int, contacts: int) -> Tuple[int, ...]:
    capacity = start_capacity
    history = [capacity]
    for _ in range(contacts):
        capacity += body_a(state)
        history.append(capacity)
    return tuple(history)


def main() -> None:
    transition_only = valid_maps()
    with_body = valid_maps(body_a, body_b)
    with_beacon = valid_maps(beacon_a, beacon_b)

    # Demonstrate the self-affecting meaning of the body channel separately from its
    # informational content.  Same current external state, repeated contact changes
    # future action capacity according to the endogenous consequence.
    capacity_examples: Dict[str, list[int]] = {
        str(state): list(simulate_capacity(4, state, 3)) for state in range(N)
    }

    result = {
        "gate": "G8_HOMEOSTATIC_ANCHOR",
        "n_states": N,
        "body_delta_pattern": list(BODY_DELTA),
        "body_channel_distinct_values": channel_class_count(body_a),
        "transition_only": {
            "zero_error_maps": len(transition_only),
            "true_map_is_present": ACTUAL_MAP in transition_only,
            "chance_of_true_map_without_anchor": 1.0 / len(transition_only),
        },
        "endogenous_body_consequence": {
            "zero_error_maps_preserving_transition_and_body_effect": len(with_body),
            "remaining_map": list(with_body[0]) if with_body else None,
            "true_map_recovered": with_body == (ACTUAL_MAP,),
            "example_capacity_trajectories_from_budget_4": capacity_examples,
        },
        "matched_external_asymmetry_attacker": {
            "beacon_pattern": list(EXTERNAL_BEACON),
            "zero_error_maps_preserving_transition_and_beacon": len(with_beacon),
            "remaining_map": list(with_beacon[0]) if with_beacon else None,
            "true_map_recovered": with_beacon == (ACTUAL_MAP,),
            "same_alignment_information_as_body_channel": with_beacon == with_body,
        },
        "classification": (
            "ENDOGENOUS_BODY_CONSEQUENCES_CAN_BREAK_AN_OPERATIONAL_AUTOMORPHISM_"
            "BUT_AN_EQUALLY_INFORMATIVE_EXTERNAL_ASYMMETRY_BREAKS_IT_IDENTICALLY_"
            "SO_HOMEOSTASIS_HAS_NOT_EARNED_SPECIAL_QUALIA_STATUS_FROM_ALIGNMENT_ALONE"
        ),
        "claim_boundary": (
            "Constructed symmetry-breaking result. A body-affecting consequence can "
            "provide an agent-internal causal anchor and can alter future action capacity, "
            "but its ability to align operational states is reproduced exactly by a "
            "matched external marker carrying the same information. Any stronger claim "
            "about for-me-ness must use closed-loop self-maintenance / controllability or "
            "viability consequences beyond mere asymmetric labeling. No phenomenology is inferred."
        ),
    }

    assert len(transition_only) == N, result
    assert ACTUAL_MAP in transition_only, result
    assert channel_class_count(body_a) == 4, result
    assert with_body == (ACTUAL_MAP,), result
    assert with_beacon == (ACTUAL_MAP,), result
    assert with_body == with_beacon, result

    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
