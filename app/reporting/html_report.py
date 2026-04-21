from __future__ import annotations

from pathlib import Path

from app.analysis.aggregator import split_findings
from app.models import RequirementCheckResult


def _card(r: RequirementCheckResult) -> str:
    evidence = "".join(
        f"<li><b>{e.file_path}:{e.line_start}-{e.line_end}</b><pre>{e.code_excerpt[:1200]}</pre></li>" for e in r.evidence
    ) or "<li>Нет доказательств</li>"
    return (
        f"<article><h3>{r.requirement_id}</h3>"
        f"<p><b>Требование:</b> {r.requirement_text}</p>"
        f"<p><b>Проблема:</b> {r.summary}</p>"
        f"<p><b>Почему это нарушение:</b> {r.reasoning_summary}</p>"
        f"<p><b>Confidence:</b> {r.confidence:.2f}</p>"
        f"<ul>{evidence}</ul></article>"
    )


def render_html_report(results: list[RequirementCheckResult], output_path: str) -> None:
    wrong, missing = split_findings(results)
    html = [
        "<html><head><meta charset='utf-8'><title>Отчет</title></head><body>",
        "<h1>Отчет по соответствию требований</h1>",
        "<h2>Реализовано неправильно</h2>",
        *( _card(r) for r in wrong),
        "<h2>Отсутствует или не найдено в коде</h2>",
        *( _card(r) for r in missing),
        "</body></html>",
    ]
    Path(output_path).write_text("\n".join(html), encoding="utf-8")
