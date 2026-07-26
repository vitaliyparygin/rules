from __future__ import annotations
import re
from rules.loader import load_classification_rules
from functools import lru_cache

_RULES = load_classification_rules()

def detect_document_type(
    text: str,
    filename: str | None = None,
) -> str | None:
    """
    Detect document type using ClassificationRule definitions.

    Filename patterns are checked first.
    Content patterns are checked second.

    Returns:
        Document type or None.
    """

    filename = filename or ""

    # filename
    for rule in _RULES:
        if any(
            re.search(pattern, filename, re.IGNORECASE)
            for pattern in rule.filename_patterns
        ):
            return rule.document_type


    # content
    for rule in _RULES:
        if any(
            re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
            for pattern in rule.content_patterns
        ):
            return rule.document_type

    return None


@lru_cache(maxsize=1)
def _rules():
    return load_classification_rules()