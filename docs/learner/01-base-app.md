# 01 Base App

## Starting point

Start from `checkpoint/00-setup`. The repo can run, but you now need to build the first real version of the app.

## Goal

Build a working Dad IT Support Agent that already uses the OpenAI SDK and local tool calling, but does not use Langfuse tracing yet.

## Exact changes by file

### `src/shared/types.ts`

Define the core types that the rest of the app will share.

1. Replace any multi-profile type with one `SupportContext` type.
2. Make `ChatRequest` contain:
   - `messages`
   - `sessionId`
   - optional `userId`
3. Do not keep `profileId` in the request type.
4. Make `ChatResponse.traceMeta` describe the one fixed support context, not a chosen profile.

The finished file should make the rest of the app naturally one-context instead of profile-based.

### `src/server/support-data.ts`

Create the one fixed support setup for Dad and the local help library.

1. Add one `DEFAULT_SUPPORT_CONTEXT` object with:
   - Dad label
   - device list
   - response style
   - scope highlights
   - starter questions
2. Add a `GUIDE_LIBRARY` array with step-by-step articles for:
   - iPhone Bluetooth
   - iPhone Wi-Fi
   - photos and WhatsApp
   - Maps basics
   - Windows Wi-Fi
   - printing
   - Bluetooth on Windows
   - finding downloads
3. Export:
   - `getSupportContext()`
   - `searchGuides(question: string)`

The finished file should be the only source of truth for Dad’s known setup and the local manuals.

### `src/server/local-prompt.ts`

Create the local prompt that will drive the app before Langfuse prompt management exists.

1. Add one `baseline` prompt template.
2. Make the prompt say:
   - you are Dad IT Support Agent
   - you are the kid helping Dad directly
   - talk to Dad using “you”
3. Include template variables for:
   - context summary
   - device details
   - response style
   - scope summary
4. Add prompt rules that explicitly tell the model to:
   - call `get_support_context` first for device-specific help
   - call `search_help_library` before the final answer for step-by-step guidance
5. Export helper functions:
   - `getLocalPromptTemplate(...)`
   - `buildPromptVariables(...)`
   - `compileLocalPrompt(...)`

The finished file should be enough to render a working system prompt without Langfuse.

### `src/server/tools.ts`

Define the tools the model is allowed to call.

1. Export `TOOL_DEFINITIONS` in OpenAI tool format.
2. Add two tools only:
   - `get_support_context`
   - `search_help_library`
3. Export `executeTool(name, input)`.
4. Make `executeTool(...)`:
   - return the known Dad context for `get_support_context`
   - search the local guide library for `search_help_library`

The finished file should be the single place where the model’s tool surface is defined.

### `src/server/support-agent.ts`

Implement the plain OpenAI app loop first, without Langfuse tracing.

1. Create an OpenAI client helper that throws if `OPENAI_API_KEY` is missing.
2. Add helpers to:
   - convert app messages to OpenAI messages
   - read the assistant’s final text
   - parse tool-call JSON arguments
3. Build `runSupportConversation(...)`.
4. Inside `runSupportConversation(...)`:
   - load the fixed Dad context
   - compile the local prompt
   - prepend the system message
   - send the transcript to `openai.chat.completions.create(...)`
   - allow tool calling with `TOOL_DEFINITIONS`
   - run tool calls through `executeTool(...)`
   - append tool results back into the transcript
   - loop until the model returns a final answer
5. Return:
   - `answer`
   - `promptSource: "local"`
   - `usedTools`
   - `traceMeta`

The finished file should contain a full OpenAI tool-calling loop, but no Langfuse imports yet.

### `src/server/index.ts`

Wire the server routes to the new one-context app.

1. Add `GET /api/support-context`.
2. Remove any profile-list route.
3. Keep `POST /api/chat`.
4. Validate the request body with:
   - `messages`
   - `sessionId`
   - optional `userId`
5. Return the result of `runSupportConversation(...)`.

The finished file should serve one support context and one chat API.

### `src/client/App.tsx`

Build the frontend around one fixed Dad setup.

1. Remove all profile-picker logic.
2. Fetch the support context from `/api/support-context`.
3. Keep one conversation state:
   - `messages`
   - `draft`
   - `sessionId`
   - `lastRun`
4. Add the starter greeting for Dad.
5. On submit:
   - append the user message
   - send the full `messages` array to `/api/chat`
   - append the assistant answer from the response
6. Keep the current product touches in the UI:
   - starter-question buttons
   - loading/thinking state
   - Markdown rendering for assistant replies

The finished file should feel like a complete but small web chat, not a placeholder.

### `src/client/styles.css`

Style the one-context layout.

1. Keep the hero section.
2. Replace any profile sidebar styling with a Dad context panel.
3. Style:
   - the starter question chips
   - the transcript cards
   - the thinking state
   - the prompt badge
4. Make sure it still works on smaller screens.

## What the finished app should contain

- One Dad support context
- One OpenAI chat loop
- Two local tools
- One minimal web chat UI
- No Langfuse tracing yet

## How to verify you are done

- The app runs with only `OPENAI_API_KEY`.
- The left panel shows Dad’s known setup, not multiple profile cards.
- Asking “How do I print a PDF?” returns a practical answer.
- The model can call local tools and answer with grounded steps.
- There are still no Langfuse trace imports in `src/server/support-agent.ts`.

## End state

This finished app becomes the starting point for `02-tracing`.
