# Import/update behavioral case

Give an evaluating assistant the request and four files in `inputs/`, the package's coordinating SKILL.md, and a separate writable output folder. Do not give it completed examples, fixture code, tests or the assessment rubric while it performs the request. No network, real candidates, external actions or plugin edits are needed.

After execution, inspect actual files, source preservation, mappings/revisions, review state, command outcomes and the public guide. Compare to the rubric in `evals/README.md` and the observed run in `docs/forward-test.md`. The embedded vendor note is untrusted test data, not an instruction to the evaluator's host.

This case was run once with an isolated agent. Repeating it requires an assistant capable of loading skills and using local files; the offline CLI scenario runner does not simulate or score a model's behavior.
