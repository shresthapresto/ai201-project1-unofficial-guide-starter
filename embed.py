import chromadb
from sentence_transformers import SentenceTransformer
from ingest import ingest_all

def build_vector_store(folder="documents"):
    chunks = ingest_all(folder)
    
    print("Loading embedding model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")
    
    client = chromadb.PersistentClient(path="./chroma_db")
    
    # Delete existing collection if rebuilding
    try:
        client.delete_collection("unofficial_guide")
    except:
        pass
    
    collection = client.create_collection("unofficial_guide")
    
    texts = [c["text"] for c in chunks]
    metadatas = [{"source": c["source"], "chunk_index": c["chunk_index"]} for c in chunks]
    ids = [f"chunk_{i}" for i in range(len(chunks))]
    
    print("Embedding chunks...")
    embeddings = model.encode(texts, show_progress_bar=True).tolist()
    
    collection.add(
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids
    )
    
    print(f"Stored {len(chunks)} chunks in ChromaDB")
    return collection

if __name__ == "__main__":
    build_vector_store()