"""Index update operations."""

import logging
from typing import List

logger = logging.getLogger(__name__)

from llama_index.core import Document

from stockrag.core.context import RAGContext
from stockrag.core.exceptions import IndexNotBuiltError


def update_with_new_data(ctx: RAGContext, new_documents: List[Document]) -> None:
    """
    Add new documents to existing index.

    Args:
        ctx: RAGContext with index built
        new_documents: List of new documents to add

    Raises:
        IndexNotBuiltError: If index is not built
    """
    if not ctx.index:
        raise IndexNotBuiltError()

    logger.info("Adding %d new documents to index...", len(new_documents))

    for doc in new_documents:
        ctx.index.insert(doc)

    # Also add to context documents list
    ctx.documents.extend(new_documents)

    logger.info("Index updated!")
