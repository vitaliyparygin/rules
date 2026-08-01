from rules.loader import load_template
from rules.extraction import extract_metadata


def test_extract_metadata_unknown_document_type():
    result = extract_metadata(
        "Invoice Number: INV-123",
        "unknown-document-type",
    )

    assert result == {}


def test_extract_metadata_extracts_group_and_full_match():
    text = """
    Invoice Number: INV-123
    Total: 1500 USD
    """

    # Реальні extraction rules можуть відрізнятися між templates,
    # тому тут підміняємо module-level rules для ізольованого тесту.
    from rules import extraction

    class Field:
        def __init__(self, name, patterns):
            self.name = name
            self.patterns = patterns

    original_rules = extraction._RULES

    extraction._RULES = {
        "invoice": [
            Field("invoice_number", [r"Invoice Number:\s*(INV-\d+)"]),
            Field("total", [r"Total:\s*1500 USD"]),
        ]
    }

    try:
        result = extraction.extract_metadata(text, "invoice")

        assert result == {
            "invoice_number": "INV-123",
            "total": "Total: 1500 USD",
        }
    finally:
        extraction._RULES = original_rules


def test_extract_metadata_skips_unmatched_pattern_and_uses_next_pattern():
    from rules import extraction

    class Field:
        def __init__(self, name, patterns):
            self.name = name
            self.patterns = patterns

    original_rules = extraction._RULES

    extraction._RULES = {
        "invoice": [
            Field(
                "invoice_number",
                [
                    r"Missing:\s*(INV-\d+)",
                    r"Invoice Number:\s*(INV-\d+)",
                ],
            )
        ]
    }

    try:
        result = extraction.extract_metadata(
            "Invoice Number: INV-456",
            "invoice",
        )

        assert result == {
            "invoice_number": "INV-456",
        }
    finally:
        extraction._RULES = original_rules


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

