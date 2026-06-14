import os
import random

def load_documents(folder="documents"):
    docs = []
    for filename in os.listdir(folder):
        if filename.endswith(".txt"):
            path = os.path.join(folder, filename)
            with open(path, "r", encoding="utf-8") as f:
                text = f.read().strip()
            docs.append({"source": filename, "text": text})
    print(f"Loaded {len(docs)} documents")
    return docs

def clean_text(text):
    # Remove extra blank lines
    lines = [line.strip() for line in text.splitlines()]
    lines = [line for line in lines if line]
    return "\n".join(lines)

def chunk_text(text, chunk_size=300, overlap=50):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        if len(chunk.strip()) > 20:
            chunks.append(chunk)
        start += chunk_size - overlap
    return chunks

def ingest_all(folder="documents"):
    docs = load_documents(folder)
    all_chunks = []
    for doc in docs:
        cleaned = clean_text(doc["text"])
        chunks = chunk_text(cleaned)
        for i, chunk in enumerate(chunks):
            all_chunks.append({
                "text": chunk,
                "source": doc["source"],
                "chunk_index": i
            })
    print(f"Total chunks: {len(all_chunks)}")
    return all_chunks

if __name__ == "__main__":
    chunks = ingest_all()
    
    # Print 5 random chunks to inspect
    print("\n--- SAMPLE CHUNKS ---")
    for c in random.sample(chunks, min(5, len(chunks))):
        print(f"\nSource: {c['source']} | Chunk {c['chunk_index']}")
        print(c["text"])
        print("-" * 40)