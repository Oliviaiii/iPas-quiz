"""Write explanation drafts for 114-2 intermediate subject two, Q1-Q10.

The script validates official answers, refuses to overwrite reviewed content,
and leaves every generated explanation in ``draft`` status.

Usage::

    python scripts/write-explanations-114-2-m2-001-010.py
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
NIST_ZSCORE = "https://itl.nist.gov/div898/handbook/eda/section3/eda35h.htm"
NIST_SKEWNESS = "https://itl.nist.gov/div898/handbook/eda/section3/eda35b.htm"
NIST_CDF = "https://www.itl.nist.gov/div898/handbook/eda/section3/eda3671.htm"
PANDAS_DESCRIBE = "https://pandas.pydata.org/pandas-docs/stable/user_guide/basics"
SKLEARN_PREPROCESSING = "https://scikit-learn.org/stable/modules/preprocessing.html"
SKLEARN_ROBUST = (
    "https://scikit-learn.org/stable/modules/generated/"
    "sklearn.preprocessing.RobustScaler.html"
)
POSTGRES_TRANSACTIONS = "https://www.postgresql.org/docs/current/tutorial-transactions.html"
GOOGLE_FEATURES = (
    "https://developers.google.com/machine-learning/crash-course/numerical-data/"
    "feature-vectors"
)
SKLEARN_ANOMALY = "https://scikit-learn.org/stable/modules/outlier_detection.html"

DEFAULT_NOTE = "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。"


def ref(title: str, url: str, locator: str) -> dict:
    return {"title": title, "url": url, "locator": locator, "checkedAt": CHECKED_AT}


def exam_ref(number: int) -> dict:
    return ref(
        "114 年第二次中級 AI 應用規劃師－大數據處理分析與應用公告試題",
        EXAM_PDF,
        f"第 {number} 題題幹、選項、附圖（如有）與官方答案",
    )


EXPECTED_ANSWER = {
    1: "D", 2: "B", 3: "A", 4: "B", 5: "B",
    6: "C", 7: "C", 8: "B", 9: "C", 10: "C",
}

DRAFTS: dict[int, dict] = {}

DRAFTS[1] = {
    "summary": "正確答案是 D。Z 分數為 2 表示該觀測值位於平均值上方 2 個標準差的位置。",
    "concept": (
        "Z 分數把原始數值轉換成以標準差為單位的相對位置，公式為 z=(x-平均值)/標準差。"
        "z 的正負表示方向：正值在平均值之上，負值在平均值之下；絕對值表示距離平均值有"
        "幾個標準差。標準化後的數字不是原始量測單位，也不能只憑一個固定門檻，在不考慮"
        "資料分佈與樣本大小時就宣告某點必然異常。"
    ),
    "answerReason": (
        "將 z=2 代入公式可得 x-平均值=2×標準差，因此 x 比平均值高兩個標準差，與 D 完全"
        "一致。題目沒有提供原始平均值與標準差，所以不能求出 x 的實際數值，也沒有提供"
        "異常判定規則。"
    ),
    "optionAnalysis": {
        "A": (
            "Z 分數 2 是無單位的相對位置，不代表原始值就是 2。只有在平均值為 0 且標準差"
            "為 1 的特殊資料尺度下，原始值才也會等於 2；題目沒有這項條件。"
        ),
        "B": (
            "比平均值低兩個標準差會使 x-平均值為負，因此 Z 分數應是 -2，而不是 +2。"
            "這個選項把 Z 分數的正負方向顛倒了。"
        ),
        "C": (
            "Z 分數可協助標示可能的極端觀測，但 z=2 不會自動等於異常值。是否異常要配合"
            "資料近似常態的前提、樣本大小、領域容忍範圍與事先設定的門檻判斷。"
        ),
        "D": (
            "正確。Z 分數的分子是觀測值減平均值；結果為正 2，表示觀測值在平均值右側，"
            "距離正好是兩個標準差。"
        ),
    },
    "trap": (
        "先看正負號判斷高於或低於平均值，再看絕對值判斷相距幾個標準差。不要把 Z 分數"
        "誤當原始值，也不要把常見的極端值經驗門檻當成任何資料都適用的絕對定義。"
    ),
    "references": [
        exam_ref(1),
        ref(
            "NIST/SEMATECH e-Handbook－Detection of Outliers",
            NIST_ZSCORE,
            "Z_i=(Y_i-平均值)/標準差；資料以距平均值幾個標準差為單位表示，並提醒以 Z 分數判異常的限制",
        ),
    ],
}

DRAFTS[2] = {
    "summary": "正確答案是 B。`df['總銷售額'].describe()` 會一次回傳筆數、平均值、標準差、最小值與各分位數等敘述統計。",
    "concept": (
        "pandas 中 `df['總銷售額']` 先從 DataFrame 取出單一欄位，結果通常是 Series。對數值型"
        "Series 呼叫 `describe()`，預設會彙整 count、mean、std、min、25%、50%、75% 與 max。"
        "它適合快速檢查集中位置、離散程度與範圍；若只要總和、排序或單一指標，則應使用"
        "對應方法，而不是把這些方法當成整套敘述統計。"
    ),
    "answerReason": (
        "題幹明確要求「敘述性統計量（如平均值、標準差等）」且欄位已指定為總銷售額。B 先"
        "選取該欄，再呼叫 pandas 官方提供的 `describe()`，一次取得題目列舉的多個統計量。"
    ),
    "optionAnalysis": {
        "A": (
            "`sum()` 只計算所有非缺失銷售額的加總，適合回答總營收是多少；它不會同時回傳"
            "平均值、標準差、分位數與範圍，因此不足以完成題目要求的敘述性統計摘要。"
        ),
        "B": (
            "正確。選取總銷售額 Series 後呼叫 `describe()`，數值欄位會得到 count、mean、std、"
            "min、四分位數與 max，是 pandas 用來快速產生敘述統計摘要的標準方法。"
        ),
        "C": (
            "`sort_values()` 會依數值排序並回傳重新排列的資料，適合找最高或最低銷售紀錄；"
            "排序本身不計算平均值或標準差，故不是敘述性統計摘要函式。"
        ),
        "D": (
            "pandas Series 沒有用來產生這套摘要的標準 `stats()` 方法；即使其他函式庫可能有"
            "同名介面，也不能套用成題目中 pandas Series 的語法。"
        ),
    },
    "trap": (
        "分清楚「單一統計量」與「摘要表」：`sum()`、`mean()` 各回一種統計，`describe()` 才"
        "一次彙整多種統計。也要注意 `describe()` 對數值欄與文字欄回傳的項目不同。"
    ),
    "references": [
        exam_ref(2),
        ref(
            "pandas User Guide－Essential basic functionality: Summarizing data",
            PANDAS_DESCRIBE,
            "describe() 對 Series/DataFrame 計算 count、mean、std、min、四分位數與 max 的範例",
        ),
    ],
}

DRAFTS[3] = {
    "summary": "正確答案是 A。官方附圖的主要資料集中在約 30～50，左側尾巴延伸到約 -20，長尾在左，因此偏態為負。",
    "concept": (
        "偏態（skewness）衡量分佈相對於中心的非對稱程度。判讀直方圖時應看哪一側的尾巴"
        "延伸較遠，而不是只看最高峰位於哪裡：左尾較長稱左偏或負偏態，skewness<0；右尾"
        "較長稱右偏或正偏態；兩側近似鏡像時偏態接近 0。少數離中心很遠的觀測會因偏態"
        "公式使用三次方差異而顯著影響符號與大小。"
    ),
    "answerReason": (
        "已目視核對題庫附圖 `/images/questions/aiap-114-intermediate-2-big-data-p01-1.png`：峰值約在"
        "40 左右，右側大致在 60 前結束，左側卻一路稀疏延伸到約 -20。左尾明顯比右尾長，"
        "依偏態定義最可能得到負值，因此選 A。"
    ),
    "optionAnalysis": {
        "A": (
            "正確。圖中大部分觀測在較高數值區，少數低值把尾巴向左拉長；NIST 對負偏態的"
            "描述即為左尾相對於右尾較長，與附圖形狀一致。"
        ),
        "B": (
            "Skewness>0 代表右偏，也就是多數資料在較低值、少數高值讓右尾延伸更長。附圖剛好"
            "相反：稀疏的長尾出現在低值左側，所以不應判為正偏態。"
        ),
        "C": (
            "Skewness=0 通常對應左右近似對稱的分佈；附圖的峰左右並非鏡像，左側延伸距離與"
            "低密度尾巴都較長，沒有足夠理由視為零偏態。"
        ),
        "D": (
            "若只有圖片而沒有原始數據，確實不能從圖上算出精確偏態係數；但題目問的是「較有"
            "可能」的選項，可依尾巴方向判斷符號。圖形資訊足以判斷最可能小於 0。"
        ),
    },
    "trap": (
        "偏態方向由長尾決定，不是由峰在哪一側決定。另一個陷阱是把「不能算出精確數值」"
        "誤解成「不能判斷正負」；本題只要求較可能的符號，附圖已提供充分線索。"
    ),
    "editorialNote": (
        "本站已於 2026-08-12 目視核對 questions.json 的 figures 欄位所指官方裁切圖；圖中左尾"
        "延伸至約 -20、峰約在 40，支持官方答案 A。本站內容仍為 AI 輔助詳解初稿，尚待獨立人工複核。"
    ),
    "references": [
        exam_ref(3),
        ref(
            "NIST/SEMATECH e-Handbook－Measures of Skewness and Kurtosis",
            NIST_SKEWNESS,
            "負偏態表示左尾相對較長，正偏態表示右尾相對較長；偏態為對稱性的量度",
        ),
    ],
}

DRAFTS[4] = {
    "summary": "正確答案是 B。對連續型隨機變數，累積分佈函數 F(x) 是機率密度函數從負無限大積分到 x 的累積面積。",
    "concept": (
        "累積分佈函數定義為 F(x)=P(X≤x)，表示隨機變數不超過 x 的機率。若 X 是具有機率密度"
        "f(t) 的連續型隨機變數，則 F(x)=∫_{-∞}^{x} f(t)dt；在可微處，CDF 的導數才是 PDF。"
        "CDF 必須單調不減，值域在 0 與 1 之間，並在 x 趨近負、正無限大時分別趨近 0、1。"
        "離散型隨機變數則以機率質量加總，不應稱為 PDF 的離散總和。"
    ),
    "answerReason": (
        "題目把 CDF 與 PDF 的關係列為四選一。對連續分佈，CDF 正是 PDF 在目標值左側的積分，"
        "也就是曲線下累積面積，因此 B 符合數學定義；平均值與標準差是分佈摘要，不會形成"
        "每個 x 對應的累積機率函數。"
    ),
    "optionAnalysis": {
        "A": (
            "PDF 的平均值不是 CDF。期望值是在整個支撐範圍積分 x f(x) 所得的一個數值，"
            "而 CDF 是隨 x 改變、回傳 P(X≤x) 的函數，兩者輸出與用途都不同。"
        ),
        "B": (
            "正確。對連續型變數，把 PDF 從負無限大積分到指定 x，即可累積所有不超過 x 的"
            "機率，得到 F(x)。積分上下限必須隨查詢點 x 改變。"
        ),
        "C": (
            "離散分佈的 CDF 可由機率質量函數 PMF 對所有不超過 x 的值加總；但選項寫的是"
            "PDF 的離散總和，混淆了連續密度與離散機率質量。題目以 PDF 提問時應選積分。"
        ),
        "D": (
            "標準差描述整體數值偏離平均值的典型幅度，只是一個分散程度統計量；它不會告訴"
            "我們 P(X≤x)，也不是由 PDF 形成 CDF 的運算。"
        ),
    },
    "trap": (
        "連續型記住「PDF 積分得到 CDF、CDF 微分得到 PDF」；離散型則是 PMF 加總得到 CDF。"
        "不要把平均值、標準差這些單一摘要值與整條分佈函數混為一談。"
    ),
    "editorialNote": (
        "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。選項 B 只有在分佈"
        "存在 PDF 的連續型情況下可直接表述為積分；一般定義應寫為 F(x)=P(X≤x)。"
    ),
    "references": [
        exam_ref(4),
        ref(
            "NIST/SEMATECH e-Handbook－CDF of the Standard Normal Distribution",
            NIST_CDF,
            "以曲線下累積面積說明 CDF，並示範 P[X≤a] 的計算",
        ),
    ],
}

DRAFTS[5] = {
    "summary": "正確答案是 B。把無序類別任意編成 0、1、2 等整數，可能讓模型誤以為類別具有大小與距離關係。",
    "concept": (
        "類別資料分成名目尺度與順序尺度。名目類別如城市、顏色只有不同，沒有自然大小；若用"
        "單一整數欄表示，某些線性、距離或分割模型會把 2 視為大於 1，甚至認為 0 到 2 的"
        "距離是 0 到 1 的兩倍，這是編碼人為製造的結構。無序類別通常可用 one-hot encoding；"
        "真正有順序的等級資料才可在明確順序下使用 ordinal encoding。"
    ),
    "answerReason": (
        "題目問 Label Encoding 最常見的潛在風險。B 精確指出將名目類別對應成整數會引入"
        "虛假順序，影響把數字大小當作資訊的模型。缺值與新類別都需要額外處理，但並非任何"
        "標籤編碼都必然無法處理；記憶體用量通常反而比 one-hot 低。"
    ),
    "optionAnalysis": {
        "A": (
            "缺值可先填補、保留專用代碼，或由支援 missing values 的編碼流程處理；Label Encoding"
            "本身不代表缺值絕對無法處理。真正普遍的語意風險是整數值被模型當成有序量。"
        ),
        "B": (
            "正確。若紅、綠、藍被任意編為 0、1、2，這些數字會暗示藍大於綠、綠大於紅及固定"
            "距離，但原始名目類別沒有這些關係，模型可能因此學到不存在的規律。"
        ),
        "C": (
            "上線遇到訓練時未見的新類別確實要設定 unknown handling，某些編碼器預設會報錯；"
            "但可以保留未知代碼或設定處理策略，所以不是「無法擴展」的必然特性。"
        ),
        "D": (
            "單欄整數編碼只為每筆資料保存一個代碼，記憶體通常比展開多欄的 one-hot 更省。"
            "高基數造成維度與記憶體壓力，反而較常見於 one-hot encoding。"
        ),
    },
    "trap": (
        "重點不是整數本身不能用，而是類別有沒有真實順序，以及模型會不會解讀數值距離。"
        "另要分清楚 scikit-learn 的 `LabelEncoder` 主要編碼目標 y，特徵欄位通常使用"
        "`OrdinalEncoder` 或 `OneHotEncoder`。"
    ),
    "editorialNote": (
        "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。題幹以 Label Encoding"
        "泛稱類別轉整數；在 scikit-learn 官方 API 中，特徵 X 與目標 y 的編碼器名稱與用途應分開。"
    ),
    "references": [
        exam_ref(5),
        ref(
            "scikit-learn User Guide－Preprocessing data: Encoding categorical features",
            SKLEARN_PREPROCESSING,
            "OneHotEncoder 將每個類別轉成獨立二元欄，OrdinalEncoder 轉為單欄整數表示，並說明未知／低頻類別處理",
        ),
    ],
}

DRAFTS[6] = {
    "summary": "正確答案是 C。標準化會把資料調整為平均值 0、標準差 1，但不會同時把數值限制在 0 到 1；後者是 Min-Max Scaling 的特性。",
    "concept": (
        "常見數值縮放有兩種容易混淆的方法。Standardization 使用 z=(x-平均值)/標準差，讓訓練"
        "資料各欄平均約 0、變異數約 1，結果可小於 0 或大於 1；Min-Max Scaling 則以最小值與"
        "最大值線性映射，預設訓練資料範圍為 [0,1]。類別資料則需依是否有序選編碼；連續資料"
        "分箱會犧牲細節以換取規則或非線性的表達。"
    ),
    "answerReason": (
        "題目問不正確敘述。C 的前半段正確描述標準化，後半段卻又宣稱會壓到 0～1，把兩種"
        "縮放法合併成一項；Z 分數沒有上下界，因此 C 整體不正確。A、B、D 都同時寫出方法"
        "用途與其典型限制。"
    ),
    "optionAnalysis": {
        "A": (
            "敘述正確。One-hot 對每個名目類別建立二元欄，不強加順序；當類別數很多時欄位數"
            "隨之增加，矩陣可能非常寬，即使採稀疏儲存仍會增加模型與治理複雜度。"
        ),
        "B": (
            "敘述正確。把名目類別映射成單一整數欄雖節省空間，但某些模型會將編碼值視為"
            "具有大小與距離；若類別本來無序，這就是人為引入的錯誤結構。"
        ),
        "C": (
            "正確（本題要選不正確者）。標準化後的值是距平均值幾個標準差，可能為 -2、0.5"
            "或 3，沒有固定在 [0,1]。將最小值映為 0、最大值映為 1 才是 Min-Max Scaling。"
        ),
        "D": (
            "敘述正確。分箱把連續數值轉成區間，能形成易解釋的門檻；若邊界沒有依分佈與"
            "業務意義設計，相近數值可能被硬切到不同箱，或同箱內差異被抹除，造成資訊損失。"
        ),
    },
    "trap": (
        "看到「平均 0、標準差 1」就是 Standardization；看到「壓到 0～1」通常是 Min-Max。"
        "題目問的是不正確，C 前半句正確不代表整句正確，需檢查後半句是否偷換方法。"
    ),
    "references": [
        exam_ref(6),
        ref(
            "scikit-learn User Guide－Preprocessing data",
            SKLEARN_PREPROCESSING,
            "StandardScaler 的均值／變異數縮放、MinMaxScaler 的固定範圍映射，以及類別編碼與分箱方法",
        ),
    ],
}

DRAFTS[7] = {
    "summary": "正確答案是 C。原子性把一個交易視為不可分割的整體：所有操作全部提交，否則全部回復，不留下部分完成狀態。",
    "concept": (
        "ACID 的 Atomicity 處理的是交易內多個操作的成敗邊界。以轉帳為例，扣款與入帳必須"
        "共同成功；若中途失敗，資料庫要 rollback 已做的變更，使結果等同整筆交易從未發生。"
        "它不同於 Consistency 的規則維持、Isolation 的並行交易可見性，以及 Durability 的"
        "提交後持久保存。原子性也不要求每次只能執行一條 SQL，而是多個步驟對外呈現為一個單位。"
    ),
    "answerReason": (
        "C 的「不可分割、完全成功或完全失敗」就是 all-or-nothing 語意。PostgreSQL 官方交易"
        "教學也以多個帳戶更新說明：任何一步失敗時，先前步驟都不應對資料庫留下效果。"
        "其他選項分別混入資料型別、批次執行或分散式複寫概念。"
    ),
    "optionAnalysis": {
        "A": (
            "欄位型別由資料表 schema 與完整性約束決定，不同欄位本來就可分別是文字、數值或"
            "日期。原子性關心的是同一交易內的操作能否整體提交，不要求所有欄位同型別。"
        ),
        "B": (
            "交易可以包含一或多個敘述，也可由互動式請求觸發，不必以排程批次執行。"
            "批次描述工作如何被安排；Atomicity 描述失敗時要全部回復的成敗語意。"
        ),
        "C": (
            "正確。交易中的扣款、入帳等步驟形成一個不可分割單位，COMMIT 後全部生效；"
            "若失敗或 ROLLBACK，所有尚未提交的變更一起取消，避免半完成資料。"
        ),
        "D": (
            "跨節點同步屬於複寫、分散式一致性或高可用架構，不是 Atomicity 的定義。單機資料庫"
            "也能提供原子交易，而多節點系統則需額外協調才能維持跨節點交易語意。"
        ),
    },
    "trap": (
        "記住 Atomicity 是「全有或全無」，不是資料欄位的原子型別，也不是自動備援。"
        "ACID 四項常被交叉混淆：原子性管交易成敗，隔離性管並行可見，持久性管提交後不遺失。"
    ),
    "references": [
        exam_ref(7),
        ref(
            "PostgreSQL Documentation－Transactions",
            POSTGRES_TRANSACTIONS,
            "交易把多個步驟包成 all-or-nothing 操作；中途失敗時所有步驟都不影響資料庫",
        ),
    ],
}

DRAFTS[8] = {
    "summary": "正確答案是 B。用既有的銷售金額與瀏覽次數計算新欄位，是從原始特徵導出具業務意義的新特徵，屬於特徵衍生。",
    "concept": (
        "特徵衍生（feature derivation）是以一個或多個既有欄位透過算術、聚合或領域公式建立"
        "新的變數，例如單次瀏覽產生的銷售額、單價、成長率或時間差。它的價值在於把原始欄位"
        "之間的關係轉成模型可直接使用的訊號。本題的比值可能表示每次瀏覽的變現效率，但實作"
        "時要處理瀏覽次數為 0、缺值、極端比值，以及該欄位在預測當下是否可取得。"
    ),
    "answerReason": (
        "題目沒有刪除欄位，也沒有只是改變單一欄位的尺度，而是以兩個現有特徵做除法，產生"
        "原資料沒有的「銷售金額/瀏覽次數」欄位。這完全符合從既有資料衍生新特徵的 B。"
    ),
    "optionAnalysis": {
        "A": (
            "特徵選擇是在既有候選欄位中保留有用特徵、移除冗餘或高成本特徵，結果通常是欄位"
            "子集合。本題沒有選掉銷售金額或瀏覽次數，而是利用兩者新增一個比值欄。"
        ),
        "B": (
            "正確。將兩個原始欄位依業務公式組合，產生代表每次瀏覽平均銷售額的新變數，"
            "就是典型的特徵衍生；模型可直接使用這個新比例捕捉兩欄互動。"
        ),
        "C": (
            "廣義上衍生也屬於特徵工程中的轉換，但考題把類別分開時，Feature Transformation"
            "通常指對同一特徵做對數、縮放、標準化等表示轉換；本題明確由兩欄創造新語意，"
            "以衍生更精確。"
        ),
        "D": (
            "分箱把連續值切成若干區間，例如將年齡轉為青年、中年、熟齡。銷售額除以瀏覽次數"
            "仍是連續比值，沒有建立任何區間邊界，因此不是 Binning。"
        ),
    },
    "trap": (
        "判斷關鍵在「有沒有創造新語意欄位」：兩欄相除得到比例是衍生；同欄標準化或取對數"
        "通常叫轉換；挑選欄位叫選擇；切區間才叫分箱。另須防範分母為零。"
    ),
    "editorialNote": (
        "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。Feature derivation 與"
        "feature transformation 在部分教材中層級會重疊；依本題四個並列選項與新欄位語意，"
        "官方答案 B 是較精確分類。"
    ),
    "references": [
        exam_ref(8),
        ref(
            "Google Machine Learning Crash Course－Numerical data: Feature vectors",
            GOOGLE_FEATURES,
            "模型使用由資料欄位衍生、處理或轉換而成的 feature vectors；建立合適表示屬於 feature engineering",
        ),
    ],
}

DRAFTS[9] = {
    "summary": "正確答案是 C。Robust Scaling 使用中位數與四分位距縮放，較不會被少數極端值拉動，最適合含離群值的數值特徵。",
    "concept": (
        "縮放方法的穩健性取決於估計中心與尺度所用的統計量。Min-Max 使用最小與最大值，"
        "一個極端值就能拉大整體範圍；Z-score 使用平均值與標準差，兩者也會受離群值影響。"
        "RobustScaler 通常減去中位數，再除以四分位距 IQR（第 75 百分位減第 25 百分位）；"
        "這些排序統計量對少數極端值較不敏感，因此主要資料不會被壓縮在狹小區間。"
    ),
    "answerReason": (
        "題目已指定資料含極端值。C 所用的中位數與 IQR 不直接依賴極端值的大小，能在保留"
        "離群樣本的同時，以主要分佈為基準縮放。A 與 B 的尺度參數會被極端值拉動，D 則把"
        "連續資料離散化，不是同類的數值標準化方法。"
    ),
    "optionAnalysis": {
        "A": (
            "Min-Max Scaling 依訓練資料最小值與最大值映射範圍。若有一個非常大的離群值，"
            "最大值被拉遠，多數正常觀測會被擠在接近 0 的狹窄區域，故對極端值特別敏感。"
        ),
        "B": (
            "Z-score 以平均值與標準差為中心、尺度，適合分佈相對穩定且離群值不嚴重的情境。"
            "極端值會同時拉動平均與放大標準差，因此不是本題四項中最穩健的選擇。"
        ),
        "C": (
            "正確。中位數只取排序中央位置，IQR 只看中間 50% 資料的跨度；少數極大或極小值"
            "不會大幅改變這兩個統計量，因此縮放基準能代表主要資料群。"
        ),
        "D": (
            "分箱把連續數值轉成區間類別，可降低精確極端值的影響，但會失去箱內差異，且不是"
            "把數值特徵縮放到可比較尺度的方法。題目問 Normalization 時 Robust Scaling 更直接。"
        ),
    },
    "trap": (
        "不要因 Z-score 名稱含「標準化」就一律選它；平均值與標準差都不穩健。看到 Outliers，"
        "先想到中位數與 IQR。Robust Scaling 只是降低尺度受影響，並不會自動刪除或判定離群值。"
    ),
    "references": [
        exam_ref(9),
        ref(
            "scikit-learn API－RobustScaler",
            SKLEARN_ROBUST,
            "以訓練集 median 移除中心、依 quantile range（預設 IQR）縮放，避免 outliers 影響 mean/variance",
        ),
    ],
}

DRAFTS[10] = {
    "summary": "正確答案是 C。即時找出與個人平常交易模式明顯不同的可疑紀錄，正是異常偵測用來辨識罕見或偏離常態觀測的典型情境。",
    "concept": (
        "異常偵測關心某個新觀測是否與既有正常分佈或行為模式顯著不同，常用於詐欺、入侵、"
        "設備故障與品質監控。它特別適合異常樣本稀少、型態持續變化，難以事先完整標註每種"
        "異常的情境。若歷史標籤充分，詐欺偵測也可改成監督式分類；題目強調的是即時資料流中"
        "相對於平常行為的偏離，直接指向 anomaly detection。"
    ),
    "answerReason": (
        "C 的任務是從大量一般交易中找出少數不尋常紀錄，判準又明確寫為「與平常交易行為"
        "明顯不同」，完全符合異常／新奇觀測的定義。A、B 是有明確目標標籤的預測分類，D 是"
        "預測未來連續數量，目標並非找出罕見偏離。"
    ),
    "optionAnalysis": {
        "A": (
            "預測旺季是否缺貨，是依歷史需求、庫存與補貨資料預測一個已定義事件，可建成二元"
            "分類；若預測缺貨數量或時間，也可建成迴歸或時間序列模型。它不是以偏離正常模式"
            "作為主要判準。"
        ),
        "B": (
            "信用風險模型通常以過去是否違約的標籤學習新申請人的違約機率，屬於監督式二元"
            "分類。除非沒有標籤而改找異常財務行為，題目描述本身不需要 anomaly detection。"
        ),
        "C": (
            "正確。金融交易資料量大而可疑事件稀少，將每筆新交易與個人或群體的正常行為分佈"
            "比較，可即時標示低密度、罕見或顯著偏離的觀測，供攔截或人工覆核。"
        ),
        "D": (
            "用既有登入次數預測次日數量是時間序列預測或迴歸，輸出是未來的連續值。若任務改"
            "成偵測登入量突然暴增或異常來源，才會轉為異常偵測。"
        ),
    },
    "trap": (
        "不要只看到金融風險就選異常偵測；關鍵在輸出形式。預測已定義的違約標籤是分類，"
        "預測明日數量是迴歸／時間序列，找出與正常分佈不同的罕見觀測才是異常偵測。"
    ),
    "editorialNote": (
        "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。真實詐欺系統通常"
        "混合監督式分類、異常分數、規則與人工覆核；本題判定 C 是依其明確強調偏離平常行為。"
    ),
    "references": [
        exam_ref(10),
        ref(
            "scikit-learn User Guide－Novelty and Outlier Detection",
            SKLEARN_ANOMALY,
            "異常偵測用於判斷新觀測是否屬於既有分佈，或是否為 abnormal/unusual observation",
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
