"""SEC EDGAR filings loader."""

from datetime import datetime
from typing import List, Optional

from llama_index.core import Document

from stockrag.core.context import RAGContext


def load_sec_filings(
    ctx: RAGContext,
    filing_types: Optional[List[str]] = None,
    add_to_context: bool = True,
) -> List[Document]:
    """
    Load SEC filings from EDGAR database.

    Args:
        ctx: RAGContext instance
        filing_types: List of filing types (e.g., ["10-K", "10-Q", "8-K"])
        add_to_context: Whether to add docs to ctx.documents

    Returns:
        List of loaded Document objects

    Note:
        This is currently a placeholder implementation.
        TODO: Implement actual SEC filing loading from EDGAR.
        Options:
        - Use SECFilingsLoader (if available)
        - Manual download from:
          https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={ticker}
        - Then use UnstructuredReader or PDFReader
    """
    if filing_types is None:
        filing_types = ["10-K", "10-Q", "8-K"]

    print(f"Loading SEC filings for {ctx.ticker}...")

    sec_docs = []
    # TODO: Implement actual SEC filing loading
    # For now, placeholder:
    for filing_type in filing_types:
        doc = Document(
            text=f"Placeholder for {filing_type} filing",
            metadata={
                "source": "SEC",
                "filing_type": filing_type,
                "ticker": ctx.ticker,
                "date": datetime.now().isoformat(),
            },
        )
        sec_docs.append(doc)

    if add_to_context:
        ctx.documents.extend(sec_docs)

    print(f"Loaded {len(sec_docs)} SEC filing documents")
    return sec_docs
