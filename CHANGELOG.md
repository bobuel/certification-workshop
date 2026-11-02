# Changes

## 1.0.1 — 2026-11-02

- Added bounded, offline SHA-256 evidence auditing with project-root path checks and fail-closed enforcement of declared digests; optional required policy exposes missing source/review/decision/release evidence. Structural validation remains distinct from filesystem evidence verification.
- Bound hashed source dependencies to item reviews and assembled forms, including supporting task sources. Changing a source digest under an unchanged version no longer reuses the prior acceptance/form binding. Historical evidence needs explicit verification before repinning.
- Added raw-point versus item-weight reconciliation, optional explicit raw-point domain targets, and per-domain method minima. No psychometric target or passing standard is selected automatically.
- Blocked candidate exports containing normalized known restricted text or serialized key/rubric markers. This is not complete semantic disclosure or secret detection.
- Verified with 87 unit tests, ten offline phases and thirteen CLI scenarios; isolated Codex CLI installation/readback and cached-helper execution are separate from model activation. Human review, PostgreSQL execution, and psychometric validity are not implied by these results. See [1.0.1 verification](docs/release-v1.0.1.md).

## 1.0.0 — 2026-10-22

- Completed the owner-delegated AI design review and added a coherent final Northstar example, with a narrowed evidence-interpretation claim, explicit practical scoring, twelve item-review records and nine worked scoring responses.
- Resolved weighting, timing, capacity and study-sequence choices. The six-person feasibility design has no passing score or credential effect; real organizational authority and candidate evidence are not invented.
- Retained original eval artifacts and the earlier candidate example without transferring their approvals or scores. Runtime skills/helper are unchanged from the observed native create/resume candidate.
- Finalized the v1 distribution and promotion copy with an explicit Windows/Python 3.11 verification claim. Cross-platform CI is configured but unobserved; Claude activation remains unverified.

## 1.0.0-rc.1 — 2026-10-22

- Prepared a public release candidate with an allowlisted sanitized export, original/public file hashes, and tests for disclosure and overwrite boundaries.
- Added offline CI for Windows, macOS and Linux and a v1 command/record compatibility policy. Hosted CI execution remains unobserved until repository publication.
- Added an owner-review packet with all twelve Northstar items, actual program artifacts and five domain decisions. Revised nine selected-response items to reduce wording cues and split the access practical's overloaded scope criterion. All remain drafts; historical eval outputs and pilot scores were not changed or transferred.
- Clarified the item skill's authoring review and actual helper commands. The ten-skill scope and record schema remain unchanged.
- Final 1.0.0 is pending the gates recorded in docs/release-candidate.md.

## 0.1.2 — 2026-10-22

- Added the two-session Northstar program-owner evaluation: creation from raw sources, pilot interpretation, product change and release recommendation.
- Added preserved receipts, output snapshots, separate artifact reviews and grader negative controls.
- Made source preservation, historical analysis and verified handoff/restore explicit in the skills.
- Reworked onboarding around the owner journey and added security/contributor guidance.
- See the verification report for executed results and remaining limits.

## 0.1.1

Bound approvals and scored forms to exact content, policies, evidence and award intent. Added CLI scenarios and boundary regressions. Historical findings remain in docs/evaluation-findings.md.

## 0.1.0

Initial portable ten-skill lifecycle package, local helpers, synthetic Harbor example and isolated installer.
