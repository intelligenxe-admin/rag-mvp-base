"""Index update operations."""

from typing import List

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

    print(f"Adding {len(new_documents)} new documents to index...")

    for doc in new_documents:
        ctx.index.insert(doc)

    # Also add to context documents list
    ctx.documents.extend(new_documents)

    print("Index updated!")
