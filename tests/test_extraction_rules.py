from rules.loader import load_template

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

