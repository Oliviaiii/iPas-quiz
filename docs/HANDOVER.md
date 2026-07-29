# 專案交接清單

## 目前進度（2026-07-29）

- 114～115 年初級 8 個場次、中級 4 個場次已建立逐科追蹤。
- 官方目前提供 12 份歷屆試卷，共 600 題；已匯入 450 題：初級 6 份共 300 題
  （114 年第四次、115 年第一次、115 年第二次），以及 114 年第二次中級三科
  150 題。
- 最新 114 年 9 月版官方樣題共 115 題；尚未匯入。
- 114 年 1 月舊版樣題共 25 題，列為重複題與版本稽核，不直接加入目標。
- 已匯入的 450 題與官方答案均已逐頁核對；目前僅 3 題有實質 A～D 詳解初稿，
  其餘 447 題為 `missing`，尚未有任何題目完成人工複核。
- 專案目前採兩階段執行：第一階段先完成 715 題全部匯入與答案核對，第二階段
  才統一處理全部詳解。
- 題目資料已支援官方附圖與共用題組敘述；中級試卷的圖片題須連同圖片匯入。
- 下一個內容工作為匯入 115 年第一次中級三科共 150 題；暫不撰寫詳解。
- 詳細數字與官方入口見 [題源與匯入進度](SOURCE_INVENTORY.md)。

每位接手者開始工作前，應先閱讀：

1. `README.md`
2. `docs/DELIVERY_PHASES.md`
3. `docs/PROJECT_PLAN.md`
4. `docs/SOURCE_AND_COVERAGE_RULES.md`
5. `docs/QUESTION_DATA_SPEC.md`
6. `docs/QUESTION_AUTHORING_GUIDE.md`
7. `docs/DEPLOYMENT.md`
8. `docs/SOURCE_INVENTORY.md`

## 每次開始工作前

- 確認目前分支與工作目錄狀態。
- 查看是否有其他人尚未提交的變更。
- 確認來源清冊的盤點截止日期。
- 確認目前是第一階段題目匯入，還是第二階段詳解工作；不得混做。
- 確認本次處理的級別、科目、年度、梯次及題號範圍。
- 確認工作屬於匯入、核對、詳解撰寫或複核，不混淆狀態。

## 每次結束工作前

每完成一個可交付進度（例如一科、一個場次、一批詳解或一次部署），必須在同一批
變更中同步更新 `docs/SOURCE_INVENTORY.md` 與本文件；若資料格式、來源規則或操作
方式有變，也要一併更新對應規格文件。不得只改程式或題庫而留下過期文件。

留下以下資訊：

- 本次處理的來源文件。
- 新增或修改的題目 ID。
- 匯入、核對、初稿及複核各完成幾題。
- 尚未解決的 PDF 擷取或答案爭議。
- 使用過的參考資料與查核日期。
- 執行過的測試及結果。
- 尚未執行的測試及原因。
- 是否有需要下一位接手者優先處理的項目。

## 建議交接格式

```md
## YYYY-MM-DD 工作交接

- 處理範圍：
- 官方來源：
- 新增題目：
- 已核對題目：
- 詳解初稿：
- 已複核詳解：
- 來源清冊更新：
- 執行測試：
- 未解問題：
- 下一步：
```

## 禁止在交接時使用的模糊說法

- 「題目應該都好了。」
- 「AI 已經檢查過。」
- 「看起來沒有問題。」
- 「大部分詳解已完成。」

應改成可以驗證的數量、題目 ID、來源網址及測試結果。

## 2026-07-29 基礎架構交接

- 處理範圍：Next.js 靜態刷題骨架、GitHub Pages workflow、Cloudflare Analytics 注入。
- 官方來源：尚未建立正式來源清冊；`app/data/sources.json` 目前為空。
- 新增題目：4 題非官方介面示範題。
- 官方題目：0 題。
- 已核對題目：示範題 4 題；不能算入官方題庫。
- 詳解初稿：示範題 4 題。
- 已複核詳解：示範題 4 題；此狀態只代表介面測試資料。
- 來源清冊更新：尚未開始。
- 執行測試：資料測試、ESLint、Next.js 靜態建置與瀏覽器作答流程。
- GitHub repository：https://github.com/Oliviaiii/iPas-quiz
- 正式網站：https://oliviaiii.github.io/iPas-quiz/
- 流量分析：Cloudflare Web Analytics 的 `oliviaiii.github.io` 網站，查看
  `/iPas-quiz/` 路徑。
- 未解問題：待建立官方來源清冊並逐批匯入正式試題。
- 下一步：盤點官方試卷，建立 `official-exam`／`official-sample` 資料。

## 2026-07-29 114 年第四次初級交接

- 處理範圍：114 年第四次初級第一科、第二科，共 100 題。
- 官方來源：兩份 iPAS 官方公告試題 PDF，逐頁渲染後核對題幹、A～D 選項、
  官方答案與來源頁碼。
- 新增題目：`aiap-elementary-114-04-ai-foundation-001` 至 `050`，
  以及 `aiap-elementary-114-04-genai-planning-001` 至 `050`。
- 移除題目：原有 4 題非官方介面示範題；舊的瀏覽器作答紀錄會在載入時自動清除。
- 已核對題目：100 題；`extractionStatus` 均為 `verified`。
- 詳解初稿：原有 100 題模板初稿已撤回；目前只有第 2～4 題共 3 題計為
  實質詳解初稿。
- 已複核詳解：0 題；不得把 `draft` 說成已人工複核。
- 來源清冊更新：兩科各為匯入 50、答案核對 50；第一科詳解初稿 3、第二科
  詳解初稿 0、詳解複核均為 0。
- 執行測試：資料完整性、官方答案序列、ESLint、Next.js 靜態建置及瀏覽器
  答錯後顯示詳解流程。
- 未解問題：97 題待撰寫實質詳解；3 題初稿仍需獨立人工複核。
- 當時建議的下一步是詳解複核或繼續匯入；此建議已由後續兩階段決策取代，
  現在固定先匯入 115 年第一次初級兩科。

## 2026-07-29 公開頁面進度資訊調整

- 處理範圍：移除首頁的題庫狀態卡、來源摘要、各年度場次卡及匯入／詳解複核
  進度條。
- 保留內容：作答統計、題目篩選、錯題功能與題目本身不受影響。
- 內部追蹤：題庫進度繼續維護於 `docs/SOURCE_INVENTORY.md`、
  `docs/HANDOVER.md`、`app/data/sources.json`。
- 新增規則：每完成一個可交付進度，必須在同一批變更中同步更新相關文件。

## 2026-07-29 選項解析品質修正

- 問題：114 年第四次初級 100 題的 A～D 選項分析使用「沒有滿足題幹的關鍵
  條件」、「機制或適用情境不同」等模板句，沒有提供可學習的內容。
- 移除內容：所有上述模板式選項解析；未完成實質改寫的欄位保持空白，前端不顯示。
- 已完成實質改寫：人工智慧基礎概論第 2、3、4 題，共 3 題、12 個選項。
- 尚待改寫：人工智慧基礎概論 47 題、生成式 AI 應用與規劃 50 題，共 97 題。
- 規則更新：`docs/QUESTION_AUTHORING_GUIDE.md` 已加入禁用句、最低資訊要求及
  「寧缺勿濫」顯示規則；自動測試會阻擋同類模板句再次進入題庫。
- 下一步：依題號逐批補寫 97 題實質 A～D 解析，每批完成後同步更新清冊與交接。

上述「下一步」已由後續兩階段決策取代；97 題詳解延後至第二階段處理。

## 2026-07-29 兩階段交付決策

- 決策：第一階段先完成目前可確認的 715 題全部匯入及官方答案核對；第二階段
  才處理全部詳解初稿與獨立複核。
- 當時階段：第一階段，進度 100／715，尚餘 615 題（最新數字見本文件開頭）。
- 第一階段限制：新題預設 `explanationStatus: "missing"`；不得批次產生模板詳解。
- 現有詳解：保留人工智慧基礎概論第 2～4 題共 3 題初稿，第一階段不繼續擴充。
- 下一批：115 年第一次初級兩科，共 100 題。
- 後續順序：115 年第二次初級 100 題、114 年第二次中級 150 題、
  115 年第一次中級 150 題、114 年 9 月官方樣題 115 題。
- 第一階段完成門檻：715 題全部匯入、答案核對、來源追溯與測試通過，且清冊、
  manifest、交接文件數字一致。
- 第二階段完成門檻：715 題全部具有合格 A～D 詳解初稿，並全部完成獨立複核。
- 詳細執行方式：[題庫建置兩階段執行計畫](DELIVERY_PHASES.md)。

## 2026-07-29 115 年第一次初級交接

- 處理範圍：115 年第一次初級第一科、第二科，共 100 題。
- 官方來源：
  - [第一科　人工智慧基礎概論公告試題](https://www.ipas.org.tw/api/proxy/uploads/certification_resource/bf93f438f7be48d295c1b40a34d79f3d/115年第一次初級AI應用規劃師_第一科_人工智慧基礎概論_公告試題_20260410164304.pdf)（12 頁）
  - [第二科　生成式 AI 應用與規劃公告試題](https://www.ipas.org.tw/api/proxy/uploads/certification_resource/bf93f438f7be48d295c1b40a34d79f3d/115年第一次初級AI應用規劃師_第二科_生成式AI應用與規劃_公告試題_20260410164328.pdf)（11 頁）
- 匯入方式：原為 `scripts/import-115-elementary-first.py`（已於下一批改寫為
  可帶批次參數的 `scripts/import-elementary-official.py`）；以 pypdf 擷取文字，
  另以 pypdfium2 將 23 頁全部轉圖，逐頁目視核對題號、題幹、A～D 選項、官方
  答案與來源頁碼。腳本只取代這兩個 `sourceId`，不影響既有題目。
- 新增題目：`aiap-elementary-115-01-ai-foundation-001` 至 `050`，以及
  `aiap-elementary-115-01-genai-planning-001` 至 `050`。
- 已核對題目：100 題；`extractionStatus` 均為 `verified`。
- 詳解初稿：0 題。依第一階段規則，`explanationStatus` 全部為 `missing`，
  詳解欄位保持空白，未產生任何模板內容。
- 已複核詳解：0 題。
- 官方答案序列（供覆核）：
  - 第一科：`DDDCBCCDAABBABACABABDCBDACCCBAACDCCABBDABDDACCDCDB`
  - 第二科：`ADADCDADBDBBBADDBACCDDADACACCBCAAABCCCDBABBBDCACBC`
- 文字整理：本批修正 PDF 斷行造成的多餘空白，並還原被字距拆開的 `VAE`、
  `Volume`。114 年第四次批次尚有同類空白殘留，未在本次變更範圍內處理。
- 來源清冊更新：兩科各為匯入 50、答案核對 50，詳解初稿與複核均為 0；
  總進度 200／715。
- 執行測試：`npm test`（manifest 一致性檢查與 8 項資料測試）、`npm run lint`、
  `npm run build`。
- 未解問題：無；兩份 PDF 皆為純文字版，沒有圖片題、跨頁表格或勘誤。
- 下一步：匯入 115 年第二次初級兩科共 100 題（`past-11.pdf`、`past-12.pdf`），
  仍不撰寫詳解。

## 2026-07-29 115 年第二次初級交接

- 處理範圍：115 年第二次初級第一科、第二科，共 100 題。
- 官方來源：
  - [第一科　人工智慧基礎概論公告試題](https://www.ipas.org.tw/api/proxy/uploads/certification_resource/bf93f438f7be48d295c1b40a34d79f3d/115年第二次初級AI應用規劃師_第一科_人工智慧基礎概論_公告試題_20260604212644.pdf)（13 頁）
  - [第二科　生成式 AI 應用與規劃公告試題](https://www.ipas.org.tw/api/proxy/uploads/certification_resource/bf93f438f7be48d295c1b40a34d79f3d/115年第二次初級AI應用規劃師_第二科_生成式AI應用與規劃_公告試題_20260604212719.pdf)（13 頁）
- 匯入方式：把上一批的專用腳本改寫為 `scripts/import-elementary-official.py`，
  以批次參數執行（`python scripts/import-elementary-official.py 115-2`）；
  重跑 `115-1` 產生的資料與改寫前逐位元組相同，確認重構未改動既有題目。
  另以 pypdfium2 將 26 頁全部轉圖，逐頁目視核對題號、題幹、A～D 選項、
  官方答案與來源頁碼。
- 新增題目：`aiap-elementary-115-02-ai-foundation-001` 至 `050`，以及
  `aiap-elementary-115-02-genai-planning-001` 至 `050`。
- 已核對題目：100 題；`extractionStatus` 均為 `verified`。
- 詳解初稿：0 題；`explanationStatus` 全部為 `missing`，未產生任何模板內容。
- 已複核詳解：0 題。
- 官方答案序列（供覆核）：
  - 第一科：`ADABCCAADACBDBDDDBABCDAAABADCBDDBCAADCCCCCBCBCBBDB`
  - 第二科：`BABCDBBCACBADBBAADCDDCCCDDBDBAACCBAAADBDADBACCCBBD`
- 文字整理：第一科第 10 題選項的 `Volume` 在官方文字層被字距拆成
  「V olume」且與後方中文之間沒有空白，已還原為「Volume 與 …」。
- 來源清冊更新：兩科各為匯入 50、答案核對 50；初級歷屆考題 6 科全部完成，
  總進度 300／715。
- 執行測試：`npm test`（manifest 一致性檢查與 8 項資料測試）、`npm run lint`、
  `npm run build`。
- 未解問題：無；兩份 PDF 皆為純文字版，沒有圖片題、跨頁表格或勘誤。
- 下一步：匯入 114 年第二次中級三科共 150 題（`past-01.pdf`～`past-03.pdf`）。
  中級試卷版面與初級不同（頁首與題型標題有差異），沿用
  `import-elementary-official.py` 前需先確認 `clean_page` 的頁首規則。

## 2026-07-29 114 年第二次中級第一科交接

- 處理範圍：114 年第二次中級第一科「人工智慧技術應用與規劃」，共 50 題。
- 官方來源：[第一科公告試題](https://www.ipas.org.tw/api/proxy/uploads/certification_resource/bf93f438f7be48d295c1b40a34d79f3d/114年第二梯次中級AI應用規劃師第一科人工智慧技術應用與規劃(當次試題公告114_20251226000616.pdf)（14 頁）。
- 匯入方式：腳本改名為 `scripts/import-official-exam.py`，改為同時支援初級與
  中級（頁首改用正規表示式、支援「答／案」被拆成兩行的欄位標題、批次帶入
  級別）。重跑 `115-1`、`115-2` 產生的資料與改寫前逐位元組相同。
  執行 `python scripts/import-official-exam.py 114-2-intermediate`。
- 新增題目：`aiap-intermediate-114-02-ai-tech-planning-001` 至 `050`。
- 已核對題目：50 題；14 頁全部渲染後逐頁目視核對，`extractionStatus` 均為
  `verified`。全卷無圖片題、無共用題組敘述。
- 詳解初稿：0 題；`explanationStatus` 全部為 `missing`。
- 官方答案序列（供覆核）：
  `BABCABACBDCBBACDDDBBBDADBDCCBABDCDABBBCAADBCDACBAC`
- 未匯入：同梯次第二科與第三科各 50 題。原因是這兩科共有 17 題的題幹、選項或
  題組敘述以圖片呈現（第二科第 3、40、41、42、47、49、50 題；第三科第 38～41、
  45～50 題），另有 5 組共用題組敘述。只匯入文字會產生無法作答的殘缺題目，
  因此依專案負責人決定，先為題目資料與網站加入附圖支援後再匯入。
- 已完成的前置作業：38 張圖片已從官方 PDF 擷取並確認位置（頁碼與座標），
  題組敘述的起始行可用「兩個半形空白開頭」的版面規則辨識。
- 執行測試：`npm test`（manifest 一致性檢查與 8 項資料測試）、`npm run lint`、
  `npm run build`。
- 下一步：加入題目附圖與題組敘述的資料格式與前端顯示，再匯入第二、三科
  共 100 題。

## 2026-07-29 114 年第二次中級第二、三科交接（含附圖支援）

- 處理範圍：114 年第二次中級第二科「大數據處理分析與應用」、第三科「機器學習
  技術與應用」，共 100 題；本梯次三科全數完成。
- 官方來源：
  - [第二科公告試題](https://www.ipas.org.tw/api/proxy/uploads/certification_resource/bf93f438f7be48d295c1b40a34d79f3d/114年第二梯次中級AI應用規劃師第二科大數據處理分析與應用(當次試題公告114_20251226000634.pdf)（17 頁）
  - [第三科公告試題](https://www.ipas.org.tw/api/proxy/uploads/certification_resource/bf93f438f7be48d295c1b40a34d79f3d/114年第二梯次中級AI應用規劃師第三科機器學習技術與應用(當次試題公告114_20251226000650.pdf)（19 頁）
- 資料格式變更：`Question` 新增 `figures`（題幹附圖）、`options[].figures`
  （選項附圖）與 `passage`（共用題組敘述，由 text／pre／figure 區塊組成）。
  規格已寫入 `docs/QUESTION_DATA_SPEC.md`。
- 圖片處理：以 pypdfium2 從官方 PDF 擷取 38 張內嵌圖片，存入
  `public/images/questions/`，檔名保留來源試卷與頁碼。圖片與題號、欄位的
  對應表在 `scripts/figures-114-2-intermediate.json`，每一筆都對照渲染頁確認。
- 解析器新增：題組敘述以「行首兩個半形空白」辨識並自動解析「X~Y 題」範圍；
  選項排在同一行時改用不限行首的比對；題幹或選項可以只有圖片而無文字。
- 新增題目：`aiap-intermediate-114-02-big-data-001` 至 `050`，
  `aiap-intermediate-114-02-machine-learning-001` 至 `050`。
- 已核對題目：100 題；36 頁全部渲染後逐頁目視核對，`extractionStatus` 均為
  `verified`。
- 詳解初稿：0 題；`explanationStatus` 全部為 `missing`。
- 官方答案序列（供覆核）：
  - 第二科：`DBABBCCBCCCADDCABACDBDCAACDADCBADBBBCBDBACBDACBDCB`
  - 第三科：`BCCBACADACDCBCBABACCCBACADDCDCBDBDADBBCCDBADBBBCCC`
- 已知限制：題幹與選項的附圖一律排在該段文字之後；題組敘述內的圖片依頁面
  順序插入。少數情況下圖片在官方版面是排在文字之前，顯示順序會略有差異，
  內容則完整。
- 來源清冊更新：兩科各為匯入 50、答案核對 50；總進度 450／715。
- 執行測試：`npm test`（manifest 一致性檢查與 9 項資料測試，新增附圖與題組
  完整性測試）、`npm run lint`、`npm run build`。
- 下一步：匯入 115 年第一次中級三科共 150 題（`past-06.pdf`～`past-08.pdf`）。
  該梯次題型標題為「一、單選題」，且同樣可能含圖片題與題組敘述，可沿用
  `scripts/import-official-exam.py` 與本次的附圖對應流程。
