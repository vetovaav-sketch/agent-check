from __future__ import annotations

from pathlib import Path

from app.analysis.aggregator import split_findings
from app.models import RequirementCheckResult


def _item_block(r: RequirementCheckResult) -> str:
    evidence_text = "\n".join(
        [
            f"- `{e.file_path}:{e.line_start}-{e.line_end}`\n```\n{e.code_excerpt[:1200]}\n```"
            for e in r.evidence
        ]
    ) or "- Нет доказательств"

    return (
        f"### {r.requirement_id}\n"
        f"**Требование:** {r.requirement_text}\n\n"
        f"**Проблема:** {r.summary}\n\n"
        f"**Почему это нарушение:** {r.reasoning_summary}\n\n"
        f"**Confidence:** {r.confidence:.2f}\n\n"
        f"**Доказательства:**\n{evidence_text}\n"
    )


def render_markdown_report(results: list[RequirementCheckResult], output_path: str) -> None:
    wrong, missing = split_findings(results)
    body = ["# Отчет по соответствию требований\n"]
    body.append("## Реализовано неправильно\n")
    body.extend(_item_block(r) for r in wrong)
    body.append("\n## Отсутствует или не найдено в коде\n")
    body.extend(_item_block(r) for r in missing)
    Path(output_path).write_text("\n".join(body), encoding="utf-8")
