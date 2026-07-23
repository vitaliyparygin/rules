from rules.loader import load_template

def test_classification_rules_have_patterns():
    for template in ("erp", "legal", "medical"):
        definition = load_template(template)

        classification = definition.classification_rules

        for rule in classification:
            assert rule.filename_patterns
            assert rule.content_patterns