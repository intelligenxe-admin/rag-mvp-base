"""Document loaders for various data sources."""

from stockrag.loaders.pdf import load_annual_reports
from stockrag.loaders.web import load_company_website
from stockrag.loaders.news import load_news_releases
from stockrag.loaders.sec_filings import load_sec_filings
from stockrag.loaders.base import add_metadata

__all__ = [
    "load_annual_reports",
    "load_company_website",
    "load_news_releases",
    "load_sec_filings",
    "add_metadata",
]
