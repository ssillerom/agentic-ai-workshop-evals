# 04 Monitoring

## Starting point

Start from `checkpoint/03-prompt-management`. You now have:

- a traced app
- a stable root observation shape
- optional Langfuse-managed prompts

## Goal

Define the first production signals you want to monitor and map them from the trace structure you created in step 2.

## Exact work to do

### `src/server/support-agent.ts`

Before you configure anything in the Langfuse UI, inspect the root observation fields in code.

1. Look at the `updateActiveObservation({ input: ... })` call.
2. Confirm that the root input contains:
   - `messages`
   - `promptSource`
   - `supportContext`
3. Look at the `updateActiveObservation({ output: ... })` call.
4. Confirm that the root output contains:
   - `answer`
   - `promptSource`
   - `usedTools`
   - `model`

You usually do not need to change code in this step unless those fields are missing or named differently.

### `docs/04-monitoring.md`

Document the monitoring design for this app.

1. Write down the app scope clearly.
2. Write down the first two monitor ideas:
   - out-of-scope requests
   - user disagreement
3. Write down the observation target:
   - type `agent`
   - name `dad-it-support-chat-turn`
4. Write down the JSON paths you want to use in Langfuse.

The point of this file is to explain the monitoring logic, not to change app behavior.

### Langfuse UI

This is where most of the actual work happens.

1. Create or select an LLM-as-a-judge template for out-of-scope detection.
2. Map variables from the root observation.
3. Use the `messages` array as the main input shape.
4. Recommended mappings:
   - `messages` from `$.messages`
   - `system_prompt` from `$.messages[0].content`
   - `assistant_output` from `$.answer`
5. Repeat the same idea for disagreement detection.

Use the whole message array instead of trying to build separate custom fields like `last_user_message` unless you truly need them.

## What you should not do in this step

- Do not redesign the app.
- Do not change the dataset yet.
- Do not add lots of custom code-side monitors.

This step is about understanding how to use the existing trace structure as a monitoring surface.

## How to verify you are done

- You can name the exact observation target for the monitors.
- You can name the exact JSON paths you will use.
- You can produce one out-of-scope example and one disagreement example in the app.
- You can explain why the `messages` array is the main field to anchor the monitor on.

## End state

This finished understanding becomes the starting point for `05-dataset`.
