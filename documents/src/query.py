from pathlib import Path
import chromadb
from sentence_transformers import SentenceTransformer

BASE_DIR = Path(__file__).resolve().parents[2]
CHROMA_PATH = BASE_DIR / "documents" / "chroma_db"

model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(path=str(CHROMA_PATH))
collection = client.get_collection(name="omsa_reviews")


def retrieve(question, top_k=4):
    query_embedding = model.encode(question).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    chunks = []

    for doc, metadata, distance in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0]
    ):
        chunks.append({
            "text": doc,
            "source": metadata["source"],
            "distance": distance
        })

    return chunks


def ask(question):
    chunks = retrieve(question)

    if len(chunks) == 0:
        return {
            "answer": "I don't have enough information in the provided documents to answer that.",
            "sources": []
        }

    answer = "Based on the retrieved documents:\n\n"

    for chunk in chunks[:3]:
        answer += f"[Source: {chunk['source']}]\n"
        answer += chunk["text"] + "\n\n"

    sources = sorted(set(chunk["source"] for chunk in chunks))

    return {
        "answer": answer,
        "sources": sources
    }


if __name__ == "__main__":
    while True:
        question = input("\nQuestion: ")

        if question.lower() == "quit":
            break

        result = ask(question)

        print("\nAnswer:")
        print(result["answer"])

        print("\nSources:")
        for source in result["sources"]:
            print("-", source)