import subprocess
import time
import urllib.request
import json
import sys

print('Starting Flask server...')
flask_proc = subprocess.Popen(
    [sys.executable, 'dashboard.py'],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)

print('Waiting for server to train model and start (12s)...')
time.sleep(12)

try:
    print('\n--- GET / ---')
    resp = urllib.request.urlopen('http://localhost:5000/', timeout=5)
    html = resp.read().decode()
    if 'Temporal XAI Cloud Monitor' in html:
        print('[OK] Title is correct.')
    else:
        print('[FAIL] Title incorrect.')

    scenarios = ['normal', 'cpu_spike', 'memory_leak', 'disk_full', 'combined']
    for s in scenarios:
        print(f'\n--- GET /api/scan?scenario={s} ---')
        resp = urllib.request.urlopen(f'http://localhost:5000/api/scan?scenario={s}', timeout=10)
        data = json.loads(resp.read().decode())
        print(f"[OK] Status {resp.status}, Risk Level: {data['prediction']['risk_level']}, Score: {data['prediction']['risk_score']}")
        print(f"     Healing Status: {data['healing']['status']}")
except Exception as e:
    print(f'[ERROR] {e}')
finally:
    print('\nTerminating Flask...')
    flask_proc.terminate()
    flask_proc.wait()
    print('Done.')
