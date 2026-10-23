from pathlib import Path
import json, hashlib, subprocess, sys, csv, statistics, shutil
root=Path(__file__).resolve().parent; r=root/'result'
def write(path,data): path.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
p=json.loads((r/'program.json').read_text())
packet=json.loads((r/'restricted/review-packet-v2.json').read_text())
print(packet['item_fingerprints'])
p['forms']=[{'id':'PILOT2','revision':1,'blueprint_revision':2,'status':'draft','item_refs':[{'item_id':i['id'],'revision':i['revision'],'item_fingerprint':packet['item_fingerprints'][i['id']]} for i in p['items']]}]
write(r/'program.json',p)
helper=root/'skills/certification-workshop/scripts/certification.py'
for command,extra,name in [('validate',[],'validate'),('status',[],'status'),('check-form',['--form','PILOT2'],'check-form'),('assemble',['--form','PILOT2_REVIEWED'],'assemble')]:
    c=subprocess.run([sys.executable,str(helper),command,'--program',str(r/'program.json'),*extra,'--out',str(r/f'restricted/validation/final-v2-{name}.json')],capture_output=True,text=True)
    print(command,c.returncode,c.stdout[:450],c.stderr)
    assert c.returncode== (1 if command in ['check-form','assemble'] else 0)
guide='''# Northstar Partner Implementation — product 2.0 draft guide

Fictional development program. No launch, registration, passing score or credential award is approved. The historical product-1.0 pilot was synthetic and does not establish 2.0 competence.

The intended audience is partner implementation consultants. The proposed assessment covers preparation and verification of bounded deployments using procedures, recognition of failures and safe escalation. Architecture, production incident command and commercial project management are excluded. Course completion alone is not evidence of competence.

Proposed delivery uses the existing LMS and written evidence sheets: twelve tasks, nine selected-response questions and three practicals, one practical in each domain. Ingestion and verification has five tasks (42% item target), safe service access four (33%), and recovery/authorized cutover three (25%). Rounding produces those counts. Each selected-response item is worth one point and each practical up to eight, maximum 33; score weights differ from item weights. Written practicals assess reasoning and evidence planning, not observed software execution.

The proposed duration is 70 minutes including instructions and review, subject to evidence and accommodations. Proposed permitted resources are the supplied product-2.0 access reference, unchanged ingestion/recovery procedures and personal notes. The individual-work rule excluding outside or generative assistance requires owner confirmation. The final resource packet and version will be identified before any authorized attempt.

Proposed eligibility is volunteer partner consultants with implementation exposure. Dates, eligibility, registration and contact channel remain unapproved; submit nothing until an authorized channel is provided. Use fictional material and never customer data or credentials.

There is no approved passing or award rule, including 80%. Developmental feedback timing and omission/interruption handling must be confirmed before a new pilot. Historical performance will not be automatically converted into product-2.0 pass/fail results.

Request accessible formats or timing support privately from Morgan Lee (fictional owner) before scheduling; contact route and final process remain pending. Raise item, scoring or technical concerns privately; appeal deadlines and independent reviewer remain undecided. Retake, credential duration and renewal policies are pending. No credentials have been issued.

Consent, restricted storage/access, separate identity mapping and retention arrangements require confirmation before collection. This is candidate-facing draft guidance, not a public announcement.
'''
(r/'public/candidate-guide.md').write_text(guide,encoding='utf-8')
# Keep superseded current-path supporting prose clearly historical, with explicit current entry points.
for name in ['charter.md','job-analysis.md','blueprint-rationale.md','reference-templates.md','pilot-protocol.md','reviewer-packet.md']:
    path=r/'restricted'/name
    original=path.read_text(encoding='utf-8-sig')
    path.write_text('> Historical product-1.0 development document, retained for context. Current product-2.0 definition is ../program.json; current changes and review requests are change-impact-review.md and review-packet-v2.json; current release position is ../release-recommendation.md. Earlier pending-state claims are superseded only as documented there.\n\n'+original,encoding='utf-8')
decision='''# Decision register — continuation for product 2.0

All case evidence is synthetic. No launch, cut-score, issuance or revised-item acceptance decision has occurred. program.json decisions remains empty. Previous DEC01–09 and rationale remain preserved in history/pre-2.0-draft/restricted/decision-register.md; those unresolved policy issues remain pending.

Confirmed authority from the current request: analyze complete cases and document the unavailable missing attempt; draft 2.0 content/recommendation; preserve inputs; use existing LMS/evidence sheets; no external actions or services. The supplied simulation receipt records only synthetic acceptance of exact 1.0 items and a synthetic 24-person pilot. It does not resolve the real release gates.

|ID|Decision or evidence|Owner|State|
|---|---|---|---|
|CONT01|Exclude SYN_24 with unavailable NS_A01@1; do not impute|Owner via supplied request|Authorized and implemented; exclusions.json records row and reason|
|CONT02|Announce 80%|Partner manager asks; Morgan decides|Not authorized; recommendation is do not announce. No alternative cut approved|
|CONT03|Accept combined-grant 2.0 revisions and current source mappings|Named content reviewers, assigned by Morgan|Pending; five revision-2 draft items require fresh exact-fingerprint verdicts|
|CONT04|Authorize a later low-stakes 2.0 pilot and assign capacity|Morgan|Pending; no launch inferred from tomorrow's recommendation deadline|
|CONT05|Choose standard-setting procedure, rounding, compensation/critical-error rules and final cut|Morgan after panel/evidence review|Pending; 19.8/33 round-one mean is arithmetic only|
|CONT06|Adopt transition and candidate policies|Morgan|Pending; recommend historical-only 1.0, separate 2.0 evidence, no retroactive awards|

Future decisions need actual actor/date, rationale, exact revision and target fingerprint from final-v2-status.json, plus accessible evidence. Hashes do not confer authority. Program, blueprint, form, policy and release changes require current decisions; synthetic review cannot satisfy live readiness.
'''
(r/'restricted/decision-register.md').write_text(decision,encoding='utf-8')
summary='''# Northstar continuation — handoff

Recommendation: hold product-2.0 credential launch and any passing-score announcement. Deliver revised content for review tomorrow and seek owner authority for a later low-stakes pilot. No external actions or new services occurred.

Current working record: program.json (RESTRICTED), product 2.0, NS_IMPLEMENTER revision 2, NS_BP revision 2, proposed PILOT2 revision 1. All are draft. Five affected items are revision 2 with no carried reviews or scores. Seven unchanged revision-1 items retain only supplied synthetic acceptance. All data, judges and receipts are synthetic; none proves real review or competence. Awards and owner decisions remain empty.

Historical PILOT1 revision 1 is preserved at restricted/history/product-1.0-pilot/program.json with its exact source files, fingerprints, raw scores, judgments and simulation receipt. The original resumed package is in restricted/history/pre-2.0-draft/. All supplied inputs, including the untrusted footer, are copied unchanged in restricted/raw-inputs/. Historical snapshot notes predate the simulation receipt; use that receipt to interpret simulated acceptance/administration, without treating it as release approval.

Delivered artifacts:

- pilot-analysis.json: helper analysis of 23 complete historical attempts; mean 18.8261/33, SD 3.6012, alpha −0.6893. restricted/data/ contains the derived matrix, row-level exclusion of SYN_24 and totals. No imputation or pass/fail classification.
- panel-summary.json: helper summary of three round-one synthetic judges, mean 19.8/33 (60%), range 18.15–21.45. Neither 60% nor 80% is an approved cut.
- release-recommendation.md: interpretation, limits, standard-setting decision, transition, owner dependencies and unsent partner response.
- restricted/change-impact-review.md and review-packet-v2.json: semantic source comparison and exact revised prompts, keys, rubrics and fingerprints. These are restricted.
- public/candidate-guide.md and candidate-guide-v2.json: product-2.0 public-audience drafts, reviewed to exclude bank content and candidate-level data.
- restricted/decision-register.md: authority, unresolved policy decisions and next owner action.
- restricted/tooling/ and restricted/validation/: self-contained helper/contracts and current/historical checks; package-verification.json and inventory-v2.json provide preservation/readback evidence.

Verification: historical structure and PILOT1 development form checks pass. Both helper analyses use only that historical form and share its fingerprint. Current structure passes; development coverage has four access-item and one recovery-practical shortfalls. Final PILOT2 check and attempted assembly correctly fail pending fresh review. Those failures are release blockers, not hidden errors. The proposed form still explicitly includes one practical per domain. No LMS import, provider readback, actual rater agreement, accessibility user test, real pilot or validity study occurred.

Next action: Morgan assigns reviewers and rater/delivery capacity and decides whether to authorize a later low-stakes 2.0 pilot after fresh item acceptance and LMS/sheet verification. Analyst investigates the historical negative associations; panel reviews stable revised content before an owner-approved passing rule. No equating, score transfer, retrospective award or recertification mandate is supported. Historical-only 1.0 and separate 2.0 evidence are recommended; no existing credential holders need transition because none were issued.

Resume with release-recommendation.md, restricted/decision-register.md, program.json and restricted/change-impact-review.md. Old named reviewer packets/validation files remain historical; use the v2/final-v2 files for current state. Local directory names do not enforce access control; preserve restricted storage practices.
'''
(r/'summary.md').write_text(summary,encoding='utf-8')
# Make continuation procedures reproducible without outside installation.
for name in ['prepare.py','revise.py','finalize.py']:
    shutil.copy2(root/name,r/'restricted/tooling'/name)
