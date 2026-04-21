from __future__ import annotations

from app.models import CheckCategory, RequirementCheckResult


def split_findings(results: list[RequirementCheckResult]) -> tuple[list[RequirementCheckResult], list[RequirementCheckResult]]:
    wrong = [r for r in results if r.category == CheckCategory.IMPLEMENTED_INCORRECTLY]
    missing = [
        r
        for r in results
        if r.category == CheckCategory.MISSING_OR_NOT_FOUND or r.status in {"missing", "unclear"}
    ]
    return wrong, missing
