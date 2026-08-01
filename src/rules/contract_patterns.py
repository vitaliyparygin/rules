import re

CONTRACT_IDENTIFIER_RE = re.compile(
    r"\b[A-Z]{1,5}(?:-\d+){1,2}\b",
    re.IGNORECASE,
)