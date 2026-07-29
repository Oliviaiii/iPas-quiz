import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

const questions = JSON.parse(
  await readFile(new URL("../app/data/demo-questions.json", import.meta.url), "utf8"),
);
const sources = JSON.parse(
  await readFile(new URL("../app/data/sources.json", import.meta.url), "utf8"),
);
const manifest = JSON.parse(
  await readFile(new URL("../public/data/manifest.json", import.meta.url), "utf8"),
);

test("keeps the temporary practice bank explicit and structurally valid", () => {
  assert.equal(questions.length, 4);
  assert.ok(questions.every((question) => question.sourceType === "practice"));
  assert.ok(questions.every((question) => question.options.length === 4));
  assert.ok(questions.every((question) => question.officialAnswer.length === 1));
  assert.ok(questions.every((question) => question.explanationStatus === "reviewed"));
  assert.ok(
    questions.every((question) =>
      ["A", "B", "C", "D"].every((label) => question.explanation.optionAnalysis[label]),
    ),
  );
});

test("uses unique stable question ids", () => {
  const ids = questions.map((question) => question.id);
  assert.equal(new Set(ids).size, ids.length);
  assert.ok(ids.every((id) => id.startsWith("aiap-practice-")));
});

test("tracks every 114 and 115 elementary/intermediate exam session", () => {
  const examSources = sources.filter((source) => source.sourceType === "official-exam");
  const expectedSessions = {
    elementary: { 114: ["1", "2", "3", "4"], 115: ["1", "2", "3", "4"] },
    intermediate: { 114: ["1", "2"], 115: ["1", "2"] },
  };
  const expectedSubjects = {
    elementary: ["ai-foundation", "genai-planning"],
    intermediate: ["ai-tech-planning", "big-data", "machine-learning"],
  };

  for (const [level, years] of Object.entries(expectedSessions)) {
    for (const [year, sessions] of Object.entries(years)) {
      for (const session of sessions) {
        const items = examSources.filter(
          (source) =>
            source.level === level &&
            source.rocYear === Number(year) &&
            source.session === session,
        );
        assert.deepEqual(
          items.map((item) => item.subjectCode).sort(),
          expectedSubjects[level].toSorted(),
          `${year} ${level} session ${session}`,
        );
      }
    }
  }
});

test("keeps source progress auditable and official-only", () => {
  assert.equal(sources.length, 38);
  assert.equal(new Set(sources.map((source) => source.sourceId)).size, sources.length);
  assert.ok(
    sources.every((source) =>
      ["www.ipas.org.tw", "ipd.nat.gov.tw"].includes(new URL(source.url).hostname),
    ),
  );
  assert.ok(sources.every((source) => source.retrievedAt === "2026-07-29"));
  assert.ok(
    sources.every(
      (source) =>
        source.importedCount <= (source.expectedCount ?? 0) &&
        source.answerVerifiedCount <= source.importedCount &&
        source.explanationReviewedCount <= source.importedCount,
    ),
  );
});

test("separates published, unavailable, future, and superseded work", () => {
  const count = (status) =>
    sources.filter((source) => source.availability === status).length;
  assert.equal(count("published"), 17);
  assert.equal(count("not-found"), 9);
  assert.equal(count("scheduled"), 7);
  assert.equal(count("superseded"), 5);

  const publishedExams = sources.filter(
    (source) =>
      source.sourceType === "official-exam" &&
      source.availability === "published",
  );
  assert.equal(publishedExams.length, 12);
  assert.ok(publishedExams.every((source) => source.expectedCount === 50));
});

test("publishes the verified inventory totals without claiming imported questions", () => {
  assert.equal(manifest.inventoryCutoff, "2026-07-29");
  assert.equal(manifest.sourceCount, 38);
  assert.equal(manifest.officialQuestionCount, 0);
  assert.equal(manifest.practiceQuestionCount, questions.length);
  assert.deepEqual(manifest.collectionProgress, {
    examSessionCount: 12,
    publishedExamPaperCount: 12,
    publishedExamQuestionTarget: 600,
    currentSampleQuestionTarget: 115,
    knownQuestionTarget: 715,
    importedCount: 0,
    answerVerifiedCount: 0,
    explanationReviewedCount: 0,
    availability: {
      published: 17,
      "not-found": 9,
      scheduled: 7,
      superseded: 5,
    },
  });
});
