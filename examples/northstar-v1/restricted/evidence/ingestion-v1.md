# Northstar ingestion 1.0 (synthetic product documentation)

## I1 Configure
Imports accept UTF-8 CSV. Set header=true when the first row names fields. Map customer_id as a required key. Empty customer_id and duplicate customer_id rows are rejected with explicit reasons; the system never generates replacement IDs.
## I2 Reconcile
Before publication, account for every source row: accepted + rejected must equal the source row count. Review the rejection report and document correction or an explicitly agreed exclusion. A matching total alone does not authorize publication. Unexplained count differences require investigation. Retrying without correcting input does not repair invalid rows.
## I3 Verify and release
preview --limit N reads accepted rows without changing them. Check the required mappings and representative values as well as counts. Publish only after reconciliation and documented disposition of rejected rows. Retain the source and reconciliation evidence. A failed verification leaves the previous published version available; escalate an unresolved discrepancy to the customer data owner.
## I4 Worked data
An input of 1,000 rows yields 970 accepted, 20 empty-key rejections and 10 duplicate-key rejections. No exclusion has been agreed. Another import reports 990 accepted and 5 rejected from 1,000 rows. Both require a documented decision before publication for different reasons.
