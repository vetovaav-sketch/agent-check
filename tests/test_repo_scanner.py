from pathlib import Path

from app.repo_reader.scanner import scan_repository


def test_scanner_excludes_noise(tmp_path: Path) -> None:
    (tmp_path / ".git").mkdir()
    (tmp_path / "node_modules").mkdir()
    (tmp_path / "src").mkdir()
    (tmp_path / ".git" / "a.py").write_text("x")
    (tmp_path / "node_modules" / "b.js").write_text("x")
    (tmp_path / "src" / "main.py").write_text("print('ok')")

    files = scan_repository(str(tmp_path))
    rel = [f.relative_to(tmp_path).as_posix() for f in files]
    assert rel == ["src/main.py"]
