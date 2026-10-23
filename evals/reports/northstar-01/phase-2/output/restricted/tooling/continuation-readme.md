# Reproduce historical calculations

Run from the result directory with Python 3.10+; no network or service is needed:

```text
python restricted/tooling/scripts/certification.py validate --program restricted/history/product-1.0-pilot/program.json
python restricted/tooling/scripts/certification.py analyze --program restricted/history/product-1.0-pilot/program.json --form PILOT1 --csv restricted/data/pilot-complete-cases.csv
python restricted/tooling/scripts/certification.py panel-summary --program restricted/history/product-1.0-pilot/program.json --form PILOT1 --csv restricted/history/product-1.0-pilot/panel-judgments.csv
python restricted/tooling/scripts/certification.py validate --program program.json
python restricted/tooling/scripts/certification.py check-form --program program.json --form PILOT2
```

The last command is expected to fail because revised items lack approval and acceptance. Historical source files resolve relative to the historical snapshot; current sources resolve relative to result. Do not analyze the historical matrix against program.json. Helpers print to stdout by default; --out accepts only a new output path.

prepare.py, revise.py and finalize.py are retained as construction provenance, not general migration commands. They assume this evaluation workspace layout and initial state and must not be rerun over the delivered result. The commands above are the supported self-contained reproduction path. Historical drafts and earlier validation files remain unchanged in the named pre-change archive; final-v2 files describe the current form.
