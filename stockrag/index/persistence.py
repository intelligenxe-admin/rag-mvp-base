"""Index persistence operations."""

import logging

from llama_index.core import VectorStoreIndex

logger = logging.getLogger(__name__)

from stockrag.core.context import RAGContext


def load_existing_index(ctx: RAGContext) -> VectorStoreIndex:
    """
    Load previously built index from vector store.

    Args:
        ctx: RAGContext with vector_store configured

    Returns:
        VectorStoreIndex instance (also stored in ctx.index)
    """
    logger.info("Loading existing index...")

    ctx.index = VectorStoreIndex.from_vector_store(
        ctx.vector_store,
        storage_context=ctx.storage_context,
    )

    logger.info("Index loaded successfully!")
    return ctx.index
