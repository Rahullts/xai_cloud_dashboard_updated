import unittest
import numpy as np

# Mock classes for testing
class MockModel:
    def __init__(self):
        self.coef_ = np.array([[1.5, -0.5, 2.0, 0.0]])

class MockScaler:
    def transform(self, X):
        return X

from xai_explainer import get_feature_attributions
from root_cause import get_feature_group, determine_root_cause
from decision_engine import get_risk_level, get_recommended_action, generate_explanation

class TestXAIDecisionLayer(unittest.TestCase):
    
    def setUp(self):
        self.model = MockModel()
        self.scaler = MockScaler()
        self.features = ["cpu_percent_current", "memory_percent_mean_5", "disk_percent_std_10", "net_bytes_recv_rate_slope_5"]
        self.raw_row = {
            "cpu_percent_current": 10.0,
            "memory_percent_mean_5": 20.0,
            "disk_percent_std_10": 5.0,
            "net_bytes_recv_rate_slope_5": 1.0,
            # Leakage fields (should be ignored by explainer)
            "target_failure_within_10": 1,
            "failure_status": 0
        }

    def test_feature_attributions(self):
        attrs = get_feature_attributions(self.model, self.scaler, self.features, self.raw_row)
        self.assertEqual(len(attrs), 4)
        
        # CPU contrib = 10.0 * 1.5 = 15.0 (highest abs)
        self.assertEqual(attrs[0]["feature"], "cpu_percent_current")
        self.assertEqual(attrs[0]["contribution"], 15.0)
        self.assertEqual(attrs[0]["rank"], 1)
        self.assertEqual(attrs[0]["direction"], "positive")
        self.assertEqual(attrs[0]["human_readable_name"], "Cpu Current")
        
        # Memory contrib = 20.0 * -0.5 = -10.0
        self.assertEqual(attrs[1]["feature"], "memory_percent_mean_5")
        self.assertEqual(attrs[1]["abs_contribution"], 10.0)
        
    def test_root_cause_cpu(self):
        attrs = [
            {'feature': 'cpu_percent_mean_10', 'contribution': 5.0},
            {'feature': 'memory_percent_mean_10', 'contribution': 1.0},
        ]
        rc, scores = determine_root_cause(attrs)
        self.assertEqual(rc, "CPU Spike")
        self.assertTrue(scores['CPU'] > 0.8)

    def test_root_cause_mixed(self):
        attrs = [
            {'feature': 'cpu_percent_mean_10', 'contribution': 5.0},
            {'feature': 'memory_percent_mean_10', 'contribution': 5.0},
        ]
        rc, _ = determine_root_cause(attrs)
        self.assertEqual(rc, "Combined Failure")

    def test_decision_mapping(self):
        self.assertEqual(get_risk_level(0.9), "CRITICAL")
        self.assertEqual(get_risk_level(0.4), "MEDIUM")
        
        action = get_recommended_action("Memory Leak")
        self.assertIn("Restart affected service", action)
        
        action_unknown = get_recommended_action("Unknown / Mixed")
        self.assertIn("Alert operator", action_unknown)
        
    def test_explanation_generation(self):
        attrs = [
            {'feature': 'cpu_percent_mean_10', 'human_readable_name': 'CPU 10-step average', 'raw_value': 80.0, 'contribution': 5.0, 'direction': 'positive'},
        ]
        text = generate_explanation(0.75, "CPU Spike", attrs)
        self.assertIn("HIGH failure risk", text)
        self.assertIn("CPU SPIKE", text)
        self.assertIn("CPU 10-step average (80.00)", text)

if __name__ == "__main__":
    unittest.main()
