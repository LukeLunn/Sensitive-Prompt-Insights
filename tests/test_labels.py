import pytest

from sensitive_prompt_insights.data.labels import (
    LABEL_TO_CATEGORY,
    Category,
    categories_for,
)
from sensitive_prompt_insights.data.load import Span

# Every label in Nemotron-PII (from the EDA label counts). Hard-coded on purpose:
# the test checks the mapping against the data, not against itself.
EXPECTED_LABELS = {
    "account_number", "age", "api_key", "bank_routing_number", "biometric_identifier",
    "blood_type", "certificate_license_number", "city", "company_name", "coordinate",
    "country", "county", "credit_debit_card", "customer_id", "cvv", "date",
    "date_of_birth", "date_time", "device_identifier", "education_level", "email",
    "employee_id", "employment_status", "fax_number", "first_name", "gender",
    "health_plan_beneficiary_number", "http_cookie", "ipv4", "ipv6", "language",
    "last_name", "license_plate", "mac_address", "medical_record_number",
    "national_id", "occupation", "password", "phone_number", "pin", "political_view",
    "postcode", "race_ethnicity", "religious_belief", "sexuality", "ssn",
    "state", "street_address", "swift_bic", "tax_id", "time", "unique_id",
    "url", "user_name", "vehicle_identifier",
}  # fmt: skip


def span(label: str) -> Span:
    """Build a Span where only the label matters."""
    return Span(start=0, end=1, value="x", label=label)


def test_every_label_is_mapped() -> None:
    """The mapping covers exactly the dataset's 55 labels: none missing, none extra."""
    assert (sorted(LABEL_TO_CATEGORY.keys())) == sorted(EXPECTED_LABELS)


def test_empty_list() -> None:
    """No spans means no sensitive categories."""
    assert categories_for([]) == set()


def test_only_not_sensitive_labels() -> None:
    """Labels that aren't sensitive alone (e.g. city, age) give an empty set."""
    spans = [
        span(label)
        for label in [
            "company_name", "date", "time", "date_time", "url", "country", "state",
            "county", "city", "occupation", "language", "education_level",
            "employment_status", "age", "gender",
        ]
    ]  # fmt: skip
    assert categories_for(spans) == set()


def test_duplicate_labels_collapse() -> None:
    """Repeated labels, or labels from the same category, give that category once."""
    spans = [
        span("first_name"),
        span("first_name"),
        span("last_name"),
        span("last_name"),
        span("date_of_birth"),
        span("date_of_birth"),
        span("city"),
        span("city"),
    ]
    assert categories_for(spans) == {Category.IDENTITY}


def test_mixed_categories() -> None:
    """Spans from several categories return all of them, minus NOT_SENSITIVE."""
    spans = [
        span("first_name"),
        span("last_name"),
        span("date_of_birth"),
        span("city"),
        span("account_number"),
        span("cvv"),
        span("password"),
        span("api_key"),
        span("medical_record_number"),
        span("blood_type"),
        span("race_ethnicity"),
        span("religious_belief"),
        span("political_view"),
        span("sexuality"),
        span("company_name"),
    ]
    assert categories_for(spans) == {
        Category.IDENTITY,
        Category.FINANCIAL,
        Category.CREDENTIALS,
        Category.HEALTH,
        Category.PROTECTED_ATTRIBUTE,
    }


def test_unknown_label_raises() -> None:
    """An unmapped label fails loudly instead of being treated as clean."""
    with pytest.raises(KeyError, match="gimli"):
        categories_for([span("gimli")])
