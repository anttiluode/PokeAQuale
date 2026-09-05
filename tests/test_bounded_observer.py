import unittest

from bounded_observer import BoundedCausalObserver, HazardAuditScheduler


class BoundedObserverTests(unittest.TestCase):
    def test_cold_cache_hit_and_drift_repair(self):
        world = {"driver": "V1"}
        observer = BoundedCausalObserver(
            ("V0", "V1", "V2"),
            cache_capacity=2,
            prior_decay=0.9,
        )

        def probe(candidate):
            return candidate == world["driver"]

        def validate(candidate):
            return candidate == world["driver"]

        cold = observer.resolve("K", probe)
        self.assertEqual(cold.identity, "V1")
        self.assertEqual(cold.source, "active_cold")
        self.assertEqual(cold.diagnostic_probes, 2)
        self.assertTrue(cold.verified)

        hit = observer.resolve("K", probe, validate_cached=validate)
        self.assertEqual(hit.identity, "V1")
        self.assertEqual(hit.source, "cache_verified")
        self.assertEqual(hit.diagnostic_probes, 0)
        self.assertEqual(hit.cache_audits, 1)
        self.assertFalse(hit.cache_invalidated)

        # A cache can be reused without evidence, but the result is explicitly marked
        # unverified rather than silently treated as current truth.
        cheap = observer.resolve("K", probe)
        self.assertEqual(cheap.identity, "V1")
        self.assertEqual(cheap.source, "cache_unverified")
        self.assertFalse(cheap.verified)
        self.assertEqual(cheap.evidence_cost, 0)

        # Operator drift makes the old key stale. Validation supplies one negative fact;
        # active search then excludes V1 and identifies V2 from the remaining set.
        world["driver"] = "V2"
        repaired = observer.resolve("K", probe, validate_cached=validate)
        self.assertEqual(repaired.identity, "V2")
        self.assertEqual(repaired.source, "cache_invalidated_then_active")
        self.assertEqual(repaired.cache_audits, 1)
        self.assertEqual(repaired.diagnostic_probes, 1)
        self.assertTrue(repaired.cache_invalidated)
        self.assertTrue(repaired.verified)
        self.assertEqual(observer.cache.snapshot(), {"K": "V2"})

    def test_slow_prior_changes_order_not_truth(self):
        observer = BoundedCausalObserver(("A", "B", "C"), cache_capacity=2)

        # Repeatedly confirm C so it becomes the first slow-prior candidate.
        for i in range(5):
            result = observer.resolve(
                f"train-{i}",
                lambda candidate: candidate == "C",
                force_reidentify=True,
            )
            self.assertEqual(result.identity, "C")

        self.assertEqual(observer.prior.order()[0], "C")

        # The world is now B. The stale prior may ask C first, but it cannot force C.
        asked = []

        def probe(candidate):
            asked.append(candidate)
            return candidate == "B"

        result = observer.resolve("shift", probe, force_reidentify=True)
        self.assertEqual(asked[0], "C")
        self.assertEqual(result.identity, "B")
        self.assertTrue(result.verified)

    def test_lru_capacity(self):
        observer = BoundedCausalObserver((0, 1), cache_capacity=2)
        observer.resolve("a", lambda candidate: candidate == 0)
        observer.resolve("b", lambda candidate: candidate == 1)
        observer.resolve("a", lambda candidate: candidate == 0)  # touch a
        observer.resolve("c", lambda candidate: candidate == 0)
        self.assertEqual(set(observer.cache.snapshot()), {"a", "c"})

    def test_hazard_scheduler_respects_max_gap(self):
        scheduler = HazardAuditScheduler(initial_interval=40, max_gap=16)
        audit_times = []
        change_times = {40, 80}

        for step in range(1, 101):
            if scheduler.due(step):
                audit_times.append(step)
                # This toy reports a change only if one occurred after the previous audit.
                previous = audit_times[-2] if len(audit_times) >= 2 else 0
                changed = any(previous < change <= step for change in change_times)
                scheduler.record(step, changed=changed)

        boundaries = [0] + audit_times + [101]
        self.assertLessEqual(
            max(b - a for a, b in zip(boundaries, boundaries[1:])),
            16,
        )
        self.assertGreater(len(audit_times), 0)

    def test_scheduler_refuses_free_early_record(self):
        scheduler = HazardAuditScheduler(initial_interval=40, max_gap=16)
        with self.assertRaises(ValueError):
            scheduler.record(1, changed=False)


if __name__ == "__main__":
    unittest.main()
