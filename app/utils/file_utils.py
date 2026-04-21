from __future__ import annotations

from pathlib import Path

BINARY_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".ico", ".pdf", ".zip", ".tar", ".gz", ".7z", ".exe", ".dll", ".so", ".dylib", ".class", ".jar", ".pyc"
}


def is_binary_or_ignored(path: Path) -> bool:
    return path.suffix.lower() in BINARY_EXTENSIONS


def ensure_parent_dir(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
