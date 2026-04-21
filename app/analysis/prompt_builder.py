from __future__ import annotations

import json

from app.models import CodeChunk, Requirement


def build_check_prompt(requirement: Requirement, evidence_chunks: list[CodeChunk]) -> str:
    evidence_data = [c.model_dump() for c in evidence_chunks]
    return (
        "Ты проверяешь соответствие кода требованию. "
        "Опирайся только на требование и доказательства. Не выдумывай факты.\n"
        "Верни JSON строго с полями: "
        "requirement_id, requirement_text, status(ok|wrong|missing|unclear), "
        "category(implemented_incorrectly|missing_or_not_found|none), summary, evidence, "
        "reasoning_summary, confidence.\n"
        f"Требование: {requirement.model_dump_json(ensure_ascii=False)}\n"
        f"Доказательства: {json.dumps(evidence_data, ensure_ascii=False)}"
    )
