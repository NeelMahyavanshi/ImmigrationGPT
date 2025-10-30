import json
import re
from playwright.sync_api import sync_playwright

def scrape_form_page(url: str):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url.strip(), wait_until="domcontentloaded", timeout=30000)
        page.wait_for_selector("main", timeout=10000)

        # Click expand buttons (if any)
        try:
            show_btn = page.get_by_role("button", name=re.compile(r"Show.*instruction", re.IGNORECASE))
            if show_btn.is_visible():
                show_btn.click()
                page.wait_for_timeout(1000)
        except:
            pass

        try:
            expand_btn = page.get_by_role("button", name=re.compile(r"Expand all", re.IGNORECASE))
            if expand_btn.is_visible():
                expand_btn.click()
                page.wait_for_timeout(2000)
        except:
            pass

        # ✅ FIX: Extract PDF URL from the actual <a> tag containing ".pdf"
        pdf_url = None
        try:
            # Look for any <a> tag with .pdf in href
            pdf_links = page.query_selector_all('a[href*=".pdf"]')
            if pdf_links:
                href = pdf_links[0].get_attribute("href")
                if href:
                    if href.startswith("/"):
                        pdf_url = "https://www.canada.ca" + href
                    else:
                        pdf_url = href
        except Exception as e:
            print(f"⚠️ PDF extraction error: {e}")

        # Extract instructions
        instructions = ""
        try:
            complete_form = page.locator('text="Complete the form"')
            if complete_form.count() > 0:
                parent = complete_form.locator("..")
                instructions = parent.text_content().strip()
                instructions = "\n".join(line.strip() for line in instructions.splitlines() if line.strip())
        except:
            pass

        browser.close()
        return {
            "form_page_url": url.strip(),
            "pdf_url": pdf_url,
            "how_to_fill_instructions": instructions
        }
# Example usage
if __name__ == "__main__":
    url = "https://www.canada.ca/en/immigration-refugees-citizenship/services/application/application-forms-guides/cit0002.html"
    result = scrape_form_page(url)
    print(json.dumps(result, indent=2, ensure_ascii=False))

    with open("cit0002_full.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)