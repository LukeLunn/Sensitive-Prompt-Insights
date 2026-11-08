import ast
from collections import Counter

import pandas as pd

from sensitive_prompt_insights.data.load import DatasetDict, load_nemotron_pii

if __name__ == "__main__":
    ds = load_nemotron_pii()

    # General prints and looking at the data
    def data_view_prints(dataDict: DatasetDict) -> None:
        # load the dataset and print some of its features
        print(dataDict)
        print(dataDict["train"].features)

        # print the first row of the training set
        row = dataDict["train"][0]
        # text_tagged is the string of text along with the spans
        # so the text and the PII highlight are next to one another
        print(row["text_tagged"][:300])
        # spans are the type, value, and location of the PII in the
        # text
        spans = ast.literal_eval(row["spans"])

        # so let's print out some of the spans and their associated
        # text values
        for s in spans[:5]:
            print(s["label"], repr(row["text"][s["start"] : s["end"]]))

    # What about text with no spans in, or rows with no text?
    def check_for_missing_values(dataDict: DatasetDict) -> pd.DataFrame:
        # convert to a dataframe and look for missing values
        df = pd.DataFrame(dataDict)
        print("List of number of NAs per column")
        print(df.isna().sum())
        print("Num text fields containing an empty string")
        print((df["text"] == "").sum())

        df["num_spans"] = df["spans"].apply(lambda x: len(ast.literal_eval(x)))
        print("Num rows with no spans")
        print((df["num_spans"] == 0).sum())
        print("Min, Med, Max number of spans per row")
        print(df["num_spans"].describe())

        return df

    def count_label_types_in_span(df: pd.DataFrame) -> Counter:
        label_counts = Counter(
            span["label"] for spans in df["spans"] for span in ast.literal_eval(spans)
        )
        return label_counts

    def check_domain_and_document_type(df: pd.DataFrame) -> None:
        domain_counts = Counter(df["domain"])
        document_type_counts = Counter(df["document_type"])
        print("Domain counts:")
        print(domain_counts)
        print("Document type counts:")
        print(document_type_counts)

    # data_view_prints(ds)
    df_train = check_for_missing_values(ds["train"])
    df_test = check_for_missing_values(ds["test"])
    # label_counts_train = count_label_types_in_span(df_train)
    # label_counts_test = count_label_types_in_span(df_test)
    # for label, val in label_counts_train.most_common():
    #     print(f"Train - {label}: {val}")
    # for label, val in label_counts_test.most_common():
    #     print(f"Test - {label}: {val}")
    check_domain_and_document_type(df_train)
    check_domain_and_document_type(df_test)
