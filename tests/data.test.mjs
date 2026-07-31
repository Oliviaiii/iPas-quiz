import assert from "node:assert/strict";
import { existsSync } from "node:fs";
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

// 每份已匯入的官方試卷：題號 1..50、官方答案序列與來源頁數上限。
const importedPapers = [
  {
    idPrefix: "aiap-elementary-114-04-",
    level: "elementary",
    rocYear: 114,
    session: "4",
    subjectCode: "ai-foundation",
    answers: "BCDCDCBBBCBADCABACAADCDCCDBDAADBDCDCBCADDCDCCBBAAA",
    pageCount: 13,
  },
  {
    idPrefix: "aiap-elementary-114-04-",
    level: "elementary",
    rocYear: 114,
    session: "4",
    subjectCode: "genai-planning",
    answers: "BDBADBCCBBACDBBDDDBDACDDBCCBCABACBBAACADAADCADBADC",
    pageCount: 13,
  },
  {
    idPrefix: "aiap-elementary-115-01-",
    level: "elementary",
    rocYear: 115,
    session: "1",
    subjectCode: "ai-foundation",
    answers: "DDDCBCCDAABBABACABABDCBDACCCBAACDCCABBDABDDACCDCDB",
    pageCount: 12,
  },
  {
    idPrefix: "aiap-elementary-115-01-",
    level: "elementary",
    rocYear: 115,
    session: "1",
    subjectCode: "genai-planning",
    answers: "ADADCDADBDBBBADDBACCDDADACACCBCAAABCCCDBABBBDCACBC",
    pageCount: 11,
  },
  {
    idPrefix: "aiap-elementary-115-02-",
    level: "elementary",
    rocYear: 115,
    session: "2",
    subjectCode: "ai-foundation",
    answers: "ADABCCAADACBDBDDDBABCDAAABADCBDDBCAADCCCCCBCBCBBDB",
    pageCount: 13,
  },
  {
    idPrefix: "aiap-elementary-115-02-",
    level: "elementary",
    rocYear: 115,
    session: "2",
    subjectCode: "genai-planning",
    answers: "BABCDBBCACBADBBAADCDDCCCDDBDBAACCBAAADBDADBACCCBBD",
    pageCount: 13,
  },
  {
    idPrefix: "aiap-intermediate-114-02-",
    level: "intermediate",
    rocYear: 114,
    session: "2",
    subjectCode: "ai-tech-planning",
    answers: "BABCABACBDCBBACDDDBBBDADBDCCBABDCDABBBCAADBCDACBAC",
    pageCount: 14,
  },
  {
    idPrefix: "aiap-intermediate-114-02-",
    level: "intermediate",
    rocYear: 114,
    session: "2",
    subjectCode: "big-data",
    answers: "DBABBCCBCCCADDCABACDBDCAACDADCBADBBBCBDBACBDACBDCB",
    pageCount: 17,
  },
  {
    idPrefix: "aiap-intermediate-114-02-",
    level: "intermediate",
    rocYear: 114,
    session: "2",
    subjectCode: "machine-learning",
    answers: "BCCBACADACDCBCBABACCCBACADDCDCBDBDADBBCCDBADBBBCCC",
    pageCount: 19,
  },
  {
    idPrefix: "aiap-intermediate-115-01-",
    level: "intermediate",
    rocYear: 115,
    session: "1",
    subjectCode: "ai-tech-planning",
    answers: "DCBCCCCBDABBCABADDAABCBDBDABCCABDBBAADADADCBBCDCAD",
    pageCount: 15,
  },
  {
    idPrefix: "aiap-intermediate-115-01-",
    level: "intermediate",
    rocYear: 115,
    session: "1",
    subjectCode: "big-data",
    answers: "AABAADBDBBCCBCCADDDBDCCCCADCDBBBACDDABCABDCACACCBD",
    pageCount: 17,
  },
  {
    idPrefix: "aiap-intermediate-115-01-",
    level: "intermediate",
    rocYear: 115,
    session: "1",
    subjectCode: "machine-learning",
    answers: "CCACCBBBAADACCDABADCDCDDADCBBBADBDDBACABBCDBABBDCB",
    pageCount: 18,
  },
];

test("contains only verified official exam questions", () => {
  assert.equal(questions.length, importedPapers.length * 50);
  assert.ok(questions.every((question) => question.sourceType === "official-exam"));
  assert.ok(
    questions.every((question) =>
      ["elementary", "intermediate"].includes(question.level),
    ),
  );
  assert.ok(questions.every((question) => question.options.length === 4));
  assert.ok(questions.every((question) => question.officialAnswer.length === 1));
  assert.ok(questions.every((question) => question.scoring === "single"));
  assert.ok(questions.every((question) => question.extractionStatus === "verified"));
  assert.ok(
    questions.every(
      (question) => question.sourceUrl && question.answerSourceUrl && question.prompt,
    ),
  );
  // 選項內容可能是文字或官方附圖；兩者皆空由附圖測試擋下。
  assert.ok(
    questions.every((question) =>
      question.options.every((option) => "ABCD".includes(option.label)),
    ),
  );
});

test("keeps explanation drafts complete and free of filler", () => {
  // 第二階段逐批撰寫；每批完成後更新此數字。
  // 114 年第四次初級第一科第 1～50 題全部完成，第二科第 1～10 題完成。
  const draftIds = [
    ...Array.from({ length: 50 }, (_, index) =>
      `aiap-elementary-114-04-ai-foundation-${String(index + 1).padStart(3, "0")}`,
    ),
    ...Array.from({ length: 10 }, (_, index) =>
      `aiap-elementary-114-04-genai-planning-${String(index + 1).padStart(3, "0")}`,
    ),
  ];
  assert.deepEqual(
    questions
      .filter((question) => question.explanationStatus === "draft")
      .map((question) => question.id),
    draftIds,
  );
  assert.equal(
    questions.filter((question) => question.explanationStatus === "missing").length,
    questions.length - draftIds.length,
  );
  assert.equal(
    questions.filter((question) => question.explanationStatus === "reviewed").length,
    0,
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
  // 標記為 draft 的題目都必須有完整的 A～D 解析，反之亦然。
  assert.deepEqual(completeOptionAnalyses.map((question) => question.id), draftIds);
  for (const question of questions.filter((q) => q.explanationStatus === "draft")) {
    assert.ok(question.explanation.summary.startsWith("正確答案是 "), question.id);
    assert.ok(
      question.explanation.summary.includes(question.officialAnswer[0]),
      question.id,
    );
    assert.ok(question.explanation.concept.length >= 60, question.id);
    assert.ok(question.explanation.answerReason.length >= 40, question.id);
    assert.ok(question.explanation.trap.length >= 20, question.id);
    assert.ok(question.explanation.references.length > 0, question.id);
    for (const reference of question.explanation.references) {
      assert.ok(/^https:\/\//.test(reference.url), `${question.id} ${reference.url}`);
      assert.ok(reference.title && reference.locator, question.id);
      assert.ok(/^\d{4}-\d{2}-\d{2}$/.test(reference.checkedAt), question.id);
    }
    assert.ok(question.explanation.author, question.id);
    assert.ok(question.explanation.authoredAt, question.id);
    assert.equal(question.explanation.reviewer, undefined, question.id);
  }
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

test("keeps official figures and shared passages usable", () => {
  const figuresOf = (question) => [
    ...(question.figures ?? []),
    ...question.options.flatMap((option) => option.figures ?? []),
    ...(question.passage?.blocks ?? [])
      .filter((block) => block.kind === "figure")
      .map((block) => block.figure),
  ];
  const seen = new Set();
  for (const question of questions) {
    for (const figure of figuresOf(question)) {
      assert.ok(figure.src.startsWith("/images/questions/"), figure.src);
      assert.ok(figure.alt.length > 0, figure.src);
      assert.ok(figure.width > 0 && figure.height > 0, figure.src);
      assert.ok(
        existsSync(new URL(`../public${figure.src}`, import.meta.url)),
        `missing asset ${figure.src}`,
      );
      seen.add(figure.src);
    }
    // 題幹沒有文字時必須有附圖，選項亦同，否則題目無法作答。
    assert.ok(
      question.prompt.length > 0 || (question.figures ?? []).length > 0,
      question.id,
    );
    for (const option of question.options) {
      assert.ok(
        option.text.length > 0 || (option.figures ?? []).length > 0,
        `${question.id} ${option.label}`,
      );
    }
    if (question.passage) {
      assert.ok(
        question.passage.questionNumbers.includes(question.officialQuestionNumber),
        question.id,
      );
      assert.ok(question.passage.blocks.length > 0, question.id);
    }
  }
  // 114 年第二次中級 38 張、115 年第一次中級 34 張。
  assert.equal(seen.size, 72);
});

test("uses unique stable question ids", () => {
  const ids = questions.map((question) => question.id);
  assert.equal(new Set(ids).size, ids.length);
  assert.ok(
    ids.every((id) =>
      importedPapers.some((paper) => id.startsWith(paper.idPrefix)),
    ),
  );
});

test("preserves complete question numbers and official answer sequences", () => {
  for (const paper of importedPapers) {
    const items = questions.filter(
      (question) =>
        question.level === paper.level &&
        question.rocYear === paper.rocYear &&
        question.session === paper.session &&
        question.subjectCode === paper.subjectCode,
    );
    const label = `${paper.rocYear}-${paper.session} ${paper.subjectCode}`;
    assert.equal(items.length, 50, label);
    assert.deepEqual(
      items.map((question) => question.officialQuestionNumber),
      Array.from({ length: 50 }, (_, index) => index + 1),
      label,
    );
    assert.equal(
      items.map((question) => question.officialAnswer[0]).join(""),
      paper.answers,
      label,
    );
    assert.ok(
      items.every(
        (question) =>
          question.sourcePage >= 1 && question.sourcePage <= paper.pageCount,
      ),
      label,
    );
    assert.ok(
      items.every(
        (question) => question.id === `${paper.idPrefix}${paper.subjectCode}-` +
          String(question.officialQuestionNumber).padStart(3, "0"),
      ),
      label,
    );
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
  // 盤點日為 2026-07-29；已於後續批次重新取得官方 PDF 的來源記錄實際取得日期。
  assert.ok(
    sources.every((source) =>
      ["2026-07-29", "2026-07-30", "2026-07-31"].includes(source.retrievedAt),
    ),
  );
  assert.ok(
    sources.every(
      (source) =>
        source.importedCount <= (source.expectedCount ?? 0) &&
        source.answerVerifiedCount <= source.importedCount &&
        source.explanationDraftCount <= source.importedCount &&
        source.explanationReviewedCount <= source.importedCount,
    ),
  );
  // 清冊的匯入數必須與實際題庫一致，不得單方面調高進度。
  for (const source of sources) {
    assert.equal(
      questions.filter((question) => question.sourceId === source.sourceId).length,
      source.importedCount,
      source.sourceId,
    );
  }
});

test("separates published, unavailable, future, and superseded work", () => {
  const count = (status) =>
    sources.filter((source) => source.availability === status).length;
  // 114 年 9 月版樣題五科已於 2026-07-31 遭官方下架，改列 not-found。
  assert.equal(count("published"), 12);
  assert.equal(count("not-found"), 14);
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
  assert.equal(manifest.inventoryCutoff, "2026-07-31");
  assert.equal(manifest.sourceCount, 38);
  assert.equal(manifest.officialQuestionCount, 600);
  assert.equal(manifest.practiceQuestionCount, 0);
  assert.equal(manifest.extractionStatus.verified, 600);
  assert.equal(manifest.explanationStatus.missing, 540);
  assert.equal(manifest.explanationStatus.draft, 60);
  assert.equal(manifest.explanationStatus.reviewed, 0);
  assert.deepEqual(manifest.countsByLevel, {
    elementary: 300,
    intermediate: 300,
  });
  assert.deepEqual(manifest.countsBySession, {
    "114-elementary-4": 100,
    "115-elementary-1": 100,
    "115-elementary-2": 100,
    "114-intermediate-2": 150,
    "115-intermediate-1": 150,
  });
  assert.deepEqual(manifest.collectionProgress, {
    examSessionCount: 12,
    publishedExamPaperCount: 12,
    publishedExamQuestionTarget: 600,
    currentSampleQuestionTarget: 0,
    knownQuestionTarget: 600,
    importedCount: 600,
    answerVerifiedCount: 600,
    explanationDraftCount: 60,
    explanationReviewedCount: 0,
    availability: {
      published: 12,
      "not-found": 14,
      scheduled: 7,
      superseded: 5,
    },
  });
  // 第一階段完成條件：目標、已匯入、答案已核對三者相等。
  assert.equal(
    manifest.collectionProgress.knownQuestionTarget,
    manifest.collectionProgress.importedCount,
  );
  assert.equal(
    manifest.collectionProgress.importedCount,
    manifest.collectionProgress.answerVerifiedCount,
  );
});
