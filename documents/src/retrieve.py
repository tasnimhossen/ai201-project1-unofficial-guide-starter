import chromadb
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_collection(
    name="omsa_reviews"
)

while True:
    query = input("\nQuestion: ")

    if query.lower() == "quit":
        break

    embedding = model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[embedding],
        n_results=4
    )

    print("\nTop Results:\n")

    docs = results["documents"][0]
    sources = results["metadatas"][0]
    distances = results["distances"][0]

    for i in range(len(docs)):
        print("=" * 60)
        print("SOURCE:", sources[i]["source"])
        print("DISTANCE:", distances[i])
        print(docs[i])
