from __future__ import annotations

import os

from dotenv import load_dotenv

from app.models import AppConfig


def load_config() -> AppConfig:
    load_dotenv()
    return AppConfig(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        model_name=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
        log_level=os.getenv("LOG_LEVEL", "INFO"),
    )
