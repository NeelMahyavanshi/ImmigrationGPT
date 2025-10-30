import json

with open("ircc_forms_catalog.json", "r", encoding= "utf-8") as f:
    pdf1 = json.load(f)

with open("ircc_forms_detailed.json", "r", encoding= "utf-8") as f:
    pdf2 = json.load(f)



pdf_link1 = pdf1[0]["pdf_url"]
pdf_link2 = pdf2[0]["form_page_url"]

for i in range(len(pdf1)):
    pdf_link1 = pdf1[i]["pdf_url"]
    pdf_link2 = pdf2[i]["form_page_url"]

    if pdf_link1 == pdf_link2:
        form_code = pdf1[i]["form_code"]
        title = pdf1[i]["title"]
        last_updated = pdf1[i]["last_updated"]
        form_page_url = pdf1[i]["pdf_url"]
        pdf_url = pdf2[i]["pdf_url"]
        how_to_fill_instructions  = pdf2[i]["how_to_fill_instructions"]

        rag_document = {
            "form_code": form_code,
            "title": title,
            "last_updated": last_updated,
            "form_page_url": form_page_url,
            "pdf_url": pdf_url,
            "how_to_fill_instructions": how_to_fill_instructions
        }

        with open("ircc_forms_details.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps(rag_document, ensure_ascii=False) + "\n")
        print(f"Processed form: {form_code}")
        print("Processing Done")

    elif pdf_link1 != pdf_link2:
        form_code = pdf1[i]["form_code"]
        title = pdf1[i]["title"]
        last_updated = pdf1[i]["last_updated"]
        form_page_url = pdf1[i]["pdf_url"]
        pdf_url = pdf2[i]["pdf_url"]
        how_to_fill_instructions  = pdf2[i]["how_to_fill_instructions"]

        rag_document = {
            "form_code": form_code,
            "title": title,
            "last_updated": last_updated,
            "form_page_url": form_page_url,
            "pdf_url": pdf_url,
            "how_to_fill_instructions": how_to_fill_instructions
        }

        with open("ircc_forms_details.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps(rag_document, ensure_ascii=False) + "\n")
        print(f"Processed form: {form_code}")
        print("Processing Done")

    else:
        print(f"Mismatch found at index {i}: pdf_link1 = {pdf_link1}, pdf_link2 = {pdf_link2}")
        break
