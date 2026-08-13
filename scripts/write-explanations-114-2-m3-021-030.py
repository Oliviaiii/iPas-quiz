"""Write draft explanations for 114-2 intermediate subject three, Q21-Q30.

The script verifies official answers and refuses to overwrite reviewed work.
Run the draft validator before applying it to the shared question bank.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUESTIONS = ROOT / "app" / "data" / "questions.json"
SOURCE_ID = "aiap-114-intermediate-2-machine-learning"
AUTHOR = "Codex（AI 輔助初稿）"
AUTHORED_AT = "2026-08-12"
CHECKED_AT = "2026-08-12"

EXAM_PDF = (
    "https://www.ipas.org.tw/api/proxy/uploads/certification_resource/"
    "bf93f438f7be48d295c1b40a34d79f3d/114年第二梯次中級AI應用規劃師"
    "第三科機器學習技術與應用(當次試題公告114_20251226000650.pdf"
)
DEFAULT_NOTE = "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。"


def exam_ref(number: int) -> dict:
    return {
        "title": "114 年第二次中級 AI 應用規劃師－機器學習技術與應用公告試題",
        "url": EXAM_PDF,
        "locator": f"第 {number} 題題幹、選項與官方答案",
        "checkedAt": CHECKED_AT,
    }


def ref(title: str, url: str, locator: str) -> dict:
    return {"title": title, "url": url, "locator": locator, "checkedAt": CHECKED_AT}


EXPECTED_ANSWER = {
    21: "C", 22: "B", 23: "A", 24: "C", 25: "A",
    26: "D", 27: "D", 28: "C", 29: "D", 30: "C",
}

DRAFTS: dict[int, dict] = {}

DRAFTS[21] = {
    "summary": "正確答案是 C。多頭注意力把 Query、Key、Value 投影到不同表示子空間，各頭可同時關注不同位置與關係，再合併成較豐富的序列表示。",
    "concept": (
        "單一 attention 會以一組相似度加權整段序列。Multi-head Attention 使用多組"
        "可學習線性投影，每個 head 在較低維的 representation subspace 獨立計算"
        "attention；一個頭可能聚焦短距離發音片段，另一個捕捉語速或長距語意關聯。"
        "各頭輸出 concat 後再投影，使模型能在同一層並行表達多種關係。它的目標不是"
        "減少總參數，也不保證比單頭更快；梯度穩定主要還仰賴 residual connection、"
        "normalization 與最佳化設計。"
    ),
    "answerReason": (
        "C 幾乎直接重述 Transformer 原論文對 multi-head 的動機：讓模型共同關注"
        "不同位置、不同表示子空間的資訊。題幹所列發音、語速與語意多層次關係正好"
        "需要這種多樣化表徵。"
    ),
    "optionAnalysis": {
        "A": "多頭需要每個 head 的 Q/K/V 投影與最後輸出投影，並非專為減少參數；即使每頭維度縮小使總計算可控，與同維單頭相比參數量不一定更少。",
        "B": "各頭可在硬體上平行，但仍要計算多組投影與注意力矩陣；主要優點是表示能力與關係多樣性，不是保證端到端速度更快。",
        "C": "正確。不同 head 以不同投影查看序列，能分別學習局部聲學線索、時間節奏與長距語意依賴，再把互補資訊合併。",
        "D": "注意力縮短長距訊息路徑，可能有助最佳化，但多頭本身不是防止梯度消失的保證；殘差連接、正規化、初始化與啟用函數才是更直接因素。",
    },
    "trap": "『多頭』的多不是把同一答案重算多次，而是讓不同投影學不同關係。不要把可平行計算誤當成主要目的，也不要把 residual connection 的功勞算給 multi-head。",
    "references": [
        exam_ref(21),
        ref("Attention Is All You Need", "https://arxiv.org/abs/1706.03762", "第 3.2.2 節：multi-head attention 讓模型共同關注不同位置、不同 representation subspaces 的資訊"),
    ],
}

DRAFTS[22] = {
    "summary": "正確答案是 B。貝氏定理將購買／不購買的先驗機率與已觀察行為在各類別下的似然結合，得到給定特徵後兩類的後驗條件機率。",
    "concept": (
        "Bayes' theorem 可寫成 P(Y|X)=P(X|Y)P(Y)/P(X)。在購買分類中，Y 是會購買"
        "或不會購買，P(Y) 是歷史先驗比例，P(X|Y) 表示各類顧客出現目前瀏覽、停留"
        "與偏好特徵的可能性；正規化後得到 P(Y|X)，再選後驗較高類別或依成本設定"
        "決策閾值。Naive Bayes 另加『給定類別後特徵條件獨立』假設以簡化聯合似然，"
        "但貝氏定理本身不要求這項假設。它是機率分類，不是分群、金額迴歸或強化學習。"
    ),
    "answerReason": (
        "題幹關鍵句『觀察到這些行為特徵的情況下，會購買的機率』就是 P(購買|特徵)，"
        "B 正確描述以條件機率計算兩分類後驗。"
    ),
    "optionAnalysis": {
        "A": "依相似度自動分群是無監督式 clustering，不需要購買標籤；貝氏分類使用已知類別的先驗與似然估計後驗，任務與所需資料不同。",
        "B": "正確。模型比較 P(購買|行為) 與 P(不購買|行為)，它們由各類先驗及觀察特徵在該類下的 likelihood 依 Bayes rule 更新而得。",
        "C": "MSE 常用於連續數值迴歸，例如購買金額；題目目標是是否購買的二元事件機率，輸出與損失型態不同。",
        "D": "強化學習以行動、環境狀態與長期 reward 學策略，適合動態推薦決策；本題只有根據固定觀察特徵推斷類別機率，沒有行動回饋迴路。",
    },
    "trap": "先區分 P(X|Y) 與 P(Y|X)：模型需要的是看到行為 X 後購買 Y 的後驗，而 Bayes rule 用 likelihood 與 prior 反轉條件。",
    "references": [
        exam_ref(22),
        ref("scikit-learn User Guide－Naive Bayes", "https://scikit-learn.org/stable/modules/naive_bayes.html", "依 Bayes theorem 計算類別後驗 P(y|x)，並以最大後驗類別作分類"),
    ],
}

DRAFTS[23] = {
    "summary": "正確答案是 A。蒙地卡羅方法從輸入不確定性的機率模型反覆隨機抽樣，逐次計算發電量，彙整大量結果即可估計輸出分布、分位數與風險區間。",
    "concept": (
        "Monte Carlo simulation 以重複隨機抽樣近似難以解析求解的機率與積分。工程師"
        "先為日照、雲量、溫度及其相關性建立分布或情境生成器，每次抽出一組可能輸入，"
        "送入發電量模型得到一個未來結果；許多次結果的 empirical distribution 可估"
        "平均、變異、尾端風險及 prediction interval。模擬品質取決於輸入分布與關聯"
        "是否合理，抽樣次數只降低 Monte Carlo sampling error，無法修正錯誤假設。"
    ),
    "answerReason": (
        "題幹明示『隨機抽樣模擬多種可能情境』『估算機率分布與風險區間』，這兩個"
        "步驟就是 Monte Carlo 的定義，因此 A 唯一符合。"
    ),
    "optionAnalysis": {
        "A": "正確。反覆從氣候輸入的不確定分布取樣並計算三個月發電量，結果樣本可直接估計輸出分布與例如第 5、95 百分位的風險範圍。",
        "B": "K-means 將觀測依距離分成 K 群，能找典型天氣型態，但不會自動對不確定輸入重複抽樣，也不能直接產生未來發電量的機率區間。",
        "C": "SVR 可學輸入與連續發電量的預測函數，能作為每次模擬中的 response model；但單次點預測本身不等於用隨機情境估計整體分布。",
        "D": "Feature selection 挑出較有預測力的變數以簡化模型；它不生成隨機情境，也不對輸出不確定性與尾端風險做數值積分。",
    },
    "trap": "模型（例如 SVR）回答『給定一組天氣會發多少』，Monte Carlo 回答『天氣不確定時，所有可能發電量如何分布』；兩者可搭配但層級不同。",
    "references": [
        exam_ref(23),
        ref("NIST SP 1214－Economic Decision Guide Software User Guidance", "https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.1214.pdf", "Monte Carlo simulation 以重複隨機抽樣取得數值結果並傳播輸入參數不確定性"),
    ],
}

DRAFTS[24] = {
    "summary": "正確答案是 C。個別極大殘差提示離群或影響點，高價區殘差呈系統性彎曲則表示線性函數形式未捕捉非線性，兩者都違反理想隨機殘差型態。",
    "concept": (
        "合適線性迴歸的 residual-versus-fitted plot 應在零附近無規則散布，且變異大致"
        "穩定。遠離大多數點的殘差可能是 response outlier，還需用 leverage、Cook's "
        "distance 與資料稽核判斷影響力；笑臉／皺眉式彎曲代表遺漏二次項、交互作用"
        "或需要非線性模型。若高價區散布同時擴大，也可能有 heteroscedasticity，可"
        "考慮 log transformation 或加權回歸。殘差圖只能指出結構，不能單憑一張圖"
        "斷言特徵數不足或訓練集過擬合。"
    ),
    "answerReason": (
        "C 同時解釋題幹兩個跡象：極大殘差對應異常／影響樣本，系統性曲線對應線性"
        "規格錯置或非線性關係。D 與觀察相反，A、B 則無法由這些圖形直接唯一推出。"
    ),
    "optionAnalysis": {
        "A": "過擬合要比較訓練與未見資料的效能落差；一張訓練殘差圖有曲線只證明當前函數形式未捕捉結構，不足以判斷模型是否因過度複雜而泛化差。",
        "B": "彎曲可能表示遺漏非線性項或轉換，但不必然是『特徵數量不足』；現有特徵加入平方、交互或改用 nonlinear model 就可能改善，且極大殘差另指向 outlier。",
        "C": "正確。少數極端 residual 要檢查 outlier／influence；高價區有規律曲線表示線性模型的 E[ε|X]=0 或函數形式假設未滿足，應做模型重規格化。",
        "D": "隨機殘差應無明顯形狀且均勻分布於零線上下；題目已明說極端值和系統性彎曲，正是模型尚未符合假設的證據。",
    },
    "trap": "Residual plot 有曲線不等於過擬合，反而常表示現有模型太簡單或函數形式錯。極端殘差也要區分 response outlier、high leverage 與 influential point。",
    "references": [
        exam_ref(24),
        ref("NIST/SEMATECH e-Handbook－Graphical Residual Analysis", "https://www.itl.nist.gov/div898/handbook/pmd/section6/pmd614.htm", "殘差曲率揭露模型函數形式規格錯置，殘差圖用於檢查模型假設"),
        ref("NIST/SEMATECH e-Handbook－Regression Diagnostics", "https://itl.nist.gov/div898/software/dataplot/refman1/auxillar/regrdiag.htm", "殘差與診斷統計用於辨識 outlier、high leverage 與 influential points"),
    ],
}

DRAFTS[25] = {
    "summary": "正確答案是 A。傳統信用評分卡以分箱、WOE／IV、特徵與共線性篩選、邏輯迴歸及穩定性監控為主，不以生成式模型自動學習特徵。",
    "concept": (
        "傳統 scorecard 強調透明、單調與可稽核。常見流程先定義好／壞樣本與觀察窗，"
        "做資料品質處理，再把連續或類別變數分箱；以 Weight of Evidence 表示各箱，"
        "Information Value 輔助篩選，檢查共線性後用 logistic regression 估計違約機率，"
        "最後縮放成分數。驗證與監控會看 discrimination、calibration、back-testing、"
        "PSI 等穩定性指標。生成式深度模型可以是現代研究工具，但黑箱式 representation "
        "learning 不是『傳統評分卡標準流程』。具體監理要求仍依司法管轄與機構政策。"
    ),
    "answerReason": (
        "A 與題幹限定的傳統 logistic scorecard 不符。B、C 是建模前常見的可解釋"
        "變數治理，D 是開發／生產族群分布穩定性檢查，均屬常見流程。"
    ),
    "optionAnalysis": {
        "A": "正確（不是常見步驟）。生成式模型從大量資料學 latent representation，屬較新的複雜模型方法；傳統 scorecard 依人工可追溯變數、分箱與 logistic coefficients 建立，不需生成模型。",
        "B": "特徵選擇可刪除弱訊號或不穩定變數，共線性分析則避免高度相關變數使 logistic coefficient 不穩與解釋困難，屬評分卡建模常見治理。",
        "C": "Binning 將變數轉成風險相近且可解釋的區間，WOE 表示各箱好壞分布，IV 常作候選變數篩選參考，是傳統信用評分卡的代表步驟。",
        "D": "PSI 比較開發基準與後續樣本的分箱比例，可監控申請族群或模型分數分布是否漂移；它不直接證明效能下降，但屬常見穩定性警訊。",
    },
    "trap": "題目問『不是傳統流程』，不要因生成式模型很先進就選它。傳統評分卡的辨識詞是 binning、WOE/IV、logistic regression、PSI 與可解釋治理。",
    "editorialNote": "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。題幹稱『監理機關建議的標準化流程』但未指定主管機關或文件；各地監理要求不完全相同，本解釋只描述業界傳統 scorecard 慣例，不宣稱單一法定流程。",
    "references": [
        exam_ref(25),
        ref("SAS－Credit Risk Modeling Using SAS", "https://support.sas.com/resources/papers/proceedings16/2340-2016.pdf", "信用風險建模流程中的 binning、WOE、Information Value、變數選擇與 logistic regression"),
        ref("SAS Model Manager User's Guide", "https://documentation.sas.com/api/docsets/mdlmgrug/v_026/content/mdlmgrug.pdf?locale=en", "Performance Monitoring 章：PSI 衡量目前特徵／分數分布相對基準的變化"),
    ],
}

DRAFTS[26] = {
    "summary": "正確答案是 D。擴增輸入特徵通常增加模型可利用的資訊與假設空間，可能提高表達能力；它不是透過降低複雜度或限制學習來防止過擬合。",
    "concept": (
        "控制過擬合可限制有效容量或停止模型繼續貼合訓練雜訊。L1/L2 對大權重加"
        "懲罰，Dropout 訓練時隨機遮蔽單元、降低 co-adaptation，Early Stopping 在"
        "驗證表現不再改善時保留較早參數，三者都具有 regularization 效果。新增特徵"
        "可能帶來真正訊號而改善泛化，但也增加維度與搜尋自由度；若只是冗餘或噪音，"
        "會增加過擬合風險。因此 feature expansion 需要驗證、selection 或搭配正則化，"
        "不能本身歸類為降低模型複雜度。"
    ),
    "answerReason": (
        "題目問『不屬於』限制學習能力的方法。D 明說提升模型表達能力，方向與降低"
        "複雜度相反；A、B、C 都是教科書常見 regularization strategy。"
    ),
    "optionAnalysis": {
        "A": "L1/L2 在訓練目標加入係數懲罰，L1 可使權重歸零，L2 抑制過大權重；兩者限制模型對訓練資料做極端擬合，屬典型複雜度控制。",
        "B": "Dropout 訓練時隨機移除部分 activation，使網路不能依賴固定共適應路徑，相當於帶噪音的子網路集成，屬限制學習與正則化。",
        "C": "Early Stopping 監控驗證指標，在模型開始貼合訓練雜訊前停止並回復最佳 checkpoint，限制實際最佳化步數與有效容量。",
        "D": "正確（不屬於）。新增特徵擴大輸入表示，模型可建立更多關係；它可能提供有用訊號，但不是限制模型，未篩選時反而可能增加維度與過擬合。",
    },
    "trap": "『可能改善泛化』不等於『降低複雜度』。有用的新特徵可讓任務更容易，但 feature expansion 的機制是增加資訊／表達，不是像正則化般限制模型。",
    "references": [
        exam_ref(26),
        ref("Deep Learning（Goodfellow, Bengio, Courville）－Regularization for Deep Learning", "https://www.deeplearningbook.org/contents/regularization.html", "第 7 章涵蓋 parameter norm penalties、early stopping、dropout 等正則化方法"),
    ],
}

DRAFTS[27] = {
    "summary": "正確答案是 D。多層網路若每層都用線性 activation，整體仍只是單一線性轉換；改用 ReLU 可引入分段線性非線性，使 CNN 組合出複雜瑕疵特徵。",
    "concept": (
        "兩個 affine layer 中間若沒有 nonlinear activation，W₂(W₁x+b₁)+b₂ 仍可合併"
        "成 Wx+b，因此單純增加線性卷積層不提升函數類別。ReLU(x)=max(0,x) 在正半軸"
        "保留梯度、負半軸輸出零，多層堆疊可形成大量分段線性區域，學習邊緣、紋理"
        "到高階瑕疵的非線性組合。Sigmoid 也非線性，但兩端飽和、深層梯度較小，且"
        "把所有隱層 activation 限在 0 到 1，通常不如 ReLU 作 CNN 隱層預設選擇。"
    ),
    "answerReason": (
        "問題根因是 linear activation 缺乏非線性。D 直接替換成 ReLU，改變模型可"
        "表達的函數類別；A 若仍全部線性，再深也可合併，B 只改輸入，C 雖引入非線性"
        "但在深層 CNN 較易飽和。"
    ),
    "optionAnalysis": {
        "A": "若新增卷積層之間仍使用線性 activation，多層線性／affine transformation 可合併成一層，深度不會帶來所需的非線性表達，因此未處理根因。",
        "B": "灰階化降低通道數與運算，但也可能丟失顏色瑕疵訊號；它不改變網路每層皆線性的事實，無法讓模型學習複雜決策邊界。",
        "C": "Sigmoid 確實引入非線性並適合二元輸出機率，但作深層隱層時大正負輸入會飽和、梯度接近零；比起 ReLU 不是最合適的一般 CNN 隱層修正。",
        "D": "正確。ReLU 讓每層卷積後產生非線性分段表示，正區域梯度不飽和，能讓深層網路組合多層特徵並突破線性模型限制。",
    },
    "trap": "增加層數只有在層間有非線性時才增加表達能力。Sigmoid 不是『錯誤函數』，只是本題比較深層 CNN 隱層時，ReLU 通常更適合。",
    "references": [
        exam_ref(27),
        ref("Rectified Linear Units Improve Restricted Boltzmann Machines", "https://proceedings.mlr.press/v15/glorot11a.html", "ReLU 作為深層網路非線性單元的定義與實驗優勢"),
    ],
}

DRAFTS[28] = {
    "summary": "正確答案是 C。訓練集只收錄曾購買三次以上的活躍顧客，與部署時包含新會員、低消費會員的整體族群不具代表性，造成取樣偏差與分布落差。",
    "concept": (
        "Sampling Bias 發生在資料蒐集或納入條件系統性排除目標族群的一部分，使訓練"
        "樣本不能代表實際推論 population。本題 selection criterion 本身依活躍程度"
        "篩人，新會員與低消費會員幾乎不在訓練 support 中；模型因此沒學到這些人的"
        "特徵與流失關係，部署到全會員便 out-of-distribution。修正需重新定義 cohort、"
        "納入各客群並按時間切分，分析 coverage 與 subgroup metrics；若無法重抽樣，"
        "可做 reweighting，但不能創造完全缺失族群的資訊。"
    ),
    "answerReason": (
        "C 直接對應資料選取規則：只有高活躍者被抽進訓練集，而部署母體更廣。題目"
        "沒有人工標籤資訊，特徵也不是因與忠誠度相關就構成偏差；未調超參數更無法"
        "解釋特定群體特別差。"
    ),
    "optionAnalysis": {
        "A": "與會員忠誠度高度相關的合法預測特徵可能正是有用訊號；feature bias 通常涉及量測代理、遺漏或不公平表示，不能因相關性高就說應排除，且不解釋訓練 cohort 缺人。",
        "B": "Label Bias 要有主觀、不一致或系統性錯誤的標記來源；題目只說以去年紀錄訓練，沒有人工標註或標籤規則偏差的證據。",
        "C": "正確。納入條件『購買三次以上』刻意選出高活躍群，排除部署時要預測的新註冊與低消費者，形成 selection／sampling bias，導致 subgroup 泛化差。",
        "D": "超參數不足可能讓整體模型表現不佳，但不會特別造成未被訓練資料涵蓋的兩個族群失準；根因是資料代表性，不是再調同一偏樣本上的模型。",
    },
    "trap": "看到某群體特別差，先查該群體在訓練資料是否有代表性。模型再複雜、參數調得再好，也不能可靠外推到完全沒看過的資料區域。",
    "references": [
        exam_ref(28),
        ref("NIST SP 1270－Towards a Standard for Identifying and Managing Bias in AI", "https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.1270.pdf", "Statistical and computational bias 可源自樣本不代表母體；模型在一種資料訓練後可能無法外推到其他資料"),
        ref("NIST/SEMATECH e-Handbook－Data are randomly sampled from the process", "https://www.itl.nist.gov/div898/handbook/pmd/section2/pmd215.htm", "非代表性抽樣難由後續統計方法修正，資料須反映實際 process variation"),
    ],
}

DRAFTS[29] = {
    "summary": "正確答案是 D。時間序列交叉驗證或滑動視窗讓模型始終用較早資料訓練、較新資料驗證，並隨時間更新評估基準，較能揭露工況漂移下的真實泛化。",
    "concept": (
        "設備資料不服從可隨機交換的 i.i.d. 假設：季節、設備老化、維修策略與負載會"
        "讓分布隨時間變動。固定舊驗證集只回答模型對舊環境的表現。Expanding-window "
        "validation 累積過去訓練並驗證下一段，rolling-window 只保留最近固定期間，"
        "兩者都尊重時間因果並產生多個時段外樣本分數。應配合 drift monitoring、"
        "重訓觸發與最後 untouched test period。若變化是突發 regime shift，歷史驗證"
        "仍不能保證未來，但比固定舊切分更接近部署條件。"
    ),
    "answerReason": (
        "D 唯一直接解決驗證資料過時：隨時間向前滾動，讓選模與調參面對多個較新"
        "工況。正則化與簡化只控制容量，不能讓評估基準代表現況；不用驗證集則無法"
        "偵測泛化惡化。"
    ),
    "optionAnalysis": {
        "A": "L2 可抑制大權重，但固定舊驗證集仍只反映舊工況；分布已改變時，即使模型較平滑，也無法知道新環境是否適用。",
        "B": "把全部資料用來訓練後沒有獨立驗證指標，Early Stopping 就失去監控依據；若改看訓練損失，不能判斷泛化，更容易把時間洩漏藏起來。",
        "C": "降低參數可能減少 variance，但環境漂移屬資料分布問題；簡單模型仍可能在新工況系統性失準，也無法替代現況驗證。",
        "D": "正確。依時間順序設計多個 train-past／validate-future folds，並移動驗證窗口，可測量跨時段穩定性、選擇較穩健設定並及早發現舊模型不再代表現況。",
    },
    "trap": "時間資料不可隨機打散，否則未來工況會洩漏到訓練。正則化處理模型容量，rolling validation 處理評估代表性；題目根因在後者。",
    "references": [
        exam_ref(29),
        ref("scikit-learn API－TimeSeriesSplit", "https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html", "時間排序資料應避免未來訓練、過去評估；每折用先前資料訓練並以後續資料測試"),
    ],
}

DRAFTS[30] = {
    "summary": "正確答案是 C。模型從英文轉到西班牙文後無法辨識新的詞彙、形態與語境，會增加漏判情緒樣本的 FN、降低 Recall，進而拉低以 Precision 與 Recall 計算的 F1。",
    "concept": (
        "F1=2PR/(P+R)，macro F1 先對每個類別各算 F1 再等權平均。模型只在英文學得"
        "token、情緒詞與語法關係，西班牙文輸入造成 language/domain shift；tokenizer "
        "coverage、embedding 與語意模式若未跨語言對齊，真正的正負情緒容易被預測為"
        "其他類別，FN 上升使 recall 下降，F1 隨之下降。也可能同時有 FP 增加與 precision "
        "下降，完整診斷仍要查看每類 confusion matrix。改成 micro F1 只改聚合權重，"
        "不修復模型；MSE 也不適合取代分類指標。"
    ),
    "answerReason": (
        "C 提供了語言轉移到 F1 下降的合理因果鏈：跨語言特徵不匹配導致漏判、Recall "
        "下降，再使 F1 下降。A 把真實 domain shift 歸咎指標，B 的過擬合方向與『評估"
        "結果偏高』不符，D 則選錯任務指標。"
    ),
    "optionAnalysis": {
        "A": "Macro F1 對各類一視同仁，若西文資料每類都變差，它會忠實反映問題；micro averaging 由多數類樣本主導，可能掩蓋少數情緒類失敗，不能當作修復跨語言效能的方法。",
        "B": "模型未在西班牙文訓練，就不能說它對西班牙文訓練資料過擬合；而過擬合通常造成訓練分數高、外樣本低，選項卻說評估結果偏高，與觀察 0.58 不符。",
        "C": "正確。英文學到的關鍵詞和語境不能直接覆蓋西班牙文，使真實情緒樣本被漏判，FN 增加、Recall 降低；調和平均中的較低 Recall 會把 F1 一起拉低。",
        "D": "MSE 衡量連續數值誤差，若直接套分類標籤還會引入任意類別距離；情感分類應保留 precision、recall、F1、confusion matrix 等分類指標。",
    },
    "trap": "更換 averaging 方法只改報表，不會提升模型。F1 下滑要回到 Precision、Recall 與 confusion matrix 找 FP/FN，再查語言資料、tokenizer 與跨語言表示。",
    "editorialNote": "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。僅憑總體 macro F1 由 0.91 降至 0.58，不能確定一定是 Recall 單獨下降；C 是選項中最合理機制，但仍應以逐類 Precision／Recall 與 confusion matrix 實證確認。",
    "references": [
        exam_ref(30),
        ref("scikit-learn API－f1_score", "https://scikit-learn.org/stable/modules/generated/sklearn.metrics.f1_score.html", "F1 為 precision 與 recall 的調和平均；macro 與 micro averaging 的定義"),
        ref("BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding", "https://arxiv.org/abs/1810.04805", "BERT 以 token 與語境表示做語言任務；跨語言部署需相應詞彙與預訓練表示支持"),
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
