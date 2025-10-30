import requests
from bs4 import BeautifulSoup
import json
import re

url = "https://www.canada.ca/en/immigration-refugees-citizenship/services/application/application-forms-guides.html"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

forms = []

rows = soup.find_all('tr')
for row in rows:
    cells = row.find_all('td')
    if len(cells) >= 3:
        code = cells[0].get_text(strip=True)
        title = cells[1].get_text(strip=True)
        date = cells[2].get_text(strip=True)
        
        # Check if code matches form pattern (e.g., IMM 0008, CIT 0001)
        if re.match(r'(IMM|CIT|IRM)\s*\d{4}', code.replace('\u2009', ' ')):
            # Extract PDF link if exists
            link_tag = cells[1].find('a', href=True)
            pdf_url = link_tag['href'] if link_tag else None
            if pdf_url and not pdf_url.startswith('http'):
                pdf_url = 'https://www.canada.ca' + pdf_url

            forms.append({
                "form_code": code,
                "title": title,
                "last_updated": date,
                "pdf_url": pdf_url
            })

# Save to JSON
with open("ircc_forms_catalog.json", "w", encoding="utf-8") as f:
    json.dump(forms, f, indent=2, ensure_ascii=False)

print(f"✅ Scraped {len(forms)} forms!")