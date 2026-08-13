"""Write draft explanations for 115-1 intermediate subject two, Q21-Q30.

The script verifies official answers, refuses to overwrite reviewed work, and
keeps every generated explanation in ``draft`` for independent review.

Usage::

    python scripts/write-explanations-115-1-m2-021-030.py
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
    "bf93f438f7be48d295c1b40a34d79f3d/115年第一次中級AI應用規劃師_"
    "第二科_大數據處理分析與應用_公告試題_20260615003416.pdf"
)
DEFAULT_NOTE = "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。"


def exam_ref(number: int) -> dict:
    return {
        "title": "115 年第一次中級 AI 應用規劃師－大數據處理分析與應用公告試題",
        "url": EXAM_PDF,
        "locator": f"第 {number} 題題幹、選項與官方答案",
        "checkedAt": CHECKED_AT,
    }


def ref(title: str, url: str, locator: str) -> dict:
    return {"title": title, "url": url, "locator": locator, "checkedAt": CHECKED_AT}


EXPECTED_ANSWER = {
    21: "D", 22: "C", 23: "C", 24: "C", 25: "C",
    26: "A", 27: "D", 28: "C", 29: "D", 30: "B",
}

DRAFTS: dict[int, dict] = {}

DRAFTS[21] = {
    "summary": "正確答案是 D。Spark 的 stddev 聚合或 RDD.aggregate() 能先在各 Executor 計算可合併的局部統計量，再彙總結果，避免把 10 億筆資料搬回 Driver。",
    "concept": (
        "分散式標準差可由筆數、總和與平方和等充分統計量合併，也可採數值較"
        "穩定的線上變異數演算法。Spark DataFrame 的 stddev／stddev_samp 屬"
        "聚合函數，執行計畫會在 partitions 上先做 partial aggregation，再 shuffle"
        "與 final aggregation。RDD.aggregate() 則要求設計可安全合併的 zero value、"
        "seqOp 與 combOp。collect() 會把所有元素送到單一 Driver，破壞分散式"
        "處理並可能造成記憶體耗盡。"
    ),
    "answerReason": (
        "D 唯一讓原始資料留在叢集分區，只傳送局部彙總狀態，通訊與 Driver"
        "記憶體需求遠小於 10 億筆原始紀錄。排序不是計算標準差的必要步驟，"
        "匯出 CSV 或 Excel 更無法承擔此規模。"
    ),
    "optionAnalysis": {
        "A": "collect() 會將 10 億筆資料序列化並集中到 Driver，可能造成網路壅塞與 OutOfMemory；statistics.stdev() 也只在單機執行，完全未利用 Executor。",
        "B": "標準差取決於每筆值相對平均數的平方差，不需知道排序或中位數；全域 sortBy 會引入昂貴 shuffle 與排序成本，仍未直接完成變異數計算。",
        "C": "CSV 會增加序列化、儲存與讀取成本，Excel 的工作表列數與單機資源也不適合十億筆資料；這是把可分散聚合問題轉成不可擴展的人工流程。",
        "D": "正確。DataFrame 聚合由 Spark 規劃局部與全域彙總；RDD.aggregate() 也可讓各 partition 累積統計狀態後合併，只需向 Driver 傳回小型結果。",
    },
    "trap": "能呼叫 Python 函式不代表適合 Spark 規模。看到 collect() 先檢查結果是否真的很小；標準差是可聚合統計，不必排序，也不應匯出後再單機計算。",
    "references": [
        exam_ref(21),
        ref("PySpark－stddev_samp 官方文件", "https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.functions.stddev_samp.html", "stddev_samp 聚合函數計算欄位的樣本標準差；stddev 為其別名"),
        ref("Apache Spark RDD Programming Guide", "https://spark.apache.org/docs/latest/rdd-programming-guide.html", "Actions－aggregate：以每個 partition 的 seqOp 與跨 partition 的 combOp 彙總資料"),
    ],
}

DRAFTS[22] = {
    "summary": "正確答案是 C。時間序列應依時間切分並以 walk-forward 驗證，建立季節、趨勢、滯後與滾動特徵，也應納入節日及颱風等事件，並用多種誤差指標檢查。",
    "concept": (
        "銷售預測不能隨機打散，否則未來型態可能洩漏到訓練資料。Walk-forward"
        "依時間向前移動訓練與驗證窗口，可模擬每次以當時可取得資料預測未來 14"
        "天。週期、年度季節性與趨勢可由分解、時間欄位及模型捕捉；lag、rolling"
        "features 必須只使用預測時點之前的資料。節日與可得事件資訊是需求驅動因子，"
        "不應當成極端值任意刪除。RMSE 對大誤差較敏感，MAPE 易受接近零銷售影響，"
        "兩者並看比只選一項完整。"
    ),
    "answerReason": (
        "C 同時處理時序驗證、趨勢與季節性、多門市特徵、已知與不定期事件，且"
        "使用互補指標。其他選項不是造成時間洩漏、忽略重要事件，就是假定深度"
        "學習可取代所有特徵與門市差異處理。"
    ),
    "optionAnalysis": {
        "A": "隨機 80/20 會讓較晚資料進入訓練、較早資料進入測試，無法模擬真實未來預測；刪除節日高峰也會移除重要業務規律，使模型在真正旺季失準。",
        "B": "依時間切分、季節模型與節日資訊方向正確，但颱風等不定期事件會造成顯著需求變化，已知或可取得時應納入；單次最後 90 天也不如 walk-forward 能檢查不同季節穩定性。",
        "C": "正確。前進式驗證保持因果時間順序，多組窗口測試穩定性；分解與特徵工程捕捉週期、趨勢與事件，多指標則呈現大誤差及相對誤差。",
        "D": "深度模型可能自動學習部分時序結構，但不保證在有限三年資料下優於其他方法；不提供節日、事件與門市識別特徵，且強迫所有門市完全同質，會忽略已知訊號。",
    },
    "trap": "時間序列的第一個門檻是禁止未來洩漏；lag 與 rolling 也必須在每個驗證窗口內重新計算。MAPE 遇到零或近零分母會失真，不宜作唯一指標。",
    "references": [
        exam_ref(22),
        ref("scikit-learn－TimeSeriesSplit", "https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html", "時間排序資料不可用一般交叉驗證，TimeSeriesSplit 以較早折訓練、後續折測試"),
        ref("Forecasting: Principles and Practice－Time series cross-validation", "https://otexts.com/fpp3/tscv.html", "Rolling forecasting origin 以逐步向前的訓練集評估一至多步預測誤差"),
    ],
}

DRAFTS[23] = {
    "summary": "正確答案是 C。圖中的 C 隨 FPR 向右增加時 TPR 卻明顯下降後再上升；單一模型依閾值掃描形成的 ROC 點集，其累積 TPR 與 FPR 應皆為非遞減。",
    "concept": (
        "二元分類器從高到低放寬 decision threshold 時，更多樣本被判為正類。"
        "因此 TP 與 FP 只會增加或不變，TPR=TP/(TP+FN) 與 FPR=FP/(FP+TN) 也只會"
        "增加或不變；將各閾值點依 FPR 排序連線，ROC 路徑可有水平、垂直與對角"
        "段，但不能往左或在 FPR 增加時向下退回。官方附圖中 A 是 TPR=1 的水平"
        "段，B 單調上升，D 是無辨識力基準對角線，C 則出現下凹回落。"
    ),
    "answerReason": (
        "實際目視可見 C 從原點上升至局部高點後，在橫軸 FPR 繼續增加時 TPR"
        "下降，再回升到右上角。這無法由同一組固定分數按單一閾值依序放寬所形成，"
        "故是四者中最不可能的 ROC 曲線。"
    ),
    "optionAnalysis": {
        "A": "水平線 A 位於 TPR=1；它可視為完美分類器先在 FPR=0 垂直升到 TPR=1，再放寬閾值使 FPR 增加的頂端路徑，水平段本身不違反單調性。",
        "B": "曲線 B 從左下往右上單調增加，且多數區段位於對角線上方，符合具有一定排序能力的分類器 ROC 形狀。",
        "C": "正確。C 在 FPR 增加期間出現 TPR 大幅下降；放寬同一模型的閾值不會讓先前已判為正類的 true positives 消失，因此這種回頭路徑不成立。",
        "D": "斜直線 D 從 (0,0) 到 (1,1)，代表各閾值下 TPR 約等於 FPR，常作隨機排序或無辨識力的 ROC 基準，仍是可能形狀。",
    },
    "trap": "ROC 不要求永遠凹向左上，有限樣本的實際曲線可呈階梯甚至局部低於對角線；真正不可能的是依 FPR 由小到大時 TPR 反向下降。",
    "editorialNote": "本站已目視官方第 23 題附圖：A 為頂端水平線、B 為單調上升曲線、C 有明顯向下回落、D 為對角線。依官方答案 C 判定；圖線為示意圖，解讀重點是 ROC 閾值路徑的座標非遞減性。",
    "references": [
        exam_ref(23),
        ref("scikit-learn－roc_curve", "https://scikit-learn.org/stable/modules/generated/sklearn.metrics.roc_curve.html", "ROC 由遞減 threshold 的 FPR 與 TPR 陣列形成；輸出 FPR、TPR 皆遞增"),
    ],
}

DRAFTS[24] = {
    "summary": "正確答案是 C。Spearman 與 Kendall 都以順序資訊降低極端數值大小的影響，但 Kendall 通常被視為對離群與小樣本較穩健，不能說 Spearman 的穩健度更強。",
    "concept": (
        "Pearson 衡量兩個連續變數的線性關係，直接使用數值，因此容易受極端值"
        "影響。Spearman 先把數值轉成 ranks，再對排名計算 Pearson correlation，"
        "適合單調但非線性的關係；有 ties 時使用平均排名。Kendall tau 比較所有"
        "觀測對是 concordant 或 discordant，並可用 tau-b 校正 ties。兩個 rank"
        "correlations 都比原始值 Pearson 不受離群幅度影響，但穩健性仍會受樣本、"
        "ties 與污染型態影響，不能把 Spearman 一概說成勝過 Kendall。"
    ),
    "answerReason": (
        "C 把兩種秩相關的穩健性方向說反，是本題不正確敘述。A 正確區分線性與"
        "單調關係，B 是 Spearman 的定義性計算方式，D 的三種係數範圍都為 [-1,1]。"
    ),
    "optionAnalysis": {
        "A": "正確。Pearson 的目標是線性共變；Spearman 與 Kendall 依次序判斷，可在關係保持單調、但曲線不是直線時仍得到高相關。",
        "B": "正確。Spearman rho 可定義為兩變數 ranks 的 Pearson correlation；無 ties 時也可用排名差平方的簡化公式，有 ties 時應採一般排名相關計算。",
        "C": "不正確。兩者都能抑制極端數值幅度，但 Kendall 以成對順序一致性衡量，通常具有較佳穩健與小樣本解釋；不能宣稱 Spearman 對離群更強。",
        "D": "正確。Pearson r、Spearman rho 與 Kendall tau 都介於 -1 到 1；正負表示關係方向，絕對值越接近 1 表示各自定義下關聯越一致。",
    },
    "trap": "本題問『不正確』。Rank-based 不等於完全不受離群值影響：極端點仍可能占據排名端點；另有大量相同的 1–5 分時，必須使用能處理 ties 的公式。",
    "editorialNote": "本站依官方答案 C 判定。Spearman 與 Kendall 的『誰更穩健』不是脫離資料條件的絕對定律，會受樣本量、ties 與污染方式影響；本題應理解為一般統計教材中 Kendall 對小樣本及異常排序較穩健的比較。滿意度只有 1–5 分，人工複核時亦應確認 ties 的處理方式。",
    "references": [
        exam_ref(24),
        ref("SciPy－pearsonr", "https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.pearsonr.html", "Pearson correlation 衡量兩資料集的線性關係，範圍為 [-1,1]"),
        ref("SciPy－spearmanr", "https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.spearmanr.html", "Spearman rank-order correlation 衡量單調關係，範圍為 [-1,1]"),
        ref("SciPy－kendalltau", "https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.kendalltau.html", "Kendall tau 以 concordant／discordant pairs 與 ties 計算，範圍為 [-1,1]"),
    ],
}

DRAFTS[25] = {
    "summary": "正確答案是 C。對 0.3% 詐欺少數類引入 class weight 或 cost-sensitive loss，可讓漏判詐欺與誤判正常交易的不同成本進入訓練，避免多數類主導目標函數。",
    "concept": (
        "Accuracy 在極度不平衡資料中可能誤導：即使全部預測正常，也可達約 99.7%"
        "準確率，卻有零詐欺 recall。Cost-sensitive learning 對少數類或不同錯誤"
        "指定較高代價，使模型不能靠忽略詐欺取得低 loss；class weight 是常見"
        "實作。評估仍應同時看詐欺 recall、precision、PR-AUC、混淆矩陣與每類"
        "業務成本，並在獨立資料上調 decision threshold。"
    ),
    "answerReason": (
        "C 直接改變模型學習目標，使稀少詐欺樣本在損失中具有足夠影響力，是"
        "選項中最完整的訓練改善。只看 precision 會忽略漏判，繼續 Accuracy 或"
        "刪除少數類則會強化原問題。"
    ),
    "optionAnalysis": {
        "A": "整體 Accuracy 被 99.7% 正常交易支配，繼續最佳化可讓模型更傾向預測正常，不能保證找回詐欺，也無法反映誤報與漏報成本。",
        "B": "Precision 能衡量被攔截交易中有多少真是詐欺，有助控制誤報；但單獨最大化 precision 可能只攔截極少數最確定案件，造成 recall 很低，未解決幾乎抓不到詐欺。",
        "C": "正確。提高詐欺類或 false negative 的損失權重，迫使模型重視少數類；再配合 PR 指標與 threshold 調整，才能平衡攔截率和誤傷。",
        "D": "移除少數類會讓模型更少看到甚至完全看不到詐欺模式，雖可能使表面收斂更穩，實際偵測能力只會惡化。",
    },
    "trap": "訓練方法與評估方法是兩件事：class weight 改 loss，Precision／Recall／PR-AUC 用來評估與選 threshold。C 最適合改善訓練，但不能因此繼續只報 Accuracy。",
    "editorialNote": "本站依官方答案 C 判定。Class Weight 或 cost-sensitive learning 是合理改善方向，但題目所述『大量誤判正常交易』也要求另看 precision、校準與決策閾值；單一加權手段不保證同時解決漏判與誤報。",
    "references": [
        exam_ref(25),
        ref("scikit-learn－Classification of text documents using sparse features", "https://scikit-learn.org/stable/auto_examples/text/plot_document_classification_20newsgroups.html", "分類報告同時呈現 precision、recall 與 F1，而非只看 accuracy"),
        ref("scikit-learn－compute_class_weight", "https://scikit-learn.org/stable/modules/generated/sklearn.utils.class_weight.compute_class_weight.html", "balanced class weights 依類別頻率反比計算，使少數類在訓練目標中取得較高權重"),
        ref("scikit-learn－Precision-Recall", "https://scikit-learn.org/stable/auto_examples/model_selection/plot_precision_recall.html", "Precision-Recall 適合類別非常不平衡時檢查正類偵測與誤報取捨"),
    ],
}

DRAFTS[26] = {
    "summary": "正確答案是 A。把連續 UNIX 時間數值切成早晨、下午、夜晚等區間，是將連續特徵分箱成離散類別的 Feature Discretization。",
    "concept": (
        "特徵離散化（discretization 或 binning）以一組邊界把連續值映射到有限"
        "區間，例如年齡層、金額級距或一天時段。它可表達非線性區段規律、降低"
        "數值細微變動影響，但邊界選擇會損失區間內資訊。離散化後得到的類別仍需"
        "依模型需求編碼；若時段只是名稱且沒有嚴格線性順序，可再用 one-hot。"
        "時間跨越午夜還具有週期性，sin/cos 編碼是另一種保留 23 時與 0 時接近的"
        "做法，但不改變題述操作名稱。"
    ),
    "answerReason": (
        "A 精確描述從連續 timestamp 衍生有限區間類別的轉換。Scaling 只改尺度，"
        "降維減少多個維度，One-Hot 則是在類別已經形成後把類別轉成指示欄位。"
    ),
    "optionAnalysis": {
        "A": "正確。先把 timestamp 轉為小時，再依 6、12、18 時等邊界分箱，連續時間便成為三個離散時段類別，屬特徵離散化。",
        "B": "Scaling 會將連續值標準化或縮放到固定範圍，但仍保留連續相對距離，不會產生早晨、下午、夜晚三個類別。",
        "C": "降維以 PCA、特徵選擇等方法把多個特徵縮成較少維度；此處是一個 timestamp 的表示轉換，目標不是降低多維資料維數。",
        "D": "One-Hot Encoding 可把三個時段類別轉成三個 0/1 欄位，但題幹描述的動作是先決定區間；它發生在 one-hot 之前，兩者不可互換。",
    },
    "trap": "『切區間』是 discretization，『把類別變成 0/1 欄』才是 one-hot。另要注意夜晚 18–6 跨日，實作邊界不能用單純 18≤hour<6。",
    "references": [
        exam_ref(26),
        ref("scikit-learn－Feature discretization", "https://scikit-learn.org/stable/modules/preprocessing.html#discretization", "Discretization 將連續特徵分割成離散值或 bins，並說明其與 one-hot encoding 的關係"),
    ],
}

DRAFTS[27] = {
    "summary": "正確答案是 D。Data Density 強調在有限圖面中呈現高比例且有意義的資料資訊，但仍須保持可讀性與清楚層次，而不是單純塞滿數字或刪掉所有輔助元素。",
    "concept": (
        "Tufte 的 data density 關注圖面中實際呈現的資料量相對於圖形面積；資料"
        "豐富的設計可讓讀者在同一視野比較大量觀測與變數。這要與 data-ink ratio"
        "一起理解：減少無助理解的裝飾，但座標、標籤、圖例與基準線若承擔解碼、"
        "定位或比較功能，就不是可一律刪除的浪費。1,000 位使用者與三項指標可"
        "考慮 small multiples、熱圖或排序後的緊湊圖形，以分組、層次與標註維持"
        "辨識度。"
    ),
    "answerReason": (
        "D 同時抓住『有限空間呈現更多有效資料』與『仍要可讀』兩個條件。A 把"
        "資料拆散會削弱同頁比較，B 把必要解碼資訊也全部刪除，C 則用裝飾占用"
        "空間、降低資料墨水比例。"
    ),
    "optionAnalysis": {
        "A": "拆成多頁或多張圖可降低單圖負擔，但決策者難以在同一視野比較 1,000 人的整體型態；它不直接追求有限頁面的高 data density。",
        "B": "移除無意義裝飾符合減少 chartjunk，但軸、單位、圖例和必要基準線是讀懂數值的語意結構；全部刪掉會使高密度資料無法解碼。",
        "C": "陰影、3D 與大量色塊若不承載資料，會增加 non-data ink、遮蔽細微差異並占用有限空間，與有效資料密度方向相反。",
        "D": "正確。以緊湊但有組織的視覺編碼呈現三項指標與大量使用者，同時保留標籤、層次和比較基準，才能兼顧資訊量與理解。",
    },
    "trap": "Data Density 不是『資訊越擠越好』；有效資料必須可比較。也不要把 data-ink ratio 誤讀成刪除所有非數據線條，必要的軸與標籤本身服務於資料理解。",
    "references": [
        exam_ref(27),
        ref("Edward Tufte－The Visual Display of Quantitative Information", "https://www.edwardtufte.com/book/the-visual-display-of-quantitative-information/", "書籍章節 The Data-Ink Maximization and Graphical Design 與 Data Density，討論有效資料呈現、chartjunk 及資訊密度"),
    ],
}

DRAFTS[28] = {
    "summary": "正確答案是 C。把 y 軸截在接近 3% 的位置會讓 A、B、C 僅 0.6～0.8 個百分點的差距佔滿圖高，容易使讀者高估實際比例差異。",
    "concept": (
        "圖形用位置與長度表達數值。若長條圖的 y 軸不從零開始，長條的視覺長度"
        "不再與數值比例一致：C 的 4.0% 相對 A 的 3.2% 是高 0.8 個百分點，"
        "相對增幅為 25%，但若座標從 3.0% 開始，圖上長度可能呈現 5 倍等誇張"
        "差異。截軸不是在所有圖型都禁止；折線圖若重點是微小變動，可在明確標示"
        "尺度、斷點與數值下使用。但題幹明說『刻意』截斷以放大差異，問題就是"
        "視覺誤導。"
    ),
    "answerReason": (
        "C 直接描述設計後果：視覺距離被放大，讀者可能把小幅轉換率差異理解為"
        "巨大成效。截軸不會提升原始數據正確性；即使增加辨識度，也必須以不誤導"
        "的標示與圖型選擇為前提。"
    ),
    "optionAnalysis": {
        "A": "截軸可能放大小變動，但讀者還需重新解讀非零基線，通常增加而非降低認知負擔；若刻意隱藏尺度，還會妨礙正確比較。",
        "B": "它確實能讓小差異在像素上更明顯，但題目問『最可能產生的問題』，且明示刻意放大；可辨識性收益不能抵銷對差異量級的誤導。",
        "C": "正確。非零基線使視覺長度不再代表從零起算的轉換率，0.2 或 0.8 個百分點差異可被畫成數倍高度，讓觀者高估效果。",
        "D": "軸的起點只改變顯示映射，不會改變 A=3.2%、B=3.8%、C=4.0% 的計算值或量測準確性；圖表可能數值正確卻視覺敘事誤導。",
    },
    "trap": "百分點與百分比增幅不同：4.0%−3.2%=0.8 個百分點，相對增幅是 25%。截軸若有合理分析目的，必須明確顯示起點與斷軸，長條圖尤其應慎用。",
    "editorialNote": "本站依題目明示『刻意截斷、造成視覺差異放大』而選 C。非零 y 軸並非所有情境都不允許，例如折線圖檢視小幅波動時可能合理；是否誤導取決於圖型、標示、分析目的與是否提供完整尺度。",
    "references": [
        exam_ref(28),
        ref("Edward Tufte－The Visual Display of Quantitative Information", "https://www.edwardtufte.com/book/the-visual-display-of-quantitative-information/", "書中 Lie Factor 與 graphical integrity 原則：圖形呈現的效果大小應與資料中的效果大小相稱"),
    ],
}

DRAFTS[29] = {
    "summary": "正確答案是 D。折線圖依時間順序連接連續延遲值，最能呈現趨勢、突增與是否跨越 P99 200ms 的 SLA 門檻。",
    "concept": (
        "Time-series line chart 以時間置於 x 軸、量測值置於 y 軸，連線強調相鄰"
        "時間點的方向與變化速度。監控 P99 延遲時，應用固定 aggregation window"
        "計算 percentile，並加一條 200ms threshold；也可同圖或分面呈現 P50、P95、"
        "P99，避免平均值掩蓋尾端延遲。折線不表示每兩點間真的線性變化，只是"
        "協助讀取時間順序。"
    ),
    "answerReason": (
        "D 的視覺編碼與任務完全吻合：時間連續、指標為連續數值、重點是變化趨勢"
        "和跨線事件。面積圖更強調總量，散佈圖重點是兩變數關係，長條圖則適合"
        "離散類別或少量時間區段比較。"
    ),
    "optionAnalysis": {
        "A": "Area chart 填滿基線到曲線之間的面積，適合強調累積量或多系列組成；延遲不是可加總存量，填色可能放大視覺重量並遮蔽多條 percentile。",
        "B": "Scatter plot 適合探索兩個數值變數的關係或離群點；雖可把時間放 x 軸，但不連接時間順序時，趨勢與連續跨越 SLA 的區段較難快速判讀。",
        "C": "Bar chart 適合比較離散類別或少數期間彙總；高頻監控會產生大量長條與視覺雜訊，不如折線緊湊呈現連續走勢。",
        "D": "正確。折線依時間連接 P99，能快速看到上升、週期、尖峰與超過 200ms 的區段；搭配 SLA 水平線即可直接判讀是否達標。",
    },
    "trap": "題目問『隨時間趨勢』時優先折線，但監控值要明確標示 aggregation window；P99 不是第 99% 的請求數量，而是 99% 請求延遲不超過的分位值。",
    "references": [
        exam_ref(29),
        ref("Grafana－Time series 官方文件", "https://grafana.com/docs/grafana/latest/panels-visualizations/visualizations/time-series/", "Time series visualization 以時間為 x 軸呈現數值，支援 thresholds 與多序列趨勢監控"),
    ],
}

DRAFTS[30] = {
    "summary": "正確答案是 B。大批次降低隨機梯度雜訊，雖能提高硬體吞吐與穩定性，卻較可能走向較尖銳的極小值；參數小幅擾動便使損失上升，常與較差泛化相關。",
    "concept": (
        "Mini-batch gradient 是全資料梯度的估計。batch 增大會降低估計變異，"
        "更新方向更穩定並可提高 GPU 平行效率；小 batch 的噪音則可能幫助軌跡"
        "離開狹窄、尖銳的低損失區域。經典研究觀察 large-batch 訓練較常收斂到"
        "sharp minima，測試表現可能較差。不過泛化同時受到 learning-rate scaling、"
        "warmup、正則化、訓練步數與模型架構影響，不能把 batch size 視為唯一"
        "決定因素。"
    ),
    "answerReason": (
        "B 是四項中唯一同時正確描述大 batch 梯度較穩定，以及其可能較差泛化的"
        "最佳化解釋。選項用『局部極小值』較寬鬆，技術上更精確的關鍵是尖銳"
        "而非僅僅局部；其餘選項否認 GPU 優勢、把噪音直接等同梯度爆炸，或宣稱"
        "batch 與泛化無關。"
    ),
    "optionAnalysis": {
        "A": "Large batch 每一步計算更多樣本，但矩陣運算通常更能利用 GPU 平行度，題幹也已觀察訓練較快；問題不是 GPU 無法處理，而是最佳化路徑與泛化差距。",
        "B": "正確（依官方題意）。大 batch 降低梯度雜訊，研究觀察其較易到達 sharp minima；這些解附近參數稍變便使 loss 快速上升，常對未見資料較不穩健。",
        "C": "小 batch 的估計變異較大，不等於 gradient explosion；爆炸通常與深層／循環結構、權重尺度或學習率造成梯度範數失控有關，可用 clipping 等處理。",
        "D": "學習率確實需隨 batch 調整，但不能因此說 batch size 與泛化無關；在其他設定相近時，梯度噪音、每 epoch 更新次數與所到達解的幾何都會改變。",
    },
    "trap": "『梯度較穩』只表示估計方差小，不等於泛化一定好；也不要把 stochastic noise 誤稱為 gradient explosion。Large batch 可透過學習率、warmup 與正則化改善，並非必然失敗。",
    "editorialNote": "本站依官方答案 B 判定，但『容易收斂至局部極小值』用語不夠精確：神經網路研究常比較 large batch 對 sharp minima、small batch 對 flatter minima 的偏好，而非主張只要是 local minimum 就泛化差。批次大小與泛化的因果也受學習率、更新步數及正則化共同影響。",
    "references": [
        exam_ref(30),
        ref("Keskar et al., On Large-Batch Training for Deep Learning: Generalization Gap and Sharp Minima（2016）", "https://arxiv.org/abs/1609.04836", "摘要與實驗：large-batch 方法傾向 sharp minimizers，並觀察到相對 small-batch 的 generalization gap"),
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
