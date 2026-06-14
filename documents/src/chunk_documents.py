from pathlib import Path
import re
import json
import random
from html import unescape

RAW_DIR = Path("data/raw")
OUT_DIR = Path("data/processed")
OUT_DIR.mkdir(parents=True, exist_ok=True)

CHUNK_SIZE = 750
OVERLAP = 100


def clean_text(text: str) -> str:
    text = unescape(text)

    # Remove HTML tags
    text = re.sub(r"<[^>]+>", " ", text)

    # Remove common boilerplate-ish phrases
    boilerplate_patterns = [
        r"Cookie Policy",
        r"Privacy Policy",
        r"Terms of Service",
        r"Log In",
        r"Sign Up",
        r"Read More",
        r"Share",
        r"Subscribe",
    ]

    for pattern in boilerplate_patterns:
        text = re.sub(pattern, " ", text, flags=re.IGNORECASE)

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text).strip()

    return text


def chunk_text(text: str, chunk_size: int = 150, overlap: int = 30):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()

        if len(chunk) > 0:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def load_documents():
    documents = []

    for path in RAW_DIR.glob("*.txt"):
        raw_text = path.read_text(encoding="utf-8")
        cleaned = clean_text(raw_text)

        documents.append({
            "source_file": path.name,
            "text": cleaned
        })

    return documents


def main():
    documents = load_documents()

    print(f"Loaded {len(documents)} documents.")

    all_chunks = []

    for doc in documents:
        chunks = chunk_text(doc["text"])

        for i, chunk in enumerate(chunks):
            all_chunks.append({
                "chunk_id": f"{doc['source_file']}_{i}",
                "source_file": doc["source_file"],
                "text": chunk
            })

    output_path = OUT_DIR / "chunks.json"
    output_path.write_text(json.dumps(all_chunks, indent=2), encoding="utf-8")

    print(f"Created {len(all_chunks)} chunks.")
    print(f"Saved chunks to {output_path}")

    print("\n===== 5 RANDOM CHUNKS FOR INSPECTION =====\n")

    sample_size = min(5, len(all_chunks))

    for chunk in random.sample(all_chunks, sample_size):
        print(f"Source: {chunk['source_file']}")
        print(f"Chunk ID: {chunk['chunk_id']}")
        print(chunk["text"])
        print("\n" + "-" * 80 + "\n")


if __name__ == "__main__":
    main()