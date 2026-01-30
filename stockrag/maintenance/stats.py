"""Knowledge base statistics."""

from typing import Dict, Any

from stockrag.core.context import RAGContext


def get_stats(ctx: RAGContext) -> Dict[str, Any]:
    """
    Get statistics about the knowledge base.

    Args:
        ctx: RAGContext instance

    Returns:
        Dictionary with statistics including:
        - total_documents: Total number of documents
        - documents_by_source: Count of documents by source type
        - ticker: Company ticker
        - company_name: Company name
    """
    doc_sources: Dict[str, int] = {}
    for doc in ctx.documents:
        source = doc.metadata.get("source", "Unknown")
        doc_sources[source] = doc_sources.get(source, 0) + 1

    return {
        "total_documents": len(ctx.documents),
        "documents_by_source": doc_sources,
        "ticker": ctx.ticker,
        "company_name": ctx.company_name,
    }
