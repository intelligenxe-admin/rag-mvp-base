"""
StockRAG client - High-level facade for the RAG system.

Provides a class-based API that wraps the functional modules
for users who prefer an object-oriented interface.
"""

import os
from typing import List, Dict, Optional, Tuple, Any

from llama_index.core import Document, Settings, StorageContext
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.groq import Groq
from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb

from stockrag.core.context import RAGContext
from stockrag.core.config import RAGConfig
from stockrag.core.exceptions import ConfigurationError
from stockrag import loaders, index, query as query_module, maintenance


def create_context(
    ticker: str,
    company_name: str,
    config: Optional[RAGConfig] = None,
) -> RAGContext:
    """
    Factory function to create and initialize a RAGContext.

    Args:
        ticker: Company stock ticker
        company_name: Full company name
        config: Optional RAGConfig (uses defaults if None)

    Returns:
        Initialized RAGContext with vector store configured
    """
    config = config or RAGConfig()
    ctx = RAGContext(ticker=ticker, company_name=company_name)
    _initialize_context(ctx, config)
    return ctx


def _initialize_context(ctx: RAGContext, config: RAGConfig) -> None:
    """Initialize LlamaIndex settings and vector store."""
    # Validate API key
    api_key = config.llm.api_key or os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ConfigurationError(
            "Groq API key must be provided or set in GROQ_API_KEY environment variable"
        )

    # Configure LLM
    Settings.llm = Groq(
        model=config.llm.model,
        temperature=config.llm.temperature,
        api_key=api_key,
    )

    # Configure embeddings
    Settings.embed_model = HuggingFaceEmbedding(
        model_name=config.embedding.model_name
    )

    # Configure chunking
    Settings.node_parser = SentenceSplitter(
        chunk_size=config.chunking.chunk_size,
        chunk_overlap=config.chunking.chunk_overlap,
    )

    # Initialize vector store
    persist_path = config.vector_store.persist_path or f"./chroma_db_{ctx.ticker}"
    collection_name = (
        config.vector_store.collection_name or f"{ctx.ticker}_knowledge_base"
    )

    ctx.chroma_client = chromadb.PersistentClient(path=persist_path)
    ctx.chroma_collection = ctx.chroma_client.get_or_create_collection(
        name=collection_name
    )
    ctx.vector_store = ChromaVectorStore(chroma_collection=ctx.chroma_collection)
    ctx.storage_context = StorageContext.from_defaults(vector_store=ctx.vector_store)


class StockRAG:
    """
    High-level RAG client for NYSE company information.

    This class provides an object-oriented interface that wraps
    the functional API. For more control, use the functional API directly.

    Example:
        rag = StockRAG("AAPL", "Apple Inc.")
        rag.load_annual_reports(["./report.pdf"])
        rag.build_index()
        answer = rag.query("What was the revenue?")
    """

    def __init__(
        self,
        ticker: str,
        company_name: str,
        config: Optional[RAGConfig] = None,
        groq_api_key: Optional[str] = None,  # Backward compatibility
    ):
        """
        Initialize RAG system.

        Args:
            ticker: Company stock ticker symbol
            company_name: Full company name
            config: Optional RAGConfig for customization
            groq_api_key: Optional Groq API key (for backward compatibility)
        """
        if groq_api_key:
            if config is None:
                config = RAGConfig()
            config.llm.api_key = groq_api_key

        self.config = config or RAGConfig()
        self.ctx = create_context(ticker, company_name, self.config)

    # Convenience properties
    @property
    def ticker(self) -> str:
        """Company stock ticker."""
        return self.ctx.ticker

    @property
    def company_name(self) -> str:
        """Company name."""
        return self.ctx.company_name

    @property
    def documents(self) -> List[Document]:
        """List of loaded documents."""
        return self.ctx.documents

    # Data Loading Methods (delegate to loaders module)
    def load_sec_filings(
        self,
        filing_types: Optional[List[str]] = None,
    ) -> List[Document]:
        """Load SEC filings from EDGAR."""
        return loaders.load_sec_filings(self.ctx, filing_types)

    def load_annual_reports(
        self,
        pdf_paths: List[str],
    ) -> List[Document]:
        """Load annual reports from PDF files."""
        return loaders.load_annual_reports(self.ctx, pdf_paths)

    def load_company_website(
        self,
        urls: List[str],
    ) -> List[Document]:
        """Load content from company website."""
        return loaders.load_company_website(self.ctx, urls)

    def load_news_releases(
        self,
        rss_url: Optional[str] = None,
        news_urls: Optional[List[str]] = None,
    ) -> List[Document]:
        """Load news releases."""
        return loaders.load_news_releases(self.ctx, rss_url, news_urls)

    # Index Methods (delegate to index module)
    def build_index(self):
        """Build vector index from loaded documents."""
        return index.build_index(self.ctx)

    def load_existing_index(self):
        """Load previously built index."""
        return index.load_existing_index(self.ctx)

    # Query Methods (delegate to query module)
    def create_query_engine(self, similarity_top_k: int = 5):
        """Create query engine."""
        return query_module.create_query_engine(self.ctx, similarity_top_k)

    def query(self, question: str) -> Any:
        """Query the knowledge base."""
        return query_module.query(self.ctx, question)

    def query_with_filters(
        self,
        question: str,
        source_filter: Optional[str] = None,
        date_range: Optional[Tuple[str, str]] = None,
    ) -> Any:
        """Query with metadata filters."""
        return query_module.query_with_filters(
            self.ctx, question, source_filter, date_range
        )

    # Maintenance Methods (delegate to maintenance module)
    def update_with_new_data(self, new_documents: List[Document]) -> None:
        """Add new documents to index."""
        return maintenance.update_with_new_data(self.ctx, new_documents)

    def get_stats(self) -> Dict[str, Any]:
        """Get knowledge base statistics."""
        return maintenance.get_stats(self.ctx)
