"""Write explanation drafts for 115-1 intermediate subject two, Q01-Q10.

The script validates each official answer before writing, refuses to overwrite
reviewed content, and leaves every generated explanation in ``draft`` status.

Usage::

    python scripts/write-explanations-115-1-m2-001-010.py
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUESTIONS = ROOT / "app" / "data" / "questions.json"
SOURCE_ID = "aiap-115-intermediate-1-big-data"
AUTHOR = "Codex（AI 輔助初稿）"
AUTHORED_AT = "2026-08-12"
CHECKED_AT = "2026-08-12"

EXAM_PDF = (
    "https://www.ipas.org.tw/api/proxy/uploads/certification_resource/"
    "bf93f438f7be48d295c1b40a34d79f3d/"
    "115年第一次中級AI應用規劃師_第二科_大數據處理分析與應用_"
    "公告試題_20260615003417.pdf"
)
NIST_BOX_PLOT = "https://itl.nist.gov/div898/handbook/eda/section3/boxplot.htm"
SKLEARN_TREE = "https://scikit-learn.org/stable/modules/tree.html#classification-criteria"
SCIPY_POISSON = "https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.poisson.html"
SCIPY_NBINOM = "https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.nbinom.html"
NIST_ANOVA = "https://www.itl.nist.gov/div898/handbook/ppc/section2/ppc231.htm"
SCIPY_ZSCORE = "https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.zscore.html"
NIST_TESTS = "https://www.itl.nist.gov/div898/handbook/prc/section1/prc13.htm"
NIST_PVALUES = "https://itl.nist.gov/div898/handbook/prc/section1/prc131.htm"
SCIPY_TTEST_REL = "https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ttest_rel.html"
SKLEARN_LEAKAGE = "https://scikit-learn.org/stable/common_pitfalls.html#data-leakage"
SKLEARN_MI = (
    "https://scikit-learn.org/stable/modules/generated/"
    "sklearn.feature_selection.mutual_info_classif.html"
)

DEFAULT_NOTE = "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。"


def ref(title: str, url: str, locator: str) -> dict:
    return {"title": title, "url": url, "locator": locator, "checkedAt": CHECKED_AT}


def exam_ref(number: int) -> dict:
    return ref(
        "115 年第一次中級 AI 應用規劃師－大數據處理分析與應用公告試題",
        EXAM_PDF,
        f"第 {number} 題題幹、附圖、選項與官方答案",
    )


EXPECTED_ANSWER = {
    1: "A", 2: "A", 3: "B", 4: "A", 5: "A",
    6: "D", 7: "B", 8: "D", 9: "B", 10: "B",
}

DRAFTS: dict[int, dict] = {}

DRAFTS[1] = {
    "summary": "正確答案是 A。短盒表示中間 50% 房價集中，長鬚表示中央區外的分散範圍較大；中位數靠近盒子下方則顯示上半部較分散，呈現右偏跡象。",
    "concept": (
        "盒鬚圖以第一四分位數 Q1、中位數與第三四分位數 Q3 描述資料。盒長是四分位距"
        "IQR=Q3−Q1，代表中間 50% 資料的散布；鬚與另行標出的點則呈現中央區以外的尾端"
        "與可能離群值。若中位數靠近 Q1，表示從中位數到 Q3 的上半盒較長，通常可視為高值"
        "方向較分散的右偏跡象。不過盒鬚圖是摘要，偏態最好仍搭配原始資料或直方圖確認。"
    ),
    "answerReason": (
        "A 同時正確連結城市 A 的短盒與長鬚，以及城市 C 中位數偏下的幾何特徵。城市 A 的"
        "中央房價集中，但尾端範圍相對較長；城市 C 在高房價方向的盒內距離較長，符合右偏"
        "判讀。其餘選項把長鬚說成離群少，或把城市 C 的偏態方向顛倒。"
    ),
    "optionAnalysis": {
        "A": (
            "正確。短盒代表 IQR 小，也就是中間 50% 房價聚集；長鬚顯示中央區之外仍延伸到"
            "較遠端值。城市 C 的中位數靠近盒子下緣，使上半盒較長，表示高值側散布較大，"
            "可判讀為右偏跡象。"
        ),
        "B": (
            "長鬚不能支持『離群值少』，反而表示四分位區間之外的資料範圍較長；是否為離群點"
            "還要依作圖規則看是否超過鬚或另有符號。中位數偏向下四分位代表高值側較長，"
            "方向也不是左偏。"
        ),
        "C": (
            "城市 B 的長盒確實代表 IQR 較大，也就是中間 50% 房價變異較大；但選項後半把"
            "城市 C 說成左偏。城市 C 上半盒較長，顯示右側或高值方向延伸較多，因此整項"
            "不能成立。"
        ),
        "D": (
            "直方圖能補充峰形與細節，確實適合確認偏態；但盒內中位數相對位置及兩側鬚長"
            "本來就能提供不對稱線索。說盒鬚圖完全無法判斷偏態過於絕對，不符合題目給定的"
            "圖形判讀原則。"
        ),
    },
    "trap": (
        "盒『長』看 IQR，鬚『長』看中央區外的延伸，不要混為一談。中位數偏下是高值側較長，"
        "所以是右偏跡象；但僅憑摘要圖不宜把偏態寫成無條件的確證。"
    ),
    "editorialNote": (
        "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。不同軟體對鬚可採"
        "最小／最大值或 1.5×IQR 規則；『長鬚』可表示尾端延伸，但不必然代表已有另標離群點。"
    ),
    "references": [
        exam_ref(1),
        ref(
            "NIST/SEMATECH e-Handbook－Box Plot",
            NIST_BOX_PLOT,
            "盒子表示中間 50%、中位數位置及極端點，並可用多個盒鬚圖比較群組",
        ),
    ],
}

DRAFTS[2] = {
    "summary": "正確答案是 A。公式中的 pᵢ 是節點內第 i 類樣本所占比例，不是樣本數；若直接代入計數，便不再是機率平方和。",
    "concept": (
        "官方附圖公式為 G = 1 − Σ(i=1…k) pᵢ²。這裡 k 是節點內的類別數，pᵢ=nᵢ/n 是"
        "第 i 類樣本比例，各類比例總和為 1。Gini 不純度可理解為按節點類別分布隨機指派"
        "標籤時產生錯分的程度：節點只有一類時平方和為 1、G=0；類別越均勻混合，不純度"
        "越高。決策樹比較候選分裂前後的加權不純度下降，以選擇較能分開類別的切分。"
    ),
    "answerReason": (
        "A 把 pᵢ 誤稱為樣本數並要求直接代入，是題目所問的不正確敘述。若某類有 nᵢ 筆，"
        "必須先除以節點總數 n 得到 pᵢ。B 正確定義類別數 k，C 正確描述混雜程度，D 也可由"
        "單一類別 p=1 直接算得 G=0。"
    ),
    "optionAnalysis": {
        "A": (
            "不正確，故為答案。pᵢ 是比例 nᵢ/n，而非原始樣本數 nᵢ；例如兩類各 5 筆時應代入"
            "0.5 與 0.5，得到 G=0.5。若直接代入 5，會得到負值，失去不純度的機率意義。"
        ),
        "B": (
            "k 表示此分類問題在節點中考慮的類別數，求和會逐類累加 pᵢ²。若某類在節點中"
            "沒有樣本，其比例為 0，不影響平方和；因此此敘述符合官方附圖的上下限記號。"
        ),
        "C": (
            "Gini 不純度用來描述節點類別是否混雜。兩類節點從 100%／0% 走向 50%／50% 時，"
            "G 由 0 增至 0.5；因此在同一類別數下，數值越高通常代表類別分布越混合。"
        ),
        "D": (
            "節點完全純淨時，某一類 p=1、其他類 p=0，平方和為 1，所以 G=1−1=0。這正是"
            "決策樹希望藉分裂達成的狀態，因此此敘述正確。"
        ),
    },
    "trap": (
        "p 常被誤看成筆數，但機率公式中的 pᵢ 必須介於 0 與 1，且總和為 1。另要看清題目問"
        "『不正確』；Gini 越低越純，並非數值越高代表分裂品質越好。"
    ),
    "editorialNote": (
        "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。已於 2026-08-12"
        "目視官方 PDF 第 1 頁，附圖確為 G = 1 − Σ(i=1…k) pᵢ²；資料庫現有本機 PNG 為全黑影像，"
        "需另行修復素材後再確認前端顯示。"
    ),
    "references": [
        exam_ref(2),
        ref(
            "scikit-learn User Guide－Decision tree classification criteria",
            SKLEARN_TREE,
            "Gini 公式：p_mk 為節點 m 中第 k 類觀測值的比例，純節點不純度為 0",
        ),
    ],
}

DRAFTS[3] = {
    "summary": "正確答案是 B。固定時間內獨立事件的計數可先用卜瓦松分布；若變異數明顯大於平均數，負二項分布可加入額外離散程度處理過度離散。",
    "concept": (
        "卜瓦松分布適合描述固定區間內事件次數，在獨立、發生率穩定等理想假設下，其平均數"
        "與變異數都等於參數 λ。實務來電量常因時段、活動或未觀測群組差異而出現過度離散，"
        "即變異數大於平均數。負二項分布可視為讓卜瓦松發生率本身具有異質性，增加離散參數，"
        "因此比硬套 equidispersion 的 Poisson 更能容納額外變異。"
    ),
    "answerReason": (
        "題目明確給出每小時事件、彼此獨立及固定發生率，正好對應卜瓦松計數模型；後續又"
        "指定變異數大於平均數，這是過度離散訊號，負二項分布是標準替代方案。增加樣本量"
        "只讓估計更精確，不會改變資料生成過程的變異結構。"
    ),
    "optionAnalysis": {
        "A": (
            "常態分布可在計數很大時作近似，但它是連續且可取負值，沒有直接表達獨立事件的"
            "計數機制。t 分布主要處理小樣本平均推論或厚尾連續誤差，不能專門修正計數資料"
            "變異數大於平均數。"
        ),
        "B": (
            "正確。Poisson 以 λ 同時決定平均與變異數，適合題設的穩定獨立事件；觀察到"
            "overdispersion 後，Negative Binomial 透過額外參數放寬均值等於變異數的限制，"
            "可更合理描述來電量。"
        ),
        "C": (
            "增加樣本數能更精確估計平均與變異數，卻不會讓真實過度離散自動消失。若發生率"
            "受未觀測因素改變，Poisson 的變異假設仍錯置，標準誤與預測區間可能被低估，"
            "應改模型或加入解釋變數。"
        ),
        "D": (
            "二項分布描述固定試驗次數中成功幾次，需要明確 n 與成功機率 p；客服來電沒有"
            "固定的可來電總人次，較符合到達計數。Poisson 本身又具均值等於變異數的限制，"
            "也不是過度離散時的調整方向。"
        ),
    },
    "trap": (
        "辨識三個關鍵：固定區間、事件計數、獨立且率穩定，先想到 Poisson；再比較平均與"
        "變異數。變異較大是模型假設問題，不是單純『資料不夠多』。"
    ),
    "references": [
        exam_ref(3),
        ref(
            "SciPy API－scipy.stats.poisson",
            SCIPY_POISSON,
            "Poisson 機率質量函數及參數 μ 的官方定義",
        ),
        ref(
            "SciPy API－scipy.stats.nbinom",
            SCIPY_NBINOM,
            "Negative Binomial 機率質量函數，以及以均值與變異數參數化的關係",
        ),
    ],
}

DRAFTS[4] = {
    "summary": "正確答案是 A。三組獨立、近似常態且變異數相近的連續損失，要先檢定三個母體平均數是否相同，適合使用單因子變異數分析。",
    "concept": (
        "One-Way ANOVA 用一個類別因子比較三組以上平均數，虛無假說是所有組別母體平均相等。"
        "它以組間變異相對於組內變異形成 F 統計量，一次進行整體檢定，避免先做多次未調整"
        "t 檢定而使家族型第一類錯誤率膨脹。前提包括觀測獨立、殘差近似常態與變異數同質；"
        "若整體顯著，再用 Tukey 等多重比較找出差異組別。"
    ),
    "answerReason": (
        "學習率是單一因子、共有三個水準，反應值是連續的驗證損失；題目又明示三組獨立、"
        "近似常態及變異數相近，完整吻合 one-way ANOVA 的典型條件。獨立 t 檢定一次只能"
        "比較兩組，反覆執行正是題目要避免的錯誤率問題。"
    ),
    "optionAnalysis": {
        "A": (
            "正確。單因子 ANOVA 用一個 F 檢定同時檢查三種學習率的平均損失是否全相同，"
            "利用每組 10 次訓練估計組內變異，並比較學習率造成的組間變異，符合題設假定。"
        ),
        "B": (
            "獨立樣本 t 檢定適合比較兩個獨立群體平均數。三組若逐對做三次未校正 t 檢定，"
            "至少一次偽陽性的整體機率會高於單次 α；除非另做多重比較校正，否則不符合題意。"
        ),
        "C": (
            "卡方獨立性檢定用列聯表的類別次數判斷兩個類別變數是否關聯，不是比較連續損失"
            "的三組平均值。把損失強制分箱還會丟失數值資訊，也不利用題目給定的常態假設。"
        ),
        "D": (
            "Wilcoxon 符號等級檢定是兩組配對或單樣本差值的非參數方法，適合相同個體前後"
            "或成對觀測不符合常態時使用。本題是三組彼此獨立的樣本，資料結構與檢定目標"
            "皆不相符。"
        ),
    },
    "trap": (
        "ANOVA 顯著只表示至少一組平均不同，不會告訴你是哪一組；要再做有校正的事後比較。"
        "另外，若三種學習率共用完全相同的種子形成配對，設計會不同，但題目已明定彼此獨立。"
    ),
    "references": [
        exam_ref(4),
        ref(
            "NIST/SEMATECH e-Handbook－One-Way ANOVA",
            NIST_ANOVA,
            "單一因子多水準、每水準多筆觀測的模型、假設與 F 檢定用途",
        ),
    ],
}

DRAFTS[5] = {
    "summary": "正確答案是 A。Z-score 為 -2 表示該觀測值比歷史平均值低 2 個歷史標準差，且依題設 |Z|≥2 應觸發警示。",
    "concept": (
        "標準分數定義為 z=(x−μ)/σ，將原始值與基準平均數的距離換算成標準差單位。正號代表"
        "高於平均、負號代表低於平均，絕對值表示距離大小；z=0 才等於平均。若基準近似常態，"
        "z 可輔助辨識尾端觀測，但警示不等於已證明資料漂移或資料錯誤，還需檢查時間窗口、"
        "多筆分布與業務原因。題設門檻含等號，所以 -2 已達警示條件。"
    ),
    "answerReason": (
        "把 z=-2 代回關係式可得 x=μ−2σ，正好是低於歷史平均兩個標準差，因此 A 正確。"
        "B 把方向顛倒，C 應對應 z=0，D 則誤以為負值代表落在分布之外；常態分布本身在平均"
        "以下仍有完整機率範圍。"
    ),
    "optionAnalysis": {
        "A": (
            "正確。z=-2 的負號表示觀測值位於平均以下，數值 2 表示距離為兩個標準差。由於"
            "系統規則是 |Z|≥2，絕對值恰為 2，這筆資料應被標記供後續調查。"
        ),
        "B": (
            "高於平均兩個標準差會得到 z=+2，而非 -2。標準化除以正的標準差不會改變"
            "x−μ 的符號，因此只要看正負號即可判斷觀測值位於基準平均的哪一側。"
        ),
        "C": (
            "觀測值等於歷史平均時，分子 x−μ=0，所以 z=0。z=-2 顯示它與平均有明確距離；"
            "但這是相對所選歷史基準的描述，基準若已過時，警示解讀也需調整。"
        ),
        "D": (
            "負 Z-score 只是低於平均，並未落在常態分布之外；常態分布在整條實數軸都有密度。"
            "數值位於尾端可能較少見，但仍可用常態模型描述，是否異常由預設門檻與情境判斷。"
        ),
    },
    "trap": (
        "負號看方向、絕對值看距離。門檻寫的是 |Z|≥2，因此 +2 與 -2 都會告警；告警只是一筆"
        "異常訊號，不能單憑單點就斷言整個輸入分布已漂移。"
    ),
    "references": [
        exam_ref(5),
        ref(
            "SciPy API－scipy.stats.zscore",
            SCIPY_ZSCORE,
            "Z-score 以相對於樣本平均值與標準差計算的官方 API 定義",
        ),
    ],
}

DRAFTS[6] = {
    "summary": "正確答案是 D。未完全答對而未達顯著，只能說現有證據不足以拒絕『隨機猜測』，不能接受並確認女士沒有辨別能力。",
    "concept": (
        "假說檢定先假設 H₀ 成立，再計算觀察結果在 H₀ 下有多極端。p<α 時拒絕 H₀；p≥α 時"
        "應表述為『不拒絕 H₀』，因為結果可能來自 H₀ 為真，也可能是樣本太少、檢定力不足而"
        "漏掉真實能力。女士品茶的設計要求從 8 杯中選出 4 杯，隨機恰好全選對的組合機率是"
        "1/C(8,4)=1/70≈0.014，因此完全答對在 α=0.05 下可拒絕 H₀。"
    ),
    "answerReason": (
        "D 把『沒有足夠證據拒絕』錯寫成『確認沒有能力』，忽略型二錯誤與檢定力，故是不正確"
        "敘述。A 正確設定能力主張，B 的精確組合機率計算正確，C 也正確描述 p 值小於 α 時"
        "拒絕 H₀ 並支持對立假說。"
    ),
    "optionAnalysis": {
        "A": (
            "正確。H₀ 以隨機猜測作為可計算的基準，H₁ 是辨別能力使答對情形比隨機更極端。"
            "這種設定讓實驗可在 H₀ 下列舉所有選取 4 杯的等可能組合。"
        ),
        "B": (
            "正確。隨機從 8 杯選 4 杯共有 C(8,4)=70 種等可能組合，只有一種完全符合真實"
            "配置，所以單尾 p 值為 1/70≈0.0143，小於 0.05。"
        ),
        "C": (
            "正確。完全答對得到 p<α，代表在隨機猜測假設下如此極端的結果很少見，因此拒絕"
            "H₀；『支持有能力』是統計證據措辭，不代表以一次實驗證明能力絕對無誤。"
        ),
        "D": (
            "不正確，故為答案。未完全答對若未進入拒絕域，只能不拒絕 H₀；8 杯的小型實驗"
            "檢定力有限，真正有部分辨別能力的人仍可能沒全答對，不能藉此確認她毫無能力。"
        ),
    },
    "trap": (
        "『不拒絕』不等於『接受並證實』，這是最常見陷阱。α 控制的是 H₀ 為真時誤拒絕的"
        "機率；證據不足也可能是型二錯誤，而非 H₀ 已被證明。"
    ),
    "references": [
        exam_ref(6),
        ref(
            "NIST/SEMATECH e-Handbook－What are statistical tests?",
            NIST_TESTS,
            "H₀、Hₐ、顯著水準 α 與型二錯誤 β 的定義及檢定結論脈絡",
        ),
        ref(
            "NIST/SEMATECH e-Handbook－Critical values and p values",
            NIST_PVALUES,
            "p 值是在 H₀ 為真時得到至少同樣極端統計量的機率；p 小於預設 α 時拒絕 H₀",
        ),
    ],
}

DRAFTS[7] = {
    "summary": "正確答案是 B。同一批 40 名患者在介入前後各量一次，觀測值一一配對，應對每人的血壓差值做成對樣本 t 檢定。",
    "concept": (
        "成對樣本 t 檢定把每位受試者的後測減前測，檢定這 40 個個人差值的母體平均是否為 0。"
        "因為同一人的兩次血壓通常相關，配對分析能消除部分個體基準差異；其常態假設主要針對"
        "差值分布，而不是要求前測與後測各自完全獨立。若差值嚴重偏態或有極端值，可評估"
        "Wilcoxon signed-rank 等替代方法，但題目已給近似常態條件。"
    ),
    "answerReason": (
        "研究問題比較同一人導入前後的收縮壓，配對身分是決定檢定方法的關鍵，B 直接利用"
        "每人的前後差值。獨立 t 檢定會錯把兩次觀測當不同病患；ANOVA 沒必要處理僅兩個"
        "配對時間點；Wilcoxon 則是常態差值假設不合時的非參數候選。"
    ),
    "optionAnalysis": {
        "A": (
            "獨立樣本 t 檢定適合兩組由不同個體構成、組間無配對關係的平均比較。本題前測與"
            "後測來自相同患者，兩值相關；忽略配對會錯估標準誤，也沒有利用個體作為自己的"
            "對照。"
        ),
        "B": (
            "正確。先計算每位患者的後測減前測差值，再檢定平均差是否為 0，直接回答 AI 推薦"
            "調整前後是否有顯著變化。實務還應報告平均差、信賴區間與效果量，不只看 p 值。"
        ),
        "C": (
            "單因子 ANOVA 常用於三個以上獨立水準平均比較；只有兩個時間點時，成對 t 檢定"
            "已能直接回答問題。一般 one-way ANOVA 若忽略重複量測結構，也會違反觀測獨立假設。"
        ),
        "D": (
            "Wilcoxon signed-rank 同樣處理成對差值，但屬非參數秩次方法，適合差值常態假設"
            "不合理且分布條件允許時。本題已明示資料近似常態，因此參數式 paired t-test"
            "是優先選擇。"
        ),
    },
    "trap": (
        "判斷重點是『同一批患者』，不是只有看組數。成對 t 檢定的分析單位是個人差值；"
        "近似常態也應檢查差值，而非把前後兩欄分開檢查後就結束。"
    ),
    "references": [
        exam_ref(7),
        ref(
            "SciPy API－scipy.stats.ttest_rel",
            SCIPY_TTEST_REL,
            "對兩個相關或重複樣本檢定平均差為 0 的官方定義",
        ),
    ],
}

DRAFTS[8] = {
    "summary": "正確答案是 D。依附圖公式計算 Z=(40−36)/(16/√9)=4/(16/3)=0.75；0.75 未超過右尾臨界值 1.645，因此不拒絕虛無假說。",
    "concept": (
        "母體標準差 σ 已知時，單一平均數的 Z 統計量是 Z=(x̄−μ₀)/(σ/√n)，分母為樣本平均"
        "的標準誤。右尾檢定 H₁:μ>μ₀ 只在 Z 大於臨界值時拒絕 H₀。此題標準誤為 16/3≈5.333，"
        "樣本平均只高出 4 分鐘，所以 Z=0.75；在 H₀ 下並不落入 α=0.05 的右尾拒絕域。"
    ),
    "answerReason": (
        "逐步代入官方附圖公式：√9=3，σ/√n=16/3，分子 40−36=4，故 Z=4÷(16/3)=0.75。"
        "右尾拒絕條件是 Z≥1.645，而 0.75<1.645，所以證據不足以認定平均外送時間超過 36"
        "分鐘，D 的數值與結論都正確。"
    ),
    "optionAnalysis": {
        "A": (
            "0.08 不是依附圖標準誤公式所得結果，且即使 Z=0.08 也遠小於右尾臨界值 1.645，"
            "不可能據此拒絕 H₀。此選項的計算與判定兩部分都不正確。"
        ),
        "B": (
            "『不拒絕』的方向雖與小 Z 值一致，但 Z 的計算錯誤。分母不是 σ×√n，也不是以"
            "平均差除以其他總量，而是 16/√9，因此正確統計量為 0.75。"
        ),
        "C": (
            "Z≈0.75 的計算正確，但右尾檢定只有超過 1.645 才進入拒絕域。0.75 落在非拒絕區，"
            "不能因樣本平均 40 大於 36 就跳過抽樣變異直接拒絕 H₀。"
        ),
        "D": (
            "正確。Z≈0.75 且小於 1.645，因此不拒絕 H₀。這只表示九筆樣本提供的證據不足，"
            "並不是證明母體平均必然等於或小於 36 分鐘。"
        ),
    },
    "trap": (
        "分母是平均數的標準誤 σ/√n，不是母體標準差 σ，也不是 σ√n。比較臨界值時還要看"
        "方向：右尾才用 Z 是否大於正的 1.645。"
    ),
    "editorialNote": (
        "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。已於 2026-08-12"
        "目視官方 PDF 第 2 頁，附圖公式確為 Z=(x̄−μ₀)/(σ/√n)；資料庫現有本機 PNG 為全黑影像，"
        "需另行修復素材後再確認前端顯示。"
    ),
    "references": [
        exam_ref(8),
        ref(
            "NIST/SEMATECH e-Handbook－Critical values and p values",
            NIST_PVALUES,
            "臨界值定義拒絕域；檢定統計量進入該區域時才拒絕 H₀",
        ),
    ],
}

DRAFTS[9] = {
    "summary": "正確答案是 B。在其他條件不變時，把 α 從 0.05 降到 0.01 會縮小拒絕域，降低 H₀ 為真卻被誤拒絕的型一錯誤機率。",
    "concept": (
        "顯著水準 α 是檢定設計容許的型一錯誤率，也就是無效藥物其實沒有療效時，仍誤拒絕"
        "H₀ 並宣稱有效的機率上限。降低 α 會要求更極端的檢定統計量或更小的 p 值才算顯著，"
        "直接減少偽陽性。若樣本數與真實效果固定，門檻變嚴通常會提高型二錯誤 β、降低 power；"
        "若想同時維持功效，往往需另行增加樣本，但那不是調整 α 自動造成的結果。"
    ),
    "answerReason": (
        "B 正確描述 α 的定義與降低後的直接影響：無效藥被誤判有效的風險下降。A 把型二錯誤"
        "方向說反，C 把可能採取的樣本數規劃誤當自動效果，D 則混淆統計決策門檻與數值計算"
        "精度。"
    ),
    "optionAnalysis": {
        "A": (
            "在樣本數與效果固定時，降低 α 使拒絕 H₀ 更困難，通常是 β 上升而非下降，也就是"
            "更可能漏掉真正有效藥物。要降低 β 可增加樣本、提高量測精度或接受較寬鬆 α，"
            "需在風險間權衡。"
        ),
        "B": (
            "正確。α 就是 H₀ 為真時誤拒絕的機率；從 0.05 降至 0.01，代表要求更強證據才"
            "宣稱療效，因而直接降低偽陽性及無效候選藥進入昂貴後續試驗的風險。"
        ),
        "C": (
            "更嚴格 α 下，研究者可能經 power analysis 規劃更大樣本以維持功效，但修改 α"
            "這個設定本身不會自動招募更多受試者。樣本數是另一項研究設計決策，不能視為"
            "直接統計效果。"
        ),
        "D": (
            "α 決定把哪些統計量視為拒絕域，不改變浮點運算、演算法誤差或 p 值估計精度。"
            "數值精度取決於資料品質、樣本與計算方法；把門檻設成 0.01 不會讓計算本身更準。"
        ),
    },
    "trap": (
        "降低 α 是降低型一錯誤，不是同時降低所有錯誤。在固定樣本下，α 與 β 通常有取捨；"
        "增加樣本可改善功效，但必須另外執行，並非 α 改變後自然發生。"
    ),
    "references": [
        exam_ref(9),
        ref(
            "NIST/SEMATECH e-Handbook－Quantitative Techniques",
            "https://www.itl.nist.gov/div898/handbook/eda/section3/eda35.htm",
            "顯著水準 α、型一錯誤、型二錯誤 β 與檢定力 1−β 的定義",
        ),
    ],
}

DRAFTS[10] = {
    "summary": "正確答案是 B。任何以全體資料決定特徵的步驟都讓測試集資訊滲入建模流程，破壞最終泛化評估；而線性相關係數也看不到一般非線性關係。",
    "concept": (
        "測試集的角色是模擬從未看過的資料，只能在模型、前處理與超參數全數確定後做一次"
        "最終評估。特徵移除、標準化及依模型重要性篩選都是需要從資料學得的步驟，必須只在"
        "訓練資料或每個交叉驗證訓練折內 fit，再原樣套到驗證／測試資料。Pearson correlation"
        "只量線性關係；零相關仍可能存在曲線或其他非線性依賴，可用互資訊、模型式方法或"
        "領域分析補充，但也要留在管線內驗證。"
    ),
    "answerReason": (
        "第一步明說在含測試集的全體資料計算並選特徵，已用未來評估資料影響模型設計，所得"
        "0.81 AUC 不再是獨立的泛化估計。B 同時指出 Pearson 線性相關的能力邊界。正確做法"
        "是重建未觸碰測試集，將所有篩選封裝在訓練／交叉驗證流程後重新評估。"
    ),
    "optionAnalysis": {
        "A": (
            "調整相關門檻可改變保留特徵數，但主要缺陷不是門檻高低，而是門檻與移除清單由"
            "含測試集的資料算出。即使方法不看標籤，仍讓測試分布參與建模決策，破壞測試集"
            "的隔離用途。"
        ),
        "B": (
            "正確。特徵篩選器應只在訓練折 fit，不能用測試集統計量；Pearson 相關又只反映"
            "線性共同變動，可能漏掉 U 形、週期或交互作用。兩項限制都使目前流程的 0.81"
            "不能直接當部署依據。"
        ),
        "C": (
            "標準化參數也只能由訓練集估計，再套用到測試集，不能『重新對測試集』自行 fit，"
            "否則同樣使用測試資訊。是否需要標準化取決於模型；樹模型通常不依賴尺度，且這"
            "不是題目流程最核心的錯誤。"
        ),
        "D": (
            "測試 AUC 上升可能正是測試資訊滲入選擇流程造成的樂觀結果，不能證明過擬合已解決。"
            "部署前應用乾淨保留集或外部資料重評，並檢查校準、穩定性、資料漂移及受傷標籤"
            "定義等需求。"
        ),
    },
    "trap": (
        "資料洩漏不只發生在『直接把答案欄放進特徵』；只要測試集參與特徵選擇、縮放或"
        "超參數決策，就不再是乾淨測試。測試分數變高有時反而是洩漏警訊。"
    ),
    "editorialNote": (
        "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。僅以未標記測試特徵"
        "計算相關性的洩漏程度可能弱於直接使用測試標籤，但仍違反最終測試集不得參與流程選擇"
        "的評估邊界；本站作答依官方答案 B。"
    ),
    "references": [
        exam_ref(10),
        ref(
            "scikit-learn User Guide－Common pitfalls: Data leakage",
            SKLEARN_LEAKAGE,
            "測試資料不可用於模型選擇；特徵選擇等 transformation 只能由訓練資料學得",
        ),
        ref(
            "scikit-learn API－mutual_info_classif",
            SKLEARN_MI,
            "互資訊可量化變數間任意依賴；等於零代表獨立，較高表示依賴程度較強",
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
