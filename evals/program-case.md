# Northstar: a certification owner's real workflow

The problem is realistic; all organizations, people, documentation and results are synthetic. A partner enablement lead has six weeks, limited reviewer time, an existing LMS, and no exam. Course completion does not demonstrate safe implementation. The deliverable must support a bounded competence claim and remain useful when the product changes after a pilot.

Phase 1 begins with a business request, conflicting discovery notes and three source guides. It requires twelve actual items including performance tasks in each domain, a reasoned blueprint, study follow-up, review materials and candidate guidance. Phase 2 starts a **fresh agent** with saved outputs, a pinned synthetic pilot form, 24 scored attempts including one incomplete attempt, three sets of panel judgments, and a changed access model. The owner needs historical analysis, revised content and a release recommendation. The expected answer is not just “blocked”: complete the analysis, revisions and concrete next decisions.

## Execute

From the package root:

```powershell
python evals/program.py prepare --run C:/path/to/new-run --phase 1
```

Give only the returned `prompt.txt` to a fresh assistant with file and Python access. The supplied skills are copied into its workspace. Allow it to read the inputs and write result/. Do not expose graders, expected values or previous conclusions. No network, accounts, API keys or new services are needed. Filesystem isolation here is an instruction boundary, not an OS sandbox.

```powershell
python evals/program.py grade --run C:/path/to/new-run --phase 1
python evals/program.py review --run C:/path/to/new-run --phase 1 --review-file C:/path/to/review.json
python evals/program.py prepare --run C:/path/to/new-run --phase 2
```

Repeat the fresh-agent, grade and review steps for phase 2. Review JSON must identify `reviewer`, `reviewer_type` (model/human), `accepted` and `findings` containing concrete artifact evidence for `source_correctness`, `owner_usefulness`, `measurement_judgment`, `privacy`, and `continuity`. Review the actual files, not the final assistant message. Use [the rubric](review-rubric.md).

Preparation records input, skill and grader hashes. Grades and reviews are write-once, bind output hashes, and preserve a snapshot. Phase 2 requires an accepted phase 1 and the same skills. Stop on a material failure, retain the run, correct the responsible skill/fixture/grader, and rerun in a new directory. Never edit evaluated artifacts to turn a failure into a pass. An assisted follow-up must be separately reported.

## What the scores mean

Mechanical checks cover record integrity, source portability, draft boundaries, public-bank leakage, raw input preservation, exact historical analysis and revised-item status. They do not judge whether tasks, distractors, rubrics or conclusions are substantively sound. A deliberately shallow fixture can pass these checks; a negative-control test demonstrates that limitation. Artifact review is mandatory and model review is not human acceptance.

Phase 2's provider/panel evidence is generated from the actual first-phase bank so score columns and form fingerprints match. This is an authored simulation, not an administered pilot or independent psychometric evidence. Numeric expected results use the same already-regression-tested helper; this grade tests that the agent selected the correct form and exclusions, not an independent calculation oracle.

After phase 2, copy/archive the whole result to a different location, compare hashes, validate there, resolve all local source references and rerun the historical analysis. Record that restore separately. This case covers creation, review preparation, pilot interpretation and maintenance. Existing offline scenarios cover issuance reconciliation; this case does not claim provider integration, native-host discovery or actual credential acceptance.
