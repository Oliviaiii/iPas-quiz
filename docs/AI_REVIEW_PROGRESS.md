# 獨立 AI 複核進度

最後更新：2026-08-13

## 目前狀態

- 固定題庫：600 題。
- 獨立 AI 複核：190／600。
- 獨立人工複核：0／600。
- 已完成：114 年第四次初級兩科 100 題、115 年第一次初級第一科 50 題、
  115 年第一次初級第二科第 1～40 題。
- 下一批：115 年第一次初級第二科第 41～50 題。
- 累計分類：`pass 135`、`corrected 36`、`human-decision 18`、`blocked 1`。

AI 複核通過不等於人工複核完成；所有題目在人工簽核前維持 `draft`。

## 批次紀錄

| 試卷／科目 | 題號 | AI 複核結果 | 人工簽核 |
| --- | --- | --- | --- |
| 114 年第四次初級－人工智慧基礎概論 | 1～50 | 完成（pass 37／corrected 5／human-decision 7／blocked 1） | 未開始 |
| 114 年第四次初級－生成式 AI 應用與規劃 | 1～50 | 完成（pass 28／corrected 14／human-decision 8） | 未開始 |
| 115 年第一次初級－人工智慧基礎概論 | 1～50 | 完成（pass 41／corrected 7／human-decision 2） | 未開始 |
| 115 年第一次初級－生成式 AI 應用與規劃 | 1～30 | 完成（pass 22／corrected 7／human-decision 1） | 未開始 |
| 115 年第一次初級－生成式 AI 應用與規劃 | 31～40 | 完成（pass 7／corrected 3） | 未開始 |

## 接手注意事項

- 每批仍固定 10 題，完成後使用 `scripts/validate-ai-review-reports.py` 驗證。
- `corrected` 的修正只能保持 `draft`；不得填入 `reviewer`／`reviewedAt`。
- `human-decision` 與 `blocked` 應集中交給人工複核者，不可算入人工完成數。
- 所有報告位於 `reviews/ai-independent/`；流程規則見 `AI_REVIEW_GUIDE.md`。
