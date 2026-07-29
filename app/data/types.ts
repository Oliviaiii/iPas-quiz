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
  optionAnalysis: Record<OptionLabel, string>;
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
  prompt: string;
  options: {
    label: OptionLabel;
    text: string;
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
