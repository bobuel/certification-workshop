# Certification Workshop v1 — finished certification example

**Northstar Implementation Evidence · fictional development program · AI design review complete.**

The five design questions are resolved. This example demonstrates the completed development workflow; no real credential is being offered. [Read the design decisions and review basis](design-review.md).

**Claim:** Using the supplied procedures, interpret evidence from a bounded deployment, identify unsafe or incomplete conditions, and recommend justified verification, correction and escalation steps.

**Design:** 12 items, 33 points, practicals first. Six-person feasibility wave, 70-minute working-session target, no pass/fail. Four content-review hours plus four rater/calibration hours are explicitly budgeted; administration is deferred if that capacity is unavailable.

## Program artifacts

- [Charter and development sequence](charter.md)
- [Blueprint and score weights](blueprint-rationale.md)
- [Task-study instrument](follow-up-instrument.md)
- [Feasibility study and scoring protocol](pilot-protocol.md)
- [Candidate-facing guide](candidate-guide.md)
- [Worked full, partial and unsafe-response scoring examples](scoring-examples.md)
- [All twelve item-level AI review records](item-review.json)

## Assessment content

These are illustrative drafts, source-checked through AI review. A real implementing program supplies its own content reviewers, study evidence and authority. All three practicals use eight explicit 0/1 criteria; award no point for an absent, incorrect or contradictory required action. The aggregate provides partial credit. No unstated overall failure rule applies.

### NS_I01 · revision 2 · 1 point(s)

A UTF-8 CSV starts with field names and contains empty and repeated customer_id values. With header=true and customer_id required, how should version 1.0 handle invalid keys?

- **A.** Reject empty keys and duplicate keys; retain valid rows.
- **B.** Generate new IDs for empty keys; reject duplicate keys.
- **C.** Reject empty keys; keep duplicates when other fields differ.
- **D.** Skip empty keys silently; keep the last duplicate row.

**Key: A.** A follows I1. B invents ID generation, C allows prohibited duplicates, and D invents silent skipping and duplicate resolution.

Source: ING 1.0, I1 Configure

### NS_I02 · revision 2 · 1 point(s)

Of 1,000 rows, 970 are accepted, 20 rejected for empty keys and 10 for duplicate keys. No exclusion is agreed. What should the consultant recommend?

- **A.** Publish the 970 rows and record the rejection counts as the disposition.
- **B.** Retry the original input and compare the next rejection report before deciding.
- **C.** Resolve rejected rows through documented correction or an explicitly agreed exclusion.
- **D.** Ask the customer to verify the 970 accepted rows before publishing that subset.

**Key: C.** C follows I2. A/D leave rejected rows without an agreed disposition; B retries unchanged invalid input without resolving it.

Source: ING 1.0, I2 Reconcile; I4 Worked data

### NS_I03 · revision 2 · 1 point(s)

A 1,000-row import reports 990 accepted and 5 rejected. The five-row gap has no explanation. Which next step follows the documented reconciliation procedure?

- **A.** Record the gap as duplicate suppression and continue to value verification.
- **B.** Investigate the gap and escalate it to the data owner if unresolved.
- **C.** Apply a 99 percent acceptance threshold and continue to value verification.
- **D.** Inspect five accepted rows and use their values to close the accounting gap.

**Key: B.** B follows I2/I3. A invents a disposition; C invents a threshold; D confuses sampling with accounting.

Source: ING 1.0, I2 Reconcile; I3 Verify and release; I4 Worked data

### NS_I04 · revision 2 · 1 point(s)

Counts reconcile and rejection dispositions are documented. Required mappings and representative values still need verification, and release evidence must be retained. What role can preview --limit 5 play?

- **A.** Repair mapping errors in the displayed rows before the full release check.
- **B.** Validate every accepted row by checking five representative returned values.
- **C.** Replace the mapping check once five returned rows match the source values.
- **D.** Inspect returned accepted rows without changing their values or mappings.

**Key: D.** D follows I3. Preview is non-mutating and limited; A invents repair, B generalizes to all rows, and C omits the separate mapping check.

Source: ING 1.0, I3 Verify and release

### NS_I05 · revision 2 · 8 point(s)

Complete an ingestion evidence sheet and publication recommendation for B-17.

**Setup:** Synthetic paper case; no commands executed. Previous published P-16 remains available. UTF-8 CSV header customer_id,amount. Six data rows: 1 C101,10; 2 C102,20; 3 [empty],30; 4 C102,40; 5 C105,50; 6 C106,60. Supplied rejection report: row 3 empty key and row 4 duplicate key. Accepted=4, rejected=2. Configuration: header=true, customer_id required. Preview shows C101/10 and C105/50. Mapping log maps source amount to destination customer_name instead of amount. No exclusion agreed. Treat the report as authoritative about which duplicate row was rejected; do not invent duplicate semantics.

**Deliverable:** One sheet with configuration/mapping findings, row accounting, rejection disposition/rerun plan and publication recommendation with evidence and escalation. Distinguish supplied evidence from proposed repairs.

| Criterion | Points | Anchor |
| --- | --- | --- |
| Configuration | 1 | 1: Identifies header=true and required customer_id as the appropriate supplied settings. 0: absent, incorrect, or contradicted by another recommendation in the response. |
| Mapping | 1 | 1: Identifies amount-to-customer_name as wrong and proposes amount-to-amount mapping. 0: absent, incorrect, or contradicted by another recommendation in the response. |
| Accounting | 1 | 1: Explicitly accounts for 4 accepted + 2 rejected = 6 source rows. 0: absent, incorrect, or contradicted by another recommendation in the response. |
| Rejection disposition | 1 | 1: Addresses both row 3 and row 4 through correction with owner input or explicitly agreed exclusion; neither is silently discarded. 0: absent, incorrect, or contradicted by another recommendation in the response. |
| Recheck plan | 1 | 1: Proposes rerun/reconciliation after correction and rechecks mappings and representative values before release. 0: absent, incorrect, or contradicted by another recommendation in the response. |
| Release decision | 1 | 1: Holds publication while the mapping and rejection dispositions are unresolved; count agreement alone is insufficient. 0: absent, incorrect, or contradicted by another recommendation in the response. |
| Evidence retention | 1 | 1: Retains source/reconciliation evidence and the available previous published version. 0: absent, incorrect, or contradicted by another recommendation in the response. |
| Escalation | 1 | 1: Escalates discrepancies that remain unresolved to the customer data owner; does not claim proposed repairs have already occurred. 0: absent, incorrect, or contradicted by another recommendation in the response. |

Source: ING 1.0, I1 Configure; I2 Reconcile; I3 Verify and release

### NS_A01 · revision 3 · 1 point(s)

Under Northstar 2.0, an integration must read only orders. Which complete grant plan meets the requirement?

- **A.** Assign workspace traverse; leave dataset grants empty.
- **B.** Assign dataset orders query; leave workspace grants empty.
- **C.** Assign workspace traverse; assign dataset orders query.
- **D.** Assign workspace reader; leave dataset grants empty.

**Key: C.** C follows A1: traverse and dataset query are jointly required. A lacks query, B lacks traversal, and D grants access beyond orders.

Source: ACC 2.0, A1 Grant

### NS_A02 · revision 3 · 1 point(s)

The orders service account must read orders, be unable to write orders, and be unable to read unrelated customer data. Which verification record establishes all three requirements?

- **A.** Administrator: orders read succeeds, orders write denied, unrelated read denied.
- **B.** Service account: orders read succeeds, orders write denied, unrelated read denied.
- **C.** Service account: orders read succeeds, orders write denied, unrelated read untested.
- **D.** Service account: orders read succeeds, orders write untested, unrelated read denied.

**Key: B.** B tests every requirement under the intended identity (A2). A uses the wrong identity; C/D omit a required negative test.

Source: ACC 2.0, A2 Verify

### NS_A03 · revision 3 · 1 point(s)

A service token was disclosed in a shared note. The incident record contains no secret. Which response follows the documented procedure?

- **A.** Revoke the disclosed token and obtain an authorized replacement.
- **B.** Rename the service account and continue using its current token.
- **C.** Issue a replacement token and leave the disclosed token active.
- **D.** Remove the shared note and keep the token until scheduled rotation.

**Key: A.** A follows A3. B/C/D leave the disclosed credential valid; note deletion does not revoke it.

Source: ACC 2.0, A3 Compromise

### NS_A04 · revision 4 · 8 point(s)

For Northstar 2.0, complete an access evidence sheet for svc-orders and a safe remediation sequence.

**Setup:** Synthetic 2.0 paper case; no token supplied or changes executed. Requirement: read orders only. Current grant: workspace reader. A proposed replacement has workspace traverse only and no dataset query grant. Under the CURRENT broad grant, svc-orders orders read succeeds, orders write is denied, unrelated customer ledger read succeeds. An administrator read also succeeds. No tests of the proposed replacement have run. A service token was disclosed in a shared note, represented only as TOKEN_REDACTED.

**Deliverable:** One sheet: exact grant replacement and explanation of each required component; interpretation of current results and proposed replacement; service-identity recheck plan; token response sequence; credential-free incident/evidence record. Separate proposed actions from supplied observations.

| Criterion | Points | Anchor |
| --- | --- | --- |
| Grant configuration | 1 | 1: Removes workspace reader and specifies both workspace traverse and dataset orders query. 0: absent, incorrect, or contradicted by another recommendation in the response. |
| Joint requirement | 1 | 1: Explains that traverse alone cannot read data and query alone cannot navigate the workspace. 0: absent, incorrect, or contradicted by another recommendation in the response. |
| Current exposure | 1 | 1: Identifies successful unrelated ledger access as a failure of the orders-only requirement. 0: absent, incorrect, or contradicted by another recommendation in the response. |
| Verification plan | 1 | 1: Proposes testing as the service identity after changes: orders read succeeds, orders write is denied, unrelated data read is denied. 0: absent, incorrect, or contradicted by another recommendation in the response. |
| Revocation | 1 | 1: Revokes or proposes revocation of the disclosed token; renaming or adding a token is not revocation. 0: absent, incorrect, or contradicted by another recommendation in the response. |
| Replacement | 1 | 1: Obtains or proposes obtaining an authorized replacement token before resumed use. 0: absent, incorrect, or contradicted by another recommendation in the response. |
| Evidence record | 1 | 1: Records the relevant identity, supplied outcomes and incident/action status without including any secret. 0: absent, incorrect, or contradicted by another recommendation in the response. |
| Observation boundary | 1 | 1: Explicitly separates the current observed tests from proposed remediation/retests; does not claim the replacement grant has already passed. 0: absent, incorrect, or contradicted by another recommendation in the response. |

Source: ACC 2.0, A1 Grant; A2 Verify; A3 Compromise

### NS_R01 · revision 2 · 1 point(s)

A snapshot is two hours old and no recovery objective is recorded. Which rehearsal plan follows the documented procedure?

- **A.** Restore over active data; request customer confirmation of acceptable age.
- **B.** Restore separately; apply a one-day age limit from the team template.
- **C.** Restore separately; let the consultant set the acceptable-loss objective.
- **D.** Restore separately; seek the missing customer-approved recovery objective.

**Key: D.** D follows R1. A risks active data; B/C substitute an unapproved objective. Acceptable loss cannot be claimed until the customer objective is known.

Source: REC 1.0, R1 Restore

### NS_R02 · revision 2 · 1 point(s)

A separate restore passes verification and meets the approved recovery objective. A cutover/rollback recommendation is ready and the old namespace is retained. Which authorization sequence permits redirecting clients?

- **A.** Record the consultant's approval of this version, then redirect clients.
- **B.** Record the customer's approval of this version, then redirect clients.
- **C.** Redirect clients after the checks, then request the customer's approval.
- **D.** Use the customer's approval of an earlier version, then redirect clients.

**Key: B.** B follows R3. A substitutes consultant authority, C reverses authorization order, and D does not authorize the exact version.

Source: REC 1.0, R2 Verify; R3 Cut over

### NS_R03 · revision 3 · 8 point(s)

Complete a recovery evidence sheet and recommendation for R-22.

**Setup:** Synthetic paper case, no executable lab. Active prod-old remains in service. Immutable S-22 snapshot taken 08:00; decision time 11:00. Customer-approved maximum snapshot age is four hours. Separate restore target rehearsal-new. Manifest count=500; restored=497. Representative IDs/values match supplied manifest examples. Intended service identity reads orders, is denied orders write, but CAN read unrelated customer data. Job status complete. No customer cutover authorization.

**Deliverable:** One sheet: age/namespace checks, count/value/permission findings, hold/cutover decision and investigation plan, conditional cutover/rollback and authorization record. Separate observed evidence from required rechecks.

| Criterion | Points | Anchor |
| --- | --- | --- |
| Snapshot age | 1 | 1: Computes a three-hour snapshot age and compares it with the four-hour customer-approved maximum. 0: absent, incorrect, or contradicted by another recommendation in the response. |
| Separate restore | 1 | 1: Uses rehearsal-new while leaving active prod-old intact; does not overwrite active data. 0: absent, incorrect, or contradicted by another recommendation in the response. |
| Count discrepancy | 1 | 1: Identifies 500 minus 497 = 3 unexplained missing rows as a verification failure. 0: absent, incorrect, or contradicted by another recommendation in the response. |
| Permission discrepancy | 1 | 1: Identifies unrelated customer-data access as excess service permission despite successful orders read/write-denial tests. 0: absent, incorrect, or contradicted by another recommendation in the response. |
| Cutover decision | 1 | 1: Holds cutover because verification failed; completion and sample matches do not override those failures. 0: absent, incorrect, or contradicted by another recommendation in the response. |
| Correction and recheck | 1 | 1: Investigates/corrects the count and permission failures, then repeats counts, representative-value checks and intended service-permission tests. 0: absent, incorrect, or contradicted by another recommendation in the response. |
| Rollback | 1 | 1: Retains prod-old and identifies redirecting clients back to that retained namespace as the rollback route. 0: absent, incorrect, or contradicted by another recommendation in the response. |
| Authorization | 1 | 1: Requires customer authorization identifying the actor and exact version before redirecting clients; does not claim incident-command authority. 0: absent, incorrect, or contradicted by another recommendation in the response. |

Source: REC 1.0, R1 Restore; R2 Verify; R3 Cut over; ACC 2.0, A2 Verify
