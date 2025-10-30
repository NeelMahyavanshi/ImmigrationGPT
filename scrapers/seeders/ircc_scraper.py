import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from crawl4ai.deep_crawling import BFSDeepCrawlStrategy
from crawl4ai.deep_crawling.filters import FilterChain, URLPatternFilter, DomainFilter, ContentTypeFilter   
import json

OUTPUT_FILE = "ircc_urls_list.json"

async def deep_crawl_example():

    config = CrawlerRunConfig(
        deep_crawl_strategy=BFSDeepCrawlStrategy(
            max_depth=5,           
            include_external=False, 
            max_pages=10000,       
        ),
        verbose=True
    )

    async with AsyncWebCrawler() as crawler:

        results = await crawler.arun("https://www.canada.ca/en/immigration-refugees-citizenship/services/study-canada/work/after-graduation/about.html", config=config)

        print(f"Discovered and crawled {len(results)} pages")

        url_list = [url.url for url in results]

        # Save IRCC-specific URLs
        
        with open(OUTPUT_FILE, "a") as f:
            json.dump(url_list, f, indent=4)
        print(f"✅ Saved {len(url_list)} IRCC URLs to {OUTPUT_FILE}")

        for result in results:
            print(f"Found: {result.url} at depth {result.metadata.get('depth', 0)}")

asyncio.run(deep_crawl_example())
