# Discovery workshop, 2026-10-01 (synthetic)

Participants: Ana (partner implementer, 18 deployments), Ben (support specialist), Chi (partner manager). Three convenience-selected participants; no representative survey has been administered.

## Tasks and consequences
Ana: Every deployment begins with mapping customer IDs and checking accepted plus rejected counts. A sample that looks good is not enough. We see imports with duplicate IDs and missing required IDs. In 4 of my last 18 deployments the first import needed correction. I spend about half my implementation time on ingestion and verification.
Ben: Access mistakes are less frequent than ingestion errors, but a broad grant can expose another customer's data. Consultants must verify both the allowed read and denied write, and know when the service token has to be revoked. Last month's support sample had six access tickets, but that is not a population incidence rate.
Chi: Recovery is the differentiator from course completion. Consultants should perform a rehearsal into a separate namespace, show the counts and access checks, and make a reasoned cutover recommendation. They are not on-call incident commanders.
Ana: Three long labs plus many questions will exceed 75 minutes. Evidence-sheet practicals with small supplied datasets might fit. We have not measured timing yet.

## Disagreement to resolve
Chi initially suggested equal domain weights because there are three course modules. Ana proposed 50% ingestion, 25% access, 25% recovery based on time on task. Ben wants access represented strongly because of consequence, not frequency. Morgan requested a draft with rationale for an SME review, not a final validity claim. No participant has seen the eventual item bank. No one approved a passing score.

## Follow-up
Recruit additional experienced partner implementers across deployment types. Ask task frequency, importance/consequence, entry-level independence, conditions and evidence of successful completion. Report sampling limitations and disagreements. This workshop supports drafting hypotheses, not declaring a validated job analysis.
