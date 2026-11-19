"""Small synthetic tests; no human psychological claims."""
import unittest
import numpy as np
from simulate_identification import Parameters, experiment, fit, simulate


class SyntheticIdentificationTests(unittest.TestCase):
    def test_seed_reproducibility(self):
        self.assertEqual(simulate(123, 3, 6, ("full", "partial")),
                         simulate(123, 3, 6, ("full", "partial")))

    def test_full_information_accurate_belief_not_equal_emotion(self):
        rows = simulate(42, 5, 8, ("full", "full"))
        self.assertTrue(all(abs(r.inferred_benign_intent - r.actual_benign_intent) < 1e-12 for r in rows))
        # Equal access to intentions does not force uniform affect between agents.
        self.assertTrue(any(abs(rows[k].next_anger - rows[k+1].next_anger) > .01
                            for k in range(0, len(rows), 2)))

    def test_reasoning_errors_are_dynamics_not_missing_rows(self):
        rows = simulate(42, 10, 9, ("biased", "full"))
        biased = [r for r in rows if r.agent == 0]
        partner = [r for r in rows if r.agent == 1]
        self.assertGreater(np.mean([abs(r.inferred_benign_intent - r.actual_benign_intent) for r in biased]), .10)
        self.assertTrue(all(abs(r.inferred_benign_intent - r.actual_benign_intent) < 1e-12 for r in partner))
        self.assertEqual(len(rows), 180)

    def test_recover_truth_in_fully_observed_simulation(self):
        rows = simulate(1001, 150, 35, ("full", "full"))
        for component in ("anger", "warmth"):
            estimate, rank = fit(rows, component, "inferred")
            self.assertEqual(rank, 5)
            np.testing.assert_allclose(estimate, getattr(Parameters(), component), atol=.015)

    def test_noisy_observation_can_break_naive_parameter_recovery(self):
        result = experiment(train_episodes=80, test_episodes=20, steps=25)
        for component in ("anger", "warmth"):
            errors = result["measurement_noise_check"]["coefficient_l2_error"][component]
            self.assertGreater(errors["noisy_observations"], errors["clean_latent"])

    def test_information_regime_transfer(self):
        results = experiment(train_episodes=65, test_episodes=25, steps=25)
        for c in ("anger", "warmth"):
            r = results["heldout_rmse"]["biased_partial"][c]
            self.assertLess(r["inferred"], r["actual"])
        self.assertGreater(results["paired_peer_effect"]["mean_sum_abs_affect_difference_agent_1"], .001)


if __name__ == "__main__":
    unittest.main()
