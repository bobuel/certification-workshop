# Certification Workshop

**Build a certification program, from the first brief to the next product change.**

Certification Workshop helps your AI assistant turn source material and real job
tasks into a certification program. Develop the blueprint, write questions and
practical exercises, work through expert feedback, and prepare for a pilot.
Return to the same saved program when the evidence or the product changes.

It is an open-source plugin with ten skills and local assessment tools. Your
program is saved as files you can read, edit, and take with you. There is no
Certification Workshop account or subscription; you use your existing AI
assistant and tools.

## Get started

**Codex** — run in your terminal:

```sh
codex plugin marketplace add bobuel/certification-workshop
codex plugin add certification-workshop@certification-workshop
```

Then start a new conversation:

> Use Certification Workshop to create a certification for partner implementation
> consultants. Here are our product guides and discovery notes. Develop the
> charter, proposed job tasks, blueprint, and actual assessment drafts for review.

You can start from scratch or bring an existing program. Local tools need
Python 3.10 or newer and use only its standard library. For portable Agent Skills
installation, Claude Code metadata, and tested host support, see the
[installation guide](docs/installation.md).

## From the first brief to a maintained program

Start with who the certification is for, what they need to do, and the material
that supports those tasks. Work through the program's purpose and scope, choose
what to assess, and develop questions, practical tasks, and scoring rubrics.

As reviewers and pilot participants contribute, bring their evidence back:

> Here are the reviewer comments and pilot scores. Reconcile the feedback,
> analyze the exact pilot form, and show what we can conclude and what still
> needs a decision.

The plugin connects sources, items, reviews, and forms so that a revision does
not silently inherit approval for older content. It helps prepare candidate
guidance and delivery handoffs, then supports operational records and updates:

> Our access model changed in version 2. Identify affected questions, revise the
> content, preserve the historical pilot evidence, and prepare a transition plan.

**See what it produces:** the [Northstar example](examples/northstar-v1/CERTIFICATION.md)
includes a charter, blueprint, twelve questions and practical exercises, scoring
rubrics, pilot protocol, and candidate guide. [Worked responses](examples/northstar-v1/scoring-examples.md)
show how the rubrics apply. Northstar is fictional; no credential is offered.

## What it helps with

| Task | Skills |
| --- | --- |
| Start a program or resume saved work | Workshop, Setup |
| Define job tasks and what to assess | Job analysis, Blueprint |
| Develop questions, practical exercises, and rubrics | Items |
| Coordinate feedback and pilot evidence | Review, Pilot |
| Prepare forms, candidate guidance, and delivery handoffs | Launch |
| Reconcile outcomes and handle program changes | Operations, Maintenance |

You can ask generally or name a skill. Install the full collection so every
skill can use the shared records, templates, and tools.

## Working with your tools

Use your existing sources, documents, delivery platform, and connected assistant
tools. Without an integration, the plugin prepares files and handoff materials.
The local helper has no network calls or telemetry. See [privacy](PRIVACY.md).

Experts review content and program owners decide policy and release. The plugin
keeps those decisions attached to the evidence; it does not certify an exam's
validity or issue credentials automatically. Candidate guides exclude answer
keys and restricted assessment records. See the [analysis scope](skills/certification-workshop/references/analysis.md).

## For contributors

```sh
git clone https://github.com/bobuel/certification-workshop.git
cd certification-workshop
python -m unittest discover -s tests -v
python scripts/validate.py
python evals/run.py
python evals/scenarios.py
```

The evaluations follow a real development problem: conflicting source material,
limited reviewer time, a new assessment, pilot evidence, and a product change.
Read the [case and actual outputs](docs/northstar-evaluation.md),
[verification record](docs/verification.md), and
[GitHub Actions results](https://github.com/bobuel/certification-workshop/actions).
Offline checks require no API key or model calls. Native assistant runs are
documented separately from deterministic checks.

Built by [Alex Aidun](https://aydoon.com/), using the portable plugin approach
behind [Eventer](https://github.com/bobuel/eventer-plugin).

[Contributing](CONTRIBUTING.md) ·
[Report an issue](https://github.com/bobuel/certification-workshop/issues) ·
[Security](SECURITY.md) · [MIT license](LICENSE)
