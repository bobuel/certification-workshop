# Harbor Ingestion Guide v1.0 — fictional

1. CSV imports accept UTF-8 data. `header=true` interprets the first row as column names; `header=false` interprets it as data.
2. Import produces accepted and rejected counts and a rejection report. Before publication, reconcile their sum with the source row count and investigate rejected rows and any discrepancy. Publication remains on hold while unexplained or unresolved required-field errors remain.
3. A row with an empty required customer_id is rejected with a reason; no ID is generated automatically.
4. `preview --limit N` reads the first N accepted rows without changing the dataset. Inspection alone does not replace reconciliation.
