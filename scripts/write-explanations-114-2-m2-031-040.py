"""Write explanation drafts for 114-2 intermediate subject two, Q31-Q40.

The script validates official answers, refuses to overwrite reviewed content,
and leaves every generated explanation in ``draft`` status.

Usage::

    python scripts/write-explanations-114-2-m2-031-040.py
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
NIST_BINOMIAL = "https://www.itl.nist.gov/div898/handbook/eda/section3/eda366i.htm"
TAIWAN_PDPA = "https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=I0050021"
NIST_DEID = "https://www.nist.gov/publications/de-identification-personal-information"
STATSMODELS_QUANTREG = (
    "https://www.statsmodels.org/stable/generated/"
    "statsmodels.regression.quantile_regression.QuantReg.html"
)
NEO4J_GRAPH = "https://neo4j.com/docs/getting-started/graph-database/"
W3C_RDF = "https://www.w3.org/TR/rdf11-concepts/"
SCIPY_BOXCOX = "https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.boxcox.html"
IMBLEARN_SMOTE = (
    "https://imbalanced-learn.org/stable/references/generated/"
    "imblearn.over_sampling.SMOTE.html"
)
STATSMODELS_PROP = (
    "https://www.statsmodels.org/stable/generated/"
    "statsmodels.stats.proportion.proportions_ztest.html"
)
SKLEARN_STRATIFIED = (
    "https://scikit-learn.org/stable/modules/generated/"
    "sklearn.model_selection.StratifiedKFold.html"
)
SKLEARN_LOO = (
    "https://scikit-learn.org/stable/modules/generated/"
    "sklearn.model_selection.LeaveOneOut.html"
)

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
    31: "B", 32: "A", 33: "D", 34: "B", 35: "B",
    36: "B", 37: "C", 38: "B", 39: "D", 40: "B",
}

DRAFTS: dict[int, dict] = {}

DRAFTS[31] = {
    "summary": "正確答案是 B。二項分佈以常態近似前，應確認成功與失敗的期望次數 np、n(1-p) 都足夠大；本題分別為 2,000 與 3,000。",
    "concept": (
        "5,000 次相互獨立、每次成功機率固定為 0.4 的伯努利試驗，其成功總數 X 服從"
        "Binomial(n=5000,p=0.4)，平均數 np=2000、變異數 np(1-p)=1200。二項分佈在 n 大且 p"
        "不太靠近 0 或 1 時會接近鐘形，可用相同平均數與變異數的常態分佈近似。實務判斷不只"
        "看 n，而要同時看預期成功數 np 與預期失敗數 n(1-p)；兩者都大，左右尾才不會太偏。"
    ),
    "answerReason": (
        "B 提供了題目採用的明確檢核條件。代入 n=5000、p=0.4，得到 np=2000、n(1-p)=3000，"
        "兩者遠大於 5，所以本題確實可採常態近似。A 的結論在本題雖碰巧成立，理由卻只看樣本"
        "數，若 p 極接近 0 或 1，即使 n 大仍可能高度偏斜，因此 B 判斷較完整。"
    ),
    "optionAnalysis": {
        "A": (
            "大樣本是常態近似的重要條件，但不是單看 n 就能無條件使用；例如成功機率極小時，"
            "np 仍可能不足，成功數多集中在 0 附近而明顯偏斜。本題應實際檢查成功與失敗的"
            "期望次數，不能只寫「樣本數極大」就直接略過。"
        ),
        "B": (
            "正確。檢查 np 與 n(1-p) 可確保預期成功與失敗次數都不是太少；本題 2,000 與"
            "3,000 均通過題目採用的 >5 經驗門檻，因此常態近似合理。"
        ),
        "C": (
            "p=0.5 時二項分佈最對稱，確實很適合常態近似，但不是唯一情況。只要 n 足夠且 p"
            "沒有使成功或失敗期望次數太小，像本題 p=0.4 也可近似。"
        ),
        "D": (
            "二項分佈在適當條件下可由常態分佈有效近似，這是大型伯努利試驗快速計算機率的"
            "常見方法。宣稱無論樣本數多大都不能近似，否定了其漸近性質。"
        ),
    },
    "trap": (
        "不要只看到 n=5000 就選 A；要把 p 一起代入，檢查成功與失敗兩側。另要注意不同教材"
        "可能採 >5、≥5 或 ≥10 的經驗門檻，本題依官方選項 B 作答。"
    ),
    "editorialNote": (
        "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。常態近似門檻是經驗"
        "法則而非數學上的唯一必要充分條件；實際尾端機率計算可使用連續性修正或直接算二項機率。"
    ),
    "references": [
        exam_ref(31),
        ref(
            "NIST/SEMATECH e-Handbook－Binomial Distribution",
            NIST_BINOMIAL,
            "二項分佈由 n 次 Bernoulli trials 與成功機率 p 定義，平均數 np、標準差 sqrt(np(1-p))",
        ),
    ],
}

DRAFTS[32] = {
    "summary": "正確答案是 A。訓練前先匿名化或偽匿名化直接識別資訊，再對模型輸出持續稽核，是兼顧資料最小化與部署風險的多層控制。",
    "concept": (
        "姓名、電話與交易資訊可直接或間接識別個人，模型若在訓練資料中看見這些內容，可能在"
        "特定提示下重現。隱私治理應從資料生命週期處理：確認合法蒐集與特定目的、限制欄位與"
        "存取、在可行範圍去識別或以代碼取代識別碼，保護對照表，並在輸出端偵測、遮罩與留下"
        "稽核紀錄。匿名化與偽匿名化不是同義；後者仍可能透過額外資訊重新連結，通常仍需保護。"
    ),
    "answerReason": (
        "A 同時降低模型在訓練時接觸真實識別資訊的機會，並以輸出稽核處理模型仍可能洩漏的"
        "殘餘風險，符合縱深防禦。B 只調整行為，沒有移除來源資料；C 會讓模型無法正常處理"
        "明文語意且不等於匿名化；D 只遮姓名，遺漏電話、交易與其他可識別組合。"
    ),
    "optionAnalysis": {
        "A": (
            "正確。訓練前移除或替換姓名、電話、帳號等識別資訊，可降低記憶與重現風險；輸出"
            "端再用規則、偵測器與人工覆核攔截殘餘洩漏，並保留事件紀錄供治理與改善。"
        ),
        "B": (
            "強化學習或偏好微調可教模型拒答特定請求，是輸出行為控制的一部分，但不能保證模型"
            "忘記已看過的真實個資，也不能取代資料蒐集目的、最小化、存取與去識別等源頭治理。"
        ),
        "C": (
            "同態加密允許在特定密文運算中保護資料，但對一般大型語言模型的完整文字訓練與生成"
            "並非直接把所有輸入加密就能實用；若模型完全無法辨識內容也無法提供客服語意功能。"
            "加密傳輸或運算仍不會消除輸出洩漏與資料合法利用問題。"
        ),
        "D": (
            "不顯示姓名只能處理一種直接識別碼；電話、地址、訂單、交易紀錄或多欄組合仍可識別"
            "個人。隱私保護還需控制訓練資料、權限、保存與輸出，不能以單一遮罩宣告完成。"
        ),
    },
    "trap": (
        "不要把模型拒答當成已刪除訓練資料，也不要把「拿掉姓名」當成完整匿名化。題目要的是"
        "實務與法規原則，應選源頭去識別加輸出稽核的多層方案。"
    ),
    "editorialNote": (
        "本站自編的 AI 輔助詳解初稿，並非法律意見或官方詳解；尚待獨立人工複核。匿名化是否"
        "足以使資料不再可識別須依資料內容、可取得的外部資訊與重識別風險判斷；偽匿名化資料"
        "通常仍須依適用法令與組織政策保護。"
    ),
    "references": [
        exam_ref(32),
        ref(
            "全國法規資料庫－個人資料保護法",
            TAIWAN_PDPA,
            "第 2 條個人資料與處理／利用定義；第 5 條蒐集、處理或利用應尊重權益且不得逾越特定目的必要範圍",
        ),
        ref(
            "NISTIR 8053－De-Identification of Personal Information",
            NIST_DEID,
            "去識別降低蒐集、處理、保存與分享個人資訊的隱私風險，同時說明仍可能被重新識別",
        ),
    ],
}

DRAFTS[33] = {
    "summary": "正確答案是 D。分位數回歸直接估計報酬條件分佈的尾部分位，不必假設常態誤差，能針對極端損失區域建模。",
    "concept": (
        "普通最小平方法主要描述條件平均數，並以平方誤差配適；只用平均與標準差概括明顯偏態、"
        "厚尾的報酬資料，可能低估極端風險。分位數回歸改為估計給定解釋變數時某一個條件分位，"
        "例如較低的 1% 或 5% 報酬分位，並用不對稱絕對損失配適。它不要求殘差服從常態，還可"
        "比較不同分位下因子影響是否改變，因此適合聚焦損失尾端。"
    ),
    "answerReason": (
        "題目要求同時滿足不依賴常態假設與捕捉極端情況。D 直接把模型目標放在 tail quantiles，"
        "能估計不利市場情境下的條件報酬；A、B 仍以平均與常態尺度為中心，C 更把真正要評估的"
        "極端損失刪除，皆違反題意。"
    ),
    "optionAnalysis": {
        "A": (
            "線性迴歸可在不要求 Y 本身常態時估計平均關係，但若進一步用常態殘差推估尾端機率，"
            "就會與題目觀察到的偏態與極端損失不符。它關注條件平均，也不是直接估計尾部分位。"
        ),
        "B": (
            "平均數與標準差能摘要位置與離散程度，但都受極端值影響，且僅靠兩個數無法描述"
            "非對稱或厚尾形狀。若再套常態倍數推估風險，正是題目要避免的限制。"
        ),
        "C": (
            "裁剪 ±3σ 可能用於確認為量測錯誤的資料清理，但題目說多次極端損失是真實風險事件。"
            "把它們刪除會系統性低估尾部，而不是改善極端風險模型。"
        ),
        "D": (
            "正確。選擇低分位數可直接建模不利報酬尾端，無須把整個誤差分佈假定為常態；"
            "分析師也能比較中位數與尾部分位的條件關係，辨識風險因子在極端情境下的影響。"
        ),
    },
    "trap": (
        "極端損失不等於資料錯誤，風險模型最不該任意刪掉尾端。另要區分平均回歸與分位數回歸："
        "前者問平均報酬如何變，後者可直接問最差 1% 或 5% 的條件報酬如何變。"
    ),
    "editorialNote": (
        "本站自編的 AI 輔助詳解初稿，並非投資建議或官方詳解；尚待獨立人工複核。分位數回歸"
        "不等於完整的市場風險制度，實務仍須驗證時間相依、尾部分位樣本量、模型穩定性及回溯測試。"
    ),
    "references": [
        exam_ref(33),
        ref(
            "statsmodels API－QuantReg",
            STATSMODELS_QUANTREG,
            "Quantile Regression 估計條件分位，LAD 是 q=0.5 的特例",
        ),
    ],
}

DRAFTS[34] = {
    "summary": "正確答案是 B。使用者與貼文是實體節點，「按讚」是兩者間的關係；時間戳與裝置類型應存成該關係的屬性。",
    "concept": (
        "屬性圖（property graph）以節點表示實體、以有方向且具類型的關係表示實體間連結，兩者"
        "都可帶鍵值屬性。社群資料可建模為 `(User)-[:LIKED {timestamp, deviceType}]->(Post)`："
        "查詢某使用者按過哪些貼文時沿關係遍歷，篩選特定時段或裝置時直接使用關係屬性。這樣"
        "互動的兩個端點與互動當下的脈絡保存在同一筆關係中。"
    ),
    "answerReason": (
        "B 同時保留 User 到 Post 的直接關係，並把只屬於這次互動的 timestamp、device type"
        "附在邊上，語意與查詢需求完全對應。若互動本身還有評論、狀態流轉或需連到更多實體，"
        "才可能提升成獨立事件節點；題目只給簡單關係屬性時不必額外節點。"
    ),
    "optionAnalysis": {
        "A": (
            "把按讚建成節點可以支援複雜事件或讓多個實體連到同一互動，但選項只說與使用者"
            "建立邊，沒有連到被按讚的貼文，反而無法完整保留 User–Post 互動。對本題的簡單"
            "時間與裝置欄位也增加不必要的遍歷。"
        ),
        "B": (
            "正確。LIKED 關係直接由使用者指向貼文，時間與裝置是這次關係的脈絡，因此存成"
            "relationship properties 最自然；可同時依端點、關係類型與屬性查詢。"
        ),
        "C": (
            "把所有按讚寫入使用者節點會把與不同貼文相關的重複事件塞進單一屬性，難以保留"
            "每筆互動的端點與欄位，也不利於沿圖查詢哪些使用者按過某篇貼文。"
        ),
        "D": (
            "關聯表可用外鍵與欄位保存按讚紀錄，在關聯式系統中是合理設計；但題目已指定圖形"
            "資料庫並要求保留互動關係與查詢行為屬性，改放另一套資料庫會破壞圖模型的一致性。"
        ),
    },
    "trap": (
        "判斷資料屬於節點還是關係，先問它是可獨立存在的實體，還是兩個實體之間的一次連結。"
        "本題的 timestamp/device type 描述的是「這次按讚」，不是使用者永久屬性。"
    ),
    "references": [
        exam_ref(34),
        ref(
            "Neo4j Documentation－What is a graph database",
            NEO4J_GRAPH,
            "節點表示實體；relationship 連接 source/target 且可如節點一樣保存 properties",
        ),
    ],
}

DRAFTS[35] = {
    "summary": "正確答案是 B。RDF 以主詞、謂詞、受詞三元組明確表達實體與語意關係，能搭配共享詞彙、SPARQL 與推理規則擴充知識圖譜。",
    "concept": (
        "RDF 的基本陳述是 `(subject, predicate, object)`：主詞與受詞代表資源，謂詞以 IRI 表示"
        "兩者關係，多個三元組組成有向圖。由於類別、屬性與關係可使用可重用的 IRI 詞彙，"
        "內部報告、專利、作者與技術主題可跨資料來源對齊；再搭配 RDF Schema 或 OWL 的語意"
        "公理與 SPARQL 查詢，可做型別繼承、關係推論與跨來源連結。"
    ),
    "answerReason": (
        "B 不只保存節點與連線，還把每個關係表示成具明確謂詞語意的標準三元組，最能支援"
        "詞彙擴充、資料交換與規則推理。其餘選項可以儲存關聯或加速特定查詢，但未提供同等的"
        "標準化語意模型與可推理的詞彙機制。"
    ),
    "optionAnalysis": {
        "A": (
            "一般節點與邊可以表示圖結構，但把所有資訊都塞進節點屬性會弱化關係本身的語意，"
            "也沒有說明共享識別碼、詞彙或推理規則。它可作 property graph，卻不必然具備題目"
            "要求的語意擴展與知識推理能力。"
        ),
        "B": (
            "正確。Subject–Predicate–Object 讓「專利－發明人－專家」或「報告－涉及技術－主題」"
            "成為可組合陳述，IRI 詞彙可跨系統重用，並能搭配 RDF 語意與查詢標準。"
        ),
        "C": (
            "文件資料庫適合保存研究報告的異質內容，標籤也能做簡單分類；但 tag 通常只是文字"
            "或應用自訂欄位，沒有明確描述關係方向、範圍與可推理語意，難以支援複雜關聯推理。"
        ),
        "D": (
            "關聯式資料庫與索引能高效處理預先設計的表格與連接，資料完整性也強；但新增關係"
            "型別常需調整 schema，且 SQL join 本身不提供本體詞彙與語意蘊涵，並非本題最佳圖模型。"
        ),
    },
    "trap": (
        "知識圖譜不只是「有節點與邊」；題目強調語意擴展與推理時，要找能明確命名 predicate、"
        "重用詞彙與套用語意規則的資料模型，因此指向 RDF。"
    ),
    "references": [
        exam_ref(35),
        ref(
            "W3C Recommendation－RDF 1.1 Concepts and Abstract Syntax",
            W3C_RDF,
            "RDF graph 是 subject、predicate、object 三元組集合；predicate 表達 subject 與 object 的關係並以 IRI 識別",
        ),
    ],
}

DRAFTS[36] = {
    "summary": "正確答案是 B。對正值且右偏的應變數 Y 做 Box–Cox 冪次轉換，可降低偏態並穩定隨平均水準增加的變異，較符合線性迴歸需求。",
    "concept": (
        "線性迴歸的診斷重點在條件關係與殘差：若 Y 隨 X 增加而散布變寬，表示殘差可能異質"
        "變異；Y 又右偏時，可考慮單調的 Box–Cox family，依參數 lambda 對正值 Y 做冪次轉換，"
        "其中 lambda=0 對應對數。適當轉換可壓縮大值、降低右尾影響並讓變異較均一。完成後仍"
        "要用殘差圖重新檢查線性、等變異與異常點，不能只因轉換就視為假設已滿足。"
    ),
    "answerReason": (
        "問題同時出在 Y 的右偏與其條件變異隨 X 增大。B 直接作用於應變數，對大 Y 值做較強"
        "壓縮，能同時改善分佈形狀與漏斗狀變異。標準化 X 只改尺度，差分針對時間序列趨勢，"
        "刪除高變異樣本則可能任意丟失真實資料。"
    ),
    "optionAnalysis": {
        "A": (
            "標準化 X 只把解釋變數重新置中與縮放，不會改變 Y 的右偏形狀，也不會消除同一 X"
            "位置上殘差散布隨 X 增加的現象。它可改善數值尺度，卻未處理題目的兩個症狀。"
        ),
        "B": (
            "正確。Box–Cox 會在一族單調冪次轉換中選 lambda；對右偏正值資料，對數或較小冪次"
            "常可壓縮高值，使殘差較對稱並穩定變異，之後再重新配適與診斷。"
        ),
        "C": (
            "一次差分計算相鄰觀測差值，主要用於時間序列移除趨勢或單根。本題只描述 Y 與 X 的"
            "橫斷面關係，沒有時間順序；任意差分會改變研究問題且無法針對右偏。"
        ),
        "D": (
            "高變異不表示那些樣本錯誤。刪除散布大的觀測會縮小資料範圍、造成選擇偏差，也可能"
            "掩蓋真正的異質變異；應先建模或轉換，只有確認資料錯誤時才排除。"
        ),
    },
    "trap": (
        "先看問題出在 X 還是 Y：標準化 X 不會修復 Y 的偏態。Box–Cox 一般要求輸入為正值，"
        "若 Y 含 0 或負數，需要平移有合理依據，或評估 Yeo–Johnson 等替代方法。"
    ),
    "editorialNote": (
        "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。題目未明說 Y 全為正值，"
        "而標準 Box–Cox 需要正值；官方答案 B 隱含此前提。轉換後仍須做殘差診斷，必要時可考慮"
        "加權最小平方法或異質變異穩健標準誤。"
    ),
    "references": [
        exam_ref(36),
        ref(
            "SciPy API－scipy.stats.boxcox",
            SCIPY_BOXCOX,
            "Box–Cox power transformation、lambda 最大概似選擇，以及輸入須為正的一維非常數資料",
        ),
    ],
}

DRAFTS[37] = {
    "summary": "正確答案是 C。SMOTE 在少數類鄰近樣本間插值生成合成病例，比直接複製罕見樣本更能增加少數類變化並降低單純記憶的風險。",
    "concept": (
        "少數類不到 1% 時，只看準確率可能得到幾乎全猜多數類的模型。Random Oversampling 會"
        "重複既有少數樣本，模型容易反覆看見相同點；SMOTE 則選擇少數樣本的近鄰，在特徵空間"
        "兩點之間插值產生新樣本，讓分類邊界取得更多局部訊號。不過合成點未必代表真實患者，"
        "尤其樣本極少、混合類別特徵或離群點存在時需謹慎。重採樣只能在每個訓練折內執行。"
    ),
    "answerReason": (
        "C 直接增加少數類訓練訊號，又不只是把同一病例複製多次，因此在四個選項中最符合"
        "提升罕病偵測並降低單純過擬合的雙重要求。欠採樣會丟掉大量多數類資訊，調閾值只改變"
        "預測取捨而沒有增加模型學到的少數類結構。"
    ),
    "optionAnalysis": {
        "A": (
            "隨機過採樣以有放回方式重複少數病例，能平衡批次並提高少數類權重，但沒有新增"
            "特徵變化；同一批極少樣本被反覆呈現時，模型較容易記憶噪聲或個案細節。"
        ),
        "B": (
            "隨機欠採樣可快速平衡類別並縮短訓練，但本題少數類不到 1%，若把多數類降到相近"
            "規模，會捨棄大量正常病例與邊界資訊，使模型難以辨識正常族群的多樣性。"
        ),
        "C": (
            "正確。SMOTE 依少數類近鄰插值產生合成樣本，擴展少數類局部特徵空間，通常比單純"
            "複製更不易只記住原病例；應配合交叉驗證、合適距離與臨床合理性審查。"
        ),
        "D": (
            "降低決策閾值可提高召回率，但通常也增加假陽性；它沒有改變模型訓練或提供更多"
            "少數類結構。如果模型本身未學到罕病特徵，只移動閾值無法從根本改善辨識。"
        ),
    },
    "trap": (
        "SMOTE 只能套在訓練資料，若先對全資料 SMOTE 再切交叉驗證，合成樣本會把驗證資訊"
        "洩漏進訓練。另要用 recall、precision、PR-AUC 等不平衡指標，不要只報 accuracy。"
    ),
    "editorialNote": (
        "本站自編的 AI 輔助詳解初稿，並非醫療建議或官方詳解；尚待獨立人工複核。SMOTE 不保證"
        "避免過擬合，合成點也可能跨越類別邊界；罕病資料須在訓練折內重採樣，並由領域專家檢查"
        "特徵距離、合成合理性與病人層級切分。"
    ),
    "references": [
        exam_ref(37),
        ref(
            "imbalanced-learn API－SMOTE",
            IMBLEARN_SMOTE,
            "SMOTE over-sampling、少數／多數類比例設定、近鄰參數與 Chawla 等原始論文引用",
        ),
    ],
}

DRAFTS[38] = {
    "summary": "正確答案是 B。兩條獨立生產線各有成功件數與樣本數，要比較良率兩個母體比例，應使用雙比例 Z 檢定。",
    "concept": (
        "每件產品只有合格或不合格兩種結果，單條線的良率是成功比例而非連續平均數。兩獨立"
        "樣本比例檢定的虛無假設可寫成 H0:p_old=p_new，統計量以兩樣本比例差除以虛無假設下的"
        "標準誤；大樣本時用常態近似取得 Z 與 p 值。方向性題目「是否提升」可設單尾替代假設"
        "p_new>p_old。若成功或失敗件數太少，精確方法可能比常態近似更合適。"
    ),
    "answerReason": (
        "原線 95/100、新線 97/100，觀測與目標都是兩個獨立二項比例，B 的雙比例 Z 檢定正好"
        "直接檢驗兩良率差。t 檢定與 ANOVA 主要比較連續結果平均數；卡方 2×2 檢定可在雙尾"
        "大樣本下得到等價關聯檢定，但選項 B 對「兩比例差」與提升方向最直接。"
    ),
    "optionAnalysis": {
        "A": (
            "雙樣本 t 檢定比較兩組連續量的平均數，例如產品重量或強度。把每件合格編成 0/1"
            "雖可在特定大樣本下連結到比例比較，但針對良率的標準且直接方法是比例檢定。"
        ),
        "B": (
            "正確。輸入每組合格件數與總件數，檢驗 p_new-p_old 是否為 0（或是否大於 0），"
            "直接回答新產線良率是否有統計上顯著提升。"
        ),
        "C": (
            "2×2 卡方獨立性檢定可以檢查產線與合格狀態是否相關，在大樣本雙尾檢定下與兩比例"
            "Z 檢定平方關係密切；但題目明確比較兩個良率及提升方向，雙比例 Z 檢定更精確對應。"
        ),
        "D": (
            "ANOVA 用來比較多組連續反應的平均數，依組間與組內變異形成 F 統計量。只有兩條線"
            "且結果是合格比例，不需要以 ANOVA 處理。"
        ),
    },
    "trap": (
        "先辨認應變數型態：合格／不合格是二元結果，彙總後是比例，不是連續平均。另要分清楚"
        "「有統計差異」與「差 2 個百分點有實務價值」，後者還需信賴區間與成本判斷。"
    ),
    "editorialNote": (
        "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。本題每組失敗件數只有"
        "5 與 3，常態近似位於經驗門檻邊界；正式分析宜檢查方法假設，必要時使用 Fisher exact"
        "或其他精確／無條件方法。官方四選一答案仍為 B。"
    ),
    "references": [
        exam_ref(38),
        ref(
            "statsmodels API－proportions_ztest",
            STATSMODELS_PROP,
            "以成功次數與觀測數做常態 Z 比例檢定；兩樣本虛無假設為 prop[0]-prop[1]=value",
        ),
    ],
}

DRAFTS[39] = {
    "summary": "正確答案是 D。Stratified K-Fold 會讓每一折維持接近整體的良性／惡性比例，避免少數類在某些驗證折過少造成指標不穩。",
    "concept": (
        "一般 K-fold 只把樣本分成 K 組，不保證分類標籤比例；資料有 80% 良性時，未分層切分"
        "可能讓某折惡性病例特別少，甚至在更極端的小資料集中缺席，導致訓練與評估波動。"
        "Stratified K-Fold 依 y 分層，讓每折各類比例近似全資料，所有樣本仍輪流做一次驗證。"
        "它改善切分代表性，但不會處理病人重複、院所群組或時間洩漏，這些需另用 Group/Time split。"
    ),
    "answerReason": (
        "D 直接針對類別不平衡造成的折間比例差異，在每折保留約 80/20 的類別結構，讓各折"
        "評估可比較且少數類指標較穩定。降低 K 不保證比例，Bootstrap 仍可能抽到不平衡樣本，"
        "刻意提高測試集良性比例反而使少數類評估更困難。"
    ),
    "optionAnalysis": {
        "A": (
            "降低 K 會讓每個驗證折變大、訓練折變小，但若仍隨機切分，就沒有保證每折良惡性"
            "比例。它改變偏差與變異的取捨，沒有直接解決不平衡分配。"
        ),
        "B": (
            "Bootstrap 以有放回抽樣建立訓練樣本，可估計指標不確定性；但普通 bootstrap 也不"
            "保證每次抽樣維持類別比例，少數類仍可能不足，除非另外採分層設計。"
        ),
        "C": (
            "把測試集良性比例提高會讓惡性病例更少，召回率、precision 等少數類指標估計更不"
            "穩。若真實部署分佈為 80/20，應維持代表性，而不是刻意再放大多數類。"
        ),
        "D": (
            "正確。依標籤分層後，每折都近似保留 80% 良性與 20% 惡性，避免某折少數類過少，"
            "同時仍完成 K 折輪替，可得到較一致的分類效能估計。"
        ),
    },
    "trap": (
        "分層只確保標籤比例，不會自動讓模型公平、校準或處理不平衡損失。醫療資料若同一患者"
        "有多張影像，還要以患者為群組切分，否則同一人的資料可能同時落入訓練與驗證。"
    ),
    "references": [
        exam_ref(39),
        ref(
            "scikit-learn API－StratifiedKFold",
            SKLEARN_STRATIFIED,
            "以分層折疊保留各類別樣本百分比的 K-fold cross-validator",
        ),
    ],
}

DRAFTS[40] = {
    "summary": "正確答案是 B。附圖演算法逐一把第 i 筆當測試集、其餘 N−1 筆訓練，共重複 N 次並平均指標，正是留一交叉驗證。",
    "concept": (
        "Leave-One-Out Cross-Validation（LOOCV）是 K-fold 的極端情況，令 K=N。資料有 N 筆時，"
        "每一輪只留下 1 筆做測試，其餘 N-1 筆訓練；每筆恰好被測試一次，最後平均 N 個損失"
        "或評估值。它最大化每輪訓練資料量，但必須訓練 N 次，計算昂貴；單筆測試指標也高度"
        "離散，最終估計可能有較高變異。"
    ),
    "answerReason": (
        "已目視核對題庫官方附圖 `/images/questions/aiap-114-intermediate-2-big-data-p11-1.png`："
        "迴圈明寫 i=1 到 N，每輪第 i 筆為 test_data、其餘 N-1 筆為 train_data，然後平均"
        "metrics。這四個特徵完整對應 LOOCV，所以選 B。"
    ),
    "optionAnalysis": {
        "A": (
            "Hold-out 只做一次固定訓練／測試切分，不會讓每一筆資料輪流成為測試集，也不會"
            "依 i=1…N 重新訓練 N 次。附圖明顯是反覆交叉驗證。"
        ),
        "B": (
            "正確。每輪測試集大小為 1、訓練集大小為 N-1，且 N 筆依序各被留下來一次，"
            "正是 Leave-One-Out 的定義；最後回傳 N 次評估的平均。"
        ),
        "C": (
            "一般 K-fold 把資料分成 K 個包含多筆資料的折，每輪留一折測試，通常 K 遠小於 N。"
            "LOOCV 可視為 K-fold 的 K=N 特例，但題圖明確逐筆留一，因此專名 B 更精確。"
        ),
        "D": (
            "Bootstrap 每輪從原資料有放回抽取訓練樣本，同一筆可能重複出現，也會有部分資料"
            "未被抽中作 out-of-bag 評估。附圖沒有有放回抽樣，而是確定留下第 i 筆。"
        ),
    },
    "trap": (
        "看每輪測試集大小：1 筆就是 LOOCV；一整折是一般 K-fold；只切一次是 hold-out；"
        "有放回重抽樣才是 bootstrap。LOOCV 雖是 K=N 的 K-fold 特例，考題有專名時要選最精確者。"
    ),
    "editorialNote": (
        "本站已於 2026-08-12 目視核對 questions.json figures 所指官方裁切圖，確認其 i=1…N、"
        "單筆 test_data 與 N-1 筆 train_data 流程。本站內容仍為 AI 輔助詳解初稿，尚待獨立人工複核。"
    ),
    "references": [
        exam_ref(40),
        ref(
            "scikit-learn API－LeaveOneOut",
            SKLEARN_LOO,
            "每個學習集合用除一筆外的全部樣本建立，測試集合為被留下的單一樣本；等價於 K=n 的 KFold",
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
