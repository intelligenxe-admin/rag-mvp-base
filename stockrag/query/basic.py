"""Basic query operations."""

from typing import Any

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
    if not ctx.query_engine:
        create_query_engine(ctx)

    print(f"\nQuery: {question}")
    response = ctx.query_engine.query(question)

    # Print sources
    if print_sources:
        print("\nSources:")
        for node in response.source_nodes:
            source = node.metadata.get("source", "Unknown")
            location = node.metadata.get("file_path", node.metadata.get("url", "N/A"))
            print(f"- {source}: {location}")

    return response
