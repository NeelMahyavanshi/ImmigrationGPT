import json

with open("test.json", "r") as f:
    urls = json.load(f)


with open("test2.json", "r") as f:
    urls_canadavisa = json.load(f)

    url_list_canadavisa = [url for url in urls_canadavisa if '/canada-immigration-discussion-board/members/' not in url]

all_urls  = urls + url_list_canadavisa

with open("urls_to_scrape.json", "w") as f:
    json.dump(all_urls, f,indent=4)