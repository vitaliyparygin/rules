from pathlib import Path

from rules.loader import (
    load_classification_rules,
    load_extraction_rules,
    load_question_templates,
)
from helpers import load_template

ROOT = Path(__file__).resolve().parent.parent / "src" / "rules" / "yaml"


# def _load(template: str):
#     base = ROOT / template
#
#     return (
#         load_classification_rules(base / "classification_rules.yaml"),
#         load_extraction_rules(base / "extraction_rules.yaml"),
#         load_question_templates(base / "question_templates.yaml"),
#     )
#
#
# def test_erp_rules_load():
#     classification, extraction, questions = _load("erp")
#
#     assert classification
#     assert extraction
#     assert questions
#
#
# def test_legal_rules_load():
#     classification, extraction, questions = _load("legal")
#
#     assert classification
#     assert extraction
#     assert questions
#
#
# def test_medical_rules_load():
#     classification, extraction, questions = _load("medical")
#
#     assert classification
#     assert extraction
#     assert questions

def test_document_types_are_consistent():
    for template in ("erp", "legal", "medical"):
        classification, extraction, questions = load_template("medical")
        classification_types = {
            rule.document_type
            for rule in classification
        }

        assert classification_types == set(extraction)
        assert classification_types == set(questions)

def test_question_fields_exist_in_extraction_rules():
    for template in ("erp", "legal", "medical"):
        _, extraction, questions = load_template(template)

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
        _, _, questions = load_template(template)
        for document_type, specs in questions.items():
            keys = [spec.key for spec in specs]
            assert len(keys) == len(set(keys)), (
                f"{template}/{document_type}: duplicate question keys"
            )