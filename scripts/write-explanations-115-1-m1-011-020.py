"""Write draft explanations for 115-1 intermediate subject one, Q11-Q20.

The script verifies every official answer, refuses to overwrite reviewed work,
and leaves all generated explanations in ``draft`` for independent review.

Usage::

    python scripts/write-explanations-115-1-m1-011-020.py
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUESTIONS = ROOT / "app" / "data" / "questions.json"
SOURCE_ID = "aiap-115-intermediate-1-ai-tech-planning"
AUTHOR = "Codex（AI 輔助初稿）"
AUTHORED_AT = "2026-08-12"
CHECKED_AT = "2026-08-12"

EXAM_PDF = (
    "https://www.ipas.org.tw/api/proxy/uploads/certification_resource/"
    "bf93f438f7be48d295c1b40a34d79f3d/115年第一次中級AI應用規劃師_"
    "第一科_人工智慧技術應用與規劃_公告試題_20260615003359.pdf"
)
ARXIV = "https://arxiv.org/abs/"
DEFAULT_NOTE = "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。"


def exam_ref(number: int) -> dict:
    return {
        "title": "115 年第一次中級 AI 應用規劃師－人工智慧技術應用與規劃公告試題",
        "url": EXAM_PDF,
        "locator": f"第 {number} 題題幹、選項與官方答案",
        "checkedAt": CHECKED_AT,
    }


def ref(title: str, url: str, locator: str) -> dict:
    return {"title": title, "url": url, "locator": locator, "checkedAt": CHECKED_AT}


def paper(paper_id: str, title: str, locator: str) -> dict:
    return ref(title, f"{ARXIV}{paper_id}", locator)


EXPECTED_ANSWER = {
    11: "B", 12: "B", 13: "C", 14: "A", 15: "B",
    16: "A", 17: "D", 18: "D", 19: "A", 20: "A",
}

DRAFTS: dict[int, dict] = {}

DRAFTS[11] = {
    "summary": "正確答案是 B。Self-Attention 讓每個 token 直接參照序列中的其他 token，並依相關程度分配權重，以整合長距離上下文。",
    "concept": (
        "自注意力（Self-Attention）先由同一序列的表示產生 Query、Key 與 Value；"
        "每個 Query 與所有 Key 計算相似分數，經縮放與 softmax 後成為權重，再"
        "加權彙整各 Value。任兩位置之間因此可在同一層直接交換資訊，不必像"
        "循環網路逐步傳遞隱藏狀態。位置編碼另負責補入順序，不能把注意力本身"
        "誤解為固定局部卷積或把整句壓成單一向量。"
    ),
    "answerReason": (
        "B 完整描述自注意力的核心：序列內各 token 彼此建立關聯，並以內容相關性"
        "決定加權程度。這條直接關聯路徑正是 Transformer 能有效處理遠距依賴的"
        "主要結構原因；其他選項分別描述 RNN、局部卷積或固定長度編碼。"
    ),
    "optionAnalysis": {
        "A": "隱藏狀態逐步遞迴是 RNN、LSTM 或 GRU 的運作方式；它能累積上下文，但遠距資訊需經過多個時間步傳遞，並非 Self-Attention 讓位置直接互相計算權重的機制。",
        "B": "正確。每個 token 的 Query 會與序列內各 token 的 Key 比較，再用得到的注意力權重彙整 Value；遠距位置可直接影響當前表示。",
        "C": "局部運算與鄰近關係是一般 CNN 的典型特性；卷積必須堆疊多層或擴張感受野才能連接遠距位置，而完整 Self-Attention 一層即可考量全序列。",
        "D": "把可變長序列壓成固定向量是早期 encoder-decoder 或池化式表徵的作法；Self-Attention 通常為每個輸入位置產生上下文化表示，不要求全序列只剩一個向量。",
    },
    "trap": "看到『序列建模』不要立即選遞迴；題目問 Transformer 的 Self-Attention，辨識點是全序列位置直接互相評分。位置編碼處理順序，注意力處理內容間的關聯。",
    "references": [
        exam_ref(11),
        paper("1706.03762", "Vaswani et al., Attention Is All You Need（2017）", "第 3.2.1 節：scaled dot-product attention 以 Query-Key 分數加權 Value；第 4 節比較長距依賴路徑"),
    ],
}

DRAFTS[12] = {
    "summary": "正確答案是 B。Sigmoid 將實數壓縮到 0 與 1 之間，適合表示二元事件的機率，但在輸入絕對值很大時導數趨近零，可能造成梯度消失。",
    "concept": (
        "Sigmoid 定義為 σ(x)=1/(1+e^(-x))，輸出落在開區間 (0,1)。二元分類可"
        "把一個 logit 經 Sigmoid 解讀為正類機率，訓練時通常搭配 binary cross-"
        "entropy；實作常直接使用合併 log-sum-exp 的 logits 損失以提升數值穩定。"
        "其導數為 σ(x)(1−σ(x))，當 x 很大或很小，輸出飽和於 1 或 0，導數便接近"
        "零，因此若在深層隱藏層反覆使用，梯度可能逐層衰減。"
    ),
    "answerReason": (
        "B 同時說對 Sigmoid 的輸出範圍、二元機率用途與飽和區梯度消失限制。"
        "A 描述無界線性輸出，C 描述 Softmax 的多類別正規化，D 則與 Sigmoid"
        "在兩端飽和、梯度變小的性質相反。"
    ),
    "optionAnalysis": {
        "A": "任意實數範圍通常由不加限制的線性輸出層提供，適合一般迴歸；Sigmoid 輸出有界於 (0,1)，若用於迴歸也只適合目標本來就在該範圍的情境。",
        "B": "正確。Sigmoid 可把單一 logit 映射成正類機率；但輸入位於兩端時函數飽和、導數接近零，反向傳播的學習訊號會變弱。",
        "C": "Softmax 會同時考量多個 logits 並正規化成總和為 1 的多類別分布；單一 Sigmoid 只將各輸入獨立映射到 (0,1)，不會讓多個輸出自動加總為 1。",
        "D": "Sigmoid 的最大導數僅為 0.25，且輸入絕對值增大時會迅速接近零，並非全域梯度穩定；深層隱藏層通常較常使用 ReLU 類函數來降低飽和問題。",
    },
    "trap": "區分二元分類的單一 Sigmoid 與互斥多分類的 Softmax；另外，輸出可以解釋為機率，不代表在所有位置都有良好梯度，飽和區正是 Sigmoid 的限制。",
    "references": [
        exam_ref(12),
        ref("PyTorch－Sigmoid 官方文件", "https://docs.pytorch.org/docs/stable/generated/torch.nn.Sigmoid.html", "Sigmoid 公式與元素逐一映射定義"),
        ref("PyTorch－BCEWithLogitsLoss 官方文件", "https://docs.pytorch.org/docs/stable/generated/torch.nn.BCEWithLogitsLoss.html", "將 Sigmoid 與 binary cross entropy 合併，利用 log-sum-exp 提升數值穩定性"),
    ],
}

DRAFTS[13] = {
    "summary": "正確答案是 C。傳統微調會更新預訓練模型的全部或大量權重；Prompt Tuning 則凍結主模型，只學習附加於輸入端的少量 soft prompt 向量。",
    "concept": (
        "傳統全參數微調以標註資料對預訓練模型反向傳播，更新模型內部權重以適應"
        "下游任務。Prompt Tuning 屬參數高效率微調：主模型保持凍結，在輸入"
        "embedding 前加入可學習的連續向量，訓練時只更新這組 soft prompt。"
        "兩者都建立在預訓練模型之上，也都可能使用監督資料；本質差異是可訓練"
        "參數放在模型本體或輸入前綴，不是學習率、容量或推論延遲。"
    ),
    "answerReason": (
        "C 正確對照更新範圍：傳統微調改動模型參數，Prompt Tuning 主要調整輸入"
        "表示的可學習提示。這讓同一凍結模型能為不同任務各保存很小的 prompt，"
        "而不需保存完整的任務專用模型副本。"
    ),
    "optionAnalysis": {
        "A": "Prompt Tuning 的主要目標是降低每個任務的可訓練與儲存參數，不保證降低推論延遲；soft prompt 反而增加少量輸入 token。傳統微調調整既有容量，並非用來擴增模型參數量。",
        "B": "兩者都可使用梯度下降，但可訓練參數集合完全不同：全參數微調更新主模型，Prompt Tuning 凍結主模型並更新 soft prompt；差異不只是學習率。",
        "C": "正確。傳統微調通常更新模型內部權重，Prompt Tuning 則把少量連續提示向量接到輸入，藉由訓練這些向量來引導凍結模型完成任務。",
        "D": "兩者都以預訓練模型作為起點；若沒有預訓練主模型，Prompt Tuning 的少量向量也無法憑空提供語言能力，所以是否預訓練不是兩者分界。",
    },
    "trap": "不要把 prompt engineering 的人工文字提示與 Prompt Tuning 混為一談；本題明定 soft prompt，它是透過訓練得到的連續 embedding。判斷重點是主模型是否凍結。",
    "references": [
        exam_ref(13),
        paper("2104.08691", "Lester, Al-Rfou & Constant, The Power of Scale for Parameter-Efficient Prompt Tuning（2021）", "摘要與第 2 節：凍結預訓練模型，僅訓練輸入前的 soft prompt 參數"),
    ],
}

DRAFTS[14] = {
    "summary": "正確答案是 A。凍結大部分預訓練權重、只訓練 LoRA 等少量新增參數，可限制對原模型的改動，兼顧資源效率並降低新任務更新干擾既有能力的風險。",
    "concept": (
        "災難性遺忘是模型學習新資料時，參數更新覆蓋原有任務所需表示，導致舊能力"
        "明顯退化。參數高效率微調（PEFT）會凍結基礎模型，只更新 adapter、LoRA"
        "等少量參數；LoRA 將低秩更新注入既有權重旁路，減少可訓練參數與記憶體，"
        "也避免直接全面改寫預訓練權重。不過凍結不等於保證所有舊能力完全不變，"
        "仍應以通用與醫療評測集檢查遺忘。"
    ),
    "answerReason": (
        "題目同時要求資源有限、學會醫療問答並保留原能力。A 只訓練少量 LoRA"
        "模組，直接縮小更新範圍且節省訓練資源，是四個方案中最貼合限制者。"
        "提高學習率、只重複新資料或單純增大 batch 都沒有保護原知識的機制。"
    ),
    "optionAnalysis": {
        "A": "正確。凍結基礎模型避免其權重被全面覆寫，只讓低秩適配器學習新任務差異；可訓練參數與最佳化器狀態較少，也較符合資源有限條件。",
        "B": "提高學習率會使每一步權重改動更大，可能更快偏離預訓練解；縮短步數未必抵銷此風險，也沒有以舊資料或參數約束保護既有能力。",
        "C": "只用醫療資料多輪訓練會持續強化新分布，卻不提供舊任務訊號，通常更容易讓模型偏向醫療領域而遺忘通用能力。",
        "D": "較大 batch 可降低梯度估計雜訊，但不會改變目標函數只來自醫療資料，也不限制哪些權重可被更新，因此不能確保保留舊知識。",
    },
    "trap": "訓練穩定不等於抗遺忘：大 batch 和快速收斂只影響最佳化過程；真正對應本題的是限制基礎權重更新範圍。若資源允許，資料重放、正則化與持續學習也可另行評估。",
    "editorialNote": "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。LoRA 可降低直接改動基礎權重的程度，但不保證部署後所有通用行為完全不變，仍需以獨立基準測試驗證。",
    "references": [
        exam_ref(14),
        paper("2106.09685", "Hu et al., LoRA: Low-Rank Adaptation of Large Language Models（2021）", "摘要與方法：凍結預訓練權重，將可訓練的低秩矩陣注入 Transformer 層，以大幅降低可訓練參數"),
        paper("1612.00796", "Kirkpatrick et al., Overcoming catastrophic forgetting in neural networks（2016）", "摘要：序列學習新任務會遺忘舊任務，並以限制重要參數變動的方式緩解"),
    ],
}

DRAFTS[15] = {
    "summary": "正確答案是 B。Orchestrator 應驗證 Worker 結果，對可恢復失敗採有界重試或轉派其他 Worker，並保存錯誤脈絡，才能讓局部失敗不直接破壞整體任務。",
    "concept": (
        "多代理系統的可靠性不能假設每個 Worker 都會成功。協調者需要明確驗收"
        "條件、錯誤分類、逾時、有限次重試、替代執行者與失敗紀錄；重試還要考量"
        "工具操作是否具冪等性，避免重複付款或重複寫入等副作用。重新分配可處理"
        "單一模型、工具或執行環境的局部故障，紀錄則支援除錯與後續改善。"
    ),
    "answerReason": (
        "B 包含結果評估、重試、轉派及失敗紀錄，形成完整的偵測與恢復閉環。"
        "它在不接受低品質輸出的前提下，讓其他 Worker 或下一次執行仍有機會完成"
        "任務；其餘選項不是忽略錯誤，就是把局部失敗放大成全域中止。"
    ),
    "optionAnalysis": {
        "A": "直接採用未達標結果會把已知錯誤帶入後續彙整，雖減少延遲卻犧牲正確性；只有在降級結果已符合預先定義的最低服務標準時，才可能作為 fallback。",
        "B": "正確。Orchestrator 先依驗收規則辨識失敗，再以有界 retry 或不同 Worker 恢復，並保存原因供追蹤；這能隔離單點失敗並持續推進整體工作。",
        "C": "統一模型可能降低部分輸出格式差異，但也會形成共同失敗模式；模型相同不代表搜尋、程式或彙整結果正確，更沒有提供失敗後的恢復流程。",
        "D": "立即終止可避免錯誤擴散，但任何暫時性逾時或單一 Worker 問題都會讓整體任務失敗；應先嘗試安全重試、替代路徑或局部降級，再決定是否升級人工處理。",
    },
    "trap": "重試不是無限重做：應設定次數、退避、逾時與冪等性。題目要的是容錯閉環，而不是追求輸出一致；相同模型的多個 Worker 仍可能一起犯同類錯誤。",
    "references": [
        exam_ref(15),
        ref("Google Cloud Workflows－Best practices", "https://cloud.google.com/workflows/docs/best-practice", "Apply retries and the saga pattern：以錯誤處理、有限重試與補償流程提升工作流韌性"),
        ref("Google Cloud－Retry strategy", "https://cloud.google.com/storage/docs/retry-strategy", "重試前需判斷請求冪等性，避免競態、重複副作用與不一致"),
    ],
}

DRAFTS[16] = {
    "summary": "正確答案是 A。題目要求的是『目前』市場資料，Agent 卻未使用搜尋工具查證便憑既有知識作答；System Prompt 應強制即時性問題先搜尋、開啟來源並附可追溯證據。",
    "concept": (
        "ReAct 交錯進行推理與行動：模型依問題決定工具，取得 observation 後更新"
        "判斷，再決定下一步或回答。『目前最大營運商及充電樁總數』會隨時間變動，"
        "且還涉及最大值口徑（站點、槍數或樁數），不能只靠模型訓練時記憶。"
        "設計上應要求先取得當日日期、搜尋候選資料、開啟原始頁面，核對統計日期"
        "與口徑後再回答；工具不是越多越好，也不必每題全部呼叫。"
    ),
    "answerReason": (
        "A 精確指出失敗根因是提示未建立『即時問題必查證』門檻，導致 Agent"
        "在 Action 為無的情況下杜撰公司與數量。加入依問題選擇 web_search、"
        "get_webpage 與日期查核的規則，才能讓答案建立於可更新的外部證據。"
    ),
    "optionAnalysis": {
        "A": "正確。System Prompt 應要求遇到『目前、最新、總數』等時效性問題先查詢，並開啟可靠來源核對日期與統計口徑；這能阻止直接以過時記憶產生答案。",
        "B": "calculator 與 get_current_date 是否使用取決於問題；未用到的工具不會自動造成錯答。此題取得日期有助界定『目前』，真正問題是未建立工具使用與證據驗收規則。",
        "C": "ReAct 的推理軌跡用來規劃行動、解讀觀察與處理例外；完全移除推理不會修復未查證問題，且可能使工具選擇更武斷。實作可不向使用者顯示內部推理，但仍需保留決策流程。",
        "D": "第一輪呼叫所有工具會浪費成本，calculator 對此題也沒有必要；正確做法是依序選擇需要的工具，並根據每次 observation 決定是否補查，而非盲目全呼叫。",
    },
    "trap": "『有工具』不等於『會用工具』。需在提示與驗收規則中辨識時效性、來源品質及口徑；同時別把 ReAct 誤解成每輪都要呼叫全部工具，核心是依觀察迭代選擇下一個行動。",
    "references": [
        exam_ref(16),
        paper("2210.03629", "Yao et al., ReAct: Synergizing Reasoning and Acting in Language Models（2022）", "摘要與方法：交錯產生 reasoning traces 與 task-specific actions，透過外部知識來源取得資訊並更新計畫"),
    ],
}

DRAFTS[17] = {
    "summary": "正確答案是 D。CNN 擅長影像的局部空間特徵，Transformer 適合文字上下文，LSTM 或 Temporal CNN 則能建模心率、血氧隨時間的變化。",
    "concept": (
        "不同模態的歸納偏置不同：影像具有二維局部與平移結構，CNN 以共享卷積核"
        "擷取邊緣、紋理到高階影像特徵；臨床文字是 token 序列，Transformer"
        "以注意力建立上下文關聯；心率與血氧是依時間排序的連續量，可用 LSTM"
        "保留時間狀態，或用 Temporal CNN 的因果／擴張卷積擷取多尺度時序模式。"
        "現代架構也可用 vision transformer 或時序 Transformer，但需有適當輸入"
        "編碼，不能因名稱含 Transformer 就直接把純文字 BERT 套到所有資料。"
    ),
    "answerReason": (
        "D 逐一對應三種資料結構與合適架構，且所有模型都能產生後續融合所需的"
        "特徵。A、B 將模型與資料型態錯配；C 忽略 BERT 預期的是 token 與位置"
        "表示，原始影像和連續感測值不能未經專用編碼直接輸入。"
    ),
    "optionAnalysis": {
        "A": "LSTM 主要處理有順序的序列，不具 CNN 對二維局部空間的原生歸納偏置；CNN 可做文字局部模式，但 BERT 也不是直接接收原始心率數值的時序模型，三者皆未最佳對應。",
        "B": "TF-IDF 是文字詞頻特徵，不能擷取 X 光影像；ResNet 是影像 CNN，不是臨床文本的自然選擇；Word2Vec 產生詞向量，也無法直接建模血氧數值的時間依賴。",
        "C": "BERT 是以文字 token 預訓練的 Transformer encoder；Transformer 架構可改造到其他模態，但影像需 patch embedding、時序需數值與時間編碼，不能把同一 BERT 未經改造套用任意原始資料。",
        "D": "正確。CNN 對 X 光的局部空間結構有效，文字 Transformer 建模診斷筆記的遠近語境，LSTM 或 Temporal CNN 則保留感測值的時間順序與跨時間模式。",
    },
    "trap": "判斷的是『資料表示＋模型歸納偏置』，不是只看模型熱門程度。Transformer 可跨模態使用，但必須搭配各模態的 tokenizer、patch 或數值時序編碼；BERT 這個具體模型不是萬用原始資料介面。",
    "references": [
        exam_ref(17),
        paper("1512.03385", "He et al., Deep Residual Learning for Image Recognition（2015）", "摘要與方法：以深層殘差卷積網路處理影像辨識"),
        paper("1810.04805", "Devlin et al., BERT（2018）", "摘要與第 3 節：以雙向 Transformer encoder 建模文字 token 上下文"),
        paper("1803.01271", "Bai, Kolter & Koltun, An Empirical Evaluation of Generic Convolutional and Recurrent Networks for Sequence Modeling（2018）", "第 3 節：以因果、擴張一維卷積構成 Temporal Convolutional Network 處理序列"),
    ],
}

DRAFTS[18] = {
    "summary": "正確答案是 D。Cross-Modal Alignment 將 CT、病歷文字與基因序列的表示映射到可比較的共同語意空間，使相同患者或相同病理概念能跨模態建立關聯。",
    "concept": (
        "不同模態的原始維度與統計形式不同，不能直接比較像素、文字 token 與基因"
        "序列。跨模態對齊以配對樣本、對比學習或投影層，使語意相符的模態表示"
        "在共同空間靠近，不相符者分離；模型因此能融合互補證據、進行跨模態"
        "檢索或共同預測。對齊通常仰賴既有配對或監督訊號，本身不等於自動產生"
        "標註，也不以降低儲存成本為主要目標。"
    ),
    "answerReason": (
        "D 說明對齊的兩個必要結果：建立共同表示空間，以及讓模態間的語意可"
        "關聯。癌症預測才可把同一患者的影像病灶、病歷描述與基因特徵互相對照；"
        "其餘選項不是捨棄多模態，就是把資料標註或系統效率誤當對齊目的。"
    ),
    "optionAnalysis": {
        "A": "只保留 CT 會變成單模態模型，病歷與基因的互補資訊被丟棄；對齊的目的正是讓異質模態能共同使用，而不是先排除其他模態。",
        "B": "對比式對齊通常需要已知哪些影像、文本或序列屬於同一患者或事件；它可利用既有配對學表示，但不會自動創造可信的臨床配對標註。",
        "C": "共同表示可能影響模型大小與計算，但對齊通常還會增加多個 encoder 與投影層；其首要問題是語意可比較與融合，不是儲存壓縮。",
        "D": "正確。各模態先由專用 encoder 轉成向量，再投影到共同空間；相同臨床概念的表示可靠近，模型便能建立影像、文字與基因之間的語意關聯。",
    },
    "trap": "融合是『把資訊合起來』，對齊則先讓不同模態的表示在語意上可比較。對比學習可作為對齊方法，但需要正負配對規則，不能把它誤稱為自動標註系統。",
    "references": [
        exam_ref(18),
        paper("2103.00020", "Radford et al., Learning Transferable Visual Models From Natural Language Supervision（2021）", "摘要與方法：以配對影像文字的對比目標學習共同 embedding，對齊影像與文字表示"),
    ],
}

DRAFTS[19] = {
    "summary": "正確答案是 A。AUC 0.91 只說明離線資料上的排序區辨能力，不能單獨證明上線商業成效；圖中 CTR 反而由 3.2% 降至 3.1%，且營收、延遲與成本都須共同評估。",
    "concept": (
        "ROC AUC 衡量分類器跨各閾值將正例排在負例之前的能力，屬離線模型指標；"
        "它不直接等同點擊率、轉換、營收或使用者體驗。上線評估需要預先定義"
        "主要業務指標與 guardrail，最好用隨機 A/B test 與舊系統同期比較，並"
        "檢查統計顯著性、流量組成及觀察期間。圖中只有導入後 AUC，CTR 由 3.2%"
        "降至 3.1%，平均訂單金額由 850 美元升至 1,020 美元，另有平均延遲 85ms"
        "與每月推論費 12,000 美元；這些方向不一致，不能只挑一項宣告成功。"
    ),
    "answerReason": (
        "A 指出評估層級錯置：離線 AUC 高不代表線上業務成果好。圖表甚至顯示"
        "CTR 小幅下降，且訂單金額提升是否由模型造成、是否抵銷成本，都需對照"
        "實驗與營收口徑驗證，故原結論證據不足。"
    ),
    "optionAnalysis": {
        "A": "正確。AUC 只反映離線標籤上的排序表現；需同時檢視 CTR、轉換、營收、延遲、成本等線上指標，並以對照實驗確認變化是否由新模型造成。",
        "B": "AUC 0.91 可表示該離線資料上的區辨能力良好，但推薦清單、介面與流量分布都可能使離線分數無法轉成實際點擊；不能在 CTR 下降時仍僅憑 AUC 判定品質提升。",
        "C": "CTR 下降值得調查，但 0.1 個百分點是否具統計與業務意義尚未知，且平均訂單金額同時上升；在沒有 A/B test、顯著性與事故證據前立即 rollback 過於武斷。",
        "D": "平均訂單金額提高不等於總營收已提高，因訂單量可能受 CTR 或轉換率影響；還要扣除每月 12,000 美元推論費並排除促銷、季節等混淆因素。",
    },
    "trap": "不要把『模型指標好』直接翻譯成『專案成功』，也不要只因單一線上指標下滑就立即回滾。先確認指標定義、基準、統計顯著性、因果對照與成本收益。",
    "editorialNote": "本站依官方答案 A 判定。附圖只有導入前後摘要，未提供同期對照組、樣本量、CTR／訂單金額的信賴區間或總營收，因此不能從圖中判定模型一定成功或失敗；需補做因果與統計驗證。",
    "references": [
        exam_ref(19),
        ref("scikit-learn User Guide－ROC metrics", "https://scikit-learn.org/stable/modules/model_evaluation.html#roc-metrics", "ROC curve 與 ROC AUC 衡量二元分類在不同決策閾值下的 true-positive／false-positive trade-off"),
        paper("1606.07659", "Kohavi et al., Online Controlled Experiments: Lessons from Running A/B/n Tests for 12 Years（2016）", "摘要與實務經驗：以線上隨機對照實驗評估產品變更對關鍵指標的因果影響"),
    ],
}

DRAFTS[20] = {
    "summary": "正確答案是 A。以批次模型產生基礎推薦、REST API 即時服務、Kafka 更新近期行為，並從 Redis 或線上 Feature Store 讀取低延遲特徵；不應讓每次即時特徵都先繞行資料倉儲。",
    "concept": (
        "100ms 服務目標需要把離線與線上路徑分離。歷史資料可在批次流程訓練"
        "協同過濾模型；線上服務以 API 接收請求，從串流管線取得最新點擊，並"
        "由 Redis 或 Feature Store 的 online store 低延遲讀取特徵。資料倉儲仍"
        "適合保存完整歷史、離線分析與再訓練，但若每次事件都先落倉再計算線上"
        "特徵，倉儲批次延遲會阻礙即時性。完整 online learning 會增加標籤延遲、"
        "漂移、回滾與維運複雜度，對三人團隊並非必要起點。"
    ),
    "answerReason": (
        "A 保留可管理的批次訓練與即時推論，使用 Kafka 處理新行為，並加入"
        "Redis／Feature Store 供低延遲讀取；移除的是『線上特徵必須先經資料倉儲』"
        "這條慢路徑，而非完全不要保存倉儲資料，最符合 100ms、3,000 QPS 與"
        "有限人力。"
    ),
    "optionAnalysis": {
        "A": "正確。批次模型降低訓練維運複雜度，API 支援即時請求，Kafka 傳遞最新事件，Redis 或 online Feature Store 提供低延遲特徵；資料倉儲可留在非同步離線路徑。",
        "B": "移除串流後，最新點擊只能等待資料進倉與批次計算，難以做到依最新行為調整；資料一致性重要，但可用事件時間、版本與離線／線上特徵定義來治理，不必犧牲即時性。",
        "C": "即時線上學習不是取得即時特徵的必要條件，而且在回饋標籤延遲、錯誤事件、模型漂移與回滾上更複雜；同時保留資料倉儲同步路徑仍可能無法達到 100ms。",
        "D": "若 (4) 位於每次線上特徵計算的必經路徑，即使另有快取，最新事件仍受進倉與轉換延遲；全部保留也增加重複元件與三人團隊的維運負擔，不能自然兼顧即時性。",
    },
    "trap": "『移除 (4)』是移出線上關鍵路徑，不代表企業不保存資料倉儲。也要區分即時特徵與即時訓練：先用串流更新特徵、批次更新模型，通常已能兼顧新鮮度與可控維運。",
    "editorialNote": "本站依官方答案 A 判定。架構上的『移除 (4)』應解讀為不讓所有即時資料先經資料倉儲才計算線上特徵；資料仍可非同步寫入倉儲作稽核、分析與批次再訓練。具體能否達成 100ms 仍須以端到端壓測確認。",
    "references": [
        exam_ref(20),
        ref("Apache Kafka Documentation－Introduction", "https://kafka.apache.org/documentation/#introduction", "Kafka event streaming：即時擷取、持久保存與處理事件串流"),
        ref("Feast Documentation－Online store", "https://docs.feast.dev/v0.57-branch/getting-started/components/online-store", "Online store 保存最新特徵值，供線上預測低延遲讀取"),
        ref("Redis Documentation－Client-side caching", "https://redis.io/docs/latest/develop/clients/client-side-caching/", "快取可讓應用程式低延遲存取頻繁使用資料，並需處理失效與一致性"),
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
