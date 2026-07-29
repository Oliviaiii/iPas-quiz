export type Level = "elementary" | "intermediate";

export type SubjectCode =
  | "ai-foundation"
  | "genai-planning"
  | "ai-tech-planning"
  | "big-data"
  | "machine-learning";

export type OptionLabel = "A" | "B" | "C" | "D";

export type QuestionExplanation = {
  summary: string;
  concept: string;
  answerReason: string;
  optionAnalysis: Partial<Record<OptionLabel, string>>;
  trap: string;
  references: {
    title: string;
    url: string;
    locator?: string;
    checkedAt: string;
  }[];
  editorialNote?: string;
  author: string;
  authoredAt: string;
  reviewer?: string;
  reviewedAt?: string;
};

/** 官方 PDF 內嵌的圖片：圖表、程式碼截圖或公式圖。 */
export type Figure = {
  /** 相對於 public/ 的路徑，例如 /images/questions/xxx.png。 */
  src: string;
  alt: string;
  width: number;
  height: number;
};

/** 題組敘述由文字、預格式區塊（表格／程式輸出）與圖片依序組成。 */
export type PassageBlock =
  | { kind: "text"; text: string }
  | { kind: "pre"; text: string }
  | { kind: "figure"; figure: Figure };

export type Passage = {
  /** 共用此敘述的官方題號，例如 [43, 44, 45, 46, 47]。 */
  questionNumbers: number[];
  blocks: PassageBlock[];
};

export type Question = {
  id: string;
  sourceId: string;
  sourceType: "official-exam" | "official-sample";
  level: Level;
  subjectCode: SubjectCode;
  subjectLabel: string;
  rocYear: number;
  session: string;
  officialQuestionNumber: number;
  sourcePage: number;
  passage?: Passage;
  prompt: string;
  figures?: Figure[];
  options: {
    label: OptionLabel;
    text: string;
    figures?: Figure[];
  }[];
  officialAnswer: OptionLabel[];
  scoring: "single";
  sourceUrl: string;
  answerSourceUrl: string;
  extractionStatus: "imported" | "verified";
  explanationStatus: "missing" | "draft" | "reviewed";
  explanation: QuestionExplanation;
};

export type SourceAvailability =
  | "published"
  | "not-found"
  | "scheduled"
  | "superseded";

export type SourceInventoryItem = {
  sourceId: string;
  title: string;
  sourceType: "official-exam" | "official-sample";
  level: Level;
  subjectCode: SubjectCode;
  subjectLabel: string;
  rocYear: number;
  session: string;
  sessionLabel: string;
  examDate: string | null;
  publishedAt: string | null;
  url: string;
  retrievedAt: string;
  expectedCount: number | null;
  importedCount: number;
  answerVerifiedCount: number;
  explanationDraftCount: number;
  explanationReviewedCount: number;
  availability: SourceAvailability;
  inclusion: "target" | "audit-only";
  notes: string;
};
