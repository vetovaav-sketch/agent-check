from __future__ import annotations

import json

from app.models import CodeChunk, Requirement


def build_check_prompt(requirement: Requirement, evidence_chunks: list[CodeChunk]) -> str:
    evidence_data = [c.model_dump() for c in evidence_chunks]
    return (
        "Ты проверяешь ОДНО требование за раз.\n"
        "Правила: \n"
        "1) Не выдумывай факты.\n"
        "2) Делай выводы только по переданным доказательствам.\n"
        "3) Если доказательств недостаточно, ставь status=unclear или missing.\n"
        "4) Поле evidence заполняй только объектами из переданного списка с file_path и line numbers.\n"
        "Верни JSON строго с полями: "
        "requirement_id, requirement_text, status(ok|wrong|missing|unclear), "
        "category(implemented_incorrectly|missing_or_not_found|none), summary, evidence, "
        "reasoning_summary, confidence.\n"
        f"Требование: {requirement.model_dump_json(ensure_ascii=False)}\n"
        f"Доказательства: {json.dumps(evidence_data, ensure_ascii=False)}"
    )
