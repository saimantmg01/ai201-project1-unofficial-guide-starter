import argparse
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

from ingest import build_chunks

MODEL_NAME = "all-MiniLM-L6-v2"
CHROMA_PATH = "chroma_db"
COLLECTION_NAME = "hunter_guide"
DEFAULT_TOP_K = 4

TEST_QUERIES = [
    "Which subway line stops directly at Hunter College's main 68th Street campus?",
    "Is Hunter-affiliated housing guaranteed to students?",
    "What alternatives do students discuss when Hunter housing is unavailable or too expensive?",
    "What should a student consider before choosing a long commute instead of housing near Hunter?",
    "What rental warning signs can indicate an illegal or unsafe NYC apartment?",
]


def load_model() -> SentenceTransformer:
    return SentenceTransformer(MODEL_NAME)


def get_client(db_path: str = CHROMA_PATH) -> chromadb.PersistentClient:
    Path(db_path).mkdir(parents=True, exist_ok=True)
    return chromadb.PersistentClient(path=db_path)


def embed_and_store(
    chunks: list[dict],
    model: SentenceTransformer,
    db_path: str = CHROMA_PATH,
) -> chromadb.Collection:
    if not chunks:
        raise ValueError("No chunks were provided for indexing")

    client = get_client(db_path)
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    collection = client.create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )

    texts = [chunk["text"] for chunk in chunks]
    embeddings = model.encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=True,
    ).tolist()
    ids = [
        f"{chunk['source']}:{chunk['chunk_index']}"
        for chunk in chunks
    ]
    metadatas = [
        {
            "source": chunk["source"],
            "title": chunk["title"],
            "source_type": chunk["source_type"],
            "url": chunk["url"],
            "chunk_index": chunk["chunk_index"],
        }
        for chunk in chunks
    ]

    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=texts,
        metadatas=metadatas,
    )
    return collection


def load_collection(
    db_path: str = CHROMA_PATH,
) -> chromadb.Collection:
    client = get_client(db_path)
    try:
        return client.get_collection(COLLECTION_NAME)
    except Exception as exc:
        raise RuntimeError(
            "The vector store is missing. Run `python retrieval.py --index` first."
        ) from exc


def retrieve(
    query: str,
    model: SentenceTransformer,
    collection: chromadb.Collection,
    k: int = DEFAULT_TOP_K,
) -> list[dict]:
    if not query.strip():
        raise ValueError("Query cannot be empty")

    query_embedding = model.encode(
        [query],
        normalize_embeddings=True,
    ).tolist()
    result = collection.query(
        query_embeddings=query_embedding,
        n_results=min(k, collection.count()),
        include=["documents", "metadatas", "distances"],
    )

    return [
        {
            "text": document,
            "distance": distance,
            **metadata,
        }
        for document, metadata, distance in zip(
            result["documents"][0],
            result["metadatas"][0],
            result["distances"][0],
        )
    ]


def print_results(query: str, results: list[dict]) -> None:
    print(f"\nQuery: {query}")
    print("=" * 80)
    for rank, result in enumerate(results, start=1):
        print(
            f"{rank}. distance={result['distance']:.3f} "
            f"source={result['source']} chunk={result['chunk_index']}"
        )
        print(f"   title: {result['title']}")
        print(f"   url: {result['url']}")
        print(f"   text: {result['text']}\n")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Index and test semantic retrieval for the Hunter guide."
    )
    parser.add_argument(
        "--index",
        action="store_true",
        help="Rebuild the ChromaDB collection before querying.",
    )
    parser.add_argument(
        "--query",
        help="Run one query instead of the five evaluation queries.",
    )
    parser.add_argument(
        "-k",
        type=int,
        default=DEFAULT_TOP_K,
        help=f"Number of chunks to retrieve (default: {DEFAULT_TOP_K}).",
    )
    args = parser.parse_args()

    model = load_model()
    if args.index:
        chunks = build_chunks()
        collection = embed_and_store(chunks, model)
        print(f"Indexed {collection.count()} chunks in {CHROMA_PATH}/")
    else:
        collection = load_collection()

    queries = [args.query] if args.query else TEST_QUERIES
    for query in queries:
        print_results(query, retrieve(query, model, collection, args.k))


if __name__ == "__main__":
    main()
