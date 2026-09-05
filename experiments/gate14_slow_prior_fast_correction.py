#!/usr/bin/env python3
"""Gate 14 — Slow history tunes probe order; fast intervention preserves correction.

After G13 separated slow population filtering from fast within-lifetime control, this
gate turns that timescale split into a constructive mechanism.

Exactly one of V0, V1, V2 controls the current episode's future affordance. A probe of
Vi returns 1 iff Vi is the driver. After two negative probes the third driver is known
by elimination, so no third paid intervention is required.

Agents:

FIXED_PRIOR_ONLY
    Guess the historically most common driver. Zero probe cost, brittle under shift.

UNIFORM_ACTIVE
    No historical prior. Randomizes probe order uniformly. Always correct, expected
    cost 5/3 probes for three candidates with third-by-elimination.

SLOW_PRIOR_FAST_CORRECTION
    Probe candidates in descending historical frequency. Always continue / infer on
    contradiction, so the prior controls cost, not truth.

ORACLE_ORDER
    Knows the current driver frequencies and uses their optimal descending order.

The environment shifts from V1-dominant to V2-dominant. The hybrid keeps 100% causal
identification immediately after the shift but temporarily pays extra probes. After a
slow prior update it recovers oracle probe cost. This is ordinary sequential testing /
active diagnosis, not a consciousness result.
"""

from __future__ import annotations

import json
from itertools import permutations
from typing import Dict, Iterable, Mapping, Sequence, Tuple


DRIVERS = ("V0", "V1", "V2")
PRE = {"V0": 0.2, "V1": 0.7, "V2": 0.1}
POST = {"V0": 0.2, "V1": 0.1, "V2": 0.7}


def validate_distribution(dist: Mapping[str, float]) -> None:
    assert set(dist) == set(DRIVERS), dist
    assert abs(sum(dist.values()) - 1.0) < 1e-12, dist
    assert all(value >= 0.0 for value in dist.values()), dist


def order_from_prior(prior: Mapping[str, float]) -> Tuple[str, ...]:
    """Descending probability; lexical tie-break only for determinism."""
    return tuple(sorted(DRIVERS, key=lambda d: (-prior[d], d)))


def paid_probes(driver: str, order: Sequence[str]) -> int:
    """Probe until positive, or infer the third candidate after two negatives."""
    assert tuple(sorted(order)) == tuple(sorted(DRIVERS)), order
    position = order.index(driver)
    return min(position + 1, len(DRIVERS) - 1)


def expected_cost(dist: Mapping[str, float], order: Sequence[str]) -> float:
    return sum(dist[driver] * paid_probes(driver, order) for driver in DRIVERS)


def identification_accuracy(order: Sequence[str]) -> float:
    # The active procedure is exhaustive up to elimination and hence exact for every
    # possible driver in this deterministic toy.
    recovered = 0
    for driver in DRIVERS:
        probes = []
        found = None
        for candidate in order[:2]:
            response = int(candidate == driver)
            probes.append((candidate, response))
            if response:
                found = candidate
                break
        if found is None:
            tested = {candidate for candidate, _ in probes}
            found = next(candidate for candidate in DRIVERS if candidate not in tested)
        recovered += int(found == driver)
    return recovered / len(DRIVERS)


def uniform_random_order_expected_cost(dist: Mapping[str, float]) -> float:
    orders = tuple(permutations(DRIVERS))
    return sum(expected_cost(dist, order) for order in orders) / len(orders)


def fixed_prior_accuracy(dist: Mapping[str, float], prior: Mapping[str, float]) -> float:
    guess = order_from_prior(prior)[0]
    return dist[guess]


def best_order(dist: Mapping[str, float]) -> Tuple[str, ...]:
    return min(permutations(DRIVERS), key=lambda order: (expected_cost(dist, order), order))


def evaluate(dist: Mapping[str, float], prior: Mapping[str, float]) -> Dict[str, object]:
    prior_order = order_from_prior(prior)
    oracle_order = best_order(dist)
    return {
        "driver_distribution": dict(dist),
        "fixed_prior_only": {
            "guess": prior_order[0],
            "accuracy": fixed_prior_accuracy(dist, prior),
            "expected_paid_probes": 0.0,
        },
        "uniform_active": {
            "accuracy": 1.0,
            "expected_paid_probes": uniform_random_order_expected_cost(dist),
        },
        "slow_prior_fast_correction": {
            "probe_order": list(prior_order),
            "accuracy": identification_accuracy(prior_order),
            "expected_paid_probes": expected_cost(dist, prior_order),
        },
        "oracle_order": {
            "probe_order": list(oracle_order),
            "accuracy": identification_accuracy(oracle_order),
            "expected_paid_probes": expected_cost(dist, oracle_order),
        },
    }


def main() -> None:
    validate_distribution(PRE)
    validate_distribution(POST)

    pre = evaluate(PRE, PRE)
    immediate_post = evaluate(POST, PRE)  # stale slow prior
    adapted_post = evaluate(POST, POST)   # slow prior updated

    hybrid_pre_cost = pre["slow_prior_fast_correction"]["expected_paid_probes"]
    uniform_pre_cost = pre["uniform_active"]["expected_paid_probes"]
    hybrid_shift_cost = immediate_post["slow_prior_fast_correction"]["expected_paid_probes"]
    uniform_shift_cost = immediate_post["uniform_active"]["expected_paid_probes"]
    hybrid_adapted_cost = adapted_post["slow_prior_fast_correction"]["expected_paid_probes"]
    oracle_adapted_cost = adapted_post["oracle_order"]["expected_paid_probes"]

    result = {
        "gate": "G14_SLOW_PRIOR_FAST_CORRECTION",
        "pre_shift": pre,
        "immediately_after_shift_with_stale_prior": immediate_post,
        "after_slow_prior_update": adapted_post,
        "summary": {
            "hybrid_pre_shift_probe_saving_vs_uniform": uniform_pre_cost - hybrid_pre_cost,
            "hybrid_immediate_shift_extra_cost_vs_uniform": hybrid_shift_cost - uniform_shift_cost,
            "hybrid_accuracy_immediately_after_shift": immediate_post["slow_prior_fast_correction"]["accuracy"],
            "fixed_prior_accuracy_immediately_after_shift": immediate_post["fixed_prior_only"]["accuracy"],
            "hybrid_adapted_cost_matches_oracle": abs(hybrid_adapted_cost - oracle_adapted_cost) < 1e-12,
        },
        "classification": (
            "A_SLOW_EMPIRICAL_PRIOR_CAN_REDUCE_CAUSAL_IDENTIFICATION_PROBE_COST_IN_RECURRENT_"
            "ENVIRONMENTS_WHILE_FAST_COUNTERFACTUAL_CORRECTION_PRESERVES_PERFECT_ACCURACY_"
            "UNDER_DISTRIBUTION_SHIFT_AT_A_TEMPORARY_COST_AND_SLOW_RELEARNING_RESTORES_ORACLE_ORDER"
        ),
        "claim_boundary": (
            "Constructed sequential-testing result. Historical frequency can compile a cheaper ordering "
            "of interventions without being allowed to dictate the answer: fast probes and elimination "
            "still determine the current causal driver. The hybrid is temporarily more expensive than "
            "uniform search after a distribution shift but remains accurate, then recovers oracle ordering "
            "after the prior updates. This is active diagnosis / Bayesian-style search economics, not qualia."
        ),
    }

    # Expected exact costs in this three-candidate toy.
    assert abs(uniform_pre_cost - (5.0 / 3.0)) < 1e-12, result
    assert abs(hybrid_pre_cost - 1.3) < 1e-12, result
    assert hybrid_pre_cost < uniform_pre_cost, result

    # Fixed prior is cheap but brittle; hybrid remains exact on the very first shifted episode.
    assert abs(immediate_post["fixed_prior_only"]["accuracy"] - 0.1) < 1e-12, result
    assert immediate_post["slow_prior_fast_correction"]["accuracy"] == 1.0, result
    assert abs(hybrid_shift_cost - 1.9) < 1e-12, result
    assert hybrid_shift_cost > uniform_shift_cost, result

    # Slow update changes only probe ordering and restores the cheap 1.3-probe regime.
    assert adapted_post["slow_prior_fast_correction"]["probe_order"] == ["V2", "V0", "V1"], result
    assert adapted_post["slow_prior_fast_correction"]["accuracy"] == 1.0, result
    assert abs(hybrid_adapted_cost - 1.3) < 1e-12, result
    assert abs(hybrid_adapted_cost - oracle_adapted_cost) < 1e-12, result

    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
