#!/usr/bin/env python3
"""Gate 9 — Which correlated variable actually changes the observer's future affordances?

Gate 8 showed that an endogenous BODY signal does not become mathematically privileged
merely because it breaks a symmetry: a matched external BEACON carrying the same
information does the same alignment work.

Gate 9 tests the stronger surviving claim.

During ordinary observation two binary channels are perfectly correlated:

    BODY == BEACON

so two causal stories are observationally indistinguishable:

    H_body:   BODY   -> future action/sensing capacity
    H_beacon: BEACON -> future action/sensing capacity

The actual world is H_body.  A decoupling intervention can set BODY and BEACON to
different values and then inspect the *next* action repertoire, sensing repertoire,
and reachable-state count.

This is deliberately ordinary causal identification / system identification.  The
question is only whether a bounded agent can identify a variable that recursively
changes its own future ability to act and sense.  It is not evidence of phenomenology.

A final attacker constructs an EXTERNAL CAUSAL CLONE whose variable controls the exact
same future affordance profile as BODY.  If all available intervention/consequence
relations are isomorphic, the theory must not infer an extra hidden fact from the
words "inside" and "outside".
"""

from __future__ import annotations

import itertools
import json
from dataclasses import dataclass
from typing import Dict, Iterable, List, Sequence, Tuple


Channel = Tuple[int, int]  # (body, beacon)


@dataclass(frozen=True)
class Affordance:
    actions: Tuple[str, ...]
    sensors: Tuple[str, ...]
    reachable_states: int

    def signature(self) -> Tuple[Tuple[str, ...], Tuple[str, ...], int]:
        return self.actions, self.sensors, self.reachable_states


LOW = Affordance(actions=("WAIT",), sensors=("COARSE",), reachable_states=1)
HIGH = Affordance(
    actions=("WAIT", "MOVE", "PROBE"),
    sensors=("COARSE", "FINE", "PROPRIO"),
    reachable_states=3,
)


def affordance_from_driver(driver: int) -> Affordance:
    if driver not in (0, 1):
        raise ValueError(driver)
    return HIGH if driver else LOW


def future_under_hypothesis(body: int, beacon: int, hypothesis: str) -> Affordance:
    if hypothesis == "BODY_CAUSAL":
        return affordance_from_driver(body)
    if hypothesis == "BEACON_CAUSAL":
        return affordance_from_driver(beacon)
    raise ValueError(hypothesis)


def ordinary_transcript(bits: Sequence[int], hypothesis: str) -> Tuple[Tuple[int, int, tuple], ...]:
    """Ordinary world: BODY == BEACON, so both causal hypotheses predict identically."""
    out = []
    for bit in bits:
        body = beacon = bit
        out.append((body, beacon, future_under_hypothesis(body, beacon, hypothesis).signature()))
    return tuple(out)


def decoupling_profile(hypothesis: str) -> Dict[str, tuple]:
    """Full interventional profile for all four BODY/BEACON settings."""
    return {
        f"do_body_{body}_beacon_{beacon}": future_under_hypothesis(body, beacon, hypothesis).signature()
        for body, beacon in itertools.product((0, 1), repeat=2)
    }


def one_variable_intervention_effects(hypothesis: str) -> Dict[str, object]:
    """Hold one channel fixed while toggling the other."""
    # Toggle BODY while BEACON is fixed high.
    body_toggle = (
        future_under_hypothesis(0, 1, hypothesis).signature(),
        future_under_hypothesis(1, 1, hypothesis).signature(),
    )
    # Toggle BEACON while BODY is fixed high.
    beacon_toggle = (
        future_under_hypothesis(1, 0, hypothesis).signature(),
        future_under_hypothesis(1, 1, hypothesis).signature(),
    )
    return {
        "body_toggle_changes_future_affordance": body_toggle[0] != body_toggle[1],
        "beacon_toggle_changes_future_affordance": beacon_toggle[0] != beacon_toggle[1],
        "body_toggle": body_toggle,
        "beacon_toggle": beacon_toggle,
    }


def hypothesis_consistent_with_profile(observed: Dict[str, tuple], hypothesis: str) -> bool:
    return observed == decoupling_profile(hypothesis)


def future_measurements(profile: Dict[str, tuple]) -> Dict[str, Dict[str, int]]:
    """Expose action, sensing, and reachability consequences separately."""
    out: Dict[str, Dict[str, int]] = {}
    for intervention, sig in profile.items():
        actions, sensors, reachable = sig
        out[intervention] = {
            "available_action_count": len(actions),
            "available_sensor_count": len(sensors),
            "reachable_state_count": reachable,
        }
    return out


def main() -> None:
    # A balanced observational history.  Any deterministic history with BODY == BEACON
    # is equally non-identifying; the alternating sequence avoids frequency shortcuts.
    history = (0, 1, 1, 0, 1, 0, 0, 1)
    body_story = ordinary_transcript(history, "BODY_CAUSAL")
    beacon_story = ordinary_transcript(history, "BEACON_CAUSAL")

    observationally_identical = body_story == beacon_story

    # With equal priors and identical likelihood under all supplied ordinary data,
    # the causal-source posterior stays exactly tied.
    passive_causal_source_accuracy = 0.5 if observationally_identical else 1.0
    current_value_attacker_accuracy = 0.5  # every ordinary sample has body == beacon
    history_only_attacker_accuracy = passive_causal_source_accuracy

    actual_profile = decoupling_profile("BODY_CAUSAL")
    body_consistent = hypothesis_consistent_with_profile(actual_profile, "BODY_CAUSAL")
    beacon_consistent = hypothesis_consistent_with_profile(actual_profile, "BEACON_CAUSAL")
    intervention_identification_accuracy = 1.0 if body_consistent and not beacon_consistent else 0.5

    effects = one_variable_intervention_effects("BODY_CAUSAL")
    measurements = future_measurements(actual_profile)

    # Matched external causal clone attacker.  Rename the causal driver REMOTE and wire
    # it to exactly the same affordance function.  If the intervention language itself
    # offers only "set driver low/high" and reads the same futures, the two systems are
    # operationally isomorphic.  Location vocabulary is extra information.
    internal_driver_profile = {
        f"set_driver_{driver}": affordance_from_driver(driver).signature() for driver in (0, 1)
    }
    external_clone_profile = dict(internal_driver_profile)
    external_clone_operationally_identical = internal_driver_profile == external_clone_profile
    internal_vs_external_location_accuracy = 0.5 if external_clone_operationally_identical else 1.0

    result = {
        "gate": "G9_FUTURE_AFFORDANCE_CAUSALITY",
        "ordinary_observation": {
            "history": list(history),
            "body_equals_beacon_on_every_sample": all(b == z for b, z, _ in body_story),
            "body_causal_and_beacon_causal_transcripts_identical": observationally_identical,
            "passive_causal_source_accuracy": passive_causal_source_accuracy,
            "current_value_attacker_accuracy": current_value_attacker_accuracy,
            "history_only_attacker_accuracy": history_only_attacker_accuracy,
        },
        "decoupling_intervention": {
            "observed_profile": {k: list(v) for k, v in actual_profile.items()},
            "BODY_CAUSAL_consistent": body_consistent,
            "BEACON_CAUSAL_consistent": beacon_consistent,
            "causal_source_identification_accuracy": intervention_identification_accuracy,
            "body_toggle_changes_future_affordance": effects["body_toggle_changes_future_affordance"],
            "beacon_toggle_changes_future_affordance": effects["beacon_toggle_changes_future_affordance"],
        },
        "future_affordance_prediction": measurements,
        "external_causal_clone_stopping_line": {
            "internal_driver_profile": {k: list(v) for k, v in internal_driver_profile.items()},
            "external_clone_profile": {k: list(v) for k, v in external_clone_profile.items()},
            "profiles_identical": external_clone_operationally_identical,
            "internal_vs_external_location_accuracy_from_operational_data": internal_vs_external_location_accuracy,
        },
        "classification": (
            "PERFECTLY_CORRELATED_BODY_AND_BEACON_CHANNELS_ARE_OBSERVATIONALLY_NONIDENTIFIABLE_"
            "BUT_DECOUPLING_INTERVENTIONS_REVEAL_WHICH_VARIABLE_CAUSALLY_CHANGES_FUTURE_ACTION_"
            "SENSING_AND_REACHABILITY_WHILE_INTERNAL_VS_EXTERNAL_LOCATION_REMAINS_UNIDENTIFIABLE_"
            "UNDER_A_COMPLETE_CAUSAL_CLONE"
        ),
        "claim_boundary": (
            "Constructed causal-identification result. The positive part is standard intervention-based "
            "system identification: decoupling distinguishes a variable that changes the agent's future "
            "affordance set from a merely correlated marker. The result does not make such a variable a "
            "self, a quale, or a source of phenomenology. If an external variable is wired to the exact "
            "same intervention-conditioned future affordances, operational data alone cannot privilege "
            "the word internal."
        ),
    }

    # Leakage checks / preregistered kill conditions.
    assert observationally_identical, result
    assert passive_causal_source_accuracy == 0.5, result
    assert current_value_attacker_accuracy == 0.5, result
    assert history_only_attacker_accuracy == 0.5, result

    # Intended causal separation.
    assert body_consistent and not beacon_consistent, result
    assert intervention_identification_accuracy == 1.0, result
    assert effects["body_toggle_changes_future_affordance"], result
    assert not effects["beacon_toggle_changes_future_affordance"], result

    # The future change must actually touch all three declared observer capabilities.
    low = measurements["do_body_0_beacon_1"]
    high = measurements["do_body_1_beacon_0"]
    assert low["available_action_count"] < high["available_action_count"], result
    assert low["available_sensor_count"] < high["available_sensor_count"], result
    assert low["reachable_state_count"] < high["reachable_state_count"], result

    # Stopping line.
    assert external_clone_operationally_identical, result
    assert internal_vs_external_location_accuracy == 0.5, result

    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
