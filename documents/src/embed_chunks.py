import json
import chromadb
from sentence_transformers import SentenceTransformer

# Load chunks
with open("data/processed/chunks.json", "r") as f:
    chunks = json.load(f)

print(f"Loaded {len(chunks)} chunks")

# Embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Chroma
client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_or_create_collection(
    name="omsa_reviews"
)

for chunk in chunks:
    embedding = model.encode(chunk["text"]).tolist()

    collection.add(
        ids=[chunk["chunk_id"]],
        embeddings=[embedding],
        documents=[chunk["text"]],
        metadatas=[
            {
                "source": chunk["source_file"]
            }
        ]
    )

print("Finished embedding chunks")