"""Index persistence operations."""

from llama_index.core import VectorStoreIndex

from stockrag.core.context import RAGContext


def load_existing_index(ctx: RAGContext) -> VectorStoreIndex:
    """
    Load previously built index from vector store.

    Args:
        ctx: RAGContext with vector_store configured

    Returns:
        VectorStoreIndex instance (also stored in ctx.index)
    """
    print("Loading existing index...")

    ctx.index = VectorStoreIndex.from_vector_store(
        ctx.vector_store,
        storage_context=ctx.storage_context,
    )

    print("Index loaded successfully!")
    return ctx.index
