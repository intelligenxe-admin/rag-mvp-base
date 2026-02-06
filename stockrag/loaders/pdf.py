"""PDF document loader for annual reports."""

import logging
from typing import List

logger = logging.getLogger(__name__)

from llama_index.core import Document
from llama_index.readers.file import PDFReader

from stockrag.core.context import RAGContext
from stockrag.loaders.base import add_metadata


def load_annual_reports(
    ctx: RAGContext,
    pdf_paths: List[str],
    add_to_context: bool = True,
) -> List[Document]:
    """
    Load annual reports from PDF files.

    Args:
        ctx: RAGContext instance
        pdf_paths: List of paths to PDF files
        add_to_context: Whether to add docs to ctx.documents

    Returns:
        List of loaded Document objects
    """
    logger.info("Loading annual reports...")
    pdf_reader = PDFReader()

    annual_docs = []
    for pdf_path in pdf_paths:
        docs = pdf_reader.load_data(file=pdf_path)

        # Add metadata
        add_metadata(
            docs,
            {
                "source": "Annual Report",
                "ticker": ctx.ticker,
                "file_path": pdf_path,
            },
        )

        annual_docs.extend(docs)

    if add_to_context:
        ctx.documents.extend(annual_docs)

    logger.info("Loaded %d annual report documents", len(annual_docs))
    return annual_docs
