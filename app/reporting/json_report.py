from __future__ import annotations

import json
from pathlib import Path

from app.models import RequirementCheckResult


def render_json_report(results: list[RequirementCheckResult], output_path: str) -> None:
    payload = [r.model_dump() for r in results]
    Path(output_path).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
