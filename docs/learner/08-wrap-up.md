# 08 Wrap-up

## Starting point

You have walked through the full workshop path.

## Goal

Be able to explain the full engineering loop and how each repository step supported it.

## What you should now be able to explain

### Product shape

You should be able to explain why the sample app is intentionally small:

- one Dad support context
- one chat interface
- two local tools
- one OpenAI app loop

### Tracing

You should be able to explain:

- where tracing is initialized
- where the root observation is created
- where the tools are traced
- why the root input contains `messages`
- why the root output contains `answer`

### Prompt management

You should be able to explain:

- where the fallback prompt lives
- where the Langfuse prompt is fetched
- how the app decides between `local` and `langfuse`

### Monitoring

You should be able to explain:

- which observation to monitor
- which JSON paths matter
- why out-of-scope and disagreement are good first monitors

### Dataset and experiments

You should be able to explain:

- why the dataset uses `input.messages`
- why the experiment reuses `runSupportConversation(...)`
- how the evaluator score is attached

### Iteration

You should be able to explain:

- what changed between two runs
- how you compared them
- what you would test next

## End state

You should now be able to take the same structure into another LLM app and rebuild the same loop there with much less guesswork.
