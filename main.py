"""
RAG Knowledge Base for NYSE Company - Example Usage

This file demonstrates how to use the stockrag package.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from stockrag import StockRAG


def main():
    """Example using the object-oriented API."""
    # Initialize RAG system with Groq API key
    rag = StockRAG(
        ticker="AAPL",
        company_name="Apple Inc.",
        groq_api_key=os.environ.get("GROQ_API_KEY"),
    )

    # Load data from various sources
    # rag.load_sec_filings(filing_types=["10-K", "10-Q"])
    rag.load_annual_reports(pdf_paths=["./data/apple_annual_report_2024.pdf"])
    # rag.load_company_website(urls=[
    #     "https://www.apple.com/investor-relations/",
    #     "https://www.apple.com/newsroom/"
    # ])
    # rag.load_news_releases(news_urls=[
    #     "https://www.apple.com/newsroom/2024/01/apple-reports-first-quarter-results/"
    # ])

    # Build index
    rag.build_index()

    # Or load existing index
    # rag.load_existing_index()

    # Create query engine
    rag.create_query_engine()

    # Query examples
    response = rag.query("What was the revenue in the last fiscal year?")
    print(f"\nAnswer: {response}")

    response = rag.query("What are the main business segments?")
    print(f"\nAnswer: {response}")

    # Query with filters
    # response = rag.query_with_filters(
    #     "What were the key highlights?",
    #     source_filter="Annual Report"
    # )

    # Get statistics
    # stats = rag.get_stats()
    # print(f"\nKnowledge Base Stats: {stats}")

    print("\nRAG system initialized with Groq LLM and open source embeddings.")
    print("Uncomment code sections to use.")


def main_functional():
    """Example using the functional API."""
    from stockrag import (
        create_context,
        load_annual_reports,
        build_index,
        query,
        RAGConfig,
        LLMConfig,
    )

    # Custom configuration (optional)
    config = RAGConfig(
        llm=LLMConfig(
            model="llama-3.3-70b-versatile",
            temperature=0.1,
        )
    )

    # Create context
    ctx = create_context("AAPL", "Apple Inc.", config)

    # Load data
    load_annual_reports(ctx, ["./data/apple_annual_report_2024.pdf"])

    # Build index
    build_index(ctx)

    # Query
    response = query(ctx, "What was the revenue in the last fiscal year?")
    print(f"\nAnswer: {response}")


if __name__ == "__main__":
    main()
    # main_functional()  # Uncomment to try the functional API
