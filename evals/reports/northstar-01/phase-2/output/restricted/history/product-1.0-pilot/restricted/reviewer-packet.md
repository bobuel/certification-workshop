# Restricted reviewer packet — revision 1, all items DRAFT

All evidence and people fictional/synthetic. No workshop participant reviewed the bank. This is restricted even without keys. Exact fingerprints are in reviewer-packet.json.
Review accuracy, claim relevance, sufficient scenario information, source support, unique keys, distractors, rubric usability, cognitive demand, clarity, accessibility and bias. Record actual reviewer/role/expertise/conflicts/date, exact revision/fingerprint, verdict, evidence and unresolved comments. Silence is not approval.
Scoring: MC correct 1 otherwise 0. Practical criteria 0/1/2. Unsafe contradictions earn zero on the affected criterion; do not double-penalize unrelated criteria. There is no overall automatic-fail or passing rule.
Authored calibration examples, not candidate data: NS_I05 gives 4+2=6 but says this permits immediate publication: reconciliation 0 and release 0. NS_A04 explains narrow grant and exposure but mentions revocation without replacement: scope 2, disclosure 1. NS_R03 detects both failures but omits authorization: failures 2, authority 0. Score other criteria from actual response only.

## NS_I01 / revision 1 / DRAFT
Domain D_I; competencies ['C_I']; tasks ['T_I1']. 1 points; proposed 2 min.
Sources: ING 1.0: I1 Configure
Apply/analyze documented rules within a scenario. Distinguish adequate evidence from plausible shortcuts; empirical difficulty unknown

A UTF-8 CSV starts with field names and contains empty and repeated customer_id values. Which configuration and expected behavior match version 1.0?

A. Set header=true, require customer_id, and expect empty or duplicate key rows to be rejected.
B. Set header=true and generate replacement IDs for invalid rows.
C. Set header=false and make customer_id optional.
D. Set header=true and accept duplicate IDs when other columns differ.

Key: A
A follows I1. B invents ID generation; C misreads headers and required key; D contradicts duplicate rejection.

Reviewer ____; role/expertise ____; conflict ____; date ____; fingerprint ____; accept/revise/reject ____; evidence/comments ____; resolution/authority ____; unresolved ____ .

## NS_I02 / revision 1 / DRAFT
Domain D_I; competencies ['C_I']; tasks ['T_I2']. 1 points; proposed 2 min.
Sources: ING 1.0: I2 Reconcile; I4 Worked data
Apply/analyze documented rules within a scenario. Distinguish adequate evidence from plausible shortcuts; empirical difficulty unknown

Of 1,000 rows, 970 are accepted, 20 rejected for empty keys and 10 for duplicate keys. No exclusion is agreed. What next?

A. Publish because accepted plus rejected equals 1,000.
B. Retry unchanged input until all rows are accepted.
C. Review rejections and document correction or explicitly agreed exclusion before considering publication.
D. Publish accepted rows and treat rejected rows as implicitly excluded.

Key: C
C follows I2. A confuses count agreement with permission; B cannot repair invalid input; D invents agreement.

Reviewer ____; role/expertise ____; conflict ____; date ____; fingerprint ____; accept/revise/reject ____; evidence/comments ____; resolution/authority ____; unresolved ____ .

## NS_I03 / revision 1 / DRAFT
Domain D_I; competencies ['C_I']; tasks ['T_I2', 'T_I3']. 1 points; proposed 2 min.
Sources: ING 1.0: I2 Reconcile; I3 Verify and release; I4 Worked data
Apply/analyze documented rules within a scenario. Distinguish adequate evidence from plausible shortcuts; empirical difficulty unknown

A 1,000-row import reports 990 accepted and 5 rejected. What conclusion is supported?

A. Treat the five remaining rows as duplicates.
B. Investigate the unexplained gap before publication; escalate unresolved discrepancy to the customer data owner.
C. Publish because acceptance is at least 99 percent.
D. Preview five accepted rows to account for the missing rows.

Key: B
B follows I2/I3: only 995 rows are accounted for. A invents reasons; C invents threshold; D confuses sampling with accounting.

Reviewer ____; role/expertise ____; conflict ____; date ____; fingerprint ____; accept/revise/reject ____; evidence/comments ____; resolution/authority ____; unresolved ____ .

## NS_I04 / revision 1 / DRAFT
Domain D_I; competencies ['C_I']; tasks ['T_I3']. 1 points; proposed 2 min.
Sources: ING 1.0: I3 Verify and release
Apply/analyze documented rules within a scenario. Distinguish adequate evidence from plausible shortcuts; empirical difficulty unknown

Counts reconcile and rejection dispositions are documented. A colleague says preview --limit 5 repairs mapping errors and proves readiness. What should you do?

A. Use preview to repair, then publish without retaining evidence.
B. Treat preview completion as proof that all values are correct.
C. Skip mappings because counts reconcile.
D. Use preview to inspect accepted rows without changing them; check required mappings and representative values, retaining source and reconciliation evidence.

Key: D
D follows I3. A incorrectly makes preview mutating; B overclaims sampling; C omits verification.

Reviewer ____; role/expertise ____; conflict ____; date ____; fingerprint ____; accept/revise/reject ____; evidence/comments ____; resolution/authority ____; unresolved ____ .

## NS_I05 / revision 1 / DRAFT
Domain D_I; competencies ['C_I']; tasks ['T_I1', 'T_I2', 'T_I3']. 8 points; proposed 12 min.
Sources: ING 1.0: I1 Configure; I2 Reconcile; I3 Verify and release
Analyze/evaluate evidence and justify safe next steps. Integrate several conditions; empirical difficulty unknown

Complete an ingestion evidence sheet and publication recommendation for B-17.

Setup: Synthetic paper case; no commands executed. Previous published P-16 remains available. UTF-8 CSV header customer_id,amount. Six data rows: 1 C101,10; 2 C102,20; 3 [empty],30; 4 C102,40; 5 C105,50; 6 C106,60. Supplied rejection report: row 3 empty key and row 4 duplicate key. Accepted=4, rejected=2. Configuration: header=true, customer_id required. Preview shows C101/10 and C105/50. Mapping log maps source amount to destination customer_name instead of amount. No exclusion agreed. Treat the report as authoritative about which duplicate row was rejected; do not invent duplicate semantics.
Deliverable: One sheet with configuration/mapping findings, row accounting, rejection disposition/rerun plan and publication recommendation with evidence and escalation. Distinguish supplied evidence from proposed repairs.
Restricted rubric:
- Configuration (2): 2: identifies appropriate header/key settings AND wrong amount mapping requiring correction; 1: only one; 0: neither or accepts mapping.
- Reconciliation (2): 2: gives 4+2=6 and says count agreement alone does not authorize release; 1: correct arithmetic without release implication; 0: arithmetic wrong or says totals alone permit release.
- Rejected rows (2): 2: addresses both invalid keys through correction with owner input or explicit agreed exclusion, then rerun/reconcile; 1: fully handles one or omits agreement/rerun; 0: silent exclusion or unchanged retry as repair.
- Release/evidence (2): 2: holds pending corrected mapping/dispositions and representative recheck, retains source/reconciliation and previous version, escalates unresolved discrepancy to data owner; 1: holds with incomplete evidence/rechecks/escalation; 0: recommends publication now.
Evidence-sheet exercise integrates documented checks and action planning; it does not observe software execution.

Reviewer ____; role/expertise ____; conflict ____; date ____; fingerprint ____; accept/revise/reject ____; evidence/comments ____; resolution/authority ____; unresolved ____ .

## NS_A01 / revision 1 / DRAFT
Domain D_A; competencies ['C_A']; tasks ['T_A1']. 1 points; proposed 2 min.
Sources: ACC 1.0: A1 Grant
Apply/analyze documented rules within a scenario. Distinguish adequate evidence from plausible shortcuts; empirical difficulty unknown

An integration must read only orders. Which grant meets the requirement?

A. Workspace reader
B. Dataset orders writer
C. Dataset orders reader
D. Workspace administrator

Key: C
C is narrow enough. A includes all datasets; B grants writes; D grants administration.

Reviewer ____; role/expertise ____; conflict ____; date ____; fingerprint ____; accept/revise/reject ____; evidence/comments ____; resolution/authority ____; unresolved ____ .

## NS_A02 / revision 1 / DRAFT
Domain D_A; competencies ['C_A']; tasks ['T_A2']. 1 points; proposed 2 min.
Sources: ACC 1.0: A2 Verify
Apply/analyze documented rules within a scenario. Distinguish adequate evidence from plausible shortcuts; empirical difficulty unknown

An administrator can read orders. What additional evidence verifies the read-only service account?

A. The administrator fails to write orders.
B. The service identity reads orders, is denied orders write and is denied unrelated customer datasets.
C. The service identity reads orders and has read-only in its name.
D. The administrator confirms the account exists.

Key: B
B follows A2. A tests wrong identity; C omits negative tests; D proves existence only.

Reviewer ____; role/expertise ____; conflict ____; date ____; fingerprint ____; accept/revise/reject ____; evidence/comments ____; resolution/authority ____; unresolved ____ .

## NS_A03 / revision 1 / DRAFT
Domain D_A; competencies ['C_A']; tasks ['T_A3']. 1 points; proposed 2 min.
Sources: ACC 1.0: A3 Compromise
Apply/analyze documented rules within a scenario. Distinguish adequate evidence from plausible shortcuts; empirical difficulty unknown

A service token was disclosed in a shared note. What follows the documented procedure?

A. Revoke the token and obtain authorized replacement; record the incident without the secret.
B. Rename the account and keep using the token.
C. Create a second token and assume the first stopped working.
D. Copy the token into a support ticket for identification.

Key: A
A follows A3. B/C do not invalidate the old token; D spreads the secret.

Reviewer ____; role/expertise ____; conflict ____; date ____; fingerprint ____; accept/revise/reject ____; evidence/comments ____; resolution/authority ____; unresolved ____ .

## NS_A04 / revision 1 / DRAFT
Domain D_A; competencies ['C_A']; tasks ['T_A1', 'T_A2', 'T_A3']. 8 points; proposed 12 min.
Sources: ACC 1.0: A1 Grant; A2 Verify; A3 Compromise
Analyze/evaluate evidence and justify safe next steps. Integrate several conditions; empirical difficulty unknown

Complete an access evidence sheet for svc-orders and a safe remediation sequence.

Setup: Synthetic paper case; no token supplied or changes executed. Requirement read orders only. Current grant workspace reader. Under svc-orders: orders read succeeds, orders write denied, unrelated customer ledger read succeeds. An administrator read also succeeds. A service token was disclosed in a shared note, represented only as TOKEN_REDACTED.
Deliverable: One sheet: grant recommendation, interpretation/recheck plan, token response sequence, credential-free incident/evidence record. Mark proposed actions separately from supplied observations.
Restricted rubric:
- Scope (2): 2: replaces workspace reader with dataset orders reader AND explains unrelated exposure; 1: one only; 0: keeps broad access or grants writer/admin.
- Verification (2): 2: identifies ledger success as failure and specifies service-identity read success/write denial/unrelated denial after remediation; 1: recognizes exposure but rechecks incomplete; 0: accepts administrator test or existing results as sufficient.
- Disclosure (2): 2: revokes disclosed token and gets authorized replacement; 1: only one; 0: rename/add token only or keep using disclosed token.
- Evidence (2): 2: records identity, outcomes and incident/action status without secrets and labels proposed rechecks as proposed; 1: safe record with missing identity/status detail; 0: copies secret or falsely claims remediation happened.
Evidence-sheet exercise integrates documented checks and action planning; it does not observe software execution.

Reviewer ____; role/expertise ____; conflict ____; date ____; fingerprint ____; accept/revise/reject ____; evidence/comments ____; resolution/authority ____; unresolved ____ .

## NS_R01 / revision 1 / DRAFT
Domain D_R; competencies ['C_R']; tasks ['T_R1']. 1 points; proposed 2 min.
Sources: REC 1.0: R1 Restore
Apply/analyze documented rules within a scenario. Distinguish adequate evidence from plausible shortcuts; empirical difficulty unknown

A snapshot is two hours old and no recovery objective is recorded. Where should a rehearsal restore go, and how should age be treated?

A. Overwrite active data and assume two hours is acceptable.
B. Restore separately and accept any snapshot under one day old.
C. Restore into active data after the consultant chooses the objective.
D. Restore into a new namespace and escalate the missing customer-approved objective before claiming acceptable loss.

Key: D
D follows R1. A/C overwrite active data. A/B/C invent authority or acceptable loss windows.

Reviewer ____; role/expertise ____; conflict ____; date ____; fingerprint ____; accept/revise/reject ____; evidence/comments ____; resolution/authority ____; unresolved ____ .

## NS_R02 / revision 1 / DRAFT
Domain D_R; competencies ['C_R']; tasks ['T_R2', 'T_R3']. 1 points; proposed 2 min.
Sources: REC 1.0: R2 Verify; R3 Cut over
Apply/analyze documented rules within a scenario. Distinguish adequate evidence from plausible shortcuts; empirical difficulty unknown

Separate restore counts, representative values and service permissions pass, and age meets the approved objective. What remains before redirecting clients?

A. Delete the old namespace.
B. Prepare cutover/rollback recommendation, retain old namespace and obtain customer authorization recording who approved which version.
C. Redirect because verification grants incident command authority.
D. Redirect now and seek authorization afterward.

Key: B
B follows R3. A removes rollback; C invents authority; D reverses authorization sequence.

Reviewer ____; role/expertise ____; conflict ____; date ____; fingerprint ____; accept/revise/reject ____; evidence/comments ____; resolution/authority ____; unresolved ____ .

## NS_R03 / revision 1 / DRAFT
Domain D_R; competencies ['C_R']; tasks ['T_R1', 'T_R2', 'T_R3']. 8 points; proposed 15 min.
Sources: REC 1.0: R1 Restore; R2 Verify; R3 Cut over; ACC 1.0: A2 Verify
Analyze/evaluate evidence and justify safe next steps. Integrate several conditions; empirical difficulty unknown

Complete a recovery evidence sheet and recommendation for R-22.

Setup: Synthetic paper case, no executable lab. Active prod-old remains in service. Immutable S-22 snapshot taken 08:00; decision time 11:00. Customer-approved maximum snapshot age is four hours. Separate restore target rehearsal-new. Manifest count=500; restored=497. Representative IDs/values match supplied manifest examples. Intended service identity reads orders, is denied orders write, but CAN read unrelated customer data. Job status complete. No customer cutover authorization.
Deliverable: One sheet: age/namespace checks, count/value/permission findings, hold/cutover decision and investigation plan, conditional cutover/rollback and authorization record. Separate observed evidence from required rechecks.
Restricted rubric:
- Starting state (2): 2: computes three-hour age within four-hour objective AND confirms separate namespace protects active data; 1: only one; 0: wrong age or proposes overwrite.
- Failures (2): 2: identifies three-row mismatch AND excess service access despite completion/sample match; 1: one failure; 0: accepts restore as verified.
- Recommendation (2): 2: holds cutover for investigation/correction and repeat counts/values/intended-permission tests; 1: holds with incomplete follow-up; 0: cutover despite a failure.
- Authority/rollback (2): 2: retains prod-old, specifies rollback route to retained namespace and requires customer authorization with actor/exact version before redirect; 1: retains old and requires approval but lacks rollback/version detail; 0: deletes old, redirects unapproved or claims incident command.
Evidence-sheet exercise integrates documented checks and action planning; it does not observe software execution.

Reviewer ____; role/expertise ____; conflict ____; date ____; fingerprint ____; accept/revise/reject ____; evidence/comments ____; resolution/authority ____; unresolved ____ .
