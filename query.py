import os

from dotenv import load_dotenv
from groq import Groq

from retrieval import DEFAULT_TOP_K, load_collection, load_model, retrieve

DEFAULT_GROQ_MODEL = "llama-3.3-70b-versatile"
MAX_RELEVANT_DISTANCE = 0.50
INSUFFICIENT_INFORMATION = "I don't have enough information on that."

SYSTEM_PROMPT = """You are the Hunter College Housing and Commuting Guide.
Answer the user's question using only the supplied source excerpts.

Rules:
1. Do not use outside knowledge or make assumptions.
2. If the excerpts do not contain enough information, reply exactly:
   I don't have enough information on that.
3. Distinguish official information from individual student experiences.
4. Cite factual claims with the supplied source labels, such as [Source 1].
5. Keep the answer concise and practical.
"""

_embedding_model = None
_collection = None


def _get_retrieval_resources():
    global _embedding_model, _collection
    if _embedding_model is None:
        _embedding_model = load_model()
    if _collection is None:
        _collection = load_collection()
    return _embedding_model, _collection


def _format_context(results: list[dict]) -> str:
    sections = []
    for index, result in enumerate(results, start=1):
        sections.append(
            "\n".join(
                [
                    f"[Source {index}]",
                    f"Title: {result['title']}",
                    f"Source type: {result['source_type']}",
                    f"URL: {result['url']}",
                    f"Excerpt: {result['text']}",
                ]
            )
        )
    return "\n\n".join(sections)


def _unique_sources(results: list[dict]) -> list[dict]:
    sources = []
    seen = set()
    for result in results:
        key = (result["title"], result["url"])
        if key in seen:
            continue
        seen.add(key)
        sources.append(
            {
                "title": result["title"],
                "url": result["url"],
                "source_type": result["source_type"],
                "distance": result["distance"],
            }
        )
    return sources


def ask(question: str, k: int = DEFAULT_TOP_K) -> dict:
    question = question.strip()
    if not question:
        raise ValueError("Please enter a question.")

    model, collection = _get_retrieval_resources()
    results = retrieve(question, model, collection, k)

    if not results or results[0]["distance"] > MAX_RELEVANT_DISTANCE:
        return {
            "answer": INSUFFICIENT_INFORMATION,
            "sources": [],
            "retrieved_chunks": results,
        }

    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY", "").strip()
    if not api_key or api_key == "your_key_here":
        raise RuntimeError("GROQ_API_KEY is missing from .env.")

    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        model=os.getenv("GROQ_MODEL", DEFAULT_GROQ_MODEL),
        temperature=0,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": (
                    f"Question: {question}\n\n"
                    f"Source excerpts:\n{_format_context(results)}"
                ),
            },
        ],
    )
    answer = response.choices[0].message.content.strip()

    return {
        "answer": answer,
        "sources": _unique_sources(results),
        "retrieved_chunks": results,
    }


if __name__ == "__main__":
    print("Hunter College Housing and Commuting Guide")
    print("Enter a question, or type 'quit' to exit.\n")
    while True:
        user_question = input("Question: ").strip()
        if user_question.lower() in {"quit", "exit"}:
            break
        try:
            result = ask(user_question)
            print(f"\n{result['answer']}")
            if result["sources"]:
                print("\nSources:")
                for source in result["sources"]:
                    print(f"- {source['title']}: {source['url']}")
            print()
        except Exception as exc:
            print(f"\nError: {exc}\n")
