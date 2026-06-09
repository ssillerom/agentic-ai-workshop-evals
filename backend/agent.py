from __future__ import annotations

import json
from typing import Any

from langfuse import get_client, propagate_attributes
from langfuse.openai import OpenAI

from .schemas import ChatRequest, ChatResponse, TraceMeta
from .settings import get_settings
from .support_data import get_support_context
from .tools import TOOL_DEFINITIONS, execute_tool

SYSTEM_PROMPT = "\n".join(
    [
        "You are Dad IT Support Agent.",
        (
            "You are talking directly to Dad. He opened this chat himself "
            "to get help with his iPhone."
        ),
        "",
        (
            "You do not yet know which iPhone Dad has or which apps he uses - "
            "call get_support_context to find out before giving any "
            "device-specific instructions."
        ),
        "",
        "Rules:",
        (
            '- Speak directly to Dad in second person ("you", "your iPhone"). '
            "Never refer to Dad in the third person."
        ),
        (
            "- Call get_support_context as your very first tool call on each "
            "turn so you know which iPhone, iOS, and apps Dad has."
        ),
        "- For step-by-step help, call search_help_library before giving the final answer.",
        "- Use short numbered steps with one action per line.",
        "- Mention what Dad should expect to see on his screen after important taps.",
        "- Be honest about limits. You cannot see his screen, passwords, or real-time location.",
        (
            "- If the request is out of scope, say so kindly and redirect to "
            "the closest iPhone-help you can give."
        ),
        "- Do not invent button names or settings paths that were not confirmed by tool results.",
        "",
    ]
)

langfuse = get_client()


def get_prompt() -> Any | None:
    settings = get_settings()
    try:
        return langfuse.get_prompt(
            settings.langfuse_prompt_name,
            label=settings.langfuse_prompt_label,
        )
    except Exception:
        return None


def to_openai_messages(request: ChatRequest) -> list[dict[str, str]]:
    return [
        {"role": message.role, "content": message.content}
        for message in request.messages
    ]


def read_assistant_text(message: Any) -> str:
    content = getattr(message, "content", None)
    if isinstance(content, str):
        return content.strip()
    return ""


def parse_tool_arguments(arguments_text: str | None) -> dict[str, Any] | None:
    try:
        parsed = json.loads(arguments_text or "{}")
    except json.JSONDecodeError:
        return None

    return parsed if isinstance(parsed, dict) else {}


def _prompt_text(langfuse_prompt: Any | None) -> str:
    if langfuse_prompt is None:
        return SYSTEM_PROMPT

    try:
        compiled = langfuse_prompt.compile()
        if isinstance(compiled, str):
            return compiled
    except Exception:
        pass

    prompt = getattr(langfuse_prompt, "prompt", None)
    return prompt if isinstance(prompt, str) else SYSTEM_PROMPT


def run_support_conversation(request: ChatRequest) -> ChatResponse:
    settings = get_settings()
    context = get_support_context()
    langfuse_prompt = get_prompt()
    system_prompt = _prompt_text(langfuse_prompt)
    user_id = request.user_id or f"workshop-{context['id']}"

    request_payload = request.model_dump(mode="json", by_alias=True)

    with langfuse.start_as_current_observation(
        name="dad-it-support-chat-turn",
        as_type="agent",
        input=request_payload,
    ) as agent_observation:
        with propagate_attributes(
            user_id=user_id,
            session_id=request.session_id,
            tags=["langfuse-workshop", "dad-it-support"],
            trace_name="dad-it-support-chat-turn",
        ):
            client = OpenAI(api_key=settings.openai_api_key)
            transcript: list[dict[str, Any]] = [
                {"role": "system", "content": system_prompt},
                *to_openai_messages(request),
            ]
            used_tools: list[str] = []
            final_answer = ""

            for _attempt in range(6):
                completion_kwargs: dict[str, Any] = {
                    "model": settings.openai_model,
                    "messages": transcript,
                    "tools": TOOL_DEFINITIONS,
                    "tool_choice": "auto",
                    "name": "dad-it-support-openai",
                }
                if langfuse_prompt is not None:
                    completion_kwargs["langfuse_prompt"] = langfuse_prompt

                response = client.chat.completions.create(**completion_kwargs)
                message = response.choices[0].message if response.choices else None
                if message is None:
                    raise RuntimeError("OpenAI returned no assistant message.")

                transcript.append(message.model_dump(exclude_none=True))
                tool_calls = message.tool_calls or []
                if not tool_calls:
                    final_answer = read_assistant_text(message)
                    break

                for tool_call in tool_calls:
                    if tool_call.type != "function":
                        continue

                    if tool_call.function.name not in used_tools:
                        used_tools.append(tool_call.function.name)
                    parsed_arguments = parse_tool_arguments(tool_call.function.arguments)
                    if parsed_arguments is None:
                        tool_result: dict[str, Any] = {
                            "ok": False,
                            "error": (
                                f"The tool arguments for {tool_call.function.name} "
                                "were not valid JSON."
                            ),
                        }
                    else:
                        tool_result = execute_tool(tool_call.function.name, parsed_arguments)

                    transcript.append(
                        {
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": json.dumps(tool_result),
                        }
                    )

            if not final_answer:
                final_answer = (
                    "I ran out of room before finishing that answer. "
                    "Please ask the question once more in a slightly shorter way."
                )

            result = ChatResponse(
                answer=final_answer,
                used_tools=used_tools,
                trace_meta=TraceMeta(
                    context_id=context["id"],
                    context_label=context["label"],
                    model=settings.openai_model,
                ),
            )
            agent_observation.update(output=result.model_dump(mode="json", by_alias=True))
            return result
