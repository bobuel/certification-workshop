# Northstar access 1.0 (synthetic product documentation)

## A1 Grant
A service account reading dataset orders needs dataset orders reader. Workspace reader includes all datasets and is broader than necessary. Writer and administrator are not appropriate for read-only integration.
## A2 Verify
Use the service identity to demonstrate a successful orders read, denied orders write and denied access to unrelated customer datasets. A successful administrator test does not verify the service identity's permissions. Retain evidence without credentials.
## A3 Compromise
If a token is disclosed, revoke that token and create a replacement through the authorized credential workflow. Renaming the account or creating another token does not invalidate the disclosed token. Record the incident without copying the secret into a ticket or report.
