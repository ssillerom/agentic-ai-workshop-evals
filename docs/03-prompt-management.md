# 03 Prompt Management

This checkpoint replaces a purely local system prompt with a Langfuse-managed prompt, while preserving a fallback path.

## Goal

Show that prompt management is useful because:

- prompts become collaborative artifacts
- versions can be compared later
- traces can be tied back to a specific prompt version

## Current implementation approach

The app uses:

- local prompt templates in `src/server/local-prompt.ts`
- a Langfuse-aware loader in `src/server/prompt-manager.ts`

If a Langfuse prompt is unavailable, the app compiles the local fallback prompt instead.

## Publish the baseline prompt

Set:

```bash
LANGFUSE_PROMPT_NAME=parent-support-agent
LANGFUSE_PROMPT_LABEL=production
WORKSHOP_PROMPT_VARIANT=baseline
```

Then run:

```bash
npm run prompt:publish
```

## Runtime behavior

At request time the app:

1. fetches the named prompt from Langfuse
2. compiles it with profile variables
3. links it to the generation when available
4. falls back to the local prompt if needed

## What to show in Langfuse

- the generation is linked to a prompt version
- prompt metrics can now be analyzed by version
- the app still behaves consistently if prompt management is skipped in a shorter workshop

## Teaching point

Prompt management should not make the system more fragile. In this repo it is deliberately additive, not a hard dependency.

