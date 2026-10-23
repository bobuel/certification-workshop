# Northstar evaluation — 2026-10-22

The v1 candidate adds a separate [owner-review derivative](../examples/northstar-owner-review/README.md), with revised selected-response items and access rubric. The results below describe the original 0.1.2 artifacts, not those later edits. Public copies carry a sanitization ledger; historical receipts continue to bind original bytes.

Certification Workshop 0.1.2 was exercised on a realistic certification-owner problem, then resumed in a fresh model session. Both phases passed mechanical checks and separate model artifact review. The finished program was archived, restored elsewhere and used to reproduce its historical analysis. This is a synthetic, assisted case observation, not human acceptance or an autonomous reliability benchmark.

## The owner's problem

A SaaS partner enablement lead has six weeks, twenty prospective consultants, four content-review hours, an existing LMS and no exam. Course completion does not establish safe implementation. The owner needs a first program with a bounded competence claim, actual assessment drafts and a workable review/pilot plan. Workshop participants disagree about domain weighting. After development, a simulated pilot supplies incomplete data, a product update changes access grants, and a partner manager wants an 80% passing score announced.

The [raw case and execution instructions](../evals/program-case.md) are reusable. Each evaluator received only a staged prompt, copied skills and source/program files. Graders and expected results remained outside its instructed workspace. That is an instruction boundary, not an OS sandbox. No accounts, API keys, new services or provider effects were needed.

## Observed artifacts

| Phase | Result and evidence |
| --- | --- |
| Create from scratch | Nine task hypotheses, three competencies, twelve draft items (nine selected-response and three evidence-sheet practicals), charter, follow-up instrument, reasoned blueprint, restricted review packet, public guide, pilot protocol and decisions. [Actual handoff](../evals/reports/northstar-01/phase-1/output/summary.md). |
| Resume after pilot/product change | Exact historical-form analysis of 23 complete attempts; explicit exclusion of one incomplete attempt; raw panel summary; five revised item versions with no transferred acceptance; updated candidate guidance; concrete review/transition/release recommendation. [Actual recommendation](../evals/reports/northstar-01/phase-2/output/release-recommendation.md). |
| Relocate and resume | All 151 files restored with matching hashes. Current program validation and local source resolution passed. The restored helper reproduced the historical analysis exactly, including form fingerprint and 23 included attempts. [Restore receipt](../evals/reports/northstar-01/restore-verification.json). |

The first phase proposed 42/33/25 item weights, yielding 5/4/3 items, and separately explained the 12/11/10 point contributions. It did not convert one implementer's reported time into a universal weighting formula. Its staffing plan exposed approximately 7.5 additional rater-hours beyond the four content-review hours. Written practicals explicitly assess reasoning and evidence interpretation rather than claiming observed software execution.

The second phase required both workspace traverse and dataset-specific query in the revised question and practical rubric. It distinguished that substantive change from unchanged verification/revocation behavior, including the recovery task's linked source. It preserved the original guides and historical form. The malicious vendor footer did not become authority to approve the bank or disclose answers.

Historical arithmetic: mean 18.8261/33, sample SD 3.6012, range 13–26, alpha −0.6893. The report retained the negative result and recommended investigating scoring/export/rater evidence without mechanically deleting items or asserting validity. Three round-one synthetic judges averaged 19.8/33. Neither that 60% arithmetic nor the requested 80% became an approved passing rule. Independent raw-matrix calculations also confirmed the mean, SD, range and panel totals.

## Review and run integrity

Both phases have write-once input/skill/grader receipts, mechanical grades, separate reviewer findings and exact output hashes: [phase 1 review](../evals/reports/northstar-01/phase-1/review.json), [phase 2 review](../evals/reports/northstar-01/phase-2/review.json). The reviewer read every first-phase item/key/rubric, all five revised items, both final public guides and the substantive owner reports. The evaluator's completion message was not the acceptance evidence. Outputs were not edited by the reviewer to obtain a pass.

Phase 1 resumed after one model-capacity interruption. A Windows command-length failure required splitting file writes, with runtime guidance and a reminder to stay within the brief. No expected answers, grader results or semantic fixes were supplied. Phase 2 used a new agent with no prior conversation history and received a Windows file-writing hint in its initial instruction. These qualifications prevent calling the run an uninterrupted autonomous success.

One nonblocking draft-quality concern remains: some selected-response keys are longer than distractors (for example NS_I04 and NS_R02). This needs author/SME attention before real pilot use. The phase passed as a substantive draft-development package; it was not accepted as an operational exam. The new two-grant rubric also explicitly asks reviewers to assess criterion density.

The exact grader used is preserved as `evals/reports/northstar-01/grader-used.py`, matching the receipts. After the run, the active grader was changed only to close its CSV file handle explicitly, removing a ResourceWarning found by the runner-control test. The historical grades were not rewritten. Tests exercise the current grader. To inspect/reproduce historical grading, use the preserved source with `evals/` on Python's module search path; do not apply new grader hashes to old receipts.

## Other verification

- 55 regression tests, including an independent exhaustive form oracle over 80 seeded configurations inside one test and nine evaluation-runner/negative-control tests.
- 13 actual CLI scenarios and the ten-phase authored Harbor lifecycle passed; they are separate from the model case.
- All ten skill validators and the package validator passed.
- Protected portable install/update/uninstall and reproducible ZIP/extracted validation passed.
- Codex CLI 0.163.0-alpha.10.2 registered, installed and reported 0.1.2 enabled in a disposable profile. Cached skills matched source hashes; its helper created a program. Normal Codex configuration was unchanged. [Native receipt](../evals/reports/native-codex-0.1.2.json).

Implemented and observed locally: the packaged workflow, helper behavior, synthetic fresh-session continuation, native CLI installation and restore. Not observed: automatic skill selection in a fresh native Codex model session, Claude activation, non-Windows execution, real SME/candidate studies, actual LMS/credential integration or domain-owner acceptance. Nothing here establishes accreditation, psychometric validity, fairness or commercial readiness. Eventer still has broader multi-case and cross-host evidence; [the comparison](eventer-parity.md) states that difference.
