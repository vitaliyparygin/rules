from rules.loader import load_template

def test_question_templates_are_not_empty():
    for template in ("erp", "legal", "medical"):
        _, _, questions = load_template(template)

        for specs in questions.values():
            assert specs
            for spec in specs:
                assert spec.key
                assert spec.query_template
                assert spec.fields
                assert spec.tags