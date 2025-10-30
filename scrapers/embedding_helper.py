import json
import os
import time
from tqdm import tqdm
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain.schema import Document

# ==================Config==============
INPUT_FILE = "immigration_chunks_ircc.jsonl"
PERSIST_DIR = "./chroma_immigration"
BATCH_SIZE = 1000
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# ================Setup===============
print("Starting RAG ingestion...")
print(f"Input: {INPUT_FILE}")
print(f"Output: {PERSIST_DIR}")
print(f"Batch size: {BATCH_SIZE}")
print(f"Model: {EMBEDDING_MODEL}\n")

# load embedding model once
embeddings = HuggingFaceEmbeddings(
    model = EMBEDDING_MODEL,
    encode_kwargs={"batch_size": 32}
)

# Track progress: use a marker file to know where we left off
progress_file = os.path.join(PERSIST_DIR, "ingestion_progress.txt")
start_line = 0
if os.path.exists(progress_file):
    with open(progress_file, "r") as f:
        content = f.read().strip()
        if content:  # Only convert if not empty
            start_line = int(content)
        else:
            print("⚠️ Progress file is empty. Starting from line 0.")
    print(f"⏭ Resuming from line {start_line}")

# Count total lines (for progress bar)
print("🔍 Counting total lines (this may take a moment)...")
total_lines = 0
with open(INPUT_FILE, "r",encoding="utf-8") as f:
    for _ in f:
        total_lines += 1
print(f"Total chunks to process: {total_lines:,}")

with open(INPUT_FILE, "r",encoding="utf-8") as f:
    for _ in range(start_line):
        next(f,None)

    # Initialize vectorstore (load if exists, else create)
    vectorstore = None
    if os.path.exists(PERSIST_DIR):
        try:
            vectorstore = Chroma(
                persist_directory=PERSIST_DIR,
                embedding_function=embeddings
            )
            print("Loaded existing ChromaDB")
        except Exception as e:
            print(f"⚠️ Could not load existing DB: {e}. Starting fresh.")
            vectorstore = None

    # Main ingestion loop
    documents = []
    current_line = start_line

    pbar = tqdm(
        total=total_lines,
        initial=start_line,
        desc="Ingesting chunks",
        unit="chunk"
    )

    start_time = time.time()

    for line in f:
        try:
            data = json.loads(line)
            doc = Document(
                page_content=data["content"],
                metadata={
                    "id": data["id"],
                    "url": data["url"],
                    "title": data["title"],
                    "description": data["description"],
                    "timestamp": data["timestamp"],
                    "content_length": data["content_length"],
                    "language": data["language"],
                    "source": "canadavisa",    #this needs to be changed for new sources
                    "document_type": data["document_type"],
                    "ingestion_batch": "2025-10-04" #this needs to be changed for new sources
                }
            )
            documents.append(doc)
        except Exception as e:
            print(f"Skipping invalid line {current_line}: {e}")
            current_line += 1
            pbar.update(1)
            continue

        # Process batch
        if len(documents) >= BATCH_SIZE:
            batch_start_time = time.time()
            try:
                if vectorstore is None:
                    vectorstore = Chroma.from_documents(
                        documents,
                        embeddings,
                        persist_directory=PERSIST_DIR
                    )
                else:
                    vectorstore.add_documents(documents)
            except Exception as e:
                print(f"\nError adding batch: {e}")
                documents = []
                current_line += BATCH_SIZE
                pbar.update(BATCH_SIZE)
                continue

            current_line += len(documents)
            with open(progress_file,"w") as pf:
                pf.write(str(current_line))
            
            elapsed = time.time() - batch_start_time
            rate = len(documents) / elapsed if elapsed > 0 else 0
            pbar.set_postfix({"batch_time" : f"{elapsed:.1f}", "rate" : f"{rate:.1f}/s"})
            pbar.update(len(documents))
            documents = []

    if documents:
        print(f"\n Processing final batch ({len(documents)} chunks)...")
        try:
            if vectorstore is None:
                vectorstore = Chroma.from_documents(
                    documents,
                    embeddings,
                    persist_directory=PERSIST_DIR
                )
            else:
                vectorstore.add_documents(documents)

            current_line += len(documents)
            with open(progress_file, "w") as pf:
                pf.write(str(current_line))

        except Exception as e:
            print(f"Final batch error: {e}")
            
    pbar.close()

# =========== Final Status ===========

total_time = time.time() - start_time
hours, rem = divmod(total_time, 3600)
minutes, seconds = divmod(rem, 60)
print("\nIngestion complete!")
print(f"Saved to: {PERSIST_DIR}")
print(f"Total time: {int(hours)}h {int(minutes)}m {seconds:.1f}s")
print(f"Avg speed: {total_lines / total_time:.1f} chunks/sec")
print("Your Immigration RAG system is ready!")
        



