# iPAS AI 應用規劃師刷題工具

本專案預計製作一套可在瀏覽器使用的簡易刷題工具，範圍只包含經濟部
iPAS「AI 應用規劃師」初級與中級。

- 線上網站：https://oliviaiii.github.io/iPas-quiz/
- GitHub：https://github.com/Oliviaiii/iPas-quiz

目前已完成可部署的第一版基礎架構及 114～115 年初級／中級場次盤點，但尚未
開始匯入官方題目。盤點截止 2026-07-29，可確認的匯入目標為 600 題歷屆考題
及 115 題最新版官方樣題，共 715 題。

網站現在提供 4 題明確標示為「非官方」的介面示範題，用來驗證：

- 初級／中級及科目篩選。
- 點選選項後鎖定答案。
- 答對／答錯提示與 A～D 選項詳解。
- 錯題篩選與瀏覽器本機進度。
- 手機與桌面響應式版面。

正式題目匯入後，示範題仍須與官方題庫分開計算。

## 專案文件

- [專案規劃](docs/PROJECT_PLAN.md)：產品範圍、階段、交付項目與完成定義。
- [題目與詳解撰寫規則](docs/QUESTION_AUTHORING_GUIDE.md)：逐題整理、撰寫及複核方式。
- [資料來源與收錄規則](docs/SOURCE_AND_COVERAGE_RULES.md)：哪些資料可以收錄，以及如何證明沒有漏題。
- [題源與匯入進度](docs/SOURCE_INVENTORY.md)：初級、中級所有場次、官方文件及逐階段數字。
- [資料格式與狀態規則](docs/QUESTION_DATA_SPEC.md)：題目 ID、必要欄位與審查狀態。
- [交接清單](docs/HANDOVER.md)：每次工作結束前應留下的紀錄。
- [部署與流量分析](docs/DEPLOYMENT.md)：GitHub Pages 與 Cloudflare Web Analytics 設定。

## 核心原則

1. 官方來源優先，第三方網站只能協助發現資料或交叉檢查。
2. 「題目已收錄」、「答案已核對」與「詳解已複核」是三種不同狀態。
3. 不把自行撰寫的解析稱為官方詳解。
4. 不整批複製第三方網站、補習班或出版品的解析。
5. 每一題都必須能追溯到原始來源文件及頁碼。
6. 題庫完整度必須由來源清冊和自動檢查證明，不能只靠人工印象。

## 本機開發

```powershell
npm.cmd install
npm.cmd run dev
```

驗證：

```powershell
npm.cmd test
npm.cmd run lint
npm.cmd run build
```

靜態輸出位於 `out/`。GitHub Pages 部署由
`.github/workflows/deploy-pages.yml` 自動執行。
