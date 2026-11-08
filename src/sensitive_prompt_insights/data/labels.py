"""Map Nemotron-PII's 55 span labels to broader report categories.

Span labels are fine-grained (e.g. `ssn`, `tax_id`); reports and the TF-IDF
baseline work at category level. Labels that are not sensitive on their own
(quasi-identifiers such as `city` or `age`) map to NOT_SENSITIVE: they only
become identifying in combination (Sweeney), which is out of scope for v1.
"""

from enum import StrEnum

from sensitive_prompt_insights.data.load import Span


class Category(StrEnum):
    """Report categories. A StrEnum member is also a str, so it prints and
    compares as its value (`Category.CONTACT == "contact"`)."""

    CONTACT = "contact"
    GOVERNMENT_ID = "government_id"
    FINANCIAL = "financial"
    CREDENTIALS = "credentials"
    HEALTH = "health"
    PROTECTED_ATTRIBUTE = "protected_attribute"
    IDENTITY = "identity"
    TECHNICAL_ID = "technical_id"
    NOT_SENSITIVE = "not_sensitive"


LABEL_TO_CATEGORY: dict[str, Category] = {
    # Contact
    "email": Category.CONTACT,
    "phone_number": Category.CONTACT,
    "fax_number": Category.CONTACT,
    "street_address": Category.CONTACT,
    "postcode": Category.CONTACT,
    # Government ID (licence plate: registered to a person via the state)
    "ssn": Category.GOVERNMENT_ID,
    "national_id": Category.GOVERNMENT_ID,
    "tax_id": Category.GOVERNMENT_ID,
    "certificate_license_number": Category.GOVERNMENT_ID,
    "license_plate": Category.GOVERNMENT_ID,
    # Financial
    "account_number": Category.FINANCIAL,
    "credit_debit_card": Category.FINANCIAL,
    "cvv": Category.FINANCIAL,
    "bank_routing_number": Category.FINANCIAL,
    "swift_bic": Category.FINANCIAL,
    # Credentials (PIN here, not Financial: it grants access, like a password)
    "password": Category.CREDENTIALS,
    "api_key": Category.CREDENTIALS,
    "http_cookie": Category.CREDENTIALS,
    "pin": Category.CREDENTIALS,
    # Health
    "medical_record_number": Category.HEALTH,
    "health_plan_beneficiary_number": Category.HEALTH,
    "blood_type": Category.HEALTH,
    "biometric_identifier": Category.HEALTH,
    # Protected attributes (special-category data under GDPR Art. 9)
    "race_ethnicity": Category.PROTECTED_ATTRIBUTE,
    "religious_belief": Category.PROTECTED_ATTRIBUTE,
    "political_view": Category.PROTECTED_ATTRIBUTE,
    "sexuality": Category.PROTECTED_ATTRIBUTE,
    # Identity (date_of_birth here, unlike plain `date`, because it identifies)
    "first_name": Category.IDENTITY,
    "last_name": Category.IDENTITY,
    "date_of_birth": Category.IDENTITY,
    # Technical IDs
    "ipv4": Category.TECHNICAL_ID,
    "ipv6": Category.TECHNICAL_ID,
    "mac_address": Category.TECHNICAL_ID,
    "device_identifier": Category.TECHNICAL_ID,
    "user_name": Category.TECHNICAL_ID,
    "customer_id": Category.TECHNICAL_ID,
    "employee_id": Category.TECHNICAL_ID,
    "unique_id": Category.TECHNICAL_ID,
    "vehicle_identifier": Category.TECHNICAL_ID,
    "coordinate": Category.TECHNICAL_ID,
    # Not sensitive alone (quasi-identifiers and generic values)
    "company_name": Category.NOT_SENSITIVE,
    "date": Category.NOT_SENSITIVE,
    "time": Category.NOT_SENSITIVE,
    "date_time": Category.NOT_SENSITIVE,
    "url": Category.NOT_SENSITIVE,
    "country": Category.NOT_SENSITIVE,
    "state": Category.NOT_SENSITIVE,
    "county": Category.NOT_SENSITIVE,
    "city": Category.NOT_SENSITIVE,
    "occupation": Category.NOT_SENSITIVE,
    "language": Category.NOT_SENSITIVE,
    "education_level": Category.NOT_SENSITIVE,
    "employment_status": Category.NOT_SENSITIVE,
    "age": Category.NOT_SENSITIVE,
    "gender": Category.NOT_SENSITIVE,
}


def categories_for(spans: list[Span]) -> set[Category]:
    """Return the sensitive categories present in a document's spans.

    NOT_SENSITIVE is excluded. Raises KeyError on an unknown label so a new
    label in the data fails loudly instead of being silently dropped.
    """
    return {
        category
        for span in spans
        if (category := LABEL_TO_CATEGORY[span["label"]]) != Category.NOT_SENSITIVE
    }
