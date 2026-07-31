import { defineConfig, globalIgnores } from "eslint/config";
import nextVitals from "eslint-config-next/core-web-vitals";
import nextTypescript from "eslint-config-next/typescript";

export default defineConfig([
  ...nextVitals,
  ...nextTypescript,
  // `.claude/**` 涵蓋 worktree 目錄，`**/.next/**` 涵蓋其中的建置快取；
  // 兩者都是產生檔，被掃到時會產生數千筆與專案原始碼無關的錯誤。
  globalIgnores([
    ".next/**",
    "**/.next/**",
    "out/**",
    ".claude/**",
    "next-env.d.ts",
  ]),
]);
