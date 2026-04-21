from __future__ import annotations

import json
from typing import Any

from app.models import AppConfig


class OpenAIClient:
    def __init__(self, config: AppConfig):
        self._enabled = bool(config.openai_api_key)
        self._model = config.model_name
        self._client = None
        if self._enabled:
            from openai import OpenAI

            self._client = OpenAI(api_key=config.openai_api_key)

    @property
    def enabled(self) -> bool:
        return self._enabled

    def structured_check(self, prompt: str) -> dict[str, Any]:
        if not self._client:
            raise RuntimeError("OpenAI client is not configured")

        response = self._client.responses.create(
            model=self._model,
            input=prompt,
            text={"format": {"type": "json_object"}},
        )
        text = response.output_text
        return json.loads(text)
