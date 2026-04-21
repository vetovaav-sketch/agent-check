from __future__ import annotations

import math
import re
from collections import Counter


def tokenize(text: str) -> list[str]:
    return [tok for tok in re.findall(r"[a-zA-Zа-яА-Я0-9_]+", text.lower()) if len(tok) > 2]


def embed_text(text: str) -> dict[str, float]:
    tokens = tokenize(text)
    if not tokens:
        return {}
    counts = Counter(tokens)
    norm = math.sqrt(sum(v * v for v in counts.values()))
    return {token: value / norm for token, value in counts.items()}


def cosine_similarity(vec_a: dict[str, float], vec_b: dict[str, float]) -> float:
    if not vec_a or not vec_b:
        return 0.0
    small, big = (vec_a, vec_b) if len(vec_a) <= len(vec_b) else (vec_b, vec_a)
    return sum(value * big.get(token, 0.0) for token, value in small.items())
