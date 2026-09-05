"""Reusable primitives distilled from PokeAQuale Gates 14–18.

The research gates ended with a fairly ordinary but useful architecture:

* FAST: buy current causal evidence when needed;
* MEDIUM: cache identities that were causally confirmed;
* SLOW: use historical frequencies to order future probes;
* SAFETY: schedule audits so a cheap cache cannot remain trusted forever.

This module extracts those mechanisms without the qualia vocabulary.  It depends only
on the Python standard library and deliberately keeps the evidence boundary explicit:
a cache hit can be returned as *unverified*, or the caller can supply a validation
operation that purchases current evidence.

The probe contract is intentionally small.  ``probe(h)`` answers the binary question
"is h the current identity?".  Candidates are tested in slow-prior order and the final
remaining candidate is inferred for free after all alternatives are ruled out.

Nothing here can detect a change that produces no observation unless the caller
actually schedules an audit.  Nothing here can reconstruct an unobserved hidden path
from identical audited endpoints.  Those are feature-level stopping lines, not bugs.
"""

from __future__ import annotations

import math
from collections import OrderedDict
from dataclasses import dataclass
from typing import Callable, Dict, Generic, Hashable, Iterable, Optional, Sequence, Tuple, TypeVar


Identity = TypeVar("Identity", bound=Hashable)
Context = TypeVar("Context", bound=Hashable)


@dataclass(frozen=True)
class Resolution(Generic[Identity]):
    """Result of resolving one context to a causal identity."""

    identity: Identity
    source: str
    diagnostic_probes: int
    cache_audits: int
    cache_invalidated: bool
    verified: bool

    @property
    def evidence_cost(self) -> int:
        """Count explicit cache audits plus diagnostic probes."""

        return self.cache_audits + self.diagnostic_probes


class SlowProbePrior(Generic[Identity]):
    """Exponentially decayed empirical prior used only to order probes.

    The prior never decides identity.  It changes search economics: likely identities
    are tested earlier, but current evidence still owns the answer.
    """

    def __init__(self, identities: Sequence[Identity], *, decay: float = 0.9) -> None:
        if not identities:
            raise ValueError("at least one identity is required")
        if len(set(identities)) != len(identities):
            raise ValueError("identities must be unique")
        if not 0.0 < decay < 1.0:
            raise ValueError("decay must be between 0 and 1")
        self._identities: Tuple[Identity, ...] = tuple(identities)
        self.decay = decay
        self._score: Dict[Identity, float] = {identity: 1.0 for identity in self._identities}
        self._tie_rank: Dict[Identity, int] = {
            identity: index for index, identity in enumerate(self._identities)
        }

    def order(self, *, excluded: Iterable[Identity] = ()) -> Tuple[Identity, ...]:
        excluded_set = set(excluded)
        return tuple(
            sorted(
                (identity for identity in self._identities if identity not in excluded_set),
                key=lambda identity: (-self._score[identity], self._tie_rank[identity]),
            )
        )

    def update(self, confirmed: Identity) -> None:
        if confirmed not in self._score:
            raise KeyError(f"unknown identity: {confirmed!r}")
        for identity in self._identities:
            self._score[identity] *= self.decay
        self._score[confirmed] += 1.0

    def scores(self) -> Dict[Identity, float]:
        return dict(self._score)


class LRUIdentityCache(Generic[Context, Identity]):
    """Small LRU cache for context -> causally confirmed identity."""

    def __init__(self, capacity: int) -> None:
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self.capacity = capacity
        self._items: "OrderedDict[Context, Identity]" = OrderedDict()

    def get(self, context: Context) -> Optional[Identity]:
        if context not in self._items:
            return None
        value = self._items.pop(context)
        self._items[context] = value
        return value

    def put(self, context: Context, identity: Identity) -> None:
        if context in self._items:
            self._items.pop(context)
        self._items[context] = identity
        if len(self._items) > self.capacity:
            self._items.popitem(last=False)

    def invalidate(self, context: Context) -> bool:
        return self._items.pop(context, None) is not None

    def snapshot(self) -> Dict[Context, Identity]:
        return dict(self._items)


class BoundedCausalObserver(Generic[Context, Identity]):
    """FAST + MEDIUM + SLOW causal identification with explicit cache auditing.

    ``resolve`` has three important modes:

    * cold context -> active binary identification;
    * cache hit without validator -> cheap but explicitly unverified reuse;
    * cache hit with validator -> audit the cached hypothesis and, on contradiction,
      invalidate it and actively identify among the remaining candidates.

    A validator is evidence.  If validation itself is expensive in the application,
    ``Resolution.cache_audits`` makes that cost visible rather than pretending it was
    free.
    """

    def __init__(
        self,
        identities: Sequence[Identity],
        *,
        cache_capacity: int = 32,
        prior_decay: float = 0.9,
    ) -> None:
        if not identities:
            raise ValueError("at least one identity is required")
        if len(set(identities)) != len(identities):
            raise ValueError("identities must be unique")
        self.identities: Tuple[Identity, ...] = tuple(identities)
        self.cache = LRUIdentityCache[Context, Identity](cache_capacity)
        self.prior = SlowProbePrior[Identity](self.identities, decay=prior_decay)

    def _identify(
        self,
        probe: Callable[[Identity], bool],
        *,
        excluded: Iterable[Identity] = (),
    ) -> Tuple[Identity, int]:
        candidates = self.prior.order(excluded=excluded)
        if not candidates:
            raise RuntimeError("no candidate identities remain")
        if len(candidates) == 1:
            return candidates[0], 0

        # Probe every candidate except the last.  If all are false, the final candidate
        # is determined by elimination and does not require another paid binary query.
        for probes, candidate in enumerate(candidates[:-1], start=1):
            if bool(probe(candidate)):
                return candidate, probes
        return candidates[-1], len(candidates) - 1

    def resolve(
        self,
        context: Context,
        probe: Callable[[Identity], bool],
        *,
        validate_cached: Optional[Callable[[Identity], bool]] = None,
        force_reidentify: bool = False,
    ) -> Resolution[Identity]:
        cached = self.cache.get(context)

        if cached is not None and not force_reidentify:
            if validate_cached is None:
                return Resolution(
                    identity=cached,
                    source="cache_unverified",
                    diagnostic_probes=0,
                    cache_audits=0,
                    cache_invalidated=False,
                    verified=False,
                )

            if bool(validate_cached(cached)):
                self.prior.update(cached)
                return Resolution(
                    identity=cached,
                    source="cache_verified",
                    diagnostic_probes=0,
                    cache_audits=1,
                    cache_invalidated=False,
                    verified=True,
                )

            # The failed validation is current evidence that the cached identity is not
            # the answer.  Reuse that negative fact and search only the remaining set.
            self.cache.invalidate(context)
            identity, probes = self._identify(probe, excluded=(cached,))
            self.cache.put(context, identity)
            self.prior.update(identity)
            return Resolution(
                identity=identity,
                source="cache_invalidated_then_active",
                diagnostic_probes=probes,
                cache_audits=1,
                cache_invalidated=True,
                verified=True,
            )

        identity, probes = self._identify(probe)
        self.cache.put(context, identity)
        self.prior.update(identity)
        return Resolution(
            identity=identity,
            source="forced_active" if force_reidentify else "active_cold",
            diagnostic_probes=probes,
            cache_audits=0,
            cache_invalidated=False,
            verified=True,
        )


class HazardAuditScheduler:
    """Historical change-hazard scheduler with an optional hard maximum audit gap.

    ``due(step)`` tells the caller when to buy an audit.  After performing it, call
    ``record(step, changed=...)``.  A detected change updates the expected interval;
    a negative audit advances a short local search step once the expected boundary has
    been reached.

    ``max_gap`` is a safety policy, not a statistical conclusion.  It bounds the time
    between audits but cannot guarantee event-complete capture if the hidden world can
    change more than once inside that bound.
    """

    def __init__(
        self,
        *,
        initial_interval: float,
        target_fraction: float = 0.75,
        search_fraction: float = 0.125,
        smoothing: float = 0.5,
        max_gap: Optional[int] = None,
        start_step: int = 0,
    ) -> None:
        if initial_interval <= 0:
            raise ValueError("initial_interval must be positive")
        if not 0.0 < target_fraction <= 1.0:
            raise ValueError("target_fraction must be in (0, 1]")
        if not 0.0 < search_fraction <= 1.0:
            raise ValueError("search_fraction must be in (0, 1]")
        if not 0.0 < smoothing <= 1.0:
            raise ValueError("smoothing must be in (0, 1]")
        if max_gap is not None and max_gap <= 0:
            raise ValueError("max_gap must be positive")

        self.expected_interval = float(initial_interval)
        self.target_fraction = target_fraction
        self.search_fraction = search_fraction
        self.smoothing = smoothing
        self.max_gap = max_gap
        self.last_detection = start_step
        self.last_audit = start_step
        self._target = start_step + self._target_delay()
        self.next_audit = self._bounded_next(self._target)

    def _target_delay(self) -> int:
        return max(1, math.ceil(self.target_fraction * self.expected_interval))

    def _search_delay(self) -> int:
        return max(1, math.ceil(self.search_fraction * self.expected_interval))

    def _bounded_next(self, target: int) -> int:
        if self.max_gap is None:
            return target
        return min(target, self.last_audit + self.max_gap)

    def due(self, step: int) -> bool:
        return step >= self.next_audit

    def record(self, step: int, *, changed: bool) -> None:
        if step < self.next_audit:
            raise ValueError("record called before the scheduled audit")
        if step < self.last_audit:
            raise ValueError("steps must be non-decreasing")

        self.last_audit = step
        if changed:
            observed_interval = step - self.last_detection
            if observed_interval <= 0:
                raise ValueError("detected-change interval must be positive")
            self.expected_interval = (
                (1.0 - self.smoothing) * self.expected_interval
                + self.smoothing * observed_interval
            )
            self.last_detection = step
            self._target = step + self._target_delay()
        elif step >= self._target:
            self._target = step + self._search_delay()

        self.next_audit = self._bounded_next(self._target)
