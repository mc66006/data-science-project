# Assignment 01 — Seattle Apartment Rent and Mixed-Income Housing

This folder contains the preliminary CISC7204 proposal, exploratory notebook, course-provided data, a reproducible analysis script, and generated visualizations.

## Research question

Across Seattle census tracts, how are the number of mixed-rate or mixed-income apartments and apartment rent levels associated? How does that tract-level count relate to year-over-year rent growth?

## Data and usage

The rent table is downloaded from Seattle Open Data’s [Apartment Market Rent Prices by Census Tract](https://data.seattle.gov/d/h27p-5k3i) dataset. The companion housing table comes from [Single-Family Home Flips by Census Tract](https://data.seattle.gov/d/e9ve-4v8v). The portal credits CoStar Group data prepared by the City of Seattle Office of Planning and Community Development for the rent indicator and King County Assessor records for the home-flip indicator. The archived CSVs are used for this coursework. The portal is publicly accessible, but its current terms and any third-party restrictions should be checked before external redistribution. The analysis uses aggregate tract observations rather than individual households.

## Methods and findings

The script standardizes column names and numeric types, removes incomplete analysis rows and non-positive rent observations, then summarizes rent over time, by community, and against mixed-income apartment counts. It creates four labeled figures and reports Pearson correlations.

- 4,500 source rows were provided; 3,931 positive-rent observations remain after cleaning, spanning 160 tracts.
- Mean monthly contract rent per unit is approximately **$1,486**; the median is approximately **$1,432**.
- Mixed-income apartment count has a positive cross-sectional association with rent level (**r = 0.4643**) and nearly no linear association with year-over-year rent growth (**r = -0.0136**).
- A quadratic model in the notebook reports R² of **0.454** for a random split and **0.479** for a time-based split. These are exploratory predictive checks, not causal evidence.

The results suggest that the count may co-vary with rent level, but they do not show that mixed-income housing raises rents. Tract size, neighborhood location, property mix, and other omitted factors may explain part of the association.

## Reproduce

Install the repository-level dependencies and run from this directory:

```bash
python -m pip install -r ../requirements.txt
python analyze_seattle_rent.py
```

The script reads `seattle_rent.csv` and recreates the figures in `figures/`. Open `seattle_rent.ipynb` in Jupyter to review the proposal's exploratory notebook. The files remain alongside the script so its relative paths work.
