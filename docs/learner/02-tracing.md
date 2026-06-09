---
title: "Workshop: Tracing an LLM Agent with Langfuse"
description: "Instrument the Python support agent so one chat turn becomes a nested Langfuse trace with OpenAI generations, agent spans, and tool calls."
---

# 02 Tracing

## Starting point

```bash
git checkout checkpoint/02-tracing
```

This is the blank slate for the tracing step - same code as `checkpoint/01-base-app`, with no Langfuse wiring yet. The Python dependencies are already in `pyproject.toml`; `npm install` installs the frontend dependencies and `uv` resolves the backend when you run the server. Make sure `.env` has your `OPENAI_API_KEY` and Langfuse keys.

## Why we trace

Tracing logs every step your agent takes: every model call, every tool invocation, the inputs that went in, and the outputs that came back. It turns the agent from a black box into something you can inspect after the fact, so when an answer is wrong you can point at the exact step where it went wrong instead of guessing.

If you want the bigger-picture motivation, see the [Langfuse Academy lesson on tracing](https://langfuse.com/academy/tracing). If you want the technical details, the [Langfuse Python SDK instrumentation docs](https://langfuse.com/docs/observability/sdk/instrumentation) cover the lower-level options.

## Goal

When Dad asks "How do I turn Bluetooth on?", the agent asks OpenAI what to do, calls `get_support_context`, asks OpenAI again, calls `search_help_library`, then asks OpenAI one more time to produce the numbered answer. None of that is visible today.

The goal of this chapter is to make every one of those steps visible in Langfuse: one chat turn becomes one nested trace with the agent run, the OpenAI generations, and the two tool calls all logged in order.

![Spec's step by step process](../images/tracing/process_illustration.png)

We will build up the trace in three steps:

1. **First trace** - log the OpenAI generations themselves.
2. **Nested traces** - group the generations under one agent run per turn.
3. **Recording tool calls** - make each tool invocation its own observation.

## Step 1 - First trace

We want observability on the OpenAI calls themselves to see the prompt, response, latency, token usage, and cost.

### `backend/agent.py`

Change the OpenAI import:

```py
from langfuse.openai import OpenAI
```

Then keep using the official OpenAI client shape where the agent creates it:

```py
client = OpenAI(api_key=settings.openai_api_key)
```

That is the whole first layer. The Langfuse OpenAI wrapper is a drop-in replacement around the OpenAI Python SDK, so the existing `client.chat.completions.create(...)` calls now emit generation observations.

**Verify:** `npm run dev`, ask one question, refresh Langfuse. You should see one generation per OpenAI call with prompt, response, tokens, and latency. Each generation is still its own top-level trace; we fix that next.

![Langfuse Traces view after Step 1 — each chat turn appears as standalone openai-chat-completion generations.](../images/tracing/02-tracing-step-1.png)

## Step 2 - Nested traces

To put the generations into context, group them under one agent run per turn.

### `backend/agent.py`

Add the imports and module-level Langfuse client:

```py
from langfuse import get_client, propagate_attributes

langfuse = get_client()
```

Wrap the body of `run_support_conversation(...)` in an agent observation:

```py
request_payload = request.model_dump(mode="json", by_alias=True)

with langfuse.start_as_current_observation(
    name="dad-it-support-chat-turn",
    as_type="agent",
    input=request_payload,
) as agent_observation:
    with propagate_attributes(
        user_id=request.user_id or f"workshop-{context['id']}",
        session_id=request.session_id,
        tags=["langfuse-workshop", "dad-it-support"],
        trace_name="dad-it-support-chat-turn",
    ):
        # ...the same tool-calling loop...
        agent_observation.update(output=result.model_dump(mode="json", by_alias=True))
        return result
```

The OpenAI generations now inherit the active Langfuse context and appear below the `dad-it-support-chat-turn` agent observation.

**Verify:** one chat turn should now show up as a single `dad-it-support-chat-turn` observation with the OpenAI generation nested underneath.

![Trace tree after Step 2 — one dad-it-support-chat-turn agent root with the OpenAI generation as a child.](../images/tracing/02-tracing-step-2.png)

## Step 3 - Recording tool calls

The OpenAI generation already mentions the tool calls in its `tool_calls` output, but we also want observations for the local tool execution itself.

### `backend/tools.py`

Add the import:

```py
from langfuse import observe
```

Decorate each local tool helper:

```py
@observe(name="get_support_context", as_type="tool")
def get_support_context_tool() -> dict:
    context = get_support_context()
    return {"ok": True, "context": context}


@observe(name="search_help_library", as_type="tool")
def search_help_library_tool(question: str) -> dict:
    guides = search_guides(question)
    return {"ok": True, "results": guides}
```

Then have `execute_tool(...)` call those observed helpers instead of calling the raw support-data functions directly.

![Full trace after Step 3 — dad-it-support-chat-turn (agent) with the OpenAI generation and get_support_context + search_help_library tool observations as siblings underneath.](../images/tracing/02-tracing-step-3.png)

## How to verify you are done

- A single user turn creates one trace in Langfuse.
- Root observation: `dad-it-support-chat-turn` (type `agent`).
- Child generations from `langfuse.openai.OpenAI` with prompt, response, tokens, latency.
- Child tool observations: `get_support_context`, `search_help_library`.
- Root input is the chat request; root output is the chat response.

## Wrap-up

Same pattern, different observation types: use the Langfuse OpenAI wrapper for model calls, `start_as_current_observation(..., as_type="agent")` for the turn, and `@observe(..., as_type="tool")` for local tools.

A more straightforward way to add rich tracing in line with Langfuse best practices is the [**Langfuse skill**](https://github.com/langfuse/skills) (`/langfuse`). It applies the recommended patterns to your codebase without you hand-rolling each wrap. This walkthrough exists so you understand what the skill is doing under the hood.

## End state

This finished traced app is the starting point for `03-prompt-management` and `04-monitoring`.
