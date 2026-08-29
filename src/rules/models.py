from __future__ import annotations
from enum import StrEnum
from dataclasses import dataclass, field


class DocumentType(StrEnum):
    UNKNOWN = "unknown"
    INVOICE = "invoice"
    CONTRACT = "contract"
    PURCHASE_ORDER = "purchase_order"
    CRM_OPPORTUNITY = "crm_opportunity"
    VENDOR_PROFILE = "vendor_profile"
    PROJECT = "project"
    EMPLOYEE = "employee"
    SERVICE_TICKET = "service_ticket"
    EMPLOYMENT_CONTRACT = "employment_contract"
    INSURANCE_POLICY = "insurance_policy"
    MEETING_MINUTES = "meeting_minutes"
    BANK_STATEMENT = "bank_statement"
    PROJECT_REPORT = "project_report"
    GENERIC_CONTRACT = "generic_contract"


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
    aliases: tuple[str, ...] = ()
    weight: float = 1.0

    def __str__(self) -> str:
        return self.name


@dataclass(frozen=True)
class QuestionTemplateRule:
    key: str
    query_template: tuple[str, ...]
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
    document_type: DocumentType
    fields: dict[str, tuple[str, ...]]


@dataclass(frozen=True)
class TemplateDefinition:
    name: str
    classification_rules: tuple[ClassificationRule, ...]
    extraction_rules: dict[str, tuple[FieldRule, ...]]
    question_templates: dict[str, list[QuestionTemplateRule]]
