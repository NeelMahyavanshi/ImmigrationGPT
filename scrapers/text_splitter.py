from langchain.text_splitter import RecursiveCharacterTextSplitter
import json
from tqdm import tqdm


scissors = RecursiveCharacterTextSplitter(
    separators=["\n\n", "\n", ". ", "!", "?", " ", ""],
    chunk_size = 300,
    chunk_overlap = 50
)

def content_splitter(input_file):
    output_file = "immigration_chunks_ircc.jsonl"

    with open(input_file, "r",encoding="utf-8") as infile:
        total_lines = sum(1 for _ in open(input_file, "r",encoding="utf-8"))
        infile.seek(0)

        with open(output_file, "w", encoding="utf-8") as outfile:
            for line in tqdm(infile ,  total=total_lines, desc="Splitting documents"):
                line = line.strip()
                if not line:
                    continue

                try:
                    doc = json.loads(line)
                
                except json.JSONDecodeError:
                    print(f"Skipping invalid JSON line: {line[:100]}...")
                    continue

                content = doc.get("content")
                if not content or not isinstance(content, str) or not content.strip():
                    print(f"Skipping document with missing/empty content. ID: {doc.get('id', 'unknown')}")
                    continue
                
                chunks = scissors.split_text(doc["content"])

                for i, chunk in enumerate(chunks):
                    small_piece = {
                        "id": f"{doc['id']}_part{i+1}",
                        "url": doc["url"],
                        "title": doc["title"],
                        "description" : doc["description"],
                        "content": chunk,
                        "timestamp" : doc["timestamp"],
                        "content_length": len(chunk),
                        "language": doc["language"],
                        "source": doc["source"],
                        "document_type": "text"
                    }

                
                    outfile.write(json.dumps(small_piece, ensure_ascii=False) + "\n")

    print(f"✅ Done! Chunks saved to {output_file}")

if __name__ == "__main__":
    content_splitter("immigration_ircc_content.jsonl")