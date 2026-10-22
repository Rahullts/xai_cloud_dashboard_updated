import tempfile
import unittest
from pathlib import Path

from detector import FEATURES, metrics_to_vector, predict, train_model
from explainer import compute_deviations, explain
from healer import select_recovery_actions
from monitor import collect_samples, simulate_anomaly, simulate_normal


class MonitoringTests(unittest.TestCase):
    def test_seed_makes_samples_reproducible(self):
        self.assertEqual(collect_samples(12, seed=17), collect_samples(12, seed=17))

    def test_supported_scenarios_return_expected_features(self):
        for scenario in ("cpu_spike", "memory_leak", "disk_full", "network_issue", "combined"):
            with self.subTest(scenario=scenario):
                metrics = simulate_anomaly(scenario)
                self.assertEqual(set(FEATURES), set(metrics))

    def test_unknown_scenario_is_rejected(self):
        with self.assertRaises(ValueError):
            simulate_anomaly("not-a-scenario")


class DetectorTests(unittest.TestCase):
    def test_missing_or_non_finite_metrics_are_rejected(self):
        metrics = simulate_normal()
        with self.assertRaises(ValueError):
            metrics_to_vector({"cpu_percent": metrics["cpu_percent"]})
        metrics["disk_percent"] = float("nan")
        with self.assertRaises(ValueError):
            metrics_to_vector(metrics)

    def test_vector_has_stable_feature_order(self):
        metrics = {name: float(index) for index, name in enumerate(FEATURES)}
        self.assertEqual(metrics_to_vector(metrics), [0.0, 1.0, 2.0, 3.0, 4.0])

    def test_training_is_reproducible_for_fixed_seed(self):
        first = train_model(n_samples=40, random_state=23)
        second = train_model(n_samples=40, random_state=23)
        sample = simulate_anomaly("cpu_spike")
        self.assertEqual(predict(first, sample), predict(second, sample))


class ExplanationAndRecoveryTests(unittest.TestCase):
    def test_explanation_labels_heuristic_method(self):
        metrics = simulate_anomaly("cpu_spike")
        report = explain(metrics, "ANOMALY", -0.1)
        self.assertIn("heuristic", report.lower())
        self.assertIn("not model attributions", report.lower())
        self.assertEqual(len(compute_deviations(metrics)), len(FEATURES))

    def test_normal_state_has_no_recovery_recommendations(self):
        self.assertEqual(select_recovery_actions(simulate_normal(), "NORMAL"), [])

    def test_high_cpu_recommends_but_does_not_execute(self):
        metrics = simulate_normal()
        metrics["cpu_percent"] = 99.0
        actions = select_recovery_actions(metrics, "ANOMALY")
        self.assertIn("restart_service", [action["action"] for action in actions])
        self.assertIn("scale_out", [action["action"] for action in actions])
        self.assertTrue(all("action" in action and "reason" in action for action in actions))


class DashboardApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from dashboard import app
        cls.app = app

    def setUp(self):
        self.client = self.app.test_client()

    def test_selected_scenario_runs_through_api(self):
        response = self.client.get("/api/scan?scenario=cpu")
        self.assertEqual(response.status_code, 200)
        body = response.get_json()
        self.assertEqual(body["scenario"], "cpu")
        self.assertIn(body["label"], {"NORMAL", "ANOMALY"})
        self.assertEqual(body["recovery_mode"], "simulation_only")
        self.assertIn("latency_ms", body["metrics"])
        self.assertIn("explanation", body)
        self.assertIsInstance(body["actions"], list)

    def test_invalid_scenario_returns_400(self):
        response = self.client.get("/api/scan?scenario=unknown")
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.get_json())


if __name__ == "__main__":
    unittest.main()
