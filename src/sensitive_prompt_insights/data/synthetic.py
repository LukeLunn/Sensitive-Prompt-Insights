"""Prompt dataset construction.

Planned: turn Nemotron-PII documents into GenAI-style prompts by wrapping each
passage in a prompt template (e.g. "Summarise this for me: ..."), shifting the
labelled PII span offsets by the template prefix length. Map Nemotron's
fine-grained PII labels onto a small set of report categories.

Add benign prompts (no PII), including hard negatives that mention sensitive
topics without containing sensitive data. Each record keeps its source group
and template id so the split can keep near-duplicates together. Sampling uses a
fixed seed so the dataset can be rebuilt exactly.
"""
