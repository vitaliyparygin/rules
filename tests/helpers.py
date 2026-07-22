from pathlib import Path

from rules.loader import (
    load_classification_rules,
    load_extraction_rules,
    load_question_templates,
)

ROOT = Path(__file__).resolve().parents[1]

RULES = ROOT / "src" / "rules" / "yaml"


def load_template(template: str):
    base = RULES / template

    return (
        load_classification_rules(base / "classification_rules.yaml"),
        load_extraction_rules(base / "extraction_rules.yaml"),
        load_question_templates(base / "question_templates.yaml"),
    )