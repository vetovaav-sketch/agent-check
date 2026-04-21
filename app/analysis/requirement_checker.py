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


def _sanitize_ai_result(result: RequirementCheckResult, relevant_chunks: list[CodeChunk]) -> RequirementCheckResult:
    # Пропускаем только evidence, которые реально были переданы в модель.
    allowed = {(c.file_path, c.line_start, c.line_end) for c in relevant_chunks}
    filtered_evidence = [
        e for e in result.evidence if (e.file_path, e.line_start, e.line_end) in allowed
    ]

    result.evidence = filtered_evidence

    # Если доказательств нет, запрещаем уверенные выводы о корректности/некорректности.
    if not result.evidence and result.status in {CheckStatus.OK, CheckStatus.WRONG}:
        result.status = CheckStatus.UNCLEAR
        result.category = CheckCategory.MISSING_OR_NOT_FOUND
        result.summary = "Недостаточно подтвержденных доказательств для уверенного вывода."
        result.reasoning_summary = "Модель вернула вывод без валидного evidence из релевантных чанков."
        result.confidence = min(result.confidence, 0.35)

    return result


def check_requirement(requirement: Requirement, relevant_chunks: list[CodeChunk], client: OpenAIClient, use_ai: bool = True) -> RequirementCheckResult:
    # Если есть API-ключ и AI не отключен — используем модель для одного требования.
    if use_ai and client.enabled:
        prompt = build_check_prompt(requirement, relevant_chunks)
        raw = client.structured_check(prompt)
        ai_result = RequirementCheckResult.model_validate(raw)
        return _sanitize_ai_result(ai_result, relevant_chunks)

    # Иначе используем локальную простую проверку.
    return _local_mvp_check(requirement, relevant_chunks)
