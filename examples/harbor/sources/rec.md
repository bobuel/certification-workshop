# Harbor Recovery Guide v1.0 — fictional

1. Snapshots are immutable and cannot be edited or overwritten.
2. Restore a snapshot into a new namespace while preserving the original dataset.
3. Reconcile restored row counts and verify required access before directing clients to the restored dataset.
4. Record snapshot identity, target namespace and verification before cutover. A completed restore is not evidence that verification happened.
