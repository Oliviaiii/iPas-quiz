# 未通過驗收的白話化 payload

這裡的檔案**不得套用**。`scripts/check-plain-language.py` 與
`scripts/apply-plain-language.py` 只掃 `content/plain-language/*.json`，
不會遞迴進本目錄，所以放在這裡就不會被誤用。

保留而非刪除，是因為內容仍有可救的部分，重做時可以參考。

## aiap-115-intermediate-1-machine-learning-026-050.json

退回原因：系統性把英文術語翻成中文而未並存，名詞保留檢查列出 20 項以上，
其中兩項是**真正的內容遺失**，不只是用語問題：

- Q42C 掉了 `nn.Linear(2048, 2)` 的 `2048,2`——那是官方附圖裡的實際參數
- Q41A 掉了「50」

其餘為 MSE／Sigmoid／Softmax／cross-entropy／ResNet／fine-tuning 等術語被
換成中文而沒有保留原文。規則要的是「名詞（English）＋白話」並存，不是二選一。

重做時整份重跑即可，payload 會依題庫現況重新產生 sha256。
