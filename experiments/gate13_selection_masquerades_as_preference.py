#!/usr/bin/env python3
"""Gate 13 — Can evolutionary selection masquerade as an intrinsic objective?

Gate 12 showed that behavior need not identify a unique reward. A common escape is to
say that survival/evolution supplies the objective. Gate 13 separates two mechanisms
that can produce the same mature survival-oriented action distribution:

A. EXPLICIT PLANNER
   observes which action currently preserves viability and chooses it, with 10%
   execution noise.

B. SELECTION ONLY
   individuals are inherited fixed-action controllers with no reward, utility,
   learning, or within-lifetime adaptation. The currently surviving controller type
   reproduces with 10% mutation into the opposite type.

At steady state in a PRESERVE-favoring regime, both populations are 90% PRESERVE and
10% COLLAPSE. A snapshot therefore cannot tell whether the behavior came from an
agent objective or population filtering.

Then the survival mapping is reversed. The explicit planner changes immediately. The
selection-only population does not: its existing individuals keep their inherited
actions, suffer a one-generation survival crash, and only the next generation shifts
through differential survival + mutation.

This is a toy population-genetics / control distinction. Evolutionary fitness is not
felt valence, and population-level adaptation is not proof of a represented objective.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Dict, Mapping, Tuple


ACTIONS = ("PRESERVE", "COLLAPSE")
N = 100
ERROR_OR_MUTATION = 0.10


@dataclass(frozen=True)
class Regime:
    name: str
    surviving_action: str


OLD = Regime("PRESERVE_FAVORED", "PRESERVE")
REVERSED = Regime("COLLAPSE_FAVORED", "COLLAPSE")


def opposite(action: str) -> str:
    if action == "PRESERVE":
        return "COLLAPSE"
    if action == "COLLAPSE":
        return "PRESERVE"
    raise ValueError(action)


def noisy_distribution(target: str, rate: float = ERROR_OR_MUTATION) -> Dict[str, int]:
    wrong = int(round(N * rate))
    right = N - wrong
    return {target: right, opposite(target): wrong}


def planner_distribution(regime: Regime) -> Dict[str, int]:
    """Within-lifetime planner reacts to current survival consequences immediately."""
    return noisy_distribution(regime.surviving_action)


def selection_offspring(parent_action: str) -> Dict[str, int]:
    """Fixed inherited controller + mutation. No objective exists inside an individual."""
    return noisy_distribution(parent_action)


def survive(population: Mapping[str, int], regime: Regime) -> Dict[str, int]:
    return {
        action: count if action == regime.surviving_action else 0
        for action, count in population.items()
    }


def survival_fraction(population: Mapping[str, int], regime: Regime) -> float:
    return sum(survive(population, regime).values()) / sum(population.values())


def normalized(population: Mapping[str, int]) -> Dict[str, float]:
    total = sum(population.values())
    if total == 0:
        return {action: 0.0 for action in ACTIONS}
    return {action: population.get(action, 0) / total for action in ACTIONS}


def selected_parent_action(survivors: Mapping[str, int]) -> str:
    nonzero = [action for action, count in survivors.items() if count > 0]
    assert len(nonzero) == 1, survivors
    return nonzero[0]


def main() -> None:
    # Old-regime steady snapshot. Selection-only descended from PRESERVE survivors;
    # explicit planner targets PRESERVE. Their observed action distributions match.
    selection_old = selection_offspring("PRESERVE")
    planner_old = planner_distribution(OLD)
    snapshot_identical = selection_old == planner_old

    # Environmental reversal occurs before these already-produced selection-only
    # individuals act. They cannot adapt within a lifetime.
    selection_immediate_after_reversal = dict(selection_old)
    planner_immediate_after_reversal = planner_distribution(REVERSED)

    selection_first_survival = survival_fraction(selection_immediate_after_reversal, REVERSED)
    planner_first_survival = survival_fraction(planner_immediate_after_reversal, REVERSED)

    # Differential survival leaves only the newly favored inherited controller.
    survivors = survive(selection_immediate_after_reversal, REVERSED)
    parent = selected_parent_action(survivors)
    selection_next_generation = selection_offspring(parent)

    # After one generation, selection has caught up to the same 90/10 action
    # distribution that the explicit planner adopted immediately.
    next_generation_matches_planner = selection_next_generation == planner_immediate_after_reversal

    result = {
        "gate": "G13_SELECTION_MASQUERADES_AS_PREFERENCE",
        "population_size": N,
        "execution_error_or_mutation_rate": ERROR_OR_MUTATION,
        "old_regime_snapshot": {
            "regime": OLD.name,
            "explicit_planner": planner_old,
            "selection_only": selection_old,
            "action_distributions_identical": snapshot_identical,
            "selection_only_individual_has_reward_model": False,
            "selection_only_individual_has_learning": False,
        },
        "survival_mapping_reversal": {
            "new_regime": REVERSED.name,
            "explicit_planner_immediate": planner_immediate_after_reversal,
            "selection_only_immediate": selection_immediate_after_reversal,
            "immediate_action_distributions_identical": (
                planner_immediate_after_reversal == selection_immediate_after_reversal
            ),
            "explicit_planner_first_exposure_survival_fraction": planner_first_survival,
            "selection_only_first_exposure_survival_fraction": selection_first_survival,
            "selected_parent_action_after_first_exposure": parent,
            "selection_only_next_generation": selection_next_generation,
            "next_generation_matches_planner": next_generation_matches_planner,
        },
        "mechanism_identifiability": {
            "mature_snapshot_only": "NONIDENTIFIABLE",
            "regime_reversal_plus_temporal_response": "IDENTIFIABLE_IN_THIS_TOY",
        },
        "classification": (
            "SELECTION_CAN_PRODUCE_THE_SAME_MATURE_SURVIVAL_ORIENTED_ACTION_DISTRIBUTION_"
            "AS_AN_EXPLICIT_VIABILITY_PLANNER_WITHOUT_ANY_WITHIN_AGENT_REWARD_REPRESENTATION_"
            "BUT_A_SURVIVAL_MAPPING_REVERSAL_REVEALS_THE_DIFFERENCE_BY_IMMEDIATE_PLANNER_"
            "ADAPTATION_VERSUS_A_GENERATIONAL_SELECTION_LAG"
        ),
        "claim_boundary": (
            "Constructed selection-versus-control result. A selected population can look as if it "
            "values viability even though its individuals contain only fixed inherited actions and no "
            "reward or learning machinery. A temporal intervention on the survival mapping separates "
            "that mechanism from an explicit planner in this toy. Evolutionary fitness is not evidence "
            "of a represented within-agent objective, and neither is evidence of subjective valence."
        ),
    }

    # Snapshot false friend.
    assert snapshot_identical, result
    assert normalized(selection_old) == {"PRESERVE": 0.9, "COLLAPSE": 0.1}, result

    # Reversal exposes timescale / mechanism difference.
    assert planner_immediate_after_reversal == {"COLLAPSE": 90, "PRESERVE": 10}, result
    assert selection_immediate_after_reversal == {"PRESERVE": 90, "COLLAPSE": 10}, result
    assert planner_first_survival == 0.9, result
    assert selection_first_survival == 0.1, result
    assert parent == "COLLAPSE", result
    assert next_generation_matches_planner, result

    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
