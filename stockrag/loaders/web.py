"""Web content loader using BeautifulSoup."""

import logging
from datetime import datetime
from typing import List

logger = logging.getLogger(__name__)

from llama_index.core import Document
from llama_index.readers.web import BeautifulSoupWebReader

from stockrag.core.context import RAGContext
from stockrag.loaders.base import add_metadata


def load_company_website(
    ctx: RAGContext,
    urls: List[str],
    add_to_context: bool = True,
) -> List[Document]:
    """
    Load content from company website URLs.

    Args:
        ctx: RAGContext instance
        urls: List of website URLs to scrape
        add_to_context: Whether to add docs to ctx.documents

    Returns:
        List of loaded Document objects
    """
    logger.info("Loading company website content...")
    web_reader = BeautifulSoupWebReader()

    web_docs = []
    for url in urls:
        try:
            docs = web_reader.load_data(urls=[url])

            # Add metadata
            add_metadata(
                docs,
                {
                    "source": "Company Website",
                    "ticker": ctx.ticker,
                    "url": url,
                    "scrape_date": datetime.now().isoformat(),
                },
            )

            web_docs.extend(docs)
        except Exception as e:
            logger.error("Error loading %s: %s", url, e)

    if add_to_context:
        ctx.documents.extend(web_docs)

    logger.info("Loaded %d website documents", len(web_docs))
    return web_docs
