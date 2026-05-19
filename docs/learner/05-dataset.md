# 05 Dataset

## Starting point

Start from `checkpoint/04-monitoring`. You already understand:

- the app scope
- the interesting failure modes
- the trace shape

## Goal

Create a starter dataset that reflects the intended scope of the Dad IT Support Agent and uses the same message-array input shape as the app.

## Exact changes by file

### `data/seed-dataset.json`

This is the main artifact for the step.

1. Add around 20 representative examples.
2. Keep the input shape aligned with the app:

```json
{
  "input": {
    "messages": [{ "role": "user", "content": "..." }]
  }
}
```

3. For every item, also add:
   - `id`
   - `expectedOutput.idealAnswer`
   - `expectedOutput.expectedKeywords`
   - `metadata`
4. Make sure the dataset covers:
   - iPhone Bluetooth
   - iPhone Wi-Fi
   - photos and WhatsApp
   - Maps basics
   - Windows Wi-Fi
   - printing
   - finding downloads
   - limits such as passwords or live location
   - out-of-scope requests

The finished file should feel like a real first evaluation set, not a random list of prompts.

### `scripts/seed-dataset.ts`

Use this script to create the dataset in Langfuse.

1. Initialize `LangfuseClient`.
2. Create the dataset if it does not already exist.
3. Loop through the JSON file and create each dataset item.
4. Pass through:
   - `id`
   - `datasetName`
   - `input`
   - `expectedOutput`
   - `metadata`
5. Flush the Langfuse client before exiting.

The finished file should be idempotent enough for workshop use. If the dataset already exists, the script should not crash for a trivial reason.

### `.env`

Make sure `DATASET_NAME` points to the dataset name you want to seed.

## How to verify you are done

Run:

```bash
npm run dataset:seed
```

Then verify:

- the dataset appears in Langfuse
- the item count matches your JSON file
- each item uses `input.messages`
- each item has an expected output

## End state

This finished dataset becomes the starting point for `06-experiments`.
