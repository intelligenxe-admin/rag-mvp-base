"""News and RSS feed loader."""

import logging
from datetime import datetime
from typing import List, Optional

logger = logging.getLogger(__name__)

from llama_index.core import Document
from llama_index.readers.web import TrafilaturaWebReader

from stockrag.core.context import RAGContext
from stockrag.loaders.base import add_metadata


def load_news_releases(
    ctx: RAGContext,
    rss_url: Optional[str] = None,
    news_urls: Optional[List[str]] = None,
    add_to_context: bool = True,
) -> List[Document]:
    """
    Load news releases from RSS feeds or direct URLs.

    Args:
        ctx: RAGContext instance
        rss_url: Optional RSS feed URL
        news_urls: Optional list of news article URLs
        add_to_context: Whether to add docs to ctx.documents

    Returns:
        List of loaded Document objects
    """
    logger.info("Loading news releases...")

    news_docs = []

    # Option 1: RSS feed
    if rss_url:
        # TODO: Implement RSS feed support using llama_index.readers.rss.RssReader
        logger.warning("RSS feed loading is not yet implemented. Provide news_urls instead.")

    # Option 2: Direct URLs
    if news_urls:
        web_reader = TrafilaturaWebReader()
        for url in news_urls:
            try:
                docs = web_reader.load_data(urls=[url])

                # Add metadata
                add_metadata(
                    docs,
                    {
                        "source": "News Release",
                        "ticker": ctx.ticker,
                        "url": url,
                        "scrape_date": datetime.now().isoformat(),
                    },
                )

                news_docs.extend(docs)
            except Exception as e:
                logger.error("Error loading news from %s: %s", url, e)

    if add_to_context:
        ctx.documents.extend(news_docs)

    logger.info("Loaded %d news documents", len(news_docs))
    return news_docs
