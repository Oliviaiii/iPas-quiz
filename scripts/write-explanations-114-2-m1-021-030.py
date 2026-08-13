"""Write explanation drafts for 114-2 intermediate subject one, Q21-Q30.

The script validates each official answer before writing, refuses to overwrite
reviewed content, and leaves every generated explanation in ``draft`` status.

Usage::

    python scripts/write-explanations-114-2-m1-021-030.py
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUESTIONS = ROOT / "app" / "data" / "questions.json"
SOURCE_ID = "aiap-114-intermediate-2-ai-tech-planning"
AUTHOR = "Codex（AI 輔助初稿）"
AUTHORED_AT = "2026-08-12"
CHECKED_AT = "2026-08-12"

EXAM_PDF = (
    "https://www.ipas.org.tw/api/proxy/uploads/certification_resource/"
    "bf93f438f7be48d295c1b40a34d79f3d/"
    "114年第二梯次中級AI應用規劃師第一科人工智慧技術應用與規劃"
    "(當次試題公告114_20251226000616.pdf"
)
CVPR_MISSING_MODALITY = (
    "https://openaccess.thecvf.com/content/CVPR2023/html/"
    "Lee_Multimodal_Prompting_With_Missing_Modalities_for_Visual_Recognition_"
    "CVPR_2023_paper.html"
)
SCIPY_ENTROPY = (
    "https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.entropy.html"
)
GOOGLE_CANARY = "https://docs.cloud.google.com/deploy/docs/deployment-strategies/canary"
FDA_PCCP = (
    "https://www.fda.gov/medical-devices/software-medical-device-samd/"
    "predetermined-change-control-plans-machine-learning-enabled-medical-devices-"
    "guiding-principles"
)
NIST_AML = "https://csrc.nist.gov/pubs/ai/100/2/e2025/final"
USCO_AI_3 = (
    "https://www.copyright.gov/ai/"
    "Copyright-and-Artificial-Intelligence-Part-3-Generative-AI-Training-Report-"
    "Pre-Publication-Version.pdf"
)
LASSO = (
    "https://statistics.stanford.edu/technical-reports/"
    "regression-shrinkage-and-selection-lasso"
)
SPARK_STREAMING = (
    "https://spark.apache.org/docs/3.5.8/structured-streaming-programming-guide.html"
)
SKLEARN_PREPROCESSING = "https://scikit-learn.org/stable/api/sklearn.preprocessing.html"
SKLEARN_TARGET_ENCODER = (
    "https://scikit-learn.org/stable/modules/generated/"
    "sklearn.preprocessing.TargetEncoder.html"
)
GITHUB_CI = "https://docs.github.com/en/actions/get-started/continuous-integration"
NIST_DSS = "https://csrc.nist.gov/pubs/fips/186-5/final"

DEFAULT_NOTE = "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。"


def ref(title: str, url: str, locator: str) -> dict:
    return {"title": title, "url": url, "locator": locator, "checkedAt": CHECKED_AT}


def exam_ref(number: int) -> dict:
    return ref(
        "114 年第二次中級 AI 應用規劃師－人工智慧技術應用與規劃公告試題",
        EXAM_PDF,
        f"第 {number} 題題幹、選項與官方答案",
    )


EXPECTED_ANSWER = {
    21: "B", 22: "D", 23: "A", 24: "D", 25: "B",
    26: "D", 27: "C", 28: "C", 29: "B", 30: "A",
}

DRAFTS: dict[int, dict] = {}

DRAFTS[21] = {
    "summary": "正確答案是 B。讓模型在訓練時接觸並辨識各種模態缺失組合，才能在推論缺少文字或影像時仍使用現存模態做穩健預測。",
    "concept": (
        "多模態模型通常假設訓練與推論都有相同的影像、文字或聲音輸入；若某一模態缺失，"
        "融合層收到的分佈便與訓練時不同，效能可能明顯下降。模態缺失感知訓練會在訓練期"
        "模擬不同缺失型態，並利用遮罩、缺失模態提示或專門的融合策略，讓模型知道哪個輸入"
        "不存在，學會在可用模態之間調整權重。這是針對部署時缺失狀況直接建立的魯棒性。"
    ),
    "answerReason": (
        "B 把缺失情境納入模型的訓練目標，模型能分辨「資料真的為零」與「該模態沒有提供」，"
        "也能練習只依現存模態完成任務。CVPR 的缺失模態研究亦以模態缺失感知提示改善多種"
        "缺失組合下的表現，因此比固定填充值、事後猜測缺失內容或刪除資料更直接而普遍。"
    ),
    "optionAnalysis": {
        "A": (
            "零向量或固定向量能維持張量尺寸，適合作為工程上的占位符，但若訓練時沒有對應的"
            "缺失遮罩與情境模擬，模型可能把占位值誤認為真實訊號；固定填充本身不會教模型"
            "如何重新分配各模態的重要性，故不能有效保證效能。"
        ),
        "B": (
            "正確。訓練時主動模擬影像、文字等不同模態的缺失，搭配遮罩或缺失感知提示，"
            "使融合機制在推論時能辨認缺少哪個來源，並依仍可用的模態調整表示與決策。"
        ),
        "C": (
            "生成模型可在模態間關聯夠強時補出近似內容，屬於可採用的特定方案；但生成結果"
            "帶有不確定性，可能補出不存在的資訊，還要額外訓練與驗證生成器。題目問一般情境"
            "下最有效維持效能的策略，直接訓練缺失感知能力更穩健。"
        ),
        "D": (
            "捨棄不完整樣本可簡化只接受完整資料的訓練流程，卻會減少資料量並改變樣本分佈；"
            "推論階段遇到缺失模態時也無法把真實請求直接丟棄。它是資料排除策略，不是讓模型"
            "具備缺失容忍能力。"
        ),
    },
    "trap": (
        "不要把「維持輸入形狀」等同「維持模型效能」；固定填充只解決介面問題。另要區分"
        "缺失感知學習與生成式補值：後者可能有用，但補出的模態不是觀測事實。"
    ),
    "references": [
        exam_ref(21),
        ref(
            "Lee et al., Multimodal Prompting With Missing Modalities for Visual Recognition (CVPR 2023)",
            CVPR_MISSING_MODALITY,
            "摘要與方法：以 modality-missing-aware prompts 處理訓練或測試時的多種缺失模態情境",
        ),
    ],
}

DRAFTS[22] = {
    "summary": "正確答案是 D。KL 散度可量化目前輸入特徵分佈相對於訓練基準分佈的差異，適合用來確認是否發生資料漂移。",
    "concept": (
        "資料漂移是模型輸入資料的統計分佈隨時間改變，與模型準確率下降並非同一件事。"
        "偵測時要保存訓練期的基準分佈，再以相同分箱或密度估計方法建立近期分佈，逐特徵"
        "比較兩者。KL 散度 D_KL(P||Q) 衡量一個機率分佈相對於另一分佈的差異；數值越大，"
        "代表分佈差異越顯著。實作時要處理零機率、分箱與方向不對稱等限制。"
    ),
    "answerReason": (
        "題目要的是「偵測並確認」輸入分佈是否變化。D 直接比較訓練資料與上線後資料的"
        "特徵分佈，能產生可追蹤的漂移量；其餘選項是可能的後續處置、模型改造或評估樣本"
        "調整，都沒有直接回答兩期輸入分佈是否不同。"
    ),
    "optionAnalysis": {
        "A": (
            "定期重訓可在已確認漂移且新資料品質足夠後更新模型，是漂移治理的處置手段。"
            "但未先量測分佈就重訓，無法證明準確率下降源於資料漂移，也可能把資料品質問題"
            "或標籤錯誤一併帶入新模型。"
        ),
        "B": (
            "提高模型複雜度可增加擬合非線性關係的能力，適用於原模型容量不足的欠擬合。"
            "它不會比較訓練期與目前資料分佈，且更複雜的模型仍會受到分佈改變影響，甚至可能"
            "增加過度擬合風險。"
        ),
        "C": (
            "增加測試資料量能降低效能估計的抽樣波動，使準確率估計更穩定；但測試集大小"
            "本身不是分佈差異指標。即使準確率估得很精確，仍需另行比較輸入特徵分佈才能"
            "判定 Data Drift。"
        ),
        "D": (
            "正確。把訓練期特徵分佈作為基準 P、近期特徵分佈作為 Q，計算 KL 散度即可量化"
            "兩者差距，並可依特徵與時間窗口持續監控；實務上須平滑零機率並設定告警門檻。"
        ),
    },
    "trap": (
        "先分清楚偵測與修復：KL 散度用來量測漂移，重新訓練才是可能的後續處置。"
        "也不要把效能下降直接當成資料漂移證據，概念漂移、標籤品質或服務錯誤也可能降準確率。"
    ),
    "editorialNote": (
        "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。KL 散度不對稱且遇到"
        "零機率可能為無限大，實務可依資料型態評估平滑、Jensen-Shannon divergence、PSI 或"
        "統計檢定；本站作答仍依官方答案 D。"
    ),
    "references": [
        exam_ref(22),
        ref(
            "SciPy API Reference－scipy.stats.entropy",
            SCIPY_ENTROPY,
            "定義：當 qk 提供時，計算相對熵即 Kullback-Leibler divergence，並列出計算公式",
        ),
    ],
}

DRAFTS[23] = {
    "summary": "正確答案是 A。先在單一專科或病房以明確邊界試行，才能限制臨床風險、集中回饋並在驗證後逐步擴大。",
    "concept": (
        "漸進式部署的核心不是單純把上線時間切段，而是先把新系統暴露範圍限制在可管理的"
        "使用者或流程，持續監測安全性、效能與工作流程影響，再依預先設定的通過條件擴大。"
        "醫療情境還需讓特定科別建立責任人、例外處置與回復機制。這種有邊界的試行可讓回饋"
        "來自相對一致的臨床場景，問題也容易定位。"
    ),
    "answerReason": (
        "A 以單一專科或特定病房界定第一批使用範圍，既能取得真實臨床回饋，又把影響限制在"
        "可監控區域；通過安全與流程驗證後才逐步擴至全院，符合先小範圍、監測、再擴大的"
        "漸進式部署原則。"
    ),
    "optionAnalysis": {
        "A": (
            "正確。專科或病房是具明確人員、病例型態與流程責任的部署單位，便於設定基準、"
            "收集一致回饋及快速停用；逐階段擴大也能把前一階段經驗帶到下一個場域。"
        ),
        "B": (
            "急診病例量高且病況多變、時間壓力大，雖能快速累積使用資料，卻把尚未充分驗證的"
            "系統先放進高風險、高衝擊流程。它追求回饋速度，沒有優先滿足風險可控與臨床衝擊"
            "最小化的要求。"
        ),
        "C": (
            "只在夜班或離峰啟用是依時間切分，不是依臨床場景建立可控試行群組。夜班人力可能"
            "較少，支援與監測反而不足；所得回饋也可能偏向特定時段，不能代表主要流程。"
        ),
        "D": (
            "提示模式若不影響診斷可作為影子測試的一部分，但讓全院同步接觸仍擴大了介面、"
            "訓練與認知負擔，回饋來源也過於分散。它欠缺由小範圍驗證後逐級擴展的核心邊界。"
        ),
    },
    "trap": (
        "漸進式部署的重點是限制「暴露範圍」並設定升級條件，不只是選離峰時段。醫療部署"
        "也不是回饋越多越好；先選流程可控、支援充足的場域，比直接進入高量急診安全。"
    ),
    "references": [
        exam_ref(23),
        ref(
            "Google Cloud Deploy－Use a canary deployment strategy",
            GOOGLE_CANARY,
            "說明 canary deployment 先向部分使用者發布，確認可靠後再完整推出",
        ),
        ref(
            "FDA, Health Canada and MHRA－PCCP Guiding Principles for ML-enabled Medical Devices",
            FDA_PCCP,
            "部署後模型應監測效能，並管理偏離與再訓練風險",
        ),
    ],
}

DRAFTS[24] = {
    "summary": "正確答案是 D。防火牆管制網路來源，無法修補模型會被細微惡意特徵擾動欺騙的對抗性脆弱性。",
    "concept": (
        "題幹描述的是推論階段的規避攻擊（evasion attack）：攻擊者刻意微調輸入，讓樣本仍看似"
        "合理，卻跨過模型決策邊界。防禦要作用在輸入、模型或輸出決策，例如偵測異常輸入、"
        "以對抗樣本訓練提高魯棒性，或用業務規則限制高風險結果。網路邊界控制則處理誰能連線，"
        "攻擊者若透過合法帳號或獲准通道送出惡意樣本，防火牆仍看不出語意擾動。"
    ),
    "answerReason": (
        "題目問何者「並非」針對此攻擊型態的技術手段。D 只能阻擋未授權網路連線，保護部署"
        "環境的存取邊界；它不檢查特徵擾動，也不改變模型決策邊界，因而沒有從根本處理模型"
        "對對抗樣本的脆弱性。"
    ),
    "optionAnalysis": {
        "A": (
            "輸入驗證與前處理可攔截格式不符、超出合理範圍或部分可辨識的異常輸入，屬於攻擊"
            "面前端的緩解措施。它未必能抓到刻意保持在合法範圍內的微小擾動，不能單獨視為"
            "完整防禦，但仍直接處理可疑輸入。"
        ),
        "B": (
            "對抗訓練把攻擊生成的擾動樣本加入訓練，讓模型學習在這些鄰域維持正確判斷，"
            "是直接改善模型魯棒性的典型方法。不過其保護通常受攻擊假設與擾動範圍限制，"
            "不代表對所有未知攻擊免疫。"
        ),
        "C": (
            "推論後規則引擎可把模型輸出與授信上限、人工覆核門檻等硬性規則交叉檢查，"
            "即使攻擊成功改變分數，也可能阻止不合業務約束的動作。它沒有修補模型本身，"
            "但仍是針對攻擊後果的縱深防禦。"
        ),
        "D": (
            "正確（本題要選並非針對對抗性擾動者）。防火牆依位址、連接埠或網路身分管制"
            "連線，能降低未授權存取，卻無法分辨合法連線中的正常特徵與惡意微擾，也不會"
            "提高模型對對抗樣本的魯棒性。"
        ),
    },
    "trap": (
        "先看題目是否有否定詞「並非」。再區分網路存取攻擊與模型規避攻擊：防火牆保護"
        "傳輸入口，對抗訓練與輸入／輸出控制才處理模型被特製樣本欺騙的風險。"
    ),
    "editorialNote": (
        "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。A 與 C 都只是有限的"
        "縱深防禦，並非保證能根除對抗性脆弱性；官方答案 D 的判準在於它處理的是網路授權來源，"
        "與惡意特徵擾動最不相干。"
    ),
    "references": [
        exam_ref(24),
        ref(
            "NIST AI 100-2 E2025－Adversarial Machine Learning: A Taxonomy and Terminology of Attacks and Mitigations",
            NIST_AML,
            "Predictive AI 的 evasion attacks、攻擊生命週期與相應緩解方法分類",
        ),
    ],
}

DRAFTS[25] = {
    "summary": "正確答案是 B。從資料來源端先做權利盤點、授權驗證與高風險排除，最能在模型訓練前預防企業使用未授權作品。",
    "concept": (
        "生成式 AI 的著作權風險可能發生在資料集建立、訓練複製、模型提供與輸出使用等不同"
        "環節，不能用單一技術保證合法。題目問的是「預防侵權問題產生」，因此應優先採源頭"
        "治理：保留資料來源、權利人、授權條款、允許用途與期限的證據，排除權利不明或用途"
        "不符的資料。輸出比對與可追溯技術則是下游偵測或問責，無法回頭補正訓練資料授權。"
    ),
    "answerReason": (
        "B 在資料進入訓練或微調前確認來源與授權範圍，直接降低企業複製、使用高風險內容的"
        "機會，也能留下合規稽核紀錄。相較之下，A 與 D 都發生在輸出端，C 的差分隱私目標是"
        "降低個別資料被推知或記憶的隱私風險，不等於取得著作權授權。"
    ),
    "optionAnalysis": {
        "A": (
            "輸出語意相似度比對可標出疑似近似既有作品的結果，適合發布前人工覆核；但相似度"
            "不是著作權侵權的法律判定，也可能漏掉資料訓練階段的權利問題。它是下游偵測，"
            "晚於來源端授權治理。"
        ),
        "B": (
            "正確。建立來源清冊、驗證授權條款與允許用途，並排除未授權或權利不明資料，"
            "能在資料被複製進訓練流程前降低風險；同時留下可供法務與稽核查驗的權利鏈紀錄。"
        ),
        "C": (
            "差分隱私透過限制單一樣本對模型輸出的影響來降低隱私洩露與成員推論風險，"
            "可能間接降低逐字記憶，但它不會判斷作品權利歸屬，也不會使未經授權的利用自動合法。"
        ),
        "D": (
            "浮水印或數位指紋可標示內容來源、協助追蹤散布與事後究責，屬於可追溯性控制。"
            "它無法證明訓練資料已獲授權，也不能阻止模型先生成可能侵權的內容，因此不是最有效"
            "的源頭預防措施。"
        ),
    },
    "trap": (
        "注意題目問「預防」而非「發現」或「追溯」：授權驗證在資料進入前控制，語意比對與"
        "浮水印在輸出後控制。也不要把差分隱私誤當著作權授權機制。"
    ),
    "editorialNote": (
        "本站自編的 AI 輔助詳解初稿，並非法律意見或官方詳解；尚待獨立人工複核。著作權是否"
        "受侵害須依適用法域、具體利用行為、授權條款與例外規定逐案判斷；資料授權治理只能"
        "降低風險，不能保證所有模型輸出均不侵權。"
    ),
    "references": [
        exam_ref(25),
        ref(
            "U.S. Copyright Office－Copyright and Artificial Intelligence, Part 3: Generative AI Training",
            USCO_AI_3,
            "訓練資料集建立、訓練複製與模型利用是不同活動；報告討論授權市場及潛在責任配置",
        ),
    ],
}

DRAFTS[26] = {
    "summary": "正確答案是 D。LASSO 的 L1 懲罰會收縮迴歸係數，部分係數可降為零，能在高度相關特徵中進行正則化與變數選擇。",
    "concept": (
        "多重共線性表示解釋變數之間高度相關，傳統最小平方法雖仍可預測，個別係數卻可能對"
        "樣本小變動非常敏感，標準誤變大、解釋不穩。LASSO 在平方誤差之外加入係數絕對值"
        "總和的 L1 懲罰；懲罰強度增加時係數被收縮，部分可精確變成零，因而同時達成正則化"
        "與特徵選擇。高度相關變數中，LASSO 常保留其中部分代表，但選擇結果仍可能不穩。"
    ),
    "answerReason": (
        "D 是四個選項中唯一明確針對迴歸係數加入正則化的模型。L1 懲罰限制係數幅度並可移除"
        "冗餘特徵，相較無正則化線性迴歸更能減輕共線性造成的係數不穩；題目要求房價預測且"
        "優先降低參數估計負面影響，因此選 D。"
    ),
    "optionAnalysis": {
        "A": (
            "決策樹以特徵切分預測，不以反矩陣估計線性係數，確實不會出現傳統線性迴歸那種"
            "共線性係數膨脹；但高度相關特徵仍會讓切分選擇不穩，而且選項沒有提供可解釋的"
            "線性參數估計。題目在所列模型中要優先降低迴歸係數問題，LASSO 更切題。"
        ),
        "B": (
            "無正則化的傳統線性迴歸正是多重共線性最直接影響的模型：相關特徵使設計矩陣"
            "接近奇異，個別係數可能大幅波動。它沒有任何收縮或變數選擇機制，不能主動降低"
            "題目所述負面影響。"
        ),
        "C": (
            "線性核支持向量機以間隔或 epsilon-insensitive loss 建模，正則化可控制模型複雜度，"
            "但選項未指明用於連續房價的 SVR，也不是以稀疏係數選擇高度相關特徵為主要設計。"
            "相較之下 LASSO 與題目的迴歸及係數估計語境直接對應。"
        ),
        "D": (
            "正確。LASSO 將 L1 懲罰加入迴歸目標，收縮相關特徵的係數，並可把部分係數壓到零，"
            "降低冗餘變數對估計穩定性的影響；懲罰強度應以交叉驗證選擇。"
        ),
    },
    "trap": (
        "不要把「決策樹不需要線性共線性假設」誤解成它必然是本題最佳模型；題目強調的是"
        "房價迴歸的參數估計。另要注意 LASSO 不保證在一組高度相關特徵中穩定選出同一個代表。"
    ),
    "editorialNote": (
        "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。若目標是讓一組高度"
        "相關特徵共同保留且穩定收縮，Ridge 或 Elastic Net 往往也是重要候選，但不在本題選項中。"
    ),
    "references": [
        exam_ref(26),
        ref(
            "Tibshirani－Regression Shrinkage and Selection via the Lasso (Stanford Statistics)",
            LASSO,
            "原始技術報告：LASSO 以係數絕對值總和約束達成收縮與變數選擇",
        ),
    ],
}

DRAFTS[27] = {
    "summary": "正確答案是 C。遞迴展開巢狀 JSON 能保留欄位語意，再依事件時間窗口聚合計數、頻率與統計量，最適合產生故障預測的時序特徵。",
    "concept": (
        "系統日誌是半結構化資料：同一事件可含巢狀物件、陣列與可選欄位。特徵工程應先依"
        "schema 解析型別與欄位路徑，把巢狀結構遞迴展開，同時保留事件時間、設備與事件類型等"
        "關聯；再用固定、滑動或工作階段窗口聚合錯誤次數、延遲平均、最大值與變化率。這樣才"
        "能把一連串事件轉為模型可用且不洩漏未來資訊的時序特徵。"
    ),
    "answerReason": (
        "C 同時處理題目的兩個關鍵：遞迴函式保留並展開複雜巢狀欄位，時間窗口則把事件依"
        "故障預測所需的觀察區間聚合。它比單純轉 CSV 更能處理陣列與多層結構，也比把原始"
        "JSON 當字串交給 RNN 更具可控性、可驗證性與工程效率。"
    ),
    "optionAnalysis": {
        "A": (
            "扁平化後轉 CSV 可用於結構固定、巢狀程度低的離線分析，均值與次數也可能是有效"
            "特徵；但直接轉檔容易丟失陣列、父子路徑與事件時間關係，選項也未依時間窗口聚合，"
            "不足以充分萃取故障前的時序訊號。"
        ),
        "B": (
            "RNN 適合處理已轉成有意義向量的事件序列，而不是把含括號、鍵名與轉義字元的原始"
            "JSON 字串直接視為序列。未先解析 schema 會浪費容量學習序列化格式，且難以處理"
            "欄位缺失、型別與巢狀語意。"
        ),
        "C": (
            "正確。遞迴展開可把 nested fields 轉成穩定欄位路徑並保留內容；再按事件時間與"
            "設備鍵建立窗口，計算錯誤頻率、延遲或狀態轉換等特徵，直接對應故障預測需求。"
        ),
        "D": (
            "時間戳記只能表示事件何時發生，無法說明事件類型、嚴重度、元件狀態或錯誤碼。"
            "刪掉其他巢狀內容會失去判斷故障原因與先兆的主要訊號，雖簡化處理卻犧牲預測能力。"
        ),
    },
    "trap": (
        "「扁平化」不是錯，但要保留欄位路徑、陣列語意與時間關係；只把 JSON 轉 CSV 並算全域"
        "平均不等於時序特徵。窗口統計還必須以預測時間為界，避免把故障後事件洩漏進特徵。"
    ),
    "references": [
        exam_ref(27),
        ref(
            "Apache Spark 3.5.8－Structured Streaming Programming Guide",
            SPARK_STREAMING,
            "支援 JSON 串流來源、事件時間聚合，以及 tumbling、sliding、session 三類時間窗口",
        ),
    ],
}

DRAFTS[28] = {
    "summary": "正確答案是 C。連續特徵標準化、類別特徵適當編碼，再建立有意義的交互特徵，是四項中最完整的混合型資料特徵工程流程。",
    "concept": (
        "混合型資料不應把所有欄位強迫成同一種表示。標準化以訓練集平均數與標準差調整連續"
        "特徵尺度，避免某些依距離或正則化的模型被大數值欄位主導；目標編碼用訓練標籤的"
        "條件統計表示高基數類別，但必須以交叉擬合、平滑及只用訓練資料避免目標洩漏。交互"
        "特徵則表達兩欄共同作用，應依業務假設與驗證結果挑選，並非越多越好。"
    ),
    "answerReason": (
        "C 分別依資料型態選擇標準化與目標編碼，並進一步建立可能有預測力的交互特徵，是"
        "選項中唯一完整利用連續與類別資訊的流程。雖然具體最佳做法仍取決於模型，C 相較"
        "任意序數編碼、全面分桶或刪除類別欄位，保留資訊並處理尺度更周全。"
    ),
    "optionAnalysis": {
        "A": (
            "標籤編碼把類別指定為整數，對樹模型有時可配合專門處理，但對一般線性或距離模型"
            "會暗示不存在的順序與間距；又未處理連續特徵尺度。直接合併並非在所有模型下都"
            "合理，尤其名目類別沒有自然次序時風險明顯。"
        ),
        "B": (
            "分桶可表達門檻效應、降低離群值影響，特定任務下有價值；但把所有連續特徵一律"
            "離散化會損失細微數值差異，也不能因此假定所有模型都應以類別方式處理。"
        ),
        "C": (
            "正確。標準化讓連續特徵尺度可比，目標編碼能精簡表示類別與預測目標的關係，"
            "交互特徵可捕捉共同作用；流程需封裝在交叉驗證內，以訓練折估計編碼值避免洩漏。"
        ),
        "D": (
            "只保留連續特徵雖降低維度，卻可能丟掉地區、產品類型或客群等重要訊號。除非驗證"
            "證明類別欄位無效或無法合法使用，不能為了簡化就忽略整類資訊。"
        ),
    },
    "trap": (
        "C 是本題四選一中的最佳流程，不代表目標編碼永遠優於 one-hot，也不代表所有模型都需要"
        "標準化。最常被忽略的風險是 Target Encoding 使用全資料標籤造成洩漏，必須交叉擬合。"
    ),
    "editorialNote": (
        "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。選項 C 的方法具有"
        "模型相依性：樹模型未必需要標準化，低基數名目類別可能較適合 one-hot；官方答案仍為 C。"
    ),
    "references": [
        exam_ref(28),
        ref(
            "scikit-learn API－Preprocessing data",
            SKLEARN_PREPROCESSING,
            "StandardScaler、TargetEncoder 與 PolynomialFeatures（含 interaction features）的官方 API 索引",
        ),
        ref(
            "scikit-learn API－TargetEncoder",
            SKLEARN_TARGET_ENCODER,
            "目標編碼定義、平滑，以及 fit_transform 以 cross fitting 防止過度擬合的說明",
        ),
    ],
}

DRAFTS[29] = {
    "summary": "正確答案是 B。每次提交後自動建置、測試與靜態分析，能及早發現小批次變更造成的錯誤，正是持續整合的核心。",
    "concept": (
        "持續整合（CI）要求開發者頻繁把小幅變更整合到共享版本庫，並由自動化流程快速驗證"
        "每次變更。典型管線包含安裝相依套件、建置、單元測試、程式碼風格與靜態安全分析；"
        "失敗時應立即回報並修復，避免多個錯誤累積成難以定位的大型整合。AI 專案還可加入"
        "資料 schema、模型介面與可重現性測試，但模型完成訓練不是觸發 CI 的必要前提。"
    ),
    "answerReason": (
        "B 同時具備「每次提交觸發」與「自動驗證」兩個關鍵，讓問題在變更仍小、責任範圍"
        "清楚時被發現，直接降低整合風險。其他選項不是依提交持續觸發，就是描述部署活動，"
        "都沒有完整呈現 CI 的頻繁整合與快速回饋。"
    ),
    "optionAnalysis": {
        "A": (
            "每日合併比長期分支好，但由人固定時間操作與測試會延遲回饋，也容易漏執行步驟。"
            "CI 的重點是提交後由一致的自動流程驗證，而非累積到一天一次才手動整合。"
        ),
        "B": (
            "正確。每個 commit 自動觸發建置、單元測試與靜態分析，能快速指出是哪個小變更"
            "破壞品質門檻，讓團隊在合併前或合併後立即修復，減少後續衝突與除錯範圍。"
        ),
        "C": (
            "模型訓練完成後才定期回顧與合併，回饋週期受長時間訓練綁住，程式碼會累積成較大"
            "批次。團隊回顧可作為治理活動，卻不能取代每次程式變更的自動整合驗證。"
        ),
        "D": (
            "把模型自動批次釋出到測試環境屬於持續交付或部署流程的一部分，關注的是發布。"
            "即使部署腳本自動化，若沒有每次提交的建置與測試門檻，仍不構成 CI 核心實踐。"
        ),
    },
    "trap": (
        "CI 的 I 是 Integration，關鍵字是頻繁提交與自動驗證；CD 才進一步處理交付或部署。"
        "固定排程不必然錯，但若等待批次且靠人工執行，就失去提交後快速回饋的優勢。"
    ),
    "references": [
        exam_ref(29),
        ref(
            "GitHub Docs－Continuous integration",
            GITHUB_CI,
            "頻繁提交降低除錯與合併成本；commit 後持續建置與測試，並可加入 lint 與安全檢查",
        ),
    ],
}

DRAFTS[30] = {
    "summary": "正確答案是 A。保存每筆推論輸入與輸出的雜湊並加上數位簽章，可驗證資料完整性與簽署來源，提供第三方稽核所需的不可否認證據。",
    "concept": (
        "不可否認性要求事後能證明某筆資料或行為出自特定簽署者，且內容未被偷偷修改。加密"
        "雜湊把輸入與輸出映射為固定長度摘要；任何內容改變通常會產生不同摘要，但雜湊本身"
        "只證明一致性，不能證明是誰建立。數位簽章用私鑰簽署摘要，驗證方可用公鑰確認來源"
        "與完整性。完整制度仍需可信時間戳、金鑰管理、身分綁定與防竄改稽核儲存。"
    ),
    "answerReason": (
        "A 同時記錄推論證據並用數位簽章綁定簽署身分；日後重算雜湊可發現輸入或輸出被改動，"
        "驗章則能確認簽署來源。NIST 的數位簽章標準明確把完整性、簽署者身分驗證及向第三方"
        "舉證列為用途，正符合題目的法務追蹤與稽核需求。"
    ),
    "optionAnalysis": {
        "A": (
            "正確。每筆推論的輸入、輸出與必要脈絡先產生雜湊，再由受控私鑰簽署，能讓稽核者"
            "驗證內容是否變更以及簽章是否來自聲稱的實體；搭配時間戳與金鑰生命週期管理可"
            "形成較完整的證據鏈。"
        ),
        "B": (
            "降低推論延遲改善的是效能與使用者體驗，只能說明系統回得快。它沒有保存每次決策"
            "內容、驗證來源或偵測紀錄被修改的機制，與不可否認性所需證據無關。"
        ),
        "C": (
            "主機備援提高可用性，讓單機故障時服務仍能持續；但多台主機不會自動產生可驗證的"
            "推論紀錄，也不能證明某筆紀錄由誰產生或之後是否遭竄改。"
        ),
        "D": (
            "負載平衡把請求分散到多個節點，改善容量、延遲與單點壅塞，屬於可用性與效能控制。"
            "它不提供資料完整性或來源認證；若未另做簽署，各節點日誌仍可能被改寫或否認。"
        ),
    },
    "trap": (
        "雜湊與數位簽章不是同一件事：雜湊驗內容，簽章再把摘要綁定到私鑰持有者。"
        "備援與負載平衡處理可用性，低延遲處理效能，都不能替代不可否認性的證據鏈。"
    ),
    "editorialNote": (
        "本站自編的 AI 輔助詳解初稿，並非金融法遵意見或官方詳解；尚待獨立人工複核。"
        "僅有雜湊與簽章仍不足以自動滿足特定主管機關全部規範，實務需另確認可信時間戳、"
        "私鑰保護、憑證撤銷、日誌保存期限、存取控制及個資最小化。"
    ),
    "references": [
        exam_ref(30),
        ref(
            "NIST FIPS 186-5－Digital Signature Standard",
            NIST_DSS,
            "數位簽章用於偵測未授權修改、驗證簽署者身分，並可向第三方證明簽署來源以支援不可否認性",
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
