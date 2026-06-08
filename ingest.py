import os
import re
import random

DOCUMENTS_FOLDER = "documents"
SKIP_FILES = {"README.txt", ".gitkeep"}


def load_documents(folder_path: str = DOCUMENTS_FOLDER) -> list[dict]:
    docs = []
    for filename in sorted(os.listdir(folder_path)):
        if not filename.endswith(".txt") or filename in SKIP_FILES:
            continue
        filepath = os.path.join(folder_path, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            raw = f.read()
        meta, content = _parse_document(raw)
        docs.append({
            "source": filename,
            "title": meta.get("title", ""),
            "source_type": meta.get("source_type", ""),
            "url": meta.get("url", ""),
            "text": content,
        })
    return docs


def _parse_document(raw: str) -> tuple[dict, str]:
    lines = raw.strip().split("\n")
    meta = {}
    content_lines = []
    in_header = True

    for line in lines:
        if in_header:
            if line.startswith("TITLE:"):
                meta["title"] = line[len("TITLE:"):].strip()
            elif line.startswith("SOURCE TYPE:"):
                meta["source_type"] = line[len("SOURCE TYPE:"):].strip()
            elif line.startswith("URL:"):
                meta["url"] = line[len("URL:"):].strip()
            elif line.startswith(("RETRIEVED:", "POSTED:")):
                pass
            elif line.strip() == "" and meta:
                in_header = False
        else:
            content_lines.append(line)

    content = "\n".join(content_lines).strip()
    return meta, content


def clean_text(text: str) -> str:
    # Remove RELIABILITY NOTE and everything after it
    text = re.sub(r"\nRELIABILITY NOTE:.*", "", text, flags=re.DOTALL)
    # Collapse 3+ newlines to 2
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def chunk_text(
    text: str,
    chunk_size: int = 250,
    overlap: int = 40,
) -> list[str]:
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    text = text.strip()
    chunks = []
    start = 0

    while start < len(text):
        max_end = min(start + chunk_size, len(text))
        end = max_end

        if max_end < len(text):
            search_area = text[start:max_end]
            boundaries = [
                search_area.rfind("\n\n"),
                search_area.rfind("\n"),
                search_area.rfind(". "),
                search_area.rfind(" "),
            ]
            best_boundary = max(boundaries)
            if best_boundary >= chunk_size // 2:
                end = start + best_boundary + 1

        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)

        if end >= len(text):
            break

        start = end - overlap
        next_space = text.find(" ", start)
        if next_space != -1 and next_space < end:
            start = next_space + 1

    return chunks


def build_chunks(folder_path: str = DOCUMENTS_FOLDER) -> list[dict]:
    docs = load_documents(folder_path)
    all_chunks = []
    for doc in docs:
        cleaned = clean_text(doc["text"])
        for i, chunk in enumerate(chunk_text(cleaned)):
            all_chunks.append({
                "text": chunk,
                "source": doc["source"],
                "title": doc["title"],
                "source_type": doc["source_type"],
                "url": doc["url"],
                "chunk_index": i,
            })
    return all_chunks


if __name__ == "__main__":
    documents = load_documents()
    cleaned_sample = clean_text(documents[0]["text"])
    print(f"Loaded documents: {len(documents)}")
    print(f"\nCleaned document sample ({documents[0]['source']}):")
    print("=" * 60)
    print(cleaned_sample)

    chunks = build_chunks()
    print(f"\nTotal chunks: {len(chunks)}\n")

    print("5 random chunks:")
    print("=" * 60)
    for chunk in random.sample(chunks, min(5, len(chunks))):
        print(f"Source : {chunk['source']}")
        print(f"Type   : {chunk['source_type']}")
        print(f"URL    : {chunk['url']}")
        print(f"Length : {len(chunk['text'])} chars")
        print(f"Text   : {chunk['text']}")
        print()
