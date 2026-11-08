"""Train/test splitting.

Source documents: Nemotron-PII's own split already holds out whole domains, so it
is used as-is, with the one shared domain (`Insurance`) removed from test (see
`load.load_nemotron_splits`). `document_type` was rejected as a grouping key: its
near-duplicates (e.g. "Tax Return" vs "Tax Return Form") would cross the split.

Planned: the prompt dataset is split by template family, so near-duplicate prompts
built from the same template never appear in both train and test.
"""
