import "dotenv/config";
import { LangfuseClient } from "@langfuse/client";
import { runSupportConversation } from "../src/server/anthropic-agent";
import { env } from "../src/server/env";

type DatasetInput = {
  profileId: string;
  message: string;
};

type DatasetExpectation = {
  idealAnswer: string;
  expectedKeywords: string[];
};

function keywordOverlap(answer: string, expectedKeywords: string[]) {
  if (expectedKeywords.length === 0) {
    return 1;
  }

  const normalizedAnswer = answer.toLowerCase();
  const matches = expectedKeywords.filter((keyword) =>
    normalizedAnswer.includes(keyword.toLowerCase())
  );

  return matches.length / expectedKeywords.length;
}

async function main() {
  if (!env.langfusePublicKey || !env.langfuseSecretKey) {
    throw new Error("Langfuse credentials are required to run dataset experiments.");
  }

  const langfuse = new LangfuseClient({
    publicKey: env.langfusePublicKey,
    secretKey: env.langfuseSecretKey,
    baseUrl: env.langfuseBaseUrl
  });

  const dataset = await langfuse.dataset.get(env.datasetName);
  const runName = `parent-support-${env.workshopPromptVariant}-${new Date().toISOString()}`;

  for (const item of dataset.items) {
    const input = item.input as DatasetInput;
    const expected = item.expectedOutput as DatasetExpectation;

    const { span, result } = await runSupportConversation({
      profileId: input.profileId,
      sessionId: `dataset-${item.id}`,
      userId: "dataset-runner",
      messages: [
        {
          id: `dataset-${item.id}`,
          role: "user",
          content: input.message,
          timestamp: new Date().toISOString()
        }
      ]
    });

    await item.link(span as never, runName, {
      description: "Workshop dataset run",
      metadata: {
        model: env.anthropicModel,
        promptVariant: env.workshopPromptVariant
      }
    });

    const overlap = keywordOverlap(result.answer, expected.expectedKeywords);

    langfuse.score.trace(span as never, {
      name: "keyword_overlap",
      value: overlap,
      comment: `Matched ${Math.round(
        overlap * expected.expectedKeywords.length
      )} of ${expected.expectedKeywords.length} expected keywords.`
    });
  }

  await langfuse.flush();
  console.log(`Finished dataset run "${runName}".`);
}

void main();

