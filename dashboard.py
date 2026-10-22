# =============================================================
# dashboard.py  — XAI Cloud Operations Platform
# Premium UI Redesign (Phase 4A Final)
# ONLY presentation layer changed. No research logic modified.
# =============================================================

from flask import Flask, render_template_string
import config
from api import api_bp, init_api_model

app = Flask(__name__)
app.register_blueprint(api_bp)

HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>XAI Cloud — Autonomous Operations | Temporal XAI Cloud Monitor</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
/* ─────────────────────────────────────────────────────────────
   DESIGN TOKENS
───────────────────────────────────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html { font-size: 13px; scroll-behavior: smooth; }

:root {
  --base:     #090b0f;
  --s0:       #0e1118;
  --s1:       #131820;
  --s2:       #181e2b;
  --br:       #1d2334;
  --br2:      #272f42;
  --tx1:      #dce1ee;
  --tx2:      #7e8aa0;
  --tx3:      #424d65;
  --green:    #22c55e;
  --amber:    #f59e0b;
  --red:      #ef4444;
  --blue:     #4b8eff;
  --violet:   #9b8cff;
  --nav-h:    52px;
  --sb-w:     224px;
  --sb-cw:    52px;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
  background: var(--base);
  color: var(--tx1);
  min-height: 100vh;
  line-height: 1.5;
  -webkit-font-smoothing: antialiased;
  overflow-x: hidden;
}
.mono { font-family: 'Cascadia Code', 'Fira Code', 'Consolas', monospace; }

::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--base); }
::-webkit-scrollbar-thumb { background: var(--br2); border-radius: 3px; }

/* ─────────────────────────────────────────────────────────────
   TOP NAV
───────────────────────────────────────────────────────────── */
#topnav {
  position: fixed; top: 0; left: 0; right: 0; z-index: 200;
  height: var(--nav-h);
  background: rgba(9,11,15,.96);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid var(--br);
  display: flex; align-items: center;
  padding: 0 20px 0 14px; gap: 14px;
}
.nav-brand { display: flex; align-items: center; gap: 10px; flex-shrink: 0; }
.brand-mark {
  width: 32px; height: 32px;
  background: linear-gradient(135deg, #4b8eff, #9b8cff);
  border-radius: 8px;
  display: flex; align-items: center; justify-content: center;
}
.brand-mark svg { width: 17px; height: 17px; }
.brand-name { font-size: 13px; font-weight: 700; color: var(--tx1); letter-spacing: -.01em; line-height: 1.2; }
.brand-sub  { font-size: 9.5px; color: var(--tx3); letter-spacing: .04em; }
.nav-sep { width: 1px; height: 24px; background: var(--br); flex-shrink: 0; }
.nav-title { font-size: 11px; color: var(--tx2); flex: 1; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.nav-right { display: flex; align-items: center; gap: 14px; flex-shrink: 0; }
.nav-sys { display: flex; align-items: center; gap: 6px; font-size: 11px; color: var(--tx2); }
.sys-dot { width: 6px; height: 6px; border-radius: 50%; background: var(--green); animation: pls 2s ease-in-out infinite; }
@keyframes pls { 0%,100%{opacity:1} 50%{opacity:.3} }
.nav-model { font-size: 10px; color: var(--tx3); }
#nav-risk-badge {
  font-size: 10px; font-weight: 700; letter-spacing: .07em;
  padding: 3px 10px; border-radius: 5px; border: 1px solid;
  transition: all .4s;
}

/* ─────────────────────────────────────────────────────────────
   SHELL
───────────────────────────────────────────────────────────── */
#shell {
  display: flex;
  height: calc(100vh - var(--nav-h));
  margin-top: var(--nav-h);
}

/* ─────────────────────────────────────────────────────────────
   SIDEBAR
───────────────────────────────────────────────────────────── */
#sidebar {
  width: var(--sb-w);
  border-right: 1px solid var(--br);
  background: var(--s0);
  display: flex; flex-direction: column;
  overflow: hidden; overflow-y: auto;
  flex-shrink: 0;
  transition: width .22s cubic-bezier(.4,0,.2,1);
}
#sidebar.collapsed { width: var(--sb-cw); }
#sidebar::-webkit-scrollbar { width: 0; }

.sb-toggle-row {
  height: 38px; display: flex; align-items: center; justify-content: flex-end;
  padding-right: 12px; border-bottom: 1px solid var(--br); flex-shrink: 0;
}
#sidebar.collapsed .sb-toggle-row { justify-content: center; padding-right: 0; }
.sb-toggle { background: none; border: none; color: var(--tx3); cursor: pointer; padding: 6px; border-radius: 5px; transition: color .2s, background .2s; }
.sb-toggle:hover { color: var(--tx2); background: var(--s1); }

.sb-grp-label {
  font-size: 9px; font-weight: 700; letter-spacing: .12em; text-transform: uppercase;
  color: var(--tx3); padding: 14px 14px 5px;
  white-space: nowrap; overflow: hidden;
  transition: opacity .2s;
}
#sidebar.collapsed .sb-grp-label { opacity: 0; }

.sb-nav { padding: 2px 6px; display: flex; flex-direction: column; gap: 1px; }
.sb-item {
  display: flex; align-items: center; gap: 10px;
  padding: 8px 8px; border-radius: 7px;
  color: var(--tx2); font-size: 11.5px; font-weight: 500;
  cursor: pointer; text-decoration: none;
  transition: color .15s, background .15s;
  white-space: nowrap; border: 1px solid transparent;
}
.sb-item:hover { color: var(--tx1); background: var(--s2); }
.sb-item.active { color: var(--blue); background: rgba(75,142,255,.08); border-color: rgba(75,142,255,.15); }
.sb-item svg { width: 15px; height: 15px; flex-shrink: 0; }
.sb-item-label { overflow: hidden; transition: opacity .2s; }
#sidebar.collapsed .sb-item-label { opacity: 0; width: 0; }

.sb-spacer { flex: 1; min-height: 16px; }

.sb-footer { border-top: 1px solid var(--br); padding: 10px 10px; }
.sb-stat { display: flex; align-items: center; gap: 7px; padding: 4px 2px; }
.sb-stat-dot { width: 5px; height: 5px; border-radius: 50%; flex-shrink: 0; }
.sb-stat-text { font-size: 10.5px; color: var(--tx3); white-space: nowrap; transition: opacity .2s; }
#sidebar.collapsed .sb-stat-text { opacity: 0; }

/* ─────────────────────────────────────────────────────────────
   MAIN CONTENT
───────────────────────────────────────────────────────────── */
#content { flex: 1; overflow-y: auto; background: var(--base); }

.section { padding: 28px 32px; border-bottom: 1px solid var(--br); }
.section:last-child { border-bottom: none; }

.sec-head { margin-bottom: 22px; }
.sec-title {
  display: flex; align-items: center; gap: 8px;
  font-size: 13.5px; font-weight: 700; color: var(--tx1);
}
.sec-dot { width: 4px; height: 4px; border-radius: 50%; flex-shrink: 0; }
.sec-sub { font-size: 11px; color: var(--tx3); margin-top: 3px; line-height: 1.5; }

/* Shared utilities */
.label { font-size: 9.5px; font-weight: 700; letter-spacing: .1em; text-transform: uppercase; color: var(--tx3); }
.surface { background: var(--s1); border: 1px solid var(--br); border-radius: 10px; padding: 18px 20px; }
.surface-2 { background: var(--s2); border: 1px solid var(--br); border-radius: 8px; padding: 12px 14px; }
.chip {
  display: inline-flex; align-items: center;
  font-size: 9px; font-weight: 700; letter-spacing: .07em; text-transform: uppercase;
  border: 1px solid; border-radius: 4px; padding: 2px 7px;
}
.hdiv { height: 1px; background: var(--br); margin: 14px 0; }

/* ─────────────────────────────────────────────────────────────
   PIPELINE BAR
───────────────────────────────────────────────────────────── */
#pipe-bar {
  display: flex; align-items: flex-start; gap: 0;
  overflow-x: auto; padding-bottom: 4px; margin-bottom: 28px;
}
#pipe-bar::-webkit-scrollbar { height: 0; }
.ps { display: flex; flex-direction: column; align-items: center; gap: 5px; min-width: 76px; }
.ps-icon {
  width: 30px; height: 30px; border-radius: 50%;
  border: 1.5px solid var(--br);
  display: flex; align-items: center; justify-content: center;
  font-size: 11px; font-weight: 700; color: var(--tx3);
  transition: all .35s;
}
.ps-name { font-size: 8.5px; color: var(--tx3); font-weight: 600; letter-spacing: .04em; text-transform: uppercase; text-align: center; white-space: nowrap; transition: color .35s; }
.ps.done .ps-icon  { border-color: var(--green); background: rgba(34,197,94,.1); color: var(--green); }
.ps.done .ps-name  { color: var(--green); }
.ps.active .ps-icon { border-color: var(--blue); background: rgba(75,142,255,.12); color: var(--blue); animation: psAnim 1.6s ease-in-out infinite; }
.ps.active .ps-name { color: var(--blue); }
@keyframes psAnim { 0%,100%{box-shadow:none} 50%{box-shadow:0 0 0 5px rgba(75,142,255,.12)} }
.ps-arrow { color: var(--br2); font-size: 14px; padding: 0 4px; margin-top: 8px; flex-shrink: 0; }

/* ─────────────────────────────────────────────────────────────
   RISK DISPLAY
───────────────────────────────────────────────────────────── */
.risk-layout { display: grid; grid-template-columns: 200px 1fr 160px; align-items: center; gap: 36px; }
.risk-level-lbl { font-size: 36px; font-weight: 900; letter-spacing: -.02em; transition: color .4s; }
.risk-desc-text { font-size: 11.5px; color: var(--tx2); margin-top: 5px; line-height: 1.55; }

.risk-track-wrap { display: flex; flex-direction: column; gap: 7px; }
.risk-track-labels { display: flex; justify-content: space-between; }
.risk-tl { font-size: 9px; color: var(--tx3); }
.risk-track {
  height: 6px; background: var(--s2); border: 1px solid var(--br); border-radius: 3px;
  position: relative; overflow: hidden;
}
.risk-fill { height: 100%; border-radius: 3px; transition: width .65s ease, background .4s; }
.risk-ticks { display: flex; justify-content: space-between; }
.risk-tick { font-size: 8px; color: var(--tx3); }
.risk-pointer {
  position: absolute; top: -5px; width: 2px; height: 16px;
  background: var(--tx1); border-radius: 1px; transform: translateX(-50%);
  transition: left .65s ease;
}
.risk-pointer::after {
  content: ''; position: absolute; bottom: -4px; left: 50%; transform: translateX(-50%);
  width: 7px; height: 7px; border-radius: 50%; background: inherit;
}

.score-block { text-align: right; }
.score-num { font-size: 38px; font-weight: 900; line-height: 1; transition: color .4s; }
.score-sub { font-size: 9px; color: var(--tx3); margin-top: 5px; letter-spacing: .08em; text-transform: uppercase; }

/* ─────────────────────────────────────────────────────────────
   LIVE TELEMETRY GRID
───────────────────────────────────────────────────────────── */
#metric-row {
  display: grid; grid-template-columns: repeat(5,1fr);
  gap: 1px; background: var(--br);
  border: 1px solid var(--br); border-radius: 10px; overflow: hidden;
}
.mc {
  background: var(--s1); padding: 16px 16px 12px;
  transition: background .2s;
}
.mc:hover { background: var(--s2); }
.mc-name { font-size: 9px; font-weight: 700; color: var(--tx3); letter-spacing: .07em; text-transform: uppercase; margin-bottom: 8px; }
.mc-val  { font-size: 22px; font-weight: 800; color: var(--tx1); line-height: 1; }
.mc-unit { font-size: 10px; color: var(--tx3); font-weight: 400; margin-left: 1px; }
.mc-spark { height: 32px; margin-top: 10px; }
.mc-delta { display: flex; align-items: center; gap: 4px; font-size: 9.5px; margin-top: 6px; }

/* ─────────────────────────────────────────────────────────────
   TEMPORAL CHART
───────────────────────────────────────────────────────────── */
#temporal-area {
  background: var(--s1); border: 1px solid var(--br); border-radius: 10px;
  padding: 20px; overflow: hidden;
}
.chart-legend { display: flex; gap: 16px; flex-wrap: wrap; margin-bottom: 14px; }
.leg-item { display: flex; align-items: center; gap: 5px; font-size: 10px; color: var(--tx2); }
.leg-dot { width: 18px; height: 2px; border-radius: 1px; }
#main-chart { display: block; width: 100%; }
#temporal-stats {
  display: grid; grid-template-columns: repeat(5,1fr);
  gap: 1px; background: var(--br);
  border: 1px solid var(--br); border-radius: 8px; overflow: hidden; margin-top: 14px;
}
.ts-cell { background: var(--s1); padding: 10px 12px; }
.ts-name { font-size: 9px; color: var(--tx3); letter-spacing: .06em; text-transform: uppercase; margin-bottom: 4px; }
.ts-val  { font-size: 14px; font-weight: 700; color: var(--tx1); }
.ts-delta { font-size: 9.5px; margin-top: 2px; }

/* ─────────────────────────────────────────────────────────────
   PREDICTION + MODEL INFO
───────────────────────────────────────────────────────────── */
.pred-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }

/* ─────────────────────────────────────────────────────────────
   XAI BARS
───────────────────────────────────────────────────────────── */
.xai-intro {
  font-size: 12px; color: var(--tx2); line-height: 1.65;
  border-left: 2px solid var(--blue);
  background: rgba(75,142,255,.05); padding: 11px 14px;
  border-radius: 0 7px 7px 0; margin-bottom: 18px;
}
.xai-row {
  display: flex; align-items: center; gap: 10px;
  padding: 9px 0; border-bottom: 1px solid rgba(29,35,52,.7);
}
.xai-row:last-of-type { border-bottom: none; }
.xai-rank { font-size: 10px; color: var(--tx3); width: 18px; flex-shrink: 0; }
.xai-name { font-size: 11.5px; color: var(--tx1); width: 190px; flex-shrink: 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.xai-bar  { flex: 1; }
.xai-track { height: 5px; background: var(--s2); border-radius: 3px; overflow: hidden; }
.xai-fill  { height: 100%; border-radius: 3px; transition: width .55s ease; }
.xai-val  { font-size: 11px; font-weight: 600; width: 60px; text-align: right; flex-shrink: 0; }
.xai-dir  { font-size: 8px; font-weight: 700; letter-spacing: .05em; text-transform: uppercase; padding: 2px 5px; border-radius: 3px; flex-shrink: 0; }
.xai-footer { font-size: 10px; color: var(--tx3); line-height: 1.6; border-top: 1px solid var(--br); padding-top: 12px; margin-top: 14px; }

/* ─────────────────────────────────────────────────────────────
   ROOT CAUSE
───────────────────────────────────────────────────────────── */
.rc-layout { display: grid; grid-template-columns: 200px 1fr; gap: 28px; align-items: start; }
.rc-cat-name { font-size: 22px; font-weight: 900; letter-spacing: -.01em; line-height: 1; transition: color .4s; }
.rc-cat-note { font-size: 10px; color: var(--tx3); margin-top: 8px; line-height: 1.5; font-style: italic; max-width: 180px; }
.ev-item { margin-bottom: 10px; }
.ev-header { display: flex; justify-content: space-between; font-size: 11px; margin-bottom: 4px; }
.ev-label { color: var(--tx2); }
.ev-strength { font-weight: 600; font-size: 10px; }
.ev-track { height: 4px; background: var(--s2); border-radius: 2px; overflow: hidden; }
.ev-fill  { height: 100%; border-radius: 2px; transition: width .55s ease; }
.rc-explain { margin-top: 14px; font-size: 11.5px; color: var(--tx2); line-height: 1.65; padding: 11px 14px; border-left: 2px solid rgba(245,158,11,.4); background: rgba(245,158,11,.04); border-radius: 0 6px 6px 0; }

/* ─────────────────────────────────────────────────────────────
   DECISION + HEALING
───────────────────────────────────────────────────────────── */
.dec-grid { display: grid; grid-template-columns: 1fr 1px 1fr; gap: 28px; }
.dec-vdiv { background: var(--br); }
.dec-field-label { font-size: 9px; font-weight: 700; color: var(--tx3); letter-spacing: .1em; text-transform: uppercase; margin-bottom: 7px; }
.dec-field-val   { font-size: 13.5px; font-weight: 600; color: var(--tx1); line-height: 1.4; }
.dec-reason      { font-size: 11px; color: var(--tx3); margin-top: 6px; }

/* ─────────────────────────────────────────────────────────────
   VERIFICATION
───────────────────────────────────────────────────────────── */
.ver-layout { display: grid; grid-template-columns: 1fr auto 1fr; gap: 14px; align-items: center; }
.ver-side { background: var(--s1); border: 1px solid var(--br); border-radius: 10px; padding: 20px 22px; }
.ver-side-lbl { font-size: 9px; font-weight: 700; letter-spacing: .1em; text-transform: uppercase; color: var(--tx3); margin-bottom: 10px; }
.ver-risk-txt  { font-size: 28px; font-weight: 900; line-height: 1; transition: color .4s; }
.ver-score-txt { font-size: 13px; color: var(--tx2); margin-top: 5px; }
.ver-mid { display: flex; flex-direction: column; align-items: center; gap: 10px; padding: 0 8px; }
.ver-arrow { font-size: 18px; color: var(--tx3); }
.ver-status {
  text-align: center; padding: 11px 18px; border-radius: 8px; border: 2px solid; min-width: 130px;
}
.ver-status-txt { font-size: 13px; font-weight: 800; letter-spacing: .03em; }
.ver-delta { font-size: 10px; font-weight: 600; }
.ver-note { font-size: 9.5px; color: var(--tx3); text-align: center; line-height: 1.5; max-width: 120px; }
.ver-footnote { margin-top: 14px; font-size: 10px; color: var(--tx3); line-height: 1.65; font-style: italic; }

/* ─────────────────────────────────────────────────────────────
   EVENT TIMELINE
───────────────────────────────────────────────────────────── */
#tl-list { max-height: 300px; overflow-y: auto; }
#tl-list::-webkit-scrollbar { width: 4px; }
.tl-item { display: flex; gap: 12px; padding: 9px 0; border-bottom: 1px solid rgba(29,35,52,.5); animation: tlIn .3s ease; }
@keyframes tlIn { from{opacity:0;transform:translateY(-3px)} to{opacity:1;transform:none} }
.tl-item:last-child { border-bottom: none; }
.tl-ts { font-size: 10px; color: var(--tx3); width: 52px; flex-shrink: 0; padding-top: 1px; }
.tl-track { display: flex; flex-direction: column; align-items: center; flex-shrink: 0; }
.tl-dot  { width: 7px; height: 7px; border-radius: 50%; margin-top: 4px; flex-shrink: 0; }
.tl-line { width: 1px; background: var(--br); flex: 1; margin-top: 4px; }
.tl-body { flex: 1; }
.tl-cat  { font-size: 9.5px; font-weight: 700; letter-spacing: .07em; text-transform: uppercase; margin-bottom: 2px; }
.tl-msg  { font-size: 11.5px; color: var(--tx2); line-height: 1.4; }

/* ─────────────────────────────────────────────────────────────
   SIMULATION LAB
───────────────────────────────────────────────────────────── */
.sim-grid { display: grid; grid-template-columns: repeat(3,1fr); gap: 10px; margin-bottom: 16px; }
.sim-card {
  background: var(--s1); border: 1px solid var(--br); border-radius: 10px; padding: 16px;
  cursor: pointer; transition: border-color .2s, background .2s;
}
.sim-card:hover { border-color: var(--br2); background: var(--s2); }
.sim-card.sel   { border-color: var(--blue); background: rgba(75,142,255,.06); }
.sc-icon  { font-size: 18px; margin-bottom: 8px; color: var(--tx2); }
.sc-name  { font-size: 12px; font-weight: 700; color: var(--tx1); margin-bottom: 3px; }
.sc-desc  { font-size: 10px; color: var(--tx3); line-height: 1.4; }
.sim-card.sel .sc-name { color: var(--blue); }

#run-sim {
  width: 100%; padding: 12px; border: none; border-radius: 8px;
  background: linear-gradient(135deg, #4b8eff, #9b8cff);
  color: #fff; font-size: 12px; font-weight: 700; letter-spacing: .05em; text-transform: uppercase;
  cursor: pointer; transition: opacity .2s, transform .15s;
  display: flex; align-items: center; justify-content: center; gap: 8px;
  box-shadow: 0 2px 12px rgba(75,142,255,.22);
}
#run-sim:hover { opacity: .92; transform: translateY(-1px); }
#run-sim:active { transform: none; }

.sim-active-box { margin-top: 10px; padding: 11px 14px; background: var(--s1); border: 1px solid var(--br); border-radius: 8px; font-size: 11.5px; color: var(--tx2); display: flex; align-items: center; gap: 8px; }
.sim-active-dot { width: 6px; height: 6px; border-radius: 50%; background: var(--green); animation: pls 2s ease-in-out infinite; flex-shrink: 0; }

/* ─────────────────────────────────────────────────────────────
   EMPTY / LOADING STATES
───────────────────────────────────────────────────────────── */
.empty-state {
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  gap: 7px; padding: 36px 20px; color: var(--tx3);
}
.empty-state-icon  { font-size: 22px; opacity: .4; }
.empty-state-title { font-size: 12px; font-weight: 600; color: var(--tx2); }
.empty-state-sub   { font-size: 11px; text-align: center; line-height: 1.5; max-width: 320px; }

.shimmer {
  background: linear-gradient(90deg, var(--s1) 25%, var(--s2) 50%, var(--s1) 75%);
  background-size: 200% 100%; border-radius: 5px;
  animation: shim 1.8s linear infinite;
}
@keyframes shim { 0%{background-position:200% 0} 100%{background-position:-200% 0} }

/* ─────────────────────────────────────────────────────────────
   RESPONSIVE
───────────────────────────────────────────────────────────── */
@media (max-width: 1140px) {
  #metric-row { grid-template-columns: repeat(3,1fr); }
  .risk-layout { grid-template-columns: 160px 1fr 140px; gap: 24px; }
  .sim-grid { grid-template-columns: repeat(2,1fr); }
  .xai-name { width: 160px; }
}
@media (max-width: 800px) {
  #sidebar { display: none; }
  .section { padding: 22px 18px; }
  #metric-row { grid-template-columns: repeat(2,1fr); }
  .risk-layout { grid-template-columns: 1fr; gap: 16px; }
  .rc-layout { grid-template-columns: 1fr; }
  .dec-grid { grid-template-columns: 1fr; }
  .dec-vdiv { display: none; }
  .ver-layout { grid-template-columns: 1fr; }
  .ver-mid { flex-direction: row; }
  .pred-grid { grid-template-columns: 1fr; }
  .nav-title { display: none; }
  #temporal-stats { grid-template-columns: repeat(3,1fr); }
}
</style>
</head>
<body>

<!-- ═══════════════════════════════════════════
     TOP NAV
════════════════════════════════════════════ -->
<nav id="topnav">
  <div class="nav-brand">
    <div class="brand-mark">
      <svg viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/>
        <polyline points="3.27 6.96 12 12.01 20.73 6.96"/><line x1="12" y1="22.08" x2="12" y2="12"/>
      </svg>
    </div>
    <div>
      <div class="brand-name">XAI Cloud</div>
      <div class="brand-sub">Autonomous Operations</div>
    </div>
  </div>
  <div class="nav-sep"></div>
  <div class="nav-title">Explainable AI-Driven Autonomous Self-Healing Cloud Management Platform</div>
  <div class="nav-right">
    <div class="nav-sys"><span class="sys-dot"></span>Operational</div>
    <div class="nav-model" id="nav-model-lbl">LR &middot; Seed&nbsp;42 &middot; 45 Features</div>
    <div class="nav-sep"></div>
    <div id="nav-risk-badge">—</div>
  </div>
</nav>

<!-- ═══════════════════════════════════════════
     SHELL
════════════════════════════════════════════ -->
<div id="shell">

  <!-- SIDEBAR -->
  <aside id="sidebar">
    <div class="sb-toggle-row">
      <button class="sb-toggle" onclick="toggleSb()" title="Toggle sidebar">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
          <line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/>
        </svg>
      </button>
    </div>

    <div class="sb-grp-label">Monitor</div>
    <div class="sb-nav">
      <a class="sb-item active" href="#sec-overview" onclick="sbClick(this)">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>
        <span class="sb-item-label">Overview</span>
      </a>
      <a class="sb-item" href="#sec-telemetry" onclick="sbClick(this)">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>
        <span class="sb-item-label">Live Monitoring</span>
      </a>
      <a class="sb-item" href="#sec-temporal" onclick="sbClick(this)">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
        <span class="sb-item-label">Temporal Intelligence</span>
      </a>
    </div>

    <div class="sb-grp-label">AI Layer</div>
    <div class="sb-nav">
      <a class="sb-item" href="#sec-prediction" onclick="sbClick(this)">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/></svg>
        <span class="sb-item-label">Failure Intelligence</span>
      </a>
      <a class="sb-item" href="#sec-xai" onclick="sbClick(this)">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M12 1v3M12 20v3M4.22 4.22l2.12 2.12M17.66 17.66l2.12 2.12M1 12h3M20 12h3M4.22 19.78l2.12-2.12M17.66 6.34l2.12-2.12"/></svg>
        <span class="sb-item-label">XAI Reasoning</span>
      </a>
      <a class="sb-item" href="#sec-rootcause" onclick="sbClick(this)">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
        <span class="sb-item-label">Incident Intelligence</span>
      </a>
    </div>

    <div class="sb-grp-label">Operations</div>
    <div class="sb-nav">
      <a class="sb-item" href="#sec-decision" onclick="sbClick(this)">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 11 12 14 22 4"/><path d="M21 12v7a2 2 0 01-2 2H5a2 2 0 01-2-2V5a2 2 0 012-2h11"/></svg>
        <span class="sb-item-label">Decision &amp; Recovery</span>
      </a>
      <a class="sb-item" href="#sec-verification" onclick="sbClick(this)">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 11-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
        <span class="sb-item-label">Verification</span>
      </a>
      <a class="sb-item" href="#sec-timeline" onclick="sbClick(this)">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/><line x1="8" y1="18" x2="21" y2="18"/><circle cx="4" cy="6" r="1" fill="currentColor"/><circle cx="4" cy="12" r="1" fill="currentColor"/><circle cx="4" cy="18" r="1" fill="currentColor"/></svg>
        <span class="sb-item-label">Event Timeline</span>
      </a>
      <a class="sb-item" href="#sec-simulation" onclick="sbClick(this)">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><polygon points="5 3 19 12 5 21 5 3"/></svg>
        <span class="sb-item-label">Simulation Lab</span>
      </a>
    </div>

    <div class="sb-spacer"></div>

    <div class="sb-footer">
      <div class="sb-stat"><div class="sb-stat-dot" style="background:var(--green)"></div><span class="sb-stat-text">Model loaded</span></div>
      <div class="sb-stat"><div class="sb-stat-dot" style="background:var(--green)"></div><span class="sb-stat-text">API online</span></div>
      <div class="sb-stat"><div class="sb-stat-dot" id="tel-dot" style="background:var(--green)"></div><span class="sb-stat-text" id="tel-txt">Streaming</span></div>
    </div>
  </aside>

  <!-- MAIN -->
  <main id="content">

    <!-- ═══ OVERVIEW ═══ -->
    <div class="section" id="sec-overview">
      <div class="sec-head">
        <div class="sec-title"><span class="sec-dot" style="background:var(--blue)"></span>System Overview</div>
        <div class="sec-sub">AI pipeline state and current failure risk index</div>
      </div>

      <!-- Pipeline bar -->
      <div id="pipe-bar">
        <div class="ps" id="ps0"><div class="ps-icon">M</div><div class="ps-name">Monitor</div></div>
        <div class="ps-arrow">›</div>
        <div class="ps" id="ps1"><div class="ps-icon">T</div><div class="ps-name">Temporal</div></div>
        <div class="ps-arrow">›</div>
        <div class="ps" id="ps2"><div class="ps-icon">P</div><div class="ps-name">Predict</div></div>
        <div class="ps-arrow">›</div>
        <div class="ps" id="ps3"><div class="ps-icon">X</div><div class="ps-name">XAI</div></div>
        <div class="ps-arrow">›</div>
        <div class="ps" id="ps4"><div class="ps-icon">R</div><div class="ps-name">Root&nbsp;Cause</div></div>
        <div class="ps-arrow">›</div>
        <div class="ps" id="ps5"><div class="ps-icon">D</div><div class="ps-name">Decide</div></div>
        <div class="ps-arrow">›</div>
        <div class="ps" id="ps6"><div class="ps-icon">H</div><div class="ps-name">Heal</div></div>
        <div class="ps-arrow">›</div>
        <div class="ps" id="ps7"><div class="ps-icon">V</div><div class="ps-name">Verify</div></div>
      </div>

      <!-- Risk block -->
      <div class="surface" style="padding:24px 28px;">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:20px;">
          <div>
            <div class="label" style="margin-bottom:4px;">Failure Risk Index — 10-Step Prediction Horizon</div>
            <div id="risk-desc" style="font-size:11.5px;color:var(--tx2);margin-top:3px;max-width:500px;line-height:1.5;">Warming up — collecting temporal buffer…</div>
          </div>
          <div id="status-chip" style="display:inline-flex;align-items:center;gap:6px;font-size:10px;font-weight:700;padding:5px 13px;border-radius:6px;border:1px solid;letter-spacing:.06em;transition:all .4s;">
            <span id="status-chip-dot" style="width:5px;height:5px;border-radius:50%;display:inline-block;"></span>
            <span id="status-chip-txt">—</span>
          </div>
        </div>
        <div class="risk-layout">
          <div>
            <div class="label" style="margin-bottom:7px;">Risk Level</div>
            <div class="risk-level-lbl" id="risk-level-lbl" style="color:var(--green)">—</div>
            <div style="font-size:10px;color:var(--tx3);margin-top:6px;" id="risk-scenario-lbl"></div>
          </div>
          <div class="risk-track-wrap">
            <div class="risk-track-labels">
              <span class="risk-tl">LOW</span><span class="risk-tl">MEDIUM</span>
              <span class="risk-tl">HIGH</span><span class="risk-tl">CRITICAL</span>
            </div>
            <div class="risk-track" id="risk-track">
              <div class="risk-fill" id="risk-fill" style="width:0%;background:var(--green)"></div>
              <div class="risk-pointer" id="risk-ptr" style="left:0%"></div>
            </div>
            <div class="risk-ticks">
              <span class="risk-tick">0.00</span><span class="risk-tick">0.25</span>
              <span class="risk-tick">0.50</span><span class="risk-tick">0.75</span>
              <span class="risk-tick">1.00</span>
            </div>
          </div>
          <div class="score-block">
            <div class="label" style="margin-bottom:7px;">Decision Score</div>
            <div class="score-num mono" id="score-num" style="color:var(--green)">0.0000</div>
            <div class="score-sub">Logistic Regression</div>
          </div>
        </div>
      </div>
    </div>

    <!-- ═══ TELEMETRY ═══ -->
    <div class="section" id="sec-telemetry">
      <div class="sec-head">
        <div class="sec-title"><span class="sec-dot" style="background:var(--green)"></span>Live Infrastructure Telemetry</div>
        <div class="sec-sub">Real-time metrics from the active simulation scenario — all values sourced from the backend</div>
      </div>
      <div id="metric-row"></div>
    </div>

    <!-- ═══ TEMPORAL INTELLIGENCE ═══ -->
    <div class="section" id="sec-temporal">
      <div class="sec-head">
        <div class="sec-title"><span class="sec-dot" style="background:var(--violet)"></span>Temporal Intelligence</div>
        <div class="sec-sub">10-step sliding window — the predictive model analyzes behavioral trajectories, not individual snapshots. Each timestep's prediction draws on the past 10 readings across all metrics.</div>
      </div>
      <div id="temporal-area">
        <div class="chart-legend">
          <div class="leg-item"><div class="leg-dot" style="background:#f97316"></div>CPU</div>
          <div class="leg-item"><div class="leg-dot" style="background:#3b82f6"></div>Memory</div>
          <div class="leg-item"><div class="leg-dot" style="background:#f59e0b"></div>Disk</div>
          <div class="leg-item"><div class="leg-dot" style="background:#22c55e"></div>Net Sent</div>
          <div class="leg-item"><div class="leg-dot" style="background:#a78bfa"></div>Net Recv</div>
        </div>
        <svg id="main-chart" viewBox="0 0 800 148" preserveAspectRatio="none" style="width:100%;height:148px;display:block;overflow:visible"></svg>
        <div id="temporal-stats"></div>
      </div>
    </div>

    <!-- ═══ AI FAILURE INTELLIGENCE ═══ -->
    <div class="section" id="sec-prediction">
      <div class="sec-head">
        <div class="sec-title"><span class="sec-dot" style="background:var(--violet)"></span>AI Failure Intelligence</div>
        <div class="sec-sub">Logistic Regression model trained on Phase 3C temporal features — re-evaluated at each timestep</div>
      </div>
      <div class="pred-grid">
        <div class="surface">
          <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:18px;">
            <div>
              <div class="label" style="margin-bottom:6px;">Predicted Risk</div>
              <div style="font-size:34px;font-weight:900;letter-spacing:-.02em;transition:color .4s;" id="pred-risk-lbl" class="mono">—</div>
            </div>
            <div style="text-align:right;">
              <div class="label" style="margin-bottom:6px;">Decision Score</div>
              <div style="font-size:22px;font-weight:800;transition:color .4s;" id="pred-score-lbl" class="mono">0.0000</div>
            </div>
          </div>
          <div class="hdiv"></div>
          <div style="font-size:11px;color:var(--tx2);line-height:1.6;">
            Prediction horizon: failure active <em>now</em> or within the next 10 timesteps
          </div>
          <div id="pred-status-msg" style="margin-top:10px;font-size:11px;color:var(--tx3);padding:9px 12px;background:var(--s2);border-radius:6px;">
            Awaiting temporal buffer…
          </div>
        </div>
        <div class="surface">
          <div class="label" style="margin-bottom:12px;">Model Configuration</div>
          <div style="display:flex;flex-direction:column;gap:7px;">
            <div style="display:flex;justify-content:space-between;">
              <span style="font-size:11.5px;color:var(--tx3)">Algorithm</span>
              <span style="font-size:11.5px;color:var(--tx1)">Logistic Regression</span>
            </div>
            <div style="display:flex;justify-content:space-between;">
              <span style="font-size:11.5px;color:var(--tx3)">Regularization C</span>
              <span style="font-size:11.5px;" class="mono">1.0</span>
            </div>
            <div style="display:flex;justify-content:space-between;">
              <span style="font-size:11.5px;color:var(--tx3)">Random seed</span>
              <span style="font-size:11.5px;" class="mono">42</span>
            </div>
            <div style="display:flex;justify-content:space-between;">
              <span style="font-size:11.5px;color:var(--tx3)">Scaling</span>
              <span style="font-size:11.5px;color:var(--tx1)">StandardScaler</span>
            </div>
            <div style="display:flex;justify-content:space-between;">
              <span style="font-size:11.5px;color:var(--tx3)">Feature count</span>
              <span style="font-size:11.5px;color:var(--tx1)">45 temporal</span>
            </div>
            <div style="display:flex;justify-content:space-between;">
              <span style="font-size:11.5px;color:var(--tx3)">Train sequences</span>
              <span style="font-size:11.5px;color:var(--tx1)">120 (Phase 3C audit)</span>
            </div>
            <div class="hdiv"></div>
            <div style="font-size:10px;color:var(--tx3);line-height:1.55;">
              LR selected over Gradient Boosting for native coefficient interpretability — no SHAP approximation required.
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- ═══ XAI: MODEL CONTRIBUTIONS ═══ -->
    <div class="section" id="sec-xai">
      <div class="sec-head">
        <div class="sec-title"><span class="sec-dot" style="background:var(--violet)"></span>Why Did the Model Decide This?</div>
        <div class="sec-sub">Model contribution analysis — coefficient attribution per feature (scaled value × LR coefficient). Deterministic, exact, no approximation.</div>
      </div>
      <div id="xai-content">
        <div class="empty-state">
          <div class="empty-state-icon">◌</div>
          <div class="empty-state-title">Awaiting Prediction</div>
          <div class="empty-state-sub">Contributions will appear once the temporal buffer is warm and a live prediction is generated.</div>
        </div>
      </div>
    </div>

    <!-- ═══ INCIDENT INTELLIGENCE ═══ -->
    <div class="section" id="sec-rootcause">
      <div class="sec-head">
        <div class="sec-title"><span class="sec-dot" style="background:var(--amber)"></span>Likely Failure Category</div>
        <div class="sec-sub">Evidence-based model interpretation of XAI attributions — does not establish mechanical causality</div>
      </div>
      <div id="rc-content">
        <div class="empty-state">
          <div class="empty-state-icon">○</div>
          <div class="empty-state-title">No Active Incident</div>
          <div class="empty-state-sub">Failure category inference appears once a prediction is live.</div>
        </div>
      </div>
    </div>

    <!-- ═══ DECISION & RECOVERY ═══ -->
    <div class="section" id="sec-decision">
      <div class="sec-head">
        <div class="sec-title"><span class="sec-dot" style="background:var(--amber)"></span>Autonomous Decision &amp; Recovery</div>
        <div class="sec-sub">Decision engine selects a recovery action based on the inferred failure category. Healing is simulated — not production.</div>
      </div>
      <div id="dec-content">
        <div class="empty-state">
          <div class="empty-state-icon">○</div>
          <div class="empty-state-title">Decision Engine Idle</div>
          <div class="empty-state-sub">Engine activates when risk reaches HIGH or CRITICAL threshold.</div>
        </div>
      </div>
    </div>

    <!-- ═══ RECOVERY VERIFICATION ═══ -->
    <div class="section" id="sec-verification">
      <div class="sec-head">
        <div class="sec-title"><span class="sec-dot" style="background:var(--green)"></span>Recovery Verification</div>
        <div class="sec-sub">Post-healing re-evaluation — same ML model, simulated normal telemetry sequence. Detect → Act → Verify.</div>
      </div>
      <div id="ver-content">
        <div class="empty-state">
          <div class="empty-state-icon">○</div>
          <div class="empty-state-title">No Recovery Executed</div>
          <div class="empty-state-sub">Verification runs automatically after a HIGH or CRITICAL risk triggers a healing action.</div>
        </div>
      </div>
    </div>

    <!-- ═══ EVENT TIMELINE ═══ -->
    <div class="section" id="sec-timeline">
      <div class="sec-head">
        <div class="sec-title"><span class="sec-dot" style="background:var(--blue)"></span>Incident &amp; Event Timeline</div>
        <div class="sec-sub">Chronological pipeline event log — predictions, actions, verifications</div>
      </div>
      <div id="tl-list"></div>
    </div>

    <!-- ═══ SIMULATION LAB ═══ -->
    <div class="section" id="sec-simulation">
      <div class="sec-head">
        <div class="sec-title"><span class="sec-dot" style="background:var(--blue)"></span>Simulation Lab</div>
        <div class="sec-sub">Inject controlled infrastructure failure scenarios into the predictive AI pipeline</div>
      </div>
      <div class="sim-grid">
        <div class="sim-card sel" data-s="normal" onclick="pickSim(this)">
          <div class="sc-icon">◉</div>
          <div class="sc-name">Normal Baseline</div>
          <div class="sc-desc">Healthy operation with expected variance</div>
        </div>
        <div class="sim-card" data-s="cpu_spike" onclick="pickSim(this)">
          <div class="sc-icon">▲</div>
          <div class="sc-name">CPU Spike</div>
          <div class="sc-desc">Sudden sustained CPU resource overload</div>
        </div>
        <div class="sim-card" data-s="memory_leak" onclick="pickSim(this)">
          <div class="sc-icon">⊛</div>
          <div class="sc-name">Memory Leak</div>
          <div class="sc-desc">Progressive memory consumption</div>
        </div>
        <div class="sim-card" data-s="disk_full" onclick="pickSim(this)">
          <div class="sc-icon">▦</div>
          <div class="sc-name">Disk Exhaustion</div>
          <div class="sc-desc">Gradual storage depletion</div>
        </div>
        <div class="sim-card" data-s="network_issue" onclick="pickSim(this)">
          <div class="sc-icon">⊙</div>
          <div class="sc-name">Network Degradation</div>
          <div class="sc-desc">Throughput and packet loss degradation</div>
        </div>
        <div class="sim-card" data-s="combined" onclick="pickSim(this)">
          <div class="sc-icon">✦</div>
          <div class="sc-name">Combined Failure</div>
          <div class="sc-desc">Multi-resource simultaneous degradation</div>
        </div>
      </div>
      <button id="run-sim" onclick="runSim()">
        <svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor"><polygon points="5 3 19 12 5 21 5 3"/></svg>
        RUN SIMULATION
      </button>
      <div class="sim-active-box">
        <div class="sim-active-dot"></div>
        <span style="font-size:9.5px;color:var(--tx3);letter-spacing:.05em;text-transform:uppercase;margin-right:6px;">Running:</span>
        <span id="sim-active-name">Normal Baseline</span>
      </div>
    </div>

  </main>
</div>

<script>
// ================================================================
// STATE
// ================================================================
const S = {
  scenario: 'normal',
  hBuf: { cpu_percent:[], memory_percent:[], disk_percent:[], net_bytes_sent_rate:[], net_bytes_recv_rate:[] },
  HMAX: 22,
  events: [],
  EMAX: 50,
  lastHeal: null,
};

const MCFG = [
  { key:'cpu_percent',          lbl:'CPU',      unit:'%',    col:'#f97316' },
  { key:'memory_percent',       lbl:'Memory',   unit:'%',    col:'#3b82f6' },
  { key:'disk_percent',         lbl:'Disk',     unit:'%',    col:'#f59e0b' },
  { key:'net_bytes_sent_rate',  lbl:'Net Sent', unit:'MB/s', col:'#22c55e' },
  { key:'net_bytes_recv_rate',  lbl:'Net Recv', unit:'MB/s', col:'#a78bfa' },
];

function rcol(lvl) { return {LOW:'#22c55e',MEDIUM:'#f59e0b',HIGH:'#ef4444',CRITICAL:'#ef4444',WARMING_UP:'#4b8eff'}[lvl]||'#424d65'; }
function rbg(lvl)  { return {LOW:'rgba(34,197,94,.07)',MEDIUM:'rgba(245,158,11,.07)',HIGH:'rgba(239,68,68,.09)',CRITICAL:'rgba(239,68,68,.12)',WARMING_UP:'rgba(75,142,255,.07)'}[lvl]||'transparent'; }
const $ = id => document.getElementById(id);

// ================================================================
// SIDEBAR
// ================================================================
let sbOpen = true;
function toggleSb() { sbOpen=!sbOpen; document.getElementById('sidebar').classList.toggle('collapsed',!sbOpen); }
function sbClick(el) { document.querySelectorAll('.sb-item').forEach(i=>i.classList.remove('active')); el.classList.add('active'); }

// ================================================================
// SIMULATION
// ================================================================
function pickSim(el) {
  document.querySelectorAll('.sim-card').forEach(c=>c.classList.remove('sel'));
  el.classList.add('sel');
  S.scenario = el.dataset.s;
}
function runSim() {
  Object.keys(S.hBuf).forEach(k=>S.hBuf[k]=[]);
  S.lastHeal = null;
  const nm = document.querySelector('.sim-card.sel .sc-name')?.textContent || S.scenario;
  $('sim-active-name').textContent = nm;
  addEv('info','SIMULATION',`Scenario activated: ${nm}`);
  pollBackend();
}

// ================================================================
// EVENTS / TIMELINE
// ================================================================
function addEv(type, cat, msg) {
  const n=new Date(), ts=`${n.getHours().toString().padStart(2,'0')}:${n.getMinutes().toString().padStart(2,'0')}:${n.getSeconds().toString().padStart(2,'0')}`;
  const cm={info:'#4b8eff',success:'#22c55e',warning:'#f59e0b',alert:'#ef4444',action:'#f97316'};
  S.events.unshift({ts, cat, msg, col: cm[type]||'#424d65'});
  if (S.events.length > S.EMAX) S.events.length = S.EMAX;
  renderTimeline();
}
function renderTimeline() {
  const el=$('tl-list'); if(!el) return;
  el.innerHTML = S.events.map((e,i) => `
    <div class="tl-item">
      <div class="tl-ts">${e.ts}</div>
      <div class="tl-track">
        <div class="tl-dot" style="background:${e.col}"></div>
        ${i < S.events.length-1 ? '<div class="tl-line"></div>' : ''}
      </div>
      <div class="tl-body">
        <div class="tl-cat" style="color:${e.col}">${e.cat}</div>
        <div class="tl-msg">${e.msg}</div>
      </div>
    </div>`).join('');
}

// ================================================================
// PIPELINE
// ================================================================
function setPipe(active) {
  for(let i=0;i<8;i++){
    const el=$(`ps${i}`); if(!el) continue;
    el.classList.remove('done','active');
    if(i<active) el.classList.add('done');
    else if(i===active) el.classList.add('active');
  }
}

// ================================================================
// SPARKLINE SVG
// ================================================================
function spark(vals, col, h=32) {
  if(!vals||vals.length<2) return `<svg style="width:100%;height:${h}px"></svg>`;
  const mn=Math.min(...vals), mx=Math.max(...vals), rng=mx-mn||.001;
  const W=180, pad=2;
  const pts=vals.map((v,i)=>[
    (pad + (i/(vals.length-1))*(W-pad*2)).toFixed(1),
    (h-pad - ((v-mn)/rng)*(h-pad*2)).toFixed(1)
  ]);
  const line=`M${pts[0].join(',')}${pts.slice(1).map(p=>`L${p.join(',')}`).join('')}`;
  const area=`${line} L${pts[pts.length-1][0]},${h} L${pts[0][0]},${h} Z`;
  const gid=`sg${col.replace('#','')}`;
  return `<svg viewBox="0 0 ${W} ${h}" preserveAspectRatio="none" style="width:100%;height:${h}px">
    <defs><linearGradient id="${gid}" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="${col}" stop-opacity=".22"/>
      <stop offset="100%" stop-color="${col}" stop-opacity="0"/>
    </linearGradient></defs>
    <path d="${area}" fill="url(#${gid})"/>
    <path d="${line}" fill="none" stroke="${col}" stroke-width="1.5" stroke-linejoin="round" stroke-linecap="round"/>
    <circle cx="${pts[pts.length-1][0]}" cy="${pts[pts.length-1][1]}" r="2.5" fill="${col}"/>
  </svg>`;
}

// ================================================================
// MULTI-LINE CHART
// ================================================================
function mlChart(datasets, W=800, H=148) {
  if(!datasets||!datasets[0]||datasets[0].values.length<2) return '';
  const n=datasets[0].values.length;
  const pL=36,pR=12,pT=10,pB=10;
  const cW=W-pL-pR, cH=H-pT-pB;
  let out='';
  // Grid
  for(let g=0;g<=4;g++){
    const y=pT+(g/4)*cH;
    out+=`<line x1="${pL}" y1="${y.toFixed(1)}" x2="${W-pR}" y2="${y.toFixed(1)}" stroke="#1d2334" stroke-width="0.6" stroke-dasharray="3,5"/>`;
  }
  for(let g=0;g<n;g++){
    const x=pL+(g/(n-1))*cW;
    out+=`<line x1="${x.toFixed(1)}" y1="${pT}" x2="${x.toFixed(1)}" y2="${H-pB}" stroke="#1d2334" stroke-width="0.4"/>`;
  }
  // Y-axis ticks
  for(let g=0;g<=4;g++){
    const y=pT+(g/4)*cH;
    out+=`<text x="${pL-5}" y="${y.toFixed(1)}" font-size="8" fill="#424d65" text-anchor="end" dominant-baseline="middle" font-family="monospace">${(100-g*25)}%</text>`;
  }
  // Lines
  datasets.forEach(ds=>{
    if(!ds.values||ds.values.length<2) return;
    const mn=Math.min(...ds.values), mx=Math.max(...ds.values), rng=mx-mn||.001;
    const pts=ds.values.map((v,i)=>[
      (pL+(i/(n-1))*cW).toFixed(1),
      (pT+cH-((v-mn)/rng)*cH).toFixed(1)
    ]);
    const lp=`M${pts[0].join(',')}${pts.slice(1).map(p=>`L${p.join(',')}`).join('')}`;
    const ap=`${lp} L${pts[pts.length-1][0]},${H-pB} L${pL},${H-pB} Z`;
    const gid=`mc${ds.col.replace('#','')}`;
    out+=`<defs><linearGradient id="${gid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="${ds.col}" stop-opacity=".14"/><stop offset="100%" stop-color="${ds.col}" stop-opacity="0"/></linearGradient></defs>`;
    out+=`<path d="${ap}" fill="url(#${gid})"/>`;
    out+=`<path d="${lp}" fill="none" stroke="${ds.col}" stroke-width="1.6" stroke-linejoin="round" stroke-linecap="round" opacity=".9"/>`;
    const lpt=pts[pts.length-1];
    out+=`<circle cx="${lpt[0]}" cy="${lpt[1]}" r="2.5" fill="${ds.col}"/>`;
    // Label at right edge
    out+=`<text x="${(W-pR+5).toFixed(1)}" y="${lpt[1]}" font-size="8" fill="${ds.col}" dominant-baseline="middle" font-family="monospace">${ds.values[ds.values.length-1].toFixed(1)}</text>`;
  });
  // NOW line
  out+=`<line x1="${W-pR}" y1="${pT}" x2="${W-pR}" y2="${H-pB}" stroke="rgba(220,225,238,.15)" stroke-width="1" stroke-dasharray="2,4"/>`;
  out+=`<text x="${(W-pR-3).toFixed(1)}" y="${pT-2}" font-size="7" fill="rgba(220,225,238,.25)" text-anchor="end" font-family="monospace">NOW</text>`;
  return out;
}

// ================================================================
// RENDER OVERVIEW
// ================================================================
function renderOverview(data) {
  const pred=data.prediction, rl=pred.risk_level, rs=pred.risk_score;
  const col=rcol(rl), bg=rbg(rl), isWarm=(pred.status==='WARMING_UP');
  const descMap={
    WARMING_UP:'Collecting temporal history — prediction activates after 10 timesteps are buffered.',
    LOW:'No impending failure predicted within the current 10-step horizon. System is operating normally.',
    MEDIUM:'Temporal trajectory shows elevated patterns. System is under observation.',
    HIGH:'Temporal features indicate high failure probability. Decision engine has been engaged.',
    CRITICAL:'Critical failure risk. Immediate simulated recovery triggered by the decision engine.',
  };
  $('risk-desc').textContent = descMap[rl]||'';
  $('risk-level-lbl').textContent = rl||'—';
  $('risk-level-lbl').style.color = col;
  $('risk-scenario-lbl').textContent = `Scenario: ${(S.scenario||'').replace(/_/g,' ').toUpperCase()}`;
  $('score-num').textContent = rs.toFixed(4);
  $('score-num').style.color = col;

  const pct = Math.min(rs*100,100);
  $('risk-fill').style.width = `${pct.toFixed(1)}%`;
  $('risk-fill').style.background = col;
  $('risk-ptr').style.left = `calc(${pct.toFixed(1)}% - 1px)`;

  const chip=$('status-chip');
  chip.style.color=col; chip.style.borderColor=col; chip.style.background=bg;
  $('status-chip-dot').style.background=col;
  $('status-chip-txt').textContent=isWarm?'WARMING UP':rl;

  const nb=$('nav-risk-badge');
  nb.textContent=isWarm?'INIT':rl; nb.style.color=col; nb.style.borderColor=col; nb.style.background=bg;

  // Prediction section
  $('pred-risk-lbl').textContent=rl; $('pred-risk-lbl').style.color=col;
  $('pred-score-lbl').textContent=rs.toFixed(4); $('pred-score-lbl').style.color=col;
  $('pred-status-msg').textContent=isWarm?'Warming up — building 10-step temporal buffer…':`Label: ${pred.label===1?'FAILURE RISK':'NOMINAL'} · Status: LIVE`;
  $('pred-status-msg').style.color=isWarm?'var(--tx3)':col;
}

// ================================================================
// RENDER METRICS
// ================================================================
function renderMetrics(tel) {
  MCFG.forEach(m=>{ const v=tel[m.key]; if(v!==undefined){ S.hBuf[m.key].push(parseFloat(v.toFixed(4))); if(S.hBuf[m.key].length>S.HMAX) S.hBuf[m.key].shift(); }});
  const el=$('metric-row'); if(!el) return;
  let h='';
  MCFG.forEach(m=>{
    const v=tel[m.key], buf=S.hBuf[m.key], prev=buf.length>=2?buf[buf.length-2]:v;
    const d=v!==undefined?(v-prev):0;
    const ds=d>0.05?'▲':(d<-0.05?'▼':'—');
    const dc=d>0.05?'#ef4444':(d<-0.05?'#22c55e':'#424d65');
    h+=`<div class="mc">
      <div class="mc-name">${m.lbl}</div>
      <div class="mc-val mono">${v!==undefined?v.toFixed(2):'—'}<span class="mc-unit">${m.unit}</span></div>
      <div class="mc-spark">${spark(buf,m.col)}</div>
      <div class="mc-delta" style="color:${dc}">${ds}<span style="font-size:9.5px;color:var(--tx3);margin-left:2px;">${Math.abs(d).toFixed(2)} ${m.unit}</span></div>
    </div>`;
  });
  el.innerHTML=h;
}

// ================================================================
// RENDER TEMPORAL
// ================================================================
function renderTemporal() {
  const datasets=MCFG.map(m=>({ col:m.col, values:S.hBuf[m.key].slice(-10) }));
  const mc=$('main-chart'); if(mc) mc.innerHTML=mlChart(datasets);
  const st=$('temporal-stats'); if(!st) return;
  let h='';
  MCFG.forEach(m=>{
    const buf=S.hBuf[m.key].slice(-10), last=buf[buf.length-1];
    const slope=buf.length>=2?(buf[buf.length-1]-buf[0]):0;
    const sd=slope>0.5?'▲':(slope<-0.5?'▼':'→');
    const sc=slope>0.5?'#ef4444':(slope<-0.5?'#22c55e':'#424d65');
    h+=`<div class="ts-cell">
      <div class="ts-name">${m.lbl}</div>
      <div class="ts-val mono">${last!==undefined?last.toFixed(2):'—'}<span style="font-size:9px;color:var(--tx3);margin-left:2px;">${m.unit}</span></div>
      <div class="ts-delta" style="color:${sc}">${sd} ${Math.abs(slope).toFixed(2)}</div>
    </div>`;
  });
  st.innerHTML=h;
}

// ================================================================
// RENDER XAI
// ================================================================
function renderXAI(xai) {
  const el=$('xai-content'); if(!el) return;
  if(!xai||!xai.top_features||!xai.top_features.length){
    el.innerHTML=`<div class="empty-state"><div class="empty-state-icon">◌</div><div class="empty-state-title">Awaiting Prediction</div><div class="empty-state-sub">XAI contributions appear once a live prediction is generated.</div></div>`;
    return;
  }
  const maxA=Math.max(...xai.top_features.map(f=>f.abs_contribution));
  const nPos=xai.top_features.filter(f=>f.direction==='positive').length;
  const nNeg=xai.top_features.filter(f=>f.direction==='negative').length;
  let interp='Evidence shows a moderate mix of risk-increasing and risk-reducing factors.';
  if(nPos>=4) interp='Multiple features are actively increasing failure probability. The model sees strong risk signals.';
  else if(nNeg>=4) interp='Most contributing features are suppressing failure probability. System trajectory appears stable from the model\'s perspective.';
  else if(nPos>=3) interp='More features push toward failure than away. Elevated caution is warranted.';

  let h=`<div class="xai-intro">${interp}</div>`;
  xai.top_features.forEach((f,i)=>{
    const isP=f.direction==='positive';
    const col=isP?'#ef4444':'#3b82f6';
    const cbg=isP?'rgba(239,68,68,.1)':'rgba(59,130,246,.1)';
    const w=maxA>0?((f.abs_contribution/maxA)*100).toFixed(1):0;
    const sign=isP?'+':'';
    h+=`<div class="xai-row">
      <div class="xai-rank">#${i+1}</div>
      <div class="xai-name" title="${f.feature}">${f.human_readable_name}</div>
      <div class="xai-bar">
        <div class="xai-track"><div class="xai-fill" style="width:${w}%;background:${col}"></div></div>
      </div>
      <div class="xai-val" style="color:${col}">${sign}${f.contribution.toFixed(4)}</div>
      <div class="xai-dir" style="color:${col};background:${cbg}">${isP?'RISK ↑':'RISK ↓'}</div>
    </div>`;
  });
  h+=`<div class="xai-footer">Method: Logistic Regression linear coefficient attribution — contribution = (scaled feature value) × (model coefficient). Deterministic and mathematically exact for LR. No SHAP approximation. Positive values increase failure probability; negative values decrease it.</div>`;
  el.innerHTML=h;
}

// ================================================================
// RENDER ROOT CAUSE
// ================================================================
function renderRC(rc) {
  const el=$('rc-content'); if(!el) return;
  if(!rc||rc.category==='N/A'){
    el.innerHTML=`<div class="empty-state"><div class="empty-state-icon">○</div><div class="empty-state-title">No Active Incident</div><div class="empty-state-sub">Root-cause inference appears once a prediction is live.</div></div>`;
    return;
  }
  const catCol={'CPU Spike':'#f97316','Memory Leak':'#3b82f6','Disk Exhaustion':'#f59e0b','Network Degradation':'#a78bfa','Combined Failure':'#ef4444','Unknown / Mixed':'#424d65'};
  const col=catCol[rc.category]||'#f59e0b';
  const evCol={CPU:'#f97316',Memory:'#3b82f6',Disk:'#f59e0b',Network:'#a78bfa'};
  const maxE=rc.evidence_scores?Math.max(...Object.values(rc.evidence_scores)):1;
  let evH='';
  if(rc.evidence_scores) {
    Object.entries(rc.evidence_scores).forEach(([k,v])=>{
      const w=maxE>0?((v/maxE)*100).toFixed(1):0;
      const ec=evCol[k]||'#424d65';
      const str=v>0.4?'Strong evidence':(v>0.2?'Moderate evidence':'Weak evidence');
      evH+=`<div class="ev-item">
        <div class="ev-header"><span class="ev-label">${k}</span><span class="ev-strength" style="color:${ec}">${str}</span></div>
        <div class="ev-track"><div class="ev-fill" style="width:${w}%;background:${ec}"></div></div>
      </div>`;
    });
  }
  el.innerHTML=`<div class="rc-layout">
    <div>
      <div class="label" style="margin-bottom:8px;">Inferred Category</div>
      <div class="rc-cat-name" style="color:${col}">${rc.category.toUpperCase()}</div>
      <div class="rc-cat-note">Evidence-based model interpretation of XAI attributions. Does not establish mechanical causality.</div>
    </div>
    <div>
      <div class="label" style="margin-bottom:12px;">Evidence Breakdown</div>
      ${evH}
      ${rc.explanation_text?`<div class="rc-explain">${rc.explanation_text}</div>`:''}
    </div>
  </div>`;
}

// ================================================================
// RENDER DECISION
// ================================================================
function renderDecision(dec, heal) {
  const el=$('dec-content'); if(!el) return;
  const healed=(heal.status==='Executed');
  if(!healed){
    el.innerHTML=`<div class="dec-grid">
      <div><div class="dec-field-label">Recommended Recovery</div><div class="dec-field-val">${dec.recommended_action||'—'}</div><div class="dec-reason">${dec.reason||''}</div></div>
      <div class="dec-vdiv"></div>
      <div><div class="dec-field-label">Engine Status</div><div class="dec-field-val" style="color:var(--tx2)">Monitoring — below action threshold</div><div style="margin-top:10px;"><span class="chip" style="color:var(--tx3);border-color:var(--br);background:var(--s2);">IDLE</span></div></div>
    </div>`;
    return;
  }
  el.innerHTML=`<div class="dec-grid">
    <div>
      <div class="dec-field-label">Detected Condition</div>
      <div class="dec-field-val">${dec.recommended_action||'—'}</div>
      <div class="dec-reason">${dec.reason||''}</div>
    </div>
    <div class="dec-vdiv"></div>
    <div>
      <div class="dec-field-label">Simulated Recovery Action</div>
      <div class="dec-field-val" style="color:var(--amber)">${heal.action||'—'}</div>
      <div style="display:flex;gap:7px;margin-top:10px;flex-wrap:wrap;">
        <span class="chip" style="color:var(--amber);border-color:rgba(245,158,11,.35);background:rgba(245,158,11,.08);">SIMULATED ACTION</span>
        <span class="chip" style="color:var(--tx3);border-color:var(--br);background:var(--s2);">NOT PRODUCTION</span>
      </div>
    </div>
  </div>`;
}

// ================================================================
// RENDER VERIFICATION
// ================================================================
function renderVerif(heal) {
  const el=$('ver-content'); if(!el) return;
  if(heal.status!=='Executed'||!heal.evidence){
    el.innerHTML=`<div class="empty-state"><div class="empty-state-icon">○</div><div class="empty-state-title">No Recovery Executed</div><div class="empty-state-sub">Verification runs after HIGH or CRITICAL risk triggers healing.</div></div>`;
    return;
  }
  const bef=heal.evidence.before, aft=heal.evidence.after, ver=heal.verification;
  const vm={RECOVERED:{col:'#22c55e',bg:'rgba(34,197,94,.08)',lbl:'RECOVERED'},NOT_RECOVERED:{col:'#ef4444',bg:'rgba(239,68,68,.08)',lbl:'NOT RECOVERED'},INCONCLUSIVE:{col:'#f59e0b',bg:'rgba(245,158,11,.08)',lbl:'INCONCLUSIVE'}};
  const vs=vm[ver]||{col:'#424d65',bg:'transparent',lbl:ver||'—'};
  const delta=bef&&aft?(bef.risk_score-aft.risk_score):null;
  const improved=delta!==null&&delta>0;
  el.innerHTML=`<div class="ver-layout">
    <div class="ver-side" style="border-color:${rcol(bef?.risk_level)}44">
      <div class="ver-side-lbl">Before Recovery</div>
      <div class="ver-risk-txt" style="color:${rcol(bef?.risk_level)}">${bef?.risk_level||'—'}</div>
      <div class="ver-score-txt mono">Score: ${bef?.risk_score?.toFixed(4)||'—'}</div>
      <div style="margin-top:8px;"><span class="chip" style="color:${rcol(bef?.risk_level)};border-color:${rcol(bef?.risk_level)}44;background:${rbg(bef?.risk_level)}">${bef?.risk_level||'—'}</span></div>
    </div>
    <div class="ver-mid">
      <div class="ver-arrow">↓</div>
      <div class="ver-status" style="color:${vs.col};border-color:${vs.col}55;background:${vs.bg}">
        <div class="ver-status-txt">${vs.lbl}</div>
      </div>
      ${delta!==null?`<div class="ver-delta" style="color:${improved?'#22c55e':'#ef4444'}">${improved?'▼':'▲'} ${(Math.abs(delta)*100).toFixed(1)}% score change</div>`:''}
      <div class="ver-note">Re-prediction on simulated normal telemetry</div>
    </div>
    <div class="ver-side" style="border-color:${rcol(aft?.risk_level)}44">
      <div class="ver-side-lbl">After Recovery</div>
      <div class="ver-risk-txt" style="color:${rcol(aft?.risk_level)}">${aft?.risk_level||'—'}</div>
      <div class="ver-score-txt mono">Score: ${aft?.risk_score?.toFixed(4)||'—'}</div>
      <div style="margin-top:8px;"><span class="chip" style="color:${rcol(aft?.risk_level)};border-color:${rcol(aft?.risk_level)}44;background:${rbg(aft?.risk_level)}">${aft?.risk_level||'—'}</span></div>
    </div>
  </div>
  <div class="ver-footnote">Simulated recovery: a 10-step normal baseline telemetry sequence was generated and evaluated by the same Logistic Regression model. INCONCLUSIVE indicates risk decreased but did not reach the LOW threshold. This does not represent real cloud infrastructure recovery.</div>`;
}

// ================================================================
// MAIN POLL
// ================================================================
function pollBackend() {
  setPipe(0);
  fetch(`/api/scan?scenario=${S.scenario}`)
    .then(r=>r.json())
    .then(d=>{
      if(d.error){ addEv('alert','API ERROR',d.message); return; }
      const pred=d.prediction, rl=pred.risk_level, isW=pred.status==='WARMING_UP';

      if(isW) setPipe(0);
      else if(d.healing?.status==='Executed') setPipe(7);
      else if(rl==='HIGH'||rl==='CRITICAL') setPipe(5);
      else setPipe(3);

      renderOverview(d);
      renderMetrics(d.telemetry);
      renderTemporal();

      if(!isW){
        renderXAI(d.xai);
        renderRC(d.root_cause);
        renderDecision(d.decision, d.healing);
        renderVerif(d.healing);

        if(d.healing?.status==='Executed'&&d.healing.status!==S.lastHeal){
          addEv('action','HEALING',`Simulated: ${d.healing.action}`);
          addEv(d.healing.verification==='RECOVERED'?'success':'warning','VERIFICATION',
            `Result: ${d.healing.verification} — Before: ${d.healing.evidence?.before?.risk_level} → After: ${d.healing.evidence?.after?.risk_level}`);
          S.lastHeal=d.healing.status;
        }
      } else {
        renderXAI(null); renderRC(null); renderDecision({recommended_action:'Waiting…',reason:'Insufficient history'},{status:'Skipped'}); renderVerif({status:'Skipped'});
      }
    })
    .catch(err=>addEv('alert','FETCH ERROR',err.toString()));
}

// ================================================================
// BOOT
// ================================================================
addEv('success','SYSTEM','Platform online — LR model loaded (Phase 3C · Seed 42 · 45 features).');
addEv('info','CONFIG','10-step temporal prediction horizon · StandardScaler · class_weight=balanced');
renderTimeline();
pollBackend();
setInterval(pollBackend, 1500);
</script>
</body>
</html>"""


@app.route("/")
def index():
    """Serve the XAI Cloud Operations Platform."""
    return render_template_string(HTML)


if __name__ == "__main__":
    init_api_model()
    app.run(host="0.0.0.0", port=config.PORT, debug=False)
