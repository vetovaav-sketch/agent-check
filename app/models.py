from __future__ import annotations

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class Requirement(BaseModel):
    requirement_id: str
    text: str


class CodeChunk(BaseModel):
    file_path: str
    line_start: int
    line_end: int
    code_excerpt: str


class CheckStatus(str, Enum):
    OK = "ok"
    WRONG = "wrong"
    MISSING = "missing"
    UNCLEAR = "unclear"


class CheckCategory(str, Enum):
    IMPLEMENTED_INCORRECTLY = "implemented_incorrectly"
    MISSING_OR_NOT_FOUND = "missing_or_not_found"
    NONE = "none"


class RequirementCheckResult(BaseModel):
    requirement_id: str
    requirement_text: str
    status: CheckStatus
    category: CheckCategory
    summary: str
    evidence: List[CodeChunk] = Field(default_factory=list)
    reasoning_summary: str
    confidence: float = Field(ge=0.0, le=1.0)


class AppConfig(BaseModel):
    openai_api_key: Optional[str] = None
    model_name: str = "gpt-4.1-mini"
    log_level: str = "INFO"
