# 題目資料格式與狀態規則

## 1. 題目 ID

正式試題建議格式：

```text
aiap-{level}-{rocYear}-{session}-{subjectCode}-{questionNumber}
```

例如：

```text
aiap-elementary-115-02-ai-foundation-023
```

官方樣題建議格式：

```text
aiap-{level}-sample-{version}-{subjectCode}-{questionNumber}
```

ID 建立後不得因為排序、文案修改或檔案搬移而變更，否則使用者的錯題紀錄會
失效。

## 2. 科目代碼

| 代碼 | 級別 | 科目 |
| --- | --- | --- |
| `ai-foundation` | 初級 | 人工智慧基礎概論 |
| `genai-planning` | 初級 | 生成式 AI 應用與規劃 |
| `ai-tech-planning` | 中級 | 人工智慧技術應用與規劃 |
| `big-data` | 中級 | 大數據處理分析與應用 |
| `machine-learning` | 中級 | 機器學習技術與應用 |

代碼如需更改，必須提供資料遷移，不直接破壞舊 ID。

## 3. 題目必要欄位

概念格式如下：

```ts
type Figure = {
  src: string; // 相對於 public/，例如 /images/questions/xxx.png
  alt: string;
  width: number;
  height: number;
};

type PassageBlock =
  | { kind: "text"; text: string }
  | { kind: "pre"; text: string } // 表格、程式碼或執行結果，需保留排版
  | { kind: "figure"; figure: Figure };

type Question = {
  id: string;
  sourceId: string;
  sourceType: "official-exam" | "official-sample";
  level: "elementary" | "intermediate";
  subjectCode: string;
  rocYear?: number;
  session?: string;
  officialQuestionNumber: number;
  sourcePage: number;
  passage?: {
    questionNumbers: number[]; // 共用此敘述的官方題號
    blocks: PassageBlock[];
  };
  prompt: string;
  figures?: Figure[]; // 題幹附圖
  options: {
    label: "A" | "B" | "C" | "D";
    text: string;
    figures?: Figure[]; // 選項本身是圖片時使用
  }[];
  officialAnswer: ("A" | "B" | "C" | "D")[];
  scoring: "single" | "multiple" | "all-credit" | "cancelled";
  sourceUrl: string;
  answerSourceUrl: string;
  extractionStatus: "imported" | "verified";
  explanationStatus: "missing" | "draft" | "reviewed";
  explanation?: QuestionExplanation;
};
```

不能把複數答案、送分或取消題強制轉成一般單選答案。

官方 PDF 內嵌的圖表、程式碼截圖與公式圖必須隨題目一起匯入，不得只留文字：

- 圖片檔放在 `public/images/questions/`，檔名須可追溯到來源試卷與頁碼。
- 圖片要掛在正確位置：題幹用 `figures`，選項用 `options[].figures`，題組敘述
  用 `passage.blocks` 中的 `figure` 區塊。
- 題幹或選項可以沒有文字，但不得同時沒有文字與圖片。
- 題組敘述複製到該組每一題，讓每題都能單獨作答。

## 4. 詳解格式

```ts
type QuestionExplanation = {
  summary: string;
  concept: string;
  answerReason: string;
  optionAnalysis: Partial<Record<"A" | "B" | "C" | "D", string>>;
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
```

若詳解狀態是 `reviewed`，`reviewer` 與 `reviewedAt` 必須存在。

`draft` 階段尚未完成實質撰寫的選項可以不放入 `optionAnalysis`；前端只顯示
非空白內容。不得用「不符合題幹」、「適用情境不同」等模板句填滿 A～D。
`reviewed` 狀態則必須具備 A、B、C、D 四個符合撰寫規則的選項解析。

## 5. 狀態的精確含義

### `extractionStatus`

- `imported`：已由 PDF 或其他官方文件轉成資料，但尚未逐題目視核對。
- `verified`：已對照官方頁面核對題幹、選項、答案、頁碼與來源。

### `explanationStatus`

- `missing`：只有官方題目與答案，沒有自行撰寫的詳解。
- `draft`：已有詳解初稿，但尚未完成獨立複核。
- `reviewed`：已依撰寫規則完成查證與複核。

不得因為有 AI 產生的文字，就直接把狀態設成 `reviewed`。

## 6. 時效性欄位

技術產品、模型能力、法規與官方政策可能改變。解析若依賴這類資訊，參考資料
必須包含 `checkedAt`，並在必要時說明：

- 題目以考試當時的知識範圍判斷。
- 現行技術或規定可能已有更新。
- 更新後的事實不應反過來擅自更改官方答案。

## 7. manifest

建置時應產生可重算的 manifest，至少包含：

- 題庫盤點截止日期。
- 來源文件總數及各狀態數量。
- 題目總數。
- 各級別、科目、年度、梯次及來源類型題數。
- `verified` 題數。
- `missing`、`draft`、`reviewed` 詳解題數。
- 題庫內容雜湊。

網站顯示的題數必須來自 manifest，不可手動寫死。
