# Draft proposed job tasks

Document-derived hypotheses only; no SME validation or respondents.

T1 → D1 → Import verification: Reconcile a UTF-8 customer import before publication, verify mappings and representative values, and document rejected-row disposition or escalate unresolved discrepancies. Source: sources/ingestion-v1.md, I1–I4, v1.0. Enabling knowledge: documented checks and release authority; skill: evidence interpretation and safe escalation.

T2 → D2 → Safe access: Configure dataset-scoped service-account read access and verify allowed read, denied write and denied unrelated-data access without retaining credentials. Source: sources/access-v1.md, A1–A3, v1.0. Enabling knowledge: documented checks and release authority; skill: evidence interpretation and safe escalation.

T3 → D3 → Recovery decision: Prepare a recovery evidence sheet from a snapshot in a new namespace, verify integrity and access, and recommend cutover only with an agreed recovery objective and customer authorization. Source: sources/recovery-v1.md, R1–R3, v1.0. Enabling knowledge: documented checks and release authority; skill: evidence interpretation and safe escalation.

Follow-up instrument (draft): select reviewers with recent partner import, access and recovery experience; record role coverage and conflicts, with no assumed recruitment. Ask for each task: Is it in scope? What observable evidence is missing? Rate importance (1 optional, 2 useful, 3 necessary, 4 essential), frequency (never, less than monthly, monthly, weekly/daily), and consequence (1 rework, 2 deployment delay, 3 data/access harm, 4 severe customer impact), with not-applicable/unknown options. Request counterexamples and omitted tasks. Report actual response counts, missingness and disagreements before revising weights; do not multiply ratings into weights automatically.
