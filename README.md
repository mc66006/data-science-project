# Data Science Project Materials

This repository contains the source files and reproducible analyses behind three projects shown on the companion [Data Science Portfolio website](https://mc66006.github.io/data-science-portfolio/).

| Folder | Project question | Status | Main materials |
|---|---|---|---|
| [`assignment1-proposal/`](assignment1-proposal/) | How are mixed-income apartment counts associated with Seattle tract-level rents? | Proposal and exploratory analysis | Proposal, notebook, downloaded source CSVs, four notebook-output figures |
| [`assignment2-proposal/`](assignment2-proposal/) | How are undergraduate tuition and ten-year earnings associated across four-year institutions? | Proposal and exploratory analysis | Proposal, notebook, College Scorecard extract, results, notebook-output figures |
| [`learning-time-and-outcomes/`](learning-time-and-outcomes/) | In a simulated sample, how do study time and tutoring relate to scores? | Completed simulation demonstration | Reproducible generator, synthetic CSV, three figures |

## Reproduce the analyses

Use Python 3.10 or later. From the repository root, install the shared dependencies:

```bash
python -m pip install -r requirements.txt
```

For the two proposal analyses, open each notebook in Jupyter and run its cells from top to bottom:

- **assignment1-proposal/seattle_rent.ipynb**
- **assignment2-proposal/CISC7204-Assgn02-Pair14-CollegeTuition-Earnings-Analysis.ipynb**

The Learning Time simulation remains reproducible from its folder:

```bash
cd learning-time-and-outcomes
python src/analyze.py
```

Proposal 1 uses Seattle Open Data rent and housing tables. The portal credits CoStar Group data prepared by the City of Seattle for the rent indicator and King County Assessor records for the home-flip indicator; redistribution terms and any third-party restrictions should be checked before reuse. Proposal 2 uses a College Scorecard institution-level extract downloaded from the U.S. Department of Education data portal. Learning Time uses synthetic data generated in the repository and contains no real student records.
## Methods, findings, and limitations

Each project folder documents its research question, data provenance and usage note, methods, findings, limitations, analysis materials, and reproduction instructions. Proposal 1 and Proposal 2 use Jupyter notebooks; Learning Time retains its simulation generator and fixed-seed synthetic dataset. Proposal 1 is an aggregate, observational Seattle analysis, so its associations do not establish causal housing effects. Proposal 2 uses institution-level College Scorecard measures; cohort, inflation, aid, selectivity, field, geography, debt, and living costs remain potential confounders. Learning Time patterns cannot be generalized to real students. The shared requirements.txt file lists the Python and Jupyter dependencies. No passwords, API keys, personal records, or restricted datasets are included.

