# 02 Tracing

## Starting point

Start from `checkpoint/01-base-app`. You now have a working OpenAI-based Dad IT Support Agent, but the app is still a black box.

## Goal

Manually add Langfuse tracing so one chat turn becomes a rich nested trace with:

- one root agent observation
- one OpenAI generation
- tool observations
- deliberate root input and output

## Exact changes by file

### `src/server/instrumentation.ts`

Add the OpenTelemetry and Langfuse initialization layer.

1. Import:
   - `NodeSDK` from `@opentelemetry/sdk-node`
   - `LangfuseSpanProcessor` from `@langfuse/otel`
2. Create module-level variables for:
   - `sdk`
   - `langfuseSpanProcessor`
3. Implement `ensureTracingInitialized()`:
   - return early if Langfuse keys are not configured
   - build the `LangfuseSpanProcessor`
   - start the `NodeSDK`
4. Export:
   - `ensureTracingInitialized()`
   - `flushTracing()`
   - `shutdownTracing()`

The finished file should be the one place that starts and stops Langfuse tracing.

### `src/server/index.ts`

Make the server actually initialize tracing.

1. Import:
   - `ensureTracingInitialized`
   - `shutdownTracing`
2. Call `ensureTracingInitialized()` near the top of the file so traces are enabled before requests are handled.
3. In the shutdown path, call `shutdownTracing()`.
4. Keep `/api/health` returning `tracingConfigured`.

The finished file should boot tracing automatically when Langfuse keys are present.

### `src/server/tools.ts`

Wrap the tool work in Langfuse observations.

1. Import `observe` from `@langfuse/tracing`.
2. Keep `TOOL_DEFINITIONS` as they were.
3. Instead of putting all the logic directly inside `executeTool(...)`, create observed helper functions:
   - one for `get_support_context`
   - one for `search_help_library`
4. Wrap those helpers with:
   - `name: "get_support_context"` and `asType: "tool"`
   - `name: "search_help_library"` and `asType: "tool"`
5. Make `executeTool(...)` delegate to those observed helpers.

The finished file should create one child tool observation every time the model calls a tool.

### `src/server/support-agent.ts`

This is the main tracing step.

1. Import:
   - `observeOpenAI` from `@langfuse/openai`
   - `observe`, `propagateAttributes`, and `updateActiveObservation` from `@langfuse/tracing`
2. Keep the plain OpenAI logic from step 1, but move it inside an observed wrapper.
3. Add a helper that builds the trace-facing `messages` array:
   - prepend the system prompt
   - then append the conversation messages
4. Wrap the top-level chat-turn function with `observe(...)` using:
   - `name: "dad-it-support-chat-turn"`
   - `asType: "agent"`
   - `captureInput: false`
   - `captureOutput: false`
5. Inside that observed function:
   - call `propagateAttributes(...)`
   - set `userId`
   - set `sessionId`
   - set `traceName`
   - set workshop tags and metadata
6. Before the model call, use `updateActiveObservation(...)` to set the root input.
7. Make the root input contain:
   - `messages`
   - `promptSource`
   - `supportContext`
8. Wrap the OpenAI client with `observeOpenAI(...)`.
9. Give the wrapped generation a clear name such as `openai-chat-completion`.
10. After the final answer is produced, use `updateActiveObservation(...)` again to set the root output.
11. Make the root output contain:
    - `answer`
    - `promptSource`
    - `usedTools`
    - `model`

The finished file should still answer questions exactly as before, but now it should produce a well-structured trace.

## What the finished trace should look like

- Root observation:
  - name `dad-it-support-chat-turn`
  - type `agent`
- Child generation:
  - OpenAI completion from `observeOpenAI(...)`
- Child tools:
  - `get_support_context`
  - `search_help_library`

## How to verify you are done

- A single user turn creates a trace in Langfuse.
- The trace shows the root agent observation, generation, and tool calls.
- The root input contains the full `messages` array.
- The root output contains `answer`.
- Tool calls appear as children, not as unstructured logs.

## End state

This finished traced app is the starting point for `03-prompt-management` and `04-monitoring`.
