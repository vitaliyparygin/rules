from pathlib import Path

import pytest
import yaml
from rules.loader import load_classification_rules


def test_load_classification_rules_missing_file():
    with pytest.raises(FileNotFoundError):
        load_classification_rules(Path("does_not_exist.yaml"))

def test_load_empty_yaml(tmp_path):
    file = tmp_path / "empty.yaml"
    file.write_text("", encoding="utf-8")

    with pytest.raises(AttributeError):
        load_classification_rules(file)


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