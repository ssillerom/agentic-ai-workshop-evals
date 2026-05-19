# 06 Experiments

## Starting point

Start from `checkpoint/05-dataset`. You have:

- a seeded Langfuse dataset
- a production-instrumented app
- one stable app entrypoint: `runSupportConversation(...)`

## Goal

Run the same app logic on the dataset and attach at least one evaluator so different runs can be compared.

## Exact changes by file

### `scripts/run-dataset.ts`

This file is the main work for the step.

1. Import:
   - `LangfuseClient`
   - the tracing helpers from `src/server/instrumentation.ts`
   - `runSupportConversation(...)`
2. Define the dataset input shape to match the JSON:
   - `input.messages`
3. Add a helper that converts dataset messages into runtime chat messages:
   - add ids
   - add timestamps
4. Initialize tracing at the top of the script with `ensureTracingInitialized()`.
5. Load the dataset from Langfuse with `langfuse.dataset.get(...)`.
6. Use `dataset.runExperiment(...)`.
7. In the `task` function:
   - read `item.input.messages`
   - convert them to runtime messages
   - call `runSupportConversation(...)`
   - return `response.answer`
8. Add run metadata such as:
   - `model`
   - `promptVariant`
9. Add at least one evaluator.
10. In this repo, the simple evaluator is `keyword_overlap`, so implement:
    - a helper that compares the answer to `expectedKeywords`
    - one evaluator that returns the overlap score
11. Flush Langfuse and shut tracing down before exiting.

The finished file should create a dataset run in Langfuse using the same app logic as the web UI.

## What you should not do in this step

- Do not create a second implementation path just for experiments.
- Do not bypass `runSupportConversation(...)`.

The point is that experiments should use the same app logic you traced in production.

## How to verify you are done

Run:

```bash
npm run dataset:run
```

Then verify in Langfuse:

- a dataset run appears
- every item has an output
- the run metadata is visible
- the `keyword_overlap` score appears
- the item traces link back to the same app structure you saw in tracing

## End state

This finished experiment workflow becomes the starting point for `07-prompt-iteration`.
