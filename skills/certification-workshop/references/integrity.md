# Local evidence and scoring checks

These additions are in the unreleased 1.0.1-dev build. They check local records and bytes; they do not authenticate a document's author, a reviewer's identity, an approval, or measurement validity.

## Preserve and verify evidence

Store source snapshots beneath the program's project folder. Keep `location` relative to that folder and add `sha256` with the exact snapshot's 64-character SHA-256 digest. Preserve the source URL, version, retrieval time, rights, and specific section locator separately. A URL alone is not a local snapshot. The helper never fetches it.

`audit-evidence --program PROGRAM` reports missing/invalid digests, missing or unreadable files, unsafe paths, external references, oversized files, and digest mismatches. It exits 1 when any check fails. The default evidence root is PROGRAM's directory; `--evidence-root PROJECT` deliberately selects a different project root. Paths may not be absolute, contain `..` or backslashes, or resolve through a symlink outside that root. The per-file limit is 10 MiB. Larger sources require an explicitly prepared bounded evidence artifact and preserved provenance, not silent truncation.

For reviews and decisions, use a local `evidence_ref` and optional `evidence_sha256`. For a form's `release_evidence`, corresponding digests belong in `release_evidence_sha256` with the same keys. Matching a digest shows consistency with the recorded bytes, not that the claimed actor acted.

Default compatibility mode is `validation_policy.evidence_integrity: if_declared`: declared source/evidence digests are enforced by assembly, form checking, restricted delivery export, and score/panel analysis. Missing undeclared digests remain visible in `status` and CLI `validate` audits, rather than silently being described as verified. An existing unpinned legacy example can still run development checks.

Use `validation_policy: {"evidence_integrity": "required"}` for a program requiring all source, review, decision, and supplied release-evidence files to be locally pinned and verified. This technical validation policy is part of the program approval fingerprint. It is not an owner-approved assessment or passing policy.

Python API callers must pass `evidence_root=Path(...)` to gated functions when declarations or required policy apply. Omitting it refuses the gate, rather than guessing the current working directory. `validate(data)` remains structural; use `audit_evidence(data, root)` for filesystem verification. CLI `validate` still returns structural exit 0 with a nested audit; use `audit-evidence` when an evidence exit gate is required.

## Bind reviews and forms to sources

`review-packet` now includes per-item `source_fingerprints`: source ID/version to SHA-256 for all direct and supporting task references with declared digests. An acceptance must retain the reviewed mapping as well as the item fingerprint. Assembly pins the corresponding mapping in the form. Changing bytes and updating a digest without changing the source version therefore still invalidates old review/form bindings.

**Migration is not automatic approval.** Retain the historical snapshot. If adding source hashes to an older bank, its earlier acceptances/forms are insufficient for the new content-bound check. Verify the original source bytes and actual review evidence before recording new bindings; do not manufacture acceptance or attach old candidate scores to an unverified reconstruction. Sources without declared digests keep the legacy record behavior with visible audit gaps.

## Reconcile item and point weights

`score-weights --program PROGRAM` summarizes the entire bank and labels it `bank_diagnostic`; use `--form FORM_ID` for an exact pinned form. Assembly and form checks also show the selected form's raw-point proportions. Item-count weights are not automatically score weights, and a larger practical rubric changes raw-point contribution.

If a program has an explicit raw-point design target, declare `blueprint.score_weight_policy` with `basis: raw_points`, a `target_percent` mapping covering every domain and summing to 100, and optional `tolerance_percentage_points` (default 0.01). Assembly searches for forms satisfying these targets without relaxing them; form checking rejects mismatches. No target means a visible `score_weight_targets_not_declared` warning, not an invented standard or automatic failure.

Only raw-point scoring is implemented. Domain-normalized scoring is rejected as unsupported, not silently simulated. Any policy field records a supplied design choice; it is not evidence of authorization, fairness, validity, a cut score, or equivalence.

Where an assessment design explicitly needs a practical exercise in a particular domain, declare `blueprint.required_methods_by_domain`, for example `{"RECOVERY": {"practical": 1}}` using actual domain IDs. These optional constraints are enforced by assembly and form checking in addition to the existing global method minima. No per-domain requirement is inferred or supplied automatically.

## Screen candidate text

`audit-public` and candidate-guide export screen every exported text field, including program/domain titles, against normalized known bank prompts, options, rationales, practical setup/deliverables, rubric anchors, and private notes. Exact normalized phrases of at least twelve characters and JSON-like restricted-record markers block export. The error names the offending field/record, not the restricted phrase.

This is deliberately conservative and incomplete. Short/common answer strings, paraphrases, new secrets, and semantic disclosure may not be detected. Legitimate reuse can also trigger a block. Revise the public guidance or resolve the classification explicitly; do not remove the private bank merely to bypass the check. Retain the allowlist and perform audience review before sharing.
