# Data Science Project Materials

This repository contains the source files and reproducible analyses behind three projects shown on the companion [Data Science Portfolio website](https://mc66006.github.io/data-science-portfolio/).

| Folder | Project question | Status | Main materials |
|---|---|---|---|
| [`proposal1/`](proposal1/) | How are mixed-income apartment counts associated with Seattle tract-level rents? | Proposal and exploratory analysis | Proposal, notebook, course-provided CSVs, analysis script, four figures |
| [`proposal2/`](proposal2/) | How are undergraduate tuition and ten-year earnings associated across four-year institutions? | Proposal and exploratory analysis | Proposal, notebook, College Scorecard extract, cleaning script, results, figures |
| [`learning-time-and-outcomes/`](learning-time-and-outcomes/) | In a simulated sample, how do study time and tutoring relate to scores? | Completed simulation demonstration | Reproducible generator, synthetic CSV, three figures |

## Reproduce the analyses

Use Python 3.10 or later. From the repository root, install the shared dependencies:

```bash
python -m pip install -r requirements.txt
```

Run a specific project from its folder so its relative input and output paths work:

```bash
cd proposal1
python analyze_seattle_rent.py
```

```bash
cd proposal2
python analyze_college_scorecard.py
```

```bash
cd learning-time-and-outcomes
python src/analyze.py
```

Proposal 1 uses Seattle Open Data rent and housing tables. The portal credits CoStar Group data prepared by the City of Seattle for the rent indicator and King County Assessor records for the home-flip indicator; redistribution terms and any third-party restrictions should be checked before reuse. Proposal 2 uses a College Scorecard institution-level extract downloaded from the U.S. Department of Education data portal. Learning Time uses synthetic data generated in the repository and contains no real student records.
