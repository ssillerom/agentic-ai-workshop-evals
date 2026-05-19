# 00 Setup

## Starting point

An untouched workshop repo.

## Goal

Get the repo to a state where you can run the app locally and later connect it to OpenAI and Langfuse Cloud EU.

## Exact changes by file

### `.env`

1. Copy `.env.example` to `.env`.
2. Fill in:
   - `OPENAI_API_KEY`
   - `OPENAI_MODEL`
   - `LANGFUSE_PUBLIC_KEY`
   - `LANGFUSE_SECRET_KEY`
   - `LANGFUSE_BASE_URL`
3. Leave `LANGFUSE_BASE_URL` set to `https://cloud.langfuse.com`.
4. Keep the prompt and dataset defaults unless the workshop tells you otherwise:
   - `LANGFUSE_PROMPT_NAME=dad-it-support-agent`
   - `LANGFUSE_PROMPT_LABEL=production`
   - `WORKSHOP_PROMPT_VARIANT=baseline`
   - `DATASET_NAME=dad-it-support-workshop`

## Commands to run

```bash
npm install
npm run dev
```

Open `http://127.0.0.1:3333`.

## What the finished setup should give you

- The client starts on port `3333`.
- The server starts on port `8787`.
- The app loads the Dad support context from the server.
- If you do not add Langfuse keys yet, the app can still boot and use its local prompt later.

## How to verify you are done

- `npm install` finishes successfully.
- `npm run dev` starts both client and server.
- The browser shows the workshop app instead of an error page.

## End state

You are ready to start from `checkpoint/01-base-app`.
