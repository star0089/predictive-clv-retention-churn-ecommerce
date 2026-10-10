# Repository audit and validation

## Baseline: 10 October 2026

Inspected the complete tracked tree, full README and available history at commit `cff47c7c5bc2dc6a9534e20a28034a8d91bfd0af`. The repository contained exactly one tracked file, README.md, and one initialization commit. There were no notebooks, scripts, SQL, datasets, figures, dependencies, tests or workflows.

### Strengths
The README has a clear customer analytics direction, useful customer-identity reasoning, reported exploratory counts and awareness of cardinality, censoring and leakage.

### Critical weaknesses
Reported results lack executable evidence. The stack mixes aspirations with demonstrated work. Setup, source acquisition and navigation are absent. Exact filters, analysis boundaries, review tie-breaking and follow-up horizons are unspecified.

### Risks
A recruiter may mistake planned models for implemented work. Repeat rates can be biased by unequal follow-up. Many-to-many joins can multiply observations. Review timing may leak future information. Revenue cannot establish profit without costs.

## Prioritized plan

1. Clarify evidence status and preserve reported metrics with qualifications — implemented in this documentation change.
2. Add source acquisition, limitations, methodology and meaningful navigation — implemented.
3. Commit the existing exploratory notebook and reproduce reported counts — next; not implemented.
4. Implement the review-versus-repeat analysis with a fixed observation horizon and validated joins — planned.
5. Extract reusable code and add targeted tests when executable logic is available — planned.

No empty notebooks, model modules, dashboards, CI workflows or artificial results were added. No analytical calculation or existing history was rewritten. A license was not selected on the owner's behalf; dataset rights are separate.

## Recruiter-readiness assessment

Scores are subjective, evidence-based assessments on a 0–10 scale. “After” assesses the proposed documentation branch, not the unfinished analysis.

| Area | Before | After | Evidence |
| --- | ---: | ---: | --- |
| First impression | 4 | 7 | Clear scope, status and navigation |
| Business understanding | 6 | 7 | Definitions and cost-data boundaries |
| Technical clarity | 3 | 5 | Grain and join specifications; no code |
| Data science rigor | 4 | 5 | Explicit censoring/leakage concerns; not executed |
| Code quality | 0 | 0 | No code available to assess |
| Documentation | 4 | 8 | Setup, methodology and limitations |
| Reproducibility | 1 | 2 | Acquisition instructions; no runnable analysis |
| Project originality | 4 | 4 | Familiar dataset with a customer-value framing |
| Analytical communication | 5 | 7 | Reported evidence separated from plans |
| Portfolio readiness | 2 | 4 | Honest foundation; substantive artifacts still missing |

The most valuable shortlist improvements are a runnable notebook, reconciled customer metrics, a well-defined review/retention result, a genuine chart with business interpretation, and reproducible dependencies. A polished README alone does not demonstrate Python, SQL or modeling competence.

## Validation report

- Full baseline file tree and available commit history inspected.
- Original reported values and strict greater-than-seven-day definition retained.
- Rounded rates checked: 2,997 / 96,096 = approximately 3.12%; 1,900 / 96,096 = approximately 1.98%.
- All relative Markdown navigation links checked against the proposed tree.
- Repository clone command successfully executed; no unsupported install or analysis commands introduced.
- No dependencies, Python version, model scores or charts invented.
- External profile and dataset URLs are provided as destinations; their contents and dataset licensing were not independently audited.
- No runtime tests run: the repository has no executable analytical logic.

## Next milestones

First upload the actual exploratory notebook and verify its outputs from local source files. Then complete the first-order review comparison, build the customer master and proceed to cohort retention. Define churn and modeling only after the observation windows and eligible population are clear.
