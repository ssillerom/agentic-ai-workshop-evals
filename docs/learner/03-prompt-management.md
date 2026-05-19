# 03 Prompt Management

## Starting point

Start from `checkpoint/02-tracing`. The app is traced, but the prompt still lives only in code.

## Goal

Replace the code-only prompt path with a Langfuse-managed prompt plus a safe local fallback.

## Exact changes by file

### `src/server/local-prompt.ts`

Keep this file as the source of the fallback prompt.

1. Keep the `baseline` prompt.
2. Optionally add a second variant such as `gentler`.
3. Keep the helper functions:
   - `getLocalPromptTemplate(...)`
   - `buildPromptVariables(...)`
   - `compileLocalPrompt(...)`
4. Make sure `buildPromptVariables(...)` is built from the one Dad context:
   - label and relationship
   - devices and device summary
   - response style
   - scope highlights

The finished file should still be able to render a complete prompt without any Langfuse API call.

### `src/server/prompt-manager.ts`

Add the prompt loading layer here.

1. Create a lazy `LangfuseClient`.
2. Add a `ResolvedPrompt` type that includes:
   - `promptText`
   - `promptSource`
   - prompt metadata
3. Implement `resolveSupportPrompt(context)`.
4. In `resolveSupportPrompt(...)`:
   - read the current prompt variant from env
   - compile the local fallback prompt
   - if Langfuse is not configured, return the local prompt immediately
   - otherwise fetch the prompt from Langfuse using:
     - prompt name
     - prompt label
     - fallback prompt
5. Return whether the final prompt came from:
   - `local`
   - `langfuse`
6. Implement `publishSupportPrompt(...)` so the workshop can push the starter prompt into Langfuse.

The finished file should be the one place that decides whether the app uses the local prompt or the Langfuse-managed prompt.

### `src/server/support-agent.ts`

Replace the hardcoded local prompt path with the prompt manager.

1. Import `resolveSupportPrompt(...)`.
2. At the top of the chat-turn function:
   - load the support context
   - call `resolveSupportPrompt(context)`
3. Replace any old direct local-prompt compilation with `prompt.promptText`.
4. Use `prompt.promptSource` in the root observation input and output.
5. When wrapping OpenAI with `observeOpenAI(...)`, pass the Langfuse prompt object if one exists.

The finished file should keep the trace shape stable while the prompt source changes underneath it.

### `scripts/publish-prompt.ts`

Use this script to publish the starter prompt.

1. Read `WORKSHOP_PROMPT_VARIANT` from env.
2. Call `publishSupportPrompt(...)`.
3. Print a human-readable success message.

### `.env`

Make sure the following values exist:

- `LANGFUSE_PROMPT_NAME`
- `LANGFUSE_PROMPT_LABEL`
- `WORKSHOP_PROMPT_VARIANT`

## What the finished system should do

- Work without Langfuse prompt management
- Prefer the Langfuse prompt when it exists
- Keep a local fallback
- Link generations back to the prompt version when Langfuse is being used

## How to verify you are done

1. Run the app with Langfuse keys but without publishing the prompt yet.
2. Confirm it still works and reports `promptSource: "local"`.
3. Run:

```bash
npm run prompt:publish
```

4. Ask a question again.
5. Confirm the response now reports `promptSource: "langfuse"`.
6. Open the trace and confirm the generation is linked to the prompt.

## End state

This finished state becomes the starting point for `04-monitoring`.
