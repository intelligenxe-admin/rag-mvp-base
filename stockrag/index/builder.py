"""Index building functionality."""

import logging

from llama_index.core import VectorStoreIndex

logger = logging.getLogger(__name__)

from stockrag.core.context import RAGContext
from stockrag.core.exceptions import NoDocumentsError


def build_index(ctx: RAGContext, show_progress: bool = True) -> VectorStoreIndex:
    """
    Build vector index from loaded documents.

    Args:
        ctx: RAGContext with documents loaded
        show_progress: Show indexing progress bar

    Returns:
        VectorStoreIndex instance (also stored in ctx.index)

    Raises:
        NoDocumentsError: If no documents are loaded
    """
    logger.info("Building index from %d documents...", len(ctx.documents))

    if not ctx.documents:
        raise NoDocumentsError()

    # Create index
    ctx.index = VectorStoreIndex.from_documents(
        ctx.documents,
        storage_context=ctx.storage_context,
        show_progress=show_progress,
    )

    logger.info("Index built successfully!")
    return ctx.index
