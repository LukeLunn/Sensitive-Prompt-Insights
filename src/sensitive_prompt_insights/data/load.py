from datasets import DatasetDict, load_dataset


def load_nemotron_pii() -> DatasetDict:
    ds = load_dataset("nvidia/Nemotron-PII")
    return ds
