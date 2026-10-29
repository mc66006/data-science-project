from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
FIGURES_DIR = ROOT / "figures"
RANDOM_SEED = 202607


def make_data(n: int = 120) -> pd.DataFrame:
    """Generate a reproducible, explicitly synthetic student example."""
    rng = np.random.default_rng(RANDOM_SEED)
    hours = rng.uniform(2, 30, n)
    tutoring = rng.random(n) < 0.36

    # A deliberately chosen pattern: larger gains up to 15 hours, then smaller gains.
    base = 58 + 2.35 * np.minimum(hours, 15) + 0.72 * np.maximum(hours - 15, 0)
    score = np.clip(base + tutoring * 5.2 + rng.normal(0, 4.2, n), 40, 100)
    return pd.DataFrame(
        {
            "study_hours_per_week": hours.round(2),
            "tutoring": np.where(tutoring, "Yes", "No"),
            "final_score": score.round(1),
        }
    )


def make_scatterplot(data: pd.DataFrame) -> None:
    colors = {"No": "#0072B2", "Yes": "#D55E00"}
    markers = {"No": "o", "Yes": "^"}
    fig, ax = plt.subplots(figsize=(10.5, 6.5), dpi=180)
    fig.patch.set_facecolor("#FBFCFD")
    ax.set_facecolor("#FBFCFD")
    ax.axvspan(10, 15, color="#E7F2F8", zorder=0)
    ax.text(12.5, 97.6, "10-15 hour zone", ha="center", color="#0072B2", weight="bold")

    for status in ["No", "Yes"]:
        group = data[data["tutoring"] == status]
        ax.scatter(
            group["study_hours_per_week"], group["final_score"],
            s=43, alpha=0.7, color=colors[status], marker=markers[status],
            edgecolor="white", linewidth=0.5, label=f"Tutoring: {status}", zorder=3,
        )

    x = np.linspace(2, 30, 250)
    base = 58 + 2.35 * np.minimum(x, 15) + 0.72 * np.maximum(x - 15, 0)
    ax.plot(x, np.minimum(base, 97.8), color=colors["No"], lw=2.7, label="Simulated pattern: no tutoring")
    ax.plot(x, np.minimum(base + 5.2, 99.2), color=colors["Yes"], lw=2.7, label="Simulated pattern: tutoring")
    ax.axvline(15, color="#34495E", lw=1, ls="--")
    ax.annotate("The simulated score increase slows after 15 hours",
                xy=(15, 91), xytext=(17, 85),
                arrowprops={"arrowstyle": "->", "color": "#34495E"}, fontsize=9)
    ax.set(title="Study time and final score (simulated students)",
           xlabel="Focused study time per week (hours)", ylabel="Final course score (0-100)")
    ax.set_xlim(0, 32); ax.set_ylim(40, 100)
    ax.grid(axis="y", color="#D9E2E8", linewidth=0.8)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(frameon=False, fontsize=8, loc="lower right")
    fig.text(0.01, 0.01, "Synthetic illustration only; association is not evidence of a causal effect.", color="#5C6B73", fontsize=8)
    fig.tight_layout(rect=[0, 0.04, 1, 1])
    fig.savefig(FIGURES_DIR / "study-hours-vs-score.png", bbox_inches="tight")
    plt.close(fig)


def make_boxplot(data: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(8.5, 5.5), dpi=180)
    fig.patch.set_facecolor("#FBFCFD"); ax.set_facecolor("#FBFCFD")
    values = [data.loc[data["tutoring"] == s, "final_score"] for s in ["No", "Yes"]]
    box = ax.boxplot(values, patch_artist=True, labels=["No tutoring", "Tutoring"], widths=0.5)
    for patch, color in zip(box["boxes"], ["#0072B2", "#D55E00"]):
        patch.set_facecolor(color); patch.set_alpha(0.65); patch.set_linewidth(1.2)
    for median in box["medians"]:
        median.set_color("#243447"); median.set_linewidth(2)
    ax.set(title="Score distributions by tutoring status (simulated)",
           xlabel="Group", ylabel="Final course score (0-100)")
    ax.set_ylim(40, 100); ax.grid(axis="y", color="#D9E2E8", linewidth=0.8)
    ax.spines[["top", "right"]].set_visible(False)
    fig.text(0.01, 0.01, "The group difference is part of the synthetic data design, not a causal estimate.", color="#5C6B73", fontsize=8)
    fig.tight_layout(rect=[0, 0.04, 1, 1])
    fig.savefig(FIGURES_DIR / "score-distribution-by-tutoring.png", bbox_inches="tight")
    plt.close(fig)


def make_binned_comparison(data: pd.DataFrame) -> None:
    """Diagnose the score ceiling among students studying at least 15 hours/week."""
    bins = [15, 20, 25, 30.01]
    labels = ["15-20", "20-25", "25-30"]
    data = data[data["study_hours_per_week"] >= 15].copy()
    data["study_band"] = pd.cut(data["study_hours_per_week"], bins=bins, labels=labels, right=False)
    grouped = data.groupby(["study_band", "tutoring"], observed=False)["final_score"].agg(["mean", "count", "std"])
    grouped["se"] = grouped["std"].fillna(0) / np.sqrt(grouped["count"].clip(lower=1))
    grouped["at_ceiling"] = data.assign(at_ceiling=data["final_score"] >= 100).groupby(
        ["study_band", "tutoring"], observed=False
    )["at_ceiling"].mean() * 100

    fig, (ax, ax2) = plt.subplots(2, 1, figsize=(9.5, 7.2), dpi=180, sharex=True,
                                  gridspec_kw={"height_ratios": [2, 1]})
    fig.patch.set_facecolor("#FBFCFD")
    for panel in (ax, ax2): panel.set_facecolor("#FBFCFD")
    colors = {"No": "#0072B2", "Yes": "#D55E00"}
    offsets = {"No": -0.12, "Yes": 0.12}
    x = np.arange(len(labels))
    for status in ["No", "Yes"]:
        g = grouped.xs(status, level="tutoring").reindex(labels)
        ax.errorbar(x + offsets[status], g["mean"], yerr=1.96 * g["se"],
                    fmt="o-", lw=2.2, capsize=4, color=colors[status],
                    label=f"Tutoring: {status}")
        ax2.plot(x + offsets[status], g["at_ceiling"], "o-", lw=2.0,
                 color=colors[status])
        for xi, mean, count in zip(x + offsets[status], g["mean"], g["count"]):
            if count > 0:
                ax.annotate(f"n={int(count)}", (xi, mean), xytext=(0, 10),
                            textcoords="offset points", ha="center", fontsize=7, color=colors[status])
    ax.set_ylabel("Mean score (zoomed 85-100 axis)")
    ax.set_ylim(85, 101)
    ax.set_title("High-hour scores: inspect the mean and the 100-point ceiling")
    ax.grid(axis="y", color="#D9E2E8", linewidth=0.8)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(frameon=False, ncol=2, loc="lower right")
    ax2.set_xticks(x, labels)
    ax2.set_xlabel("Focused study-time band (hours/week)")
    ax2.set_ylabel("At 100 (%)")
    ax2.set_ylim(-5, 105)
    ax2.grid(axis="y", color="#D9E2E8", linewidth=0.8)
    ax2.spines[["top", "right"]].set_visible(False)
    fig.text(0.01, 0.01, "Top: group means with descriptive 95% CIs; the y-axis is deliberately zoomed. Bottom: share at the 100-point cap. Synthetic sample; small bins are labeled with n.", color="#5C6B73", fontsize=7.5)
    fig.tight_layout(rect=[0, 0.04, 1, 1])
    fig.savefig(FIGURES_DIR / "binned-score-comparison.png", bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    DATA_DIR.mkdir(exist_ok=True)
    FIGURES_DIR.mkdir(exist_ok=True)
    data = make_data()
    data.to_csv(DATA_DIR / "study_hours_simulated.csv", index=False)
    make_scatterplot(data)
    make_boxplot(data)
    make_binned_comparison(data)
    print(f"Saved {len(data)} synthetic records and three figures under {ROOT}")


if __name__ == "__main__":
    main()
