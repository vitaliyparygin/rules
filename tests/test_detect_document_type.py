import pytest

from rules import detect_document_type


@pytest.mark.parametrize(
    ("filename", "text", "expected"),
    [
        (
            "Invoice.pdf",
            "",
            "Invoice",
        ),
        (
            "",
            "Invoice Number: INV-001",
            "Invoice",
        ),
        (
            "Vendor Agreement.pdf",
            "",
            "Contract",
        ),
        (
            "",
            """
            This Agreement
            Effective Date: 2025-01-01
            """,
            "Contract",
        ),
        (
            "Purchase Order.pdf",
            "",
            "Purchase Order",
        ),
        (
            "",
            """
            Purchase Order

            PO Number: PO-001
            """,
            "Purchase Order",
        ),
        (
            "",
            """
            Opportunity Stage: Qualification
            """,
            "CRM Opportunity",
        ),
        (
            "",
            "Some random document",
            None,
        ),
    ],
)
def test_detect_document_type(
    filename: str,
    text: str,
    expected: str | None,
):
    assert detect_document_type(
        text=text,
        filename=filename,
    ) == expected