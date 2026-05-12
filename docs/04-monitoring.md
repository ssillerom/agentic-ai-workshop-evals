# 04 Monitoring

This checkpoint shifts the story from “we can inspect one trace” to “we can detect interesting production behavior at scale.”

## Scope of the sample app

In scope:

- practical help with the known device profiles
- Bluetooth, Wi-Fi, photos, printing, and basic maps usage

Out of scope:

- medical advice
- taxes
- booking travel on the user’s behalf
- anything unrelated to helping with the known devices

## Suggested first two monitors

- Out-of-scope request
- User disagreement

These are both high-signal and easy to explain live.

## Recommended evaluator target

Use an observation-level evaluator on the root `agent` observation:

- observation type: `agent`
- observation name: `parent-support-chat-turn`

This repo records the fields you need directly on the root observation.

## Useful mappings

For out-of-scope:

- `system_prompt` -> `$.systemPrompt`
- `last_user_message` -> `$.lastUserMessage`

For disagreement:

- `conversation_history` -> `$.conversationHistory`
- `last_user_message` -> `$.lastUserMessage`
- optional `assistant_output` -> `$.answer`

The root input contains:

- `systemPrompt`
- `promptSource`
- `conversationHistory`
- `lastUserMessage`

The root output contains:

- `answer`
- `promptSource`
- `usedTools`

## Demo suggestion

1. Ask a clearly out-of-scope question such as:
   - “Can you file her taxes for her?”
2. Ask a question, get an answer, then send a disagreement follow-up such as:
   - “No, that menu is not there.”
3. Show how those traces become review candidates in Langfuse.

## Teaching point

Monitoring is not about scoring everything. It is about catching the kinds of events that actually tell you where to look next.

