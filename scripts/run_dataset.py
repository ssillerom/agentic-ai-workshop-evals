from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from langfuse import Evaluation, get_client

from backend.agent import run_support_conversation
from backend.schemas import ChatMessage, ChatRequest
from backend.settings import get_settings, is_langfuse_configured


def keyword_overlap(answer: str, expected_keywords: list[str]) -> float:
    if not expected_keywords:
        return 1.0

    normalized_answer = answer.lower()
    matches = [
        keyword
        for keyword in expected_keywords
        if keyword.lower() in normalized_answer
    ]
    return len(matches) / len(expected_keywords)


def to_runtime_messages(input_data: dict) -> list[ChatMessage]:
    return [
        ChatMessage(
            id=f"dataset-message-{index + 1}",
            role=message["role"],
            content=message["content"],
            timestamp=datetime.now(UTC).isoformat(),
        )
        for index, message in enumerate(input_data["messages"])
    ]


def keyword_overlap_evaluator(
    *,
    output: str,
    expected_output: dict,
    **_kwargs: object,
) -> Evaluation:
    expected_keywords = expected_output["expectedKeywords"]
    overlap = keyword_overlap(output, expected_keywords)
    matched = round(overlap * len(expected_keywords))

    return Evaluation(
        name="keyword_overlap",
        value=overlap,
        comment=f"Matched {matched} of {len(expected_keywords)} expected keywords.",
    )


def main() -> None:
    settings = get_settings()
    if not is_langfuse_configured(settings):
        raise RuntimeError("Langfuse credentials are required to run dataset experiments.")

    langfuse = get_client()
    dataset = langfuse.get_dataset(settings.dataset_name)
    run_name = f"dad-it-support-{datetime.now(UTC).isoformat()}"

    def task(*, item, **_kwargs: object) -> str:
        response = run_support_conversation(
            ChatRequest(
                session_id=f"dataset-{uuid4()}",
                user_id="dataset-runner",
                messages=to_runtime_messages(item.input),
            )
        )
        return response.answer

    result = dataset.run_experiment(
        name="Dad IT Support Agent experiment",
        run_name=run_name,
        description="Workshop dataset run for the Dad IT Support Agent",
        metadata={"model": settings.openai_model},
        max_concurrency=1,
        task=task,
        evaluators=[keyword_overlap_evaluator],
    )

    print(result.format())
    langfuse.flush()


if __name__ == "__main__":
    main()
