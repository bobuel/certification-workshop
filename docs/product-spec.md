# Certification Workshop

Status: implementation specification, 2026-10-21. This package is an assistant workflow product, not an exam delivery service or an accreditation claim.

## Full promise and journeys

Create a certification from a brief and source materials; continue development across sessions; pilot and launch through existing delivery systems; operate and revise the program. The credential owner controls the claim, program policies, passing standard, publication, and awards. The assistant does substantive drafting, mapping, analysis, reconciliation, and preparation without inventing participants or decisions.

The primary journey starts with no certification. Establish intended audience and performance, draft a charter, develop a task inventory and SME instruments, record actual findings, construct competencies and a blueprint, author items and practical exercises, conduct recorded reviews, assemble a pilot form, analyze supplied results, support standard setting, prepare launch materials, reconcile authorized operational records, and maintain versions. An existing program enters wherever its evidence supports it. A request for one artifact should not trigger every stage.

## Existing capabilities and reuse

- Evidenced: Eventer 0.1.3 local package has routing skills, portable manifests, durable records, local Python helpers, installer, and offline evaluation patterns. Reuse that architecture and adapt its installer with attribution.
- Evidenced: the user's source-based assessment skill supplies source mapping, rationales, cognitive demand, distractor review, and objective coverage. Adapt these to restricted certification content.
- Evidenced: selected historical chats contain JTA, KSA, competency, blueprint, item review, defensibility, and no-LMS credentialing explorations. They are design history, not validated banks or actual studies. See provenance.md.
- Missing by design: external credentials and verified provider integrations. The package uses reviewed file handoffs and existing assistant tools. No new service, database, API account, subscription, or daemon is required. Existing assistant, delivery-provider, and expert costs remain the owner's.

## Architecture and contracts

One coordinating skill plus nine specialist skills share `program.json` in the user's program folder. The installed plugin contains instructions, templates, example synthetic artifacts, and standard-library Python helpers. Keep each program outside the plugin installation. The schema and CLI contracts live in the coordinating skill's references; packaged skills remain usable after a portable skill-only installation.

The assistant edits records and prepares documents; read-only helpers validate, calculate, propose forms, analyze results, and export explicitly chosen audiences. The initializer exclusively creates a new folder. CLI output files use exclusive creation. No helper sends, issues, publishes, deletes user files, or changes live integrations. Program state is not a security boundary; filesystem and harness access still govern access.

Source versions and item revisions are pinned in references. Reviews and decisions apply to exact revisions. Changes require new revisions; keep old program snapshots and exam packages. Do not automatically substitute revised items into historical forms or mix candidate data across forms. Pending external actions with unknown outcomes require readback before retry. Issuance uses a stable candidate/program/version key and a provider receipt, never a guessed successful response.

## Scope and limits

Implemented helper scope: program initialization and structural audit; item-count blueprint allocation; exact constrained form proposals; review packets; form-version-aware descriptive classical item analysis for supplied scored responses; expected-score panel summaries; dependency impact; candidate-guide and restricted-form exports; award reconciliation; resumable status summaries. Helpers do not infer legal compliance, validity, fairness, accreditation, population representativeness, equating, IRT, DIF, or inter-rater agreement from these calculations. Those tasks get a documented study plan and a handoff to suitable expertise/tools when requested.

All lifecycle stages have actionable skills and artifact templates. Live administration, actual SME participation, actual standard setting, candidate studies, and owner acceptance are activities a real program must supply; an illustrative example never satisfies them for a real credential.

## Acceptance and execution

1. Author the package, shared contracts, and lifecycle workflows. Accept when native manifests agree, skills load, relative references resolve, and no local-history transcript or private source is distributed.
2. Implement helpers and run behavioral tests. Accept when malformed references, stale reviews, impossible forms, changed sources, incomplete score data, conflicting awards, and candidate-key leakage are handled; verify calculations against known arithmetic.
3. Run a from-scratch synthetic journey including charter, JTA instruments, competencies, blueprint, bank, reviews, pilot, panel summary, release handoff, operational reconciliation, and a changed-source scenario. Record exact evidence and limitations.
4. Package and test isolated installation and ZIP extraction. Produce a user-readable verification report. Public publishing, live issuance, and global installation are separate from building this package.

Authority: current user instructions > approved program-owner decisions > this specification > helper contract > example artifacts. Examples are synthetic. Later corrections update this specification and affected contracts before release. No parallel code ownership is needed.
