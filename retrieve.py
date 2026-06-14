import chromadb
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_collection("unofficial_guide")

def retrieve(query, top_k=5):
    query_embedding = model.encode([query]).tolist()
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )
    chunks = []
    for doc, meta, dist in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0]
    ):
        chunks.append({
            "text": doc,
            "source": meta["source"],
            "distance": round(dist, 3)
        })
    return chunks

if __name__ == "__main__":
    # Test with 3 of your evaluation questions
    test_queries = [
        "What GPA do most admitted CMU MSCS students have?",
        "Can you get into Georgia Tech OMSCS with a GPA below 3.0?",
        "Do CS master's programs still require the GRE in 2024?"
    ]
    
    for query in test_queries:
        print(f"\n=== Query: {query} ===")
        results = retrieve(query)
        for r in results:
            print(f"[distance={r['distance']}] ({r['source']})")
            print(r["text"][:200])
            print("-" * 40)