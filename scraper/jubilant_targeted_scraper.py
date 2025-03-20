import asyncio
import json
from datetime import datetime
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BFSDeepCrawlStrategy, DomainFilter, FilterChain, CSSExtractionStrategy

async def main():
    # Configure the crawler with targeted extraction
    config = CrawlerRunConfig(
        crawling_strategy=BFSDeepCrawlStrategy(
            max_depth=2,
            include_external=False,
            max_pages=50
        ),
        filter_chain=FilterChain(
            filters=[
                DomainFilter(allowed_domains=["jubilantpharmova.com"])
            ]
        ),
        extraction_strategy=CSSExtractionStrategy(
            css_selector="h1, h2, h3, p, a.nav-link, .content-area, .footer-content",
            output_format="json"
        ),
        output_format="markdown"
    )
    
    # Create and run the crawler
    async with AsyncWebCrawler(config=config) as crawler:
        results = await crawler.arun_many(
            urls=["https://www.jubilantpharmova.com/"],
            run_config=config,
        )
        
        # Process and save results
        output = []
        for result in results:
            page_data = {
                "url": result.url,
                "title": result.title,
                "extracted_elements": result.extracted_data,
                "full_content": result.markdown,
            }
            output.append(page_data)
            
            # Print progress
            print(f"Scraped: {result.url}")
        
        # Save to file with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"jubilant_pharmova_targeted_data_{timestamp}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        
        print(f"\nScraping complete. Saved {len(output)} pages to {filename}")

if __name__ == "__main__":
    asyncio.run(main()) 