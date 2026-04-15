# =============================================================
# dashboard.py — Flask Web Dashboard (Orange Theme v2.0)
# Run: python dashboard.py
# Open: http://localhost:5000
# =============================================================

from flask import Flask, render_template_string, jsonify
import random, io, sys
from monitor   import simulate_normal, simulate_anomaly
from detector  import train_model, predict
from explainer import explain
from healer    import decide_and_heal

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
function renderXAI(m,anomaly,score){
  const cpuT=parseInt(document.getElementById('cpu-thresh').value);
  const memT=parseInt(document.getElementById('mem-thresh').value);
  const devs=FEATURES.map(f=>({f,z:parseFloat(zScore(f,m[f])),abs:Math.abs(parseFloat(zScore(f,m[f])))})).sort((a,b)=>b.abs-a.abs);
  const rules=[];
  if(m.cpu_percent>cpuT) rules.push(`<span style="color:#f97316">CPU at ${m.cpu_percent.toFixed(1)}% exceeds ${cpuT}% threshold — possible runaway process</span>`);
  if(m.memory_percent>memT) rules.push(`<span style="color:#3b82f6">Memory at ${m.memory_percent.toFixed(1)}% exceeds ${memT}% — possible memory leak</span>`);
  if(m.disk_percent>85) rules.push(`<span style="color:#eab308">Disk at ${m.disk_percent.toFixed(1)}% critically low on storage</span>`);
  if(m.net_bytes_sent>40) rules.push(`<span style="color:#8b5cf6">Network sent ${m.net_bytes_sent.toFixed(1)} MB — abnormally high traffic</span>`);
  if(m.latency_ms>150) rules.push(`<span style="color:#ec4899">Latency ${m.latency_ms.toFixed(0)}ms — network degradation detected</span>`);
  if(!rules.length) rules.push(`<span style="color:#22c55e">All metrics within acceptable thresholds</span>`);
  let html=`<div style="margin-bottom:10px"><span style="color:#6b7590">Detection: </span><span style="font-weight:600;color:${anomaly?'#ef4444':'#22c55e'}">${anomaly?'ANOMALY':'NORMAL'}</span><span style="color:#6b7590;margin-left:12px">Score: </span><span style="color:#fb923c;font-weight:600">${score}</span></div>`;
  html+=`<div style="font-size:11px;color:#f97316;letter-spacing:0.06em;text-transform:uppercase;margin-bottom:6px">Feature importance</div>`;
  devs.slice(0,3).forEach((d,i)=>{
    const w=Math.min(d.abs*12,80),col=d.abs>3?'#ef4444':d.abs>1.5?'#f97316':'#6b7590';
    html+=`<div style="display:flex;align-items:center;gap:8px;margin-bottom:5px">
      <span style="font-size:11px;color:#6b7590;min-width:12px">#${i+1}</span>
      <span style="font-size:12px;color:#9aa3b8;min-width:100px">${LABELS[d.f]}</span>
      <div style="flex:1;height:4px;background:#2a3550;border-radius:2px"><div style="height:4px;border-radius:2px;background:${col};width:${w}%"></div></div>
      <span style="font-size:11px;color:${col};min-width:36px;text-align:right">z=${d.z>0?'+':''}${d.z}</span>
    </div>`;
  });
  html+=`<div style="font-size:11px;color:#f97316;letter-spacing:0.06em;text-transform:uppercase;margin:10px 0 6px">Rule-based reasoning</div>`;
  rules.forEach(r=>{html+=`<div style="margin-bottom:3px;padding-left:8px;border-left:2px solid #2a3550">${r}</div>`;});
  document.getElementById('xai-panel').innerHTML=html;
}
function renderActions(m,anomaly){
  const autoHeal=document.getElementById('auto-heal').checked;
  const appName=document.getElementById('app-name').value||'web-app-server';
  const cpuT=parseInt(document.getElementById('cpu-thresh').value);
  const memT=parseInt(document.getElementById('mem-thresh').value);
  if(!anomaly){
    document.getElementById('actions-panel').innerHTML=`<div style="display:flex;align-items:center;gap:8px;color:#22c55e"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#22c55e" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>No healing action required</div>`;
    return;
  }
  const acts=[];
  if(m.cpu_percent>cpuT){acts.push({icon:'↺',color:'#f97316',text:`Restart service: ${appName}`,status:'executed'});acts.push({icon:'⊕',color:'#fb923c',text:'Scale out +1 instance',status:'executed'});}
  if(m.memory_percent>memT){acts.push({icon:'✕',color:'#3b82f6',text:'Kill runaway process',status:'executed'});acts.push({icon:'↺',color:'#3b82f6',text:'Restart memory worker',status:'executed'});}
  if(m.disk_percent>85) acts.push({icon:'⊟',color:'#eab308',text:'Clear cache (512 MB freed)',status:'executed'});
  if(m.net_bytes_sent>40||m.latency_ms>150) acts.push({icon:'◉',color:'#8b5cf6',text:'Alert: ops team notified',status:'alerted'});
  if(!acts.length) acts.push({icon:'◉',color:'#f97316',text:'Alert: manual review needed',status:'alerted'});
  let html='';
  acts.forEach(a=>{
    const sc=a.status==='executed'?'#22c55e':'#f97316',sb=a.status==='executed'?'#162a1a':'#2a1800';
    html+=`<div class="action-row"><span style="color:${a.color};font-size:14px;min-width:16px;text-align:center">${a.icon}</span><span style="flex:1;color:#c8d0e0;font-size:12px">${a.text}</span><span style="font-size:10px;padding:2px 8px;border-radius:4px;background:${sb};color:${sc};font-weight:600">${autoHeal?a.status:'skipped'}</span></div>`;
  });
  document.getElementById('actions-panel').innerHTML=html;
  if(autoHeal){healCount++;addLog(`RECOVERY [#${healCount}] — Actions executed for ${acts.length} condition(s) on ${appName}`);}
  else addLog('AUTO-HEAL disabled — anomaly logged, no action taken');
}
function renderBanner(anomaly,score){
  const env=document.getElementById('env-select').value;
  const b=document.getElementById('status-banner'),bi=document.getElementById('banner-icon'),bt=document.getElementById('banner-text'),bs=document.getElementById('banner-sub');
  document.getElementById('banner-score-val').textContent=score;
  if(anomaly){
    b.style.background='#2a0a0a';b.style.borderColor='#ef4444';bi.style.background='#ef4444';bt.style.color='#ef4444';bt.textContent='Anomaly Detected';bs.textContent=`${env} environment — healing initiated`;
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
function runScenario(s){
  currentScenario=s;const m=getMetrics(s),anomaly=isAnomaly(m),score=anomalyScore(m);
  renderMetricCards(m,anomaly);renderXAI(m,anomaly,score);renderActions(m,anomaly);renderBanner(m,anomaly,score);
  addLog(`Scenario injected: ${s.toUpperCase()} — ${anomaly?'ANOMALY detected':'NORMAL state'}`);restartTimer();
}
function renderBanner(anomaly,score){
  const env=document.getElementById('env-select').value;
  const b=document.getElementById('status-banner'),bi=document.getElementById('banner-icon'),bt=document.getElementById('banner-text'),bs=document.getElementById('banner-sub');
  document.getElementById('banner-score-val').textContent=score;
  if(anomaly){b.style.background='#2a0a0a';b.style.borderColor='#ef4444';bi.style.background='#ef4444';bt.style.color='#ef4444';bt.textContent='Anomaly Detected';bs.textContent=`${env} environment — healing initiated`;document.getElementById('status-label').textContent='Alert Active';document.getElementById('pulse-dot').style.background='#ef4444';}
  else{b.style.background='#0f1e13';b.style.borderColor='#22c55e';bi.style.background='#22c55e';bt.style.color='#22c55e';bt.textContent='System Normal';bs.textContent='All metrics within safe range';document.getElementById('status-label').textContent='System Online';document.getElementById('pulse-dot').style.background='#22c55e';}
}
function autoScan(){const m=getMetrics(currentScenario),anomaly=isAnomaly(m),score=anomalyScore(m);renderMetricCards(m,anomaly);renderXAI(m,anomaly,score);renderActions(m,anomaly);renderBanner(anomaly,score);}
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
    """Serve the orange-themed dashboard. All simulation logic runs client-side."""
    return render_template_string(HTML)


@app.route("/api/scan")
def api_scan():
    """
    Optional JSON API: server-side ML prediction via Isolation Forest.
    The JS dashboard is fully standalone, but this endpoint can be
    consumed for ML-backed results if desired.
    """
    anomaly_type = random.choice(["cpu_spike", "memory_leak", "disk_full", "combined", None])
    metrics = simulate_anomaly(anomaly_type) if anomaly_type else simulate_normal()

    label, score, _ = predict(model, metrics)
    xai_report = explain(metrics, label, score)

    old_stdout = sys.stdout
    sys.stdout = buffer = io.StringIO()
    decide_and_heal(metrics, label, xai_report)
    sys.stdout = old_stdout

    return jsonify({
        "metrics": metrics,
        "label": label,
        "score": score,
        "explanation": xai_report,
        "actions": buffer.getvalue(),
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)
