from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parents[1]

# Keep the workshop .env authoritative for the Python server and helper scripts.
load_dotenv(ROOT_DIR / ".env", override=True)


@dataclass(frozen=True)
class Settings:
    port: int = 8787
    openai_api_key: str = ""
    openai_model: str = "gpt-5.5-2026-04-23"
    langfuse_public_key: str = ""
    langfuse_secret_key: str = ""
    langfuse_base_url: str = "https://cloud.langfuse.com"
    langfuse_prompt_name: str = "dad-it-support-agent"
    langfuse_prompt_label: str = "production"
    workshop_prompt_variant: str = "default"
    dataset_name: str = "dad-it-support-workshop"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings(
        port=int(os.getenv("PORT", "8787")),
        openai_api_key=os.getenv("OPENAI_API_KEY", ""),
        openai_model=os.getenv("OPENAI_MODEL", "gpt-5.5-2026-04-23"),
        langfuse_public_key=os.getenv("LANGFUSE_PUBLIC_KEY", ""),
        langfuse_secret_key=os.getenv("LANGFUSE_SECRET_KEY", ""),
        langfuse_base_url=os.getenv("LANGFUSE_BASE_URL", "https://cloud.langfuse.com"),
        langfuse_prompt_name=os.getenv("LANGFUSE_PROMPT_NAME", "dad-it-support-agent"),
        langfuse_prompt_label=os.getenv("LANGFUSE_PROMPT_LABEL", "production"),
        workshop_prompt_variant=os.getenv("WORKSHOP_PROMPT_VARIANT", "default"),
        dataset_name=os.getenv("DATASET_NAME", "dad-it-support-workshop"),
    )


def is_langfuse_configured(settings: Settings | None = None) -> bool:
    current = settings or get_settings()
    return bool(current.langfuse_public_key and current.langfuse_secret_key)
