---
title: "Workshop: Dad IT Support Agent Base App"
description: "Tour the Python support agent before instrumentation: chat UI, FastAPI routes, OpenAI tool loop, local tools, and support data."
---

# 01 Base App

> You already cloned the repo and checked out the workshop app in `00-setup`. The base app is in that same checkout, so there is nothing to build in this chapter — just orient yourself before tracing starts in `02-tracing`.

## What the running app does

- Dad himself is the user. Specs (the agent) talks directly to him about his iPhone.
- One OpenAI tool-calling loop. Two local tools (`get_support_context`, `search_help_library`).
- The system prompt is rendered locally from `backend/agent.py`. No Langfuse yet.

![How Specs handles a ticket — one agent, two tools, one model, each hop an observation in the trace.](../images/specs_illustration.png)

## Where to look in the code

- `src/client/App.tsx` — chat UI + side panel
- `backend/main.py` — FastAPI routes
- `backend/agent.py` — the tool-calling loop you'll instrument in `02-tracing`
- `backend/tools.py` — tool definitions and `execute_tool(...)`
- `backend/support_data.py` — Dad's fixed context + guide library
- `backend/agent.py` — system-prompt template


## Bonus

You can customize your experience by changing the phone specs in `backend/support_data.py`. Adding your dad's phone information means you will get replies for the right type of phone.

## End state

You are ready to start `02-tracing`.
