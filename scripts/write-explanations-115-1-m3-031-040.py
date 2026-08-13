"""Write draft explanations for 115-1 intermediate subject three, Q31-Q40.

The script verifies official answers and refuses to overwrite reviewed work.
Run the draft validator before applying it to the shared question bank.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUESTIONS = ROOT / "app" / "data" / "questions.json"
SOURCE_ID = "aiap-115-intermediate-1-machine-learning"
AUTHOR = "Codex（AI 輔助初稿）"
AUTHORED_AT = "2026-08-13"
CHECKED_AT = "2026-08-13"

EXAM_PDF = (
    "https://www.ipas.org.tw/api/proxy/uploads/certification_resource/"
    "bf93f438f7be48d295c1b40a34d79f3d/"
    "115年第一次中級AI應用規劃師_第三科_機器學習技術與應用_公告試題_20260615003428.pdf"
)
DEFAULT_NOTE = "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。"


def exam_ref(number: int) -> dict:
    return {
        "title": "115 年第一次中級 AI 應用規劃師－機器學習技術與應用公告試題",
        "url": EXAM_PDF,
        "locator": f"第 {number} 題題幹、選項與官方答案",
        "checkedAt": CHECKED_AT,
    }


def ref(title: str, url: str, locator: str) -> dict:
    return {"title": title, "url": url, "locator": locator, "checkedAt": CHECKED_AT}


EXPECTED_ANSWER = {
    31: "A", 32: "D", 33: "B", 34: "D", 35: "D",
    36: "B", 37: "A", 38: "C", 39: "A", 40: "B",
}

DRAFTS: dict[int, dict] = {}

DRAFTS[31] = {
    "summary": "正確答案是 A。代理人利用『每次抓取』的漏洞反覆刷分，屬於獎勵規格偏離任務目的；應把獎勵對齊完成一次有效揀貨。",
    "concept": (
        "強化學習會最佳化設計者實際給定的 reward，而不是自動理解設計者心中的業務目標。"
        "若中間行為可以重複計分，代理人可能達成高回報卻不完成訂單，這稱 specification gaming 或 reward hacking。"
        "獎勵塑形需把分數綁在不可重複計算的任務進度，例如物品成功放入正確位置、完成訂單，並可加入時間成本、重複動作懲罰與 episode 終止條件。"
    ),
    "answerReason": "A 直接修正代理人可刷分的獎勵漏洞：不再為單次抓取計分，而以一次完整、有效且不可重複的揀貨成果給獎勵。",
    "optionAnalysis": {
        "A": "正確。將 reward 從可重複觸發的抓取動作改成物品被正確搬到目的地的任務成果，可讓最大化累積回報與真正的倉儲效率一致。",
        "B": "降低學習率只能縮小參數更新步幅，可能讓訓練較穩；但目前策略正確地利用既有獎勵規則，學得再穩仍會反覆抓放，無法修正目標錯置。",
        "C": "信用分配處理延遲回報應歸因於哪些先前動作，advantage 可降低策略梯度變異；本題的回報立即且歸因清楚，問題是錯誤行為也能合法領獎。",
        "D": "災難性遺忘是學新任務後舊能力下降；experience replay 可重用經驗、降低相關性，但不會改變『重複抓取即可得分』的錯誤誘因。",
    },
    "trap": "先分清楚『學不會目標』與『把錯誤目標學得很好』。代理人高分但任務失敗時，應優先檢查 reward specification，而非只調 optimizer。",
    "references": [
        exam_ref(31),
        ref("Google DeepMind－Specification gaming: the flip side of AI ingenuity", "https://deepmind.google/blog/specification-gaming-the-flip-side-of-ai-ingenuity/", "代理人利用目標規格捷徑取得高 reward，卻未達設計者真正目的的案例與成因"),
    ],
}

DRAFTS[32] = {
    "summary": "正確答案是 D。F1 是 Precision 與 Recall 的調和平均，任何一項偏低都會明顯拉低分數，適合要求兩者兼顧時使用。",
    "concept": (
        "Precision 衡量被模型判為詐欺者中有多少是真的，Recall 衡量真詐欺中有多少被抓到。"
        "F1=2PR/(P+R)，等價於兩者倒數的算術平均再取倒數，因此比算術平均更受較小值影響。"
        "它在需要單一數字平衡兩者時有用，但不納入 true negatives，也不表達誤凍與漏抓的實際成本；若成本不對稱，可調 threshold 或採 F-beta。"
    ),
    "answerReason": "D 給出正確公式與調和平均性質；只有 Precision 或 Recall 其中一項很高，不能補償另一項過低，所以能反映兩者平衡。",
    "optionAnalysis": {
        "A": "(P+R)/2 是算術平均，例如 1 與 0 的平均仍為 0.5；F1 對同一組值為 0，更強烈反映其中一項完全失敗，因此兩者不可混用。",
        "B": "F1 對 Precision 與 Recall 對稱，並非只對 Precision 加權；需要偏重 Recall 或 Precision 時，才使用 beta 不等於 1 的 F-beta score。",
        "C": "F1 常用於類別不平衡情境，但並非只適用於不平衡或只適用於平衡資料；是否合適取決於是否關注正類檢出且可忽略 true negatives。",
        "D": "正確。調和平均 2PR/(P+R) 會向較小值靠近，要求模型同時維持 Precision 與 Recall，任一側明顯下降都會壓低 F1。",
    },
    "trap": "F1 不是算術平均，也不是把兩種錯誤成本自動設成業務成本。題目若特別要求偏重漏抓，應考慮 F-beta 或直接以成本選 threshold。",
    "references": [
        exam_ref(32),
        ref("scikit-learn API－f1_score", "https://scikit-learn.org/stable/modules/generated/sklearn.metrics.f1_score.html", "F1 的調和平均公式、Precision 與 Recall 定義"),
    ],
}

DRAFTS[33] = {
    "summary": "正確答案是 B。Ridge 的 L2 平方懲罰會共同縮小係數，在高度相關特徵下穩定估計，通常不會把係數精確壓成零。",
    "concept": (
        "多重共線性使多組係數都能產生相近預測，OLS 係數因而對樣本擾動敏感。Ridge 在殘差平方和加入 alpha×Σw²，"
        "以些許偏差換取較低變異，並將相關特徵的影響較平滑地分攤。Lasso 的 L1 懲罰可產生稀疏解；Elastic Net 同時含 L1，因此也可能歸零。"
        "題目要求保留全部特徵的係數，故 L2 最符合，但仍應先標準化並避免把冗餘係數當成獨立因果效果。"
    ),
    "answerReason": "B 同時滿足控制複雜度、緩和共線性係數不穩，以及不做稀疏特徵刪除三項條件，因此優於含 L1 或無正則化方案。",
    "optionAnalysis": {
        "A": "Lasso 以 L1 絕對值懲罰促成稀疏解，部分係數可精確成為零；它適合特徵選擇，但違反題目要求保留所有特徵係數。",
        "B": "正確。Ridge 對大係數施加平方懲罰並整體縮小權重，在相關特徵間通常分散影響，可降低係數變異且一般不會精確歸零。",
        "C": "Elastic Net 可利用 L2 處理相關群組，也保留 L1 的稀疏性；只要 L1 比例非零，仍可能把部分係數壓成零，不符合全部保留的明確要求。",
        "D": "OLS 不加入複雜度懲罰，高維與共線資料下係數可能高度不穩、標準誤變大；它雖不主動歸零，卻未滿足控制過擬合與穩定估計。",
    },
    "trap": "L1 的關鍵是 sparse／可歸零，L2 是 shrinkage／通常保留全部。『保留解釋能力』不代表 Ridge 係數就是因果效果，共線性仍會限制個別解讀。",
    "references": [
        exam_ref(33),
        ref("scikit-learn User Guide－Ridge regression and classification", "https://scikit-learn.org/stable/modules/linear_model.html#ridge-regression-and-classification", "Ridge 以 L2 penalty 處理係數大小與共線性，使問題更穩定"),
    ],
}

DRAFTS[34] = {
    "summary": "正確答案是 D。完整網格共有 3×4×5×3×3=540 組參數，每組做 5 folds，總計擬合 2,700 個模型。",
    "concept": (
        "Grid Search 會取各超參數候選集合的笛卡兒積，因此組合數是各候選數量相乘，而不是相加。"
        "K-fold 交叉驗證對每組參數輪流用 K−1 folds 訓練、剩餘一 fold 驗證，共需 K 次 fit。"
        "本題 540 組各做五次訓練，得到 2,700 次交叉驗證 fit；實作若最後再用最佳參數對完整資料 refit，還可能多一次，題目未把該步驟計入。"
    ),
    "answerReason": "五個網格維度必須全部排列組合，再乘上每組的 5-fold 訓練次數，所以 3×4×5×3×3×5=2,700。",
    "optionAnalysis": {
        "A": "把候選數量相加只算出清單中共有多少個值，沒有列舉 learning_rate 與其他四個參數的所有搭配，因此嚴重低估網格大小。",
        "B": "5×5 把『五種超參數』誤當成每種只有一個候選，再乘 folds；實際候選數不同，應先計算五個集合的笛卡兒積。",
        "C": "取最大候選數只適合每次單獨改一個參數等非完整網格策略；Grid Search 會測試不同參數之間的全部組合，不能只取最大值。",
        "D": "正確。參數組合為 540，5-fold 對每組擬合五次，故交叉驗證共訓練 2,700 個模型；若工具設定 refit，最終模型另計。",
    },
    "trap": "Grid Search 的組合數用乘法；Randomized Search 才是直接指定抽樣次數。工具預設的最佳參數 refit 是否另計，要看題目是否問全部 fit calls。",
    "references": [
        exam_ref(34),
        ref("scikit-learn API－GridSearchCV", "https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GridSearchCV.html", "參數網格的 exhaustive search、cross-validation 與 refit 行為"),
    ],
}

DRAFTS[35] = {
    "summary": "正確答案是 D。在固定可訓練參數預算下，降低單層 LoRA rank 並把 adapter 分配到更多層，可讓任務調整涵蓋更廣的模型深度。",
    "concept": (
        "LoRA 凍結原權重，對選定線性層加入低秩更新 BA；一個 d_in×d_out 權重的可訓練參數約為 r(d_in+d_out)，所以 rank 與套用層數共同決定參數及 optimizer state 記憶體。"
        "提高 rank 增加單層更新的表達維度；增加 target layers 則讓更多深度位置可適應任務。"
        "在固定總參數下，以較小 rank 覆蓋更多相關層可能比少數層高 rank 更能處理複雜資訊，但最佳分配依模型、資料與層敏感度而定，必須實驗驗證。"
    ),
    "answerReason": "D 是唯一明確維持 trainable 總參數近似不變、同時擴大適應層覆蓋面的方案，因而最符合顯存受限且想改善複雜條款摘要的條件。",
    "optionAnalysis": {
        "A": "提高 rank 可增加單層低秩更新容量，但可訓練參數、梯度與 optimizer state 也隨 rank 增加；顯存已近上限時，不符合不明顯增加記憶體的限制。",
        "B": "完整微調需為原模型大量權重保存梯度與 optimizer state，記憶體遠高於 LoRA；即使表達能力較大，也直接違反顯存限制。",
        "C": "降低 rank 並增大 batch 可改善梯度估計或吞吐，但會減少 adapter 表達容量，且沒有擴大可調整的模型位置，未直接回應複雜條款內容遺漏。",
        "D": "正確。在總 trainable 參數預算固定時，以較低 rank 將 LoRA 分配到更多注意力或 MLP 層，可讓更多深度位置參與任務適應，而不必明顯增加 adapter 記憶體。",
    },
    "trap": "rank 與 target modules 是兩個資源分配旋鈕，不是越大越好。固定參數量只控制部分顯存，activation、序列長度與 batch size 仍會影響總峰值。",
    "editorialNote": (
        "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。"
        "官方答案 D 是固定參數預算下合理的配置假設，但『較低 rank、更多層』不保證對每個模型與摘要資料都優於其他配置；"
        "實際效果取決於 target modules、rank 分配、序列長度與訓練資料，應以消融實驗確認。"
    ),
    "references": [
        exam_ref(35),
        ref("LoRA: Low-Rank Adaptation of Large Language Models", "https://arxiv.org/abs/2106.09685", "原始論文：凍結預訓練權重並在 Transformer 層注入可訓練低秩分解矩陣"),
    ],
}

DRAFTS[36] = {
    "summary": "正確答案是 B。同態加密允許雲端直接在密文上執行特定運算，解密運算結果後可得到對應的明文模型輸出。",
    "concept": (
        "同態加密（Homomorphic Encryption, HE）支援在加密資料上計算；伺服器不必持有解密金鑰，回傳的密文結果由資料方解密。"
        "全同態加密可組合加法與乘法以表示一般計算，但實務模型常需多項式近似、量化與參數調整，且有顯著延遲與密文膨脹成本。"
        "題目指定單一雲端、資料始終加密，與 HE 最吻合；這不代表模型參數、存取模式與端點風險都自動受到保護。"
    ),
    "answerReason": "法務條件的辨識關鍵是『單一服務商』『不解密』『直接對加密資料運算』，這正是同態加密提供的密文運算能力。",
    "optionAnalysis": {
        "A": "聯邦學習讓多個資料持有者在本地訓練並彙整模型更新，目的是資料不集中；本題是單一雲端對一筆加密輸入做推論，不是分散式訓練。",
        "B": "正確。同態加密讓雲端在看不到明文的情況下對密文執行支援的運算，產生加密預測結果，再由持有金鑰的一方解密。",
        "C": "差分隱私透過隨機化限制單筆資料對輸出或模型的影響，提供統計隱私保證；它不等於讓伺服器在從未解密的輸入上直接計算。",
        "D": "安全多方計算把祕密分散給多個互動參與者共同計算，適合不互信多方；題目明確要求由單一雲端服務商直接處理，因此 HE 更直接。",
    },
    "trap": "『資料不離開本地』常指 federated learning；『加入可證明噪音』是 differential privacy；『密文仍可運算』才是 homomorphic encryption。",
    "references": [
        exam_ref(36),
        ref("Microsoft SEAL－Homomorphic Encryption Library", "https://github.com/microsoft/SEAL", "同態加密可由雲端直接對加密資料運算，資料擁有者解密結果"),
    ],
}

DRAFTS[37] = {
    "summary": "正確答案是 A。SHAP 可針對單筆貸款預測，量化每個特徵相對基準值使輸出上升或下降的貢獻，屬於局部解釋。",
    "concept": (
        "局部可解釋性回答『這一筆為何得到此結果』，全域解釋則摘要模型在整體資料的行為。"
        "SHAP 以合作賽局 Shapley value 為基礎，把單一預測相對 expected value 的差異分配給各輸入特徵，因此可列出哪些因素推高或降低拒貸分數。"
        "SHAP 描述模型行為而非因果理由；高度相關特徵、背景資料選擇與模型近似都會影響歸因，監管說明仍需轉成可理解且合規的 reason codes。"
    ),
    "answerReason": "A 明確提供單筆預測的逐特徵貢獻，直接對應被拒申請的個案解釋；其餘選項不是單筆表格信用模型的局部理由。",
    "optionAnalysis": {
        "A": "正確。SHAP 將某申請的模型輸出與基準輸出差異分配到各特徵，可顯示收入、負債比等因素分別把風險分數往哪個方向推動。",
        "B": "全域特徵重要性摘要整體資料上哪些欄位常有影響，不能說明特定申請人的哪些特徵造成這一次拒絕；可作治理補充但不符合個案要求。",
        "C": "Grad-CAM 以卷積特徵圖梯度產生影像區域熱圖，適用 CNN 影像分類；貸款審核通常是表格特徵，且監管要的是欄位層級理由。",
        "D": "混淆矩陣彙總 TP、FP、TN、FN，評估整體分類錯誤型態；它不含單筆輸入特徵對某個預測的貢獻資訊。",
    },
    "trap": "Local explanation 解釋個案，global importance 解釋整體。SHAP 的 feature contribution 是模型歸因，不可直接寫成『此特徵造成違約』的因果結論。",
    "references": [
        exam_ref(37),
        ref("A Unified Approach to Interpreting Model Predictions", "https://papers.nips.cc/paper/7062-a-unified-approach-to-interpreting-model-predictions", "SHAP 原始論文：以 Shapley values 統一 additive feature attribution methods"),
    ],
}

DRAFTS[38] = {
    "summary": "正確答案是 C。統計均等要求不同敏感群體獲得正向決策的機率相同；55% 與 30% 明顯不同，因此不符合。",
    "concept": (
        "Statistical Parity／Demographic Parity 比較 P(預測為正向｜群體) 是否跨群體相等，不以個人真實資格或模型是否直接讀入敏感欄位為條件。"
        "男性通過率 0.55、女性 0.30，相差 0.25，已不符合嚴格相等定義。"
        "此指標只看選取率，不衡量各群體準確率、false positive 或 false negative；是否應採此公平準則還要結合職務資格、法規與其他公平指標。"
    ),
    "answerReason": "統計均等的判定量就是各群體正向決策比例。題目已提供兩組比例且不相等，不必知道模型準確率即可判定不符合。",
    "optionAnalysis": {
        "A": "不把性別直接當輸入稱為 fairness through unawareness，但其他特徵可能代理性別，使選取率仍不同；統計均等看輸出比例，不看欄位是否被明列。",
        "B": "兩群體都有人通過只表示通過率不是零；統計均等要求比例相同或在制度允許的容差內接近，55% 與 30% 不能因皆非零就視為相等。",
        "C": "正確。正向決策率分別為 55% 與 30%，條件機率 P(Ŷ=1｜A=group) 跨群體不一致，所以違反 statistical parity 的定義。",
        "D": "題目沒有提供各群體真實標籤或預測正確筆數，無法推論女性準確率較低；即使準確率相同，選取率不同仍可能違反統計均等。",
    },
    "trap": "Demographic parity 看 selection rate；equal opportunity 看真實正類中的 true positive rate。題目只有通過率，不能自行推論準確率或錯誤率。",
    "references": [
        exam_ref(38),
        ref("Fairlearn User Guide－Common fairness metrics", "https://fairlearn.org/main/user_guide/assessment/common_fairness_metrics.html", "Demographic parity 比較不同群體的 selection rate，與真實標籤無關"),
    ],
}

DRAFTS[39] = {
    "summary": "正確答案是 A。可在重新訓練時把群體錯誤拒絕差異寫入損失或約束，使模型學到較公平的決策規則，而推論時不必依性別另調門檻。",
    "concept": (
        "公平性介入可分前處理、訓練中與後處理。In-processing 在模型擬合階段把公平性約束或 penalty 納入最佳化，可針對 false negative rate 等群體差異尋找效能與公平折衷；"
        "部署後沿用學得的單一模型規則，不必在每次推論按性別切換 threshold。Post-processing 若依群體設不同門檻，則明確需要推論時取得敏感屬性。"
        "不論哪種重訓策略，都需合法取得受保護欄位作公平評估、留存審計證據並監控其他錯誤率。"
    ),
    "answerReason": "A 把公平修正放在訓練階段，部署時可使用同一模型輸出規則，不違反『推論階段不得用性別調整』的限制；C 則直接違反限制。",
    "optionAnalysis": {
        "A": "正確。重新訓練時以群體 false negative rate 差異建立 constraint 或 penalty，模型參數可吸收公平目標；部署時不需依申請人性別另設門檻。",
        "B": "重新採樣是可行的 pre-processing 候選，也不必在推論時使用性別；但選項限定它『僅』處理訓練資料且不能直接修正既有模型，若不重新訓練便不會改變已部署參數。",
        "C": "依性別分組調整 threshold 是典型後處理，必須在推論時知道每位申請人的群體才能選門檻，與法務限制直接衝突。",
        "D": "改用另一個評估指標不會自動改變模型參數或錯誤拒絕率；Demographic Parity 關注選取率，也不等同於對齊具有還款能力者的 false negative rate。",
    },
    "trap": "公平指標不會自己修模型；要有實際 mitigation。另要分清推論時按群體改 threshold 的 post-processing，與訓練時使用群體資料學出共同規則。",
    "editorialNote": (
        "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。本站作答判定仍依官方答案 A。"
        "但若允許重新訓練，B 所述的重新採樣也屬不需在推論階段使用性別的前處理策略；A 同樣無法在不重訓下『直接』改變既有模型。"
        "因此題目若要使 A 成為唯一答案，宜明確要求以訓練中公平性約束直接針對錯誤拒絕率最佳化，或說明排除前處理重訓。"
    ),
    "references": [
        exam_ref(39),
        ref("Fairlearn User Guide－Reductions", "https://fairlearn.org/main/user_guide/mitigation/reductions.html", "以公平性 moment 約束進行 in-processing reduction；敏感特徵用於訓練約束而非 estimator 的 predict 輸入"),
        ref("A Reductions Approach to Fair Classification", "https://proceedings.mlr.press/v80/agarwal18a.html", "將公平分類化約為具約束最佳化，涵蓋 error-rate parity 等條件"),
    ],
}

DRAFTS[40] = {
    "summary": "正確答案是 B。10 類單標籤輸出應以 softmax 形成總和為 1 的類別機率；One-Hot 標籤則搭配 categorical cross-entropy。",
    "concept": (
        "附圖程式的最後一層是 Dense(10)，每個 logit 對應數字 0 到 9。Softmax 將十個 logits 正規化為互斥類別的機率分布，推論時取最高機率類別。"
        "標籤已是長度 10 的 One-Hot 向量，所以 Keras 應使用 categorical_crossentropy；若標籤仍是整數 0～9，才使用 sparse_categorical_crossentropy。"
        "sigmoid 與 binary cross-entropy 適合各類別可獨立成立的多標籤問題，不符合本題每張圖只有一個數字。"
    ),
    "answerReason": "圖中輸出節點數為 10，題目又明示單標籤與 One-Hot 編碼，因此 (A) 應是 softmax，(B) 應是 categorical_crossentropy，選 B。",
    "optionAnalysis": {
        "A": "Sigmoid 會把十個輸出各自壓到 0～1，但不保證總和為 1，較適合多標籤；MSE 雖能計算 one-hot 差值，卻不是互斥類別機率的標準對數似然損失。",
        "B": "正確。Softmax 建立十類互斥機率分布，categorical cross-entropy 直接比較 one-hot 真實分布與預測分布，完全對應附圖的 Dense(10) 單標籤分類。",
        "C": "ReLU 常用於隱藏層，但輸出非負且不正規化成類別機率；binary cross-entropy 將各輸出當獨立二元標籤，適用一張圖可同時有多類的情境。",
        "D": "Tanh 輸出範圍為 −1 到 1，不能直接表示十類機率；sparse categorical cross-entropy 要求整數類別標籤，而題目已將標籤轉成 One-Hot。",
    },
    "trap": "先分單標籤或多標籤，再看標籤格式。單標籤＋one-hot 用 softmax＋categorical；單標籤＋整數用 softmax＋sparse categorical。",
    "references": [
        exam_ref(40),
        ref("Keras API－Dense layer", "https://keras.io/api/layers/core_layers/dense/", "Dense(units, activation) 的輸出維度與 activation 設定；對照附圖 Dense(10)"),
        ref("Keras API－Probabilistic losses", "https://keras.io/api/losses/probabilistic_losses/", "CategoricalCrossentropy 預期 one-hot labels；SparseCategoricalCrossentropy 預期整數 labels"),
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
