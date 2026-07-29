"use client";

import { useEffect, useMemo, useState } from "react";
import questionData from "../data/questions.json";
import type { Level, OptionLabel, Question, SubjectCode } from "../data/types";
import { loadProgress, saveProgress, type Progress } from "../lib/progress";
import { QuestionCard } from "./QuestionCard";

const questions = questionData as Question[];

const levelLabels: Record<Level, string> = {
  elementary: "初級",
  intermediate: "中級",
};

export function QuizApp() {
  const [level, setLevel] = useState<Level>("elementary");
  const [subject, setSubject] = useState<SubjectCode | "all">("all");
  const [wrongOnly, setWrongOnly] = useState(false);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [progress, setProgress] = useState<Progress>({});
  const [ready, setReady] = useState(false);

  useEffect(() => {
    const frame = window.requestAnimationFrame(() => {
      const savedProgress = loadProgress();
      const validQuestionIds = new Set(questions.map((question) => question.id));
      const validProgress = Object.fromEntries(
        Object.entries(savedProgress).filter(([questionId]) =>
          validQuestionIds.has(questionId),
        ),
      );
      setProgress(validProgress);
      if (Object.keys(validProgress).length !== Object.keys(savedProgress).length) {
        saveProgress(validProgress);
      }
      setReady(true);
    });
    return () => window.cancelAnimationFrame(frame);
  }, []);

  const subjects = useMemo(
    () =>
      Array.from(
        new Map(
          questions
            .filter((question) => question.level === level)
            .map((question) => [question.subjectCode, question.subjectLabel]),
        ),
      ),
    [level],
  );

  const filtered = useMemo(
    () =>
      questions.filter((question) => {
        if (question.level !== level) return false;
        if (subject !== "all" && question.subjectCode !== subject) return false;
        if (wrongOnly && progress[question.id]?.correct !== false) return false;
        return true;
      }),
    [level, progress, subject, wrongOnly],
  );

  function choose(question: Question, selected: OptionLabel) {
    if (progress[question.id]) return;
    const next = {
      ...progress,
      [question.id]: {
        selected,
        correct: question.officialAnswer.includes(selected),
        answeredAt: new Date().toISOString(),
      },
    };
    setProgress(next);
    saveProgress(next);
  }

  function resetProgress() {
    const next = {};
    setProgress(next);
    saveProgress(next);
    setWrongOnly(false);
  }

  const answeredCount = Object.keys(progress).length;
  const wrongCount = Object.values(progress).filter((answer) => !answer.correct).length;
  const current = filtered[currentIndex];

  return (
    <main>
      <header className="hero">
        <div className="hero-copy">
          <p className="kicker">iPAS AI APPLICATION PLANNER</p>
          <h1>AI 應用規劃師刷題工具</h1>
          <p>
            初級與中級考古題依官方來源逐批匯入。現在可練習初級 114 年第四次、
            115 年第一次與第二次兩科試題，以及中級 114 年第二次三科；作答後會顯示
            官方答案，已完成撰寫的題目另有本站自編詳解。
          </p>
        </div>
      </header>

      <section className="dashboard" aria-label="作答統計">
        <div>
          <span>已作答</span>
          <strong>{answeredCount}</strong>
        </div>
        <div>
          <span>錯題</span>
          <strong>{wrongCount}</strong>
        </div>
        <div>
          <span>目前級別</span>
          <strong>{levelLabels[level]}</strong>
        </div>
      </section>

      <section className="workspace">
        <aside className="filters">
          <div>
            <p className="eyebrow">選擇級別</p>
            <div className="segmented">
              {(Object.keys(levelLabels) as Level[]).map((value) => (
                <button
                  type="button"
                  className={level === value ? "active" : ""}
                  key={value}
                  onClick={() => {
                    setLevel(value);
                    setSubject("all");
                    setCurrentIndex(0);
                  }}
                >
                  {levelLabels[value]}
                </button>
              ))}
            </div>
          </div>

          <label>
            <span className="eyebrow">科目</span>
            <select
              value={subject}
              onChange={(event) => {
                setSubject(event.target.value as SubjectCode | "all");
                setCurrentIndex(0);
              }}
            >
              <option value="all">全部科目</option>
              {subjects.map(([code, label]) => (
                <option key={code} value={code}>
                  {label}
                </option>
              ))}
            </select>
          </label>

          <button
            type="button"
            className={`filter-toggle ${wrongOnly ? "active" : ""}`}
            onClick={() => {
              setWrongOnly((value) => !value);
              setCurrentIndex(0);
            }}
          >
            只看錯題
            <span>{wrongCount}</span>
          </button>

          <button type="button" className="text-button" onClick={resetProgress}>
            清除作答進度
          </button>

          <div className="notice">
            <b>資料說明</b>
            <p>
              本批題幹與答案取自官方公告 PDF。本站只顯示有實質內容的自編解析；
              尚未完成的選項解析不以模板文字充數。
            </p>
          </div>
        </aside>

        <div className="quiz-area">
          {!ready ? (
            <div className="empty-state">讀取作答紀錄中…</div>
          ) : current ? (
            <QuestionCard
              key={current.id}
              question={current}
              position={currentIndex + 1}
              total={filtered.length}
              answer={progress[current.id]}
              onAnswer={(selected) => choose(current, selected)}
              onMove={(direction) =>
                setCurrentIndex((index) => {
                  const next = index + direction;
                  if (next < 0) return filtered.length - 1;
                  if (next >= filtered.length) return 0;
                  return next;
                })
              }
            />
          ) : (
            <div className="empty-state">
              <strong>目前沒有符合條件的題目</strong>
              <p>{wrongOnly ? "完成作答後，答錯的題目會出現在這裡。" : "請調整篩選條件。"}</p>
            </div>
          )}
        </div>
      </section>

      <footer className="site-footer">
        <p>非 iPAS 官方網站。題目依官方公開資料整理；詳解為本站自編內容。</p>
        <p>作答紀錄只保存在你的瀏覽器中。</p>
      </footer>
    </main>
  );
}
