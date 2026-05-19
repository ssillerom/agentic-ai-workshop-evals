# 07 Prompt Iteration

## Starting point

Start from `checkpoint/06-experiments`. You can already run the current app and prompt on the dataset.

## Goal

Make one prompt change and compare the new run against the previous run.

## Exact work to do

### Option A: change the Langfuse-managed prompt

Use this option if you want to demonstrate prompt management inside Langfuse.

1. Open the `dad-it-support-agent` prompt in Langfuse.
2. Change one small thing only.
3. Good examples:
   - ask for more explicit reassurance
   - ask for more exact button names
   - ask for shorter steps
4. Publish the updated prompt version.
5. Run the dataset again with:

```bash
npm run dataset:run
```

### Option B: change the local prompt variant

Use this option if you want the repo itself to show the prompt change.

1. Open `src/server/local-prompt.ts`.
2. Add or adjust a variant such as `gentler`.
3. Change only a few prompt rules.
4. In `.env`, switch:

```bash
WORKSHOP_PROMPT_VARIANT=gentler
```

5. Run the dataset again.

### Comparison work in Langfuse

After rerunning, compare the old and new runs.

Look at:

- which individual answers improved
- which answers got worse
- whether `keyword_overlap` changed
- whether the tone changed in a way you actually wanted

## What to avoid

- Do not change the app logic and the prompt at the same time.
- Do not change the dataset and the prompt at the same time.

You want one clear cause for the differences between the two runs.

## How to verify you are done

- You have at least two runs on the same dataset.
- You can explain exactly what changed in the prompt.
- You can point to at least one improvement and one unchanged or worse result.

## End state

You now have the full loop: app, tracing, prompt management, monitoring, dataset, experiments, and iteration.
