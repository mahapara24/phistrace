"""Draw the three paper figures from data/eval_*.json. Run from the repo root or this folder."""
import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data"
plt.rcParams.update({"font.family": "serif", "font.serif": ["Times New Roman", "DejaVu Serif"], "font.size": 8})

# Fig. 1: pipeline
fig, ax = plt.subplots(figsize=(3.5, 2.35), dpi=300)
ax.set_xlim(0, 10); ax.set_ylim(0, 6.6); ax.axis("off")
def box(x, y, w, h, title, sub, fill="#DBEAFE", edge="#1E40AF"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05,rounding_size=0.15", lw=0.9, ec=edge, fc=fill))
    ax.text(x + w / 2, y + h * 0.66, title, ha="center", va="center", fontsize=7.2, weight="bold")
    ax.text(x + w / 2, y + h * 0.28, sub, ha="center", va="center", fontsize=5.0)
def arrow(x1, y1, x2, y2, label=None):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle="-|>", lw=0.7, color="black"))
    if label:
        ax.text((x1 + x2) / 2 + 0.1, (y1 + y2) / 2, label, fontsize=5.3, ha="left", va="center", style="italic")
box(0.1, 5.2, 2.9, 1.2, "1. Input", "URL text only")
box(3.55, 5.2, 2.9, 1.2, "2. Prepare", "host, domain, suffix")
box(7.0, 5.2, 2.9, 1.2, "3. Detect", "22 weighted rules")
arrow(3.0, 5.8, 3.55, 5.8); arrow(6.45, 5.8, 7.0, 5.8)
box(7.0, 3.2, 2.9, 1.3, "4. Plan path", "light, standard\nor deep path", "#D1FAE5", "#047857")
arrow(8.45, 5.2, 8.45, 4.5, "score")
box(3.55, 3.2, 2.9, 1.3, "5. Tools", "registries +\ntag retrieval", "#D1FAE5", "#047857")
arrow(7.0, 3.85, 6.45, 3.85)
box(0.1, 3.2, 2.9, 1.3, "6. Verify", "keep sentences an\nexhibit tag covers", "#D1FAE5", "#047857")
arrow(3.55, 3.85, 3.0, 3.85)
box(0.1, 1.2, 2.9, 1.3, "7. Report", "verdict, published\nand withheld claims", "#FFEDD5", "#C2410C")
arrow(1.55, 3.2, 1.55, 2.5, "supported only")
box(3.55, 1.2, 6.35, 1.3, "Baselines on the same signal", "Rules only: no retrieval, no verifier\nRetrieval only: one search, no verifier", "#F3F4F6", "#6B7280")
ax.text(5.0, 0.45, "Blue: detection   Green: agentic chain   Orange: report   Gray: baselines", ha="center", fontsize=5.4)
fig.savefig(HERE / "fig1_pipeline.png", bbox_inches="tight", pad_inches=0.02)

# Fig. 2: v1 to v4 on the held-out PhiUSIIL test split
runs = [
    ("v1 (17 rules)", json.loads((DATA / "eval_baseline.json").read_text()), "#F59E0B", "#92400E"),
    ("v2 (20 rules)", json.loads((DATA / "eval_v2.json").read_text()), "#60A5FA", "#1E40AF"),
    ("v3 (22 rules)", json.loads((DATA / "eval_v3.json").read_text()), "#A7F3D0", "#047857"),
    ("v4 (22 rules)", json.loads((DATA / "eval_results.json").read_text()), "#059669", "#064E3B"),
]
names = ["Accuracy", "Precision", "Recall", "F1", "ROC-AUC"]
def vals(t):
    a = t["alert"]
    return [a["accuracy"], a["precision"], a["recall"], a["f1"], t["roc_auc"]]
fig, ax = plt.subplots(figsize=(3.5, 1.95), dpi=300)
w = 0.2
for k, (label, run, fill, edge) in enumerate(runs):
    xs = [x + (k - 1.5) * w for x in range(len(names))]
    bars = ax.bar(xs, vals(run["phiusiil"]["test"]), w, label=label, color=fill, ec=edge, lw=0.5)
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.012, f"{bar.get_height():.2f}", ha="center", fontsize=3.4, rotation=90, va="bottom")
ax.set_xticks(range(len(names))); ax.set_xticklabels(names, fontsize=6.5); ax.set_ylim(0, 1.22); ax.set_ylabel("Score")
ax.spines[["top", "right"]].set_visible(False); ax.legend(frameon=False, fontsize=5.4, ncol=4, loc="upper center", bbox_to_anchor=(0.5, 1.16))
fig.savefig(HERE / "fig2_v1_v2.png", bbox_inches="tight", pad_inches=0.02)

# Fig. 3: real-world feeds, v2, v3, v4 (alert point). Recall on malicious feeds, false alarms on Tranco.
v2 = runs[1][1]["external"]; v3 = runs[2][1]["external"]; v4 = runs[3][1]["external"]
groups = [("OpenPhish\nrecall", "openphish", "alert_recall"), ("Phishing.DB\nrecall", "phishing_database", "alert_recall"),
          ("URLhaus\nrecall", "urlhaus", "alert_recall"), ("Tranco top-100k\nfalse alarms", "tranco", "alert_fpr")]
fig, ax = plt.subplots(figsize=(3.5, 1.95), dpi=300)
w = 0.27
for k, (label, ext, fill, edge) in enumerate([("v2", v2, "#60A5FA", "#1E40AF"), ("v3", v3, "#A7F3D0", "#047857"), ("v4", v4, "#059669", "#064E3B")]):
    xs = [x + (k - 1) * w for x in range(len(groups))]
    ys = [ext[key][field] * 100 for _, key, field in groups]
    bars = ax.bar(xs, ys, w, label=label, color=fill, ec=edge, lw=0.5)
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1.2, f"{bar.get_height():.1f}", ha="center", fontsize=3.8)
ax.axvspan(2.5, 3.5, color="#FEE2E2", zorder=0)
ax.set_xticks(range(len(groups))); ax.set_xticklabels([g[0] for g in groups], fontsize=5.6); ax.set_ylim(0, 112); ax.set_ylabel("Percent")
ax.spines[["top", "right"]].set_visible(False); ax.legend(frameon=False, fontsize=6, ncol=3, loc="upper center", bbox_to_anchor=(0.5, 1.14))
fig.savefig(HERE / "fig3_realworld.png", bbox_inches="tight", pad_inches=0.02)
print("figures written")
