# 06 Experiments

This checkpoint turns the sample dataset into repeatable experiment runs.

## Goal

Run the same app logic against a fixed dataset and compare outcomes over time.

## Run the dataset

```bash
npm run dataset:run
```

This script:

1. loads the dataset from Langfuse
2. runs the same server-side agent logic used by the web app
3. links each result trace to the dataset run
4. writes a simple `keyword_overlap` score for each item

File:

- `scripts/run-dataset.ts`

## What to evaluate in Langfuse

The workshop should still center the Langfuse evaluator UI:

- compare expected output vs actual output
- review individual failures side by side
- compare aggregated results between runs

## Why the code score is still useful

`keyword_overlap` is not the final judge. It is a cheap extra signal that helps demonstrate:

- programmatic scores
- how scores appear on experiment runs
- that evaluation can combine deterministic and model-based methods

## Teaching point

The real value is not “we ran a script.” The value is that the same application can now be tested systematically before prompt or logic changes go to production.

