# Assignment 01 — Seattle Apartment Rent and Mixed-Income Housing

This folder contains the preliminary CISC7204 proposal, exploratory notebook, course-provided data, a reproducible analysis script, and generated visualizations.

## Research question

Across Seattle census tracts, how are the number of mixed-rate or mixed-income apartments and apartment rent levels associated? How does that tract-level count relate to year-over-year rent growth?

## Data and usage

The notebook and CSV files were supplied with the course materials. The rent data include tract-level observations from 2001–2025. The archive does not identify the original publisher or state the raw files' redistribution terms. Those details must be verified before reusing or redistributing the raw data outside this coursework. The analysis uses aggregate tract observations rather than individual households.

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
