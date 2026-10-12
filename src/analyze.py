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
    score = np.clip(base + tutoring * 5.2 + rng.normal(0, 4.2, n), 40, 99)
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


def main() -> None:
    DATA_DIR.mkdir(exist_ok=True)
    FIGURES_DIR.mkdir(exist_ok=True)
    data = make_data()
    data.to_csv(DATA_DIR / "study_hours_simulated.csv", index=False)
    make_scatterplot(data)
    make_boxplot(data)
    print(f"Saved {len(data)} synthetic records and two figures under {ROOT}")


if __name__ == "__main__":
    main()
