# 07 Prompt Iteration

This checkpoint closes the loop: make a concrete change, run again, and compare.

## Current prompt variants

The repo includes two local variants:

- `baseline`
- `gentler`

File:

- `src/server/local-prompt.ts`

## Switch variants locally

```bash
WORKSHOP_PROMPT_VARIANT=gentler
```

Then rerun:

```bash
npm run dataset:run
```

## Optional Langfuse-managed versioning flow

1. publish the prompt variant to Langfuse
2. label it appropriately
3. rerun the dataset
4. compare runs side by side in Langfuse

## What to look for

- does the prompt reduce harsh or confusing answers?
- does it improve ambiguous cases?
- does it hurt concise mechanical tasks like Bluetooth or printing?

## Teaching point

A prompt change is only meaningful when you can compare it against a stable baseline.

