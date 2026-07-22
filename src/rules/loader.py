from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from .models import (ExtractionField, ExtractionRuleSet, QuestionSpec,
                      ClassificationRule, QuestionField)
import yaml

RULES_DIR = Path(__file__).parent

FIELD_RULES_FILE = RULES_DIR / "yaml/field_rules.yaml"
CLASSIFICATION_RULES_FILE = RULES_DIR / "yaml/classification_rules.yaml"
EXTRACTION_RULES_FILE = RULES_DIR / "yaml/extraction_rules.yaml"
QUESTION_RULES_FILE = RULES_DIR / "yaml/question_rules.yaml"

@dataclass(frozen=True)
class FieldRule:
    name: str
    patterns: tuple[str, ...]


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
) -> dict[str, ClassificationRule]:

    path = path or CLASSIFICATION_RULES_FILE

    with path.open("r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)

    result = []

    for document_type, rule in raw.items():
        result.append(
            ClassificationRule(
                document_type=document_type,
                filename_patterns=tuple(rule["filename_patterns"]),
                content_patterns=tuple(rule["content_patterns"]),
            )
        )

    return result

def load_question_templates(path: Path) -> dict[str, list[QuestionSpec]]:
    with path.open("r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)

    result: dict[str, list[QuestionSpec]] = {}

    for document_type, specs in raw.items():

        result[document_type] = []

        for spec in specs:

            result[document_type].append(
                QuestionSpec(
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
