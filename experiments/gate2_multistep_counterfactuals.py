#!/usr/bin/env python3
"""Gate 2 — Same one-step statistics, different multi-step counterfactuals.

Two tiny hidden machines have:
- identical passive observation;
- identical one-step action->response map;
- identical marginal response histogram over the complete length-2 probe battery;
- different *ordered* action-conditioned two-step futures.

The point is to attack a static / one-step version of the poke-profile idea.  If an
unordered response bag or one-step map is sufficient, the temporal predictive-state
object has earned nothing.

This is a constructed automata sanity check, not a consciousness result.
"""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from itertools import product
from typing import Callable, Dict, Hashable, Iterable, Mapping, Sequence, Tuple


ACTIONS = (0, 1)
START = 0
OBSERVATION = {0: 0, 1: 1, 2: 1, 3: 0, 4: 1}

# Both worlds make the same first transition from START, so every one-step test is
# identical.  They differ only in which second action continues versus flips the
# observed response.
TRANSITIONS = {
    "X": {
        0: {0: 1, 1: 2},
        1: {0: 3, 1: 4},
        2: {0: 4, 1: 3},
        3: {0: 3, 1: 3},
        4: {0: 4, 1: 4},
    },
    "Y": {
        0: {0: 1, 1: 2},
        1: {0: 4, 1: 3},
        2: {0: 3, 1: 4},
        3: {0: 3, 1: 3},
        4: {0: 4, 1: 4},
    },
}


def run(world: str, actions: Sequence[int]) -> Tuple[int, ...]:
    state = START
    responses = []
    table = TRANSITIONS[world]
    for action in actions:
        state = table[state][action]
        responses.append(OBSERVATION[state])
    return tuple(responses)


def passive_signature(_: str) -> Tuple[int, ...]:
    # Same current appearance in both worlds.
    return (OBSERVATION[START],)


def one_step_signature(world: str) -> Tuple[Tuple[int, int], ...]:
    return tuple((a, run(world, (a,))[0]) for a in ACTIONS)


def marginal_histogram_signature(world: str) -> Tuple[Tuple[int, int], ...]:
    # Deliberately throws away which action sequence produced which response and
    # also throws away temporal order.  It only retains the global response bag.
    counts: Counter[int] = Counter()
    for seq in product(ACTIONS, repeat=2):
        counts.update(run(world, seq))
    return tuple(sorted(counts.items()))


def ordered_predictive_signature(world: str) -> Tuple[Tuple[Tuple[int, ...], Tuple[int, ...]], ...]:
    return tuple((seq, run(world, seq)) for seq in product(ACTIONS, repeat=2))


def exact_signature_accuracy(signature_fn: Callable[[str], Hashable]) -> float:
    """Best exact lookup accuracy under equal prior over the two hidden worlds.

    If signatures collide, no classifier using only that signature can distinguish
    the colliding labels; the optimal exact lookup predicts the majority label.
    """

    groups: Dict[Hashable, list[str]] = defaultdict(list)
    for world in TRANSITIONS:
        groups[signature_fn(world)].append(world)
    correct = sum(1 for _signature, labels in groups.items())
    return correct / len(TRANSITIONS)


def main() -> None:
    worlds = tuple(TRANSITIONS)
    length2 = tuple(product(ACTIONS, repeat=2))

    passive = {w: passive_signature(w) for w in worlds}
    one_step = {w: one_step_signature(w) for w in worlds}
    marginal = {w: marginal_histogram_signature(w) for w in worlds}
    ordered = {w: ordered_predictive_signature(w) for w in worlds}

    result = {
        "gate": "G2_MULTISTEP_COUNTERFACTUALS",
        "worlds": list(worlds),
        "action_sequences": [list(seq) for seq in length2],
        "passive_signatures": {k: list(v) for k, v in passive.items()},
        "one_step_signatures": {
            k: [[a, r] for a, r in v] for k, v in one_step.items()
        },
        "marginal_response_histograms": {
            k: [[response, count] for response, count in v]
            for k, v in marginal.items()
        },
        "ordered_profiles": {
            k: [[list(seq), list(response)] for seq, response in v]
            for k, v in ordered.items()
        },
        "passive_accuracy": exact_signature_accuracy(passive_signature),
        "one_step_accuracy": exact_signature_accuracy(one_step_signature),
        "unordered_marginal_accuracy": exact_signature_accuracy(marginal_histogram_signature),
        "ordered_two_step_predictive_accuracy": exact_signature_accuracy(ordered_predictive_signature),
        "oracle_accuracy": 1.0,
        "classification": (
            "ORDERED_ACTION_CONDITIONED_MULTI_STEP_FUTURES_SEPARATE_HIDDEN_WORLDS_"
            "THAT_PASSIVE_ONE_STEP_AND_UNORDERED_RESPONSE_STATISTICS_CANNOT"
        ),
        "claim_boundary": (
            "Constructed finite-state predictive-state sanity check. It only shows that "
            "temporal action-conditioned structure can contain distinctions erased by "
            "passive, one-step, and unordered summaries; it says nothing about phenomenology."
        ),
    }

    assert passive["X"] == passive["Y"], result
    assert one_step["X"] == one_step["Y"], result
    assert marginal["X"] == marginal["Y"], result
    assert ordered["X"] != ordered["Y"], result
    assert result["passive_accuracy"] == 0.5, result
    assert result["one_step_accuracy"] == 0.5, result
    assert result["unordered_marginal_accuracy"] == 0.5, result
    assert result["ordered_two_step_predictive_accuracy"] == 1.0, result

    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
