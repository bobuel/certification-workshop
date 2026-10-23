# Harbor Access Guide v1 — fictional

1. A dataset reader may read only the named dataset. Writers can modify it; administrators have broad access. Dataset reader alone grants the specified read access.
2. Revoking a token immediately invalidates it. Renaming an account or creating another token does not invalidate the old one.
3. Verify a permitted read and denied write in a safe test environment. Record the observed results and retain credential secrecy.
