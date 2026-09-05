#!/usr/bin/env python3
"""Gate 16 — silent drift proves that cache invalidation has an evidence cost.

Gate 15 let the ordinary task consequence audit a cached causal identity for free. This
gate removes that convenience.

The hidden operator generation changes at known-to-the-experiment but hidden-to-agent
change points. The ordinary action produces exactly the same immediate observation
("OK") under every generation. Therefore no passive/current consequence can reveal
that the cached causal identity became stale. Only an explicit paid AUDIT reveals the
current generation.

Policies:

NO_AUDIT
    Trust the initial cache forever. Cost zero; cannot detect silent drift.

AUDIT_EVERY_EPISODE
    Pay every episode. Detects each change immediately.

PERIODIC_16
    Fixed 16-episode audit cadence. We evaluate every phase offset and equalize all
    schedules to the same 20-audit budget so alignment is not cherry-picked.

SLOW_HAZARD
    Starts with a historical 40-episode change-interval prior. It begins auditing at
    75% of the expected interval and then every 12.5% until a change is found. After a
    detection it updates the interval estimate from detection timing. The environment
    later doubles its change rate from every 40 episodes to every 20.

ORACLE_CHANGE_POINT
    Audits exactly at true changes. Benchmark only.

The important negative is structural: when normal consequences are identical, no
non-oracle method can detect drift without buying evidence. The slow hazard scheduler
can spend its fixed audit budget more economically while its historical hazard remains
valid, but it loses that advantage when the hazard changes and can even skip an
intermediate operator generation between audits.

This is change detection / inspection scheduling, not a consciousness result.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from typing import Dict, Iterable, List, Mapping, Sequence, Tuple


HORIZON = 320
CHANGE_POINTS: Tuple[int, ...] = (
    40,
    80,
    120,
    160,  # historical 40-episode regime
    180,
    200,
    220,
    240,
    260,
    280,
    300,  # new 20-episode regime
)
HAZARD_SHIFT = 180
PERIOD = 16
PERIODIC_BUDGET = 20


def operator_generation(t: int) -> int:
    return sum(change <= t for change in CHANGE_POINTS)


def ordinary_observation(t: int) -> str:
    # Deliberately invariant: this channel contains zero change information.
    _ = operator_generation(t)
    return "OK"


def audit(t: int) -> int:
    # The only evidence-bearing operation in this gate.
    return operator_generation(t)


@dataclass
class Trace:
    audit_times: List[int]
    detection_times: List[int]
    generation_jumps: List[int]
    stale_times: List[int]

    @property
    def paid_audits(self) -> int:
        return len(self.audit_times)

    @property
    def stale_episodes(self) -> int:
        return len(self.stale_times)

    @property
    def identity_accuracy(self) -> float:
        return 1.0 - self.stale_episodes / HORIZON

    @property
    def detection_events(self) -> int:
        return len(self.detection_times)

    @property
    def max_generation_jump(self) -> int:
        return max(self.generation_jumps, default=0)


def evaluate_schedule(audit_times: Iterable[int]) -> Trace:
    scheduled = set(audit_times)
    assert all(0 < t < HORIZON for t in scheduled), scheduled
    cache_generation = 0  # free initial calibration at t=0
    audits: List[int] = []
    detections: List[int] = []
    jumps: List[int] = []
    stale: List[int] = []

    for t in range(HORIZON):
        assert ordinary_observation(t) == "OK"
        if t in scheduled:
            audits.append(t)
            current = audit(t)
            if current != cache_generation:
                detections.append(t)
                jumps.append(current - cache_generation)
            cache_generation = current
        if cache_generation != operator_generation(t):
            stale.append(t)

    return Trace(audits, detections, jumps, stale)


def periodic_schedule(offset: int) -> Tuple[int, ...]:
    """A fixed-period schedule with a phase offset and exactly 20 paid audits."""
    assert 0 <= offset < PERIOD
    times = [
        t
        for t in range(1, HORIZON)
        if (t - offset) % PERIOD == 0
    ]
    # Offset 0 naturally has 19 audits in [1,319]. Add a terminal audit so every
    # phase gets the same budget. This cannot repair earlier stale dwell.
    while len(times) < PERIODIC_BUDGET:
        candidate = HORIZON - 1
        while candidate in times:
            candidate -= 1
        times.append(candidate)
    times = sorted(times[:PERIODIC_BUDGET])
    assert len(times) == PERIODIC_BUDGET
    return tuple(times)


def slow_hazard_trace() -> Tuple[Trace, float]:
    """Inspection scheduler using only prior hazard and its own detection times."""
    cache_generation = 0
    estimate = 40.0
    last_detection = 0
    next_audit = math.ceil(0.75 * estimate)
    search_step = max(1, math.ceil(0.125 * estimate))

    audits: List[int] = []
    detections: List[int] = []
    jumps: List[int] = []
    stale: List[int] = []

    for t in range(HORIZON):
        assert ordinary_observation(t) == "OK"
        if t == next_audit:
            audits.append(t)
            current = audit(t)
            if current != cache_generation:
                detections.append(t)
                jumps.append(current - cache_generation)
                observed_detection_interval = t - last_detection
                estimate = 0.5 * estimate + 0.5 * observed_detection_interval
                last_detection = t
                cache_generation = current
                next_audit = t + math.ceil(0.75 * estimate)
                search_step = max(1, math.ceil(0.125 * estimate))
            else:
                cache_generation = current
                next_audit = t + search_step

        if cache_generation != operator_generation(t):
            stale.append(t)

    return Trace(audits, detections, jumps, stale), estimate


def change_to_next_audit_latencies(audit_times: Sequence[int]) -> List[int]:
    latencies: List[int] = []
    for change in CHANGE_POINTS:
        later = [t for t in audit_times if t >= change]
        latencies.append((min(later) - change) if later else HORIZON - change)
    return latencies


def trace_summary(trace: Trace) -> Dict[str, object]:
    pre_stale = sum(t < HAZARD_SHIFT for t in trace.stale_times)
    post_stale = sum(t >= HAZARD_SHIFT for t in trace.stale_times)
    return {
        "paid_audits": trace.paid_audits,
        "stale_identity_episodes": trace.stale_episodes,
        "hidden_identity_accuracy": trace.identity_accuracy,
        "pre_hazard_shift_stale_episodes": pre_stale,
        "post_hazard_shift_stale_episodes": post_stale,
        "detection_events": trace.detection_events,
        "max_generation_jump": trace.max_generation_jump,
        "audit_times": list(trace.audit_times),
        "detection_times": list(trace.detection_times),
        "change_to_next_audit_latency": change_to_next_audit_latencies(trace.audit_times),
    }


def main() -> None:
    # Prove the cheap channel is genuinely silent under all hidden generations.
    assert {ordinary_observation(t) for t in range(HORIZON)} == {"OK"}

    no_audit = evaluate_schedule(())
    every = evaluate_schedule(range(1, HORIZON))
    oracle = evaluate_schedule(CHANGE_POINTS)

    periodic_rows: List[Dict[str, object]] = []
    for offset in range(PERIOD):
        trace = evaluate_schedule(periodic_schedule(offset))
        row = trace_summary(trace)
        row["offset"] = offset
        periodic_rows.append(row)

    hazard, final_estimate = slow_hazard_trace()

    periodic_stale = [int(row["stale_identity_episodes"]) for row in periodic_rows]
    periodic_pre = [int(row["pre_hazard_shift_stale_episodes"]) for row in periodic_rows]
    periodic_post = [int(row["post_hazard_shift_stale_episodes"]) for row in periodic_rows]

    periodic_summary = {
        "interval": PERIOD,
        "paid_audits_each": PERIODIC_BUDGET,
        "mean_stale_identity_episodes_over_all_offsets": sum(periodic_stale) / len(periodic_stale),
        "best_offset_stale_identity_episodes": min(periodic_stale),
        "worst_offset_stale_identity_episodes": max(periodic_stale),
        "mean_pre_hazard_shift_stale": sum(periodic_pre) / len(periodic_pre),
        "mean_post_hazard_shift_stale": sum(periodic_post) / len(periodic_post),
        "all_offsets_detect_every_generation_separately": all(
            int(row["detection_events"]) == len(CHANGE_POINTS)
            and int(row["max_generation_jump"]) == 1
            for row in periodic_rows
        ),
        "offsets": periodic_rows,
    }

    result = {
        "gate": "G16_SILENT_DRIFT_AUDIT_COST",
        "world": {
            "horizon": HORIZON,
            "change_points": list(CHANGE_POINTS),
            "historical_interval": 40,
            "new_interval_after_t180": 20,
            "ordinary_observation": "OK for every operator generation",
            "initial_generation_is_calibrated_free": True,
        },
        "no_audit": trace_summary(no_audit),
        "audit_every_episode": trace_summary(every),
        "periodic_16_equal_budget_ensemble": periodic_summary,
        "slow_hazard": {
            **trace_summary(hazard),
            "initial_expected_interval": 40.0,
            "final_expected_interval": final_estimate,
        },
        "oracle_change_point": trace_summary(oracle),
        "summary": {
            "silent_drift_is_undetectable_without_audit": no_audit.detection_events == 0,
            "slow_hazard_same_budget_as_periodic": hazard.paid_audits == PERIODIC_BUDGET,
            "slow_hazard_stale_vs_periodic_mean": (
                hazard.stale_episodes,
                periodic_summary["mean_stale_identity_episodes_over_all_offsets"],
            ),
            "slow_hazard_stale_vs_periodic_best_offset": (
                hazard.stale_episodes,
                periodic_summary["best_offset_stale_identity_episodes"],
            ),
            "slow_hazard_advantage_before_hazard_change": (
                sum(t < HAZARD_SHIFT for t in hazard.stale_times),
                periodic_summary["mean_pre_hazard_shift_stale"],
            ),
            "slow_hazard_after_hazard_change": (
                sum(t >= HAZARD_SHIFT for t in hazard.stale_times),
                periodic_summary["mean_post_hazard_shift_stale"],
            ),
            "slow_hazard_skipped_an_intermediate_generation": hazard.max_generation_jump > 1,
        },
        "classification": (
            "SILENT_OPERATOR_DRIFT_CANNOT_BE_DETECTED_FROM_AN_INFORMATION_FREE_NORMAL_CONSEQUENCE_"
            "AUDITING_HAS_AN_IRREDUCIBLE_EVIDENCE_COST_A_LEARNED_HAZARD_CAN_ALLOCATE_A_FIXED_AUDIT_"
            "BUDGET_MORE_EFFICIENTLY_WHILE_ITS_CHANGE_STATISTICS_HOLD_BUT_AFTER_THE_HAZARD_CHANGES_"
            "THE_ADVANTAGE_COLLAPSES_AND_AN_INTERMEDIATE_OPERATOR_GENERATION_CAN_BE_MISSED"
        ),
        "claim_boundary": (
            "Constructed inspection-scheduling result. No-audit failure is an identifiability result, not an "
            "algorithmic weakness: the ordinary observation is exactly constant. The slow-hazard scheduler "
            "uses only historical timing and its own audit detections. It improves stale-dwell economics in "
            "the familiar regime but gives no guarantee under hazard shift and misses one intermediate "
            "generation. This is change detection / maintenance scheduling, not qualia or phenomenology."
        ),
    }

    # Hard negative: no evidence means no detection.
    assert no_audit.paid_audits == 0, result
    assert no_audit.detection_events == 0, result
    assert no_audit.stale_episodes == 280, result

    # Paying every episode or knowing the change point removes stale dwell by construction.
    assert every.paid_audits == 319, result
    assert every.stale_episodes == 0, result
    assert every.detection_events == len(CHANGE_POINTS), result
    assert oracle.paid_audits == len(CHANGE_POINTS), result
    assert oracle.stale_episodes == 0, result

    # Fair periodic ensemble: same 20-audit budget for all 16 phase offsets.
    assert all(int(row["paid_audits"]) == 20 for row in periodic_rows), result
    assert abs(periodic_summary["mean_stale_identity_episodes_over_all_offsets"] - 82.5) < 1e-12, result
    assert periodic_summary["best_offset_stale_identity_episodes"] == 56, result
    assert periodic_summary["worst_offset_stale_identity_episodes"] == 109, result
    assert abs(periodic_summary["mean_pre_hazard_shift_stale"] - 30.0) < 1e-12, result
    assert abs(periodic_summary["mean_post_hazard_shift_stale"] - 52.5) < 1e-12, result
    assert periodic_summary["all_offsets_detect_every_generation_separately"] is True, result

    # Slow hazard scheduling spends the same 20 audits. It is excellent while its 40-step
    # historical prior is correct, but the advantage vanishes when the rate doubles.
    assert hazard.paid_audits == 20, result
    assert hazard.stale_episodes == 52, result
    assert sum(t < HAZARD_SHIFT for t in hazard.stale_times) == 0, result
    assert sum(t >= HAZARD_SHIFT for t in hazard.stale_times) == 52, result
    assert hazard.stale_episodes < periodic_summary["best_offset_stale_identity_episodes"], result

    # Crucial negative: the stale-dwell win is not a guarantee of complete change capture.
    # One audit jumps directly from generation 6 to generation 8 after the hazard shift.
    assert hazard.detection_events == 10, result
    assert hazard.max_generation_jump == 2, result
    assert abs(final_estimate - 20.8125) < 1e-12, result

    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
