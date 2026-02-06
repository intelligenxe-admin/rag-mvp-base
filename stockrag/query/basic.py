"""Basic query operations."""

import logging
from typing import Any

logger = logging.getLogger(__name__)

from stockrag.core.context import RAGContext
from stockrag.query.engine import create_query_engine


def query(
    ctx: RAGContext,
    question: str,
    print_sources: bool = True,
) -> Any:
    """
    Query the knowledge base.

    Args:
        ctx: RAGContext with index built
        question: Natural language question
        print_sources: Print source documents used

    Returns:
        Response from the LLM
    """
    # Reuse existing engine, or create default one on first call
    if not ctx.query_engine:
        create_query_engine(ctx)

    logger.info("Query: %s", question)
    response = ctx.query_engine.query(question)

    # Log sources
    if print_sources:
        logger.info("Sources:")
        for node in response.source_nodes:
            source = node.metadata.get("source", "Unknown")
            location = node.metadata.get("file_path", node.metadata.get("url", "N/A"))
            logger.info("- %s: %s", source, location)

    return response
