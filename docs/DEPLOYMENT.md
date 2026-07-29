# GitHub Pages 與 Cloudflare Web Analytics

最後更新：2026-07-29

## 目前環境

- GitHub repository：https://github.com/Oliviaiii/iPas-quiz
- GitHub Pages：https://oliviaiii.github.io/iPas-quiz/
- Pages 來源：GitHub Actions
- Cloudflare Web Analytics 網站：`oliviaiii.github.io`
- 專案路徑：`/iPas-quiz/`

## 1. 部署方式

本專案使用 Next.js 靜態輸出：

- `next.config.ts` 設定 `output: "export"`。
- GitHub Actions 環境自動使用 repository 名稱作為 `basePath`。
- `.github/workflows/deploy-pages.yml` 在 `main` 更新後執行驗證、建置與 Pages 部署。
- 部署產物是 `out/`，不需要獨立應用程式伺服器。

## 2. GitHub Pages workflow

workflow 順序：

1. Checkout。
2. 安裝 Node.js 24。
3. 設定 GitHub Pages。
4. `npm ci`。
5. `npm test`。
6. `npm run lint`。
7. `npm run build`。
8. 上傳 `out/` 並部署。

如果其中任何一步失敗，不應部署舊或不完整的產物。

## 3. Cloudflare Web Analytics

本專案沿用 Cloudflare 中既有的 `oliviaiii.github.io` Web Analytics 網站，因為
GitHub Pages 專案網址仍屬於同一個 hostname。

Analytics token 不寫入 repository：

1. 在 GitHub repository 的 Variables 建立
   `CLOUDFLARE_WEB_ANALYTICS_TOKEN`。
2. workflow 將它傳給
   `NEXT_PUBLIC_CLOUDFLARE_WEB_ANALYTICS_TOKEN`。
3. `app/layout.tsx` 只有在 token 存在時才插入
   `https://static.cloudflareinsights.com/beacon.min.js`。

token 雖然會出現在公開網站的追蹤碼中，但仍由部署設定管理，避免在原始碼中
硬編碼，也方便未來更換。

## 4. 在哪裡看瀏覽數據

Cloudflare Dashboard 路徑：

```text
分析 → Web Analytics → oliviaiii.github.io
```

若要只看本專案，新增篩選條件：

```text
路徑包含 /iPas-quiz/
```

可查看：

- 造訪次數。
- 點閱率／頁面瀏覽。
- 來源網站。
- 國家與瀏覽器。
- Core Web Vitals。

新部署後不會立即產生歷史數據；需要有人實際開啟頁面，Cloudflare 收到 beacon
後才會出現。

## 5. 部署後必要驗證

不能只看 GitHub Actions 綠燈，還要確認：

- 正式網址回傳成功。
- CSS 與 JavaScript 資產使用正確的 `/iPas-quiz/` 路徑。
- 初級／中級切換與作答功能可用。
- 頁面 HTML 含 Cloudflare `beacon.min.js`。
- HTML 的 `data-cf-beacon` 存在。
- `public/data/manifest.json` 可由正式網址取得。

回報時不得公開完整 Analytics token。
