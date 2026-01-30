"""Base loader utilities."""

from typing import List, Dict, Any

from llama_index.core import Document


def add_metadata(docs: List[Document], metadata: Dict[str, Any]) -> List[Document]:
    """
    Add metadata to a list of documents.

    Args:
        docs: List of Document objects
        metadata: Dictionary of metadata to add

    Returns:
        The same list of documents with metadata updated
    """
    for doc in docs:
        doc.metadata.update(metadata)
    return docs
