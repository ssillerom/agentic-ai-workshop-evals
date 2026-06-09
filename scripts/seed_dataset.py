from __future__ import annotations

import json

from langfuse import get_client

from backend.settings import ROOT_DIR, get_settings, is_langfuse_configured


def main() -> None:
    settings = get_settings()
    if not is_langfuse_configured(settings):
        raise RuntimeError("Langfuse credentials are required to seed a dataset.")

    langfuse = get_client()

    try:
        langfuse.create_dataset(
            name=settings.dataset_name,
            description="Starter workshop dataset for the Dad IT Support Agent",
            metadata={
                "source": "repo-seed",
                "workshop": "langfuse-dad-it-support",
            },
        )
    except Exception as exc:
        if not any(marker in str(exc).lower() for marker in ("exists", "duplicate", "already")):
            raise

    seed_path = ROOT_DIR / "data" / "seed-dataset.json"
    seed_dataset = json.loads(seed_path.read_text(encoding="utf-8"))

    for item in seed_dataset:
        langfuse.create_dataset_item(
            id=item["id"],
            dataset_name=settings.dataset_name,
            input=item["input"],
            expected_output=item["expectedOutput"],
            metadata=item["metadata"],
        )

    langfuse.flush()
    print(f'Seeded dataset "{settings.dataset_name}" with {len(seed_dataset)} items.')


if __name__ == "__main__":
    main()
