import asyncio
from crawl4ai.async_configs import CrawlerRunConfig
from crawl4ai import AsyncWebCrawler, CacheMode,  RateLimiter, MemoryAdaptiveDispatcher
import json
import time

INPUT_FILE = "backend/data/ircc_urls_list.json"
OUTPUT_FILE = "immigration_ircc_content.jsonl"


# Truncation marker for Canadavisa (more robust)
TRUNCATE_MARKER = "**Immigrate to Canada**"


async def main():

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        urls = json.load(f)

    run_config = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        stream=True,  
        word_count_threshold=100,
        excluded_tags=["nav", "footer", "header", "aside", "script", "style"],
        wait_until= "networkidle",
        page_timeout= 60000
    )   

    rate_limiter = RateLimiter(
        base_delay=(1.0, 3.0),
        max_delay=30.0,
        max_retries=2,
        rate_limit_codes=[429, 503]
    )

    dispatcher = MemoryAdaptiveDispatcher(
        max_session_permit=5,
        rate_limiter=rate_limiter
    )


    stats = {"processed": 0, "success": 0, "failed": 0, "errors": 0}
    async with AsyncWebCrawler() as crawler:
        for url in urls:
            try:
                result = await crawler.arun(
                    url=url.strip(),  # strip whitespace!
                    config=run_config,
                    dispatcher=dispatcher
                )

                if result.success and result.markdown.strip():
                    clean_text = result.markdown.strip()
                    rag_document = {
                        "id" : f"Immigration_{stats['processed']}_{int(time.time())}",
                        "url" : result.url,
                        "title" : result.metadata.get("title", ""),
                        "description" : result.metadata.get("description", ""),
                        "content" : clean_text,
                        "timestamp" : time.time(),
                        "content_length" : len(result.markdown),
                        "language" : "fr" if "/fr/" in result.url else "en",
                        "source" : "ircc_gov" if "canadavisa" not in result.url else "canadavisa"
                    }

                    with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
                        f.write(json.dumps(rag_document, ensure_ascii=False) + "\n")

                    stats["success"] += 1
                    print(f"✅ {result.metadata.get('title', '')[:50]}...")

                else:
                    print(f"❌ Failed or empty: {url}")
                    stats["failed"] += 1

            except Exception as e:
                print(f"❗ Error on {url}: {e}")
                stats["errors"] += 1

            stats["processed"] += 1
            print(f"📊 Processed: {stats['processed']} | Success: {stats['success']}")

            # Be polite: 1-2 sec delay
            await asyncio.sleep(1.5)


if __name__ == "__main__":
    asyncio.run(main())