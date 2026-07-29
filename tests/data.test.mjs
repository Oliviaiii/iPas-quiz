import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

const questions = JSON.parse(
  await readFile(new URL("../app/data/demo-questions.json", import.meta.url), "utf8"),
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

test("does not claim official coverage before the source inventory exists", () => {
  assert.equal(manifest.inventoryCutoff, null);
  assert.equal(manifest.sourceCount, 0);
  assert.equal(manifest.officialQuestionCount, 0);
  assert.equal(manifest.practiceQuestionCount, questions.length);
});
