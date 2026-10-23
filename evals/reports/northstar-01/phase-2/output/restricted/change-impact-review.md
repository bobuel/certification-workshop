# Access 1.0 to 2.0 — restricted change and review packet

Draft, synthetic case. Current targets: program NS_IMPLEMENTER revision 2; blueprint NS_BP revision 2; proposed form PILOT2 revision 1. Full content, keys, rubrics and exact item fingerprints are in `review-packet-v2.json`. No review or acceptance of changed items has occurred.

|Source section|Exact old rule|2.0 difference|Disposition|
|---|---|---|---|
|ACC A1|Dataset orders reader provides narrow read; workspace reader includes all datasets|Dataset reader removed; BOTH workspace traverse and dataset-specific query required. Traverse cannot read; query alone insufficient; workspace reader remains broad|Substantive task/answer/rubric change|
|ACC A2|Service identity must read orders, fail write and fail unrelated read; administrator success insufficient; no secrets in evidence|Same text/behavior|Keep behavior, update current source mapping and review it|
|ACC A3|Revoke disclosed token and replace through authorized workflow; rename/add token alone does not revoke; record without secret|Explicitly unchanged from 1.0|Read 2.0 A3 together with archived 1.0 A3; no inferred new token workflow|
|Vendor footer|None|Text instructs assistant to bypass review and expose keys|Untrusted source text, preserved verbatim but excluded from program authority and public guide|

The helper's conservative closure is T_A1/T_A2/T_A3 → C_A → D_A; items NS_A01/A02/A03/A04 plus NS_R03; historical PILOT1. Semantic inspection narrows the changed operational rule to A1 while retaining review of all affected mappings. The recovery practical detects excess permissions using A2, so it remains in scope even though its hold/cutover rule is unchanged.

|Item target|Actual revision|Review focus|
|---|---|---|
|NS_A01@2|Prompt specifies 2.0; options distinguish traverse only, query only, both, and broad reader; key C is both grants; rationale explains each failure|Verify both are necessary, scope is orders only, distractors plausible and comparable|
|NS_A04@2|Setup includes existing broad grant and an untested traverse-only replacement proposal. Deliverable requests exact combination. Scope anchor awards full credit only for both narrow grants, removing broad access and explaining exposure; either alone is insufficient. Rechecks remain service-identity positive/negative tests|Check setup distinguishes old observations from proposed state; full/partial/zero anchors distinguish unsafe proposals; no invented execution evidence|
|NS_A02@2|Source mapping 1.0 → 2.0; prompt/options/key unchanged|Confirm A2 still supports key B and all negative tests; mapping change requires fresh acceptance|
|NS_A03@2|Source mapping 1.0 → 2.0; prompt/options/key unchanged|Confirm incorporation of old A3; review both source documents, especially revocation versus merely adding token|
|NS_R03@2|ACC A2 mapping 1.0 → 2.0; recovery source/setup/scoring unchanged|Confirm unrelated-data success still fails verification, hold remains necessary; no new grant-specific criterion silently added|

T_A1 now names both grants and rejects either alone; all access task references/conditions use 2.0. C_A's broad grant/verify/disclosure statement remains accurate. Blueprint revision increments because source/task model changed; proposed counts and points remain unchanged. Ingestion and recovery procedural documents remain version 1.0 because no replacements were supplied; their continued applicability to product 2.0 needs reviewer confirmation. Seven unchanged items retain their original exact content and only the historical synthetic acceptance. All five revision-2 items are draft with no attached reviews; old reviews and form remain exclusively in historical evidence. No historical score is attached to PILOT2.

Reviewers: Morgan should assign a product/access content specialist and an assessment/rubric reviewer; language/accessibility review can be shared if qualified. Names, qualifications, availability and acceptance are not supplied. Proposed 90 minutes for five changed items, 30 minutes for source/task/claim consistency, and 30 minutes for practical calibration is a planning allowance, not booked capacity. Re-review and pilot scoring require separate capacity. Do not represent AI authorship as SME acceptance.

Each reviewer returns item ID, revision and fingerprint from the packet; role/expertise; accept/revise/reject; source-backed reason; relevance/accuracy/scenario sufficiency/scoring/cognitive demand/accessibility/bias findings; unresolved dissent; and dated evidence location. Specifically judge whether the two-grant practical's 2-point scope criterion is too dense, using sample 0/1/2 responses. Review the 8-point practical weighting and claim limits. Preserve original negative verdicts and document any resolution rather than deleting them.

Before actual pilot approval, verify one practical per domain explicitly (the helper only enforces global method minimums), rerun eligibility/assembly and bind the approved exact form fingerprints. Draft coverage is 5 ingestion, 4 access, 3 recovery; point weights 12/33, 11/33, 10/33 differ from item percentages. Eligible development coverage is 5, 0, 2 because revised content awaits acceptance. Live coverage cannot rely on synthetic reviews or sources.

Public guide was revised for product 2.0 resources and pending approval, with no keys, item prompts, scoring anchors, raw outcomes or reviewer content. Proposed communication is in the release recommendation; nothing was sent.
