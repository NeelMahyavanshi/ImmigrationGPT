import json
import time
import os
from scrapers.pdf_content_scraper import scrape_form_page  # your existing function

OUTPUT_FILE = "ircc_forms_detailed.json"
CATALOG_FILE = "ircc_forms_catalog.json"

# Load catalog
with open(CATALOG_FILE, "r", encoding="utf-8") as f:
    catalog = json.load(f)

# Build list of landing page URLs (NOT PDFs!)
form_pages = []
for form in catalog:
    # If you saved landing_page_url during initial scrape, use it
    if "landing_page_url" in form and form["landing_page_url"]:
        form_pages.append(form["landing_page_url"])
    else:
        # Fallback: try to guess from form code (risky!)
        code = form.get("form_code", "").replace(" ", "").lower()
        if code:
            url = f"https://www.canada.ca/en/immigration-refugees-citizenship/services/application/application-forms-guides/{code}.html"
            form_pages.append(url)

# Load existing results (for resume)
if os.path.exists(OUTPUT_FILE):
    with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
        results = json.load(f)
    completed = {item["form_page_url"] for item in results}
else:
    results = []
    completed = set()

print(f"Starting scrape. Already completed: {len(completed)}")

for i, url in enumerate(form_pages):
    if url in completed:
        print(f"Skipping (already done): {url}")
        continue

    print(f"[{i+1}/{len(form_pages)}] Scraping: {url}")
    try:
        data = scrape_form_page(url)
        results.append(data)
        completed.add(url)

        # Save after every success (resume-safe)
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

        time.sleep(1)  # Be kind to IRCC servers

    except Exception as e:
        print(f"❌ Failed to scrape {url}: {e}")
        # Optional: save error placeholder
        results.append({
            "form_page_url": url,
            "error": str(e),
            "pdf_url": None,
            "how_to_fill_instructions": ""
        })
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        time.sleep(2)  # Wait longer on error

print("✅ Scrape complete!")