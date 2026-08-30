# 獨立 AI 複核進度

最後更新：2026-08-30

## 目前狀態

- 固定題庫：600 題。
- 獨立 AI 複核：210／600。
- 獨立人工複核：0／600。
- 已完成：114 年第四次初級兩科 100 題、115 年第一次初級兩科 100 題、
  115 年第二次初級第一科第 1～10 題。
- 下一批：115 年第二次初級第一科第 11～20 題。
- 累計分類：`pass 150`、`corrected 41`、`human-decision 18`、`blocked 1`。

AI 複核通過不等於人工複核完成；所有題目在人工簽核前維持 `draft`。

## 批次紀錄

| 試卷／科目 | 題號 | AI 複核結果 | 人工簽核 |
| --- | --- | --- | --- |
| 114 年第四次初級－人工智慧基礎概論 | 1～50 | 完成（pass 37／corrected 5／human-decision 7／blocked 1） | 未開始 |
| 114 年第四次初級－生成式 AI 應用與規劃 | 1～50 | 完成（pass 28／corrected 14／human-decision 8） | 未開始 |
| 115 年第一次初級－人工智慧基礎概論 | 1～50 | 完成（pass 41／corrected 7／human-decision 2） | 未開始 |
| 115 年第一次初級－生成式 AI 應用與規劃 | 1～30 | 完成（pass 22／corrected 7／human-decision 1） | 未開始 |
| 115 年第一次初級－生成式 AI 應用與規劃 | 31～40 | 完成（pass 7／corrected 3） | 未開始 |
| 115 年第一次初級－生成式 AI 應用與規劃 | 41～50 | 完成（pass 9／corrected 1） | 未開始 |
| 115 年第二次初級－人工智慧基礎概論 | 1～10 | 完成（pass 6／corrected 4） | 未開始 |

## 複核工具與環境

官方 PDF 不進版控。開始複核前需放行 `www.ipas.org.tw`，把 12 份公告試題與 2 份
初級學習指引下載到 `tmp/pdfs/`，檔名使用 `sourceId.pdf`。所需套件為
`pymupdf`（PDF 文字擷取與頁面渲染）。

`scripts/ai-review-context.py` 把一批題目與官方 PDF 併排輸出，供逐題比對：

```sh
python scripts/ai-review-context.py <sourceId> --answers      # 只抽答案欄做交叉檢查
python scripts/ai-review-context.py <sourceId> --pages 7-9    # 傾印 PDF 頁面文字
python scripts/ai-review-context.py <sourceId> 41 50          # 題庫內容與詳解初稿
python scripts/ai-review-context.py <sourceId> --render 7,8   # 需目視的頁面轉 PNG
```

`--answers` 會把公告試題左欄的官方答案與題庫的 `officialAnswer` 對照。2026-08-30
對 12 份試卷全數執行的結果：600 題中 581 題可自動抽出答案欄，**零筆衝突**；其餘
19 題因該列含附圖或跨頁而抽取不到（顯示為 `pdf None`，不是答案不一致），仍須在
所屬批次以渲染頁面目視確認。

## 接手注意事項

- 每批仍固定 10 題，完成後使用 `scripts/validate-ai-review-reports.py` 驗證。
- `corrected` 的修正只能保持 `draft`；不得填入 `reviewer`／`reviewedAt`。
- `human-decision` 與 `blocked` 應集中交給人工複核者，不可算入人工完成數。
- 所有報告位於 `reviews/ai-independent/`；流程規則見 `AI_REVIEW_GUIDE.md`。
- 已知跨題全站項目：部分詳解內文的英數字與中文之間漏空格（例如「只有 A直接對應」），
  屬排版瑕疵而非內容錯誤，宜另案一次掃過，不逐批計入 `corrected`。
