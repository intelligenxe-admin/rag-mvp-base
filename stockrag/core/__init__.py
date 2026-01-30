"""Core module for StockRAG - context, configuration, and exceptions."""

from stockrag.core.context import RAGContext
from stockrag.core.config import (
    RAGConfig,
    LLMConfig,
    EmbeddingConfig,
    ChunkingConfig,
    VectorStoreConfig,
)
from stockrag.core.exceptions import (
    StockRAGError,
    NoDocumentsError,
    IndexNotBuiltError,
    ConfigurationError,
)

__all__ = [
    "RAGContext",
    "RAGConfig",
    "LLMConfig",
    "EmbeddingConfig",
    "ChunkingConfig",
    "VectorStoreConfig",
    "StockRAGError",
    "NoDocumentsError",
    "IndexNotBuiltError",
    "ConfigurationError",
]
