# =============================================================
# dashboard.py — Flask Web Dashboard (Orange Theme v2.0)
# Run: python dashboard.py
# Open: http://localhost:5000
# =============================================================

from flask import Flask, render_template_string, jsonify, request

from monitor   import simulate_normal, simulate_anomaly
from detector  import train_model, predict
from explainer import explain
from healer    import select_recovery_actions

app = Flask(__name__)

# Train once on startup
print("[dashboard] Training model...")
model = train_model(n_samples=200)
print("[dashboard] Model ready.")

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>XAI Self-Healing Cloud Dashboard</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    *{box-sizing:border-box;margin:0;padding:0}
    body{font-family:'Segoe UI',system-ui,sans-serif;background:#0e1420;color:#e8ecf4;min-height:100vh}
    .topbar{background:#161d2e;border-bottom:1px solid #2a3550;padding:14px 24px;display:flex;align-items:center;justify-content:space-between}
    .logo-icon{width:34px;height:34px;background:#f97316;border-radius:8px;display:flex;align-items:center;justify-content:center}
    #pulse-dot{width:8px;height:8px;border-radius:50%;background:#22c55e;animation:pulse 2s infinite}
    @keyframes pulse{0%,100%{opacity:1}50%{opacity:.4}}
    .main{padding:20px 24px;display:flex;flex-direction:column;gap:16px}
    .card{background:#161d2e;border:1px solid #2a3550;border-radius:14px;padding:18px 20px}
    .card-title{font-size:11px;font-weight:600;color:#f97316;letter-spacing:0.08em;text-transform:uppercase;margin-bottom:14px}
    .control-grid{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:14px}
    .field-label{font-size:11px;color:#9aa3b8;display:block;margin-bottom:5px;letter-spacing:0.04em}
    input[type=text],select{width:100%;background:#1c2540;border:1px solid #2a3550;border-radius:8px;padding:8px 10px;font-size:13px;color:#e8ecf4;outline:none}
    input[type=range]{flex:1;accent-color:#f97316}
    .slider-row{display:flex;align-items:center;gap:8px}
    .slider-val{font-size:13px;color:#fb923c;font-weight:600;min-width:32px}
    .toggle-track{position:relative;display:inline-block;width:40px;height:22px}
    .toggle-track input{opacity:0;width:0;height:0}
    .toggle-bg{position:absolute;inset:0;border-radius:11px;cursor:pointer;transition:background .2s;background:#f97316}
    .toggle-knob{position:absolute;top:3px;left:3px;width:16px;height:16px;background:#fff;border-radius:50%;transition:transform .2s;transform:translateX(18px)}
    .scenario-row{display:flex;flex-wrap:wrap;gap:8px;border-top:1px solid #2a3550;padding-top:14px}
    .btn-s{border-radius:8px;font-size:12px;cursor:pointer;font-weight:500;padding:7px 14px;transition:opacity .15s}
    .btn-s:hover{opacity:.82}
    #status-banner{border-radius:10px;padding:12px 16px;display:flex;align-items:center;justify-content:space-between}
    #metric-cards{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}
    .mc{background:#1c2540;border:1px solid #2a3550;border-radius:10px;padding:14px 14px 12px}
    .mc.alert{border-color:#ef444466}
    .two-col{display:grid;grid-template-columns:1fr 1fr;gap:14px}
    #xai-panel,#actions-panel{font-size:12px;color:#9aa3b8;line-height:1.7}
    #log-panel{font-size:11px;font-family:'Courier New',monospace;color:#6b7590;max-height:130px;overflow-y:auto;display:flex;flex-direction:column;gap:3px}
    .action-row{display:flex;align-items:center;gap:10px;padding:7px 10px;background:#1c2540;border-radius:7px;margin-bottom:6px;border:1px solid #2a3550}
  </style>
</head>
<body>
<div class="topbar">
  <div style="display:flex;align-items:center;gap:12px">
    <div class="logo-icon">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.5" stroke-linecap="round">
        <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>
      </svg>
    </div>
    <div>
      <div style="font-size:15px;font-weight:600;color:#e8ecf4;letter-spacing:0.01em">XAI Cloud Monitor</div>
      <div style="font-size:11px;color:#6b7590;letter-spacing:0.03em">SELF-HEALING SYSTEM v2.0</div>
    </div>
  </div>
  <div style="display:flex;align-items:center;gap:16px">
    <div style="display:flex;align-items:center;gap:6px;font-size:12px;color:#9aa3b8">
      <div id="pulse-dot"></div>
      <span id="status-label">System Online</span>
    </div>
    <div id="clock" style="font-size:12px;color:#6b7590">--:--:--</div>
  </div>
</div>

<div class="main">
  <div class="card">
    <div class="card-title">Control Panel</div>
    <div class="control-grid">
      <div>
        <label class="field-label">Application Name</label>
        <input id="app-name" type="text" value="web-app-server">
      </div>
      <div>
        <label class="field-label">Environment</label>
        <select id="env-select">
          <option>Production</option><option>Staging</option><option>Development</option>
        </select>
      </div>
      <div>
        <label class="field-label">CPU threshold (%)</label>
        <div class="slider-row">
          <input id="cpu-thresh" type="range" min="50" max="95" value="85" step="1">
          <span id="cpu-thresh-val" class="slider-val">85%</span>
        </div>
      </div>
      <div>
        <label class="field-label">Memory threshold (%)</label>
        <div class="slider-row">
          <input id="mem-thresh" type="range" min="50" max="95" value="85" step="1">
          <span id="mem-thresh-val" class="slider-val">85%</span>
        </div>
      </div>
      <div>
        <label class="field-label">Scan interval</label>
        <select id="interval-select">
          <option value="3000">Every 3 seconds</option>
          <option value="5000" selected>Every 5 seconds</option>
          <option value="10000">Every 10 seconds</option>
        </select>
      </div>
      <div>
        <label class="field-label">Auto-heal</label>
        <div style="display:flex;align-items:center;gap:10px;padding:8px 0">
          <label class="toggle-track">
            <input type="checkbox" id="auto-heal" checked>
            <span class="toggle-bg" id="toggle-bg"></span>
            <span class="toggle-knob" id="toggle-knob"></span>
          </label>
          <span style="font-size:13px;color:#9aa3b8" id="auto-heal-label">Enabled</span>
        </div>
      </div>
    </div>
    <div class="scenario-row">
      <div style="font-size:11px;color:#9aa3b8;width:100%;margin-bottom:4px;letter-spacing:0.04em">Inject scenario</div>
      <button class="btn-s" style="background:#1c2540;border:1px solid #3a4a6a;color:#9aa3b8" onclick="runScenario('normal')">Normal</button>
      <button class="btn-s" style="background:#7c3a0a;border:1px solid #f97316;color:#fdba74" onclick="runScenario('cpu')">CPU Spike</button>
      <button class="btn-s" style="background:#1c2540;border:1px solid #3b82f6;color:#93c5fd" onclick="runScenario('memory')">Memory Leak</button>
      <button class="btn-s" style="background:#1c2540;border:1px solid #eab308;color:#fde047" onclick="runScenario('disk')">Disk Full</button>
      <button class="btn-s" style="background:#1c2540;border:1px solid #8b5cf6;color:#c4b5fd" onclick="runScenario('network')">Network Issue</button>
      <button class="btn-s" style="background:#3b1a1a;border:1px solid #ef4444;color:#fca5a5" onclick="runScenario('combined')">Combined Failure</button>
    </div>
  </div>

  <div id="status-banner" style="background:#0f1e13;border:1px solid #22c55e">
    <div style="display:flex;align-items:center;gap:10px">
      <div id="banner-icon" style="width:10px;height:10px;border-radius:50%;background:#22c55e"></div>
      <span id="banner-text" style="font-size:14px;font-weight:600;color:#22c55e">System Normal</span>
      <span id="banner-sub" style="font-size:12px;color:#9aa3b8">All metrics within safe range</span>
    </div>
    <div style="font-size:12px;color:#9aa3b8">Score: <span id="banner-score-val" style="color:#fb923c;font-weight:600">+0.15</span></div>
  </div>

  <div id="metric-cards"></div>

  <div class="two-col">
    <div class="card"><div class="card-title">XAI Explanation</div><div id="xai-panel"></div></div>
    <div class="card"><div class="card-title">Recovery Actions</div><div id="actions-panel"></div></div>
  </div>

  <div class="card">
    <div class="card-title">Recovery Log</div>
    <div id="log-panel"></div>
  </div>
</div>

<script>
const FEATURES=['cpu_percent','memory_percent','disk_percent','net_bytes_sent','net_bytes_recv','latency_ms'];
const LABELS={cpu_percent:'CPU Usage',memory_percent:'Memory',disk_percent:'Disk',net_bytes_sent:'Net Sent (MB)',net_bytes_recv:'Net Recv (MB)',latency_ms:'Latency (ms)'};
const NORMS={cpu_percent:{mean:25,std:10},memory_percent:{mean:42,std:10},disk_percent:{mean:35,std:10},net_bytes_sent:{mean:5,std:3},net_bytes_recv:{mean:5,std:3},latency_ms:{mean:30,std:8}};
const UNITS={cpu_percent:'%',memory_percent:'%',disk_percent:'%',net_bytes_sent:' MB',net_bytes_recv:' MB',latency_ms:' ms'};
let currentScenario='normal',scanTimer=null,logLines=[],healCount=0;
function rnd(a,b){return Math.random()*(b-a)+a;}
function getMetrics(s){
  let m={cpu_percent:rnd(10,40),memory_percent:rnd(30,55),disk_percent:rnd(20,50),net_bytes_sent:rnd(1,10),net_bytes_recv:rnd(1,10),latency_ms:rnd(20,45)};
  if(s==='cpu') m.cpu_percent=rnd(88,98);
  else if(s==='memory') m.memory_percent=rnd(88,97);
  else if(s==='disk') m.disk_percent=rnd(88,98);
  else if(s==='network'){m.net_bytes_sent=rnd(45,70);m.latency_ms=rnd(180,400);}
  else if(s==='combined'){m.cpu_percent=rnd(85,97);m.memory_percent=rnd(82,95);m.disk_percent=rnd(80,94);}
  return m;
}
function zScore(f,v){return((v-NORMS[f].mean)/NORMS[f].std).toFixed(1);}
function isAnomaly(m){
  const cpuT=parseInt(document.getElementById('cpu-thresh').value);
  const memT=parseInt(document.getElementById('mem-thresh').value);
  return m.cpu_percent>cpuT||m.memory_percent>memT||m.disk_percent>85||m.net_bytes_sent>40||m.latency_ms>150;
}
function anomalyScore(m){
  const devs=FEATURES.map(f=>Math.abs((m[f]-NORMS[f].mean)/NORMS[f].std));
  const s=0.15-(Math.max(...devs)-1)*0.06;
  return Math.max(-0.25,Math.min(0.20,s)).toFixed(4);
}
function renderMetricCards(m,anomaly){
  const cpuT=parseInt(document.getElementById('cpu-thresh').value);
  const memT=parseInt(document.getElementById('mem-thresh').value);
  const thresh={cpu_percent:cpuT,memory_percent:memT,disk_percent:85,net_bytes_sent:40,net_bytes_recv:40,latency_ms:150};
  document.getElementById('metric-cards').innerHTML=FEATURES.map(f=>{
    const val=m[f],pct=f.includes('percent')?val:f==='latency_ms'?Math.min(val/200*100,100):Math.min(val/60*100,100);
    const over=val>thresh[f],barColor=over?'#ef4444':val>thresh[f]*0.8?'#eab308':'#f97316';
    return `<div class="mc${over?' alert':''}">
      <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:8px">
        <div style="font-size:11px;color:#6b7590;letter-spacing:0.04em">${LABELS[f]}</div>
        <div style="font-size:10px;padding:2px 6px;border-radius:4px;background:${over?'#3b1a1a':'#1c2540'};color:${over?'#fca5a5':'#6b7590'}">z=${zScore(f,val)}</div>
      </div>
      <div style="font-size:22px;font-weight:700;color:${over?'#ef4444':'#e8ecf4'};letter-spacing:-0.02em;margin-bottom:8px">${val.toFixed(1)}<span style="font-size:12px;font-weight:400;color:#6b7590">${UNITS[f]}</span></div>
      <div style="height:3px;background:#2a3550;border-radius:2px"><div style="height:3px;border-radius:2px;background:${barColor};width:${Math.min(pct,100).toFixed(1)}%;transition:width .5s"></div></div>
    </div>`;
  }).join('');
}
function renderXAI(m,anomaly,score,serverReport=''){
  const panel=document.getElementById('xai-panel');
  panel.textContent=serverReport || 'Server explanation unavailable.';
  panel.style.whiteSpace='pre-wrap';
  panel.style.fontFamily="'Cascadia Code','Consolas',monospace";
  panel.style.fontSize='11px';
  panel.style.lineHeight='1.6';
}function renderActions(m,anomaly,serverActions=[]){
  if(!anomaly || !serverActions.length){
    document.getElementById('actions-panel').innerHTML=`<div style="display:flex;align-items:center;gap:8px;color:#22c55e">No recovery recommendation returned by the server</div>`;
    return;
  }
  const labels={
    restart_service:'Recommend restart service',
    scale_out:'Recommend scale-out',
    inspect_memory_pressure:'Inspect memory pressure',
    restart_worker:'Recommend worker restart',
    review_disk_cleanup:'Review disk cleanup',
    notify_operator:'Recommend operator notification',
    manual_review:'Manual review recommended'
  };
  const colors=['#f97316','#fb923c','#3b82f6','#eab308','#8b5cf6'];
  const html=serverActions.map((action,index)=>{
    const label=labels[action.action]||action.action;
    const color=colors[index%colors.length];
    return `<div class="action-row"><span style="color:${color};font-size:14px;min-width:16px;text-align:center">•</span><span style="flex:1;color:#c8d0e0;font-size:12px">${label}<div style="font-size:10px;color:#6b7590">${action.reason}</div></span><span style="font-size:10px;padding:2px 8px;border-radius:4px;background:#2a1800;color:#fb923c;font-weight:600">PROPOSED</span></div>`;
  }).join('');
  document.getElementById('actions-panel').innerHTML=html;
}function renderBanner(anomaly,score){
  const env=document.getElementById('env-select').value;
  const b=document.getElementById('status-banner'),bi=document.getElementById('banner-icon'),bt=document.getElementById('banner-text'),bs=document.getElementById('banner-sub');
  document.getElementById('banner-score-val').textContent=score;
  if(anomaly){
    b.style.background='#2a0a0a';b.style.borderColor='#ef4444';bi.style.background='#ef4444';bt.style.color='#ef4444';bt.textContent='Anomaly Detected';bs.textContent=`${env} environment — recovery plan proposed (simulation only)`;
    document.getElementById('status-label').textContent='Alert Active';document.getElementById('pulse-dot').style.background='#ef4444';
  } else {
    b.style.background='#0f1e13';b.style.borderColor='#22c55e';bi.style.background='#22c55e';bt.style.color='#22c55e';bt.textContent='System Normal';bs.textContent='All metrics within safe range';
    document.getElementById('status-label').textContent='System Online';document.getElementById('pulse-dot').style.background='#22c55e';
  }
}
function addLog(msg){
  const n=new Date(),ts=`${n.getHours().toString().padStart(2,'0')}:${n.getMinutes().toString().padStart(2,'0')}:${n.getSeconds().toString().padStart(2,'0')}`;
  logLines.unshift(`[${ts}]  ${msg}`);
  if(logLines.length>20) logLines=logLines.slice(0,20);
  document.getElementById('log-panel').innerHTML=logLines.map((l,i)=>`<div style="color:${i===0?'#9aa3b8':'#6b7590'}">${l}</div>`).join('');
}
async function runScenario(s, resetTimer=true){
  currentScenario=s;
  try {
    const response=await fetch('/api/scan?scenario='+encodeURIComponent(s));
    const data=await response.json();
    if(!response.ok) throw new Error(data.error||'Scan failed');
    const m=data.metrics;
    const anomaly=data.label==='ANOMALY';
    const score=Number(data.score).toFixed(4);
    renderMetricCards(m,anomaly);
    renderXAI(m,anomaly,score,data.explanation);
    renderActions(m,anomaly,data.actions);
    renderBanner(anomaly,score);
    addLog(`Server ML scan: ${s.toUpperCase()} — ${data.label}; recovery recommendations are simulation-only`);
  } catch(error) {
    addLog('Scan error: '+error.message);
  }
  if(resetTimer) restartTimer();
}
function autoScan(){runScenario(currentScenario,false);}
function restartTimer(){if(scanTimer)clearInterval(scanTimer);const iv=parseInt(document.getElementById('interval-select').value)||5000;scanTimer=setInterval(autoScan,iv);}
document.getElementById('cpu-thresh').addEventListener('input',function(){document.getElementById('cpu-thresh-val').textContent=this.value+'%';});
document.getElementById('mem-thresh').addEventListener('input',function(){document.getElementById('mem-thresh-val').textContent=this.value+'%';});
document.getElementById('interval-select').addEventListener('change',restartTimer);
const ahCb=document.getElementById('auto-heal');
ahCb.addEventListener('change',function(){
  document.getElementById('toggle-bg').style.background=this.checked?'#f97316':'#2a3550';
  document.getElementById('toggle-knob').style.transform=this.checked?'translateX(18px)':'translateX(0)';
  document.getElementById('auto-heal-label').textContent=this.checked?'Enabled':'Disabled';
});
setInterval(()=>{const n=new Date();document.getElementById('clock').textContent=`${n.getHours().toString().padStart(2,'0')}:${n.getMinutes().toString().padStart(2,'0')}:${n.getSeconds().toString().padStart(2,'0')}`;},1000);
runScenario('normal');restartTimer();
</script>
</body>
</html>"""


@app.route("/")
def index():
    """Serve the orange-themed dashboard connected to the server-side ML and simulation pipeline."""
    return render_template_string(HTML)


@app.route("/api/scan")
def api_scan():
    """Run the selected synthetic scenario through the server-side ML pipeline."""
    scenario_map = {
        "normal": None,
        "cpu": "cpu_spike",
        "memory": "memory_leak",
        "disk": "disk_full",
        "network": "network_issue",
        "combined": "combined",
    }
    scenario = request.args.get("scenario", "normal")
    if scenario not in scenario_map:
        return jsonify({"error": "Unsupported scenario."}), 400

    metrics = simulate_normal() if scenario_map[scenario] is None else simulate_anomaly(scenario_map[scenario])
    label, score, _ = predict(model, metrics)
    xai_report = explain(metrics, label, score)
    actions = select_recovery_actions(metrics, label)

    # The dashboard displays latency as a supplemental synthetic demo metric;
    # it is not part of the five-feature Isolation Forest input.
    metrics["latency_ms"] = 25.0 if scenario in {"normal", "cpu"} else (220.0 if scenario == "network" else 45.0)
    return jsonify({
        "scenario": scenario,
        "metrics": metrics,
        "label": label,
        "score": score,
        "explanation": xai_report,
        "actions": actions,
        "recovery_mode": "simulation_only",
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
