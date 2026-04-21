from __future__ import annotations

import re
from typing import List

from app.models import Requirement


def split_into_requirements(text: str) -> List[Requirement]:
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    reqs: List[Requirement] = []
    buffer: list[str] = []
    idx = 1

    bullet_pattern = re.compile(r"^(\d+[\.)]|[-*])\s+")

    for line in lines:
        if bullet_pattern.match(line) and buffer:
            reqs.append(Requirement(requirement_id=f"R{idx}", text=" ".join(buffer).strip()))
            idx += 1
            buffer = [bullet_pattern.sub("", line)]
        else:
            buffer.append(bullet_pattern.sub("", line))

    if buffer:
        reqs.append(Requirement(requirement_id=f"R{idx}", text=" ".join(buffer).strip()))

    if not reqs and text.strip():
        reqs = [Requirement(requirement_id="R1", text=text.strip())]

    return reqs
