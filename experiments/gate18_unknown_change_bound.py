#!/usr/bin/env python3
"""Gate 18 — violate the assumed hidden-change-rate bound.

Gate 17's MAX_GAP=16 safety floor captured every operator generation only because the
constructed world never changed faster than once every 20 episodes. This gate removes
that guarantee.

The ordinary observation remains exactly "OK" for every hidden operator state. A paid
audit reveals only the *current* operator label, not a revision counter or hidden event
log.

The actual world begins in C and contains a burst:

    t=100: C -> A
    t=106: A -> B

Both changes happen between the fixed audits at t=96 and t=112. At t=112 the observer
can recover the current state B, but it cannot know whether the path was C->A->B or a
single direct C->B change. We construct that alternative world explicitly and verify
that every observation and every audit available to the tested bounded observers is
identical.

After the first surprise, ESCALATING_AUDITOR shortens its future gap from 16 to 4. It
therefore reduces later stale dwell and captures later state changes separately. It
still cannot retroactively recover the unobserved A state from t=100..105.

This is a finite observability / sampled-change-detection stopping line, not a
consciousness result.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Dict, Iterable, List, Sequence, Tuple


HORIZON = 176
START_STATE = "C"
FIXED_GAP = 16
ESCALATED_GAP = 4

# Seven true hidden transitions. The first two violate the 16-step event-capture bound.
ACTUAL_CHANGES: Tuple[Tuple[int, str], ...] = (
    (100, "A"),
    (106, "B"),
    (118, "C"),
    (124, "A"),
    (130, "B"),
    (138, "C"),
    (146, "A"),
)

# Same audited endpoints as ACTUAL for all tested non-oracle schedules, but the hidden
# intermediate A in the first burst never exists.
ALTERNATE_CHANGES: Tuple[Tuple[int, str], ...] = (
    (106, "B"),
    (118, "C"),
    (124, "A"),
    (130, "B"),
    (138, "C"),
    (146, "A"),
)


def hidden_state(t: int, changes: Sequence[Tuple[int, str]]) -> str:
    state = START_STATE
    for change_t, new_state in changes:
        if change_t <= t:
            state = new_state
        else:
            break
    return state


def ordinary_observation(t: int, changes: Sequence[Tuple[int, str]]) -> str:
    _ = hidden_state(t, changes)
    return "OK"


def audit(t: int, changes: Sequence[Tuple[int, str]]) -> str:
    return hidden_state(t, changes)


@dataclass
class Trace:
    audit_times: List[int]
    audit_states: List[str]
    detections: List[Tuple[int, str, str]]
    stale_times: List[int]

    @property
    def paid_audits(self) -> int:
        return len(self.audit_times)

    @property
    def stale_episodes(self) -> int:
        return len(self.stale_times)

    @property
    def detection_events(self) -> int:
        return len(self.detections)


def evaluate_schedule(
    audit_times: Iterable[int],
    changes: Sequence[Tuple[int, str]],
) -> Trace:
    schedule = set(audit_times)
    cache = START_STATE
    times: List[int] = []
    states: List[str] = []
    detections: List[Tuple[int, str, str]] = []
    stale: List[int] = []

    for t in range(HORIZON):
        assert ordinary_observation(t, changes) == "OK"
        if t in schedule:
            times.append(t)
            current = audit(t, changes)
            states.append(current)
            if current != cache:
                detections.append((t, cache, current))
            cache = current
        if cache != hidden_state(t, changes):
            stale.append(t)

    return Trace(times, states, detections, stale)


def fixed_schedule() -> Tuple[int, ...]:
    return tuple(range(FIXED_GAP, HORIZON, FIXED_GAP))


def escalating_trace(changes: Sequence[Tuple[int, str]]) -> Trace:
    """Use gap16 until first changed audit endpoint, then gap4 thereafter."""
    cache = START_STATE
    times: List[int] = []
    states: List[str] = []
    detections: List[Tuple[int, str, str]] = []
    stale: List[int] = []

    gap = FIXED_GAP
    next_audit = FIXED_GAP
    escalated = False

    for t in range(HORIZON):
        assert ordinary_observation(t, changes) == "OK"
        if t == next_audit:
            times.append(t)
            current = audit(t, changes)
            states.append(current)
            if current != cache:
                detections.append((t, cache, current))
                if not escalated:
                    escalated = True
                    gap = ESCALATED_GAP
            cache = current
            next_audit = t + gap
        if cache != hidden_state(t, changes):
            stale.append(t)

    return Trace(times, states, detections, stale)


def transcript(trace: Trace) -> Tuple[Tuple[int, str], ...]:
    return tuple(zip(trace.audit_times, trace.audit_states))


def summarize(trace: Trace) -> Dict[str, object]:
    return {
        "paid_audits": trace.paid_audits,
        "stale_identity_episodes": trace.stale_episodes,
        "current_identity_accuracy": 1.0 - trace.stale_episodes / HORIZON,
        "detected_endpoint_changes": trace.detection_events,
        "audit_times": list(trace.audit_times),
        "audit_states": list(trace.audit_states),
        "detections": [list(item) for item in trace.detections],
    }


def main() -> None:
    # The normal channel is exactly non-informative in both possible worlds.
    assert {ordinary_observation(t, ACTUAL_CHANGES) for t in range(HORIZON)} == {"OK"}
    assert {ordinary_observation(t, ALTERNATE_CHANGES) for t in range(HORIZON)} == {"OK"}

    fixed_actual = evaluate_schedule(fixed_schedule(), ACTUAL_CHANGES)
    fixed_alt = evaluate_schedule(fixed_schedule(), ALTERNATE_CHANGES)
    escalating_actual = escalating_trace(ACTUAL_CHANGES)
    escalating_alt = escalating_trace(ALTERNATE_CHANGES)
    every_actual = evaluate_schedule(range(1, HORIZON), ACTUAL_CHANGES)
    oracle_actual = evaluate_schedule((t for t, _ in ACTUAL_CHANGES), ACTUAL_CHANGES)

    # The critical indistinguishability witness: the actual two-change burst and the
    # alternate one-change path generate the same complete audit transcripts for both
    # bounded observers. No estimator downstream of these transcripts can know which
    # hidden path occurred.
    fixed_transcripts_equal = transcript(fixed_actual) == transcript(fixed_alt)
    escalating_transcripts_equal = transcript(escalating_actual) == transcript(escalating_alt)

    result = {
        "gate": "G18_UNKNOWN_CHANGE_BOUND",
        "world": {
            "horizon": HORIZON,
            "fixed_max_gap": FIXED_GAP,
            "escalated_gap": ESCALATED_GAP,
            "actual_changes": [list(item) for item in ACTUAL_CHANGES],
            "alternate_changes": [list(item) for item in ALTERNATE_CHANGES],
            "ordinary_observation": "OK under every hidden state",
            "ambiguous_interval": [96, 112],
            "actual_hidden_path_in_interval": ["C", "A", "B"],
            "alternate_hidden_path_in_interval": ["C", "B"],
            "audited_endpoints_in_both_worlds": ["C", "B"],
        },
        "fixed_max_gap16": summarize(fixed_actual),
        "escalating_auditor": summarize(escalating_actual),
        "audit_every_episode": summarize(every_actual),
        "oracle_change_times": summarize(oracle_actual),
        "nonidentifiability_witness": {
            "fixed_complete_audit_transcripts_equal": fixed_transcripts_equal,
            "escalating_complete_audit_transcripts_equal": escalating_transcripts_equal,
            "actual_number_of_hidden_changes": len(ACTUAL_CHANGES),
            "alternate_number_of_hidden_changes": len(ALTERNATE_CHANGES),
            "first_burst_actual_change_count": 2,
            "first_burst_alternate_change_count": 1,
            "retroactive_intermediate_state_A_identifiable": False,
        },
        "summary": {
            "fixed_paid_audits": fixed_actual.paid_audits,
            "fixed_stale_episodes": fixed_actual.stale_episodes,
            "fixed_detected_endpoint_changes": fixed_actual.detection_events,
            "escalating_paid_audits": escalating_actual.paid_audits,
            "escalating_stale_episodes": escalating_actual.stale_episodes,
            "escalating_detected_endpoint_changes": escalating_actual.detection_events,
            "escalation_future_stale_reduction": fixed_actual.stale_episodes - escalating_actual.stale_episodes,
            "current_state_at_t112_recovered": audit(112, ACTUAL_CHANGES) == "B",
            "exact_hidden_path_before_t112_recoverable_from_tested_transcript": False,
        },
        "classification": (
            "WHEN_MULTIPLE_SILENT_OPERATOR_CHANGES_CAN_OCCUR_INSIDE_THE_DECLARED_AUDIT_BOUND_"
            "THE_NEXT_AUDIT_CAN_RESTORE_CORRECT_CURRENT_IDENTITY_WITHOUT_IDENTIFYING_THE_UNOBSERVED_"
            "INTERMEDIATE_PATH_ADAPTIVE_ESCALATION_CAN_REDUCE_FUTURE_STALENESS_BUT_CANNOT_"
            "RETROACTIVELY_CREATE_EVIDENCE_FOR_A_HIDDEN_TRANSITION_THAT_LEFT_THE_SAME_AUDITED_ENDPOINTS"
        ),
        "claim_boundary": (
            "Constructed sampled-observability stopping line. The actual and alternate worlds differ in "
            "whether an intermediate A state occurred, yet every normal observation and every audit made "
            "by FIXED16 or the tested escalating observer is identical. Therefore exact path recovery is "
            "not merely hard; it is non-identifiable from the supplied evidence. Faster auditing after the "
            "surprise improves future current-state tracking but cannot reconstruct the missed past."
        ),
    }

    # Exact deterministic receipts.
    assert fixed_actual.paid_audits == 10, result
    assert fixed_actual.stale_episodes == 50, result
    assert fixed_actual.detection_events == 4, result

    assert escalating_actual.paid_audits == 22, result
    assert escalating_actual.stale_episodes == 20, result
    assert escalating_actual.detection_events == 6, result
    assert fixed_actual.stale_episodes - escalating_actual.stale_episodes == 30, result

    # Perfectly sampled and oracle schedules establish the obvious cost ceiling / lower benchmark.
    assert every_actual.paid_audits == 175, result
    assert every_actual.stale_episodes == 0, result
    assert every_actual.detection_events == len(ACTUAL_CHANGES), result
    assert oracle_actual.paid_audits == len(ACTUAL_CHANGES), result
    assert oracle_actual.stale_episodes == 0, result

    # Stopping line: two different hidden event histories yield exactly the same entire
    # evidence transcript for both bounded observers.
    assert ACTUAL_CHANGES != ALTERNATE_CHANGES
    assert len(ACTUAL_CHANGES) == 7 and len(ALTERNATE_CHANGES) == 6
    assert fixed_transcripts_equal is True, result
    assert escalating_transcripts_equal is True, result
    assert audit(96, ACTUAL_CHANGES) == audit(96, ALTERNATE_CHANGES) == "C"
    assert audit(112, ACTUAL_CHANGES) == audit(112, ALTERNATE_CHANGES) == "B"
    assert hidden_state(102, ACTUAL_CHANGES) == "A"
    assert hidden_state(102, ALTERNATE_CHANGES) == "C"

    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
