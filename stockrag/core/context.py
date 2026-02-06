"""
RAGContext - Shared state container for RAG operations.

This dataclass holds all shared state including documents, index,
vector store, and configuration. Functions accept this context
as their first parameter.
"""

from dataclasses import dataclass, field
from typing import List, Optional, TYPE_CHECKING

from llama_index.core import Document, VectorStoreIndex, StorageContext

if TYPE_CHECKING:
    from llama_index.core.query_engine import BaseQueryEngine
    from llama_index.vector_stores.chroma import ChromaVectorStore
    from chromadb import ClientAPI
    from chromadb.api.models.Collection import Collection


@dataclass
class RAGContext:
    """
    Container for all RAG system state.

    Attributes:
        ticker: Company stock ticker symbol
        company_name: Full company name
        documents: List of loaded documents
        index: VectorStoreIndex instance (after build)
        query_engine: Query engine instance
        vector_store: ChromaVectorStore instance
        storage_context: LlamaIndex StorageContext
        chroma_client: ChromaDB client
        chroma_collection: ChromaDB collection
    """

    ticker: str
    company_name: str
    documents: List[Document] = field(default_factory=list)
    index: Optional[VectorStoreIndex] = None
    query_engine: Optional["BaseQueryEngine"] = None
    vector_store: Optional["ChromaVectorStore"] = None
    storage_context: Optional[StorageContext] = None
    chroma_client: Optional["ClientAPI"] = None
    chroma_collection: Optional["Collection"] = None
