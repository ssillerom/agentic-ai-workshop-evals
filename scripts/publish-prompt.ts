import "dotenv/config";
import { publishSupportPrompt } from "../src/server/prompt-manager";
import type { PromptVariant } from "../src/server/local-prompt";

async function main() {
  const variant = (process.env.WORKSHOP_PROMPT_VARIANT ?? "baseline") as PromptVariant;
  const result = await publishSupportPrompt(variant);
  console.log(
    `Published prompt "${result.name}" with label "${result.label}" using the "${result.variant}" variant.`
  );
}

void main();

