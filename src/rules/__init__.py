# src/rules/__init__.py

__version__ = "0.1.9"

from .document_type import detect_document_type
from .extraction import extract_metadata
from .models import DocumentType

__all__ = [
    "DocumentType",
    "detect_document_type",
    "extract_metadata",
]