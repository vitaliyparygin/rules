from rules.loader import load_template

def test_classification_rules_have_patterns():
    for template in ("erp", "legal", "medical"):
        classification, _, _ = load_template(template)

        for rule in classification.values():
            assert rule.filename_patterns
            assert rule.content_patterns