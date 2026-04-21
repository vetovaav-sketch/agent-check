from pathlib import Path

EXCLUDED_DIRS = {".git", "node_modules", "dist", "build", "target", ".venv", "venv", "__pycache__"}
EXCLUDED_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".zip", ".tar", ".gz", ".7z", ".pdf", ".exe", ".dll", ".so", ".dylib"}


def should_exclude_dir(path: Path) -> bool:
    return path.name in EXCLUDED_DIRS


def should_exclude_file(path: Path) -> bool:
    return path.suffix.lower() in EXCLUDED_EXTS
