"use client";

import type { OptionLabel, Question } from "../data/types";
import type { StoredAnswer } from "../lib/progress";

export function QuestionCard({
  question,
  position,
  total,
  answer,
  onAnswer,
  onMove,
}: {
  question: Question;
  position: number;
  total: number;
  answer?: StoredAnswer;
  onAnswer: (label: OptionLabel) => void;
  onMove: (direction: -1 | 1) => void;
}) {
  const correctAnswer = question.officialAnswer[0];

  return (
    <article className="question-card">
      <div className="question-topline">
        <div className="tag-row">
          <span className="tag">
            {question.rocYear} 年第{question.session}次・官方公告試題
          </span>
          <span className="tag">{question.subjectLabel}</span>
          {question.explanationStatus === "draft" ? (
            <span className="tag draft">詳解初稿</span>
          ) : null}
        </div>
        <span className="question-position">
          官方第 {question.officialQuestionNumber} 題・{position} / {total}
        </span>
      </div>

      <h2>{question.prompt}</h2>

      <div className="options" aria-label="作答選項">
        {question.options.map((option) => {
          const isSelected = answer?.selected === option.label;
          const isCorrect = Boolean(answer && option.label === correctAnswer);
          const isWrong = Boolean(answer && isSelected && !answer.correct);
          return (
            <button
              type="button"
              key={option.label}
              className={`option ${isCorrect ? "correct" : ""} ${isWrong ? "wrong" : ""}`}
              disabled={Boolean(answer)}
              onClick={() => onAnswer(option.label)}
            >
              <span className="option-label">{option.label}</span>
              <span>{option.text}</span>
              {isCorrect ? <strong>正確答案</strong> : null}
              {isWrong ? <strong>你的答案</strong> : null}
            </button>
          );
        })}
      </div>

      {answer ? (
        <section
          className={`analysis ${answer.correct ? "analysis-correct" : "analysis-wrong"}`}
          aria-live="polite"
        >
          <div className="result-heading">
            <span>{answer.correct ? "答對了" : "這題答錯了"}</span>
            <strong>正確答案：{correctAnswer}</strong>
          </div>
          <p className="analysis-summary">{question.explanation.summary}</p>

          <div className="analysis-grid">
            <section>
              <p className="eyebrow">核心觀念</p>
              <p>{question.explanation.concept}</p>
            </section>
            <section>
              <p className="eyebrow">解題理由</p>
              <p>{question.explanation.answerReason}</p>
            </section>
          </div>

          <section className="option-analysis">
            <p className="eyebrow">選項分析</p>
            {question.options.map((option) => (
              <div key={option.label}>
                <b>{option.label}</b>
                <p>{question.explanation.optionAnalysis[option.label]}</p>
              </div>
            ))}
          </section>

          <div className="trap-note">
            <b>容易混淆</b>
            <p>{question.explanation.trap}</p>
          </div>

          {question.explanation.editorialNote ? (
            <p className="editorial-note">{question.explanation.editorialNote}</p>
          ) : null}

          <div className="reference-list">
            <p className="eyebrow">參考來源</p>
            <ul>
              {question.explanation.references.map((reference) => (
                <li key={`${reference.url}-${reference.locator ?? ""}`}>
                  <a href={reference.url} target="_blank" rel="noreferrer">
                    {reference.title}
                  </a>
                  {reference.locator ? `－${reference.locator}` : ""}
                </li>
              ))}
            </ul>
          </div>
        </section>
      ) : (
        <p className="answer-hint">選擇答案後，會立即顯示結果與詳解初稿。</p>
      )}

      <footer className="question-navigation">
        <button type="button" onClick={() => onMove(-1)}>
          上一題
        </button>
        <button type="button" className="primary" onClick={() => onMove(1)}>
          下一題
        </button>
      </footer>
    </article>
  );
}
