from __future__ import annotations

from app.models import CodeChunk


class InMemoryVectorStore:
    def __init__(self) -> None:
        self._chunks: list[CodeChunk] = []

    def add_chunks(self, chunks: list[CodeChunk]) -> None:
        self._chunks.extend(chunks)

    def search(self, query: str, limit: int = 8) -> list[CodeChunk]:
        tokens = {t.lower() for t in query.split() if len(t) > 2}
        scored: list[tuple[int, CodeChunk]] = []
        for chunk in self._chunks:
            text = chunk.code_excerpt.lower()
            score = sum(1 for token in tokens if token in text)
            if score > 0:
                scored.append((score, chunk))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [c for _, c in scored[:limit]]
