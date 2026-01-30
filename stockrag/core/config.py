"""
Configuration management for StockRAG.

Handles LLM, embeddings, chunking, and vector store configuration.
Supports loading from environment variables, config files, or direct parameters.
"""

import os
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class LLMConfig:
    """LLM configuration."""

    provider: str = "groq"  # groq, openai, anthropic, ollama
    model: str = "llama-3.3-70b-versatile"
    temperature: float = 0.1
    api_key: Optional[str] = None

    def __post_init__(self):
        if self.api_key is None:
            self.api_key = os.environ.get("GROQ_API_KEY")


@dataclass
class EmbeddingConfig:
    """Embedding model configuration."""

    provider: str = "huggingface"  # huggingface, openai
    model_name: str = "BAAI/bge-small-en-v1.5"
    # Alternative: "sentence-transformers/all-MiniLM-L6-v2"


@dataclass
class ChunkingConfig:
    """Text chunking configuration."""

    chunk_size: int = 1024
    chunk_overlap: int = 200


@dataclass
class VectorStoreConfig:
    """Vector store configuration."""

    provider: str = "chroma"  # chroma, pinecone, weaviate, qdrant
    persist_path: Optional[str] = None  # Auto-generated if None
    collection_name: Optional[str] = None  # Auto-generated if None


@dataclass
class RAGConfig:
    """
    Complete RAG system configuration.

    Usage:
        # Default configuration
        config = RAGConfig()

        # Custom configuration
        config = RAGConfig(
            llm=LLMConfig(model="mixtral-8x7b-32768"),
            embedding=EmbeddingConfig(model_name="BAAI/bge-base-en-v1.5"),
            chunking=ChunkingConfig(chunk_size=512)
        )
    """

    llm: LLMConfig = field(default_factory=LLMConfig)
    embedding: EmbeddingConfig = field(default_factory=EmbeddingConfig)
    chunking: ChunkingConfig = field(default_factory=ChunkingConfig)
    vector_store: VectorStoreConfig = field(default_factory=VectorStoreConfig)
