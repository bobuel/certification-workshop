# Certification Workshop 1.0.1 verification

November 2, 2026. This maintenance update retains the ten-skill, local-files architecture and Python standard-library runtime. It introduces no hosted service, mandatory provider, model API key or persistent installation.

## Fixed boundaries

- Local source snapshots and review/decision/release receipts can be checked against SHA-256 digests. Declared hashes fail closed; a required-evidence policy also rejects missing pins. Checks are bounded to project-relative files and do not fetch URLs or establish authorship.
- Reviews and assembled forms pin hashed source dependencies, including task sources. Changing or deleting those pins invalidates acceptance and form checks rather than silently downgrading to legacy behavior.
- Raw-point shares are reported separately from blueprint item shares. Explicit raw-point targets and per-domain method minima can be enforced; the software does not invent an owner scoring standard.
- Candidate exports reject known restricted phrases and serialized key/rubric markers in allowlisted free text. This is a deterministic guard, not semantic leak prevention or complete secret detection.

Read the [integrity and scoring contract](../skills/certification-workshop/references/integrity.md) before adding source pins to an existing program. Historical evidence must be verified, not automatically re-approved or repinned.

## Executed local checks

Linux, Python 3.12.14:

```sh
python -m unittest discover -s tests -v
python scripts/validate.py
python evals/run.py
python evals/scenarios.py
python scripts/public_export.py --check .
python scripts/package.py
git diff --check
```

The local suite passed 87 unit tests (28 added regressions), ten offline lifecycle phases, thirteen CLI scenarios, package validation, the public-export scan and reproducible packaging. Negative controls cover missing/tampered/unsafe evidence, stale review bindings, removal of source pins, score targets, method coverage and restricted export text. Hosted CI status must be read for the exact published commit; these local results are not a cross-platform CI claim.

A separate bounded validation used preserved official PostgreSQL documentation: eight draft items, 62 workflow assertions and 16 sample/revision checks. The real-mode draft has no human approvals, decisions, forms or awards. Synthetic acceptance records were isolated as development-only fixtures. The source-version change exercise did not establish a semantic PostgreSQL change. The sample remains outside the distributable plugin and repository, consistent with the synthetic-only examples policy.

Codex CLI 0.166.0-alpha.1 installed 1.0.1 in a disposable Linux profile, reported installed/enabled and ran its byte-matching cached helper against the sample evidence. The profile was removed. No normal profile or user desktop configuration was changed. This verifies installation/readback and helper execution only, not fresh-model discovery/resume or desktop UI. Earlier 1.0.0 model-activation results remain historical, because this update changes runtime content.

## Not established

Human SME acceptance, psychometric validity, a passing standard, execution of the PostgreSQL practical exercises, semantic secrecy, fresh-model activation and Claude activation are not established by these checks. Source digests establish equality to declared local bytes, not real-world author authenticity. Real programs still need expert review and owner decisions.
