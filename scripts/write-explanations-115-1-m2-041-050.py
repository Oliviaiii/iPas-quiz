"""Write draft explanations for 115-1 intermediate subject two, Q41-Q50.

The script verifies official answers, refuses to overwrite reviewed work, and
keeps every generated explanation in ``draft`` for independent review.

Usage::

    python scripts/write-explanations-115-1-m2-041-050.py
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUESTIONS = ROOT / "app" / "data" / "questions.json"
SOURCE_ID = "aiap-115-intermediate-1-big-data"
AUTHOR = "Codex（AI 輔助初稿）"
AUTHORED_AT = "2026-08-13"
CHECKED_AT = "2026-08-13"

EXAM_PDF = (
    "https://www.ipas.org.tw/api/proxy/uploads/certification_resource/"
    "bf93f438f7be48d295c1b40a34d79f3d/115年第一次中級AI應用規劃師_"
    "第二科_大數據處理分析與應用_公告試題_20260615003417.pdf"
)
DEFAULT_NOTE = "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。"


def exam_ref(number: int, locator: str | None = None) -> dict:
    return {
        "title": "115 年第一次中級 AI 應用規劃師－大數據處理分析與應用公告試題",
        "url": EXAM_PDF,
        "locator": locator or f"第 {number} 題題幹、選項與官方答案",
        "checkedAt": CHECKED_AT,
    }


def ref(title: str, url: str, locator: str) -> dict:
    return {"title": title, "url": url, "locator": locator, "checkedAt": CHECKED_AT}


EXPECTED_ANSWER = {
    41: "B", 42: "D", 43: "C", 44: "A", 45: "C",
    46: "A", 47: "C", 48: "C", 49: "B", 50: "D",
}

DRAFTS: dict[int, dict] = {}

DRAFTS[41] = {
    "summary": "正確答案是 B。附圖的 describe() 顯示平均數 223.41 遠高於中位數 128.55，且最大值達 4500，分布明顯右偏；以中位數補值較不受極端高收入牽動。",
    "concept": (
        "已目視核對附圖程式：它讀入 driver_daily_stats.csv，並從 daily_earnings.describe()"
        "取出 mean、50% 與 max。平均數會被少數極端大值拉高，中位數則只由排序後的中央位置"
        "決定，因此在右偏且含離群值的收入資料中較具穩健性。單一常數補值仍會縮小變異、改變"
        "相關性；正式模型應再檢查缺失機制、加入缺失指標，並只以訓練集估計補值統計量。"
    ),
    "answerReason": (
        "題目給定 mean 約 223、median 約 129、max 4500，顯示高值把平均拉離典型收入。缺失僅約"
        "5% 且目標是盡量降低補值偏差時，B 用中位數代表典型位置，比平均或最大值更不受右尾影響；"
        "直接刪除也不是數值欄位的必然規則。"
    ),
    "optionAnalysis": {
        "A": "平均數會受 4500 等極端高收入牽動；以約 223 補入每個缺值，會把缺失列系統性推向高於典型值的位置，對右偏分布通常不如中位數穩健。",
        "B": "正確。中位數約 128.55，對右尾極端值不敏感；在四個選項中，它較能代表多數司機的典型日收入並降低常數補值受離群值造成的偏移。",
        "C": "最大值 4500 位於分布極端端點，把所有缺值補成最大收入會人為製造大量極端觀測，嚴重扭曲平均、變異與線性迴歸係數。",
        "D": "數值欄位可以使用中位數、模型式補值等方法；刪除列只有在缺失近似隨機且樣本損失可接受時才可能合理，不能因欄位為數值就一律刪除。",
    },
    "trap": "50% 就是中位數。看到 mean 明顯大於 50% 且 max 極大，要先想到右偏與離群值；但中位數補值只是本題四選一的較佳方案，不代表完全保留原分布。",
    "editorialNote": (
        "本站已於 2026-08-13 目視核對 Q41 附圖，程式為 `pd.read_csv` 後執行"
        " `df['daily_earnings'].describe()[['mean', '50%', 'max']]`。官方答案 B 的統計理由成立；"
        "但四個程式選項中的 `df[col].fillna(..., inplace=True)` 屬 chained inplace assignment，"
        "pandas 2.2 已提出 FutureWarning。較穩妥寫法是指定回欄位，或對 DataFrame 呼叫 fillna。"
    ),
    "references": [
        exam_ref(41, "第 41 題題組敘述、附圖程式、統計輸出、選項與官方答案"),
        ref("pandas.Series.median 官方文件", "https://pandas.pydata.org/docs/reference/api/pandas.Series.median.html", "Series.median 計算中位數並預設排除缺失值"),
        ref("pandas 2.2.0 What's new", "https://pandas.pydata.org/pandas-docs/version/2.2.3/whatsnew/v2.2.0.html", "Chained assignment 與 df[col].fillna(..., inplace=True) 的棄用說明及替代寫法"),
    ],
}

DRAFTS[42] = {
    "summary": "正確答案是 D。隨機森林迴歸以多棵決策樹的非線性切分預測收入，不會像線性迴歸那樣強迫 region 編碼每增加 1 就產生固定幅度的收入變化。",
    "concept": (
        "把 A、B、C 等無序類別編成 1、2、3，會引入原本不存在的順序與距離。線性模型把此數值乘"
        "上一個係數，因此隱含 1 到 2 與 2 到 3 的效果相同。樹模型依門檻把資料分區，再由多棵樹"
        "平均，可表達非線性與交互作用，不要求固定線性斜率。不過整數編碼仍限制樹只能做相鄰數值"
        "切分，最佳實務通常仍是 one-hot 或具原生類別支援的模型。"
    ),
    "answerReason": (
        "主管禁止更改 1、2、3 編碼時，四項中只有 D 的隨機森林能以多次門檻切分降低單一線性"
        "大小關係的影響，且可用 RandomForestRegressor 預測連續收入。Ridge 與線性核 SVM 仍是"
        "線性關係；羅吉斯迴歸則主要用於分類，不適合此連續收入目標。"
    ),
    "optionAnalysis": {
        "A": "羅吉斯迴歸用來估計類別機率，不是一般連續收入迴歸；而且其線性預測子仍會把 1、2、3 當具有固定方向與間距，未處理題述核心問題。",
        "B": "Ridge 只在線性迴歸損失中加入 L2 正則化，使係數收縮；region 每增加 1 仍造成相同係數效果，因此錯誤的序數假設仍存在。",
        "C": "線性核的支援向量方法仍以特徵的線性組合形成決策／迴歸函數，整數編碼的大小與等距關係仍會進入模型；題目又以 SVM 泛稱，未明確指定連續目標所需的 SVR。",
        "D": "正確。RandomForestRegressor 聚合多棵決策樹，能透過不同門檻與其他特徵的交互切分建立非線性收入預測，較不會把區域代碼直接解釋為固定線性增幅。",
    },
    "trap": "樹模型降低線性誤解，不等於把錯誤編碼變正確；代碼次序仍會限制可用切分。若沒有『不得修改編碼』限制，無序區域通常應 one-hot 編碼。",
    "editorialNote": "本站依官方答案 D 判定，並將題目所稱隨機森林理解為連續收入任務的 RandomForestRegressor。整數標籤對樹模型仍非完全無害；本題只能說 D 是給定選項中較合理的替代。",
    "references": [
        exam_ref(42),
        ref("scikit-learn－RandomForestRegressor", "https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestRegressor.html", "以多棵決策樹擬合連續目標並平均預測"),
        ref("scikit-learn－Encoding categorical features", "https://scikit-learn.org/stable/modules/preprocessing.html#encoding-categorical-features", "無序類別整數編碼會被估計器解讀為有順序，常以 OneHotEncoder 處理"),
    ],
}

DRAFTS[43] = {
    "summary": "正確答案是 C。異常偵測只要有可信標籤就能使用監督式二元分類；聲稱只能用分群或離群值方法，並不是合理的上線質疑。",
    "concept": (
        "Accuracy 是預測正確筆數占全部筆數的比例。在正類僅 0.05% 時，永遠預測正常即可得到"
        "99.95%，卻抓不到任何作弊者，因此應另外檢查作弊類 recall、precision、混淆矩陣、PR 曲線"
        "及閾值表現。附圖雖顯示類別 0、1 的 precision、recall、F1 都為 1.00，但仍需確認測試集"
        "是否獨立、包含多少正類、是否有資料洩漏，以及指標是否因四捨五入掩蓋錯誤。"
    ),
    "answerReason": (
        "A、B、D 都指出極度不平衡資料只看 Accuracy 的具體風險。C 把可用方法錯誤限縮：若"
        "歷史案件能提供作弊／正常標籤，二元分類正是可行方法；缺少標籤時才常改用孤立森林、"
        "分群等非監督異常偵測。題目問『不是合理理由』，故選 C。"
    ),
    "optionAnalysis": {
        "A": "合理質疑。正常占 99.95% 時，全猜正常的 accuracy 就是 99.95%，但作弊類 TP=0、FN 為全部作弊者，正類 recall 為 0。",
        "B": "合理質疑。業務要攔截作弊者，就要知道 TP/(TP+FN) 的 recall；只報整體 accuracy 無法判斷漏掉多少真正外掛司機。附圖雖列 recall，仍應核對樣本數與評估切分。",
        "C": "正確答案。異常案件若已有標籤，可用羅吉斯迴歸、樹模型等二元分類器監督學習；分群與離群值法是缺標籤時的可選方向，不是唯一合法方法。",
        "D": "合理質疑。多數類會支配 accuracy，讓模型看似接近完美；需要逐類指標、PR-AUC、混淆矩陣與符合商業成本的閾值評估異常偵測能力。",
    },
    "trap": "題目問『不是』。另不要被附圖四捨五入後的 1.00 欺騙：若少數類測試樣本很少，完美分數的不確定性很大，也必須排查重複資料與洩漏。",
    "editorialNote": "本站已目視核對 Q43 圖：classification report 中類別 0、1 以及 macro／weighted average 均顯示 1.00，但圖未呈現 support。故解析保留測試正類數量、切分方式與資料洩漏仍待核對的限制。",
    "references": [
        exam_ref(43, "第 43 題題組敘述、classification report 附圖、選項與官方答案"),
        ref("scikit-learn－Metrics and scoring", "https://scikit-learn.org/stable/modules/model_evaluation.html", "不平衡分類、balanced accuracy、precision、recall 與 F1 的定義及適用性"),
        ref("scikit-learn－classification_report", "https://scikit-learn.org/stable/modules/generated/sklearn.metrics.classification_report.html", "逐類 precision、recall、F1、support 與 macro／weighted average 的報表定義"),
    ],
}

DRAFTS[44] = {
    "summary": "正確答案是 A。商業目標把漏掉作弊者視為最嚴重錯誤，因此應優先最大化作弊類 Recall；降低判定門檻通常會增加被判為作弊的人數並減少假陰性。",
    "concept": (
        "Recall=TP/(TP+FN)，衡量真正作弊者中有多少被抓到；Precision=TP/(TP+FP)，衡量被攔截者"
        "中有多少真的作弊。降低正類機率閾值，通常使更多樣本判為正類，recall 上升但 false"
        " positives 也增加，precision 與 specificity 可能下降。閾值應在獨立驗證集上依漏判與誤判"
        "成本選擇，不能把訓練預設的 0.5 當成不可更動規則。"
    ),
    "answerReason": (
        "題幹明示不能放過任何外掛司機，卻可接受誤凍結後人工覆核，也就是假陰性成本遠高於"
        "假陽性成本。A 的高 recall 直接降低 FN，且降低 threshold 通常符合此方向；其他選項"
        "分別優先減少 FP、僵化使用 0.5，或要求正常類零誤判，皆與商業優先序相反。"
    ),
    "optionAnalysis": {
        "A": "正確。降低 threshold 會把更多可疑分數納入正類，通常提高 TP 並降低 FN，使作弊類 recall 上升；增加的誤凍結可依題意交由人工覆核。",
        "B": "提高 threshold 常減少 FP、提高 precision，卻也可能把分數未達高門檻的真正作弊者改判正常，使 FN 增加；這與『不能放過』目標相反。",
        "C": "0.5 只是常見預設決策界線，不是訓練平衡的一部分。訓練完成後依驗證資料調 threshold 不會改模型參數，反而是落實業務成本的重要步驟。",
        "D": "Specificity=TN/(TN+FP)；要求 100% 是完全不誤傷正常者，通常需提高門檻並犧牲作弊 recall。題幹明確允許部分 FP，因此不應把 specificity 放在首位。",
    },
    "trap": "先把文字成本翻成混淆矩陣：不能漏掉正類就是壓低 FN、提高 Recall；不能誤傷正常類才是壓低 FP、提高 Specificity／Precision。",
    "editorialNote": "『零容忍』在有限資料上通常無法保證真正 100% recall。實務上應在獨立且具代表性的驗證集設定可接受漏判上限，並估算人工覆核量、模型漂移與申訴風險。",
    "references": [
        exam_ref(44),
        ref("scikit-learn－Precision-Recall", "https://scikit-learn.org/stable/auto_examples/model_selection/plot_precision_recall.html", "決策閾值改變時 precision 與 recall 的取捨"),
        ref("scikit-learn－recall_score", "https://scikit-learn.org/stable/modules/generated/sklearn.metrics.recall_score.html", "Recall 為 tp/(tp+fn)，亦稱 sensitivity"),
    ],
}

DRAFTS[45] = {
    "summary": "正確答案是 C。先依 CustomerID 分組加總每位客戶所有交易的 Revenue，再以 nlargest(3) 直接取總營收最高三名，才符合『總貢獻營收』。",
    "concept": (
        "交易表是一客戶對多訂單；客戶層級總貢獻必須先用 groupby 將相同 CustomerID 的 Revenue"
        "加總，再在聚合結果上排名。Series.nlargest(n) 直接傳回最大的 n 筆值及其索引，語意比"
        "先全排序再 head 清楚，且通常不必完整排序所有客戶。若 Revenue 含缺值，sum 預設略過"
        "缺值，分析時仍應先確認缺值代表未知還是零。"
    ),
    "answerReason": "C 完整執行客戶分組、營收加總與前三名選取。A 排的是單筆訂單；B 只取各客戶最大一筆且未依結果降冪排序；D 計算客戶出現次數，回答的是訂單筆數而非營收。",
    "optionAnalysis": {
        "A": "它先按每筆 Revenue 排序，只會得到最高的三筆交易；同一客戶可能重複出現，也會漏掉靠多筆中等訂單累積成最高總營收的客戶。",
        "B": "groupby 後的 max 只保留每位客戶最大單筆收入，不是總貢獻；接著 head(3) 也只是取目前索引順序前三組，並未選最大三個聚合值。",
        "C": "正確。sum 將每位客戶的所有交易營收聚合，CustomerID 成為結果索引；nlargest(3) 再選出總額最大的三位客戶及其總營收。",
        "D": "value_counts('CustomerID') 計算各客戶出現筆數，適合找訂單最多或紀錄最多者；它不讀取 Revenue，所以高頻低額客戶可能被誤認為營收最高。",
    },
    "trap": "先辨認分析單位：資料列是訂單，問題要客戶。看到『總貢獻』必須 groupby + sum；max 是最大單筆，value_counts 是筆數，兩者都不是總額。",
    "references": [
        exam_ref(45, "第 45～47 題共用電商資料情境、第 45 題選項與官方答案"),
        ref("pandas GroupBy sum", "https://pandas.pydata.org/docs/reference/api/pandas.core.groupby.DataFrameGroupBy.sum.html", "依群組計算數值總和"),
        ref("pandas.Series.nlargest", "https://pandas.pydata.org/docs/reference/api/pandas.Series.nlargest.html", "回傳 Series 中最大的 n 個元素"),
    ],
}

DRAFTS[46] = {
    "summary": "正確答案是 A。`df['Category'] == 'Electronics'` 先產生布林遮罩選出電子產品列，再從這些列取 Revenue 並計算平均值。",
    "concept": (
        "pandas 布林索引先對欄位逐列比較，得到與 DataFrame 同長度的 True／False Series，再以"
        "df[mask] 或 df.loc[mask, columns] 篩列。篩選後的 Revenue 是 Series，mean() 計算其中"
        "非缺失值的算術平均。`.loc[row_selector, column_selector]` 的第一維通常是索引標籤或布林"
        "遮罩；DataFrame.filter 則依欄名或索引標籤選軸，不是依儲存格內容篩選。"
    ),
    "answerReason": "A 的比較發生在 Category Series 上，因此會正確選出 Category 等於 Electronics 的全部交易，再計算其 Revenue 平均。B 比較的是兩個常值字串；C 把分類值誤當列索引；D 把分類值誤當欄名。",
    "optionAnalysis": {
        "A": "正確。內層 `df['Category'] == 'Electronics'` 逐列產生布林遮罩，外層取出符合列，最後選 Revenue Series 並呼叫 mean()。",
        "B": "`'Category' == 'Electronics'` 是兩個固定字串比較，結果為 False，不會逐列檢查 Category 欄；因此 `df[False]` 不是有效的資料列篩選方式。",
        "C": "`.loc['Electronics', 'Revenue']` 會尋找索引標籤為 Electronics 的列；題組只說 Category 欄含該值，沒有說 DataFrame 索引已設成 Category。",
        "D": "DataFrame.filter(items=...) 依指定軸的標籤挑選欄或列；Electronics 是 Category 欄中的值而非欄名，無法以此語法篩出該分類交易。",
    },
    "trap": "欄位值篩選要把比較寫在 Series 上：`df['欄位'] == 值`。`.loc['值']` 查的是索引標籤，filter(items=...) 查的是軸標籤，都不是內容條件。",
    "references": [
        exam_ref(46, "第 45～47 題共用電商資料情境、第 46 題選項與官方答案"),
        ref("pandas User Guide－Boolean indexing", "https://pandas.pydata.org/docs/user_guide/indexing.html#boolean-indexing", "以布林向量篩選 Series 與 DataFrame 的列"),
        ref("pandas.Series.mean", "https://pandas.pydata.org/docs/reference/api/pandas.Series.mean.html", "計算 Series 的平均值並預設排除缺失值"),
    ],
}

DRAFTS[47] = {
    "summary": "正確答案是 C。以 CustomerID 為鍵做 inner merge，只保留 df 與 customers 兩表鍵值交集中的交易，並把匹配客戶的 Region 欄接入結果。",
    "concept": (
        "關聯式合併依 key 對齊資料。Inner join 保留左右兩表都出現的鍵；left join 保留左表全部；"
        "outer join 保留兩表鍵的聯集。pd.merge(..., on='CustomerID') 明確指定共同欄位為連接鍵。"
        "若 customers 中同一 CustomerID 重複，合併會造成交易列倍增，因此實務上應驗證右表鍵"
        "唯一，例如使用 validate='many_to_one'。"
    ),
    "answerReason": "題目要求只保留 customers 有對應資料的交易，也就是兩表 CustomerID 的交集，恰好是 C 的 inner merge。concat 只按索引並排；outer 保留未匹配列；未指定索引設定的 join 也不等同明確欄對欄合併。",
    "optionAnalysis": {
        "A": "axis=1 的 concat 主要按現有索引把兩表橫向排列，不會自動以 CustomerID 比對；兩表列順序或索引不同時，Region 可能接到錯誤交易。",
        "B": "outer merge 保留 CustomerID 聯集，包含 df 中找不到客戶資料的交易，以及 customers 中沒有交易的客戶；這與『只保留有對應資料』相反。",
        "C": "正確。`on='CustomerID'` 指定共同鍵，`how='inner'` 只輸出兩表都匹配的鍵；df 的交易欄與 customers 的 Region 會組合到同一列。",
        "D": "DataFrame.join 預設把呼叫端欄位 CustomerID 對到 customers 的索引，且預設 how='left'；除非先把 customers 索引設為 CustomerID 並改用 inner，否則不符合題設。",
    },
    "trap": "『只保留兩邊都有』就是 inner。還要分清 merge(on=共同欄) 與 join(on=左欄、右索引)；名稱都叫合併，但預設對齊位置不同。",
    "references": [
        exam_ref(47, "第 45～47 題共用電商資料情境、第 47 題選項與官方答案"),
        ref("pandas.merge 官方文件", "https://pandas.pydata.org/docs/reference/api/pandas.merge.html", "inner merge 使用兩表鍵的交集，並說明 on 與 how 參數"),
        ref("pandas.DataFrame.join 官方文件", "https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.join.html", "join 的 on 參數將呼叫端欄位對齊另一表索引，預設 how 為 left"),
    ],
}

DRAFTS[48] = {
    "summary": "正確答案是 C。新建立的 StandardScaler 尚未學到平均數與標準差，`fit_transform(X)` 會先以 X 擬合縮放參數，再立即回傳標準化後資料。",
    "concept": (
        "StandardScaler 對每個特徵計算訓練資料的平均數與標準差，再轉換為 z=(x-u)/s。fit() 只估計"
        "並保存 mean_、scale_ 等參數；transform() 使用已保存參數轉換資料；fit_transform() 結合"
        "兩步。已目視核對題組圖：X 是 iris.data 的四個連續特徵，y 是三類標籤。評估模型時"
        "應先切分，只在 X_train 上 fit，再用相同 scaler transform X_train 與 X_test，避免洩漏。"
    ),
    "answerReason": "題幹的 scaler 剛由 StandardScaler() 建立，尚未擬合；C 同時完成參數估計與資料轉換並回傳 X_norm。A 缺少 fit，B 只回傳估計器本身，D 的呼叫對象與輸入方向都錯。",
    "optionAnalysis": {
        "A": "transform 必須在同一 scaler 已 fit 後才能使用；剛建立的 scaler 沒有 mean_ 與 scale_，直接 transform(X) 會觸發尚未擬合錯誤。",
        "B": "fit(X) 會學得各欄平均與尺度，但回傳的是 fitted scaler 物件，不是轉換後的數值矩陣，因此 X_norm 不會是標準化特徵。",
        "C": "正確。scaler.fit_transform(X) 先學習 X 各特徵的平均與標準差，再以相同參數轉換 X，回傳可供後續建模的標準化陣列。",
        "D": "fit_transform 是 scaler 的方法，應以 `scaler.fit_transform(X)` 呼叫；此寫法把 scaler 當成待轉換資料，且沒有以物件方法或合法函式簽章執行。",
    },
    "trap": "fit 是學參數，transform 才產生轉換資料。考試單句選 C；真實評估流程則不能先對完整 X fit_transform，否則測試集資訊會滲入平均與標準差。",
    "editorialNote": "本站已目視核對 Q48～50 共用附圖：load_iris 後設定 `X = iris.data, y = iris.target`，四個 feature_names 與三個 target_names 亦清楚列出。Q48 依單獨語法題選 C；若承接後續 train/test 評估，應改在切分後只以訓練集擬合 scaler。",
    "references": [
        exam_ref(48, "第 48～50 題共用 iris 程式附圖、第 48 題選項與官方答案"),
        ref("scikit-learn－StandardScaler", "https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html", "標準化公式、fit、transform 與 fit_transform 行為"),
        ref("scikit-learn－Common pitfalls", "https://scikit-learn.org/stable/common_pitfalls.html#data-leakage", "切分後只以訓練資料學習前處理參數以避免資料洩漏"),
    ],
}

DRAFTS[49] = {
    "summary": "正確答案是 B。附圖 B 以 `train_test_split(X_norm, y, ...)` 維持特徵在前、標籤在後，建立 `LogisticRegression(solver='lbfgs')`，再以 `fit(X_train, y_train)` 擬合三類 iris。",
    "concept": (
        "train_test_split 依輸入順序回傳每個陣列的 train、test，因此傳入 X、y 後應接成 X_train、"
        "X_test、y_train、y_test。估計器 fit 的慣例是 fit(X, y)，X 為二維樣本×特徵，y 為一維"
        "目標。已目視核對四張選項圖：A、B 的 X/y 順序正確，C、D 反傳 y、X_norm；B 使用 lbfgs，"
        "A 使用 liblinear。題組是三類 iris，lbfgs 適合直接處理多類羅吉斯迴歸。"
    ),
    "answerReason": (
        "B 的資料輸入、變數承接與 fit 參數形狀皆正確，且 lbfgs 支援三類問題。C、D 因把 y 放在"
        "第一個輸入，會使 X_train 實為一維標籤、y_train 實為二維特徵，fit 無法成立。A 的順序"
        "雖正確，但 liblinear 不直接最佳化 multinomial，多類時需 One-vs-Rest 包裝，因此 B 最合適。"
    ),
    "optionAnalysis": {
        "A": "X、y 與 fit 的順序正確，但圖中 solver='liblinear'；官方現行文件指出多類問題若仍使用 liblinear，應以 OneVsRestClassifier 包裝，不如 B 的 lbfgs 直接適合三類 iris。",
        "B": "正確。圖中先以 `train_test_split(X_norm, y, train_size=0.2, random_state=123)` 切分，再建立 lbfgs 羅吉斯迴歸並 `fit(X_train, y_train)`，資料形狀與三類求解器均相符。",
        "C": "圖中把 `y, X_norm` 傳入切分器，卻仍用 X_train、X_test 接前兩個輸出；結果 X_train 是一維類別標籤，而 y_train 是二維特徵矩陣，fit 的 X/y 角色顛倒。",
        "D": "它和 C 一樣交換 train_test_split 的 y 與 X_norm，造成 fit 輸入角色與維度錯誤；即使 lbfgs 求解器適合多類，也無法補救資料順序錯置。",
    },
    "trap": "先逐字追蹤切分器的輸入與四個輸出，不要只看 solver。另圖中是 train_size=0.2，代表訓練集只有 20%；這雖語法有效，實務上通常會再確認是否原意其實是 test_size=0.2。",
    "editorialNote": (
        "本站已於 2026-08-13 目視核對 Q49 四張選項圖。官方答案 B 最符合當前三類模型建議；"
        "但 A 在部分舊版 scikit-learn 可由 LogisticRegression 對多類資料採 OvR 而成功執行，故題目"
        "若只問『可執行』存在版本依賴的解釋空間。另 A、B 都寫 train_size=0.2，僅以 20% 訓練，"
        "以及題組先標準化再切分可能造成資料洩漏，均應在人工複核時註記。"
    ),
    "references": [
        exam_ref(49, "第 48～50 題共用 iris 附圖、第 49 題 A～D 四張程式選項圖與官方答案"),
        ref("scikit-learn－train_test_split", "https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html", "依輸入陣列順序回傳各自 train/test 子集，並定義 train_size"),
        ref("scikit-learn－LogisticRegression", "https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html", "fit(X,y) 介面、solver 支援與多類分類限制"),
        ref("scikit-learn－Linear Models", "https://scikit-learn.org/stable/modules/linear_model.html#logistic-regression", "liblinear 用於多類問題時搭配 OneVsRestClassifier 的官方說明"),
    ],
}

DRAFTS[50] = {
    "summary": "正確答案是 D。附圖以 `f1_score(y_test, y_pred, average='weighted')` 先算各類 Precision 與 Recall 的 F1 調和平均，再依各類真實樣本數 support 加權平均，以反映類別占比。",
    "concept": (
        "單一類別 F1=2PR/(P+R)，同時要求 precision 與 recall；weighted average 則以每類在 y_true"
        "中的 support 作權重。已目視核對附圖：混淆矩陣為 [[13,0,0],[0,6,0],[0,1,10]]，只有一筆"
        " virginica 被預測成 versicolor，weighted F1 約 0.967。scikit-learn confusion_matrix 的列"
        "代表真實類別、欄代表預測類別；對角線較大只表示此測試集多數預測正確，不能單獨診斷過擬合。"
    ),
    "answerReason": "D 完整描述 F1 的類內調和平均與 weighted 的跨類 support 加權。A 把列與欄混淆；B 只憑測試混淆矩陣對角線判定過擬合；C 只說『平均』而未說明按各類樣本數加權，資訊不足。",
    "optionAnalysis": {
        "A": "cm 的確是混淆矩陣，但 scikit-learn 定義 `C[i,j]` 為真實類別 i 被預測成類別 j 的數量，所以橫列是真實值、直欄才是預測值；此選項後半錯誤。",
        "B": "對角線大代表分類正確數較多，附圖 30 筆中有 29 筆正確；過度擬合必須比較訓練與獨立驗證／測試表現，不能只由單一測試矩陣的形狀判定。",
        "C": "weighted 當然會產生一個平均 F1，但關鍵不是普通算術平均；它先計算每一類 F1，再依該類 support 加權。少了權重定義，未完整說明參數意義。",
        "D": "正確。每類 F1 是該類 precision 與 recall 的調和平均，`average='weighted'` 再依真實樣本數加權；附圖 support 13、6、11 導出約 0.967 的 weighted F1。",
    },
    "trap": "混淆矩陣記成 row=true、column=predicted；weighted F1 的『weighted』是按 support，不是把 Precision 和 Recall 任意加權。高測試分數也不等同過擬合。",
    "editorialNote": "本站已目視核對 Q50 圖中完整程式與輸出，包括 confusion matrix、weighted F1=0.9671550671550672 及 classification report。Weighted F1 會讓多數類影響較大，極度不平衡時仍應同看逐類 F1 與 macro F1。",
    "references": [
        exam_ref(50, "第 50 題程式、混淆矩陣與 classification report 附圖、選項及官方答案"),
        ref("scikit-learn－confusion_matrix", "https://scikit-learn.org/stable/modules/generated/sklearn.metrics.confusion_matrix.html", "C[i,j] 表示真實類別 i 被預測為類別 j 的樣本數"),
        ref("scikit-learn－f1_score", "https://scikit-learn.org/stable/modules/generated/sklearn.metrics.f1_score.html", "F1 調和平均公式與 weighted 依各類 support 加權的定義"),
        ref("scikit-learn－classification_report", "https://scikit-learn.org/stable/modules/generated/sklearn.metrics.classification_report.html", "逐類 precision、recall、F1、support 與 weighted average"),
    ],
}


def main() -> None:
    questions = json.loads(QUESTIONS.read_text(encoding="utf-8"))
    index = {
        q["officialQuestionNumber"]: q
        for q in questions
        if q["sourceId"] == SOURCE_ID
    }

    written = 0
    for number, draft in sorted(DRAFTS.items()):
        question = index.get(number)
        if question is None:
            raise SystemExit(f"Q{number} not found in {SOURCE_ID}")
        actual = question["officialAnswer"][0]
        if actual != EXPECTED_ANSWER[number]:
            raise SystemExit(
                f"Q{number}: official answer is {actual}, "
                f"but the draft was written for {EXPECTED_ANSWER[number]}"
            )
        if question["explanationStatus"] == "reviewed":
            raise SystemExit(f"Q{number} is already reviewed; refusing to overwrite")
        if sorted(draft["optionAnalysis"]) != ["A", "B", "C", "D"]:
            raise SystemExit(f"Q{number}: option analysis must cover A-D")
        if not draft["summary"].startswith(f"正確答案是 {actual}"):
            raise SystemExit(f"Q{number}: summary does not state the official answer")

        explanation = question["explanation"]
        explanation["summary"] = draft["summary"]
        explanation["concept"] = draft["concept"]
        explanation["answerReason"] = draft["answerReason"]
        explanation["optionAnalysis"] = {
            label: draft["optionAnalysis"][label] for label in "ABCD"
        }
        explanation["trap"] = draft["trap"]
        explanation["references"] = draft["references"]
        explanation["editorialNote"] = draft.get("editorialNote", DEFAULT_NOTE)
        explanation["author"] = AUTHOR
        explanation["authoredAt"] = AUTHORED_AT
        explanation.pop("reviewer", None)
        explanation.pop("reviewedAt", None)
        question["explanationStatus"] = "draft"
        written += 1

    QUESTIONS.write_text(
        json.dumps(questions, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    drafts = sum(1 for q in questions if q["explanationStatus"] == "draft")
    print(f"Wrote {written} explanation drafts; {drafts} drafts in {QUESTIONS}")


if __name__ == "__main__":
    main()
