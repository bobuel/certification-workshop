# Your certification review packet

**Fictional Northstar case · v1 plugin release candidate · all assessment content is draft.**

Review the program, then the actual items below. The original evaluation remains unchanged; this packet contains the new author revision.

## Five decisions

1. **Claim:** bounded implementation reasoning, verification and escalation. The written practicals do not observe actual software execution. Keep that scope?
2. **Weighting:** 5 ingestion, 4 access and 3 recovery items; 12/11/10 points respectively. Practicals carry 24 of 33 points. Is that intended?
3. **Quality:** are the options plausible, keys defensible and rubric anchors independently scoreable? Note item IDs that need changes.
4. **Capacity:** a proposed 70-minute assessment; four content-review hours plus an estimated 7.5 rater-hours. Add capacity or reduce scope?
5. **Release judgment:** hold launch, investigate negative associations in the synthetic pilot, review changed items, and obtain a justified exact-version passing rule. Is that the right decision sequence?

## Program outputs

- [Charter and six-week plan](charter.md)
- [Job tasks and competencies](job-analysis.md)
- [SME follow-up instrument](follow-up-instrument.md)
- [Blueprint and weight rationale](blueprint-rationale.md)
- [Pilot protocol](pilot-protocol.md)
- [Candidate guide](candidate-guide.md)
- [Pilot interpretation and release recommendation](release-recommendation.md)
- [Product-change analysis](change-impact-review.md)
- [Open owner decisions](decision-register.md)

The first five documents are the original product-1.0 design proposals. The guide and change/release documents describe product 2.0 before this author pass. Historical PILOT1/PILOT2 and revision-2 statistics do not describe the revised bank below. [Provenance and revision details](README.md).

## Assessment drafts

All nine multiple-choice items were revised to reduce wording cues. The access practical now separates grant replacement and explanation. No human acceptance, pilot score or approval transfers to these drafts.

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

### NS_I05 · revision 1 · 8 point(s)

Complete an ingestion evidence sheet and publication recommendation for B-17.

**Setup:** Synthetic paper case; no commands executed. Previous published P-16 remains available. UTF-8 CSV header customer_id,amount. Six data rows: 1 C101,10; 2 C102,20; 3 [empty],30; 4 C102,40; 5 C105,50; 6 C106,60. Supplied rejection report: row 3 empty key and row 4 duplicate key. Accepted=4, rejected=2. Configuration: header=true, customer_id required. Preview shows C101/10 and C105/50. Mapping log maps source amount to destination customer_name instead of amount. No exclusion agreed. Treat the report as authoritative about which duplicate row was rejected; do not invent duplicate semantics.

**Deliverable:** One sheet with configuration/mapping findings, row accounting, rejection disposition/rerun plan and publication recommendation with evidence and escalation. Distinguish supplied evidence from proposed repairs.

| Criterion | Points | Anchor |
| --- | --- | --- |
| Configuration | 2 | 2: identifies appropriate header/key settings AND wrong amount mapping requiring correction; 1: only one; 0: neither or accepts mapping. |
| Reconciliation | 2 | 2: gives 4+2=6 and says count agreement alone does not authorize release; 1: correct arithmetic without release implication; 0: arithmetic wrong or says totals alone permit release. |
| Rejected rows | 2 | 2: addresses both invalid keys through correction with owner input or explicit agreed exclusion, then rerun/reconcile; 1: fully handles one or omits agreement/rerun; 0: silent exclusion or unchanged retry as repair. |
| Release/evidence | 2 | 2: holds pending corrected mapping/dispositions and representative recheck, retains source/reconciliation and previous version, escalates unresolved discrepancy to data owner; 1: holds with incomplete evidence/rechecks/escalation; 0: recommends publication now. |

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

### NS_A04 · revision 3 · 8 point(s)

For Northstar 2.0, complete an access evidence sheet for svc-orders and a safe remediation sequence.

**Setup:** Synthetic 2.0 paper case; no token supplied or changes executed. Requirement: read orders only. Current grant: workspace reader. A proposed replacement has workspace traverse only and no dataset query grant. Under the CURRENT broad grant, svc-orders orders read succeeds, orders write is denied, unrelated customer ledger read succeeds. An administrator read also succeeds. No tests of the proposed replacement have run. A service token was disclosed in a shared note, represented only as TOKEN_REDACTED.

**Deliverable:** One sheet: exact grant replacement and explanation of each required component; interpretation of current results and proposed replacement; service-identity recheck plan; token response sequence; credential-free incident/evidence record. Separate proposed actions from supplied observations.

| Criterion | Points | Anchor |
| --- | --- | --- |
| Grant replacement | 1 | 1: removes workspace reader and specifies both workspace traverse and dataset orders query. 0: any required change missing, or endorses broad access or either grant alone. |
| Explain joint requirement | 1 | 1: explains that traverse alone cannot read data and query alone cannot navigate the workspace. 0: either explanation missing or contradicted. |
| Verification | 2 | 2: identifies current ledger success as failure and requires service-identity orders read success, orders write denial and unrelated-data denial after BOTH replacement grants; 1: recognizes exposure but rechecks incomplete; 0: accepts administrator test or current results as verification of proposed replacement. |
| Disclosure | 2 | 2: revokes disclosed token and gets authorized replacement; 1: only one; 0: rename/add token only or keep using disclosed token. |
| Evidence | 2 | 2: records identity, outcomes and incident/action status without secrets and labels proposed rechecks as proposed; 1: safe record with missing identity/status detail; 0: copies secret or falsely claims remediation happened. |

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

### NS_R03 · revision 2 · 8 point(s)

Complete a recovery evidence sheet and recommendation for R-22.

**Setup:** Synthetic paper case, no executable lab. Active prod-old remains in service. Immutable S-22 snapshot taken 08:00; decision time 11:00. Customer-approved maximum snapshot age is four hours. Separate restore target rehearsal-new. Manifest count=500; restored=497. Representative IDs/values match supplied manifest examples. Intended service identity reads orders, is denied orders write, but CAN read unrelated customer data. Job status complete. No customer cutover authorization.

**Deliverable:** One sheet: age/namespace checks, count/value/permission findings, hold/cutover decision and investigation plan, conditional cutover/rollback and authorization record. Separate observed evidence from required rechecks.

| Criterion | Points | Anchor |
| --- | --- | --- |
| Starting state | 2 | 2: computes three-hour age within four-hour objective AND confirms separate namespace protects active data; 1: only one; 0: wrong age or proposes overwrite. |
| Failures | 2 | 2: identifies three-row mismatch AND excess service access despite completion/sample match; 1: one failure; 0: accepts restore as verified. |
| Recommendation | 2 | 2: holds cutover for investigation/correction and repeat counts/values/intended-permission tests; 1: holds with incomplete follow-up; 0: cutover despite a failure. |
| Authority/rollback | 2 | 2: retains prod-old, specifies rollback route to retained namespace and requires customer authorization with actor/exact version before redirect; 1: retains old and requires approval but lacks rollback/version detail; 0: deletes old, redirects unapproved or claims incident command. |

Source: REC 1.0, R1 Restore; R2 Verify; R3 Cut over; ACC 2.0, A2 Verify
