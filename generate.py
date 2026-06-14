import os
from dotenv import load_dotenv
from groq import Groq
from retrieve import retrieve

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """You are a helpful assistant for students researching 
CS Master's program admissions. Answer ONLY using the information provided 
in the context documents below. Do NOT use your general training knowledge.
If the context does not contain enough information to answer the question, 
say exactly: "I don't have enough information in my documents to answer that."
Always end your response by citing which source document(s) your answer 
draws from."""

def ask(question):
    chunks = retrieve(question, top_k=5)
    context = "\n\n".join(
        f"[Source: {c['source']}]\n{c['text']}" for c in chunks
    )
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}
    ]
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        max_tokens=500
    )
    answer = response.choices[0].message.content
    sources = list({c["source"] for c in chunks})
    return {"answer": answer, "sources": sources}

if __name__ == "__main__":
    test_questions = [
        "What GPA do most admitted CMU MSCS students have?",
        "Can you get into Georgia Tech OMSCS with a GPA below 3.0?",
        "What is the best pizza place in New York?"
    ]
    for q in test_questions:
        print(f"\n=== Question: {q} ===")
        result = ask(q)
        print(result["answer"])
        print(f"\nSources: {result['sources']}")
        print("-" * 50)