__version__ = "0.1.6"

from .document_type import detect_document_type
from .extraction import extract_metadata

__all__ = [
    "detect_document_type",
    "extract_metadata",
]