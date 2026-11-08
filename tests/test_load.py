import pytest

import sensitive_prompt_insights.data.load as load

# debugging: run "uv run pytest tests/test_load.py -s" with Jason replaced with Jasmine
# test should pass as is, but fail with Jasmine
FAKE_SPANS = (
    "[{'start': 3, 'end': 8, 'text': 'Jason', 'label': 'first_name'}, "
    "{'start': 22, 'end': 32, 'text': '1987-05-22', 'label': 'date_of_birth'}]"
)


def test_parse_spans() -> None:
    """
    Test that `parse_spans` correctly parses a raw spans string into typed spans.
    """
    spans = load.parse_spans(FAKE_SPANS)
    assert spans == [
        load.Span(start=3, end=8, value="Jason", label="first_name"),
        load.Span(start=22, end=32, value="1987-05-22", label="date_of_birth"),
    ]


def test_parse_spans_match_with_text() -> None:
    """
    Test that the parsed spans match the text they are supposed to highlight.
    This ensures that the `start` and `end` indices in the spans are correct.
    """
    spans = load.parse_spans(FAKE_SPANS)
    text = "I, Jason, was born on 1987-05-22."
    for span in spans:
        assert text[span["start"] : span["end"]] == span["value"]


def test_parse_spans_empty_list() -> None:
    """
    Test that `parse_spans` correctly handles an empty list of spans.
    """
    assert load.parse_spans("[]") == []


@pytest.mark.parametrize("raw", ["{'start': 3}", "42", "'just a string'"])
def test_parse_spans_rejects_non_list(raw: str) -> None:
    """
    Test that `parse_spans` raises a ValueError for input that parses as a
    literal but is not a list (a dict, a number, a string).
    """
    with pytest.raises(ValueError, match="expected a list"):
        load.parse_spans(raw)


def test_parse_spans_refuses_code() -> None:
    """
    Test that `parse_spans` never executes code from the data.

    `ast.literal_eval` rejects anything that isn't a plain literal, such as a
    function call. This guards against someone swapping in `eval`.
    """
    with pytest.raises(ValueError):
        load.parse_spans("__import__('os').getcwd()")


def test_parse_spans_missing_field_raises() -> None:
    """
    Test that a span missing a required field (here `label`) stops the load
    loudly instead of producing an incomplete Span.
    """
    with pytest.raises(KeyError):
        load.parse_spans("[{'start': 1, 'end': 2, 'text': 'x'}]")
