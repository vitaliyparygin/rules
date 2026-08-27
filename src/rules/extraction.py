import re

from rules.loader import load_extraction_rules
from rules.models import DocumentType

_RULES = load_extraction_rules()


def extract_metadata(
    text: str,
    document_type: DocumentType | str | None,
) -> dict[str, str]:
    if document_type is None:
        return {}

    metadata: dict[str, str] = {}

    document_type_key = (
        document_type.value
        if isinstance(document_type, DocumentType)
        else document_type
    )

    fields = _RULES.get(document_type)

    if fields is None:
        return {}

    for field in fields:
        for pattern in field.patterns:
            match = re.search(
                pattern,
                text,
                re.IGNORECASE | re.MULTILINE,
            )

            if not match:
                continue

            metadata[field.name] = (
                match.group(1)
                if match.lastindex
                else match.group(0)
            ).strip()
            break

    return metadata