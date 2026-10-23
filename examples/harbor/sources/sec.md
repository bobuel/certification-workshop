# Harbor Access Guide v1.0 — fictional

1. A dataset reader can read only the named dataset. A dataset writer can modify it. Workspace administrators and owners have broader privileges. Use dataset-specific reader access when only reading is required.
2. Revoking a service-account token immediately invalidates it. Creating another token or changing account metadata does not invalidate an existing token.
3. Verify least privilege through a successful permitted read and a denied write using the designated test workflow. Do not disclose actual tokens in reports.
4. Record the chosen grant, scope, reason and verification results. A plan is not proof that the grant was applied.
