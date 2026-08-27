import pytest

from rules import detect_document_type


@pytest.mark.parametrize(
    ("filename", "text", "expected"),
    [
        (
            "Invoice.pdf",
            "",
            "invoice",
        ),
        (
            "",
            "Invoice Number: INV-001",
            "invoice",
        ),
        (
            "Vendor Agreement.pdf",
            "",
            "contract",
        ),
        (
            "",
            """
            This Agreement
            Effective Date: 2025-01-01
            """,
            "contract",
        ),
        (
            "Purchase Order.pdf",
            "",
            "purchase_order",
        ),
        (
            "",
            """
            Purchase Order

            PO Number: PO-001
            """,
            "purchase_order",
        ),
        (
            "",
            """
            Opportunity Stage: Qualification
            """,
            "crm_opportunity",
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