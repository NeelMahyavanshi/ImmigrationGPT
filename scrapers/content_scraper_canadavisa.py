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

    word = "**Immigrate to Canada**"

    stats = {"processed": 0, "success": 0, "failed": 0, "errors": 0}

    async with AsyncWebCrawler() as crawler:

        async for result in await crawler.arun_many(
            urls=urls[241:],
            config=run_config,
            dispatcher=dispatcher
        ):            

            try :

                if not result.success:
                    print(f"Failed or empty: {result.url}")
                    stats["failed"] += 1
                    continue
                
                clean_text = result.markdown

                if result.success:
                    stats["success"] += 1

                    if "canadavisa.com" in result.url:
                        idx = clean_text.find(TRUNCATE_MARKER)
                        if idx != -1:
                            clean_text = clean_text[:idx].strip()

                    
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
                    

                    with open(OUTPUT_FILE,"a",encoding="utf-8") as f:
                        f.write(json.dumps(rag_document, ensure_ascii=False) + "\n")
            
                else:
                    print(f"Failed to crawl {result.url}: {result.error_message}")
                    stats["failed"] += 1

            except Exception as e:
                print(f"❗ Error processing {result.url}: {e}")
                stats["errors"] += 1

            stats["processed"] +=1

            print(f"📊 Total: {stats['processed']} | Success: {stats['success']} | Failed: {stats['failed']} | Errors: {stats['errors']}")

if __name__ == "__main__":
    asyncio.run(main())