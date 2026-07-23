from pathlib import Path

from rules.loader import (
    load_template
)

ROOT = Path(__file__).resolve().parent.parent / "src" / "rules" / "yaml"


def test_document_types_are_consistent():
    for template in ("erp", "legal", "medical"):
        definition = load_template(template)

        classification = definition.classification_rules
        extraction = definition.extraction_rules
        questions = definition.question_templates

        classification_types = {
            rule.document_type
            for rule in classification
        }

        assert classification_types == set(extraction)
        assert classification_types == set(questions)

def test_question_fields_exist_in_extraction_rules():
    for template in ("erp", "legal", "medical"):
        definition = load_template(template)

        extraction = definition.extraction_rules
        questions = definition.question_templates

        for document_type, specs in questions.items():

            extraction_fields = {
                field.name
                for field in extraction[document_type]
            }

            for spec in specs:
                for field in spec.fields:
                    assert field.name in extraction_fields

def test_no_duplicate_question_keys():
    for template in ("erp", "legal", "medical"):
        definition = load_template(template)

        questions = definition.question_templates
        for document_type, specs in questions.items():
            keys = [spec.key for spec in specs]
            assert len(keys) == len(set(keys)), (
                f"{template}/{document_type}: duplicate question keys"
            )