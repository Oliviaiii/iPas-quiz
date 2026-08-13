# 獨立 AI 複核規則

最後更新：2026-08-13

## 1. 定位

本流程是第二階段 B 之前的「獨立 AI 複核」，用來降低後續人工複核負擔。
複核者必須是不同於原詳解撰寫者的新 AI 工作階段，不得只沿用原撰寫結論。

獨立 AI 複核不是人工複核，因此：

- 題目維持 `explanationStatus: draft`。
- 不填入 `reviewer` 或 `reviewedAt`。
- 不增加 `explanationReviewedCount`。
- 不得在文件或網站宣稱已完成獨立人工複核。

## 2. 每題必查項目

1. 對照官方 PDF，核對題幹、A～D 選項、官方答案、頁碼、附圖及共用題組。
2. 不參考原詳解結論，先獨立判斷正確答案及四個選項。
3. 再檢查既有 `summary`、`concept`、`answerReason`、`optionAnalysis` 與 `trap`。
4. 開啟參考來源，確認網址可用、定位可支持實際敘述、查核日期合理。
5. 檢查時效、法域、版本、前提條件、過度絕對語氣及可能的複選疑義。
6. 若發現可確定修正的錯誤，建立具防護條件的修正腳本；不得直接修改共用題庫。

PDF 不能只靠文字擷取。含表格、公式、程式碼或圖片的題目必須渲染頁面並目視。

## 3. 結果分類

每題只能使用以下一種結果：

- `pass`：未發現需修改事項，適合交由人工作最終簽核。
- `corrected`：發現明確錯誤，已提出並驗證修正腳本；套用後仍維持 `draft`。
- `human-decision`：官方答案、選項區辨、法規全文、產品版本或來源證據仍需人類判斷。
- `blocked`：官方 PDF、必要圖片或權威來源無法取得，尚不足以完成複核。

不得因為原文已有 `editorialNote` 就自動判為 `human-decision`；複核者須自行驗證該疑義是否仍成立。

## 4. 批次紀錄

每批固定 10 題，在 `reviews/ai-independent/` 建立一份 JSON：

```json
{
  "schemaVersion": 1,
  "reviewType": "independent-ai",
  "sourceId": "...",
  "range": { "start": 1, "end": 10 },
  "reviewedAt": "YYYY-MM-DD",
  "reviewer": "Codex independent AI reviewer",
  "counts": { "pass": 0, "corrected": 0, "humanDecision": 0, "blocked": 0 },
  "items": [
    {
      "questionId": "...",
      "officialQuestionNumber": 1,
      "officialAnswer": "A",
      "answerIndependentlyConfirmed": true,
      "result": "pass",
      "findings": [],
      "sourcesChecked": [
        { "title": "...", "url": "https://...", "locator": "...", "checkedAt": "YYYY-MM-DD" }
      ]
    }
  ]
}
```

`items` 必須剛好 10 筆、題號連續、計數一致。若結果不是 `pass`，`findings` 必須寫清楚風險、證據與建議動作。

## 5. 修正與人工簽核

- 明確錯誤可在 AI 複核階段修正，但修正後仍是新的 AI 初稿，必須保留 `draft`。
- 有解釋空間時保留官方答案，記錄為 `human-decision`，不可擅自改答案。
- 只有指定的人類複核者逐題確認後，才能填入 `reviewer`、`reviewedAt` 並改成 `reviewed`。
