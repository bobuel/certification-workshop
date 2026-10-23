# Worked scoring examples

These responses and ratings are authored illustrations, not candidate submissions or observed rater agreement. Criterion order matches the current review packet. Give one point only when the whole stated criterion is met and not contradicted. Do not infer unstated actions. Flag unsafe recommendations separately; no hidden whole-test fail rule applies.

## NS_I05@2 — complete

Use header=true and required customer_id. Correct amount-to-customer_name to amount-to-amount. Account for 4+2=6. Resolve row 3 and row 4 by owner-supported correction or explicitly agreed exclusion. Rerun/reconcile and recheck mappings and representative values. Hold publication until resolved; count agreement alone is insufficient. Retain source/reconciliation and P-16. Escalate unresolved discrepancies to the customer data owner. These are proposed actions, not completed repairs.

Illustrative criterion points: [1, 1, 1, 1, 1, 1, 1, 1]. Total: **8/8**. Unsafe recommendation flag: False.

## NS_I05@2 — partial

The header and required-key settings are right. Map amount to amount instead of customer_name. Four accepted and two rejected account for six rows. Hold publication; this count does not itself allow release.

Illustrative criterion points: [1, 1, 1, 0, 0, 1, 0, 0]. Total: **4/8**. Unsafe recommendation flag: False.

## NS_I05@2 — unsafe

Keep header=true and required customer_id. Four accepted plus two rejected equals six. Publish the accepted rows now, silently omit both rejections and delete the source evidence.

Illustrative criterion points: [1, 0, 1, 0, 0, 0, 0, 0]. Total: **2/8**. Unsafe recommendation flag: True.

## NS_A04@4 — complete

Remove workspace reader; use workspace traverse and orders query. Traverse alone cannot read and query alone cannot navigate. Ledger read success violates orders-only access. After changes, test as svc-orders: orders read succeeds, orders write denied, unrelated reads denied. Revoke the disclosed token and obtain an authorized replacement before reuse. Record svc-orders, current read/write/ledger outcomes and the incident/action status without secrets. Current broad-grant tests are observations; changes and retests are proposed and have not occurred.

Illustrative criterion points: [1, 1, 1, 1, 1, 1, 1, 1]. Total: **8/8**. Unsafe recommendation flag: False.

## NS_A04@4 — partial

Remove workspace reader and use workspace traverse plus orders query. Ledger read success shows excessive access. Revoke the disclosed token and obtain an authorized replacement before reuse.

Illustrative criterion points: [1, 0, 1, 0, 1, 1, 0, 0]. Total: **4/8**. Unsafe recommendation flag: False.

## NS_A04@4 — unsafe

Keep workspace reader; the administrator read proves the service is verified. Add a new token and continue using the disclosed one. No follow-up is needed.

Illustrative criterion points: [0, 0, 0, 0, 0, 0, 0, 0]. Total: **0/8**. Unsafe recommendation flag: True.

## NS_R03@3 — complete

S-22 is three hours old at 11:00, within the approved four-hour objective. Use rehearsal-new and leave prod-old active. The 500/497 difference leaves three rows missing; unrelated customer-data access is also a failure. Hold cutover despite job completion and sample matches. Investigate/correct both failures, then repeat counts, representative values and service-permission tests. Retain prod-old and roll back by redirecting clients to it if an authorized cutover needs reversal. Require customer approval recording actor and exact version before redirection; I do not assume incident command.

Illustrative criterion points: [1, 1, 1, 1, 1, 1, 1, 1]. Total: **8/8**. Unsafe recommendation flag: False.

## NS_R03@3 — partial

The snapshot is three hours old, within the four-hour objective. Keep rehearsal-new separate from active prod-old. Three rows are missing and unrelated-data access is excessive. Hold cutover until these problems are resolved.

Illustrative criterion points: [1, 1, 1, 1, 1, 0, 0, 0]. Total: **5/8**. Unsafe recommendation flag: False.

## NS_R03@3 — unsafe

The snapshot is three hours old within the four-hour objective. Use rehearsal-new and keep prod-old active for now. The completed job and sample values are enough: redirect clients immediately without customer approval, then delete prod-old.

Illustrative criterion points: [1, 1, 0, 0, 0, 0, 0, 0]. Total: **2/8**. Unsafe recommendation flag: True.

For a real calibration, hide these expected ratings for the first independent scoring round, retain each rater's points and rationale, compare disagreements criterion by criterion, and revise ambiguous instructions before the next round. Do not count author ratings as independent agreement.
