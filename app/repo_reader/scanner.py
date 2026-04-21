from __future__ import annotations

from pathlib import Path
from typing import List

from app.repo_reader.filters import should_exclude_dir, should_exclude_file


def scan_repository(repo_path: str, max_files: int | None = None, include_tests: bool = False) -> List[Path]:
    root = Path(repo_path)
    files: List[Path] = []

    for path in root.rglob("*"):
        if path.is_dir() and should_exclude_dir(path):
            continue
        if not path.is_file():
            continue
        if any(part in {".git", "node_modules", "dist", "build", "target", ".venv", "venv", "__pycache__"} for part in path.parts):
            continue
        if should_exclude_file(path):
            continue
        if not include_tests and "test" in path.name.lower():
            continue
        files.append(path)
        if max_files and len(files) >= max_files:
            break

    return files
