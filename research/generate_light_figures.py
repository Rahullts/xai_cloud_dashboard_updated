"""
generate_light_figures.py
Generates clean, light-background, print-friendly academic vector figures (PDF + SVG)
for the IEEE conference paper:
"Explainable AI-Driven Autonomous Self-Healing Cloud Management Platform"
"""

import os
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# Destination directories
OUT_DIRS = [
    Path("C:/Users/rahul/.gemini/antigravity/scratch/xai_cloud_dashboard_updated/01_PAPER_CURRENT/figures"),
    Path("C:/Users/rahul/.gemini/antigravity/scratch/xai_cloud_dashboard_updated/research/figures_light")
]

for d in OUT_DIRS:
    d.mkdir(parents=True, exist_ok=True)

# Set global academic typography & styling
plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "DejaVu Serif", "Times"],
    "font.size": 10,
    "axes.titlesize": 11,
    "axes.labelsize": 10,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "legend.fontsize": 9,
    "figure.titlesize": 12,
    "text.color": "#0f172a",
    "axes.labelcolor": "#0f172a",
    "xtick.color": "#0f172a",
    "ytick.color": "#0f172a",
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "figure.dpi": 300,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.05
})

def save_fig(fig, base_name):
    for d in OUT_DIRS:
        pdf_path = d / f"{base_name}.pdf"
        svg_path = d / f"{base_name}.svg"
        fig.savefig(pdf_path, format="pdf")
        fig.savefig(svg_path, format="svg")
    print(f"Saved {base_name}.pdf and {base_name}.svg to {len(OUT_DIRS)} directories.")
    plt.close(fig)

# ==============================================================================
# FIGURE 1: System Architecture (Ten-Stage Pipeline)
# ==============================================================================
def make_fig1_architecture():
    fig = plt.figure(figsize=(8.5, 4.3), facecolor="white")
    ax = fig.add_subplot(111)
    ax.set_facecolor("white")
    ax.set_xlim(0, 850)
    ax.set_ylim(0, 440)
    ax.axis("off")

    # Title
    ax.text(425, 420, "System Architecture: Ten-Stage Autonomous Closed-Loop Pipeline",
            ha="center", va="center", fontsize=11.5, fontweight="bold", color="#0f172a")

    # Stage metadata: (stage_num, title, subtitle, x, y, w, h, border_color, fill_color)
    stages = [
        # Top Row (left to right, y=280)
        (1, "Telemetry Ingestion", "5 raw metric streams\n(CPU, Mem, Disk, Net)", 25, 270, 140, 72, "#2563eb", "#eff6ff"),
        (2, "Anomaly Detection", "Snapshot baseline\nIsolation Forest", 195, 270, 140, 72, "#0d9488", "#f0fdfa"),
        (3, "Temporal Buffer", "10-step FIFO window\nTrailing history", 365, 270, 140, 72, "#2563eb", "#eff6ff"),
        (4, "Feature Extraction", "45 leak-free features\nMean, slope, std, delta", 535, 270, 140, 72, "#7c3aed", "#faf5ff"),
        (5, "Failure Prediction", "Logistic Regression\nHorizon: t+1..t+10", 705, 270, 140, 72, "#dc2626", "#fef2f2"),
        
        # Bottom Row (right to left, y=120)
        (6, "XAI Attribution", "Exact coeff. method\nc_i = z_i * w_i (deterministic)", 705, 120, 140, 72, "#2563eb", "#eff6ff"),
        (7, "Failure Category", "Evidence score sum\nDomain attribution (CPU..)", 535, 120, 140, 72, "#d97706", "#fffbeb"),
        (8, "Decision Logic", "Rule-based mapping\nRisk >= 0.50 threshold", 365, 120, 140, 72, "#d97706", "#fffbeb"),
        (9, "Simulated Healing", "Targeted mock action\n(String selection, not API)", 195, 120, 140, 72, "#d97706", "#fffbeb"),
        (10, "Model Verification", "Re-predict on normal proxy\nVerdict: RECOVERED / INCONC.", 25, 120, 140, 72, "#16a34a", "#f0fdf4"),
    ]

    for s_num, title, subtitle, x, y, w, h, border, fill in stages:
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=6",
                                      facecolor=fill, edgecolor=border, linewidth=1.4)
        ax.add_patch(rect)
        # Stage badge
        badge = patches.FancyBboxPatch((x + 8, y + h - 17), 54, 13, boxstyle="round,pad=0,rounding_size=3",
                                       facecolor=border, edgecolor="none")
        ax.add_patch(badge)
        ax.text(x + 35, y + h - 10.5, f"STAGE {s_num}", ha="center", va="center", fontsize=7.2, fontweight="bold", color="white")
        
        # Title & subtitle
        ax.text(x + w/2, y + h - 31, title, ha="center", va="center", fontsize=9.2, fontweight="bold", color="#0f172a")
        ax.text(x + w/2, y + 17, subtitle, ha="center", va="center", fontsize=7.8, color="#475569")

    # Connectors
    kw = dict(arrowstyle="-|>", color="#475569", lw=1.4, mutation_scale=13)
    # Top row forward arrows
    ax.annotate("", xy=(195, 306), xytext=(165, 306), arrowprops=kw)
    ax.annotate("", xy=(365, 306), xytext=(335, 306), arrowprops=kw)
    ax.annotate("", xy=(535, 306), xytext=(505, 306), arrowprops=kw)
    ax.annotate("", xy=(705, 306), xytext=(675, 306), arrowprops=kw)

    # Vertical turn: Stage 5 to Stage 6
    ax.annotate("", xy=(775, 192), xytext=(775, 270), arrowprops=kw)
    ax.text(785, 231, "Predicted Risk", ha="left", va="center", fontsize=7.8, color="#dc2626", fontweight="bold")

    # Bottom row backward arrows
    ax.annotate("", xy=(675, 156), xytext=(705, 156), arrowprops=kw)
    ax.annotate("", xy=(505, 156), xytext=(535, 156), arrowprops=kw)
    ax.annotate("", xy=(335, 156), xytext=(365, 156), arrowprops=kw)
    ax.annotate("", xy=(165, 156), xytext=(195, 156), arrowprops=kw)

    # Feedback loop: Stage 10 back to Stage 3 Buffer
    ax.annotate("", xy=(385, 270), xytext=(75, 192),
                arrowprops=dict(arrowstyle="-|>", color="#16a34a", lw=1.4, ls="--",
                                connectionstyle="arc3,rad=-0.25", mutation_scale=13))
    ax.text(180, 231, "Post-Remediation Feedback\n(10-Step Buffer Reset)",
            ha="center", va="center", fontsize=7.8, color="#16a34a", fontweight="bold")

    # Phase grouping banners at bottom
    ax.plot([25, 845], [68, 68], color="#e2e8f0", lw=0.8)
    
    # Phase 1
    p1 = patches.FancyBboxPatch((25, 28), 310, 26, boxstyle="round,pad=0,rounding_size=4", facecolor="#f8fafc", edgecolor="#cbd5e1", lw=0.8)
    ax.add_patch(p1)
    ax.text(180, 41, "Phase 1: Telemetry & Snapshot Anomaly Detection", ha="center", va="center", fontsize=8, fontweight="bold", color="#334155")

    # Phase 2
    p2 = patches.FancyBboxPatch((350, 28), 325, 26, boxstyle="round,pad=0,rounding_size=4", facecolor="#f8fafc", edgecolor="#cbd5e1", lw=0.8)
    ax.add_patch(p2)
    ax.text(512, 41, "Phase 2: Temporal Sequence Modeling & Exact XAI", ha="center", va="center", fontsize=8, fontweight="bold", color="#334155")

    # Phase 3
    p3 = patches.FancyBboxPatch((690, 28), 155, 26, boxstyle="round,pad=0,rounding_size=4", facecolor="#f8fafc", edgecolor="#cbd5e1", lw=0.8)
    ax.add_patch(p3)
    ax.text(767, 41, "Phase 3: Verification", ha="center", va="center", fontsize=8, fontweight="bold", color="#334155")

    save_fig(fig, "fig1_system_architecture")

# ==============================================================================
# FIGURE 2: Model Comparison across 5 Random Seeds (F1-Score and ROC-AUC)
# ==============================================================================
def make_fig4_model_comparison():
    fig, ax = plt.subplots(figsize=(7.2, 3.3), facecolor="white")
    ax.set_facecolor("white")

    models = [
        "Majority\nBaseline",
        "Threshold\nBaseline",
        "Logistic\nRegression",
        "Random\nForest",
        "Gradient\nBoosting"
    ]
    
    # 5-seed empirical results from Table IV
    f1_means = [0.514, 0.156, 0.692, 0.696, 0.699]
    f1_stds  = [0.259, 0.054, 0.036, 0.021, 0.030]
    
    # ROC-AUC (None for non-scoring baselines)
    auc_means = [0.0, 0.0, 0.813, 0.819, 0.826]
    auc_stds  = [0.0, 0.0, 0.021, 0.005, 0.013]

    x = np.arange(len(models))
    width = 0.36

    # Draw grid lines behind bars
    ax.grid(axis="y", linestyle="--", linewidth=0.7, color="#e2e8f0", zorder=0)

    # F1 bars
    f1_colors = ["#94a3b8", "#94a3b8", "#1d4ed8", "#2563eb", "#3b82f6"]
    bars_f1 = ax.bar(x - width/2, f1_means, width, yerr=f1_stds, capsize=4,
                     label=r"F1-Score (mean $\pm$ std)", color=f1_colors, edgecolor="#0f172a",
                     linewidth=0.8, zorder=3)

    # ROC-AUC bars (only for predictive ML models)
    auc_colors = ["#cbd5e1", "#cbd5e1", "#0f766e", "#0d9488", "#14b8a6"]
    bars_auc = ax.bar(x + width/2, auc_means, width, yerr=auc_stds, capsize=4,
                      label=r"ROC-AUC (mean $\pm$ std)", color=auc_colors, edgecolor="#0f172a",
                      linewidth=0.8, zorder=3)

    # Value tags on top of bars
    for i in range(len(models)):
        # F1 label
        h1 = f1_means[i]
        err1 = f1_stds[i]
        ax.text(x[i] - width/2, h1 + err1 + 0.025, f"{h1:.3f}", ha="center", va="bottom",
                fontsize=8, fontweight="bold", color="#0f172a")
        
        # AUC label
        h2 = auc_means[i]
        err2 = auc_stds[i]
        if h2 > 0:
            ax.text(x[i] + width/2, h2 + err2 + 0.025, f"{h2:.3f}", ha="center", va="bottom",
                    fontsize=8, fontweight="bold", color="#0f766e")
        else:
            ax.text(x[i] + width/2, 0.03, "N/A", ha="center", va="bottom",
                    fontsize=8, color="#64748b", fontstyle="italic")

    # Benchmarks & bounds
    ax.set_ylabel("Score (5-Seed Average)", fontsize=10, fontweight="bold")
    ax.set_ylim(0, 1.05)
    ax.set_xticks(x)
    ax.set_xticklabels(models, fontsize=9.5)
    
    # Baseline comparison note
    ax.axhline(0.50, color="#cbd5e1", linestyle=":", linewidth=1, zorder=1)

    # Legend
    legend = ax.legend(loc="upper left", frameon=True, facecolor="white", edgecolor="#cbd5e1", framealpha=0.95)
    legend.get_frame().set_linewidth(0.8)

    # Spines styling
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)
    for s in ["left", "bottom"]:
        ax.spines[s].set_color("#64748b")
        ax.spines[s].set_linewidth(0.8)

    save_fig(fig, "fig4_model_comparison")

# ==============================================================================
# FIGURE 3: XAI Feature Contributions (Case Study: Gradual Disk Exhaustion)
# ==============================================================================
def make_fig6_xai_contributions():
    fig, ax = plt.subplots(figsize=(7.0, 3.0), facecolor="white")
    ax.set_facecolor("white")

    # Features from test_1 (Table VII / xai_case_study_results.json)
    features = [
        "Memory 10-step mean\n(memory_percent_mean_10)",
        "Memory 10-step std\n(memory_percent_std_10)",
        "CPU 10-step std\n(cpu_percent_std_10)",
        "Net Recv 10-step mean\n(net_bytes_recv_rate_mean_10)",
        "Net Sent 10-step std\n(net_bytes_sent_rate_std_10)"
    ]
    contributions = [-0.9994, 0.5870, 0.3622, 0.3433, 0.3275]
    y_pos = np.arange(len(features))[::-1]  # Top feature at top

    # Grid
    ax.grid(axis="x", linestyle="--", linewidth=0.7, color="#e2e8f0", zorder=0)

    # Bar colors based on direction: negative (Risk Reduction) -> Blue, positive (Risk Increase) -> Red
    colors = ["#2563eb" if c < 0 else "#dc2626" for c in contributions]
    
    bars = ax.barh(y_pos, contributions, height=0.52, color=colors, edgecolor="#0f172a",
                   linewidth=0.8, zorder=3, alpha=0.9)

    # Zero reference line
    ax.axvline(0, color="#334155", linewidth=1.2, zorder=4)

    # Value tags
    for i, (val, y) in enumerate(zip(contributions, y_pos)):
        if val < 0:
            ax.text(val - 0.03, y, f"{val:+.4f} (Risk ↓)", ha="right", va="center",
                    fontsize=8.5, fontweight="bold", color="#1d4ed8")
        else:
            ax.text(val + 0.03, y, f"{val:+.4f} (Risk ↑)", ha="left", va="center",
                    fontsize=8.5, fontweight="bold", color="#b91c1c")

    ax.set_yticks(y_pos)
    ax.set_yticklabels(features, fontsize=9, fontweight="medium")
    ax.set_xlabel("Linear Attribution Score:  $c_i = z_i \\cdot w_i$", fontsize=10, fontweight="bold")
    ax.set_xlim(-1.45, 0.95)

    # Header annotation box
    info_text = "Case A: Gradual Disk Exhaustion (test_1, t=14)\nRisk Score: 0.591 (MEDIUM) | Inferred Root Cause: Combined Failure"
    ax.text(0.02, 0.96, info_text, transform=ax.transAxes, fontsize=8,
            verticalalignment="top", bbox=dict(boxstyle="round,pad=0.4", facecolor="#f8fafc", edgecolor="#cbd5e1", lw=0.8))

    # Spines styling
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)
    for s in ["left", "bottom"]:
        ax.spines[s].set_color("#64748b")
        ax.spines[s].set_linewidth(0.8)

    save_fig(fig, "fig6_xai_contributions")

# ==============================================================================
# FIGURE 4: Recovery Verification Flow (Network Degradation Evaluation)
# ==============================================================================
def make_fig7_verification():
    fig = plt.figure(figsize=(7.8, 3.0), facecolor="white")
    ax = fig.add_subplot(111)
    ax.set_facecolor("white")
    ax.set_xlim(0, 780)
    ax.set_ylim(0, 340)
    ax.axis("off")

    # Title
    ax.text(390, 320, "Closed-Loop Post-Recovery Verification Protocol (Network Degradation Scenario)",
            ha="center", va="center", fontsize=11, fontweight="bold", color="#0f172a")

    # 1. BEFORE BOX (Left)
    b_rect = patches.FancyBboxPatch((30, 90), 200, 195, boxstyle="round,pad=0,rounding_size=8",
                                    facecolor="#fef2f2", edgecolor="#dc2626", linewidth=1.8)
    ax.add_patch(b_rect)
    ax.text(130, 260, "PRE-RECOVERY STATE", ha="center", va="center", fontsize=9, fontweight="bold", color="#b91c1c")
    ax.text(130, 225, "CRITICAL", ha="center", va="center", fontsize=20, fontweight="900", color="#dc2626")
    ax.text(130, 185, "Risk Score: 0.884", ha="center", va="center", fontsize=11, fontweight="bold", color="#0f172a")
    ax.text(130, 160, "Label: 1 (Failure Impending)", ha="center", va="center", fontsize=8.5, color="#475569")
    ax.text(130, 135, "Threshold Exceeded: >= 0.50", ha="center", va="center", fontsize=8, color="#dc2626", fontstyle="italic")
    ax.text(130, 110, "Model: Logistic Regression (Seed 42)", ha="center", va="center", fontsize=7.5, color="#64748b")

    # 2. MIDDLE SECTION: Action Pill + Verification Verdict
    # Arrow 1: Before to Action
    kw = dict(arrowstyle="-|>", color="#475569", lw=1.6, mutation_scale=14)
    ax.annotate("", xy=(285, 230), xytext=(230, 230), arrowprops=kw)

    # Action Pill
    act_rect = patches.FancyBboxPatch((285, 190), 210, 80, boxstyle="round,pad=0,rounding_size=6",
                                      facecolor="#fffbeb", edgecolor="#d97706", linewidth=1.5)
    ax.add_patch(act_rect)
    ax.text(390, 250, "SIMULATED MITIGATION", ha="center", va="center", fontsize=8, fontweight="bold", color="#b45309")
    ax.text(390, 230, "Controlled recovery sequence", ha="center", va="center", fontsize=9, fontweight="bold", color="#0f172a")
    ax.text(390, 215, "+ Human operator alert", ha="center", va="center", fontsize=9, fontweight="bold", color="#0f172a")
    ax.text(390, 198, "(Simulated rule dispatch; no real cloud API)", ha="center", va="center", fontsize=7.5, color="#64748b", fontstyle="italic")

    # Arrow 2: Action to After
    ax.annotate("", xy=(550, 230), xytext=(495, 230), arrowprops=kw)

    # Verdict Box in Middle Lower
    v_rect = patches.FancyBboxPatch((280, 85), 220, 85, boxstyle="round,pad=0,rounding_size=6",
                                    facecolor="#fefce8", edgecolor="#eab308", linewidth=1.8)
    ax.add_patch(v_rect)
    ax.text(390, 150, "VERIFICATION VERDICT", ha="center", va="center", fontsize=8, fontweight="bold", color="#854d0e")
    ax.text(390, 128, "INCONCLUSIVE", ha="center", va="center", fontsize=15, fontweight="900", color="#d97706")
    ax.text(390, 105, "Score Delta: -0.437 (43.7% Drop)", ha="center", va="center", fontsize=8.5, fontweight="bold", color="#15803d")
    ax.text(390, 92, "Remains in Medium band (> 0.25 LOW bound)", ha="center", va="center", fontsize=7.5, color="#475569")

    # Arrow from After to Verdict
    ax.annotate("", xy=(440, 170), xytext=(550, 150),
                arrowprops=dict(arrowstyle="-|>", color="#d97706", lw=1.3, ls=":", connectionstyle="arc3,rad=-0.15", mutation_scale=12))

    # 3. AFTER BOX (Right)
    a_rect = patches.FancyBboxPatch((550, 90), 200, 195, boxstyle="round,pad=0,rounding_size=8",
                                    facecolor="#fffbeb", edgecolor="#d97706", linewidth=1.8)
    ax.add_patch(a_rect)
    ax.text(650, 260, "POST-RECOVERY STATE", ha="center", va="center", fontsize=9, fontweight="bold", color="#b45309")
    ax.text(650, 225, "MEDIUM", ha="center", va="center", fontsize=20, fontweight="900", color="#d97706")
    ax.text(650, 185, "Risk Score: 0.447", ha="center", va="center", fontsize=11, fontweight="bold", color="#0f172a")
    ax.text(650, 160, "Label: 0 (Below Threshold)", ha="center", va="center", fontsize=8.5, color="#475569")
    ax.text(650, 135, "Synthetic Normal Proxy Evaluation", ha="center", va="center", fontsize=8, color="#0f172a", fontstyle="italic")
    ax.text(650, 110, "Same LR Model · Zero Retraining", ha="center", va="center", fontsize=7.5, color="#64748b")

    # Footnote
    ax.text(390, 45, "Honest Operational Conservatism: Evaluated against a 10-step simulated telemetry stream. By avoiding a false\n'RECOVERED' claim when residual variance remains, the platform prevents hazardous false confidence.",
            ha="center", va="center", fontsize=7.5, color="#475569", fontstyle="italic",
            bbox=dict(boxstyle="square,pad=0.4", facecolor="#f8fafc", edgecolor="#e2e8f0", lw=0.6))

    save_fig(fig, "fig7_verification")

# ==============================================================================
# FIGURE 5: Temporal Feature Engineering Pipeline (45 Features from 10-Step Window)
# ==============================================================================
def make_fig2_temporal_features():
    fig = plt.figure(figsize=(8.0, 4.0), facecolor="white")
    ax = fig.add_subplot(111)
    ax.set_facecolor("white")
    ax.set_xlim(0, 800)
    ax.set_ylim(0, 400)
    ax.axis("off")

    ax.text(400, 380, "Temporal Feature Engineering Pipeline: 10-Step Sliding Window",
            ha="center", va="center", fontsize=11.5, fontweight="bold", color="#0f172a")

    # Step 1: Raw Metrics Box (Left)
    raw_rect = patches.FancyBboxPatch((20, 100), 160, 240, boxstyle="round,pad=0,rounding_size=6",
                                      facecolor="#eff6ff", edgecolor="#2563eb", linewidth=1.5)
    ax.add_patch(raw_rect)
    ax.text(100, 320, "5 Raw Metrics", ha="center", va="center", fontsize=10, fontweight="bold", color="#1d4ed8")
    ax.text(100, 295, "(Continuous KPIs)", ha="center", va="center", fontsize=8, color="#64748b")
    metrics = ["1. CPU Utilization (%)", "2. Memory Usage (%)", "3. Disk Usage (%)", "4. Net Bytes Sent (MB/s)", "5. Net Bytes Recv (MB/s)"]
    for i, m in enumerate(metrics):
        ax.text(32, 255 - i * 32, m, ha="left", va="center", fontsize=8, fontweight="medium", color="#0f172a")

    # Arrow 1
    kw = dict(arrowstyle="-|>", color="#475569", lw=1.5, mutation_scale=14)
    ax.annotate("", xy=(230, 220), xytext=(180, 220), arrowprops=kw)

    # Step 2: Sliding Window Box (Middle)
    win_rect = patches.FancyBboxPatch((230, 100), 200, 240, boxstyle="round,pad=0,rounding_size=6",
                                      facecolor="#f0fdfa", edgecolor="#0d9488", linewidth=1.5)
    ax.add_patch(win_rect)
    ax.text(330, 320, "10-Step Sliding Window", ha="center", va="center", fontsize=10, fontweight="bold", color="#0f766e")
    ax.text(330, 295, "Trailing FIFO Buffer: [t-9 .. t]", ha="center", va="center", fontsize=8, color="#64748b")
    ax.text(330, 260, "Strict Leak-Free Construction:\nZero future visibility ($t' \\leq t$)", ha="center", va="center", fontsize=8, color="#0f172a")
    
    # Graphic of sliding window slots
    for slot in range(10):
        color = "#0d9488" if slot >= 5 else "#94a3b8"
        s_rect = patches.Rectangle((245 + slot * 17, 180), 14, 30, facecolor=color, edgecolor="#0f172a", lw=0.6)
        ax.add_patch(s_rect)
    ax.text(330, 160, "Short Window (w=5) | Full Window (w=10)", ha="center", va="center", fontsize=7.5, color="#475569")
    ax.text(330, 125, "StandardScaler Normalization\n(Fit exclusively on training split)", ha="center", va="center", fontsize=7.5, color="#64748b", fontstyle="italic")

    # Arrow 2
    ax.annotate("", xy=(480, 220), xytext=(430, 220), arrowprops=kw)

    # Step 3: Derived Temporal Features (Right)
    feat_rect = patches.FancyBboxPatch((480, 70), 300, 270, boxstyle="round,pad=0,rounding_size=6",
                                       facecolor="#faf5ff", edgecolor="#7c3aed", linewidth=1.5)
    ax.add_patch(feat_rect)
    ax.text(630, 320, "45 Derived Temporal Features", ha="center", va="center", fontsize=10, fontweight="bold", color="#6d28d9")
    ax.text(630, 298, "(9 features per metric $\\times$ 5 metrics)", ha="center", va="center", fontsize=8, color="#64748b")
    
    derived = [
        ("Current Value", "$x_t$", "Point-in-time state"),
        ("Rolling Means", "$\\mu_5, \\mu_{10}$", "Local & historical level"),
        ("Rolling Deltas", "$\\Delta_5, \\Delta_{10}$", "Magnitude shift from baseline"),
        ("Rolling Slopes", "$m_5, m_{10}$", "OLS linear trend trajectory"),
        ("Rolling Std Dev", "$\\sigma_5, \\sigma_{10}$", "Incidence of temporal jitter")
    ]
    for i, (fn, math_f, desc) in enumerate(derived):
        y_c = 265 - i * 36
        ax.text(495, y_c, f"• {fn} ({math_f})", fontsize=8.5, fontweight="bold", color="#0f172a")
        ax.text(495, y_c - 12, f"  {desc}", fontsize=7.5, color="#475569")

    # Footnote
    ax.text(400, 30, "Forward-looking label target: y = 1 if failure occurs in [t+1 .. t+10]. Current step t excluded from target to eliminate circularity.",
            ha="center", va="center", fontsize=7.5, color="#475569", fontstyle="italic")

    save_fig(fig, "fig2_temporal_features")

# ==============================================================================
# FIGURE 6: Scenario-Level Predictive Performance Breakdown
# ==============================================================================
def make_fig5_scenario_performance():
    fig, ax = plt.subplots(figsize=(7.5, 3.8), facecolor="white")
    ax.set_facecolor("white")

    scenarios = [
        "CPU Sudden\n(Step Fault)",
        "CPU Gradual\n(Linear Ramp)",
        "Memory Leak\n(Gradual)",
        "Disk Exhaustion\n(Gradual)",
        "Network Degr.\n(Jitter/Loss)",
        "Combined Fail.\n(Multi-Resource)"
    ]
    
    # Values from Table V (Logistic Regression, Seed 42, Test Split)
    prec = [0.529, 0.817, 1.000, 0.952, 0.635, 0.820]
    rec  = [0.529, 0.527, 0.649, 0.791, 0.783, 0.755]
    f1   = [0.529, 0.641, 0.787, 0.864, 0.702, 0.786]

    x = np.arange(len(scenarios))
    width = 0.26

    ax.grid(axis="y", linestyle="--", linewidth=0.7, color="#e2e8f0", zorder=0)

    # Bars
    ax.bar(x - width, prec, width, label="Precision", color="#3b82f6", edgecolor="#0f172a", lw=0.7, zorder=3)
    ax.bar(x, rec, width, label="Recall", color="#0d9488", edgecolor="#0f172a", lw=0.7, zorder=3)
    ax.bar(x + width, f1, width, label="F1-Score", color="#d97706", edgecolor="#0f172a", lw=0.7, zorder=3)

    # Values on F1 bars
    for i in range(len(scenarios)):
        ax.text(x[i] + width, f1[i] + 0.02, f"{f1[i]:.2f}", ha="center", va="bottom",
                fontsize=7.5, fontweight="bold", color="#b45309")

    ax.set_ylabel("Classification Metric", fontsize=10, fontweight="bold")
    ax.set_ylim(0, 1.12)
    ax.set_xticks(x)
    ax.set_xticklabels(scenarios, fontsize=8.5)
    
    legend = ax.legend(loc="upper left", ncol=3, frameon=True, facecolor="white", edgecolor="#cbd5e1")
    legend.get_frame().set_linewidth(0.8)

    # Spines styling
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)
    for s in ["left", "bottom"]:
        ax.spines[s].set_color("#64748b")
        ax.spines[s].set_linewidth(0.8)

    save_fig(fig, "fig5_scenario_performance")

if __name__ == "__main__":
    print("Generating redesigned light, print-friendly figures...")
    make_fig1_architecture()
    make_fig4_model_comparison()
    make_fig6_xai_contributions()
    make_fig7_verification()
    make_fig2_temporal_features()
    make_fig5_scenario_performance()
    print("All figures successfully created.")
