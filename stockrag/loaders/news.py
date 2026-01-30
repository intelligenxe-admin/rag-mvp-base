"""News and RSS feed loader."""

from datetime import datetime
from typing import List, Optional

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
    print("Loading news releases...")

    news_docs = []

    # Option 1: RSS feed
    if rss_url:
        # from llama_index.readers.rss import RssReader
        # rss_reader = RssReader()
        # docs = rss_reader.load_data(urls=[rss_url])
        pass

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
                print(f"Error loading news from {url}: {e}")

    if add_to_context:
        ctx.documents.extend(news_docs)

    print(f"Loaded {len(news_docs)} news documents")
    return news_docs
