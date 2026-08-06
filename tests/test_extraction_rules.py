from rules.loader import load_template
from rules import extraction
from rules.extraction import extract_metadata

class Field:
    def __init__(self, name, patterns):
        self.name = name
        self.patterns = patterns

def test_extract_metadata_unknown_document_type():
    result = extract_metadata(
        "Invoice Number: INV-123",
        "unknown-document-type",
    )

    assert result == {}



def test_extract_metadata_with_capture_group_and_full_match(monkeypatch):
    monkeypatch.setattr(
        extraction,
        "_RULES",
        {
            "invoice": [
                Field(
                    "invoice_number",
                    [r"Invoice Number:\s*(INV-\d+)"],
                ),
                Field(
                    "total",
                    [r"Total:\s*1500 USD"],
                ),
            ]
        },
    )

    result = extraction.extract_metadata(
        """
        Invoice Number: INV-123
        Total: 1500 USD
        """,
        "invoice",
    )

    assert result == {
        "invoice_number": "INV-123",
        "total": "Total: 1500 USD",
    }


def test_extract_metadata_tries_next_pattern(monkeypatch):
    monkeypatch.setattr(
        extraction,
        "_RULES",
        {
            "invoice": [
                Field(
                    "invoice_number",
                    [
                        r"Missing:\s*(INV-\d+)",
                        r"Invoice Number:\s*(INV-\d+)",
                    ],
                )
            ]
        },
    )

    result = extraction.extract_metadata(
        "Invoice Number: INV-456",
        "invoice",
    )

    assert result == {
        "invoice_number": "INV-456",
    }


def test_every_field_has_regex():
    for template in ("erp", "legal", "medical"):
        definition = load_template(template)

        extraction = definition.extraction_rules

        for document_type, rules in extraction.items():
            for field in rules:
                assert field.patterns

                for pattern in field.patterns:
                    assert pattern.strip(), (
                        f"{template}/{document_type}/{field.name!r}: "
                        f"invalid pattern {pattern!r}"
                    )

