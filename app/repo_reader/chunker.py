from __future__ import annotations

from pathlib import Path
from typing import List

from app.models import CodeChunk


def chunk_file(path: Path, repo_root: Path, chunk_size: int = 60, overlap: int = 10) -> List[CodeChunk]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    lines = text.splitlines()
    chunks: List[CodeChunk] = []

    i = 0
    while i < len(lines):
        end = min(len(lines), i + chunk_size)
        excerpt = "\n".join(lines[i:end]).strip()
        if excerpt:
            chunks.append(
                CodeChunk(
                    file_path=str(path.relative_to(repo_root)),
                    line_start=i + 1,
                    line_end=end,
                    code_excerpt=excerpt,
                )
            )
        if end == len(lines):
            break
        i = max(i + 1, end - overlap)

    return chunks


def chunk_repository(files: list[Path], repo_root: str) -> List[CodeChunk]:
    root = Path(repo_root)
    all_chunks: List[CodeChunk] = []
    for file in files:
        all_chunks.extend(chunk_file(file, root))
    return all_chunks
