from __future__ import annotations

from app.models import CodeChunk
from app.retrieval.embeddings import cosine_similarity, embed_text


class InMemoryVectorStore:
    def __init__(self) -> None:
        self._entries: list[tuple[CodeChunk, dict[str, float]]] = []

    def add_chunks(self, chunks: list[CodeChunk]) -> None:
        for chunk in chunks:
            text = f"{chunk.file_path}\n{chunk.code_excerpt}"
            self._entries.append((chunk, embed_text(text)))

    def search(self, query: str, limit: int = 8) -> list[CodeChunk]:
        query_vec = embed_text(query)
        scored: list[tuple[float, CodeChunk]] = []
        for chunk, vec in self._entries:
            score = cosine_similarity(query_vec, vec)
            if score > 0:
                scored.append((score, chunk))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [chunk for _, chunk in scored[:limit]]
