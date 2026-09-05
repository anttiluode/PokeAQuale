#!/usr/bin/env python3
"""Gate 4 — Cached counterfactuals do not create a missing observation.

The hoped-for story was:

    first encounter: ambiguous -> poke -> remember relation
    later encounter: memory -> immediate perception

This gate attacks that jump.

Eight hidden qualities arrive repeatedly.  The passive sensor reveals only a coarse
pair ID, leaving two qualities exactly aliased.  One reversible poke reveals the
missing within-pair bit.

Three facts are tested:

1. A library of remembered action/response relations still needs the current poke
   when the passive state remains exactly aliased and there is no recurrence key.
2. If a stable object key *is* supplied, an ordinary lookup cache avoids the poke
   just as well as any richer relational cache.
3. If that arbitrary key is remapped by a new representation generation, an
   unversioned lookup can become confidently wrong; generation-aware invalidation
   fixes it by repurchasing evidence.

So memory can amortize sensing only through some reusable current handle: a stable
key, a changed passive representation, or changed structure.  Remembering the old
counterfactual by itself does not manufacture present evidence.

Constructed toy result; no phenomenology claim.
"""

from __future__ import annotations

import json
from typing import Dict, Iterable, List, Tuple


N_QUALITIES = 8
ROUNDS_PER_GENERATION = 5


def passive_group(quality: int) -> int:
    return quality // 2


def poke_response(quality: int) -> int:
    return quality % 2


def decode(group: int, response: int) -> int:
    return 2 * group + response


def key_generation_0(quality: int) -> int:
    # Arbitrary bijection over 0..7.
    return (5 * quality + 3) % N_QUALITIES


def key_generation_1(quality: int) -> int:
    # Same objects, arbitrary coordinate/key remap.  Every key shifts, so blindly
    # reusing the old key->quality map is wrong for every quality.
    return (key_generation_0(quality) + 1) % N_QUALITIES


def episodes(rounds: int = ROUNDS_PER_GENERATION) -> List[int]:
    return [q for _ in range(rounds) for q in range(N_QUALITIES)]


def passive_only_accuracy(stream: Iterable[int]) -> float:
    # Best balanced-prior deterministic guess from pair ID alone: choose member 0.
    stream = list(stream)
    correct = sum((2 * passive_group(q)) == q for q in stream)
    return correct / len(stream)


def no_memory(stream: Iterable[int]) -> Tuple[float, int]:
    stream = list(stream)
    correct = 0
    pokes = 0
    for q in stream:
        response = poke_response(q)
        pokes += 1
        pred = decode(passive_group(q), response)
        correct += pred == q
    return correct / len(stream), pokes


def relational_library_without_key(stream: Iterable[int]) -> Tuple[float, int, int]:
    """Remember every discovered group/action/response relation.

    The library becomes complete after the first eight encounters, but because the
    current passive cue still identifies only a pair, the current response bit must
    still be purchased every episode.
    """

    stream = list(stream)
    library: Dict[Tuple[int, int], int] = {}
    correct = 0
    pokes = 0
    learned_entries = 0

    for q in stream:
        group = passive_group(q)
        response = poke_response(q)
        pokes += 1
        key = (group, response)
        if key not in library:
            learned_entries += 1
        library[key] = q
        pred = library[key]
        correct += pred == q

    return correct / len(stream), pokes, learned_entries


def lookup_with_stable_key(stream: Iterable[int], key_fn) -> Tuple[float, int, Dict[int, int]]:
    stream = list(stream)
    cache: Dict[int, int] = {}
    correct = 0
    pokes = 0

    for q in stream:
        key = key_fn(q)
        if key not in cache:
            # The cache miss still needs the diagnostic poke to identify the object.
            response = poke_response(q)
            pokes += 1
            cache[key] = decode(passive_group(q), response)
        pred = cache[key]
        correct += pred == q

    return correct / len(stream), pokes, cache


def stale_lookup_after_key_remap(stream: Iterable[int], old_cache: Dict[int, int]) -> float:
    stream = list(stream)
    correct = 0
    for q in stream:
        pred = old_cache[key_generation_1(q)]
        correct += pred == q
    return correct / len(stream)


def main() -> None:
    phase0 = episodes()
    phase1 = episodes()

    passive_acc = passive_only_accuracy(phase0)
    no_mem_acc, no_mem_pokes = no_memory(phase0)
    relational_acc, relational_pokes, relational_entries = relational_library_without_key(phase0)
    lookup_acc, lookup_pokes, cache0 = lookup_with_stable_key(phase0, key_generation_0)

    stale_lookup_acc = stale_lookup_after_key_remap(phase1, cache0)
    refreshed_lookup_acc, refreshed_lookup_pokes, _cache1 = lookup_with_stable_key(
        phase1, key_generation_1
    )
    relational_phase1_acc, relational_phase1_pokes, _ = relational_library_without_key(phase1)

    result = {
        "gate": "G4_MEMORY_DOES_NOT_CREATE_OBSERVATION",
        "n_qualities": N_QUALITIES,
        "episodes_per_generation": len(phase0),
        "phase0_stable_key": {
            "passive_only_accuracy": passive_acc,
            "no_memory": {"accuracy": no_mem_acc, "paid_pokes": no_mem_pokes},
            "counterfactual_library_without_recurrence_key": {
                "accuracy": relational_acc,
                "paid_pokes": relational_pokes,
                "learned_relation_entries": relational_entries,
            },
            "ordinary_lookup_with_stable_key": {
                "accuracy": lookup_acc,
                "paid_pokes": lookup_pokes,
                "poke_reduction_vs_no_memory": 1.0 - lookup_pokes / no_mem_pokes,
            },
        },
        "phase1_key_remap": {
            "unversioned_old_lookup_accuracy": stale_lookup_acc,
            "unversioned_old_lookup_paid_new_pokes": 0,
            "generation_aware_flush_and_relearn": {
                "accuracy": refreshed_lookup_acc,
                "paid_pokes": refreshed_lookup_pokes,
            },
            "counterfactual_library_without_recurrence_key": {
                "accuracy": relational_phase1_acc,
                "paid_pokes": relational_phase1_pokes,
            },
        },
        "classification": (
            "CACHED_COUNTERFACTUALS_ALONE_DO_NOT_REMOVE_PRESENT_PASSIVE_ALIASING_"
            "WHILE_A_STABLE_KEY_REDUCES_POKES_BY_ORDINARY_LOOKUP_AND_KEY_REMAP_"
            "REQUIRES_INVALIDATION_OR_REPURCHASE"
        ),
        "claim_boundary": (
            "Negative constructed result. Remembered action/response structure can "
            "identify a state once a current discriminating response is available, but "
            "it cannot infer which exactly aliased state is present for free. Immediate "
            "perception therefore requires a reusable current key or a changed passive/"
            "structural representation; this says nothing about subjective experience."
        ),
    }

    assert passive_acc == 0.5, result
    assert no_mem_acc == 1.0 and no_mem_pokes == 40, result
    assert relational_acc == 1.0 and relational_pokes == no_mem_pokes, result
    assert relational_entries == N_QUALITIES, result
    assert lookup_acc == 1.0 and lookup_pokes == N_QUALITIES, result
    assert result["phase0_stable_key"]["ordinary_lookup_with_stable_key"]["poke_reduction_vs_no_memory"] == 0.8, result
    assert stale_lookup_acc == 0.0, result
    assert refreshed_lookup_acc == 1.0 and refreshed_lookup_pokes == N_QUALITIES, result
    assert relational_phase1_acc == 1.0 and relational_phase1_pokes == no_mem_pokes, result

    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
