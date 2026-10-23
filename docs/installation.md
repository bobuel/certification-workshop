# Installation and portability

Final 1.0.0 was installed and reported enabled by the native Codex CLI in a disposable profile; its copied helper initialized and validated a new program. All 28 runtime files match the candidate that passed native model discovery/create/resume. See the [final installation receipt](../evals/reports/native-codex-1.0.0.json). Verified scope: Windows/Python 3.11 and the recorded Codex CLI; other host/platform combinations are unverified.

## What has been implemented

The package uses Eventer's portable distribution pattern: root `plugin.json`, `.codex-plugin/plugin.json`, `.claude-plugin/plugin.json`, `skills/`, icon, local marketplace catalogs, and a portable collection installer. The manifests share one identity and version. [Official OpenAI packaging guidance](https://developers.openai.com/plugins/build/plugins) was checked on 2026-10-21.

## Install from GitHub

In your terminal, using your existing Codex CLI:

```sh
codex plugin marketplace add bobuel/certification-workshop
codex plugin add certification-workshop@certification-workshop
codex plugin list --marketplace certification-workshop
```

Start a fresh conversation and ask to use Certification Workshop. Save new
programs outside the installed plugin directory. Installation does not create a
program or publish anything.

Claude Code users can use the included catalog with these commands inside Claude
Code; this host's activation has not been tested for this release:

```text
/plugin marketplace add bobuel/certification-workshop
/plugin install certification-workshop@certification-workshop
```

For other assistants supporting Agent Skills, use the portable installer below.
GitHub distribution is separate from inclusion in a curated plugin directory.

## Portable skill collection

Run `python scripts/install.py --destination PATH` to preview all writes. Choose the skills directory that your existing harness uses. Add `--apply` to install. The collection includes all ten skills and their shared relative references, templates and helper, so a skill-only installation remains self-contained.

Run the same command to update a managed collection. It refuses changes if an installed file was edited locally, and refuses to merge with an unowned same-name skill. Uninstall uses `--uninstall --apply`, requires the install marker, and refuses locally modified/unowned files. Back up and deliberately resolve modifications first. Do not put program files inside installed skills.

This workflow has been tested in a disposable skills directory, including invoking the copied helper, updating, protecting a local edit, and uninstalling the managed files. It does not mean this user's global installation was changed.

## Native plugin hosts

For Codex, the package has a repository-scoped catalog at `.agents/plugins/marketplace.json` referring to the package root. To add it to an existing personal/team catalog, preserve the existing catalog entries and use the host's documented local-source workflow. The catalog must point to this package folder relative to the marketplace root. A restart/refresh may be required. Do not overwrite an existing user catalog to install this package.

The following local-source commands were exercised with Codex CLI 0.163.0-alpha.10.2 on Windows using a disposable profile:

```powershell
codex plugin marketplace add "C:\path\to\certification-workshop" --json
codex plugin add certification-workshop@certification-workshop --json
codex plugin list --marketplace certification-workshop --json
```

The original readback reported version 0.1.2 installed and enabled, and the cached helper initialized a new program. The 1.0.0-rc.1 pass repeated native installation in a disposable profile and exercised discovery, creation and fresh-session continuation using its exact installed cache. Normal configuration stayed unchanged; activation was session-only. See the [candidate receipt](../evals/reports/native-codex-1.0.0-rc.1.json) for setup assistance and the bounded three-item test. Run these commands in your normal profile only when you intend to install there.

For Claude Code, the package includes the usual `.claude-plugin` identity and local catalog. Use the host's installed plugin manager and current local-source instructions. No Claude account/config was changed during this build.

Native desktop UI discovery remains separate from the observed CLI skill-selection test. Once activated, use a fresh chat and ask it to create a new certification from source material; verify it loads the coordination and setup skills and creates its program outside the installation.

## Distribution

`python scripts/package.py` builds a reproducible allowlisted ZIP and checksum. It excludes development caches, work folders and Git state. Do not place real program data in `examples/`; that folder is distributed. Directory publication may require publisher metadata and verification beyond this local package; no submission has been made.
