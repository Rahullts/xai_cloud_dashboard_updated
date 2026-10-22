# config.py
# Reusable configuration and constants for the XAI Cloud Platform

PORT = 5000
DEBUG = False
MODEL_SAMPLES = 200

# Supported backend simulation scenarios
SCENARIOS = [
    "normal",
    "cpu_spike",
    "memory_leak",
    "disk_full",
    "network_issue",
    "combined"
]
