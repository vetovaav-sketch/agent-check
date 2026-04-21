from pathlib import Path

from app.models import CheckCategory, CheckStatus, RequirementCheckResult
from app.reporting.markdown_report import render_markdown_report


def test_markdown_report_sections(tmp_path: Path) -> None:
    out = tmp_path / "report.md"
    results = [
        RequirementCheckResult(
            requirement_id="R1",
            requirement_text="x",
            status=CheckStatus.MISSING,
            category=CheckCategory.MISSING_OR_NOT_FOUND,
            summary="Нет",
            evidence=[],
            reasoning_summary="Не найдено",
            confidence=0.9,
        )
    ]
    render_markdown_report(results, str(out))
    text = out.read_text(encoding="utf-8")
    assert "Реализовано неправильно" in text
    assert "Отсутствует или не найдено в коде" in text
