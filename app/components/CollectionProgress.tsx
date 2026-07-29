import sourceData from "../data/sources.json";
import type {
  Level,
  SourceAvailability,
  SourceInventoryItem,
} from "../data/types";

const sources = sourceData as SourceInventoryItem[];

const levelLabels: Record<Level, string> = {
  elementary: "初級",
  intermediate: "中級",
};

const availabilityLabels: Record<SourceAvailability, string> = {
  published: "官方已公告・待匯入",
  "not-found": "官方未提供試題",
  scheduled: "尚未考試",
  superseded: "舊版樣題",
};

function groupExamSessions(level: Level) {
  const items = sources.filter(
    (source) => source.sourceType === "official-exam" && source.level === level,
  );
  return Array.from(
    Map.groupBy(items, (source) => `${source.rocYear}-${source.session}`).values(),
  );
}

function sum(
  items: SourceInventoryItem[],
  field:
    | "expectedCount"
    | "importedCount"
    | "answerVerifiedCount"
    | "explanationReviewedCount",
) {
  return items.reduce((total, item) => total + (item[field] ?? 0), 0);
}

function sessionAvailability(items: SourceInventoryItem[]): SourceAvailability {
  if (items.every((item) => item.availability === "published")) return "published";
  if (items.every((item) => item.availability === "scheduled")) return "scheduled";
  return "not-found";
}

function sessionStatus(items: SourceInventoryItem[], availability: SourceAvailability) {
  const expected = sum(items, "expectedCount");
  if (expected > 0 && sum(items, "explanationReviewedCount") === expected) {
    return { label: "題目與詳解已完成", className: "complete" };
  }
  if (expected > 0 && sum(items, "importedCount") === expected) {
    return { label: "題目已匯入・詳解待複核", className: "imported" };
  }
  return {
    label: availabilityLabels[availability],
    className: availability,
  };
}

function ProgressMeter({
  label,
  value,
  total,
}: {
  label: string;
  value: number;
  total: number | null;
}) {
  const percentage = total ? Math.round((value / total) * 100) : 0;
  return (
    <div className="meter">
      <div className="meter-label">
        <span>{label}</span>
        <b>{total === null ? "待官方公告" : `${value} / ${total}`}</b>
      </div>
      <div className="meter-track" aria-hidden="true">
        <span style={{ width: `${percentage}%` }} />
      </div>
    </div>
  );
}

export function CollectionProgress() {
  const targetSources = sources.filter((source) => source.inclusion === "target");
  const publishedPapers = sources.filter(
    (source) =>
      source.sourceType === "official-exam" &&
      source.availability === "published",
  );
  const sampleSources = sources.filter(
    (source) =>
      source.sourceType === "official-sample" &&
      source.availability === "published",
  );
  const legacySamples = sources.filter(
    (source) => source.availability === "superseded",
  );

  return (
    <section className="collection-progress" aria-labelledby="collection-title">
      <div className="section-heading">
        <div>
          <p className="eyebrow">OFFICIAL SOURCE INVENTORY</p>
          <h2 id="collection-title">初級與中級完整進度</h2>
        </div>
        <p>
          盤點截止 2026-07-29。題數只計入已找到官方 PDF 的文件；
          找不到與尚未考試的場次仍保留追蹤。
        </p>
      </div>

      <div className="inventory-summary">
        <div>
          <span>官方歷屆試卷</span>
          <strong>{publishedPapers.length} 份</strong>
          <small>每科 50 題，共 {sum(publishedPapers, "expectedCount")} 題</small>
        </div>
        <div>
          <span>最新版官方樣題</span>
          <strong>{sum(sampleSources, "expectedCount")} 題</strong>
          <small>初級 70 題・中級 45 題</small>
        </div>
        <div>
          <span>目前已知匯入目標</span>
          <strong>{sum(targetSources, "expectedCount")} 題</strong>
          <small>目前已匯入 {sum(targetSources, "importedCount")} 題</small>
        </div>
        <div>
          <span>待持續追蹤</span>
          <strong>
            {sources.filter((source) => source.availability === "not-found").length} +{" "}
            {sources.filter((source) => source.availability === "scheduled").length} 科
          </strong>
          <small>官方未提供 + 尚未考試</small>
        </div>
      </div>

      {(Object.keys(levelLabels) as Level[]).map((level) => {
        const sessions = groupExamSessions(level);
        return (
          <section className="level-progress" key={level}>
            <div className="level-heading">
              <h3>{levelLabels[level]}歷屆試題</h3>
              <span>{sessions.length} 個考試場次</span>
            </div>
            <div className="session-grid">
              {sessions.map((items) => {
                const first = items[0];
                const availability = sessionAvailability(items);
                const status = sessionStatus(items, availability);
                const expected = items.some((item) => item.expectedCount === null)
                  ? null
                  : sum(items, "expectedCount");
                return (
                  <article className="session-card" key={`${level}-${first.rocYear}-${first.session}`}>
                    <div className="session-title">
                      <div>
                        <span>{first.examDate}</span>
                        <h4>
                          {first.rocYear} 年{first.sessionLabel}
                        </h4>
                      </div>
                      <span className={`source-status ${status.className}`}>
                        {status.label}
                      </span>
                    </div>

                    <ul className="subject-list">
                      {items.map((item) => (
                        <li key={item.sourceId}>
                          <span>{item.subjectLabel}</span>
                          {item.availability === "published" ? (
                            <a href={item.url} target="_blank" rel="noreferrer">
                              官方 PDF
                            </a>
                          ) : (
                            <small>
                              {item.availability === "scheduled" ? "待考後追蹤" : "未列於官方題庫頁"}
                            </small>
                          )}
                        </li>
                      ))}
                    </ul>

                    <ProgressMeter
                      label="題目匯入"
                      value={sum(items, "importedCount")}
                      total={expected}
                    />
                    <ProgressMeter
                      label="詳解複核"
                      value={sum(items, "explanationReviewedCount")}
                      total={expected}
                    />
                  </article>
                );
              })}
            </div>
          </section>
        );
      })}

      <div className="sample-note">
        <div>
          <b>官方樣題也納入工作範圍</b>
          <p>
            最新 114 年 9 月版共 115 題，會納入正式匯入目標。114 年 1 月舊版共{" "}
            {sum(legacySamples, "expectedCount")} 題，先作版本稽核與重複比對，不重複灌入題庫。
          </p>
        </div>
        <a
          href="https://ipd.nat.gov.tw/ipas/certification/AIAP/learning-resources"
          target="_blank"
          rel="noreferrer"
        >
          查看官方學習資源
        </a>
      </div>
    </section>
  );
}
