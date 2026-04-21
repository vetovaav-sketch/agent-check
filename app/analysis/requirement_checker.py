from __future__ import annotations

from app.analysis.prompt_builder import build_check_prompt
from app.models import CheckCategory, CheckStatus, CodeChunk, Requirement, RequirementCheckResult
from app.openai_client import OpenAIClient


def _local_mvp_check(requirement: Requirement, relevant_chunks: list[CodeChunk]) -> RequirementCheckResult:
    # Простой безопасный режим: выводы только по найденным кускам кода.
    if not relevant_chunks:
        return RequirementCheckResult(
            requirement_id=requirement.requirement_id,
            requirement_text=requirement.text,
            status=CheckStatus.MISSING,
            category=CheckCategory.MISSING_OR_NOT_FOUND,
            summary="Не найдено подтверждение реализации в проверенном коде.",
            evidence=[],
            reasoning_summary="Поиск не вернул релевантные участки кода.",
            confidence=0.8,
        )

    joined = "\n".join(chunk.code_excerpt.lower() for chunk in relevant_chunks[:3])
    words = [w.lower() for w in requirement.text.split() if len(w) > 3]
    coverage = sum(1 for w in words if w in joined) / max(1, len(words))

    if coverage > 0.45:
        status = CheckStatus.UNCLEAR
        category = CheckCategory.NONE
        summary = "Есть связанный код, но без AI-проверки нельзя уверенно подтвердить полное соответствие."
        reasoning = "Найдены совпадения по ключевым словам, но этого мало для строгого вывода."
        confidence = 0.45
    else:
        status = CheckStatus.MISSING
        category = CheckCategory.MISSING_OR_NOT_FOUND
        summary = "Найдены слабо связанные фрагменты, явной реализации требования не видно."
        reasoning = "Ключевые слова требования почти не встречаются в найденных чанках."
        confidence = 0.7

    return RequirementCheckResult(
        requirement_id=requirement.requirement_id,
        requirement_text=requirement.text,
        status=status,
        category=category,
        summary=summary,
        evidence=relevant_chunks[:5],
        reasoning_summary=reasoning,
        confidence=confidence,
    )


def check_requirement(requirement: Requirement, relevant_chunks: list[CodeChunk], client: OpenAIClient, use_ai: bool = True) -> RequirementCheckResult:
    # Если есть API-ключ и AI не отключен — используем модель.
    if use_ai and client.enabled:
        prompt = build_check_prompt(requirement, relevant_chunks)
        raw = client.structured_check(prompt)
        return RequirementCheckResult.model_validate(raw)

    # Иначе используем локальную простую проверку.
    return _local_mvp_check(requirement, relevant_chunks)
