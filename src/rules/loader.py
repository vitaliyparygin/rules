from __future__ import annotations
import yaml
from pathlib import Path
from .models import (QuestionTemplateRule,
                      ClassificationRule,
                     QuestionField,
                     FieldRule,
                     TemplateDefinition)


RULES_DIR = Path(__file__).resolve().parent

FIELD_RULES_FILE = RULES_DIR / "yaml/field_rules.yaml"
CLASSIFICATION_RULES_FILE = RULES_DIR / "yaml/classification_rules.yaml"
EXTRACTION_RULES_FILE = RULES_DIR / "yaml/extraction_rules.yaml"
QUESTION_RULES_FILE = RULES_DIR / "yaml/question_rules.yaml"

ROOT = Path(__file__).resolve().parents[1]

RULES = ROOT / "src" / "rules" / "yaml"


def load_template(template: str) -> TemplateDefinition:
    base = RULES_DIR / "yaml" / template

    classification: tuple[ClassificationRule, ...] = ()
    classification_file = base / "classification_rules.yaml"

    if classification_file.exists():
        classification = load_classification_rules(classification_file)

    extraction = {}
    extraction_file = base / "extraction_rules.yaml"

    if extraction_file.exists():
        extraction = load_extraction_rules(extraction_file)

    questions = load_question_templates(base / "question_templates.yaml")

    return TemplateDefinition(
        name=template,
        classification_rules=classification,
        extraction_rules=extraction,
        question_templates=questions,
    )


def load_field_rules(
    path: Path | None = None,
) -> dict[str, tuple[FieldRule, ...]]:

    path = path or FIELD_RULES_FILE

    with path.open("r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)

    result: dict[str, tuple[FieldRule, ...]] = {}

    for document_type, fields in raw.items():
        result[document_type] = tuple(
            FieldRule(
                name=field["name"],
                patterns=tuple(field["patterns"]),
            )
            for field in fields
        )

    return result


def load_classification_rules(
    path: Path | None = None,
) -> tuple[ClassificationRule, ...]:

    path = path or CLASSIFICATION_RULES_FILE

    with path.open("r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)

    result: list[ClassificationRule] = []

    for document_type, rule in raw.items():
        result.append(
            ClassificationRule(
                document_type=document_type,
                filename_patterns=tuple(rule["filename_patterns"]),
                content_patterns=tuple(rule["content_patterns"]),
            )
        )

    return tuple(result)

def load_question_templates(path: Path) -> dict[str, list[QuestionTemplateRule]]:
    with path.open("r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)

    result: dict[str, list[QuestionTemplateRule]] = {}

    for document_type, specs in raw.items():

        result[document_type] = []

        for spec in specs:

            result[document_type].append(
                QuestionTemplateRule(
                    key=spec["key"],
                    query_template=tuple(spec["query_template"]),
                    fields=tuple(
                        QuestionField(name)
                        for name in spec["fields"]
                    ),
                    tags=tuple(spec.get("tags", ())),
                )
            )

    return result


def load_extraction_rules(
    path: Path | None = None,
) -> dict[str, tuple[FieldRule, ...]]:
    path = path or EXTRACTION_RULES_FILE

    with path.open("r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)

    result: dict[str, tuple[FieldRule, ...]] = {}

    for document_type, fields in raw.items():
        result[document_type] = tuple(
            FieldRule(
                name=field_name,
                patterns=tuple(patterns),
            )
            for field_name, patterns in fields.items()
        )

    return result
