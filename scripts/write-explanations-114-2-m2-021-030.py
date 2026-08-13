"""Write draft explanations for 114-2 intermediate big-data, Q21-Q30.

Usage::

    python scripts/write-explanations-114-2-m2-021-030.py
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
    "bf93f438f7be48d295c1b40a34d79f3d/114年第二梯次中級AI應用規劃師"
    "第二科大數據處理分析與應用(當次試題公告114_20251226000634.pdf"
)
SKLEARN = "https://scikit-learn.org/stable/"
DEFAULT_NOTE = "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。"


def exam_ref(number: int) -> dict:
    return {
        "title": "114 年第二次中級 AI 應用規劃師－第二科 大數據處理分析與應用公告試題",
        "url": EXAM_PDF,
        "locator": f"第 {number} 題題幹、選項與官方答案",
        "checkedAt": CHECKED_AT,
    }


def sklearn_ref(path: str, title: str, locator: str) -> dict:
    return {
        "title": f"scikit-learn－{title}",
        "url": f"{SKLEARN}{path}",
        "locator": locator,
        "checkedAt": CHECKED_AT,
    }


EXPECTED_ANSWER = {
    21: "B", 22: "D", 23: "C", 24: "A", 25: "A",
    26: "C", 27: "D", 28: "A", 29: "D", 30: "C",
}

DRAFTS: dict[int, dict] = {}

DRAFTS[21] = {
    "summary": "正確答案是 B。在比例一致、標註清楚的前提下，把多區域與產品線趨勢整合於同一視圖，可提高單位版面的有效資料密度。",
    "concept": (
        "Tufte 所談的資料密度（Data Density）關注圖形面積中呈現多少有意義的"
        "資料資訊，而不是單純把元素塞滿畫面。高密度視覺化應讓讀者在有限空間"
        "比較多筆數值與模式，同時維持尺度一致、編碼可辨識、標註清楚，避免"
        "裝飾性墨水與混亂遮蔽。多條趨勢共用座標系，能讓主管直接比較區域與"
        "產品線的方向、轉折和差距。"
    ),
    "answerReason": (
        "B 把多個序列整合在相同尺度的單一圖表，並明確保留顏色區分與標註，"
        "使一頁可承載且可比較的資料量提高，最符合資料密度精神。A 分圖會增加"
        "版面與跨圖比較成本；C 移除所有標籤犧牲可讀性；D 的表格適合精確查值，"
        "卻不如趨勢圖快速呈現整體走向。"
    ),
    "optionAnalysis": {
        "A": (
            "小多圖可在線條嚴重重疊時提升可讀性，也不是永遠錯；但每區各用一張"
            "圖會重複座標與標題，並讓主管跨圖搜尋。在題設要求單頁快速掌握整體"
            "且 B 已保證標註清楚時，A 的有效資料密度較低。"
        ),
        "B": (
            "正確。共用一致比例能直接比較多區域趨勢，顏色與清晰標註則維持"
            "辨識度；在同一版面保留較多可比較數據，兼顧密度與可讀性。"
        ),
        "C": (
            "減少不必要網格線可降低視覺雜訊，但『所有』標籤都移除會讓讀者"
            "不知道線條代表何區域、產品與數值尺度。高資料密度不等於刪除理解"
            "資料所必需的編碼說明。"
        ),
        "D": (
            "表格可精確查閱單一數值，適合稽核或明細；但大量區域、產品與日期"
            "形成龐大格網，讀者難在短時間看出斜率、轉折與共通趨勢，未滿足"
            "題目的整體走向需求。"
        ),
    },
    "trap": (
        "資料密度不是『線越多越好』。判斷時要同時看單位空間的資訊量與讀者"
        "是否仍能解碼；若線條重疊到不可辨識，小多圖反而較好。本題 B 額外給了"
        "比例一致與標註清楚，才成為最佳答案。"
    ),
    "references": [
        exam_ref(21),
        {
            "title": "Edward Tufte－The Visual Display of Quantitative Information",
            "url": "https://www.edwardtufte.com/book/the-visual-display-of-quantitative-information/",
            "locator": "第 2 版第 161–168 頁 Data Density and Small Multiples：在合理圖面空間呈現大量可比較數據，同時維持清楚與效率",
            "checkedAt": CHECKED_AT,
        },
    ],
}

DRAFTS[22] = {
    "summary": "正確答案是 D。相關係數矩陣配合熱力圖，可在單一視圖同時呈現四檔股票兩兩關聯的方向與強度。",
    "concept": (
        "相關矩陣把每一對變數的相關係數排成方陣；若採 Pearson 係數，數值由"
        "−1 到 1，正負號表示線性同向或反向，絕對值表示線性關聯強弱。再把"
        "矩陣數值映射為發散色階的熱力圖，研究員可以一次掃描所有股票配對，"
        "快速找出高度正相關、負相關或低相關組合。這是關聯摘要，不代表因果，"
        "也應留意極端值與非線性。"
    ),
    "answerReason": (
        "四檔股票共有六組不重複的兩兩關係，D 能在同一張對稱矩陣中完整呈現，"
        "顏色表示方向與強度，最符合『單一圖表快速比較』。直方圖只看單檔分佈；"
        "散佈圖一次主要看一組；雙軸圖不適合四個序列，且股價水準也不等同每日"
        "報酬率相關性。"
    ),
    "optionAnalysis": {
        "A": (
            "直方圖顯示每檔報酬率的中心、離散與偏態，可比較邊際分佈；它不保留"
            "同一天兩檔股票報酬的配對資訊，因此無法計算或看出共變動方向。"
        ),
        "B": (
            "兩檔散佈圖加趨勢線能細看單一配對的線性形狀、離群點與異方差，"
            "但四檔需多張配對圖。題目要求單一圖表快速總覽全部關聯，矩陣熱力圖"
            "更合適。"
        ),
        "C": (
            "雙軸圖最多通常比較兩種尺度，硬放四檔會造成軸歸屬與視覺解讀混亂；"
            "而且題目要分析每日報酬率，不是股價水準的共同上升或下降。"
        ),
        "D": (
            "正確。相關矩陣列出 A、B、C、D 所有兩兩係數，熱力圖以一致色階"
            "呈現正負與大小，能快速辨認共同波動及可能的分散效果。"
        ),
    },
    "trap": (
        "要比較兩個變數的詳細形狀用散佈圖，要總覽多個變數全部配對用相關矩陣"
        "熱力圖。投資上低相關只表示歷史線性共變較低，不能保證未來或壓力期間"
        "一定維持分散效果。"
    ),
    "references": [
        exam_ref(22),
        {
            "title": "pandas－DataFrame.corr 官方文件",
            "url": "https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.corr.html",
            "locator": "計算欄位間成對相關係數，預設方法為 Pearson，輸出 correlation matrix",
            "checkedAt": CHECKED_AT,
        },
        {
            "title": "seaborn－heatmap 官方文件",
            "url": "https://seaborn.pydata.org/generated/seaborn.heatmap.html",
            "locator": "以顏色編碼矩形資料集，適合呈現二維相關矩陣並可註記數值",
            "checkedAt": CHECKED_AT,
        },
    ],
}

DRAFTS[23] = {
    "summary": "正確答案是 C。p 值 0.08 大於 0.05，且虛無值 100 萬元落在 95% 信賴區間內，因此在 5% 顯著水準無法拒絕虛無假設。",
    "concept": (
        "雙尾單樣本 t 檢定的虛無假設是母體平均數等於 100 萬元，對立假設是"
        "不等於。決策規則是 p ≤ α 才拒絕 H0；此題 0.08 > 0.05，所以證據不足。"
        "同一雙尾檢定下，95% 信賴區間與 α=0.05 的檢定一致：區間包含 100，"
        "表示該虛無值仍與資料相容。『無法拒絕』不等於證明 H0 為真。"
    ),
    "answerReason": (
        "C 同時符合 p 值與信賴區間兩項證據。A 把 0.08 錯看成小於 0.05；B"
        "若改 α=0.10，0.08 反而小於 0.10，會達顯著；D 忽略樣本數、樣本變異"
        "與信賴水準都會影響區間寬度。"
    ),
    "optionAnalysis": {
        "A": (
            "0.08 大於而非小於 0.05，所以在既定顯著水準不能拒絕 H0。不能因"
            "p 值看似接近門檻，就把不顯著結果改寫為顯著。"
        ),
        "B": (
            "把 α 放寬為 0.10 時，p=0.08 ≤ 0.10，依同一檢定會拒絕 H0。改門檻"
            "應有研究前理由，不能看到結果後才挑顯著水準，但此選項的數值判斷"
            "仍明確錯誤。"
        ),
        "C": (
            "正確。100 萬元位於 [95,108] 萬元內，表示在對應的 5% 雙尾檢定下"
            "不能排除母體平均為 100；這與 p=0.08 > 0.05 的結論一致。"
        ),
        "D": (
            "信賴區間寬度除信賴水準外，也受樣本標準差與樣本數影響；其他條件"
            "相同時，樣本越多標準誤通常越小，區間會變窄。"
        ),
    },
    "trap": (
        "先比較 p 與 α 的大小，再用信賴區間交叉檢查。記得『無法拒絕』只表示"
        "目前資料證據不足，不代表兩個平均數已被證明完全相同；也不能在看完"
        "p 值後任意把 α 改成 0.10。"
    ),
    "references": [
        exam_ref(23),
        {
            "title": "SciPy－ttest_1samp 官方文件",
            "url": "https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ttest_1samp.html",
            "locator": "單樣本 t 檢定檢查樣本平均是否等於指定母體平均；結果包含 p-value 與指定信賴水準的 confidence interval",
            "checkedAt": CHECKED_AT,
        },
        {
            "title": "NIST/SEMATECH e-Handbook－Confidence Limits for the Mean",
            "url": "https://www.itl.nist.gov/div898/handbook/eda/section3/eda352.htm",
            "locator": "母體標準差未知時，平均數信賴區間以 t 分佈、樣本標準差與樣本數計算",
            "checkedAt": CHECKED_AT,
        },
    ],
}

DRAFTS[24] = {
    "summary": "正確答案是 A。資料湖可容納多型態原始資料，Spark 或 Ray 能分散式執行一致的預處理，再以管線銜接模型訓練。",
    "concept": (
        "資料湖將文字、影像、表格等結構化與非結構化資料保存在可擴展儲存層，"
        "並保留來源與版本；計算層再依資料型態解析、清理、去重、切分及抽取"
        "特徵。Spark 與 Ray Data 能把大型資料集分割到多個工作節點平行處理，"
        "管線則固定轉換步驟、參數與輸出格式，使重跑與訓練資料一致。效能不只"
        "看吞吐量，也需驗證轉換前後的語意與品質。"
    ),
    "answerReason": (
        "題幹同時要求多樣資料、效率、一致性與串接訓練，A 提供儲存、分散運算"
        "與可重現管線的完整架構。B 單節點擴充受限；C 只處理文字向量，忽略"
        "影像、表格與資料品質流程；D 讓生成模型自行清理缺乏確定性與稽核，"
        "也可能改寫原始事實。"
    ),
    "optionAnalysis": {
        "A": (
            "正確。資料湖承接多模態原始與處理後資料，Spark／Ray 將轉換分散到"
            "多節點，版本化 pipeline 再確保訓練每次採相同清理、切分與特徵規則。"
        ),
        "B": (
            "單節點批次處理架構簡單，資料量不大時可能合適；但大量多型態資料"
            "會受單機 CPU、記憶體與 I/O 上限限制，也形成單點瓶頸，不符合題目"
            "的擴展效率需求。"
        ),
        "C": (
            "文字向量與向量索引適合語意檢索，但訓練仍需 tokenizer、批次組裝、"
            "標籤與品質控制；而題目還有影像與表格，不能把全部資料處理簡化成"
            "文字向量直接餵模型。"
        ),
        "D": (
            "生成模型可輔助分類或提出清理候選，但輸出可能不穩定、遺漏或改寫"
            "內容。若沒有規則驗證、原始資料保留與人工抽查，無法保證一致性，"
            "也不宜作為唯一清理層。"
        ),
    },
    "trap": (
        "資料湖是儲存與治理架構，不會自動保證資料品質；Spark／Ray 是計算層，"
        "也不等於模型訓練本身。A 成立是因為三者組成可擴展且可重現的流程，"
        "仍需 schema、版本、權限與品質檢查。"
    ),
    "references": [
        exam_ref(24),
        {
            "title": "Apache Spark－Overview 官方文件",
            "url": "https://spark.apache.org/docs/latest/",
            "locator": "Spark 為大規模資料分析的多語言引擎，提供 SQL/DataFrame、串流與機器學習等分散式處理能力",
            "checkedAt": CHECKED_AT,
        },
        {
            "title": "Ray Data－Loading and Preprocessing Data 官方文件",
            "url": "https://docs.ray.io/en/latest/data/data.html",
            "locator": "Ray Data 提供分散式資料載入、轉換與串流執行，可串接機器學習訓練工作負載",
            "checkedAt": CHECKED_AT,
        },
    ],
}

DRAFTS[25] = {
    "summary": "正確答案是 A。對數刻度可壓縮右偏長尾的數值跨度，使主要消費群與高額族群的層級差異同時可見。",
    "concept": (
        "IQR 很小、上鬚長且高端有多筆離群值，表示消費金額高度右偏：大多數"
        "交易集中在低範圍，少數高額交易跨越數個數量級。線性刻度會讓中央箱體"
        "被壓扁。對正值使用對數座標或先做 log 轉換，能把倍數差異轉成較均勻"
        "距離，讓低、中、高消費層級均可辨識。若含零值，應另採 log1p 或明確"
        "處理，不能直接取對數。"
    ),
    "answerReason": (
        "A 直接處理長尾尺度問題，又保留高額顧客供行銷分群觀察。B 刪掉高額"
        "資料正好失去重要客群；C 的等距分箱在極端跨度下常讓多數樣本擠在前幾"
        "箱、尾端大量空箱；D 折線圖需要有序時間軸，不能單憑消費分佈產生。"
    ),
    "optionAnalysis": {
        "A": (
            "正確。對數刻度把 100、1,000、10,000 這類倍數變化映射成等距，"
            "壓縮極端高值占用的畫面，同時展開低額集中區，便於辨認不同消費層。"
        ),
        "B": (
            "箱型圖標為離群只代表超過基於 IQR 的統計界線，不等於資料錯誤。"
            "高額交易可能正是高價值會員；應先驗證真實性，不能為了圖形集中就"
            "全部移除。"
        ),
        "C": (
            "等距分箱在 0 到極高金額的長尾範圍內，每箱寬度相同，常使低額"
            "大多數落在同一箱而尾端稀疏。若要分群可考慮分位數箱或業務門檻，"
            "但本題問最能凸顯差異的視覺化。"
        ),
        "D": (
            "折線圖用來呈現時間或其他有序變數上的連續變化；題目只描述單筆"
            "消費金額分佈，沒有時間序列。依任意列順序連線會製造不存在的趨勢。"
        ),
    },
    "trap": (
        "離群值不是錯誤值的同義詞，尤其行銷分析中高額尾端可能很有商業價值。"
        "對數刻度改善顯示但會改變視覺距離，圖上應清楚標示；若有零或負值，"
        "需採適當轉換而非直接套 log。"
    ),
    "references": [
        exam_ref(25),
        {
            "title": "Matplotlib－log scale 官方範例",
            "url": "https://matplotlib.org/stable/gallery/scales/log_demo.html",
            "locator": "以 set_yscale('log') 等方式在對數座標呈現跨數量級資料",
            "checkedAt": CHECKED_AT,
        },
        {
            "title": "NIST/SEMATECH e-Handbook－Box Plot",
            "url": "https://www.itl.nist.gov/div898/handbook/eda/section3/boxplot.htm",
            "locator": "箱型圖呈現位置、尺度、偏態與離群點，可用於比較多組分佈差異",
            "checkedAt": CHECKED_AT,
        },
    ],
}

DRAFTS[26] = {
    "summary": "正確答案是 C。Confidence 50% 表示觀看科幻影集者中有一半也看超級英雄電影，而 Lift 1.8 顯示此比例高於基準。",
    "concept": (
        "對規則 X→Y，support(X∪Y) 是兩者同時出現的比例；confidence=P(Y|X)，"
        "表示出現 X 後也出現 Y 的比例；lift=confidence/P(Y)，把條件比例除以"
        "Y 的整體基準率。Lift>1 表示正向關聯，=1 近似獨立，<1 表示負向關聯。"
        "本題 support=12%、confidence=50%、lift=1.8，因此這不是隨機重疊或"
        "互斥，但是否值得推薦仍需流量、成本與離線／線上驗證。"
    ),
    "answerReason": (
        "C 正確解讀 confidence，且 lift 1.8 佐證觀看科幻者看超級英雄片的機率"
        "是整體基準的 1.8 倍，具有正向傾向。12% 是否商業上過低不能只看數字"
        "斷言；lift>1 與無關恰好相反；同時觀看比例為正也不能推成互相排斥。"
    ),
    "optionAnalysis": {
        "A": (
            "Support 12% 代表每百筆約有 12 筆同時出現，是否足以創造價值要看"
            "總用戶量、推薦收益與成本。不能僅因比例不是多數就宣告毫無商業價值。"
        ),
        "B": (
            "Lift=1 才表示 X 出現與否不改變 Y 的機率；1.8>1 表示正向關聯，"
            "即在 X 群體中 Y 的機率高於整體基準，不是隨機獨立。"
        ),
        "C": (
            "正確。Confidence=P(超級英雄|科幻)=50%，意指科幻觀看者有一半也"
            "看超級英雄；再結合 lift 1.8，可說這是相對基準率明顯較高的傾向。"
        ),
        "D": (
            "互相排斥意味兩者幾乎不能共同出現，support 應接近 0，且 lift 通常"
            "低於 1。本題同時觀看有 12%、lift 又大於 1，證據指向正向而非排斥。"
        ),
    },
    "trap": (
        "Confidence 會受後件 Y 本來就多常見影響，所以一定要搭配 lift。也不要"
        "把關聯寫成因果：規則只能說兩種觀看行為共現，不能證明科幻內容造成"
        "使用者觀看超級英雄電影。"
    ),
    "references": [
        exam_ref(26),
        {
            "title": "mlxtend－Association Rules 官方文件",
            "url": "https://rasbt.github.io/mlxtend/user_guide/frequent_patterns/association_rules/",
            "locator": "定義 support、confidence 與 lift；lift=1 代表獨立，lift>1 表示 antecedent 出現會提高 consequent 的機率",
            "checkedAt": CHECKED_AT,
        },
    ],
}

DRAFTS[27] = {
    "summary": "正確答案是 D。近似分位數以可設定的誤差換取較低時間與記憶體成本，讓大規模或串流資料能快速取得分位摘要。",
    "concept": (
        "精確分位數通常需要排序全部資料或維護大量狀態，對每日上億筆資料成本"
        "很高。近似演算法以摘要結構保留有限資訊，回傳排名落在目標分位附近的"
        "值，並提供相對誤差或排名誤差界線。使用者可依風控需求調整精度—成本"
        "取捨：容許較小誤差即可大幅降低計算與記憶體，適用大批次與即時資料流。"
    ),
    "answerReason": (
        "D 完整描述核心取捨：不要求逐筆全排序的絕對精確，而在可容忍誤差內"
        "快速估計分位值。A 與近似概念相反；B 不必使用機器學習預測位置；C"
        "又錯稱不能用於資料流，許多 quantile sketch 正是為有限記憶體與線上"
        "更新設計。"
    ),
    "optionAnalysis": {
        "A": (
            "完全精確且願意付出較長時間描述的是 exact quantile。近似方法的"
            "價值正是允許明確誤差以減少排序、通訊與記憶體成本。"
        ),
        "B": (
            "近似分位數通常使用可合併的統計摘要、取樣或 sketch 演算法維護"
            "排序資訊，不必先訓練機器學習模型；稱為『預測分位位置』混淆了"
            "quantile regression。"
        ),
        "C": (
            "許多近似摘要可逐筆更新並保持有限大小，適合串流或分散式資料。"
            "結構化欄位確實便於計算數值分位，但技術不只限於離線批次。"
        ),
        "D": (
            "正確。以可設定的 relativeError 或排名誤差換取速度與資源效率，"
            "讓團隊及時監控中位數、尾端分位與異常門檻。"
        ),
    },
    "trap": (
        "近似不等於隨便猜測；成熟演算法會定義可驗證的排名誤差界線。另分清楚"
        "近似分位數與分位數迴歸：前者摘要觀測分佈，後者依特徵預測條件分位數。"
    ),
    "references": [
        exam_ref(27),
        {
            "title": "Apache Spark－DataFrameStatFunctions.approxQuantile 官方文件",
            "url": "https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrameStatFunctions.approxQuantile.html",
            "locator": "以 probabilistic algorithm 計算 approximate quantiles，並以 relativeError 控制目標分位的確定性排名界線；relativeError=0 會付出高成本求精確值",
            "checkedAt": CHECKED_AT,
        },
    ],
}

DRAFTS[28] = {
    "summary": "正確答案是 A。高維空間中距離容易集中，近鄰與遠鄰差異縮小，使固定 ε 難以區分稠密區與稀疏區。",
    "concept": (
        "DBSCAN 以 ε 半徑與 MinPts 判定核心點：若一點的 ε 鄰域內達到足夠"
        "樣本，就從它擴張密度連通群集。高維時資料空間體積快速增加，樣本變得"
        "稀疏，常用距離的最近與最遠差距也可能相對縮小；這是維度災難的一種"
        "表現。原本在低維可分辨密度的 ε 到高維可能讓每點鄰居都不足，於是"
        "全部標成 noise。"
    ),
    "answerReason": (
        "題目特別給出 >500 維，A 直接指出距離集中讓 ε 選擇失去辨識力，是"
        "最可能原因。B 只有在距離度量確實不適合時才成立，題幹沒有此證據；"
        "MinPts 太小反而較容易形成核心點；標準化不會通常把特徵『消失』，"
        "而是調整尺度。"
    ),
    "optionAnalysis": {
        "A": (
            "正確。維度很高時，樣本間距離更難形成清楚近遠差異；若 ε 仍設得"
            "像低維一樣小，各點鄰域內達不到 MinPts，就全部被判為非核心且無法"
            "被其他群集涵蓋。"
        ),
        "B": (
            "距離函數與資料型態不合確實可能造成問題，例如稀疏文字直接用"
            "Euclidean 未必理想；但『使用錯誤』需要額外證據。題幹強調超高維，"
            "更普遍的答案是距離集中。"
        ),
        "C": (
            "MinPts 越小，成為核心點所需鄰居越少，通常會形成更多或較容易形成"
            "群集，而不是使所有點都成為 noise。MinPts 過大才更可能造成此現象。"
        ),
        "D": (
            "標準化把特徵調整到可比較尺度，不會自動刪除特徵或令所有值相同；"
            "只有近乎零變異欄位或錯誤前處理才可能喪失資訊，不能稱為一般原因。"
        ),
    },
    "trap": (
        "『所有點是 noise』直接機制是 ε 鄰域中的點數不足，可能由 ε 太小、"
        "MinPts 太大或高維稀疏造成。本題未把 ε 數值列成選項，卻明示 >500 維，"
        "所以應選距離集中。"
    ),
    "editorialNote": (
        "本站依官方答案 A 撰寫。僅憑『全部為 noise』不能唯一診斷維度災難；"
        "ε 過小、MinPts 過大、不合適距離、極端標準化結果也可能造成相同現象。"
        "A 是題幹強調 >500 維時最合理的首要原因，實務仍應檢查 k-distance 圖、"
        "尺度與距離度量。查核日期 2026-08-12。"
    ),
    "references": [
        exam_ref(28),
        sklearn_ref(
            "modules/clustering.html#dbscan",
            "Clustering－DBSCAN",
            "DBSCAN 將核心樣本的高密度區擴張為群集，eps 控制鄰域距離、min_samples 控制核心點的鄰域樣本數",
        ),
        sklearn_ref(
            "modules/neighbors.html#nearest-neighbor-algorithms",
            "Nearest Neighbors－algorithm selection",
            "Curse of dimensionality：維度增加使資料在空間中更稀疏，近鄰方法需要更多資料且距離方法可能退化",
        ),
    ],
}

DRAFTS[29] = {
    "summary": "正確答案是 D。PCA 依變異量找主成分，未先標準化時，大尺度的交易金額會支配共變異結構。",
    "concept": (
        "PCA 在置中資料上尋找變異最大的正交方向。若直接使用原始單位，變數的"
        "方差會隨尺度平方放大：金額約 10⁵，遠大於次數 10¹與年齡 10²，PC1"
        "自然幾乎沿金額方向。當三個欄位單位不同且沒有業務理由讓某單位支配時，"
        "應先做 z-score 標準化，使各欄平均為 0、標準差為 1，再以相對變動"
        "決定主成分。標準化參數只能在訓練資料擬合，以免洩漏。"
    ),
    "answerReason": (
        "D 直接修正量級差異造成的 PCA 偏向。A 把測量單位導致的變異誤當成"
        "必然重要性；B 的特徵選擇決定保留欄位，但不會自動把保留欄位變成"
        "同尺度；C 未經業務判斷刪除交易金額會損失可能非常重要的風險訊號。"
    ),
    "optionAnalysis": {
        "A": (
            "若金額變異大是業務上刻意要賦予較高權重，原尺度 PCA 才可能合理；"
            "但本題三欄單位不同、量級懸殊，PC1 被金額支配很可能只是單位選擇"
            "的人工結果，不能直接稱為正常重要性。"
        ),
        "B": (
            "特徵選擇會刪除部分變數，判準可能是標籤關聯、統計檢定或模型重要度；"
            "它不會自動將 10⁵、10²、10¹ 的量級對齊，尺度問題仍需前處理。"
        ),
        "C": (
            "交易金額可能是風險模型的重要特徵，僅因尺度大就刪除會丟失資訊。"
            "應先把單位尺度標準化，再看 PCA 負荷量、解釋變異與下游效能決定"
            "是否保留。"
        ),
        "D": (
            "正確。z-score 標準化讓各特徵以自身標準差為單位，避免新台幣、"
            "次／月與歲的數值量級直接決定共變異矩陣，讓 PCA 比較相對變化。"
        ),
    },
    "trap": (
        "PCA 只會自動置中，不代表所有實作會自動縮放到單位方差。標準化也不是"
        "一律必要：同單位且絕對變異本來就有意義時可保留原尺度；本題因單位與"
        "量級明顯不同，才應標準化。"
    ),
    "references": [
        exam_ref(29),
        sklearn_ref(
            "auto_examples/preprocessing/plot_scaling_importance.html",
            "Importance of Feature Scaling",
            "PCA 段落：未縮放時，尺度較大的特徵會主導主成分；先以 StandardScaler 縮放會使各特徵貢獻更平衡",
        ),
        sklearn_ref(
            "modules/generated/sklearn.decomposition.PCA.html",
            "PCA",
            "PCA 執行前會置中但不會自動逐特徵縮放，components 依 explained variance 排序",
        ),
    ],
}

DRAFTS[30] = {
    "summary": "正確答案是 C。皮爾森相關係數是經尺度標準化的共變異量，可直接表示兩個連續變數線性關係的方向與強度。",
    "concept": (
        "Pearson r = cov(X,Y)/(σXσY)，將共變異數除以兩變數標準差，因此沒有"
        "單位，範圍為 −1 到 1。正值表示廣告預算高時銷售通常也高，負值表示"
        "反向，絕對值越接近 1 代表線性關係越強。題幹已確認散佈圖近似線性且"
        "無明顯離群值，正適合 Pearson。相關不等於因果，預算與銷售仍可能同受"
        "季節、促銷或市場需求影響。"
    ),
    "answerReason": (
        "C 同時提供可比較的強度與正負方向。Covariance 雖有正負方向，但大小受"
        "新台幣單位與尺度影響，無固定界線；RMSE 與 MAE 都需要一組預測值與"
        "真值來衡量模型誤差，並非兩個觀測變數的對稱關聯指標。"
    ),
    "optionAnalysis": {
        "A": (
            "RMSE 將預測殘差平方平均後開根號，適合評估銷售預測模型，單位與"
            "銷售金額相同。題目沒有提供預測值，也不是要衡量模型錯誤，因此"
            "不適用。"
        ),
        "B": (
            "共變異數正負可表示同向或反向，但大小取決於兩變數單位；若把預算"
            "從元改成萬元，數值就改變，無法以固定尺度直接說關聯有多強。"
        ),
        "C": (
            "正確。Pearson 把 covariance 以兩個標準差正規化，得到 −1 到 1 的"
            "無單位係數，適合題示的兩個連續變數與明顯線性、無離群情境。"
        ),
        "D": (
            "MAE 是預測值與真值絕對差的平均，對大誤差的敏感度低於 RMSE；"
            "它仍屬模型誤差指標，不能描述廣告與銷售之間的關聯方向。"
        ),
    },
    "trap": (
        "Covariance 與 Pearson 都有方向，但只有 Pearson 經標準化，能用固定"
        "範圍比較強度。若關係單調但非線性或有嚴重離群值，Spearman 可能更合適；"
        "本題已排除這些情況。"
    ),
    "references": [
        exam_ref(30),
        {
            "title": "SciPy－pearsonr 官方文件",
            "url": "https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.pearsonr.html",
            "locator": "Pearson correlation coefficient 衡量兩資料集的線性關係，範圍 [-1,1]，並列出 r=Σ(x-mx)(y-my)/sqrt(Σ(x-mx)²Σ(y-my)²) 公式",
            "checkedAt": CHECKED_AT,
        },
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
