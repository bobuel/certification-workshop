from pathlib import Path
import json, csv, shutil, subprocess, sys, hashlib
root=Path(__file__).resolve().parent
r=root/'result'
def write(path, data):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
# Preserve the entire resumed package before any substantive change.
archive=r/'restricted/history/pre-2.0-draft'
archive.mkdir(parents=True,exist_ok=False)
for p in list(r.iterdir()):
    if p.name=='restricted':
        for q in p.iterdir():
            if q.name!='history':
                dest=archive/'restricted'/q.name
                if q.is_dir(): shutil.copytree(q,dest)
                else: dest.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(q,dest)
    elif p.is_dir(): shutil.copytree(p,archive/p.name)
    else: shutil.copy2(p,archive/p.name)
raw=r/'restricted/raw-inputs'
shutil.copytree(root/'inputs',raw)
shutil.copy2(root/'prompt.txt',raw/'request.txt')
hist=r/'restricted/history/product-1.0-pilot'
shutil.copytree(root/'inputs/historical-evidence',hist)
shutil.copy2(root/'inputs/pilot-snapshot.json',hist/'program.json')
shutil.copy2(root/'inputs/simulation-receipt.md',hist/'simulation-receipt.md')
shutil.copy2(root/'inputs/pilot-scores.csv',hist/'pilot-scores-raw.csv')
shutil.copy2(root/'inputs/panel-judgments.csv',hist/'panel-judgments.csv')
data=r/'restricted/data'
data.mkdir(exist_ok=True)
with (hist/'pilot-scores-raw.csv').open(newline='',encoding='utf-8-sig') as f:
    reader=csv.DictReader(f); headers=reader.fieldnames; rows=list(reader)
excluded=[]; complete=[]
for line,row in enumerate(rows,2):
    missing=[k for k,v in row.items() if v is None or not v.strip()]
    if missing: excluded.append({'candidate_id':row['candidate_id'],'csv_line':line,'missing_fields':missing,'reason':'Unfinished attempt; score unavailable. Owner authorizes complete-case exclusion; no imputation.','original_row':row})
    else: complete.append(row)
assert len(rows)==24 and len(complete)==23 and excluded[0]['candidate_id']=='SYN_24'
with (data/'pilot-complete-cases.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=headers); w.writeheader(); w.writerows(complete)
write(data/'exclusions.json',{'evidence_kind':'synthetic','authority':'restricted/raw-inputs/request.txt','source_rows':24,'included_rows':23,'excluded_rows':1,'imputation':False,'exclusions':excluded,'limitation':'Complete-case findings may be biased by the unfinished attempt and describe only this synthetic cohort.'})
helper=root/'skills/certification-workshop/scripts/certification.py'
def run(args,out):
    p=subprocess.run([sys.executable,str(helper),*args,'--out',str(r/out)],capture_output=True,text=True)
    print(out,p.returncode,p.stdout,p.stderr)
    if p.returncode==2: raise RuntimeError(p.stderr or p.stdout)
run(['validate','--program',str(hist/'program.json')],'restricted/validation/historical-validate.json')
run(['check-form','--program',str(hist/'program.json'),'--form','PILOT1'],'restricted/validation/historical-form.json')
run(['analyze','--program',str(hist/'program.json'),'--form','PILOT1','--csv',str(data/'pilot-complete-cases.csv')],'pilot-analysis.json')
run(['panel-summary','--program',str(hist/'program.json'),'--form','PILOT1','--csv',str(hist/'panel-judgments.csv')],'panel-summary.json')
run(['impact','--program',str(hist/'program.json'),'--source','ACC'],'restricted/validation/access-impact-historical.json')
