from __future__ import annotations

from langfuse import get_client

from backend.agent import SYSTEM_PROMPT
from backend.settings import get_settings, is_langfuse_configured


def prompt_variants() -> dict[str, str]:
    return {
        "default": SYSTEM_PROMPT,
        "gentler": f"""{SYSTEM_PROMPT.strip()}

Tone variant:
- Be extra patient and reassuring when Dad seems uncertain.
- Use plain, familiar wording before technical terms.
- Start in-scope final answers with one brief confidence-building sentence.
- If the request is out of scope, say so directly but warmly, then offer the closest
  iPhone-help next step.
""",
    }


def resolve_prompt_variant(variant_name: str) -> tuple[str, str]:
    variants = prompt_variants()
    normalized = variant_name.strip() or "default"
    if normalized not in variants:
        supported = ", ".join(sorted(variants))
        raise ValueError(
            f'Unsupported WORKSHOP_PROMPT_VARIANT "{variant_name}". '
            f"Supported variants: {supported}."
        )
    return normalized, variants[normalized]


def main() -> None:
    settings = get_settings()
    if not is_langfuse_configured(settings):
        raise RuntimeError("Langfuse credentials are required to publish prompts.")

    variant_name, prompt = resolve_prompt_variant(settings.workshop_prompt_variant)
    langfuse = get_client()
    langfuse.create_prompt(
        name=settings.langfuse_prompt_name,
        type="text",
        prompt=prompt,
        labels=[settings.langfuse_prompt_label],
    )
    langfuse.flush()

    print(
        f'Published prompt "{settings.langfuse_prompt_name}" '
        f'({variant_name} variant) with label "{settings.langfuse_prompt_label}".'
    )


if __name__ == "__main__":
    main()
