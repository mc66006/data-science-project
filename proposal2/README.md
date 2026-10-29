# CISC7204 Assignment 02 — College tuition and earnings proposal

This is the standalone Assignment 02 proposal repository. It contains the proposal, notebook, data, figures, and reproducible analysis formerly stored under the CISC7204 coursework archive.

This folder preserves the Pair 14 revised project proposal and its working data files in the same `personalproposal` layout used for Assignment 01.

## Research question

Is annual undergraduate tuition associated with the median earnings of students who are working and not enrolled 10 years after entering U.S. four-year colleges, and does this relationship differ between public and private institutions?

## Files

- `CISC7204-Assgn02-Pair14-RevisedProjectProposal.docx` — revised proposal, scope, success criteria, task plan, and collaboration plan.
- `CISC7204-Assgn02-Pair14-CollegeTuition-Earnings-Analysis.ipynb` — executable notebook with data selection, cleaning, summary statistics, visualizations, findings, and limitations.
- `Most-Recent-Cohorts-Institution.csv` — unchanged source extract supplied with the proposal archive.
- `cleaned_data.csv` — notebook output after restricting to predominantly four-year institutions and removing missing, suppressed, and invalid analysis values.
- `analyze_college_scorecard.py` — standalone script that recreates the cleaning, summary statistics, and figures.
- `RESULTS.md` — executed findings, limitations, and reproducibility status.
- `figures/` — generated charts used in the Portfolio showcase.

## Data provenance and responsible use

The institution-level CSV extract was downloaded from the U.S. Department of Education [College Scorecard data portal](https://collegescorecard.ed.gov/data/). When checked on 2026-10-29, the portal stated that the data were last updated on 2026-10-15; the exact release date of the archived CSV supplied with this project has not been verified. The analysis uses aggregate institutional measures, including tuition and median earnings ten years after entry, and does not use individual student records. Consult the official source page and its current data-use notice before redistributing the archived extract outside this coursework.

## Reproduce the notebook

Keep the notebook, `Most-Recent-Cohorts-Institution.csv`, and `cleaned_data.csv` in this folder. Install the packages listed in the repository-level [`requirements.txt`](../../requirements.txt), open the notebook in Jupyter, and run the cells from top to bottom. The notebook reads the raw CSV, writes `cleaned_data.csv`, and produces the tuition, regression, radar, and violin visualizations.

The original proposal and notebook are retained, with a findings and limitations discussion added to the notebook. The standalone script and [`RESULTS.md`](RESULTS.md) provide an independently rerunnable analysis and reproducibility record.
# CISC7204 Assignment 02 — College tuition and earnings proposal

This is the standalone Assignment 02 proposal repository. It contains the proposal, notebook, data, figures, and reproducible analysis formerly stored under the CISC7204 coursework archive.

This folder preserves the Pair 14 revised project proposal and its working data files in the same `personalproposal` layout used for Assignment 01.

## Research question

Is annual undergraduate tuition associated with the median earnings of students who are working and not enrolled 10 years after entering U.S. four-year colleges, and does this relationship differ between public and private institutions?

## Files

- `CISC7204-Assgn02-Pair14-RevisedProjectProposal.docx` — revised proposal, scope, success criteria, task plan, and collaboration plan.
- `CISC7204-Assgn02-Pair14-CollegeTuition-Earnings-Analysis.ipynb` — executable notebook with data selection, cleaning, summary statistics, visualizations, findings, and limitations.
- `Most-Recent-Cohorts-Institution.csv` — unchanged source extract supplied with the proposal archive.
- `cleaned_data.csv` — notebook output after restricting to predominantly four-year institutions and removing missing, suppressed, and invalid analysis values.
- `analyze_college_scorecard.py` — standalone script that recreates the cleaning, summary statistics, and figures.
- `RESULTS.md` — executed findings, limitations, and reproducibility status.
- `figures/` — generated charts used in the Portfolio showcase.

## Data provenance and responsible use

The raw file is an extract from the U.S. Department of Education College Scorecard institution-level data. The official data page is <https://collegescorecard.ed.gov/data/>. On 2026-10-29, that page stated that College Scorecard data were last updated on 2026-10-15; the supplied archived CSV's exact release date has not been verified. The analysis uses institution-level aggregate measures, including tuition and median earnings ten years after entry; it does not contain passwords, API keys, or direct individual records. The source's current data-use notice should be checked before redistributing the raw extract outside this coursework archive.

## Reproduce the notebook

Keep the notebook, `Most-Recent-Cohorts-Institution.csv`, and `cleaned_data.csv` in this folder. Install the packages listed in the repository-level [`requirements.txt`](../../requirements.txt), open the notebook in Jupyter, and run the cells from top to bottom. The notebook reads the raw CSV, writes `cleaned_data.csv`, and produces the tuition, regression, radar, and violin visualizations.

The original proposal and notebook are retained, with a findings and limitations discussion added to the notebook. The standalone script and [`RESULTS.md`](RESULTS.md) provide an independently rerunnable analysis and reproducibility record.
