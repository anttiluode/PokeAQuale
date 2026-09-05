#!/usr/bin/env python3
"""Gate 15 — FAST + MEDIUM + SLOW compose under operator drift.

This is the end-to-end composition preregistered after Gate 14.

A persistent passive context usually predicts which of V0/V1/V2 is the causal driver.
The mapping is stable for a long epoch and then remaps abruptly. The same context key
therefore becomes stale: a cached answer can remain syntactically valid while its
causal meaning has changed.

Timescales:

FAST
    Paid causal probes identify the current driver. If a cached prediction is
    contradicted by the ordinary task consequence, FAST re-grounds the context.

MEDIUM
    A bounded LRU cache stores context -> poke-confirmed driver. A correct cache hit
    needs no extra diagnostic probe; the normal task consequence audits the shortcut.

SLOW
    A decayed empirical prior over drivers orders future paid probes. It may make a
    search cheaper, but it is never allowed to decide truth without current evidence.

Attackers:

ALWAYS_ACTIVE
    Ignore context and identify causally on every episode. Robust, expensive.

CACHE_NO_INVALIDATION
    Fill a bounded cache on cold misses, then trust hits forever. Cheap while stable,
    but stale hot entries remain confidently wrong after remap.

PRIOR_ONLY
    Use the dominant pre-shift cause forever. Zero diagnostic cost, brittle.

FAST_MEDIUM
    Cache + contradiction-triggered re-grounding, with neutral probe ordering.

FAST_MEDIUM_SLOW
    Same robust cache invalidation plus slow empirical probe ordering.

The ordinary control action is common to all agents and is not counted as a diagnostic
probe. Its observed success/failure is allowed to audit a cached prediction. Thus a
stale cache hit can be detected without inventing a free hidden label: the agent sees
that the action it expected to work did not. It then pays for additional causal tests.

This is an adaptive diagnosis / audited-cache result, not a consciousness result.
"""

from __future__ import annotations

import json
from collections import OrderedDict
from itertools import permutations
from typing import Dict, Iterable, List, Mapping, MutableMapping, Optional, Sequence, Tuple


DRIVERS: Tuple[str, ...] = ("V0", "V1", "V2")
CONTEXTS: Tuple[str, ...] = tuple(f"K{i}" for i in range(10))
CACHE_CAPACITY = 4
SLOW_DECAY = 0.9
CYCLES_PER_PHASE = 6

# The stable pre-shift operator. Seven contexts use V1, two V0, one V2.
PRE_MAP: Dict[str, str] = {
    **{f"K{i}": "V1" for i in range(7)},
    "K7": "V0",
    "K8": "V0",
    "K9": "V2",
}

# Abrupt operator drift preserves passive context names while changing causal meaning.
# V1 -> V2, V2 -> V1, and V0 stays V0.
POST_MAP: Dict[str, str] = {
    context: {"V0": "V0", "V1": "V2", "V2": "V1"}[driver]
    for context, driver in PRE_MAP.items()
}

# K0/K1 are recurrent hot contexts; K2..K9 appear once each per motif. This makes a
# bounded medium cache useful without making every context permanently resident.
MOTIF: Tuple[str, ...] = tuple(
    item
    for rare in range(2, 10)
    for item in ("K0", "K1", f"K{rare}")
)

NEUTRAL_ORDERS: Tuple[Tuple[str, ...], ...] = tuple(permutations(DRIVERS))


class LRUCache:
    """Tiny deterministic LRU cache used as the MEDIUM timescale."""

    def __init__(self, capacity: int) -> None:
        assert capacity > 0
        self.capacity = capacity
        self._items: "OrderedDict[str, str]" = OrderedDict()

    def get(self, key: str) -> Optional[str]:
        if key not in self._items:
            return None
        value = self._items.pop(key)
        self._items[key] = value
        return value

    def put(self, key: str, value: str) -> None:
        if key in self._items:
            self._items.pop(key)
        self._items[key] = value
        if len(self._items) > self.capacity:
            self._items.popitem(last=False)


class SlowPrior:
    """Exponentially decayed empirical driver counts used only to order probes."""

    def __init__(self, decay: float = SLOW_DECAY) -> None:
        assert 0.0 < decay < 1.0
        self.decay = decay
        self.score: Dict[str, float] = {driver: 1.0 for driver in DRIVERS}

    def order(self, excluded: Iterable[str] = ()) -> Tuple[str, ...]:
        excluded_set = set(excluded)
        return tuple(
            sorted(
                (driver for driver in DRIVERS if driver not in excluded_set),
                key=lambda driver: (-self.score[driver], driver),
            )
        )

    def update(self, confirmed_driver: str) -> None:
        for driver in DRIVERS:
            self.score[driver] *= self.decay
        self.score[confirmed_driver] += 1.0


class NeutralOrder:
    """Cycles all six label permutations so FAST_MEDIUM has no privileged label."""

    def __init__(self) -> None:
        self.index = 0

    def next(self, excluded: Iterable[str] = ()) -> Tuple[str, ...]:
        excluded_set = set(excluded)
        order = NEUTRAL_ORDERS[self.index % len(NEUTRAL_ORDERS)]
        self.index += 1
        return tuple(driver for driver in order if driver not in excluded_set)


def identify_cost(driver: str, order: Sequence[str]) -> int:
    """Paid binary probes until positive; final candidate can be inferred for free."""
    assert driver in order, (driver, order)
    assert len(set(order)) == len(order), order
    if len(order) == 1:
        return 0
    position = order.index(driver)
    return min(position + 1, len(order) - 1)


def episode_stream() -> List[Tuple[str, str, str]]:
    stream: List[Tuple[str, str, str]] = []
    for phase, mapping in (("pre", PRE_MAP), ("post", POST_MAP)):
        for _ in range(CYCLES_PER_PHASE):
            for context in MOTIF:
                stream.append((phase, context, mapping[context]))
    return stream


def dominant_pre_driver() -> str:
    counts = {driver: 0 for driver in DRIVERS}
    for context in MOTIF:
        counts[PRE_MAP[context]] += 1
    return max(DRIVERS, key=lambda driver: (counts[driver], driver))


def empty_metrics() -> Dict[str, object]:
    return {
        "episodes": 0,
        "final_correct": 0,
        "diagnostic_probes": 0,
        "cache_hits": 0,
        "cache_misses": 0,
        "cache_invalidations": 0,
        "stale_initial_predictions": 0,
        "first_post_invalidation_offset": None,
        "timeline": [],
    }


def record(
    metrics: MutableMapping[str, object],
    *,
    phase: str,
    context: str,
    driver: str,
    final_prediction: str,
    probes: int,
    stale_initial: bool = False,
    invalidated: bool = False,
    post_offset: Optional[int] = None,
) -> None:
    metrics["episodes"] = int(metrics["episodes"]) + 1
    metrics["final_correct"] = int(metrics["final_correct"]) + int(final_prediction == driver)
    metrics["diagnostic_probes"] = int(metrics["diagnostic_probes"]) + probes
    if stale_initial:
        metrics["stale_initial_predictions"] = int(metrics["stale_initial_predictions"]) + 1
    if invalidated:
        metrics["cache_invalidations"] = int(metrics["cache_invalidations"]) + 1
        if phase == "post" and metrics["first_post_invalidation_offset"] is None:
            metrics["first_post_invalidation_offset"] = post_offset
    timeline = metrics["timeline"]
    assert isinstance(timeline, list)
    timeline.append(
        {
            "phase": phase,
            "context": context,
            "driver": driver,
            "prediction": final_prediction,
            "diagnostic_probes": probes,
            "stale_initial": stale_initial,
            "invalidated": invalidated,
        }
    )


def run_always_active(stream: Sequence[Tuple[str, str, str]]) -> Dict[str, object]:
    metrics = empty_metrics()
    neutral = NeutralOrder()
    post_offset = 0
    for phase, context, driver in stream:
        probes = identify_cost(driver, neutral.next())
        record(
            metrics,
            phase=phase,
            context=context,
            driver=driver,
            final_prediction=driver,
            probes=probes,
            post_offset=post_offset if phase == "post" else None,
        )
        if phase == "post":
            post_offset += 1
    return metrics


def run_prior_only(stream: Sequence[Tuple[str, str, str]]) -> Dict[str, object]:
    metrics = empty_metrics()
    guess = dominant_pre_driver()
    post_offset = 0
    for phase, context, driver in stream:
        record(
            metrics,
            phase=phase,
            context=context,
            driver=driver,
            final_prediction=guess,
            probes=0,
            post_offset=post_offset if phase == "post" else None,
        )
        if phase == "post":
            post_offset += 1
    metrics["compiled_guess"] = guess
    return metrics


def run_cached(
    stream: Sequence[Tuple[str, str, str]],
    *,
    invalidate_on_contradiction: bool,
    use_slow_prior: bool,
) -> Dict[str, object]:
    metrics = empty_metrics()
    cache = LRUCache(CACHE_CAPACITY)
    neutral = NeutralOrder()
    slow = SlowPrior()
    post_offset = 0

    for phase, context, driver in stream:
        cached = cache.get(context)
        probes = 0
        stale_initial = False
        invalidated = False

        if cached is None:
            metrics["cache_misses"] = int(metrics["cache_misses"]) + 1
            order = slow.order() if use_slow_prior else neutral.next()
            probes = identify_cost(driver, order)
            final_prediction = driver
            cache.put(context, driver)
        else:
            metrics["cache_hits"] = int(metrics["cache_hits"]) + 1
            if cached == driver:
                # The normal control consequence agrees with the cached expectation.
                final_prediction = cached
            elif not invalidate_on_contradiction:
                # Attacker: the task consequence says the cached prediction failed, but
                # this system has no invalidation path and keeps trusting the old key.
                stale_initial = True
                final_prediction = cached
            else:
                # The normal consequence contradicts the cached hypothesis. The stale
                # candidate is already ruled out; one paid probe distinguishes the two
                # remaining causes, with the last candidate inferred on a negative.
                stale_initial = True
                invalidated = True
                if use_slow_prior:
                    order = slow.order(excluded=(cached,))
                else:
                    order = neutral.next(excluded=(cached,))
                probes = identify_cost(driver, order)
                final_prediction = driver
                cache.put(context, driver)

        # The slow prior learns only from a confirmed current driver. Cache hits count as
        # confirmation because the ordinary task consequence agreed with the prediction.
        if use_slow_prior:
            assert final_prediction == driver, "slow history must not learn from unverified error"
            slow.update(driver)

        record(
            metrics,
            phase=phase,
            context=context,
            driver=driver,
            final_prediction=final_prediction,
            probes=probes,
            stale_initial=stale_initial,
            invalidated=invalidated,
            post_offset=post_offset if phase == "post" else None,
        )
        if phase == "post":
            post_offset += 1

    if use_slow_prior:
        metrics["final_slow_order"] = list(slow.order())
        metrics["final_slow_score"] = dict(slow.score)
    return metrics


def segment(timeline: Sequence[Mapping[str, object]], start: int, stop: int) -> Dict[str, float]:
    rows = timeline[start:stop]
    assert rows
    return {
        "episodes": float(len(rows)),
        "accuracy": sum(row["prediction"] == row["driver"] for row in rows) / len(rows),
        "diagnostic_probes": float(sum(int(row["diagnostic_probes"]) for row in rows)),
        "diagnostic_probes_per_episode": sum(int(row["diagnostic_probes"]) for row in rows) / len(rows),
        "stale_initial_predictions": float(sum(bool(row["stale_initial"]) for row in rows)),
        "cache_invalidations": float(sum(bool(row["invalidated"]) for row in rows)),
    }


def summarize(metrics: Mapping[str, object]) -> Dict[str, object]:
    episodes = int(metrics["episodes"])
    timeline = metrics["timeline"]
    assert isinstance(timeline, list)
    phase_len = len(MOTIF) * CYCLES_PER_PHASE
    cycle = len(MOTIF)
    assert episodes == 2 * phase_len

    result: Dict[str, object] = {
        "accuracy": int(metrics["final_correct"]) / episodes,
        "total_diagnostic_probes": int(metrics["diagnostic_probes"]),
        "diagnostic_probes_per_episode": int(metrics["diagnostic_probes"]) / episodes,
        "cache_hits": int(metrics["cache_hits"]),
        "cache_misses": int(metrics["cache_misses"]),
        "cache_invalidations": int(metrics["cache_invalidations"]),
        "stale_initial_predictions": int(metrics["stale_initial_predictions"]),
        "first_post_invalidation_offset": metrics["first_post_invalidation_offset"],
        "pre_first_cycle": segment(timeline, 0, cycle),
        "pre_steady_last_cycle": segment(timeline, phase_len - cycle, phase_len),
        "post_first_cycle": segment(timeline, phase_len, phase_len + cycle),
        "post_steady_last_cycle": segment(timeline, 2 * phase_len - cycle, 2 * phase_len),
    }
    for optional in ("compiled_guess", "final_slow_order", "final_slow_score"):
        if optional in metrics:
            result[optional] = metrics[optional]
    return result


def main() -> None:
    assert set(PRE_MAP) == set(CONTEXTS)
    assert set(POST_MAP) == set(CONTEXTS)
    assert len(MOTIF) == 24
    assert dominant_pre_driver() == "V1"

    stream = episode_stream()
    raw = {
        "always_active": run_always_active(stream),
        "cache_no_invalidation": run_cached(
            stream,
            invalidate_on_contradiction=False,
            use_slow_prior=False,
        ),
        "prior_only": run_prior_only(stream),
        "fast_medium": run_cached(
            stream,
            invalidate_on_contradiction=True,
            use_slow_prior=False,
        ),
        "fast_medium_slow": run_cached(
            stream,
            invalidate_on_contradiction=True,
            use_slow_prior=True,
        ),
    }
    agents = {name: summarize(metrics) for name, metrics in raw.items()}

    always = agents["always_active"]
    cache = agents["cache_no_invalidation"]
    prior = agents["prior_only"]
    fm = agents["fast_medium"]
    fms = agents["fast_medium_slow"]

    result = {
        "gate": "G15_THREE_TIMESCALE_OBSERVER",
        "world": {
            "contexts": len(CONTEXTS),
            "cache_capacity": CACHE_CAPACITY,
            "motif_length": len(MOTIF),
            "cycles_per_phase": CYCLES_PER_PHASE,
            "episodes": len(stream),
            "operator_shift": "same passive context keys; V1<->V2 causal meaning remapped, V0 unchanged",
        },
        "agents": agents,
        "summary": {
            "full_probe_saving_vs_fast_medium": (
                int(fm["total_diagnostic_probes"]) - int(fms["total_diagnostic_probes"])
            ),
            "full_fractional_probe_saving_vs_fast_medium": 1.0
            - int(fms["total_diagnostic_probes"]) / int(fm["total_diagnostic_probes"]),
            "full_probe_saving_vs_always_active": (
                int(always["total_diagnostic_probes"]) - int(fms["total_diagnostic_probes"])
            ),
            "full_detects_shift_on_first_post_episode": fms["first_post_invalidation_offset"] == 0,
            "full_post_first_cycle_final_errors": int(
                fms["post_first_cycle"]["episodes"]
                * (1.0 - fms["post_first_cycle"]["accuracy"])
            ),
            "cache_only_post_first_cycle_final_errors": int(
                cache["post_first_cycle"]["episodes"]
                * (1.0 - cache["post_first_cycle"]["accuracy"])
            ),
        },
        "classification": (
            "FAST_CAUSAL_RE_GROUNDING_MEDIUM_AUDITED_CACHING_AND_SLOW_PROBE_ORDERING_COMPOSE_"
            "IN_ONE_BOUNDED_OBSERVER_MEDIUM_MEMORY_AMORTIZES_RECURRENT_IDENTIFICATION_SLOW_HISTORY_"
            "REDUCES_THE_REMAINING_PROBE_BILL_AND_FAST_CONTRADICTION_TRIGGERED_INTERVENTION_PREVENTS_"
            "STALE_KEYS_FROM_BECOMING_FINAL_CAUSAL_ERRORS_AFTER_OPERATOR_DRIFT"
        ),
        "claim_boundary": (
            "Constructed finite adaptive-diagnosis result. The medium cache is audited by ordinary task "
            "consequences, the slow prior changes search economics rather than truth, and fast causal probes "
            "repair stale mappings after an abrupt operator remap. Standard cache invalidation, sequential "
            "testing and change-detection language fully explains the mechanism. No result here identifies "
            "a quale, self, intrinsic value or phenomenology."
        ),
    }

    # Exact deterministic receipt for this world.
    assert len(stream) == 288, result
    assert always["accuracy"] == 1.0, result
    assert fm["accuracy"] == 1.0, result
    assert fms["accuracy"] == 1.0, result
    assert int(always["total_diagnostic_probes"]) == 492, result
    assert int(fm["total_diagnostic_probes"]) == 166, result
    assert int(fms["total_diagnostic_probes"]) == 138, result

    # MEDIUM compilation must save substantial work over always-active identification.
    assert int(fm["total_diagnostic_probes"]) < int(always["total_diagnostic_probes"]), result

    # SLOW ordering must add real savings at equal perfect accuracy, or it is ornamental.
    assert int(fms["total_diagnostic_probes"]) < int(fm["total_diagnostic_probes"]), result
    assert int(result["summary"]["full_probe_saving_vs_fast_medium"]) == 28, result

    # The robust cache detects the operator shift on the first post-shift episode and
    # re-grounds before emitting a final wrong causal identity.
    assert fms["first_post_invalidation_offset"] == 0, result
    assert fm["first_post_invalidation_offset"] == 0, result
    assert fms["post_first_cycle"]["accuracy"] == 1.0, result
    assert int(fms["cache_invalidations"]) == 2, result

    # A cache with no invalidation path remains cheaply and repeatedly wrong on hot keys.
    assert cache["post_first_cycle"]["accuracy"] == 1.0 / 3.0, result
    assert int(result["summary"]["cache_only_post_first_cycle_final_errors"]) == 16, result

    # PRIOR_ONLY is cheap but the dominant pre-shift cause becomes almost maximally wrong.
    assert prior["pre_first_cycle"]["accuracy"] == 21.0 / 24.0, result
    assert prior["post_first_cycle"]["accuracy"] == 1.0 / 24.0, result

    # In steady state, all three timescales retain perfect truth while paying less than
    # FAST+MEDIUM and far less than ALWAYS_ACTIVE.
    assert fms["post_steady_last_cycle"]["accuracy"] == 1.0, result
    assert fms["post_steady_last_cycle"]["diagnostic_probes"] == 11.0, result
    assert fm["post_steady_last_cycle"]["diagnostic_probes"] == 12.0, result
    assert always["post_steady_last_cycle"]["diagnostic_probes"] == 42.0, result
    assert fms["final_slow_order"][0] == "V2", result

    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
