"""Load Nemotron-PII and convert it to typed pandas DataFrames.

The `datasets` library is untyped, so data is converted to pandas at this boundary
and everything downstream is type-checked.
"""

import ast
from typing import TypedDict

import pandas as pd
from datasets import DatasetDict, load_dataset


class Span(TypedDict):
    """One labelled PII value: `text[start:end] == span["value"]`."""

    start: int
    end: int
    value: str
    label: str


def parse_spans(raw: str) -> list[Span]:
    """Parse a raw spans string into typed spans.

    The source stores spans as a Python-literal string (single quotes, so not
    JSON). `ast.literal_eval` only accepts literals, so unlike `eval` it can't
    run code from downloaded data.
    """
    parsed = ast.literal_eval(raw)
    if not isinstance(parsed, list):
        raise ValueError(f"expected a list of spans, got {type(parsed).__name__}")
    return [
        Span(
            start=int(item["start"]),
            end=int(item["end"]),
            value=str(item["text"]),
            label=str(item["label"]),
        )
        for item in parsed
    ]


def load_nemotron_pii() -> DatasetDict:
    """Download (or load from cache) the raw Nemotron-PII dataset."""
    return load_dataset("nvidia/Nemotron-PII")


def load_nemotron_splits() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Return (train, test) DataFrames with parsed spans.

    The overlapping domain is removed from test so no domain is in both splits.
    """
    ds = load_nemotron_pii()
    train: pd.DataFrame = ds["train"].to_pandas()
    test: pd.DataFrame = ds["test"].to_pandas()
    test = test[test["domain"] != "Insurance"].reset_index(drop=True)
    for df in (train, test):
        df["spans"] = df["spans"].map(parse_spans)
    return train, test
