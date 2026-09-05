#!/usr/bin/env python3
"""Small runnable example for bounded_observer.py.

The same passive context key is reused while its hidden causal driver changes.  The
observer first buys active evidence, then reuses a verified cache hit, then invalidates
and repairs the stale entry after drift.
"""

from bounded_observer import BoundedCausalObserver


world = {"driver": "V1"}
observer = BoundedCausalObserver(("V0", "V1", "V2"), cache_capacity=4)


def probe(candidate: str) -> bool:
    print(f"  diagnostic probe: is driver {candidate}?", end=" ")
    answer = candidate == world["driver"]
    print(answer)
    return answer


def validate(candidate: str) -> bool:
    print(f"  cache audit: does cached {candidate} still predict the consequence?", end=" ")
    answer = candidate == world["driver"]
    print(answer)
    return answer


def show(label: str, result) -> None:
    print(f"{label}: {result.identity}")
    print(
        f"  source={result.source} verified={result.verified} "
        f"diagnostic_probes={result.diagnostic_probes} "
        f"cache_audits={result.cache_audits} evidence_cost={result.evidence_cost}"
    )


print("FIRST ENCOUNTER — buy evidence")
show("resolved", observer.resolve("same-passive-key", probe))

print("\nRECURRENCE — audit and reuse medium cache")
show(
    "resolved",
    observer.resolve("same-passive-key", probe, validate_cached=validate),
)

print("\nSILENT TRUST — zero-cost reuse is explicitly unverified")
show("resolved", observer.resolve("same-passive-key", probe))

print("\nOPERATOR DRIFT — same key, new cause")
world["driver"] = "V2"
show(
    "resolved",
    observer.resolve("same-passive-key", probe, validate_cached=validate),
)

print("\nslow probe order:", observer.prior.order())
print("cache:", observer.cache.snapshot())
