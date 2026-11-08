"""Train/test splitting.

Planned: a grouped split so near-duplicate prompts never appear in both train and
test, which would inflate the scores. The grouping key (candidates: Nemotron
`domain` or `document_type`) is chosen after exploring the data.
"""
