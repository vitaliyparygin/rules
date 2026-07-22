from __future__ import annotations
from enum import StrEnum
from dataclasses import dataclass, field
# FieldRule

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
class QuestionSpec:
    """
    Template describing one family of questions.
    """

    key: str
    query_template: list[str]
    fields: tuple[QuestionField, ...]
    difficulty: Difficulty = Difficulty.EASY
    tags: tuple[str, ...] = ()
    max_questions: int | None = None


@dataclass
class ExtractionField:
    patterns: tuple[str, ...]
    aliases: tuple[str, ...] = ()
    normalize: str | None = None


@dataclass
class ExtractionRuleSet:
    document_type: str
    fields: dict[str, tuple[str, ...]]
