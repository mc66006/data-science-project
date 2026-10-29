"""Recreate the main figures and summary tables for the Seattle rent study.

The script mirrors the transformations in ``seattle_rent.ipynb`` while keeping
the raw course-provided CSV unchanged. Run it from this directory or pass no
arguments; all outputs are written to ``figures/``.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "seattle_rent.csv"
FIGURES = ROOT / "figures"
FIGURES.mkdir(exist_ok=True)

sns.set_theme(style="whitegrid", context="notebook")


def load_data() -> pd.DataFrame:
    raw = pd.read_csv(DATA)
    df = raw.rename(
        columns={
            "Tract Median Apartment Contract Rent per Square Foot": "rent_per_sqft",
            "Tract Median Apartment Contract Rent per Unit": "rent_per_unit",
            "Year over Year Change in Rent per Unit": "yoy_change_unit",
            "Mixed-Rate or Mixed-Income Apartment in Tract": "mixed_income_count",
            "PROPERTIES": "property_count",
            "Community Reporting Area Name": "community",
        }
    ).copy()
    numeric = [
        "Year",
        "rent_per_sqft",
        "rent_per_unit",
        "yoy_change_unit",
        "mixed_income_count",
        "property_count",
    ]
    for column in numeric:
        df[column] = pd.to_numeric(df[column], errors="coerce")
    df = df.dropna(subset=numeric + ["GEOID", "community"])
    return df.loc[df["rent_per_unit"] > 0].copy()


def save_figures(df: pd.DataFrame) -> None:
    yearly = (
        df.groupby("Year", as_index=False)
        .agg(mean_rent=("rent_per_unit", "mean"), median_rent=("rent_per_unit", "median"))
    )
    yearly["rolling_mean"] = yearly["mean_rent"].rolling(3, min_periods=1).mean()
    plt.figure(figsize=(10, 5.5))
    plt.plot(yearly["Year"], yearly["mean_rent"], marker="o", linewidth=1.5, alpha=0.65, label="Mean rent")
    plt.plot(yearly["Year"], yearly["rolling_mean"], linewidth=3, label="Three-year rolling mean")
    plt.plot(yearly["Year"], yearly["median_rent"], linestyle="--", linewidth=1.5, label="Median rent")
    plt.title("Seattle tract-level apartment rent, 2001–2025")
    plt.xlabel("Year")
    plt.ylabel("Median contract rent per unit (USD/month)")
    plt.legend(frameon=True)
    plt.tight_layout()
    plt.savefig(FIGURES / "rent-trend.png", dpi=180, bbox_inches="tight")
    plt.close()

    corr = df["mixed_income_count"].corr(df["rent_per_unit"])
    plt.figure(figsize=(8.5, 6))
    sns.regplot(
        data=df,
        x="mixed_income_count",
        y="rent_per_unit",
        scatter_kws={"alpha": 0.22, "s": 20, "color": "#2563eb"},
        line_kws={"color": "#dc2626", "linewidth": 2},
    )
    plt.title("Mixed-income apartments and median rent")
    plt.xlabel("Mixed-income apartments in tract")
    plt.ylabel("Median contract rent per unit (USD/month)")
    plt.annotate(f"Pearson r = {corr:.3f}", xy=(0.03, 0.94), xycoords="axes fraction", fontsize=11)
    plt.tight_layout()
    plt.savefig(FIGURES / "mixed-income-rent.png", dpi=180, bbox_inches="tight")
    plt.close()

    top = (
        df.groupby("community", as_index=False)
        .agg(mean_rent=("rent_per_unit", "mean"), observations=("rent_per_unit", "size"))
        .sort_values("mean_rent", ascending=False)
        .head(8)
        .sort_values("mean_rent")
    )
    plt.figure(figsize=(10, 5.5))
    ax = sns.barplot(data=top, x="mean_rent", y="community", color="#0f766e")
    ax.set_title("Eight Seattle communities with the highest mean rent")
    ax.set_xlabel("Mean median contract rent per unit (USD/month)")
    ax.set_ylabel("")
    for i, row in enumerate(top.itertuples()):
        ax.text(row.mean_rent + 15, i, f"n={row.observations}", va="center", fontsize=9)
    plt.tight_layout()
    plt.savefig(FIGURES / "community-rent.png", dpi=180, bbox_inches="tight")
    plt.close()

    heatmap = df[["rent_per_unit", "rent_per_sqft", "yoy_change_unit", "mixed_income_count", "property_count"]].corr()
    plt.figure(figsize=(8, 6.5))
    sns.heatmap(heatmap, annot=True, fmt=".2f", cmap="vlag", center=0, square=True)
    plt.title("Correlation structure of the analysis variables")
    plt.tight_layout()
    plt.savefig(FIGURES / "correlation-heatmap.png", dpi=180, bbox_inches="tight")
    plt.close()


def main() -> None:
    df = load_data()
    save_figures(df)
    print(f"Rows used: {len(df):,}")
    print(f"Years: {int(df['Year'].min())}–{int(df['Year'].max())}")
    print(f"Tracts: {df['GEOID'].nunique():,}")
    print(f"Rent/mixed-income correlation: {df['rent_per_unit'].corr(df['mixed_income_count']):.4f}")
    print(f"Rent-growth/mixed-income correlation: {df['yoy_change_unit'].corr(df['mixed_income_count']):.4f}")
    print(f"Figures written to {FIGURES}")


if __name__ == "__main__":
    main()
