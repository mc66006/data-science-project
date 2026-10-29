"""Reproduce the College Scorecard cleaning, summary, and project figures."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parent
RAW_FILE = ROOT / "Most-Recent-Cohorts-Institution.csv"
CLEAN_FILE = ROOT / "cleaned_data.csv"
FIGURE_DIR = ROOT / "figures"


def load_clean_data() -> pd.DataFrame:
    columns = [
        "UNITID",
        "INSTNM",
        "PREDDEG",
        "CONTROL",
        "TUITIONFEE_IN",
        "TUITIONFEE_OUT",
        "MD_EARN_WNE_P10",
        "COUNT_WNE_P10",
    ]
    raw = pd.read_csv(RAW_FILE, usecols=columns, low_memory=False)
    raw["MD_EARN_WNE_P10"] = raw["MD_EARN_WNE_P10"].replace("PS", np.nan)
    raw["COUNT_WNE_P10"] = raw["COUNT_WNE_P10"].replace("PS", np.nan)
    for column in columns[4:]:
        raw[column] = pd.to_numeric(raw[column], errors="coerce")

    data = raw.loc[raw["PREDDEG"].eq(3)].copy()
    data = data.dropna(
        subset=[
            "TUITIONFEE_IN",
            "TUITIONFEE_OUT",
            "MD_EARN_WNE_P10",
            "COUNT_WNE_P10",
        ]
    )
    data = data.loc[
        data["TUITIONFEE_IN"].gt(0)
        & data["TUITIONFEE_OUT"].gt(0)
        & data["MD_EARN_WNE_P10"].gt(0)
        & data["COUNT_WNE_P10"].gt(0)
    ].copy()
    data["institution_type"] = data["CONTROL"].map(
        {1: "Public", 2: "Private", 3: "Private"}
    )
    data = data.loc[data["institution_type"].notna()]
    data = data.rename(
        columns={
            "UNITID": "unit_id",
            "INSTNM": "institution_name",
            "TUITIONFEE_IN": "tuition_in",
            "TUITIONFEE_OUT": "tuition_out",
            "MD_EARN_WNE_P10": "earnings_10yr",
            "COUNT_WNE_P10": "earnings_count",
        }
    )
    return data[
        [
            "unit_id",
            "institution_name",
            "tuition_in",
            "tuition_out",
            "earnings_10yr",
            "earnings_count",
            "institution_type",
        ]
    ].reset_index(drop=True)


def make_figures(data: pd.DataFrame) -> None:
    FIGURE_DIR.mkdir(exist_ok=True)
    colors = {"Private": "#b45309", "Public": "#2563eb"}

    fig, ax = plt.subplots(figsize=(9, 6))
    for group in ["Public", "Private"]:
        subset = data.loc[data["institution_type"].eq(group)]
        x = subset["tuition_in"].to_numpy()
        y = subset["earnings_10yr"].to_numpy()
        ax.scatter(x, y, s=18, alpha=0.32, color=colors[group], label=f"{group} (n={len(subset):,})")
        slope, intercept = np.polyfit(x, y, 1)
        trend_x = np.linspace(x.min(), x.max(), 100)
        ax.plot(trend_x, slope * trend_x + intercept, color=colors[group], linewidth=2)
    ax.set_title("Tuition and 10-Year Median Earnings by Institution Type")
    ax.set_xlabel("Annual in-state tuition (US dollars)")
    ax.set_ylabel("Median earnings 10 years after entry (US dollars)")
    ax.legend(frameon=False)
    ax.grid(alpha=0.2)
    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "tuition-earnings-scatter.png", dpi=180)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 5.5))
    groups = ["Public", "Private"]
    values = [data.loc[data["institution_type"].eq(g), "earnings_10yr"] for g in groups]
    ax.boxplot(values, showfliers=False, patch_artist=True,
               boxprops={"facecolor": "#dbeafe", "edgecolor": "#334155"},
               medianprops={"color": "#b45309", "linewidth": 2})
    ax.set_xticks(range(1, len(groups) + 1), groups)
    for pos, group in enumerate(groups, start=1):
        median = data.loc[data["institution_type"].eq(group), "earnings_10yr"].median()
        ax.annotate(f"Median ${median:,.0f}", (pos, median), xytext=(7, 4),
                    textcoords="offset points", fontsize=9)
    ax.set_title("10-Year Median Earnings by Institution Type")
    ax.set_xlabel("Institution type")
    ax.set_ylabel("Median earnings 10 years after entry (US dollars)")
    ax.grid(axis="y", alpha=0.2)
    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "earnings-by-institution-type.png", dpi=180)
    plt.close(fig)

    public = data.loc[data["institution_type"].eq("Public")]
    tuition_categories = [
        public["tuition_in"].rename("Public in-state"),
        public["tuition_out"].rename("Public out-of-state"),
        data.loc[data["institution_type"].eq("Private"), "tuition_in"].rename("Private"),
    ]
    fig, ax = plt.subplots(figsize=(8, 5.5))
    category_labels = [series.name for series in tuition_categories]
    ax.boxplot(tuition_categories, showfliers=False, patch_artist=True,
               boxprops={"facecolor": "#dcfce7", "edgecolor": "#334155"},
               medianprops={"color": "#b45309", "linewidth": 2})
    ax.set_xticks(range(1, len(category_labels) + 1), category_labels)
    ax.set_title("Annual Tuition Distribution by Institution and Residency")
    ax.set_xlabel("Tuition category")
    ax.set_ylabel("Annual tuition (US dollars)")
    ax.grid(axis="y", alpha=0.2)
    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "tuition-distribution.png", dpi=180)
    plt.close(fig)


def main() -> None:
    data = load_clean_data()
    data.to_csv(CLEAN_FILE, index=False)
    make_figures(data)
    summary = data.groupby("institution_type").agg(
        institutions=("unit_id", "count"),
        median_tuition_in=("tuition_in", "median"),
        median_earnings_10yr=("earnings_10yr", "median"),
        mean_tuition_in=("tuition_in", "mean"),
        mean_earnings_10yr=("earnings_10yr", "mean"),
    )
    summary["tuition_earnings_pearson_r"] = data.groupby("institution_type").apply(
        lambda group: group["tuition_in"].corr(group["earnings_10yr"]),
        include_groups=False,
    )
    print(f"Cleaned institutions: {len(data):,}")
    print(summary.round(3).to_string())
    print(f"Figures saved in: {FIGURE_DIR}")


if __name__ == "__main__":
    main()
