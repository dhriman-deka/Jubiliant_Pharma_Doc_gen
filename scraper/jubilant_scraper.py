import asyncio
import json
from datetime import datetime
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BFSDeepCrawlStrategy, DomainFilter, FilterChain

async def main():
    # Configure the crawler
    config = CrawlerRunConfig(
        crawling_strategy=BFSDeepCrawlStrategy(
            max_depth=2,           # Limit depth to 2 for simplicity
            include_external=False, # Only crawl within the same domain
            max_pages=50           # Limit to 50 pages to avoid overwhelming the site
        ),
        filter_chain=FilterChain(
            filters=[
                DomainFilter(allowed_domains=["jubilantpharmova.com"])
            ]
        ),
        output_format="markdown"  # Get cleaned content in markdown format
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
                "content": result.markdown,
            }
            output.append(page_data)
            
            # Print progress
            print(f"Scraped: {result.url}")
        
        # Save to file with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"jubilant_pharmova_data_{timestamp}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        
        print(f"\nScraping complete. Saved {len(output)} pages to {filename}")

if __name__ == "__main__":
    asyncio.run(main()) 