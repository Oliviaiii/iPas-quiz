# 專案交接清單

## 目前進度（2026-07-31）

- **第一階段（全部題目匯入）已完成：600／600。已進入第二階段 A：詳解初稿。**
- 114～115 年初級 8 個場次、中級 4 個場次已建立逐科追蹤。
- 官方目前發布的 12 份歷屆試卷共 600 題**已全部匯入並核對**：初級 6 科 300 題
  （114 年第四次、115 年第一次、115 年第二次），中級 6 科 300 題
  （114 年第二次、115 年第一次）。與官方學習資源頁列出的檔案一份不差。
- 114 年 9 月版官方樣題 115 題與 114 年 1 月舊版樣題 25 題**已遭官方下架**
  （2026-07-31 複查），改列 `not-found`／維持 `superseded`，均不計入目標。
  盤點基準因此由 715 調整為 600。
- 詳解進度：13 題有合格 A～D 初稿（`draft`），587 題為 `missing`，
  0 題完成人工複核。已完成批次為 114 年第四次初級第一科第 2～4、5～14 題。
- 第二階段 A（逐批撰寫初稿）進行中；第二階段 B（獨立複核）待初稿全部完成
  後才開始，且複核者應與撰寫者不同。
- 題目資料已支援官方附圖與共用題組敘述；目前共 72 張官方附圖、12 組共用
  題組敘述。
- 官方 PDF 不進版控，每次匯入需先放行 `www.ipas.org.tw` 與 `ipd.nat.gov.tw`
  的連外權限，再執行 `scripts/fetch-official-pdfs.py`。
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

上述 715 題基準已於 2026-07-31 因官方下架樣題而調整為 600 題；兩階段的執行方式不變。

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

## 2026-07-30 115 年第一次中級三科交接

- 處理範圍：115 年第一次中級第一科「人工智慧技術應用與規劃」、第二科「大數據
  處理分析與應用」、第三科「機器學習技術與應用」，共 150 題；官方 12 份歷屆
  試卷 600 題至此全部匯入完畢。
- 官方來源（皆為 15/17/18 頁，考試日期 115 年 05 月 23 日）：
  - [第一科公告試題](https://www.ipas.org.tw/api/proxy/uploads/certification_resource/bf93f438f7be48d295c1b40a34d79f3d/115年第一次中級AI應用規劃師_第一科_人工智慧技術應用與規劃_公告試題_20260615003359.pdf)（15 頁）
  - [第二科公告試題](https://www.ipas.org.tw/api/proxy/uploads/certification_resource/bf93f438f7be48d295c1b40a34d79f3d/115年第一次中級AI應用規劃師_第二科_大數據處理分析與應用_公告試題_20260615003417.pdf)（17 頁）
  - [第三科公告試題](https://www.ipas.org.tw/api/proxy/uploads/certification_resource/bf93f438f7be48d295c1b40a34d79f3d/115年第一次中級AI應用規劃師_第三科_機器學習技術與應用_公告試題_20260615003428.pdf)（18 頁）
- 取得 PDF 的前置條件：執行環境預設的 Trusted 連外等級不含
  `www.ipas.org.tw` 與 `ipd.nat.gov.tw`，會在 CONNECT 階段被回 403。本次由專案
  負責人把環境連外改為 Custom 並加入這兩個網域後才取得官方 PDF。
- 匯入方式：`python scripts/fetch-official-pdfs.py 115-1-intermediate` 下載，
  再 `python scripts/import-official-exam.py 115-1-intermediate`。
- 新增題目：`aiap-intermediate-115-01-ai-tech-planning-001` 至 `050`、
  `aiap-intermediate-115-01-big-data-001` 至 `050`、
  `aiap-intermediate-115-01-machine-learning-001` 至 `050`。
- 已核對題目：150 題，`extractionStatus` 均為 `verified`。核對方式：
  1. 50 頁全部渲染；含圖片、題組或自動檢查有疑慮的 23 頁逐頁目視核對。
  2. 官方答案以 pdfplumber 依表格座標獨立讀取最左欄字母，與匯入結果逐題比對，
     150/150 完全一致（此路徑不與匯入用的正規表示式共用程式碼）。
  3. 題幹與選項共 746 個欄位，改以 pdfplumber 裁掉答案欄與題號欄後重新擷取比對；
     4 筆不符全部個別檢視確認為參考端裁切與下標排版造成，資料本身無誤。
  4. 三份 PDF 內嵌圖片以程式全數列舉（每頁重複的 1084×454 iPAS 浮水印已確認為
     標誌並排除），因此不會漏圖。
- 詳解初稿：0 題；`explanationStatus` 全部為 `missing`，未產生任何模板內容。
- 已複核詳解：0 題。
- 官方答案序列（供覆核）：
  - 第一科：`DCBCCCCBDABBCABADDAABCBDBDABCCABDBBAADADADCBBCDCAD`
  - 第二科：`AABAADBDBBCCBCCADDDBDCCCCADCDBBBACDDABCABDCACACCBD`
  - 第三科：`CCACCBBBAADACCDABADCDCDDADCBBBADBDDBACABBCDBABBDCB`
- 圖片：34 張（第一科 1、第二科 14、第三科 19），對照表為
  `scripts/figures-115-1-intermediate.json`。第二科第 49 題的 A～D 選項本身即為
  程式碼截圖；第二科第 48～50 題與第三科第 42～43、44～45、46～48 題的題組敘述
  含附圖。共用題組共 7 組：第二科 41～44、45～47、48～50，第三科 42～43、
  44～45、46～48、49～50。
- 解析器修正（三項，皆為本梯次版面差異所暴露的既有缺陷）：
  1. `clean_page` 原本只移除「一、選擇題」。本梯次第二科第 12 頁、第三科第 11 頁
     另有「二、程式題」章節標題，會被併進前一題最後一個選項的文字。改為以
     `SECTION_HEADING` 正規表示式移除任何「N、XX題」標題。
  2. 第三科程式題章節（第 11～18 頁）的兩欄標題印成「題目 答案」，與其他試卷
     相反，原本的字串比對漏掉。改為兩種順序都移除。
  3. 題目起始樣式的 `^\s*` 會把前一頁結尾的換行一起吃掉，使跨頁第一題的
     `sourcePage` 少算一頁。改為 `^[ \t　]*` 只允許同一行的空白。此修正同時
     更正既有資料一筆：`aiap-intermediate-114-02-big-data-043` 的 `sourcePage`
     由 13 改為 14（該題實際印在第 14 頁）。六份中級試卷的 `sourcePage` 現已
     全數與逐頁掃描結果一致。
- 迴歸驗證：重跑 `114-2-intermediate` 後，除上述 Q43 頁碼修正外，既有 450 題
  逐位元組相同（449/450 完全未變，1 筆為刻意更正）。
- 網站驗證：`npm run build` 靜態輸出後以 Chromium（桌面 1280×900、手機 390×844）
  實際操作，切到中級→第二科→第 49 題，4 張選項截圖與題組附圖共 5 張圖片全部
  正常載入，無 broken image、無 console error。首頁說明文字已同步加入
  115 年第一次中級。
- 來源清冊更新：三科各為匯入 50、答案核對 50，詳解初稿與複核均為 0；
  總進度 600／715。三科 `retrievedAt` 記為 2026-07-30（實際取得 PDF 之日）；
  盤點截止日仍為 2026-07-29，因為本次未新增匯入目標。
- 自動測試更新：`tests/data.test.mjs` 新增三份試卷的題號、答案序列與頁數上限，
  圖片總數 38 → 72，manifest 期望值改為 600 題，並放寬 `retrievedAt` 允許
  2026-07-30。
- 執行測試：`npm test`（manifest 一致性檢查與 9 項資料測試，全部通過）、
  `npm run lint`、`npm run build`，以及上述瀏覽器操作。
- 已知限制（沿用上一批）：題幹與選項的附圖一律排在該段文字之後；官方版面中
  少數圖片排在文字之前或文字中間（如第二科第 43 題），顯示順序會略有差異，
  內容則完整。題幹內的編號清單（如第二科第 49 題的 1./2./3.）在正規化時會併成
  同一段，內容不缺但版面不保留。
- 未解問題：無。
- 下一步：匯入 114 年 9 月最新版官方樣題五科共 115 題（初級兩科 35+35、中級三科
  15+15+15），即第一階段最後一批。樣題與歷屆考題來源不同（`official-sample`、
  `DownloadFile.ashx` 網址、同一 PDF 內含多科），需在 `scripts/import-official-exam.py`
  另建批次規則，且不得與 114 年 1 月舊版樣題重複匯入。

## 2026-07-31 官方樣題下架複查與第一階段完成

- 處理範圍：原定匯入 114 年 9 月版官方樣題五科共 115 題（第一階段最後一批）。
  複查後確認官方已將樣題全數下架，無法匯入；改為完成盤點基準調整與階段結算。
- 新增題目：0 題。已核對題目：0 題。詳解初稿：0 題。已複核詳解：0 題。
  `questions.json` 未變動。
- 複查證據（2026-07-31）：
  - 官方學習資源頁目前只有兩個檔案區塊：「初級能力鑑定試題公告」6 份、
    「中級能力鑑定試題公告」6 份，**沒有考試樣題區塊**。頁面上「考試樣題」
    四字只出現在 title／description／og／JSON-LD 等靜態 metadata。
  - 清冊記錄的 9 月版樣題下載網址（初級、中級各一）與 1 月版網址，皆回傳
    官方「找不到頁面」404。
  - 檔案下載頁與考試資訊頁均無樣題 PDF；官方最新消息 0 次提及樣題。
  - 官方新增的「AI 應用規劃師能力鑑定_評鑑內容範圍參考」（115.06 更新）已下載
    檢視：4 頁考科範圍對照表，0 題、0 個選項，不能替代樣題。
  - 官方頁列出的 12 份試卷與本站已匯入的 12 份完全一致。
- 未採取的做法：不以第三方流傳的樣題檔案或記憶生成題目替代官方文件。
- 基準調整（經專案負責人決定）：五科 9 月版樣題 `availability` 由 `published`
  改為 `not-found`、`expectedCount` 設為 `null`（與其他 `not-found` 來源一致），
  但維持 `inclusion: target` 並在 `notes` 保留盤點時的題數（35/35/15/15/15），
  官方若重新發布可直接回補。`knownQuestionTarget` 因此由 715 變為 600。
  盤點截止日更新為 2026-07-31。
- 階段結算：`knownQuestionTarget` = `importedCount` = `answerVerifiedCount`
  = 600，**第一階段完成**。第二階段（600 題詳解初稿與獨立複核）尚未開始，
  依負責人指示須待明確指令後才動工，本次未寫任何詳解。
- 文件更新：`SOURCE_INVENTORY.md`（工作階段、進度摘要、樣題表、下架複查紀錄、
  `not-found` 定義擴充為含「曾發布後被下架」）、`DELIVERY_PHASES.md`（基準
  715→600 及調整理由、匯入順序表、第一、二階段完成條件）、本文件開頭進度區塊。
- 自動測試更新：`tests/data.test.mjs` 的 availability 計數改為 published 12／
  not-found 14，manifest 期望值改為 `knownQuestionTarget` 600、
  `currentSampleQuestionTarget` 0、`inventoryCutoff` 2026-07-31，並新增一項
  斷言鎖住「目標＝已匯入＝答案已核對」的第一階段完成條件。
- 執行測試：`npm test`（9 項全過）、`npm run lint`、`npm run build`。
- 未解問題：官方是否會重新發布樣題未知。建議每次接手時順手複查官方三個入口；
  若樣題回歸，先更新盤點截止日與目標數，再依既有流程匯入。
- 下一步：等待專案負責人指示是否開始第二階段。若開始，依
  `DELIVERY_PHASES.md` 第 4 節，從同一科連續 10～25 題為一批撰寫 A～D 逐項
  解析，每批完成後同步更新清冊與本文件；初稿全部完成後才進行獨立複核。

## 2026-07-31 第二階段開始：114 年第四次初級第一科第 5～14 題詳解初稿

- 處理範圍：114 年第四次初級第一科「人工智慧基礎概論」第 5～14 題，共 10 題
  詳解初稿。這是第二階段 A 的第一批。
- 階段切換：專案負責人於 2026-07-31 指示第一階段完成後開始撰寫詳解，
  `DELIVERY_PHASES.md` 與 `SOURCE_INVENTORY.md` 已記錄切換。
- 新增題目：0 題。題幹、選項與官方答案完全未變動，本批只填寫 `explanation`。
- 詳解初稿：10 題（累計 13 題）。每題均含一句話答案、核心觀念、正解理由、
  A～D 四項獨立解析、常見陷阱與可追溯的參考資料，狀態一律為 `draft`。
- 已複核詳解：0 題。本批由 AI 輔助撰寫，依 `QUESTION_AUTHORING_GUIDE.md`
  第 7 節，未經人工查證前不得標記為 `reviewed`。
- 撰寫依據與查證方式：
  - 官方公告試題 PDF：核對每題題號、選項與官方答案。
  - iPAS 初級學習指引科目一（官方 PDF，71 頁）：第 5～14 題中，第 7、8、
    11、12、13、14 題的核心定義直接取自指引，並在參考資料標明章節頁碼
    （如 3-8 散佈圖、3-10 預測性分析、3-13 學習類型、3-17 生成式 AI）。
  - 第 9 題（人工智慧基本法）：查行政院新聞稿確認草案第 5 條「創新實驗環境」
    文字，並以歐盟 AI Act 第 57 條的 AI 監理沙盒作為對應制度依據。
  - 第 10 題（金融機構運用人工智慧技術作業規範）：查銀行公會規範頁與學習
    指引參考書目確認發布單位與版本。
  - 第 5、6、7 題另引 scikit-learn 官方文件說明欠擬合／過度擬合、Lasso 的
    稀疏解與單純貝氏。
  - 所有參考連結皆於 2026-07-31 實際開啟確認可讀取，`checkedAt` 記錄該日期。
- 已知待查項目（已寫入該題 `editorialNote`）：
  - 第 9 題：題幹寫「2025 年 9 月行政院通過」，但行政院新聞稿日期為
    2025 年 8 月 28 日；本站保留官方題目原文不改。另《人工智慧基本法》已於
    2025 年 12 月 23 日三讀通過，現行狀態已非草案，本題仍依考試當時作答。
  - 第 10 題：撰寫時銀行公會的規範全文下載連結回傳空檔案，條文內容依規範
    公開說明與學習指引參考書目整理，尚未逐條比對全文。複核者須自銀行公會
    規範頁開啟 PDF 確認四個選項對應條文的實際用語。
- 腳本：新增 `scripts/write-explanations-114-4-s1-005-014.py`。腳本會在寫入前
  比對官方答案是否與初稿撰寫時一致、拒絕覆蓋已標記 `reviewed` 的題目、
  並檢查 A～D 四項解析齊備與摘要是否敘明官方答案，重跑安全。
- 來源清冊更新：`aiap-114-elementary-4-ai-foundation` 的
  `explanationDraftCount` 由 3 改為 13。
- 自動測試更新：原「keeps explanations out of phase one imports」改寫為
  「keeps explanation drafts complete and free of filler」，改以 `draftIds`
  清單比對，並新增檢查：draft 題目必須有完整 A～D 解析（反向亦成立）、
  摘要須以「正確答案是 X」開頭且與官方答案一致、核心觀念／正解理由／陷阱
  長度下限、每筆參考資料須有標題、定位與 ISO 日期且網址為 https、
  尚未複核者不得有 `reviewer` 欄位。
- 執行測試：`npm test`（9 項全過）、`npm run lint`、`npm run build`，
  並以 Chromium 實際操作靜態輸出：第 5 題作答前不顯示詳解，作答後正確顯示
  「詳解初稿」標記、一句話答案、核心觀念、選項分析、常見陷阱與參考資料，
  無 console error。
- 未解問題：見上述第 9、10 題待查項目。
- 下一步：續寫同科第 15～24 題。撰寫前建議先讀 `QUESTION_AUTHORING_GUIDE.md`
  第 3、4 節，並沿用本批作法：能對應官方學習指引的先引指引並標明章節頁碼，
  法規題以主管機關原始公告為準，且每個引用連結都要實際開啟確認。
