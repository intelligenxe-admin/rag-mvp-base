"""Query engine creation and configuration."""

from typing import Any

from stockrag.core.context import RAGContext
from stockrag.core.exceptions import IndexNotBuiltError


def create_query_engine(
    ctx: RAGContext,
    similarity_top_k: int = 5,
    response_mode: str = "compact",
    verbose: bool = True,
) -> Any:
    """
    Create and configure query engine.

    Args:
        ctx: RAGContext with index built
        similarity_top_k: Number of similar documents to retrieve
        response_mode: Response mode ("compact", "refine", "tree_summarize")
        verbose: Enable verbose output

    Returns:
        Query engine instance (also stored in ctx.query_engine)

    Raises:
        IndexNotBuiltError: If index is not built
    """
    if not ctx.index:
        raise IndexNotBuiltError()

    ctx.query_engine = ctx.index.as_query_engine(
        similarity_top_k=similarity_top_k,
        response_mode=response_mode,
        verbose=verbose,
    )

    return ctx.query_engine
