#!/usr/bin/env python3
"""Gate 12 — Can behavior reveal a unique objective / valence?

Gate 11 showed that fixed causal dynamics do not define a canonical good/bad ordering:
preferences depend on an objective. Gate 12 attacks the obvious escape hatch: perhaps
the organism's behavior reveals the objective.

We construct a tiny two-step episodic decision process. From START the agent chooses
A, B, or C, reaches an intermediate state, then must FINISH at the same terminal T.

Three reward hypotheses are compared:

1. BASE: A > B > C.
2. SHAPED: a potential-based transformation of BASE. Numerical rewards change, but
   every complete START->...->T trajectory gets the same additive offset, so all
   trajectory preferences and the optimal policy are unchanged.
3. ALTERNATE: A remains optimal, but the two off-policy paths reverse order: A > C > B.

A demonstration of the complete optimal policy therefore fits all three hypotheses.
A same-start/same-end preference query between B and C eliminates ALTERNATE, but BASE
and SHAPED remain exactly preference-equivalent. The true numeric reward is not
recoverable from this behavioral vocabulary.

This is standard reward / inverse-RL non-identifiability in a constructed finite MDP.
It is not evidence about felt valence.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Dict, Mapping, Sequence, Tuple


GAMMA = 0.9
START = "START"
TERMINAL = "T"
PATHS = {
    "A": "SA",
    "B": "SB",
    "C": "SC",
}


@dataclass(frozen=True)
class RewardModel:
    name: str
    first_step: Mapping[str, float]
    finish_step: Mapping[str, float]

    def trajectory_return(self, action: str) -> float:
        mid = PATHS[action]
        return self.first_step[action] + GAMMA * self.finish_step[mid]

    def ranking(self) -> Tuple[str, ...]:
        return tuple(
            sorted(PATHS, key=lambda action: (-self.trajectory_return(action), action))
        )

    def optimal_action(self) -> str:
        return self.ranking()[0]


BASE = RewardModel(
    name="BASE",
    first_step={"A": 0.0, "B": 0.0, "C": 0.0},
    finish_step={"SA": 3.0, "SB": 2.0, "SC": 1.0},
)

# A different but policy-equivalent reward that reverses only the two suboptimal paths.
ALTERNATE = RewardModel(
    name="ALTERNATE",
    first_step={"A": 0.0, "B": 0.0, "C": 0.0},
    finish_step={"SA": 3.0, "SB": 1.0, "SC": 2.0},
)

# Potential-based reward shaping: r'(s,a,s') = r + gamma*Phi(s') - Phi(s).
PHI = {
    START: 2.0,
    "SA": -1.0,
    "SB": 0.5,
    "SC": 3.0,
    TERMINAL: 0.0,
}


def make_shaped(base: RewardModel) -> RewardModel:
    first: Dict[str, float] = {}
    finish: Dict[str, float] = {}
    for action, mid in PATHS.items():
        first[action] = (
            base.first_step[action] + GAMMA * PHI[mid] - PHI[START]
        )
        finish[mid] = (
            base.finish_step[mid] + GAMMA * PHI[TERMINAL] - PHI[mid]
        )
    return RewardModel(name="SHAPED", first_step=first, finish_step=finish)


SHAPED = make_shaped(BASE)
MODELS = (BASE, SHAPED, ALTERNATE)


def demonstration_likelihood(model: RewardModel) -> int:
    """Complete deterministic optimal-policy demo: choose A, then FINISH."""
    return int(model.optimal_action() == "A")


def preference(model: RewardModel, left: str, right: str) -> str:
    lval = model.trajectory_return(left)
    rval = model.trajectory_return(right)
    if lval > rval:
        return left
    if rval > lval:
        return right
    return "TIE"


def reward_table(model: RewardModel) -> Dict[str, float]:
    out = {f"START--{action}": value for action, value in model.first_step.items()}
    out.update({f"{mid}--FINISH": value for mid, value in model.finish_step.items()})
    return out


def max_abs_reward_difference(a: RewardModel, b: RewardModel) -> float:
    ta = reward_table(a)
    tb = reward_table(b)
    return max(abs(ta[key] - tb[key]) for key in ta)


def main() -> None:
    returns = {
        model.name: {action: model.trajectory_return(action) for action in PATHS}
        for model in MODELS
    }
    rankings = {model.name: list(model.ranking()) for model in MODELS}
    demonstrations = {model.name: demonstration_likelihood(model) for model in MODELS}

    behavior_consistent = [name for name, ok in demonstrations.items() if ok]

    # Query one off-policy comparison. The oracle/base answer is B > C.
    oracle_query_answer = preference(BASE, "B", "C")
    query_answers = {
        model.name: preference(model, "B", "C") for model in MODELS
    }
    after_query = [
        name for name, answer in query_answers.items() if answer == oracle_query_answer
    ]

    # Potential shaping should add the same constant -Phi(START) to every complete
    # START->mid->T discounted return because Phi(T)=0.
    shaping_offsets = {
        action: SHAPED.trajectory_return(action) - BASE.trajectory_return(action)
        for action in PATHS
    }
    offset_values = tuple(round(value, 12) for value in shaping_offsets.values())
    constant_shaping_offset = len(set(offset_values)) == 1

    full_pairwise_preferences_equal = all(
        preference(BASE, left, right) == preference(SHAPED, left, right)
        for left in PATHS
        for right in PATHS
    )

    result = {
        "gate": "G12_REWARD_NONIDENTIFIABILITY",
        "gamma": GAMMA,
        "trajectory_returns": returns,
        "trajectory_rankings": rankings,
        "complete_optimal_policy_demonstration": {
            "observed_start_action": "A",
            "consistent_reward_models": behavior_consistent,
            "n_consistent_models": len(behavior_consistent),
            "unique_reward_identified": len(behavior_consistent) == 1,
        },
        "off_policy_preference_query": {
            "query": "prefer B-path or C-path from the same START and same terminal T?",
            "oracle_answer": oracle_query_answer,
            "model_answers": query_answers,
            "remaining_models": after_query,
            "n_remaining_models": len(after_query),
        },
        "potential_shaping_stopping_line": {
            "potential": PHI,
            "base_vs_shaped_max_abs_immediate_reward_difference": max_abs_reward_difference(BASE, SHAPED),
            "trajectory_return_offsets": shaping_offsets,
            "constant_offset_for_all_complete_paths": constant_shaping_offset,
            "all_pairwise_complete_path_preferences_identical": full_pairwise_preferences_equal,
            "optimal_policy_identical": BASE.optimal_action() == SHAPED.optimal_action(),
            "numeric_rewards_identical": reward_table(BASE) == reward_table(SHAPED),
        },
        "classification": (
            "A_COMPLETE_OPTIMAL_POLICY_CAN_BE_EXACTLY_COMPATIBLE_WITH_MULTIPLE_DISTINCT_REWARD_"
            "FUNCTIONS_AND_AN_OFF_POLICY_PREFERENCE_QUERY_CAN_NARROW_THE_SET_BUT_POTENTIAL_BASED_"
            "REWARD_SHAPING_REMAINS_BEHAVIORALLY_AND_PREFERENCE_EQUIVALENT_FOR_ALL_AVAILABLE_"
            "SAME_START_SAME_TERMINAL_TRAJECTORIES_SO_NUMERIC_VALUE_ORIGIN_IS_NOT_IDENTIFIABLE"
        ),
        "claim_boundary": (
            "Constructed inverse-reward sanity result. Behavior constrains an equivalence class of "
            "objectives rather than revealing a unique numerical reward. Extra preference evidence can "
            "remove some policy-equivalent alternatives, but the base and potential-shaped rewards remain "
            "indistinguishable under every supplied complete-path preference while assigning different "
            "immediate rewards. This is reward non-identifiability, not evidence about subjective valence."
        ),
    }

    # All reward hypotheses explain the full optimal policy demonstration.
    assert behavior_consistent == ["BASE", "SHAPED", "ALTERNATE"], result
    assert not result["complete_optimal_policy_demonstration"]["unique_reward_identified"], result

    # Query adds evidence: alternate is removed, but the shaping equivalence survives.
    assert oracle_query_answer == "B", result
    assert query_answers["ALTERNATE"] == "C", result
    assert after_query == ["BASE", "SHAPED"], result

    # Strong stopping line: the two remaining rewards are numerically different but
    # preserve the full preference geometry available in this toy.
    assert max_abs_reward_difference(BASE, SHAPED) > 0.0, result
    assert constant_shaping_offset, result
    assert full_pairwise_preferences_equal, result
    assert BASE.ranking() == SHAPED.ranking() == ("A", "B", "C"), result
    assert BASE.optimal_action() == SHAPED.optimal_action() == "A", result

    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
