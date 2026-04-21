from __future__ import annotations

from difflib import SequenceMatcher

from app.models import CodeChunk, Requirement
from app.retrieval.vector_store import InMemoryVectorStore


def keyword_search(requirement: Requirement, chunks: list[CodeChunk], limit: int = 10) -> list[CodeChunk]:
    words = [w.lower() for w in requirement.text.split() if len(w) > 2]
    scored: list[tuple[int, CodeChunk]] = []
    for chunk in chunks:
        content = f"{chunk.file_path}\n{chunk.code_excerpt}".lower()
        score = sum(1 for w in words if w in content)
        if score:
            scored.append((score, chunk))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [c for _, c in scored[:limit]]


def fallback_similarity_search(requirement: Requirement, chunks: list[CodeChunk], limit: int = 10) -> list[CodeChunk]:
    scored: list[tuple[float, CodeChunk]] = []
    for chunk in chunks:
        ratio = SequenceMatcher(None, requirement.text.lower(), chunk.code_excerpt.lower()).ratio()
        if ratio > 0.07:
            scored.append((ratio, chunk))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [c for _, c in scored[:limit]]


def find_relevant_chunks(requirement: Requirement, chunks: list[CodeChunk], store: InMemoryVectorStore, limit: int) -> list[CodeChunk]:
    first_pass = keyword_search(requirement, chunks, limit)
    if first_pass:
        return first_pass
    vector_like = store.search(requirement.text, limit)
    if vector_like:
        return vector_like
    return fallback_similarity_search(requirement, chunks, limit)
