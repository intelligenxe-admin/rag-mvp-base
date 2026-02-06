"""Custom exceptions for StockRAG."""


class StockRAGError(Exception):
    """Base exception for StockRAG."""

    pass


class NoDocumentsError(StockRAGError):
    """Raised when attempting to build index without documents."""

    def __init__(self, message: str = "No documents loaded. Load data first."):
        super().__init__(message)


class IndexNotBuiltError(StockRAGError):
    """Raised when attempting to query without building index."""

    def __init__(self, message: str = "Index not built. Call build_index() first."):
        super().__init__(message)


class ConfigurationError(StockRAGError):
    """Raised when there's a configuration issue."""

    pass
