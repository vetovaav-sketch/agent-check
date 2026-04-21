from __future__ import annotations

from difflib import SequenceMatcher

from app.models import CodeChunk, Requirement


def keyword_search(requirement: Requirement, chunks: list[CodeChunk], limit: int = 10) -> list[CodeChunk]:
    # Ищем простые совпадения слов из требования в тексте кода.
    words = [w.lower() for w in requirement.text.split() if len(w) > 2]
    scored: list[tuple[int, CodeChunk]] = []
    for chunk in chunks:
        content = f"{chunk.file_path}\n{chunk.code_excerpt}".lower()
        score = sum(1 for w in words if w in content)
        if score:
            scored.append((score, chunk))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [c for _, c in scored[:limit]]


def similarity_search(requirement: Requirement, chunks: list[CodeChunk], limit: int = 10) -> list[CodeChunk]:
    # Если слов почти нет, используем грубую похожесть текста.
    scored: list[tuple[float, CodeChunk]] = []
    for chunk in chunks:
        ratio = SequenceMatcher(None, requirement.text.lower(), chunk.code_excerpt.lower()).ratio()
        if ratio > 0.07:
            scored.append((ratio, chunk))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [c for _, c in scored[:limit]]


def find_relevant_chunks(requirement: Requirement, chunks: list[CodeChunk], limit: int) -> list[CodeChunk]:
    found = keyword_search(requirement, chunks, limit)
    if found:
        return found
    return similarity_search(requirement, chunks, limit)
