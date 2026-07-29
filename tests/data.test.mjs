import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

const questions = JSON.parse(
  await readFile(new URL("../app/data/questions.json", import.meta.url), "utf8"),
);
const sources = JSON.parse(
  await readFile(new URL("../app/data/sources.json", import.meta.url), "utf8"),
);
const manifest = JSON.parse(
  await readFile(new URL("../public/data/manifest.json", import.meta.url), "utf8"),
);

test("contains exactly the 100 official 114 fourth-session elementary questions", () => {
  assert.equal(questions.length, 100);
  assert.ok(questions.every((question) => question.sourceType === "official-exam"));
  assert.ok(questions.every((question) => question.level === "elementary"));
  assert.ok(questions.every((question) => question.rocYear === 114));
  assert.ok(questions.every((question) => question.session === "4"));
  assert.ok(questions.every((question) => question.options.length === 4));
  assert.ok(questions.every((question) => question.officialAnswer.length === 1));
  assert.ok(questions.every((question) => question.extractionStatus === "verified"));
  assert.equal(
    questions.filter((question) => question.explanationStatus === "draft").length,
    3,
  );
  assert.equal(
    questions.filter((question) => question.explanationStatus === "missing").length,
    97,
  );
  const forbiddenFiller = [
    "沒有滿足題幹的關鍵條件",
    "機制或適用情境不同",
    "直接符合題幹設定",
    "也對應",
    "在題幹脈絡下屬於可成立或可採用的描述",
  ];
  assert.ok(
    questions.every((question) =>
      Object.values(question.explanation.optionAnalysis).every(
        (analysis) => !forbiddenFiller.some((filler) => analysis.includes(filler)),
      ),
    ),
  );
  const completeOptionAnalyses = questions.filter((question) =>
    ["A", "B", "C", "D"].every(
      (label) => question.explanation.optionAnalysis[label]?.length >= 35,
    ),
  );
  assert.deepEqual(
    completeOptionAnalyses.map((question) => question.id),
    [
      "aiap-elementary-114-04-ai-foundation-002",
      "aiap-elementary-114-04-ai-foundation-003",
      "aiap-elementary-114-04-ai-foundation-004",
    ],
  );
  const questionsAwaitingExplanation = questions.filter(
    (question) => question.explanationStatus === "missing",
  );
  assert.ok(
    questionsAwaitingExplanation.every(
      (question) =>
        question.explanation.summary === "" &&
        question.explanation.concept === "" &&
        question.explanation.answerReason === "" &&
        question.explanation.trap === "" &&
        Object.keys(question.explanation.optionAnalysis).length === 0,
    ),
  );
  assert.ok(questions.every((question) => question.explanation.editorialNote));
});

test("uses unique stable question ids", () => {
  const ids = questions.map((question) => question.id);
  assert.equal(new Set(ids).size, ids.length);
  assert.ok(ids.every((id) => id.startsWith("aiap-elementary-114-04-")));
});

test("preserves complete question numbers and official answer sequences", () => {
  const expectations = {
    "ai-foundation": "BCDCDCBBBCBADCABACAADCDCCDBDAADBDCDCBCADDCDCCBBAAA",
    "genai-planning": "BDBADBCCBBACDBBDDDBDACDDBCCBCABACBBAACADAADCADBADC",
  };
  for (const [subjectCode, answers] of Object.entries(expectations)) {
    const items = questions.filter((question) => question.subjectCode === subjectCode);
    assert.equal(items.length, 50);
    assert.deepEqual(
      items.map((question) => question.officialQuestionNumber),
      Array.from({ length: 50 }, (_, index) => index + 1),
    );
    assert.equal(items.map((question) => question.officialAnswer[0]).join(""), answers);
    assert.ok(items.every((question) => question.sourcePage >= 1 && question.sourcePage <= 13));
  }
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
        source.explanationDraftCount <= source.importedCount &&
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

test("publishes the verified inventory and imported-question totals", () => {
  assert.equal(manifest.inventoryCutoff, "2026-07-29");
  assert.equal(manifest.sourceCount, 38);
  assert.equal(manifest.officialQuestionCount, 100);
  assert.equal(manifest.practiceQuestionCount, 0);
  assert.equal(manifest.extractionStatus.verified, 100);
  assert.equal(manifest.explanationStatus.missing, 97);
  assert.equal(manifest.explanationStatus.draft, 3);
  assert.deepEqual(manifest.collectionProgress, {
    examSessionCount: 12,
    publishedExamPaperCount: 12,
    publishedExamQuestionTarget: 600,
    currentSampleQuestionTarget: 115,
    knownQuestionTarget: 715,
    importedCount: 100,
    answerVerifiedCount: 100,
    explanationDraftCount: 3,
    explanationReviewedCount: 0,
    availability: {
      published: 17,
      "not-found": 9,
      scheduled: 7,
      superseded: 5,
    },
  });
});
