# config.py
# Reusable configuration and constants for the XAI Cloud Platform
import os

HOST = os.environ.get("HOST", "0.0.0.0")
PORT = int(os.environ.get("PORT", 5000))
DEBUG = os.environ.get("DEBUG", "False").lower() in ("true", "1", "yes")
MODEL_SAMPLES = int(os.environ.get("MODEL_SAMPLES", 200))

# Supported backend simulation scenarios
SCENARIOS = [
    "normal",
    "cpu_spike",
    "memory_leak",
    "disk_full",
    "network_issue",
    "combined"
]
