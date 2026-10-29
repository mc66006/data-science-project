# Assignment 02 results — College Tuition and Graduate Earnings

## Research question

Is annual undergraduate tuition associated with the median earnings of students who are working and not enrolled 10 years after entering U.S. four-year colleges, and does this relationship differ between public and private institutions?

## Data and method

The analysis uses the College Scorecard institution-level extract supplied in the project archive. It keeps institutions whose predominant degree is bachelor's degree (`PREDDEG == 3`), converts the suppressed `PS` earnings values to missing, removes missing or non-positive tuition and earnings values, and maps control code 1 to Public and codes 2 or 3 to Private. The Private category combines for-profit and nonprofit institutions. The final table contains 1,731 institutions: 566 public and 1,165 private.

The main tuition variable is annual in-state tuition. Public out-of-state tuition is used only for the tuition-distribution comparison. The analysis reports unweighted medians, means, and Pearson correlations within institution type. The script also creates a scatter plot with group trend lines, an earnings box plot, and a tuition-distribution box plot.

Run from this directory:

```bash
python analyze_college_scorecard.py
```

The script rewrites `cleaned_data.csv` and saves figures in `figures/`.

## Findings

| Institution type | Institutions | Median in-state tuition | Median 10-year earnings | Tuition/earnings Pearson r |
|---|---:|---:|---:|---:|
| Public | 566 | $10,330 | $59,272 | 0.523 |
| Private | 1,165 | $35,760 | $58,029 | 0.644 |

In this filtered institution-level sample, tuition and 10-year median earnings have a positive association in both groups. The association is stronger for private institutions in this descriptive comparison. Median earnings are similar across the two groups despite the much higher median private tuition. The results answer the exploratory question for this dataset, but they do not show that tuition causes later earnings.

## Limitations

- The data are institution-level aggregates, so they cannot describe individual students or establish an individual return on tuition.
- The tuition measure and the earnings outcome can represent different cohorts and does not adjust for inflation, field of study, geography, student preparation, selectivity, financial aid, or living costs.
- The analysis uses predominantly four-year institutions with usable reported values; excluded institutions and suppressed values may make the sample less representative.
- The combined Private category includes both nonprofit and for-profit institutions, which can have different missions and student outcomes.
- Public in-state tuition is a baseline rather than the price paid by every student. Private tuition, net price, debt, and aid are also not interchangeable.
- Pearson correlations and fitted trend lines summarize association and can be affected by outliers and confounding variables. A causal claim would require a stronger design and additional covariates.

## Reproducibility status

The proposal, raw extract, cleaned data, notebook, executable script, results, and generated figures are stored together in this folder. The original proposal and notebook are retained; the notebook now includes a findings and limitations discussion, while the script and this report provide independent reproduction and presentation-ready figures.
