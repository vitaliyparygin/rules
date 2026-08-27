from __future__ import annotations
import yaml
from pathlib import Path
from .models import (QuestionTemplateRule,
                      ClassificationRule,
                     QuestionField,
                     FieldRule,
                     TemplateDefinition, DocumentType)

RULES_DIR = Path(__file__).resolve().parent
_RESOURCE_DIR = Path(__file__).parent / "yaml"

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

    path = path or (RULES_DIR / "yaml" / "field_rules.yaml")

    with path.open("r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)
    if raw is None:
        raise ValueError(
            f"{path} is empty or invalid YAML"
        )
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
    path = path or (RULES_DIR / "yaml/erp" / "classification_rules.yaml")

    with path.open("r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)

    if raw is None:
        raise ValueError(f"{path} is empty or invalid YAML")

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


def load_question_templates(
    path: Path | None = None,
) -> dict[str, list[QuestionTemplateRule]]:
    path = path or (RULES_DIR / "yaml/erp" / "question_templates.yaml")

    with path.open("r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)

    if raw is None:
        raise ValueError(f"{path} is empty or invalid YAML")

    result: dict[str, list[QuestionTemplateRule]] = {}

    for document_type, specs in raw.items():
        result[document_type] = []

        for spec in specs:
            query_template = spec["query_template"]

            if isinstance(query_template, str):
                query_template = (query_template,)
            else:
                query_template = tuple(query_template)

            result[document_type].append(
                QuestionTemplateRule(
                    key=spec["key"],
                    query_template=query_template,
                    fields=tuple(
                        QuestionField(
                            name=field["name"] if isinstance(field, dict) else field,
                            required=field.get("required", False) if isinstance(field,
                                                                                dict) else False,
                            aliases=tuple(field.get("aliases", ())) if isinstance(field,
                                                                                  dict) else (),
                            weight=field.get("weight", 1.0) if isinstance(field, dict) else 1.0,
                        )
                        for field in spec["fields"]
                    ),
                    tags=tuple(spec.get("tags", ())),
                )
            )

    return result




def load_extraction_rules(
    path: Path | None = None,
) -> dict[str, tuple[FieldRule, ...]]:
    path = path or (RULES_DIR / "yaml/erp" / "extraction_rules.yaml")

    with path.open("r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)
    if raw is None:
        raise ValueError(
            f"{path} is empty or invalid YAML"
        )
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

def _load_question_field(raw_field: str | dict) -> QuestionField:
    if isinstance(raw_field, str):
        return QuestionField(name=raw_field)

    if isinstance(raw_field, dict):
        if "name" not in raw_field:
            raise ValueError(
                f"Question field mapping must contain 'name': {raw_field!r}"
            )

        return QuestionField(
            name=raw_field["name"],
            aliases=raw_field.get("aliases", []),
            required=raw_field.get("required", False),
            weight=raw_field.get("weight", 1),
        )

    raise TypeError(
        "Question field must be a string or mapping, "
        f"got {type(raw_field).__name__}"
    )
