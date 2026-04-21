from pathlib import Path

from docx import Document

from app.requirements_parser.extractor import extract_text


def test_extract_txt(tmp_path: Path) -> None:
    f = tmp_path / "spec.txt"
    f.write_text("1. Требование A\n2. Требование B", encoding="utf-8")
    text = extract_text(str(f))
    assert "Требование A" in text


def test_extract_docx(tmp_path: Path) -> None:
    f = tmp_path / "spec.docx"
    doc = Document()
    doc.add_paragraph("Требование из docx")
    doc.save(f)
    text = extract_text(str(f))
    assert "docx" in text
