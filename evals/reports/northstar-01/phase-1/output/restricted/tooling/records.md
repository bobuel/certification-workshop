# Program record contract, version 1

UTF-8 JSON, `schema_version: 1`. All record IDs are letter-led identifiers containing letters, digits, `_` or `-`, up to 64 characters. Revisions are positive integers. Version strings on sources/credentials are nonempty text. No comments, duplicate keys, NaN or Infinity. `init` creates an empty structurally valid record; `examples/harbor/program.json` in the complete package is a populated synthetic example.

## Top-level objects

| Object | Fields and meaning |
| --- | --- |
| `program` | `id`, `title`, `mode` (`real`/`demo`), `revision`, `owner`, `audience`, `claim`, `purpose`, `status`. Empty scope fields are allowed at initialization; complete them in the charter. |
| `sources[]` | `id`, `version`, `location`, optional `title`, `evidence_kind` (`real`/`synthetic`), `current` boolean. Retain old versions; exactly one may be current per ID. |
| `tasks[]` | `id`, `statement`, `source_refs[]`, optional KSA, conditions, outcome, study status and findings. Draft/inferred tasks are not validated tasks. |
| `competencies[]` | `id`, `statement`, nonempty `task_ids[]`; optional proficiency anchors and evidence notes. |
| `blueprint` | `id`, `revision`, `status`, `weight_basis: items`, `form_length`, `domains[]`, `required_methods` mapping type to a global form-level minimum count. Per-domain method minimums require separate review and are not enforced by this helper. |
| `items[]` | See item contract below. Current revisions only; retain historical snapshots for old forms. |
| `reviews[]` | `id`, `item_id`, exact `revision`, `reviewer`, `role`, `verdict` (`accept`/`revise`/`reject`), `evidence_kind`, `evidence_ref`, `item_fingerprint` from the review packet; optional `resolved`, `resolution`, `resolved_by`. A missing or changed fingerprint cannot support acceptance. |
| `decisions[]` | `id`, `target_type` (`program`/`blueprint`/`form`/`award`), `target_id`, `revision`, `decision` (`approve`/`reject`), `actor`, `evidence_kind`, `evidence_ref`, `rationale`. Live program/blueprint/form approvals also need `target_fingerprint` from the review material. Conflicting decisions require reconciliation/new target revision. |
| `forms[]` | `id`, `revision`, `blueprint_revision`, `status`, `item_refs[]` of `{item_id, revision, item_fingerprint}`; optional `release_evidence` with report/readback locations. Assembly pins content hashes. Legacy unpinned forms remain structurally readable but cannot pass checks or be analyzed. |
| `awards[]` | `id`, `revision` (default 1), pseudonymous `candidate_id`, `credential_version`, `action` (`issue` default, or `revoke`), `decision_id`, `status` (`draft`/`authorized`/`submitted`/`unknown`/`issued`/`revoked`), issuance `receipt` or separate `revocation_receipt`. A current content-bound owner decision must target this exact candidate/version/action. Real issuance also requires `eligibility_evidence` and `result_evidence`; revocation requires `reason`. |
| `policies` | Owner-approved text for `passing_standard`, `eligibility`, `retakes`, `appeals`, `accommodations`, `renewal`, `data_retention`, `delivery`. A draft remains labeled draft in supporting documents. |
| `public` | Reviewed public text fields; only named fields in the export contract are released. Never put exam answers or restricted evidence here. |
| `notes` | Optional working notes. Never exported to the public guide. |

Each `source_refs` entry is `{source_id, version, locator}`. `locator` is a specific section/page/timestamp or artifact location, not a generic website. Domain fields: `id`, `title`, positive `weight` percentage, nonempty `competency_ids`. Weights sum to 100. Form length and weights are by **item count**; practical exercises may have more points, so score percentages differ. Helper allocation uses largest remainder with domain ID as the stable tie-break. A domain rounded to zero is a visible design issue.

## Item contract

Every item: `id`, `revision`, `domain_id`, nonempty `competency_ids` belonging to that domain, `type` (`single_choice`/`practical`), `status` (`draft`/`in_review`/`approved`/`retired`), `prompt`, `rationale`, nonempty `source_refs`, positive `max_score`, optional `enemy_groups[]`. Items sharing any enemy group may not appear together.

Single-choice: `options` object of distinct labeled answers, `answer_key` matching a label, `max_score: 1`.

Practical: `setup`, `deliverable`, `rubric[]` with `criterion`, positive `points`, explicit `anchor`. Rubric points sum to max_score. Include partial-credit/zero-score behavior in anchors. Rubric correctness and rater agreement require actual review/study, not a structural pass.

Optional useful fields: cognitive level with reason, intended challenge, task criticality, response time proposal, author, review notes, media/accessibility needs, and exposure controls. They do not alter scoring helpers.

## Readiness and versioning

Structure validation checks relationships and field types. Eligibility for form assembly additionally requires `approved`, a current content-role acceptance, no unresolved negative current review, and current source versions. `--live` requires those supporting source/review entries to be real. It does not authenticate identities or documents.

Live form record checks additionally require real program/blueprint/form approvals for exact revisions and content fingerprints, approved statuses, populated owner/audience/claim/purpose, a real-mode program, policy entries, and form release evidence locations for `job_analysis_report`, `pilot_report`, `standard_setting_report`, `delivery_verification`. Item eligibility checks both direct source references and supporting task-source references. These are minimum record checks, not a full technical or organizational release review.

Changing an item without incrementing its revision violates the contract and invalidates both its review fingerprint and the form's pinned content. `content_fingerprint` hashes all object fields except status/release_evidence; obtain item fingerprints from review-packet. Form identity includes practical setup/deliverable, scoring and all other item content. A historical form referencing superseded or edited items cannot be analyzed from the new bank; load its archived program snapshot. Never carry scores or approvals to changed content by renaming it.

Obtain approval target hashes from `status.decision_target_fingerprints`, then bind the actual decision to the reviewed target. These hashes have different scopes:

- Program: program definition, policies and public guide text. A changed passing rule invalidates prior program approval.
- Blueprint: blueprint, task/competency model and source inventory. Changed competence claims invalidate prior blueprint approval.
- Form: assessment identity plus release-evidence references. Replacing a study/readback reference invalidates prior form approval. Adding release evidence does not change the separately reported scored-form identity.
- Award: ID/revision, candidate, credential version, action and relevant eligibility/result/revocation evidence. Status progression and observed provider receipts do not change intent. Approval to issue does not authorize revocation or a different recipient.

For a legacy unpinned form, preserve the original and find the exact historical item content and scoring used. After verification, record those item fingerprints in a new working copy. Do not blindly pin the current bank and attach old scores. If the historical content cannot be established, report that limitation and do not analyze the matrix against invented content. Old v0.1.0 approval hashes must be reviewed/rebound to the expanded scopes; the helper does not migrate authority automatically.

IDs are local references, not permission grants. A copied approval field is not evidence that a person approved it. The assistant must read and reconcile referenced evidence in a real program.
