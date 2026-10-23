from pathlib import Path
import json, csv, shutil, subprocess, sys, statistics
root=Path(__file__).resolve().parent; r=root/'result'
def write(path,data):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
p=json.loads((r/'restricted/history/product-1.0-pilot/program.json').read_text(encoding='utf-8-sig'))
p['program'].update(revision=2,product_version='2.0',status='draft')
p['blueprint'].update(revision=2,status='draft')
for s in p['sources']:
    if s['id']=='ACC': s['current']=False
p['sources'].append({'id':'ACC','version':'2.0','location':'restricted/evidence/access-v2.md','evidence_kind':'synthetic','current':True})
shutil.copy2(root/'inputs/access-v2.md',r/'restricted/evidence/access-v2.md')
for t in p['tasks']:
    if t['id'].startswith('T_A'):
        t['revision']=2
        t['conditions']='Product 2.0 access procedures available; bounded customer deployment'
        for ref in t['source_refs']: ref['version']='2.0'
        if t['id']=='T_A1':
            t['statement']='Select workspace traverse together with dataset orders query for an orders-only read integration; reject either grant alone and broad workspace reader.'
            t['KSA']='Combined navigation and dataset-specific query grants'
            t['outcome']='Both required narrow grants; no broad read access'
        if t['id']=='T_A3':
            t['source_refs'].append({'source_id':'ACC','version':'1.0','locator':'A3 Compromise (definition expressly retained by 2.0 A3)'})
            # Keep direct current task references eligible; the old behavior is incorporated in the new evidence companion.
            t['source_refs']=t['source_refs'][:1]
affected={'NS_A01','NS_A02','NS_A03','NS_A04','NS_R03'}
for item in p['items']:
    if item['id'] not in affected: continue
    item.update(revision=2,status='draft')
    for ref in item['source_refs']:
        if ref['source_id']=='ACC': ref['version']='2.0'
    if item['id']=='NS_A01':
        item['prompt']='Under Northstar 2.0, an integration must read only orders. Which grant configuration meets the requirement?'
        item['options']={'A':'Workspace traverse only','B':'Dataset orders query only','C':'Workspace traverse and dataset orders query','D':'Workspace reader'}
        item['answer_key']='C'
        item['rationale']='2.0 A1 requires both traverse and dataset-specific query. A cannot read data; B cannot navigate; D grants all datasets and is broader than necessary. The old dataset reader role is removed.'
    if item['id']=='NS_A04':
        item['prompt']='For Northstar 2.0, complete an access evidence sheet for svc-orders and a safe remediation sequence.'
        item['setup']='Synthetic 2.0 paper case; no token supplied or changes executed. Requirement: read orders only. Current grant: workspace reader. A proposed replacement has workspace traverse only and no dataset query grant. Under the CURRENT broad grant, svc-orders orders read succeeds, orders write is denied, unrelated customer ledger read succeeds. An administrator read also succeeds. No tests of the proposed replacement have run. A service token was disclosed in a shared note, represented only as TOKEN_REDACTED.'
        item['deliverable']='One sheet: exact grant replacement and explanation of each required component; interpretation of current results and proposed replacement; service-identity recheck plan; token response sequence; credential-free incident/evidence record. Separate proposed actions from supplied observations.'
        item['rubric'][0]['anchor']='2: removes broad workspace reader and specifies BOTH workspace traverse AND dataset orders query, explains traverse-only cannot read and query-only is insufficient, and identifies unrelated exposure; 1: proposes both narrow grants but omits removal or one explanation; 0: recommends either grant alone, removed dataset reader, broad reader, writer or administrator as sufficient.'
        item['rubric'][1]['anchor']='2: identifies current ledger success as failure and requires service-identity orders read success, orders write denial and unrelated-data denial after BOTH replacement grants; 1: recognizes exposure but rechecks incomplete; 0: accepts administrator test or current results as verification of proposed replacement.'
        item['rationale']='2.0 A1 changes remediation to two jointly necessary grants. A2 verification and A3 revocation/replacement remain required. Paper evidence planning does not demonstrate actual execution.'
p['reviews']=[v for v in p['reviews'] if v['item_id'] not in affected]
for v in p['reviews']: v['evidence_ref']='restricted/history/product-1.0-pilot/simulation-receipt.md'
p['forms']=[]; p['decisions']=[]; p['awards']=[]
p['public']['overview']='Fictional product 2.0 development draft for bounded implementation reasoning. No credential launch or passing rule is approved; the historical 1.0 pilot is synthetic.'
p['public']['permitted_resources']='Proposed: supplied product 2.0 access reference, unchanged ingestion/recovery procedures and personal notes; individual work without outside or generative assistance. Owner confirmation pending.'
p['public']['format']='Proposed 12 tasks: nine selected-response questions and three written evidence-sheet practicals; 70 minutes unvalidated. Existing LMS and evidence sheets. These do not observe actual software execution.'
p['policies']['passing_standard']='UNAPPROVED. Historical round-one expected-score mean is not a passing rule; neither 60% nor 80% is authorized. See release-recommendation.md.'
p['notes']=['All case sources, reviewers, judges and scores are synthetic; no real review, launch or issuance.','Product 1.0 PILOT1 and its exact scores/reviews remain in restricted/history/product-1.0-pilot. Historical snapshot notes predate its simulation receipt; receipt explains later simulated acceptance and pilot.','Five revised item mappings/content are draft revision 2, without carried reviews or scores. Seven unchanged revision-1 items retain only synthetic acceptance.','Current program and blueprint revision 2 are drafts. Intended form PILOT2 is a pinned review proposal, not an assembled approved release.','Item weights 42/33/25 yield 5/4/3; score weights 12/11/10 of 33. No evidence of equating between versions.','program.json, analysis and panel outputs are RESTRICTED; only public/ is candidate-facing draft.']
write(r/'program.json',p)
helper=root/'skills/certification-workshop/scripts/certification.py'
def run(args,out):
    c=subprocess.run([sys.executable,str(helper),*args,'--out',str(r/out)],capture_output=True,text=True)
    print(out,c.returncode,c.stdout[:250],c.stderr)
    if c.returncode==2: raise RuntimeError(c.stderr or c.stdout)
run(['review-packet','--program',str(r/'program.json')],'restricted/review-packet-v2.json')
packet=json.loads((r/'restricted/review-packet-v2.json').read_text())
write(r/'restricted/data/total-score-distribution.json',{'classification':'restricted','evidence_kind':'synthetic','form_id':'PILOT1','n':23,'totals':[{ 'candidate_id':row['candidate_id'],'total':sum(float(v) for k,v in row.items() if k!='candidate_id')} for row in csv.DictReader((r/'restricted/data/pilot-complete-cases.csv').open())]})
run(['validate','--program',str(r/'program.json')],'restricted/validation/current-v2-validate.json')
run(['coverage','--program',str(r/'program.json')],'restricted/validation/current-v2-coverage.json')
run(['status','--program',str(r/'program.json')],'restricted/validation/current-v2-status.json')
run(['export','--program',str(r/'program.json'),'--audience','candidate-guide'],'public/candidate-guide-v2.json')
