#!/usr/bin/env python3
"""Gate 17 — learned audit hazard plus a hard maximum audit gap.

Gate 16 established that silent drift cannot be detected without buying evidence and
showed a pure historical-hazard scheduler can skip an intermediate operator generation
when the true change rate increases.

This gate tests the natural composition:

SLOW HAZARD
    Spend audits where historical change timing says they are likely to matter.

HARD SAFETY FLOOR
    Regardless of confidence, never allow more than MAX_GAP episodes between audits.

The hidden world is the same as Gate 16: changes every 40 episodes at first, then every
20 after t=180, while the ordinary observation remains exactly "OK". Only a paid audit
reveals the current operator generation.

The result should be read as maintenance / inspection scheduling. The maximum-gap rule
is a declared engineering constraint, not a learned truth and not a consciousness
mechanism.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from typing import Dict, Iterable, List, Sequence, Tuple


HORIZON = 320
CHANGE_POINTS: Tuple[int, ...] = (40, 80, 120, 160, 180, 200, 220, 240, 260, 280, 300)
HAZARD_SHIFT = 180
MAX_GAP = 16


def generation(t: int) -> int:
    return sum(change <= t for change in CHANGE_POINTS)


def ordinary_observation(t: int) -> str:
    _ = generation(t)
    return "OK"


def paid_audit(t: int) -> int:
    return generation(t)


@dataclass
class Trace:
    audits: List[int]
    detections: List[int]
    jumps: List[int]
    stale: List[int]

    @property
    def max_gap(self) -> int:
        boundaries = [0] + self.audits + [HORIZON]
        return max(b - a for a, b in zip(boundaries, boundaries[1:]))

    @property
    def pre_stale(self) -> int:
        return sum(t < HAZARD_SHIFT for t in self.stale)

    @property
    def post_stale(self) -> int:
        return sum(t >= HAZARD_SHIFT for t in self.stale)


def evaluate_schedule(times: Iterable[int]) -> Trace:
    schedule = set(times)
    cache = 0  # free initial calibration
    audits: List[int] = []
    detections: List[int] = []
    jumps: List[int] = []
    stale: List[int] = []

    for t in range(HORIZON):
        assert ordinary_observation(t) == "OK"
        if t in schedule:
            audits.append(t)
            current = paid_audit(t)
            if current != cache:
                detections.append(t)
                jumps.append(current - cache)
            cache = current
        if cache != generation(t):
            stale.append(t)
    return Trace(audits, detections, jumps, stale)


def run_hazard(max_gap: int | None) -> Tuple[Trace, float]:
    """Historical hazard scheduler, optionally constrained by a maximum audit gap."""
    cache = 0
    estimate = 40.0
    last_detection = 0
    last_audit = 0

    target = math.ceil(0.75 * estimate)
    search_step = max(1, math.ceil(0.125 * estimate))
    next_audit = target if max_gap is None else min(target, last_audit + max_gap)

    audits: List[int] = []
    detections: List[int] = []
    jumps: List[int] = []
    stale: List[int] = []

    for t in range(HORIZON):
        assert ordinary_observation(t) == "OK"
        if t == next_audit:
            audits.append(t)
            last_audit = t
            current = paid_audit(t)

            if current != cache:
                detections.append(t)
                jumps.append(current - cache)
                observed_detection_interval = t - last_detection
                estimate = 0.5 * estimate + 0.5 * observed_detection_interval
                last_detection = t
                cache = current
                target = t + math.ceil(0.75 * estimate)
                search_step = max(1, math.ceil(0.125 * estimate))
            else:
                cache = current
                if t >= target:
                    target = t + search_step

            if max_gap is None:
                next_audit = target
            else:
                next_audit = min(target, last_audit + max_gap)

        if cache != generation(t):
            stale.append(t)

    return Trace(audits, detections, jumps, stale), estimate


def periodic_trace(interval: int, offset: int) -> Trace:
    assert interval > 0
    assert 0 <= offset < interval
    times = [
        t
        for t in range(1, HORIZON)
        if (t - offset) % interval == 0
    ]
    return evaluate_schedule(times)


def summarize(trace: Trace) -> Dict[str, object]:
    return {
        "paid_audits": len(trace.audits),
        "stale_identity_episodes": len(trace.stale),
        "hidden_identity_accuracy": 1.0 - len(trace.stale) / HORIZON,
        "detected_audit_events": len(trace.detections),
        "max_generation_jump": max(trace.jumps, default=0),
        "max_audit_gap": trace.max_gap,
        "pre_hazard_shift_stale": trace.pre_stale,
        "post_hazard_shift_stale": trace.post_stale,
        "audit_times": list(trace.audits),
        "detection_times": list(trace.detections),
    }


def periodic_ensemble(interval: int) -> Dict[str, object]:
    rows = []
    for offset in range(interval):
        trace = periodic_trace(interval, offset)
        row = summarize(trace)
        row["offset"] = offset
        rows.append(row)
    return {
        "interval": interval,
        "mean_paid_audits": sum(int(row["paid_audits"]) for row in rows) / len(rows),
        "mean_stale_identity_episodes": sum(int(row["stale_identity_episodes"]) for row in rows) / len(rows),
        "best_phase_stale_identity_episodes": min(int(row["stale_identity_episodes"]) for row in rows),
        "worst_phase_stale_identity_episodes": max(int(row["stale_identity_episodes"]) for row in rows),
        "all_phases_capture_each_generation": all(
            int(row["detected_audit_events"]) == len(CHANGE_POINTS)
            and int(row["max_generation_jump"]) == 1
            for row in rows
        ),
        "rows": rows,
    }


def main() -> None:
    assert {ordinary_observation(t) for t in range(HORIZON)} == {"OK"}

    hazard_only, hazard_only_final = run_hazard(max_gap=None)
    hybrid, hybrid_final = run_hazard(max_gap=MAX_GAP)
    every = evaluate_schedule(range(1, HORIZON))
    oracle = evaluate_schedule(CHANGE_POINTS)

    # Rather than choose one convenient periodic phase, sweep several nearby audit
    # budgets and every phase offset. Interval 10 is the closest mean audit budget to
    # the 31-audit hybrid; 8..16 gives a small cost/staleness frontier.
    periodic_frontier = {
        str(interval): periodic_ensemble(interval)
        for interval in range(8, 17)
    }
    near = periodic_frontier["10"]

    result = {
        "gate": "G17_HAZARD_PLUS_SAFETY_FLOOR",
        "world": {
            "horizon": HORIZON,
            "change_points": list(CHANGE_POINTS),
            "historical_interval": 40,
            "new_interval_after_t180": 20,
            "ordinary_observation": "OK for every operator generation",
            "hybrid_max_gap": MAX_GAP,
        },
        "hazard_only": {
            **summarize(hazard_only),
            "final_expected_interval": hazard_only_final,
        },
        "hazard_plus_max_gap": {
            **summarize(hybrid),
            "final_expected_interval": hybrid_final,
        },
        "periodic_frontier_all_phase_offsets": periodic_frontier,
        "audit_every_episode": summarize(every),
        "oracle_change_point": summarize(oracle),
        "summary": {
            "hybrid_extra_audits_vs_hazard_only": len(hybrid.audits) - len(hazard_only.audits),
            "hybrid_stale_reduction_vs_hazard_only": len(hazard_only.stale) - len(hybrid.stale),
            "hybrid_restores_complete_generation_capture": (
                max(hybrid.jumps, default=0) == 1
                and len(hybrid.detections) == len(CHANGE_POINTS)
            ),
            "nearest_periodic_mean_budget": near["mean_paid_audits"],
            "nearest_periodic_mean_stale": near["mean_stale_identity_episodes"],
            "hybrid_budget": len(hybrid.audits),
            "hybrid_stale": len(hybrid.stale),
            "phase_lucky_periodic_can_still_win": near["best_phase_stale_identity_episodes"] < len(hybrid.stale),
        },
        "classification": (
            "A_HARD_MAXIMUM_AUDIT_GAP_CAN_COMPLEMENT_A_LEARNED_CHANGE_HAZARD_THE_HYBRID_"
            "PREVENTS_THE_PURE_HAZARD_SCHEDULERS_MISSED_OPERATOR_GENERATION_AND_REDUCES_STALE_"
            "DWELL_AT_A_MODERATE_EXTRA_EVIDENCE_COST_WHILE_RETAINING_STATISTICAL_TARGETING_BUT_"
            "A_FORTUITOUSLY_PHASE_ALIGNED_PERIODIC_SCHEDULE_CAN_STILL_OUTPERFORM_IT_IN_THIS_TOY"
        ),
        "claim_boundary": (
            "Constructed maintenance-scheduling result. The safety floor is an explicit engineering "
            "constraint, not learned semantics. It prevents gaps longer than 16 episodes in a world whose "
            "fastest changes are 20 episodes apart, so complete generation capture is expected. The hybrid "
            "improves the phase-averaged periodic tradeoff near the same audit budget, but a lucky periodic "
            "phase aligned to the hidden changes can do better. No universal optimality or phenomenology is claimed."
        ),
    }

    # Reproduce Gate 16's pure-hazard weakness.
    assert len(hazard_only.audits) == 20, result
    assert len(hazard_only.stale) == 52, result
    assert len(hazard_only.detections) == 10, result
    assert max(hazard_only.jumps) == 2, result
    assert hazard_only.max_gap == 30, result

    # Safety-bounded hybrid: moderate extra audits, less stale dwell, no skipped generation.
    assert len(hybrid.audits) == 31, result
    assert len(hybrid.stale) == 24, result
    assert hybrid.pre_stale == 0, result
    assert hybrid.post_stale == 24, result
    assert len(hybrid.detections) == len(CHANGE_POINTS), result
    assert max(hybrid.jumps) == 1, result
    assert hybrid.max_gap == MAX_GAP, result
    assert abs(hybrid_final - 20.359375) < 1e-12, result

    # The safety floor has a measurable price and a measurable benefit.
    assert len(hybrid.audits) - len(hazard_only.audits) == 11, result
    assert len(hazard_only.stale) - len(hybrid.stale) == 28, result

    # Periodic interval 10 is the closest phase-averaged audit budget.
    assert abs(near["mean_paid_audits"] - 31.9) < 1e-12, result
    assert abs(near["mean_stale_identity_episodes"] - 49.5) < 1e-12, result
    assert near["all_phases_capture_each_generation"] is True, result
    assert len(hybrid.audits) < near["mean_paid_audits"], result
    assert len(hybrid.stale) < near["mean_stale_identity_episodes"], result

    # Important honesty check: one perfectly phase-aligned periodic-10 schedule audits
    # exactly on all hidden changes and therefore beats the hybrid. We do not claim
    # universal optimality from this constructed world.
    assert near["best_phase_stale_identity_episodes"] == 0, result
    assert result["summary"]["phase_lucky_periodic_can_still_win"] is True, result

    assert len(every.stale) == 0 and len(every.audits) == 319, result
    assert len(oracle.stale) == 0 and len(oracle.audits) == len(CHANGE_POINTS), result

    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
