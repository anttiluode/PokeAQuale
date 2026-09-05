#!/usr/bin/env python3
"""Gate 1 — Embodiment refines the operational quotient.

Same hidden world. Same passive observation. The only thing that changes is which
reversible actions the agent is able to issue.

Result expected by construction:
- no actions: all 8 hidden states collapse to one operational class;
- 1 binary poke: 2 classes;
- 2 binary pokes: 4 classes;
- 3 binary pokes: 8 classes.

This is a sanity theorem/example about agent-relative distinguishability, not a
consciousness result.
"""

from __future__ import annotations

import json
from collections import defaultdict
from typing import Dict, Iterable, List, Sequence, Tuple


N_STATES = 8
ALL_ACTIONS = (0, 1, 2)


def passive_observation(_: int) -> int:
    # The passive sensor is intentionally useless: every hidden state looks alike.
    return 0


def response(state: int, action: int) -> int:
    # Each reversible action exposes one hidden bit.
    return (state >> action) & 1


def operational_signature(state: int, actions: Sequence[int]) -> Tuple[int, ...]:
    return (passive_observation(state),) + tuple(response(state, a) for a in actions)


def partition(actions: Sequence[int]) -> Tuple[Tuple[int, ...], ...]:
    groups: Dict[Tuple[int, ...], List[int]] = defaultdict(list)
    for state in range(N_STATES):
        groups[operational_signature(state, actions)].append(state)
    return tuple(sorted(tuple(v) for v in groups.values()))


def is_refinement(fine: Iterable[Tuple[int, ...]], coarse: Iterable[Tuple[int, ...]]) -> bool:
    coarse_sets = [set(c) for c in coarse]
    return all(any(set(f).issubset(c) for c in coarse_sets) for f in fine)


def main() -> None:
    action_sets = [(), (0,), (0, 1), (0, 1, 2)]
    partitions = [partition(a) for a in action_sets]
    class_counts = [len(p) for p in partitions]

    refinement_chain = all(
        is_refinement(partitions[i + 1], partitions[i])
        for i in range(len(partitions) - 1)
    )

    # Strict refinement should occur at every added action in this toy.
    strict = all(class_counts[i + 1] > class_counts[i] for i in range(len(class_counts) - 1))

    result = {
        "gate": "G1_EMBODIMENT_REFINES_QUOTIENT",
        "n_hidden_states": N_STATES,
        "passive_observation_classes": 1,
        "action_sets": [list(a) for a in action_sets],
        "operational_class_counts": class_counts,
        "partitions": [[list(group) for group in p] for p in partitions],
        "monotone_refinement": refinement_chain,
        "strict_refinement_in_this_world": strict,
        "classification": (
            "ADDING_AVAILABLE_INTERVENTIONS_REFINES_THE_AGENT_RELATIVE_OPERATIONAL_"
            "STATE_SPACE_WITHOUT_CHANGING_WORLD_OR_PASSIVE_SENSOR"
        ),
        "claim_boundary": (
            "Constructed finite-state sanity result. Demonstrates embodiment-relative "
            "distinguishability only; it does not imply phenomenology."
        ),
    }

    assert class_counts == [1, 2, 4, 8], result
    assert refinement_chain, result
    assert strict, result

    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
