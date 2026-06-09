---
title: "Workshop: Instructor Notes for Tracing"
description: "Facilitator notes for teaching Langfuse tracing in three layers: OpenAI generations, one agent root, and tool observations."
---

# 02 Tracing

Learner guide: [02 Tracing](../learner/02-tracing.md)

## Instructor notes

- Teach the progression in three visible layers: OpenAI generations, one agent root, then tool observations.
- Keep the code changes small and local. The point is to show that Langfuse wraps existing app boundaries instead of forcing an architecture rewrite.
- The user/session propagation section is optional live, but later checkpoints include it so the following chapters have attribution available.

## Demo rhythm

1. Switch to `langfuse.openai.OpenAI`, run one turn, show separate generation traces.
2. Wrap `run_support_conversation(...)` in `start_as_current_observation(..., as_type="agent")`, run again, show nested generations.
3. Decorate the two local tool helpers with `@observe(..., as_type="tool")`, run again, show the full tree.

## Watch for

- Learners wrapping the OpenAI client in a separate factory. The workshop intentionally keeps the wrapped Python client at the call site.
- Forgetting to flush in short-lived scripts; the server can buffer normally, but prompt and dataset helpers should call `langfuse.flush()`.
