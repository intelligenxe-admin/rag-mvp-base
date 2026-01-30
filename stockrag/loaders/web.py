"""Web content loader using BeautifulSoup."""

from datetime import datetime
from typing import List

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
    print("Loading company website content...")
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
            print(f"Error loading {url}: {e}")

    if add_to_context:
        ctx.documents.extend(web_docs)

    print(f"Loaded {len(web_docs)} website documents")
    return web_docs
