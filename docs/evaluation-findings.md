# Expanded evaluation findings — 0.1.1

On 2026-10-21, seven new evidence-boundary probes were run against 0.1.0 before fixes. All seven failed. The failures were local record-checking gaps; no provider action, real credential, real candidate data or public release occurred.

| Reproduced gap in 0.1.0 | Correction in 0.1.1 | Regression evidence |
| --- | --- | --- |
| Passing-policy edits retained an old program approval | Program approval includes policies and public guidance | Changed policy blocks live record checks |
| Competency edits retained an old blueprint approval | Blueprint approval includes tasks, competencies and source inventory | Changed competency blocks live record checks |
| Replacing a study reference retained old form approval | Release approval includes the form's evidence references | Replaced standard-setting reference invalidates approval |
| Candidate identity could change under an award's old approval | Award authority binds candidate, credential version, action and supporting evidence | Retargeted candidate fails reconciliation |
| Issuance authority/receipt could support a revoked state | Revocation requires its own action, current authority and receipt | Issue-only authority cannot reconcile revocation; correctly authorized revocation passes |
| Analysis accepted edited items carrying unchanged revision numbers | Forms pin exact content fingerprints and analysis verifies them | Same-revision edits and unpinned legacy forms are rejected |
| Form identity omitted practical setup/deliverable | Form fingerprints include complete item content | A changed starting state changes assessment identity |

## Additional evaluation

- Regression suite: 46 test methods pass. One method independently enumerates possible forms for 80 seeded banks and compares the constrained search result to that oracle; the 80 configurations are not counted as 80 extra test methods.
- Command-line scenarios: 13 pass, covering new-program initialization, draft-bank refusal, conflicting reviews, missing pilot scores, reordered score headers, same-revision content edits, legacy imports, source changes, public exports, synthetic live-readiness refusal, unknown issuance outcomes, output collisions and read-only inputs.
- Statistical checks include independent expected arithmetic, undefined zero-variance cases, negative alpha retention and raw unrounded panel summaries.
- Existing ten-phase synthetic lifecycle and packaging/installation checks remain part of the verification.

See [the machine-readable CLI report](../evals/reports/offline-scenarios-0.1.1.json), [verification](verification.md), and [behavioral walkthroughs](forward-test.md). These layers are deliberately reported separately; none alone establishes model reliability or a credential's measurement quality.

## Compatibility

Existing record schema version 1 remains structurally readable. Old form references without content fingerprints cannot pass form checks or be used for score analysis until the exact historical content is verified and pinned. Approval target scopes have expanded, so old program/blueprint/form/award hashes require actual review against the new scope. No helper silently creates that authority or rewrites old records.

All bundled synthetic examples were regenerated under 0.1.1. The local package is still unsubmitted/unpublished, and native host activation, real candidate/SME studies, provider integrations and owner acceptance remain separate validation work.
