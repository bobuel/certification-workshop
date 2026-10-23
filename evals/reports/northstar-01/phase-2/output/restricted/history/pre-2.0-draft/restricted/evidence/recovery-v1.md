# Northstar recovery 1.0 (synthetic product documentation)

## R1 Restore
Snapshots are immutable. Restore into a new namespace; never overwrite the active dataset as a rehearsal. Check snapshot age against the customer-approved recovery objective. If no objective was agreed, escalate that decision rather than inventing an acceptable loss window.
## R2 Verify
Compare restored counts with the snapshot manifest, inspect representative values and verify intended service-account permissions. Restore completion alone is not a cutover decision. A count mismatch or excess access blocks cutover pending investigation.
## R3 Cut over
Prepare a cutover recommendation and rollback route, retain the old namespace, and obtain customer authorization before redirecting clients. Record who authorized which version. The consultant prepares evidence and executes authorized steps; they do not unilaterally command a production incident.
