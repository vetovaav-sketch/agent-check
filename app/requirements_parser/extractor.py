from __future__ import annotations

from pathlib import Path


def extract_text(requirements_path: str) -> str:
    path = Path(requirements_path)
    suffix = path.suffix.lower()

    if suffix in {".txt", ".md"}:
        return path.read_text(encoding="utf-8")

    if suffix == ".docx":
        from docx import Document

        doc = Document(requirements_path)
        return "\n".join(p.text for p in doc.paragraphs if p.text.strip())

    if suffix == ".pdf":
        from pypdf import PdfReader

        reader = PdfReader(requirements_path)
        pages = [p.extract_text() or "" for p in reader.pages]
        return "\n".join(pages)

    raise ValueError(f"Unsupported requirements format: {suffix}")
