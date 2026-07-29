import { createHash } from "node:crypto";
import { readFile, writeFile } from "node:fs/promises";

const questionsUrl = new URL("../app/data/demo-questions.json", import.meta.url);
const sourcesUrl = new URL("../app/data/sources.json", import.meta.url);
const manifestUrl = new URL("../public/data/manifest.json", import.meta.url);
const checking = process.argv.includes("--check");

const [questionsText, sourcesText] = await Promise.all([
  readFile(questionsUrl, "utf8"),
  readFile(sourcesUrl, "utf8"),
]);
const questions = JSON.parse(questionsText);
const sources = JSON.parse(sourcesText);
const digest = createHash("sha256")
  .update(JSON.stringify({ questions, sources }))
  .digest("hex")
  .slice(0, 16);

const byLevel = Object.groupBy(questions, (question) => question.level);
const bySubject = Object.groupBy(questions, (question) => question.subjectCode);
const targetSources = sources.filter((source) => source.inclusion === "target");
const examSources = sources.filter((source) => source.sourceType === "official-exam");
const publishedExamSources = examSources.filter(
  (source) => source.availability === "published",
);
const currentSampleSources = sources.filter(
  (source) =>
    source.sourceType === "official-sample" &&
    source.availability === "published",
);
const sumSourceField = (items, field) =>
  items.reduce((total, item) => total + (item[field] ?? 0), 0);
const manifest = {
  schemaVersion: 1,
  inventoryCutoff: "2026-07-29",
  sourceCount: sources.length,
  officialQuestionCount: questions.filter((question) =>
    question.sourceType.startsWith("official-"),
  ).length,
  practiceQuestionCount: questions.filter((question) => question.sourceType === "practice").length,
  countsByLevel: Object.fromEntries(
    Object.entries(byLevel).map(([key, items]) => [key, items.length]),
  ),
  countsBySubject: Object.fromEntries(
    Object.entries(bySubject).map(([key, items]) => [key, items.length]),
  ),
  explanationStatus: {
    missing: questions.filter((question) => question.explanationStatus === "missing").length,
    draft: questions.filter((question) => question.explanationStatus === "draft").length,
    reviewed: questions.filter((question) => question.explanationStatus === "reviewed").length,
  },
  collectionProgress: {
    examSessionCount: new Set(
      examSources.map(
        (source) => `${source.rocYear}-${source.level}-${source.session}`,
      ),
    ).size,
    publishedExamPaperCount: publishedExamSources.length,
    publishedExamQuestionTarget: sumSourceField(
      publishedExamSources,
      "expectedCount",
    ),
    currentSampleQuestionTarget: sumSourceField(
      currentSampleSources,
      "expectedCount",
    ),
    knownQuestionTarget: sumSourceField(targetSources, "expectedCount"),
    importedCount: sumSourceField(targetSources, "importedCount"),
    answerVerifiedCount: sumSourceField(targetSources, "answerVerifiedCount"),
    explanationReviewedCount: sumSourceField(
      targetSources,
      "explanationReviewedCount",
    ),
    availability: Object.fromEntries(
      ["published", "not-found", "scheduled", "superseded"].map((status) => [
        status,
        sources.filter((source) => source.availability === status).length,
      ]),
    ),
  },
  contentHash: digest,
};
const serialized = `${JSON.stringify(manifest, null, 2)}\n`;

if (checking) {
  const current = await readFile(manifestUrl, "utf8").catch(() => "");
  if (current !== serialized) {
    throw new Error("public/data/manifest.json is out of date; run npm run prebuild");
  }
} else {
  await writeFile(manifestUrl, serialized, "utf8");
}
