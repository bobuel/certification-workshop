# Version and compatibility policy

Current version: **1.0.0**. The delegated AI design review is complete, and the bounded native Codex create/resume check passed against runtime files unchanged in final v1. Repeat that check if runtime content changes. Claude metadata is included but Claude activation is unverified; it is not a supported-host claim.

The core is ten skills plus a standard-library Python helper. It uses existing local storage and assistant tools. Python 3.10+ is the intended minimum; **Windows/Python 3.11 is the verified v1 environment**. CI is configured for Python 3.10 and 3.13 on Windows, Linux and macOS; configuration is not a passing run. Other combinations are unverified until those checks run. This narrower support claim replaces the candidate's proposed all-platform release gate; see release-v1.md for the explicit scope decision.

Within v1, preserve the documented command names, meanings, exit codes and schema_version 1 record fields. Additions may be optional. Changes requiring user action need migration instructions and a major release. Correctness/security fixes may reject previously accepted unsafe records; document these explicitly in the changelog. JSON property order and explanatory prose are not stable interfaces.

Commands: `init`, `validate`, `status`, `coverage`, `assemble`, `check-form`, `review-packet`, `analyze`, `panel-summary`, `impact`, `export`, `reconcile-awards`. See the [helper contract](../skills/certification-workshop/references/helpers.md) for arguments. Exit 0 means a command completed, not that a program is ready; inspect returned gaps. Exit 1 indicates a failed gate and exit 2 invalid input.

Never silently migrate historical evidence. The pre-v1 fingerprint hardening requires verification and explicit repinning of legacy forms before analysis. Keep the old snapshot, exact form and supplied data. New wording, keys or rubrics require new item revisions and fresh review. Historical scores remain attached to their administered form; no automatic equating or approval transfer.

Release archives use an allowlist and fixed ZIP timestamps. Public exports have an original/public SHA-256 ledger. That ledger describes redaction; historical evaluation receipts continue to refer to original artifacts and are not new grades of edited artifacts. Retain the original evaluation privately when preparing a public derivative.
