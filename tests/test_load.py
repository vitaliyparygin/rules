from pathlib import Path
import re
import pytest
import yaml
from rules.loader import load_classification_rules, load_extraction_rules, load_extraction_rules


def test_load_classification_rules_missing_file():
    with pytest.raises(FileNotFoundError):
        load_classification_rules(Path("does_not_exist.yaml"))

def test_load_empty_yaml(tmp_path):
    file = tmp_path / "broken.yaml"
    file.write_text("")
    file = tmp_path / "empty.yaml"
    file.write_text("", encoding="utf-8")

    with pytest.raises(ValueError, match="empty or invalid YAML"):
        load_extraction_rules(file)


def test_load_invalid_yaml(tmp_path):
    file = tmp_path / "broken.yaml"

    file.write_text(
        """
Invoice:
  filename_patterns:
    - invoice
  content_patterns:
    - abc
    - [unclosed
""",
        encoding="utf-8",
    )

    with pytest.raises(yaml.YAMLError):
        load_classification_rules(file)


def test_extraction_rules_are_loaded_as_regex_lists():
    rules = load_extraction_rules()

    for document_type, field_rules in rules.items():
        for field in field_rules:
            assert isinstance(field.patterns, tuple)

            assert field.patterns, (
                f"{document_type}.{field.name} has no patterns"
            )

            for pattern in field.patterns:
                assert isinstance(pattern, str)

                # дуже важлива перевірка
                assert len(pattern) > 1, (
                    f"{document_type}.{field.name} "
                    f"looks split into characters: {field.patterns!r}"
                )




def test_all_regexes_compile():
    rules = load_extraction_rules()

    for document_type, field_rules in rules.items():
        for field in field_rules:
            for pattern in field.patterns:
                try:
                    re.compile(pattern)
                except re.error as exc:
                    raise AssertionError(
                        f"{document_type}.{field.name}: {pattern!r}\n{exc}"
                    )

def test_customer_rule():
    rules = load_extraction_rules()

    contract = {
        f.name: f
        for f in rules["Contract"]
    }

    assert contract["customer"].patterns == (
        r"client\s*[:\-]?\s*([^\n]+)",
    )