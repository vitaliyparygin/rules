from __future__ import annotations
from enum import StrEnum
from dataclasses import dataclass, field

@dataclass(frozen=True)
class FieldRule:
    name: str
    patterns: tuple[str, ...]

class Difficulty(StrEnum):
    """Difficulty tiers for generated benchmark questions."""

    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

@dataclass(frozen=True)
class ClassificationRule:
    """A single rule mapping filename/content signals to a document type.

    Attributes:
        document_type: The label produced when this rule matches.
        filename_patterns: Regex patterns checked against the filename.
        content_patterns: Regex patterns checked against document text.
        content_weight: Relative importance of a content match vs filename.
    """

    document_type: str
    filename_patterns: tuple[str, ...] = field(default_factory=tuple)
    content_patterns: tuple[str, ...] = field(default_factory=tuple)
    content_weight: float = 0.7

@dataclass
class QuestionField:
    name: str
    required: bool = False
    aliases: list[str] = field(default_factory=list)
    weight: int = 1

    def __str__(self) -> str:
        return self.name


@dataclass(frozen=True)
class QuestionTemplateRule:
    key: str
    query_template: tuple[str, ...]
    fields: tuple[QuestionField, ...]
    tags: tuple[str, ...]


@dataclass
class ExtractionField:
    patterns: tuple[str, ...]
    aliases: tuple[str, ...] = ()
    normalize: str | None = None


@dataclass
class ExtractionRuleSet:
    document_type: str
    fields: dict[str, tuple[str, ...]]
