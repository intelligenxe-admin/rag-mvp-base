"""Filtered query operations."""

from typing import Any, Optional, Tuple

from llama_index.core.vector_stores import MetadataFilters, ExactMatchFilter

from stockrag.core.context import RAGContext
from stockrag.core.exceptions import IndexNotBuiltError


def query_with_filters(
    ctx: RAGContext,
    question: str,
    source_filter: Optional[str] = None,
    date_range: Optional[Tuple[str, str]] = None,
    similarity_top_k: int = 5,
) -> Any:
    """
    Query with metadata filters.

    Args:
        ctx: RAGContext with index built
        question: Natural language question
        source_filter: Filter by source type (e.g., "Annual Report", "SEC")
        date_range: Optional date range filter (start, end) - not yet implemented
        similarity_top_k: Number of similar documents to retrieve

    Returns:
        Response from the LLM
    """
    if not ctx.index:
        raise IndexNotBuiltError()

    filters = []
    if source_filter:
        filters.append(ExactMatchFilter(key="source", value=source_filter))

    # TODO: Add date range filter support
    # if date_range:
    #     filters.append(...)

    metadata_filters = MetadataFilters(filters=filters) if filters else None

    query_engine = ctx.index.as_query_engine(
        similarity_top_k=similarity_top_k,
        filters=metadata_filters,
    )

    response = query_engine.query(question)
    return response
