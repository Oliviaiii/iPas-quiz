"""Write explanation drafts for 114-2 intermediate subject two, Q41-Q50.

The script validates official answers, refuses to overwrite reviewed content,
and leaves every generated explanation in ``draft`` status.

Usage::

    python scripts/write-explanations-114-2-m2-041-050.py
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUESTIONS = ROOT / "app" / "data" / "questions.json"
SOURCE_ID = "aiap-114-intermediate-2-big-data"
AUTHOR = "Codex（AI 輔助初稿）"
AUTHORED_AT = "2026-08-12"
CHECKED_AT = "2026-08-12"

EXAM_PDF = (
    "https://www.ipas.org.tw/api/proxy/uploads/certification_resource/"
    "bf93f438f7be48d295c1b40a34d79f3d/"
    "114年第二梯次中級AI應用規劃師第二科大數據處理分析與應用"
    "(當次試題公告114_20251226000634.pdf"
)
SKLEARN_KMEANS = "https://scikit-learn.org/stable/modules/clustering.html#k-means"
SCIPY_POISSON = (
    "https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.poisson.html"
)
PANDAS_INTEGER = "https://pandas.pydata.org/pandas-docs/stable/user_guide/integer_na.html"
PANDAS_GROUPBY_SUM = (
    "https://pandas.pydata.org/pandas-docs/stable/reference/api/"
    "pandas.api.typing.DataFrameGroupBy.sum.html"
)
PANDAS_MELT = "https://pandas.pydata.org/docs/reference/api/pandas.melt.html"
SEABORN_BARPLOT = "https://seaborn.pydata.org/generated/seaborn.barplot.html"
PANDAS_NLARGEST = (
    "https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.nlargest.html"
)
PANDAS_DESCRIBE = (
    "https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.describe.html"
)
PANDAS_ISNA = "https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.isna.html"
PANDAS_ISNULL = "https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.isnull.html"
SKLEARN_LINEAR = "https://scikit-learn.org/stable/modules/linear_model.html"
STATSMODELS_OLS = (
    "https://www.statsmodels.org/stable/generated/statsmodels.regression.linear_model.OLS.html"
)

DEFAULT_NOTE = "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。"


def ref(title: str, url: str, locator: str) -> dict:
    return {"title": title, "url": url, "locator": locator, "checkedAt": CHECKED_AT}


def exam_ref(number: int) -> dict:
    return ref(
        "114 年第二次中級 AI 應用規劃師－大數據處理分析與應用公告試題",
        EXAM_PDF,
        f"第 {number} 題題幹、選項、共用題組附圖與官方答案",
    )


EXPECTED_ANSWER = {
    41: "A", 42: "C", 43: "B", 44: "D", 45: "A",
    46: "C", 47: "B", 48: "D", 49: "C", 50: "B",
}

DRAFTS: dict[int, dict] = {}

DRAFTS[41] = {
    "summary": "正確答案是 A。附圖反覆將每筆資料指派給最近中心，再用群內資料平均值更新中心，正是 K-means 分群。",
    "concept": (
        "K-means 先選定 K 個初始中心，接著交替做兩個步驟：指派步驟把每個樣本放到距離最近的"
        "中心；更新步驟把每群所有樣本的座標平均，作為新中心。兩步反覆執行，直到中心不再"
        "明顯移動或目標函數改善小於門檻。它最小化群內平方距離總和，適合近似球形、尺度相近"
        "的群；結果會受特徵尺度、離群值與初始中心影響。"
    ),
    "answerReason": (
        "已目視核對官方附圖：先隨機選 K 個資料點當中心，逐點計算到每個中心的距離並指派最近"
        "群，再以群內平均更新中心，中心不動即停止。這些是 K-means 的完整識別特徵，因此選 A。"
    ),
    "optionAnalysis": {
        "A": (
            "正確。最近中心指派與群內平均更新正是 K-means 的兩個交替步驟；輸出群標籤與最後"
            "centroids 也與附圖定義一致。"
        ),
        "B": (
            "高斯混合模型會估計每個成分的權重、平均與共變異數，並以機率責任值做軟分群；"
            "附圖只有最近距離的硬指派，沒有高斯密度、共變異數或 EM 責任值。"
        ),
        "C": (
            "階層式分群通常逐步合併最近群或拆分群，產生樹狀圖，不需反覆計算固定 K 個中心。"
            "附圖沒有 linkage 或 dendrogram，而是明確更新均值中心。"
        ),
        "D": (
            "DBSCAN 依 epsilon 鄰域與 MinPts 找密度相連區域，能標記噪聲且不先指定群數；附圖"
            "要求輸入 K，並依中心距離分群，與密度式流程不同。"
        ),
    },
    "trap": (
        "看到「最近中心＋取平均更新」就鎖定 K-means。GMM 也有平均參數，但使用機率軟指派；"
        "DBSCAN 看鄰域密度；階層式看群合併／拆分，不會反覆更新固定數目的中心。"
    ),
    "editorialNote": (
        "本站已於 2026-08-12 目視核對 questions.json figures 所指官方裁切圖。本站內容為 AI"
        "輔助詳解初稿，並非官方詳解；尚待獨立人工複核。"
    ),
    "references": [
        exam_ref(41),
        ref(
            "scikit-learn User Guide－K-means",
            SKLEARN_KMEANS,
            "先指派樣本至最近 centroid，再以群內樣本平均建立新 centroid，重複至中心移動低於門檻",
        ),
    ],
}

DRAFTS[42] = {
    "summary": "正確答案是 C。卜瓦松模型假設事件在區間內獨立發生且平均發生率固定；本題 lambda=5 是平均每小時 5 件，不是最大值。",
    "concept": (
        "Poisson 分佈描述固定時間或空間區間內的事件計數，參數 lambda 是該區間的期望事件數，"
        "其支撐為 0、1、2…，沒有以 lambda 為上限。標準模型要求在足夠小的區間內發生機會"
        "與區間長度成比例、事件彼此獨立且發生率穩定。SciPy 的 `poisson.pmf(k, mu)` 回傳"
        "P(X=k)，`cdf(k, mu)` 回傳 P(X≤k)，右尾機率則可用 survival function。"
    ),
    "answerReason": (
        "附圖設定 `lambda_poisson=5` 並呼叫 `poisson.pmf(5, lambda_poisson)`，只是在平均率 5"
        "下計算剛好 5 件的機率。四項中 C 正確描述 Poisson 的核心建模條件；A 把平均當上限，"
        "B 把 PMF 當累積機率，D 把 CDF 的方向寫反。"
    ),
    "optionAnalysis": {
        "A": (
            "lambda=5 表示每小時瑕疵數的期望值為 5，不是最多只能 5 件。Poisson 隨機變數可"
            "取任何非負整數，只是離平均越遠通常機率越小。"
        ),
        "B": (
            "`poisson.pmf(5,5)` 是 P(X=5)，即恰好 5 個瑕疵品。小於 5 的機率應加總 0 到 4，"
            "可用 `poisson.cdf(4,5)`。"
        ),
        "C": (
            "正確。獨立事件與固定平均發生率是標準 Poisson process／計數模型的重要條件，"
            "使單位時間的事件數可由同一 lambda 描述。"
        ),
        "D": (
            "`poisson.cdf(10,5)` 回傳 P(X≤10)，不是 P(X≥10)。若要至少 10 件，可用"
            "P(X≥10)=1-P(X≤9)，在 SciPy 中以 `poisson.sf(9,5)` 較直接。"
        ),
    },
    "trap": (
        "PMF 的 m 是 mass：求剛好 k；CDF 是累積到 k：求 ≤k；SF 是右尾：求 >k。另不要把"
        "Poisson 的 lambda 當成最大值，它同時是該分佈的平均數與變異數。"
    ),
    "editorialNote": (
        "本站已於 2026-08-12 目視核對官方程式碼附圖。實際生產瑕疵若有批次效應、事件相依或"
        "發生率隨時間改變，單一 Poisson 模型可能不適合；本站仍依題目設定與官方答案 C 作答。"
    ),
    "references": [
        exam_ref(42),
        ref(
            "SciPy API－scipy.stats.poisson",
            SCIPY_POISSON,
            "Poisson PMF 公式、mu 參數，以及 pmf、cdf、sf、mean、var 等方法定義",
        ),
    ],
}

DRAFTS[43] = {
    "summary": "正確答案是 B。Year 欄含 NaN 時，傳統 NumPy 整數欄無法表示缺值，pandas 常提升為 float；原始值若寫成 2006.0 也會被推斷為浮點。",
    "concept": (
        "CSV 沒有內建資料型態，`read_csv` 會依欄位內容推斷 dtype。一般 NumPy `int64` 無法存"
        "`NaN`，因此整數樣式的欄位只要含傳統 `NaN`，常被轉為 `float64`，其非缺值會顯示為"
        "2006.0。若檔案本來含小數表示，如 `2006.0`，也會推斷為浮點。純整數且沒有缺值的"
        "數值欄通常可維持整數，pandas 並不會把所有數值無條件讀成 float64。"
    ),
    "answerReason": (
        "題組附圖顯示 Year 有 16,598 筆並以 `2006.0` 等格式輸出。原因 A 符合缺值迫使傳統"
        "整數欄轉浮點的機制，原因 D 也可直接導致浮點推斷；B 所謂字串轉換「出錯而變浮點」"
        "不是一般推斷規則，C 更錯稱所有數值都預設為 float，因此組合為 A、D，即選 B。"
    ),
    "optionAnalysis": {
        "A": (
            "正確。原因 B 與 C 都不成立：可解析的年份字串可被正常判斷為數值，解析失敗更可能"
            "保留為文字／object；pandas 也會在全為整數時使用整數 dtype。"
        ),
        "B": (
            "正確答案。原因 A 成立，因傳統整數陣列不能保存 NaN；原因 D 也成立，CSV 若含"
            "`2006.0` 等小數記法，欄位內容本身就支持 float64。"
        ),
        "C": (
            "此組合多列了原因 B。字串 `\"2006\"` 若整欄都能解析，轉數值不會因「出錯」而"
            "自然變成 float；若混入無法解析字串，欄位常維持字串／object，除非另行指定轉換。"
        ),
        "D": (
            "原因 D 成立，但原因 C 不成立。pandas 會依內容選整數、浮點、文字等 dtype，不是"
            "所有數值都預設 float64。"
        ),
    },
    "trap": (
        "看到年份顯示 `.0` 不代表它真的含有年份小數，可能只是整數欄為了容納 NaN 而被提升成"
        "float。要用 `isna().sum()` 與原始 CSV 實際檢查，不能只憑前五列判定原因。"
    ),
    "editorialNote": (
        "本站已目視核對第 43～47 題共用 `vgsales.csv` 圖與第 43 題 Year 輸出圖。題目只問可能"
        "原因，附圖本身不能區分 A 或 D 哪一個實際發生；因此依官方答案採 A、D 皆可能。"
    ),
    "references": [
        exam_ref(43),
        ref(
            "pandas User Guide－Nullable integer data type",
            PANDAS_INTEGER,
            "NaN 是浮點值，含缺值的傳統整數陣列會被迫成浮點；可用 nullable Int64 與 pandas.NA",
        ),
    ],
}

DRAFTS[44] = {
    "summary": "正確答案是 D。pandas 的 nullable `Int64` 可同時保存整數年份與缺失標記 `<NA>`，不必捏造 0 或 1 年。",
    "concept": (
        "NumPy 的小寫 `int64` 不能表示 NaN，直接把含缺值的 Series `astype(int)` 通常會失敗。"
        "pandas 提供大寫 I 的 extension dtype `Int64`，以 `pandas.NA` 表示缺失，其他值保持真正"
        "整數。這對年份、識別碼等「語意上是整數但允許未知」的欄位特別合適。若分析本身要求"
        "完整年份，之後仍須依資料來源決定補值、排除或保留未知，而不是任意填入有效數字。"
    ),
    "answerReason": (
        "D 的 `astype('Int64')` 直接把 2006.0 等完整值轉為整數，同時把 NaN 保留為 `<NA>`，"
        "符合題目「可能包含缺失值」的條件。A 無法容納缺值；B、C 雖能強制轉型，卻分別把"
        "未知年份偽造成 0 或 1，會污染趨勢分析。"
    ),
    "optionAnalysis": {
        "A": (
            "`astype(int)` 使用一般整數 dtype；若欄位仍有 NaN，轉換會因無法把非有限值轉成"
            "整數而失敗。只有先確認沒有缺值時才適用。"
        ),
        "B": (
            "填 0 可讓後續 `astype(int)` 成功，但年份 0 是人造資料，繪製趨勢時會形成錯誤年代"
            "與統計。除非 0 是文件明定的缺值代碼並在分析中排除，否則不應使用。"
        ),
        "C": (
            "填 1 與填 0 有同樣問題，甚至可能被解讀為西元 1 年；它只是繞過轉型錯誤，沒有"
            "合理處理未知年份的語意。"
        ),
        "D": (
            "正確。大寫 `Int64` 是 pandas 可空整數型別，完整年份以整數保存，缺值使用 `<NA>`"
            "傳遞，既保留資料品質資訊又方便後續篩選與分組。"
        ),
    },
    "trap": (
        "注意 `Int64` 與 `int64` 大小寫不同：前者是 pandas nullable integer，後者通常是不能含"
        "NaN 的 NumPy 整數。能轉型不等於處理正確，任意填 0/1 會扭曲年份分析。"
    ),
    "references": [
        exam_ref(44),
        ref(
            "pandas User Guide－Nullable integer data type",
            PANDAS_INTEGER,
            "字串別名 `Int64` 以 pandas.NA 保存缺值，並與 NumPy `int64` 區分",
        ),
    ],
}

DRAFTS[45] = {
    "summary": "正確答案是 A。先依 Platform 分組，再對 Global_Sales 求和，最後繪製 bar，才是每個平台的全球銷售總額長條圖。",
    "concept": (
        "分組彙總可拆成 split–apply–combine：用 `groupby('Platform')` 依平台切組，選取數值欄"
        "`Global_Sales`，以 `sum()` 加總每組所有遊戲銷量，得到平台到總銷售額的 Series；再"
        "`plot(kind='bar')` 把平台放在類別軸、總額作為高度。`count()` 與 `value_counts()` 算的是"
        "筆數，`mean()` 算每款平均銷量，都不是總額。"
    ),
    "answerReason": (
        "題組欄位說明明確指出 Global_Sales 是每款遊戲的全球銷量（百萬份）。A 依 Platform"
        "彙總該欄的 `sum()`，恰好回答各平台合計銷售多少；後接 bar plot 也符合視覺化要求。"
    ),
    "optionAnalysis": {
        "A": (
            "正確。分組鍵為 Platform、彙總值為 Global_Sales、聚合函式為 sum，產出每平台總量"
            "後以長條圖呈現，三個步驟都符合題意。"
        ),
        "B": (
            "`count()` 計算每平台 Global_Sales 的非缺失筆數，表示收錄多少款有銷售資料的遊戲，"
            "不會把百萬份銷量相加。"
        ),
        "C": (
            "`Platform.value_counts()` 統計每個平台在資料集出現的列數，也就是遊戲款數／紀錄數；"
            "它完全沒有使用 Global_Sales，因此不能代表市場銷售總額。"
        ),
        "D": (
            "`mean()` 計算每平台單款遊戲的平均全球銷量，可比較典型作品表現；平台遊戲數不同時，"
            "平均值與總市場規模可能排序相反，不符合「總額」。"
        ),
    },
    "trap": (
        "題目常用「總額、款數、平均」偷換聚合函式：總額用 sum，非缺失筆數用 count，類別"
        "出現次數用 value_counts，平均才用 mean。先圈出題目要求的量再看程式。"
    ),
    "references": [
        exam_ref(45),
        ref(
            "pandas API－DataFrameGroupBy.sum",
            PANDAS_GROUPBY_SUM,
            "GroupBy.sum 計算各群組數值總和並回傳 Series 或 DataFrame",
        ),
    ],
}

DRAFTS[46] = {
    "summary": "正確答案是 C。`melt` 把四個地區銷售欄轉為 variable/value 長格式，再由 `barplot(..., estimator=sum)` 對每個地區加總。",
    "concept": (
        "seaborn 的長格式資料通常一欄放類別、一欄放數值。原始資料把 NA、EU、JP、Other 銷量"
        "分散在四欄，`pd.melt(..., value_vars=[...])` 會將欄名放入 `variable`、銷量放入 `value`，"
        "每款遊戲產生四列。`sns.barplot(x='variable', y='value', estimator=sum)` 再依地區欄名分組"
        "加總，四根柱子的相對高度呈現各地區總銷售構成。若要百分比標籤，還需除以全部總額。"
    ),
    "answerReason": (
        "C 是唯一同時完成寬轉長、以地區為類別軸、以銷售數值為高度，並指定 `sum` 聚合的程式。"
        "其餘方法分別在數資料列、畫平台折線或呈現各欄分佈，沒有算出四地區銷售總額。"
    ),
    "optionAnalysis": {
        "A": (
            "`countplot` 計算每個類別出現幾次，不以銷售量欄位的數值加總；而把四個欄名字串直接"
            "當 x 也不是從 data 逐列取得地區銷售，因此無法顯示總額比例。"
        ),
        "B": (
            "`lineplot` 適合有順序的 x（常見為時間）及單一 y 變數；把四個欄名列表直接作 y 並"
            "以 Platform 為 x 不能形成題目要的四個地區總額長條。"
        ),
        "C": (
            "正確。melt 後 `variable` 值是四個地區欄名、`value` 是每筆銷量，barplot 使用 sum"
            "將同地區所有遊戲加總，得到可比較的四根柱。"
        ),
        "D": (
            "`histplot` 顯示銷售數值落在各區間的頻數或密度，回答的是分佈形狀；它不會產生每個"
            "地區一根、代表總銷售量的柱。"
        ),
    },
    "trap": (
        "seaborn 長格式的關鍵是 `variable`/`value`，聚合關鍵是 `estimator=sum`；預設 barplot"
        "通常算 mean。另要留意題目稱「比例」但程式畫的是總額，相對柱高可比較構成，真正百分比"
        "仍需額外正規化。"
    ),
    "editorialNote": (
        "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。選項 C 計算並顯示的是"
        "各地區銷售總額，沒有明確除以四地區總和轉成 0～100%；題目將此稱為「總額比例」可能是"
        "以柱高相對比較構成的寬鬆用語，本站作答仍依官方答案 C。"
    ),
    "references": [
        exam_ref(46),
        ref(
            "pandas API－pandas.melt",
            PANDAS_MELT,
            "將寬格式 value_vars unpivot 為預設名為 variable 與 value 的長格式欄位",
        ),
        ref(
            "seaborn API－barplot",
            SEABORN_BARPLOT,
            "barplot 以 estimator 對每個類別 bin 彙總數值；官方範例示範 estimator='sum'",
        ),
    ],
}

DRAFTS[47] = {
    "summary": "正確答案是 B。`data.nlargest(5, 'NA_Sales')` 先選出北美銷量最高的五列，再以 Name 與 NA_Sales 畫 seaborn 長條圖。",
    "concept": (
        "Top-N 分析必須先依目標數值排序或使用 `nlargest`，不能假設資料原本已按該欄排序。"
        "`DataFrame.nlargest(5,'NA_Sales')` 回傳 NA_Sales 最大的五列並保留 Name 等其他欄位，"
        "再把遊戲名稱作類別軸、北美銷量作數值軸即可比較。若同分要全部保留，可另考慮"
        "`keep='all'`，這可能使結果超過五列。"
    ),
    "answerReason": (
        "B 使用正確的排名欄 NA_Sales 先挑五筆，且 barplot 的 x/y 分別指向 Name、NA_Sales。"
        "A 只拿原資料前五列，那是題組圖中全球排名前五，不一定是北美前五；C 圖形種類不符；"
        "D 的 countplot 介面與任務都不對。"
    ),
    "optionAnalysis": {
        "A": (
            "`head(5)` 只取目前列順序的前五筆。題組資料可能按 Rank 或 Global_Sales 排序，而非"
            "NA_Sales；即使樣例恰巧接近，也沒有執行北美銷量排名，不能保證正確。"
        ),
        "B": (
            "正確。`nlargest(5,'NA_Sales')` 直接找北美銷量最高五列，Name 與 NA_Sales 都保留，"
            "barplot 便可用遊戲名分類並以銷量作柱高。"
        ),
        "C": (
            "前半段 `nlargest` 選資料正確，但 `lineplot` 用線連接五個離散遊戲名稱，會暗示不存在"
            "的連續順序；題目明確要求條狀圖，應使用 barplot。"
        ),
        "D": (
            "countplot 用來計算每個類別出現筆數，通常只指定一個分類軸，不接受以 y 指定銷售量"
            "來畫數值柱高。它也沒有先挑出 NA_Sales 最大五筆。"
        ),
    },
    "trap": (
        "`head(5)` 是目前順序前五，`nlargest(5,column)` 才是指定欄位前五。條狀圖比較離散"
        "類別數值，折線圖會暗示類別之間有連續順序，題目指定圖形時也要一起核對。"
    ),
    "references": [
        exam_ref(47),
        ref(
            "pandas API－DataFrame.nlargest",
            PANDAS_NLARGEST,
            "回傳指定 columns 數值最大的前 n 列並以遞減順序排列",
        ),
        ref(
            "seaborn API－barplot",
            SEABORN_BARPLOT,
            "以類別變數與數值變數畫出彙總值的矩形柱",
        ),
    ],
}

DRAFTS[48] = {
    "summary": "正確答案是 D。共用 `df.describe()` 圖中 youtube 的 25% 欄為 89.25，正是第一四分位數 Q1。",
    "concept": (
        "pandas 對數值 DataFrame 執行 `describe()`，每欄會列出非缺失筆數 count、平均 mean、"
        "標準差 std、最小值、25%、50%、75% 與最大值。25%、50%、75% 分別是 Q1、中位數 Q2、"
        "Q3。`count` 是該欄非缺失值數，不等於資料表總列數；不同欄 count 不同可快速暴露缺值。"
    ),
    "answerReason": (
        "已目視核對第 48～50 題共用附圖：youtube 的 25% 是 89.250000，因此 D 正確。圖中四欄"
        "youtube/facebook/newspaper/sales 的總列數為 200，facebook count=199 只是少一個非缺失值；"
        "sales 16.827 是 mean 而非 median；facebook 11.94 是 25% 而非 75%。"
    ),
    "optionAnalysis": {
        "A": (
            "資料有 4 個變數，但不是 199 筆。youtube、newspaper、sales 的 count 都是 200，"
            "只有 facebook 因一個 NaN 而 count=199；資料總列數仍為 200。"
        ),
        "B": (
            "sales 的 16.827 出現在 mean 列，是平均數；中位數要看 50% 列，圖中為 15.48。"
            "這個選項把 mean 與 median 混淆。"
        ),
        "C": (
            "facebook 的 11.94 出現在 25% 列，是第一四分位數 Q1；第三四分位數 Q3 要看 75%"
            "列，圖中是 43.68。"
        ),
        "D": (
            "正確。youtube 欄的 25% 數值明列 89.25，而第 25 百分位就是第一四分位數 Q1。"
        ),
    },
    "trap": (
        "先讀列標籤再讀數字：mean 是平均、50% 才是中位數、25%/75% 才是 Q1/Q3。count 是"
        "每欄非缺失數，不要把單欄 count=199 誤當整份資料只有 199 列。"
    ),
    "editorialNote": (
        "本站已於 2026-08-12 目視核對共用 `df.head()` 與 `df.describe()` 官方裁切圖。本站內容"
        "仍為 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。"
    ),
    "references": [
        exam_ref(48),
        ref(
            "pandas API－DataFrame.describe",
            PANDAS_DESCRIBE,
            "數值欄敘述統計包含 count、mean、std、min、25%、50%、75%、max，並排除 NaN",
        ),
    ],
}

DRAFTS[49] = {
    "summary": "正確答案是 C。pandas DataFrame 的 `isnull()` 與 `isna()` 都能標記缺失值，接 `.sum()` 即可逐欄計數；`isNaN()`、`isnan()` 不是其方法。",
    "concept": (
        "`DataFrame.isna()` 會回傳同形狀布林表格，NaN、None、pd.NA 等缺失位置為 True；對這個"
        "布林表格沿預設 axis=0 執行 `sum()`，True 會當 1，相加後得到每欄缺失數。`isnull()` 是"
        "`isna()` 的別名，語意相同。pandas 的方法名稱區分大小寫，DataFrame 並沒有 `isNaN()`"
        "或 `isnan()` 這兩個成員方法。"
    ),
    "answerReason": (
        "官方附圖輸出 youtube=0、facebook=1、newspaper=0、sales=0，符合共用 `head()` 中 facebook"
        "第二列為 NaN。選項 A `df.isnull().sum()` 與 C `df.isna().sum()` 都可得到此結果，B、D"
        "會因方法不存在而失敗，所以正確組合為 A、C，即選 C。"
    ),
    "optionAnalysis": {
        "A": (
            "選項 A 正確、D 錯誤；只選 D 會呼叫不存在的 `DataFrame.isnan()`，無法得到附圖結果。"
        ),
        "B": (
            "這個組合只有 C 正確。`isNaN()` 與 `isnan()` 都不是 pandas DataFrame 方法，方法名稱"
            "不能任意改大小寫或套用 NumPy 函式命名。"
        ),
        "C": (
            "正確答案。`isnull()` 與 `isna()` 是等價的缺失值偵測方法，兩者回傳布林遮罩後，"
            "`.sum()` 逐欄計算 True 數量。"
        ),
        "D": (
            "此組合多列了 B。A 與 C 可用，但 `df.isNaN()` 不存在；若要使用 NumPy 的"
            "`np.isnan`，那是函式呼叫且主要適用數值陣列，不是 DataFrame 成員方法。"
        ),
    },
    "trap": (
        "pandas API 名稱是全小寫 `isna`/`isnull`，不是 JavaScript 風格的 `isNaN`。`.sum()`"
        "加總布林 True 才把逐格偵測結果轉成每欄缺失數。"
    ),
    "editorialNote": (
        "本站已於 2026-08-12 目視核對共用資料圖與第 49 題缺失計數圖，確認 facebook 唯一缺失"
        "一筆。本站內容為 AI 輔助詳解初稿，尚待獨立人工複核。"
    ),
    "references": [
        exam_ref(49),
        ref(
            "pandas API－DataFrame.isna",
            PANDAS_ISNA,
            "回傳與原物件同尺寸的布林遮罩，以 True 標記 NA 值",
        ),
        ref(
            "pandas API－DataFrame.isnull",
            PANDAS_ISNULL,
            "DataFrame.isna 的別名",
        ),
    ],
}

DRAFTS[50] = {
    "summary": "正確答案是 B。scikit-learn 應以 `fit(X, y)` 訓練，附圖 OLS 的截距為 3.5561；其餘敘述與係數介面、OLS 參數順序或 p 值不符。",
    "concept": (
        "在 scikit-learn，`LinearRegression().fit(X,y)` 的 X 是形狀 `(n_samples,n_features)` 的"
        "特徵矩陣，y 是目標；預設截距另存在 `intercept_`，`coef_` 只放三個特徵係數。statsmodels"
        "的 OLS 建構順序則是 `OLS(endog, exog)`，也就是 `sm.OLS(y,X2)`；`add_constant(X)` 把截距"
        "欄顯式加入 X2。summary 中每列 `P>|t|` 用來檢驗該係數為 0。"
    ),
    "answerReason": (
        "官方附圖顯示三個特徵 youtube、facebook、newspaper，空格 1 必須是 `.fit(X,y)`，所以 B"
        "成立；summary 的 const 係數明列 3.5561，所以 F 成立。`coef_` 不含截距，C 錯；OLS 應"
        "`sm.OLS(y,X2)`，D 顛倒；newspaper p=0.914>0.05，E 也錯。因此只有 B、F，即選 B。"
    ),
    "optionAnalysis": {
        "A": (
            "此組合含 B、F 雖正確，但 C 錯。scikit-learn 把三個斜率存於 `coef_`，截距另存於"
            "`intercept_`，所以 `print(reg.coef_)` 不會輸出包括截距在內的四個值。"
        ),
        "B": (
            "正確答案。`LinearRegression().fit(X,y)` 的參數順序正確；statsmodels 表格的 const"
            "row 係數為 3.5561，故 F 也正確，且組合沒有加入其他錯誤敘述。"
        ),
        "C": (
            "A 把 fit 參數反成 `(y,X)`；C 錯稱 `coef_` 含截距；D 又把 statsmodels 的 endog/exog"
            "順序寫成 `(X2,y)`。雖 F 正確，整組仍錯。"
        ),
        "D": (
            "B 正確，但 E 錯。summary 顯示 newspaper 的 p 值 0.914，大於 alpha=0.05，不能拒絕"
            "其係數為 0 的虛無假設；不是所有迴歸係數都有顯著解釋力。"
        ),
    },
    "trap": (
        "兩套 API 的順序都以 X/y 語意核對：scikit-learn 是 `fit(X,y)`，statsmodels 是"
        "`OLS(y,X)`。另分清 `coef_` 與 `intercept_`，以及整體 F 檢定顯著不代表每個個別係數都顯著。"
    ),
    "editorialNote": (
        "本站已於 2026-08-12 目視核對第 50 題完整 OLS summary：const=3.5561，youtube 與 facebook"
        "p<0.001，newspaper p=0.914。題幹說資料已填補缺值，故 200 筆皆進入模型；本站內容仍為"
        "AI 輔助詳解初稿，尚待獨立人工複核。"
    ),
    "references": [
        exam_ref(50),
        ref(
            "scikit-learn User Guide－Ordinary Least Squares",
            SKLEARN_LINEAR,
            "LinearRegression.fit 接受 X、y，斜率存於 coef_，截距 w0 存於 intercept_",
        ),
        ref(
            "statsmodels API－OLS",
            STATSMODELS_OLS,
            "OLS(endog, exog) 的參數順序，且模型預設不自動加入截距常數",
        ),
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
