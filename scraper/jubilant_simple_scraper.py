import asyncio
import json
from datetime import datetime
from crawl4ai import AsyncWebCrawler

async def main():
    # Create the crawler with default configuration
    async with AsyncWebCrawler() as crawler:
        # Crawl the website - using the simplest API approach
        results = await crawler.arun_many(
            urls=["https://www.jubilantpharmova.com/"],
            max_pages=50,  # Limit to 50 pages
            include_external=False,  # Only crawl within the same domain
        )
        
        # Process and save results
        output = []
        for result in results:
            # First, let's print what attributes are available on the result object
            print(f"Available attributes: {dir(result)}")
            
            # Store the basic information we know is available
            page_data = {
                "url": result.url,
                "content": result.markdown if hasattr(result, 'markdown') else None,
                "html": result.html if hasattr(result, 'html') else None,
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