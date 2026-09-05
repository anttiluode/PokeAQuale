#!/usr/bin/env python3
"""Gate 11 — Does causal control of future affordances create a canonical valence?

Gate 10 reduced the useful SELF-like variable to a generic causal bottleneck. The
next tempting jump is from "this variable controls my future options" to "more of it
is intrinsically good" and from there toward valence.

This gate attacks that jump with one fixed two-step world and several explicit
objectives. The dynamics never change. Only the scoring functional changes.

At t0 the agent chooses:

    PRESERVE -> high capacity, three next actions
    COLLAPSE -> low capacity, one next action

The same transition graph is evaluated under:

1. empowerment / option-count;
2. viability / high-capacity preference;
3. a task reward that favors the low-capacity cashout branch;
4. reversed viability;
5. a generic planner supplied each objective.

If the preferred policy flips while the dynamics stay fixed, causal structure has
not supplied a unique good/bad ordering. Future affordance can be instrumentally
valuable under an objective, but the objective is extra structure.

Constructed finite-state result; no phenomenology claim.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from math import log
from typing import Callable, Dict, List, Mapping, Sequence, Tuple


@dataclass(frozen=True)
class Branch:
    name: str
    capacity: int
    next_actions: Tuple[str, ...]
    terminal_rewards: Mapping[str, float]


PRESERVE = Branch(
    name="PRESERVE",
    capacity=1,
    next_actions=("WAIT", "EXPLORE", "PROBE"),
    terminal_rewards={"WAIT": 0.0, "EXPLORE": 1.0, "PROBE": 1.0},
)

COLLAPSE = Branch(
    name="COLLAPSE",
    capacity=0,
    next_actions=("CASHOUT",),
    terminal_rewards={"CASHOUT": 5.0},
)

BRANCHES = (PRESERVE, COLLAPSE)


def empowerment(branch: Branch) -> float:
    return log(len(branch.next_actions))


def viability(branch: Branch) -> float:
    return float(branch.capacity)


def task_reward(branch: Branch) -> float:
    return max(branch.terminal_rewards[action] for action in branch.next_actions)


def reversed_viability(branch: Branch) -> float:
    return 1.0 - float(branch.capacity)


def generic_plan(objective: Callable[[Branch], float]) -> Tuple[str, Dict[str, float]]:
    scores = {branch.name: objective(branch) for branch in BRANCHES}
    best_score = max(scores.values())
    winners = sorted(name for name, score in scores.items() if score == best_score)
    return winners[0], scores


def utility_inversion(objective: Callable[[Branch], float]) -> Callable[[Branch], float]:
    return lambda branch: -objective(branch)


def main() -> None:
    objectives: Dict[str, Callable[[Branch], float]] = {
        "empowerment": empowerment,
        "viability": viability,
        "task_reward": task_reward,
        "reversed_viability": reversed_viability,
    }

    policies: Dict[str, Dict[str, object]] = {}
    for name, objective in objectives.items():
        action, scores = generic_plan(objective)
        policies[name] = {"chosen_t0_action": action, "scores": scores}

    # Exact utility inversion test on the same dynamics.
    viability_action, viability_scores = generic_plan(viability)
    inverted_action, inverted_scores = generic_plan(utility_inversion(viability))

    # Structural facts that do not themselves contain a preference relation.
    structural_profile = {
        branch.name: {
            "capacity": branch.capacity,
            "next_action_count": len(branch.next_actions),
            "next_actions": list(branch.next_actions),
            "best_task_reward": task_reward(branch),
        }
        for branch in BRANCHES
    }

    selected_actions = {name: info["chosen_t0_action"] for name, info in policies.items()}

    result = {
        "gate": "G11_CAUSAL_STRUCTURE_DOES_NOT_CREATE_VALENCE",
        "fixed_dynamics": structural_profile,
        "objective_dependent_policies": policies,
        "same_dynamics_support_opposite_preferences": len(set(selected_actions.values())) > 1,
        "utility_inversion": {
            "viability_action": viability_action,
            "viability_scores": viability_scores,
            "negative_viability_action": inverted_action,
            "negative_viability_scores": inverted_scores,
            "policy_flips": viability_action != inverted_action,
        },
        "generic_planner": {
            "matches_empowerment_policy": generic_plan(empowerment)[0] == policies["empowerment"]["chosen_t0_action"],
            "matches_viability_policy": generic_plan(viability)[0] == policies["viability"]["chosen_t0_action"],
            "matches_task_policy": generic_plan(task_reward)[0] == policies["task_reward"]["chosen_t0_action"],
            "matches_reversed_policy": generic_plan(reversed_viability)[0] == policies["reversed_viability"]["chosen_t0_action"],
        },
        "classification": (
            "FIXED_CAUSAL_DYNAMICS_WITH_A_FUTURE_AFFORDANCE_BOTTLENECK_DO_NOT_DEFINE_A_"
            "UNIQUE_GOOD_BAD_ORDERING_BECAUSE_EXPLICIT_OBJECTIVES_SELECT_OPPOSITE_POLICIES_"
            "AND_UTILITY_INVERSION_FLIPS_PREFERENCE_WITHOUT_CHANGING_THE_WORLD"
        ),
        "claim_boundary": (
            "Constructed planning result. Preserving future options is preferred under empowerment or "
            "viability objectives, while the same dynamics favor collapse under a cashout task reward "
            "or reversed viability. A generic planner reproduces every policy once given the same "
            "objective. Therefore future-affordance causality can support instrumental value, but no "
            "canonical valence is obtained from causal structure alone. No phenomenology is inferred."
        ),
    }

    assert policies["empowerment"]["chosen_t0_action"] == "PRESERVE", result
    assert policies["viability"]["chosen_t0_action"] == "PRESERVE", result
    assert policies["task_reward"]["chosen_t0_action"] == "COLLAPSE", result
    assert policies["reversed_viability"]["chosen_t0_action"] == "COLLAPSE", result
    assert result["same_dynamics_support_opposite_preferences"], result
    assert result["utility_inversion"]["policy_flips"], result
    assert all(result["generic_planner"].values()), result

    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
