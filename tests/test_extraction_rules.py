from helpers import load_template

def test_every_field_has_regex():
    for template in ("erp", "legal", "medical"):
        _, extraction, _ = load_template(template)

        for document_type, rules in extraction.items():
            for field in rules:
                assert field.patterns

                for pattern in field.patterns:
                    assert pattern.strip(), (
                        f"{template}/{document_type}/{field.name!r}: "
                        f"invalid pattern {pattern!r}"
                    )

