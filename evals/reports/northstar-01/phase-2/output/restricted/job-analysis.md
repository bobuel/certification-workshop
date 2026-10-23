> Historical product-1.0 development document, retained for context. Current product-2.0 definition is ../program.json; current changes and review requests are change-impact-review.md and review-packet-v2.json; current release position is ../release-recommendation.md. Earlier pending-state claims are superseded only as documented there.

# Job-analysis synthesis — draft, synthetic evidence only

Question: what bounded implementation work must an entry-level independent consultant perform safely using references? This is a document-derived model informed by one fictional workshop, not a completed representative job analysis.

The 2026-10-01 workshop has three convenience-selected participants: Ana (partner implementer, 18 deployments), Ben (support) and Chi (partner manager). Morgan asked for a draft. No survey was administered: survey respondent count zero; structured ratings/missingness unavailable. Three workshop participants are not three completed survey responses. All observations are synthetic.

Ana reports correction in 4 of her last 18 first imports and about half her implementation time in ingestion. This supports substantial coverage, not a population error rate. Ben's six support access tickets are explicitly not incidence data; cross-customer exposure motivates consequence-based coverage. Chi identifies recovery rehearsal and authorized recommendation as distinguishing competence. Ana warns three long labs plus questions could exceed 75 minutes; no timing was measured.

Preserved disagreement: Chi initially proposed equal module weights; Ana 50/25/25 based on time; Ben stronger access coverage based on consequences. Proposed 42/33/25 item weights balance these views, pending owner and follow-up review. No universal frequency-times-importance formula is supported.

All tasks below are hypotheses, not validated tasks or item approvals. Conditions: product 1.0 procedures available; bounded customer implementation; consultant prepares evidence and executes only authorized steps.

|Task|Action and observable outcome|Enabling knowledge/skill|Source/version/locator|Competency and items|
|---|---|---|---|---|
|T_I1|Configure CSV header/key mapping and explain invalid rows|Header and required/duplicate-key rules|ING 1.0 I1|C_I; NS_I01, NS_I05|
|T_I2|Account for every row and document correction or agreed exclusion|Reconciliation and rejection review|ING 1.0 I2,I4|C_I; NS_I02, NS_I03, NS_I05|
|T_I3|Check mappings/values; retain evidence; hold/escalate discrepancies|Preview and release boundaries|ING 1.0 I3|C_I; NS_I03, NS_I04, NS_I05|
|T_A1|Select narrow orders read permission|Scope of grants|ACC 1.0 A1|C_A; NS_A01, NS_A04|
|T_A2|Verify allowed read and denied write/unrelated access as service identity|Positive/negative testing|ACC 1.0 A2|C_A; NS_A02, NS_A04|
|T_A3|Revoke disclosed token and use authorized replacement without exposing secret|Credential lifecycle and safe records|ACC 1.0 A3|C_A; NS_A03, NS_A04|
|T_R1|Restore separately and compare age to approved objective, escalating absence|Snapshot age and authority|REC 1.0 R1|C_R; NS_R01, NS_R03|
|T_R2|Check counts/values/permissions and identify cutover blockers|Restore evidence interpretation|REC 1.0 R2|C_R; NS_R02, NS_R03|
|T_R3|Retain old namespace and plan rollback plus version-bound customer approval|Cutover and role boundaries|REC 1.0 R3|C_R; NS_R02, NS_R03|

Competencies C_I/C_A/C_R group related observed work into ingestion, safe access and recovery. Proposed target anchor: independently apply the bounded procedure, retain adequate evidence and escalate unresolved failure/authority. Below target: overlooks a blocker or substitutes appearance of success for verification. Above-scope architecture/incident command is not inferred from high scores. These anchors are unvalidated.

Retain all nine tasks because each has direct procedural support and a relevant consequence. Exclude architecture, incident command and commercial management by the brief, not by low ratings. Missing perspectives include additional deployment types, newer consultants, customer data owners and accessible delivery needs. No saturation, representative coverage or subgroup conclusions. Follow-up may change scope, independence boundaries and weighting. Preserve minority safety concerns rather than averaging them away.
