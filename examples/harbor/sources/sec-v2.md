# Harbor Access Guide v2.0 — fictional change scenario

The dataset reader role has been replaced by dataset-viewer. A viewer also needs an explicit workspace-entry grant. Writers, administrators and owners are unchanged. Token revocation behavior remains unchanged. The new grant combination must be checked before updating access-control items and candidate guidance.

This is deliberately a semantic change: the old S01 answer no longer states the full access requirement. The impact helper conservatively flags all dependencies on the access guide, including unchanged token content; expert inspection narrows the actual revisions.
