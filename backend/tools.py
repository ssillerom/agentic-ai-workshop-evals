from __future__ import annotations

from typing import Any

from langfuse import observe

from .support_data import get_support_context, search_guides

ToolResult = dict[str, Any]

TOOL_DEFINITIONS: list[dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": "get_support_context",
            "description": "Look up Dad's known device setup so the answer stays grounded.",
            "parameters": {
                "type": "object",
                "properties": {},
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_help_library",
            "description": (
                "Search the local help library for practical step-by-step device instructions."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {
                        "type": "string",
                        "description": "Dad's practical device question.",
                    },
                },
                "required": ["question"],
                "additionalProperties": False,
            },
        },
    },
]


@observe(name="get_support_context", as_type="tool")
def get_support_context_tool() -> ToolResult:
    context = get_support_context()

    return {
        "ok": True,
        "context": {
            "id": context["id"],
            "label": context["label"],
            "devices": context["devices"],
            "deviceSummary": context["deviceSummary"],
            "responseStyle": context["responseStyle"],
            "scopeHighlights": context["scopeHighlights"],
            "notableApps": context["notableApps"],
        },
    }


@observe(name="search_help_library", as_type="tool")
def search_help_library_tool(question: str) -> ToolResult:
    guides = search_guides(question)

    return {
        "ok": True,
        "results": [
            {
                "id": guide["id"],
                "title": guide["title"],
                "summary": guide["summary"],
                "steps": guide["steps"],
                "caution": guide.get("caution"),
            }
            for guide in guides
        ],
    }


def execute_tool(name: str, input_data: dict[str, Any]) -> ToolResult:
    match name:
        case "get_support_context":
            return get_support_context_tool()
        case "search_help_library":
            return search_help_library_tool(question=str(input_data.get("question", "")))
        case _:
            return {
                "ok": False,
                "error": f"Unsupported tool: {name}",
            }
