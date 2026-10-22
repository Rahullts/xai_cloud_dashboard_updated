import unittest
import sys
import numpy as np
from flask import Flask
from api import api_bp, init_api_model, _temporal_history, _scenario_state

class TestPhase3EIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Setup Flask test client
        cls.app = Flask(__name__)
        cls.app.register_blueprint(api_bp)
        cls.client = cls.app.test_client()
        init_api_model()
        
    def setUp(self):
        # Reset state before each test
        _temporal_history.clear()
        _scenario_state["scenario"] = None
        _scenario_state["index"] = 0
        _scenario_state["sequence"] = []

    def _warm_up(self, scenario):
        """Helper to run 10 iterations to get past the WARMING_UP phase."""
        for _ in range(10):
            response = self.client.get(f"/api/scan?scenario={scenario}")
            data = response.get_json()
            self.assertEqual(response.status_code, 200)
        return data

    def test_01_normal_scenario(self):
        data = self._warm_up("normal")
        self.assertEqual(data["prediction"]["status"], "LIVE")
        self.assertIn(data["prediction"]["risk_level"], ["LOW", "MEDIUM"]) # Normal should rarely be HIGH
        self.assertEqual(data["healing"]["status"], "Skipped")

    def test_02_cpu_spike_scenario(self):
        # Run until healing is triggered (HIGH/CRITICAL) or max 50 steps
        for _ in range(50):
            response = self.client.get("/api/scan?scenario=cpu_spike")
            data = response.get_json()
            
            if data["healing"]["status"] == "Executed":
                self.assertIn(data["prediction"]["risk_level"], ["HIGH", "CRITICAL"])
                self.assertIsNotNone(data["healing"]["evidence"])
                self.assertIn(data["healing"]["verification"], ["RECOVERED", "INCONCLUSIVE"])
                self.assertEqual(data["healing"]["evidence"]["before"]["risk_level"], data["prediction"]["risk_level"])
                self.assertIn(data["healing"]["evidence"]["after"]["risk_level"], ["LOW", "MEDIUM"])
                self.assertTrue(isinstance(data["healing"]["action"], str))
                return
        self.fail("CPU spike scenario did not trigger healing within 50 steps.")
        
    def test_03_memory_leak_scenario(self):
        for _ in range(60):
            response = self.client.get("/api/scan?scenario=memory_leak")
            data = response.get_json()
            if data["healing"]["status"] == "Executed":
                self.assertIsNotNone(data["healing"]["evidence"])
                self.assertTrue(data["healing"]["evidence"]["after"]["risk_score"] < data["healing"]["evidence"]["before"]["risk_score"])
                return
        self.fail("Memory leak scenario did not trigger healing.")

    def test_04_api_schema(self):
        response = self.client.get("/api/scan?scenario=normal")
        data = response.get_json()
        
        self.assertIn("scenario", data)
        self.assertIn("telemetry", data)
        self.assertIn("prediction", data)
        self.assertIn("xai", data)
        self.assertIn("root_cause", data)
        self.assertIn("decision", data)
        self.assertIn("healing", data)
        
        self.assertIn("risk_score", data["prediction"])
        self.assertIn("top_features", data["xai"])
        
    def test_05_warm_up_behavior(self):
        _temporal_history.clear()
        response = self.client.get("/api/scan?scenario=normal")
        data = response.get_json()
        self.assertEqual(data["prediction"]["status"], "WARMING_UP")
        self.assertEqual(data["decision"]["recommended_action"], "Wait for telemetry buffer to fill")

if __name__ == '__main__':
    unittest.main()
