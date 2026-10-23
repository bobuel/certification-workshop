# Harbor Access Guide v2 — fictional, current

1. The dataset reader role has been replaced by dataset-viewer. A viewer also needs an explicit workspace-entry grant. Both grants are necessary for dataset read access. Writers and administrators remain broader than required.
2. Revoking a token immediately invalidates it. Renaming an account or creating another token does not invalidate the old one.
3. Verify a permitted read and denied write in a safe test environment. Record the observed results and retain credential secrecy.
