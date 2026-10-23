# Local helper interface

Requires Python 3.10+ standard library. No network, model API, credentials or daemon. Locate `scripts/certification.py` relative to the coordinating skill. In these examples `HELPER` means that absolute script path and `PROGRAM` means the user's `program.json`; substitute actual quoted paths in the host shell.

```text
python HELPER init --directory NEW_FOLDER --id PROGRAM_ID --title "Program title" [--mode demo]
python HELPER validate --program PROGRAM
python HELPER status --program PROGRAM
python HELPER coverage --program PROGRAM [--live]
python HELPER assemble --program PROGRAM --form NEW_FORM_ID [--live]
python HELPER check-form --program PROGRAM --form FORM_ID [--live]
python HELPER review-packet --program PROGRAM [--item ITEM_ID ...]
python HELPER analyze --program PROGRAM --form FORM_ID --csv SCORES.csv
python HELPER panel-summary --program PROGRAM --form FORM_ID --csv JUDGMENTS.csv
python HELPER impact --program PROGRAM --source SOURCE_ID [--source SOURCE_ID ...]
python HELPER export --program PROGRAM --audience candidate-guide
python HELPER export --program PROGRAM --audience delivery --form FORM_ID
python HELPER reconcile-awards --program PROGRAM
```

All commands except init accept `--out NEW_JSON_FILE` and otherwise print JSON. Output files are exclusively created: an existing file is never replaced. Create the parent directory first. Init creates a new program folder with program.json, summary.md and working-templates.md. It does not create a finished certification. Helpers never mutate an input record or issue/send/publish anything.

Exit 0: successful calculation/structural validation. Exit 1: requested form/assembly/award checks failed, with structured reasons. Exit 2: invalid input, missing file, or refused output overwrite. Coverage and status return issues in JSON and are not launch exit gates.

## Form assembly

Largest-remainder item-count targets, exact current accepted items, no shared enemy groups, and global form-level required method minimums. Per-domain method minimums are not enforced; review them explicitly if the specification requires them. Deterministic bounded search (100,000 nodes). `infeasible` means no form under the supported constraints; `search_limit` means the search did not establish an answer. Both return no form. Never silently relax constraints. On success, manually add the returned proposal to `forms` only after examining it. A proposed form is not approved or delivered.

## Analysis files

Scores CSV: one row per pseudonymous candidate, header `candidate_id` plus exact `ITEM_ID@REVISION` columns for every form item. The form must also retain matching content fingerprints in its item references; identical version labels alone are insufficient. Column order may differ. No duplicate IDs/headers, extra/missing columns, blanks, NaN, infinity or out-of-range scores. Single choice is 0 or 1; practical tasks accept recorded scores between 0 and max_score. Define omission scoring with the owner before replacing a blank with zero. For multiple attempts, select a justified cohort rather than disguising duplicates as independent candidates.

Expected-score judgment CSV: same layout with `judge_id`. Each entry is the judge's expected score for the defined minimally competent candidate, from 0 to that item's max_score. Single-choice judgments can be fractional. The helper summarizes one round and one form. It does not verify judge expertise, select the method or approve a cut score. See [analysis limits](analysis.md).

## Exports

`candidate-guide` is a public draft containing program title, domain titles/item weights, and only `public.overview`, `audience`, `eligibility`, `format`, `permitted_resources`, `accommodations`, `retakes`, `appeals`, `renewal`, `support`. It never serializes bank, reviews, notes, scores or award records. Free-text fields must still be reviewed before sharing.

`delivery` is a **restricted** neutral JSON authoring handoff including item keys and rubrics. It checks development form constraints, records demo/real mode and fingerprint, and does not claim compatibility with any external delivery system. For a named platform, create and test an explicit mapping to its current import schema. Do not send this export to candidates.

## Impact and operations

Impact returns a conservative closure through source -> tasks -> competencies -> domains/items -> forms, without editing records. An editorial source change can have a smaller actual effect; inspect the difference.

Award reconciliation checks duplicate credential intent, exact candidate/version/action decision fingerprints, missing or duplicate receipts, and unknown/submitted states needing readback. A revocation needs its own current authority, reason (for a real program), and revocation receipt; an issuance receipt cannot stand in for it. Real issuance needs result and eligibility evidence references. This is local evidence checking, not a provider query. IDs/hashes/receipts alone do not authenticate an award. No helper claims legal compliance or measurement validity.
