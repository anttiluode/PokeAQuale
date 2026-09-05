#!/usr/bin/env python3
"""Gate 3 — Owned poke versus matched external perturbation.

This gate isolates what efference/action binding can and cannot add.

Scenario A (operationally separable):
- SELF and WORLD episodes have the same sensory-event statistics;
- both contain exactly one outgoing command and one sensory event;
- command times are marginally uniform in both classes;
- only the *lag relation* differs: SELF has the learned command->consequence lag,
  WORLD has an unrelated decoy command while an external perturbation causes the
  same sensory event.

A bound command/consequence transcript can separate the stories; sensory-only and
unordered event bags cannot.

Scenario B (perfect causal mimic):
- the external perturbation is synchronized so perfectly that command and sensory
  transcripts are identical to the SELF story.

Then no operational classifier using the supplied transcript can distinguish the
causal stories.  The framework must abstain rather than invent a hidden Self fact.

This is a constructed causal-attribution sanity check, not a phenomenology result.
"""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from typing import Callable, Dict, Hashable, Iterable, List, Sequence, Tuple


N_TIMES = 8
LEARNED_LAG = 2
DECOY_LAG = 3
CAUSES = ("SELF", "WORLD")


def one_hot(time_index: int) -> Tuple[int, ...]:
    return tuple(1 if t == time_index else 0 for t in range(N_TIMES))


def build_episodes(perfect_mimic: bool = False) -> List[dict]:
    episodes: List[dict] = []
    for response_time in range(N_TIMES):
        for cause in CAUSES:
            if cause == "SELF" or perfect_mimic:
                command_time = (response_time - LEARNED_LAG) % N_TIMES
            else:
                command_time = (response_time - DECOY_LAG) % N_TIMES

            episodes.append(
                {
                    "cause": cause,
                    "response_time": response_time,
                    "command_time": command_time,
                    "sensory": one_hot(response_time),
                    "efference": one_hot(command_time),
                }
            )
    return episodes


def lag(episode: dict) -> int:
    return (episode["response_time"] - episode["command_time"]) % N_TIMES


def sensory_signature(episode: dict) -> Hashable:
    return episode["sensory"]


def unordered_event_bag_signature(episode: dict) -> Hashable:
    # Throws away time and binding.  Every episode contains one outgoing command
    # and one sensory event.
    return (
        sum(episode["efference"]),
        sum(episode["sensory"]),
    )


def bound_lag_signature(episode: dict) -> Hashable:
    # The minimal relational feature: when did the sensory event occur relative
    # to the command the agent knows it issued?
    return lag(episode)


def best_signature_accuracy(episodes: Sequence[dict], signature_fn: Callable[[dict], Hashable]) -> float:
    groups: Dict[Hashable, Counter[str]] = defaultdict(Counter)
    for episode in episodes:
        groups[signature_fn(episode)][episode["cause"]] += 1
    correct = sum(max(counts.values()) for counts in groups.values())
    return correct / len(episodes)


def marginal_time_histogram(episodes: Sequence[dict], cause: str, key: str) -> Tuple[int, ...]:
    counts = Counter(ep[key] for ep in episodes if ep["cause"] == cause)
    return tuple(counts[t] for t in range(N_TIMES))


def main() -> None:
    separable = build_episodes(perfect_mimic=False)
    mimic = build_episodes(perfect_mimic=True)

    command_hist_self = marginal_time_histogram(separable, "SELF", "command_time")
    command_hist_world = marginal_time_histogram(separable, "WORLD", "command_time")
    response_hist_self = marginal_time_histogram(separable, "SELF", "response_time")
    response_hist_world = marginal_time_histogram(separable, "WORLD", "response_time")

    result = {
        "gate": "G3_OWNED_VS_EXTERNAL_POKE",
        "n_times": N_TIMES,
        "learned_action_consequence_lag": LEARNED_LAG,
        "decoy_command_lag": DECOY_LAG,
        "separable_scenario": {
            "sensory_only_accuracy": best_signature_accuracy(separable, sensory_signature),
            "unordered_event_bag_accuracy": best_signature_accuracy(separable, unordered_event_bag_signature),
            "bound_efference_lag_accuracy": best_signature_accuracy(separable, bound_lag_signature),
            "self_lags": sorted({lag(ep) for ep in separable if ep["cause"] == "SELF"}),
            "world_lags": sorted({lag(ep) for ep in separable if ep["cause"] == "WORLD"}),
            "self_command_time_histogram": list(command_hist_self),
            "world_command_time_histogram": list(command_hist_world),
            "self_response_time_histogram": list(response_hist_self),
            "world_response_time_histogram": list(response_hist_world),
        },
        "perfect_mimic_scenario": {
            "sensory_only_accuracy": best_signature_accuracy(mimic, sensory_signature),
            "bound_efference_lag_accuracy": best_signature_accuracy(mimic, bound_lag_signature),
            "full_transcript_accuracy": best_signature_accuracy(
                mimic, lambda ep: (ep["efference"], ep["sensory"])
            ),
        },
        "classification": (
            "OWNED_ACTION_RESPONSE_BINDING_ADDS_CAUSAL_ATTRIBUTION_WHEN_CAUSAL_"
            "STORIES_DIFFER_OPERATIONALLY_BUT_PERFECT_EXTERNAL_MIMICS_REMAIN_"
            "INDISTINGUISHABLE"
        ),
        "claim_boundary": (
            "Constructed causal-attribution example. Efference supplies an internally "
            "privileged action/consequence relation only when that relation differs in "
            "the available data. Perfectly matched causal stories remain operationally "
            "equivalent; no Self or phenomenology is inferred."
        ),
    }

    assert command_hist_self == command_hist_world, result
    assert response_hist_self == response_hist_world, result
    assert result["separable_scenario"]["sensory_only_accuracy"] == 0.5, result
    assert result["separable_scenario"]["unordered_event_bag_accuracy"] == 0.5, result
    assert result["separable_scenario"]["bound_efference_lag_accuracy"] == 1.0, result
    assert result["perfect_mimic_scenario"]["sensory_only_accuracy"] == 0.5, result
    assert result["perfect_mimic_scenario"]["bound_efference_lag_accuracy"] == 0.5, result
    assert result["perfect_mimic_scenario"]["full_transcript_accuracy"] == 0.5, result

    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
