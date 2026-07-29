"""Import the two official 114 fourth-session elementary AIAP PDFs.

This script intentionally creates explanation drafts. Official questions and
answers can be mechanically verified against the rendered PDFs, but the
editorial explanations still require a separate human review cycle.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "app" / "data" / "questions.json"
CHECKED_AT = "2026-07-29"
OFFICIAL_RESOURCE_URL = (
    "https://ipd.nat.gov.tw/ipas/certification/AIAP/learning-resources"
)

SOURCES = [
    {
        "path": ROOT / "tmp" / "pdfs" / "past-04.pdf",
        "sourceId": "aiap-114-elementary-4-ai-foundation",
        "subjectCode": "ai-foundation",
        "subjectLabel": "人工智慧基礎概論",
        "url": "https://www.ipas.org.tw/api/proxy/uploads/certification_resource/bf93f438f7be48d295c1b40a34d79f3d/114年第四梯次初級AI應用規劃師第一科人工智慧基礎概論(當次試題公告114_20251226000442.pdf",
    },
    {
        "path": ROOT / "tmp" / "pdfs" / "past-05.pdf",
        "sourceId": "aiap-114-elementary-4-genai-planning",
        "subjectCode": "genai-planning",
        "subjectLabel": "生成式 AI 應用與規劃",
        "url": "https://www.ipas.org.tw/api/proxy/uploads/certification_resource/bf93f438f7be48d295c1b40a34d79f3d/114年第四梯次初級AI應用規劃師第二科生成式AI應用與規劃(當次試題公告114_20251226000507.pdf",
    },
]

ANSWER_TRANSLATION = str.maketrans(
    {
        "\uff21": "A",
        "\uff22": "B",
        "\uff23": "C",
        "\uff24": "D",
    }
)

# Ordered from specific to broad. These descriptions are editorial scaffolding,
# not official explanations.
CONCEPTS = [
    (
        ("human-over-the-loop", "human-in-the-loop", "人在迴圈"),
        "人類監督與介入",
        "人在迴圈內、迴圈上與迴圈外的差別，在於人類介入決策的時點與程度。",
        "不要只看到「人類監督」就作答，要辨認人類是逐筆核准、日常監督，還是只在異常時接手。",
    ),
    (
        ("feature cross", "特徵交叉"),
        "特徵交叉",
        "特徵交叉把兩個或多個欄位的組合關係建立成新特徵，讓模型學到單一欄位看不出的交互作用。",
        "編碼與縮放處理的是單一欄位表示；特徵交叉處理的是欄位之間的組合關係。",
    ),
    (
        ("etl", "extract-transform-load"),
        "ETL 資料流程",
        "ETL 依序代表擷取、轉換與載入；清理、排序與格式轉換通常屬於 Transform。",
        "題目常把 Extract、Transform、Load 的工作內容互換，應先依三個字母的順序判斷。",
    ),
    (
        ("lasso", "regularization", "正則化", "偏差與變異"),
        "模型正則化與泛化",
        "正則化用懲罰項限制模型複雜度；L1 容易產生稀疏權重，L2 則傾向讓權重平滑縮小。",
        "Lasso 對應 L1、Ridge 對應 L2；「趨近零」與「直接變成零」也要分清楚。",
    ),
    (
        ("監督式學習", "非監督式學習", "強化學習"),
        "機器學習類型",
        "監督式學習使用標籤，非監督式學習探索未標註資料結構，強化學習則依環境回饋學習行動策略。",
        "判斷時先找標籤、獎勵與互動環境三個線索，不要只看應用名稱。",
    ),
    (
        ("decision tree", "random forest", "support vector", "k-means", "分群"),
        "機器學習模型選擇",
        "模型選擇要配合分類、迴歸、分群等任務，以及資料型態、可解釋性與運算限制。",
        "同一演算法可能有分類或迴歸版本；題目的預測目標才是選模型的第一判斷點。",
    ),
    (
        ("cross-entropy", "loss", "損失函數"),
        "損失函數",
        "損失函數衡量模型預測與真實目標的差距；分類與迴歸通常使用不同形式的損失。",
        "損失函數是訓練目標，不等同於最終呈現給使用者的評估指標。",
    ),
    (
        ("precision", "recall", "f1", "auc", "roc", "混淆矩陣"),
        "分類模型評估",
        "Precision、Recall、F1 與 ROC-AUC 分別觀察不同錯誤成本與分類表現，需依任務風險選擇。",
        "先判斷題目在意誤報還是漏報，再選 Precision 或 Recall；不要只看 Accuracy。",
    ),
    (
        ("data drift", "concept drift", "資料漂移", "概念漂移"),
        "模型漂移監控",
        "資料漂移是輸入分布改變；概念漂移是輸入與目標之間的關係改變。",
        "輸入特徵變化與判斷規則變化是兩件事，題目通常會用情境提示其中一種。",
    ),
    (
        ("explainable ai", "lime", "shap", "counterfactual", "可解釋"),
        "可解釋人工智慧",
        "可解釋方法用來說明模型輸出的依據；LIME、SHAP 與反事實解釋的觀察角度不同。",
        "解釋模型不等於取代原模型，也不保證模型本身公平或正確。",
    ),
    (
        ("data bias", "algorithmic bias", "偏誤", "公平"),
        "AI 公平性與偏誤",
        "偏誤可能來自資料蒐集、標註、抽樣、模型設計或部署情境，需透過檢測與治理持續管理。",
        "公平性問題不只靠增加資料量解決，資料代表性與評估分群同樣重要。",
    ),
    (
        ("federated learning", "聯邦學習"),
        "聯邦學習與隱私",
        "聯邦學習讓各節點在本地訓練，再交換模型更新，降低集中搬移原始敏感資料的需求。",
        "聯邦學習不代表零風險，仍要搭配安全聚合、權限與隱私保護措施。",
    ),
    (
        ("homomorphic", "多方計算", "零知識", "加密"),
        "隱私強化技術",
        "同態加密、安全多方計算與零知識證明解決的信任與計算問題不同，應依資料是否移動及誰參與計算判斷。",
        "加密技術不是彼此可任意替換；先確認題目要求的是共同計算、驗證，還是加密狀態運算。",
    ),
    (
        ("low code", "no code"),
        "No Code／Low Code",
        "No Code／Low Code 以視覺模型、元件與自動化降低開發門檻，但整合、測試、治理與客製化仍需工程管理。",
        "低程式碼不代表完全沒有程式碼，也不代表可忽略測試、資安與生命週期管理。",
    ),
    (
        ("prompt", "提示工程", "ape", "chain-of-thought", "few-shot", "zero-shot"),
        "提示工程",
        "提示工程透過任務、限制、範例與輸出格式等上下文，引導模型產生較符合需求的結果。",
        "提示方法改善的是輸入引導，不等同於重新訓練模型，也不能保證消除幻覺。",
    ),
    (
        ("rag", "retrieval", "檢索增強", "向量", "embedding"),
        "檢索增強生成",
        "RAG 先檢索外部知識，再把相關內容提供給生成模型，可改善可追溯性與知識更新效率。",
        "Embedding、向量資料庫、檢索與生成是不同環節；題目會針對其中一段提問。",
    ),
    (
        ("agent", "代理", "solution graph"),
        "AI 代理與任務規劃",
        "AI 代理會結合目標、規劃、工具使用、記憶與回饋，逐步完成多階段任務。",
        "代理不是單次文字生成；需注意它如何拆解任務、選工具與依結果調整。",
    ),
    (
        ("fine-tun", "微調", "lora", "peft"),
        "模型微調",
        "微調以領域資料調整模型參數；參數高效微調只更新少量參數，以降低訓練資源需求。",
        "提示工程、RAG 與微調處理問題的層次不同，不要因為都能改善回答就混為一談。",
    ),
    (
        ("token", "context window", "上下文"),
        "Token 與上下文管理",
        "模型以 Token 處理輸入輸出；上下文長度會影響可納入資訊量、成本與推論表現。",
        "上下文較長不保證每段資訊都能被同等利用，仍需切分、檢索與重點安排。",
    ),
    (
        ("temperature", "top-p", "top-k"),
        "生成取樣參數",
        "Temperature、Top-p 與 Top-k 會改變候選 Token 的取樣範圍與隨機程度。",
        "降低隨機性通常提高一致性，但不代表內容自然變得正確或可驗證。",
    ),
    (
        ("transformer", "attention", "注意力"),
        "Transformer 與注意力機制",
        "注意力機制讓模型依上下文調整不同位置資訊的權重，是 Transformer 處理序列關係的核心。",
        "注意力改善長距依賴，但不等於模型具有真正理解或永不遺忘。",
    ),
    (
        ("gan", "vae", "diffusion", "擴散模型", "生成對抗"),
        "生成式模型",
        "GAN、VAE、自迴歸模型與擴散模型採用不同方式學習資料分布並生成新內容。",
        "生成模型與分類模型的目標不同；也要區分模型架構與實際產品功能。",
    ),
    (
        ("multimodal", "多模態"),
        "多模態 AI",
        "多模態模型整合文字、影像、聲音等不同資料表示，需處理對齊、融合與缺失模態。",
        "能接收多種格式不代表所有模態都被有效融合，資料對齊仍是關鍵。",
    ),
    (
        ("hallucination", "幻覺"),
        "生成式 AI 幻覺",
        "幻覺是模型產生流暢但缺乏事實依據的內容，需用檢索、引用、限制與人工覆核降低風險。",
        "語句流暢與事實正確是兩個維度；不能只靠調整文風判斷可信度。",
    ),
    (
        ("copyright", "著作權", "個人資料", "隱私", "gdpr"),
        "法遵與資料治理",
        "AI 導入需區分個資、著作權、授權、跨境傳輸與用途限制，並保留可稽核的治理流程。",
        "技術上可處理資料，不代表法律上可任意蒐集、利用或再公開。",
    ),
    (
        ("zero trust", "零信任", "權限", "存取控制", "資安"),
        "AI 系統資安",
        "AI 系統安全涵蓋身分、權限、資料、模型、供應鏈、API 與監控，需採分層控制。",
        "單一加密或驗證措施不能取代完整的權限、稽核與事件應變。",
    ),
    (
        ("api", "client", "server", "host", "remote"),
        "系統整合與 API",
        "系統整合需釐清用戶端、伺服端、通訊協定、介面契約與錯誤處理責任。",
        "能連線不等於整合完成；還要驗證資料格式、權限、重試與可測試性。",
    ),
    (
        ("test", "測試", "poc", "概念驗證"),
        "AI 專案測試與驗證",
        "AI 系統需分別驗證模型品質、系統整合、效能、風險與實際業務價值。",
        "開發環境表現不等於上線品質；測試範圍要對應題目所處的生命週期。",
    ),
    (
        ("data", "資料", "特徵", "標註"),
        "資料品質與前處理",
        "AI 模型品質取決於資料的正確性、完整性、代表性、格式與標註一致性。",
        "增加資料量不一定改善模型；若資料本身有偏誤或品質問題，可能放大錯誤。",
    ),
]


def clean_page(text: str) -> str:
    lines = []
    for line in text.splitlines():
        compact = line.replace(" ", "")
        if line.startswith("114 年第四次AI 應用規劃師-初級能力鑑定"):
            continue
        if line.startswith("第一科：") or line.startswith("第二科："):
            continue
        if line.startswith("考試日期："):
            continue
        if line.startswith("第 ") and "頁，共 13 頁" in line:
            continue
        if compact == "答案題目":
            continue
        if "以下空白" in compact:
            continue
        lines.append(line.rstrip())
    return "\n".join(lines)


def normalize_text(text: str) -> str:
    text = re.sub(r"([A-Za-z])-\s*\n\s*([A-Za-z])", r"\1-\2", text)
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"(?<=[\u3400-\u9fff])\s+(?=[\u3400-\u9fff])", "", text)
    text = re.sub(r"\s+([；，。！？：])", r"\1", text)
    return text.strip(" \n;；")


def concept_for(text: str) -> tuple[str, str, str]:
    lowered = text.lower()
    for keywords, title, overview, trap in CONCEPTS:
        if any(keyword in lowered for keyword in keywords):
            return title, overview, trap
    return (
        "AI 應用情境判斷",
        "本題要求依題幹限制，比較各選項的技術目的、適用條件與導入風險。",
        "遇到情境題時，先圈出目標、資料條件與限制，再排除只符合部分條件的選項。",
    )


EXPLANATION_OVERRIDES = {
    "aiap-elementary-114-04-ai-foundation-002": {
        "summary": "正確答案是 C。題目要把「星期幾」與「幾點」的組合關係直接做成模型可學習的特徵。",
        "concept": "特徵交叉會把兩個或多個欄位的組合建立成新特徵，例如「星期一_08時」與「星期日_08時」。模型因此能分別學到平日早上尖峰與假日早上的通勤差異。",
        "answerReason": "單看星期幾或時間，無法直接表示兩者交互作用；特徵交叉正是用來建立「星期幾 × 時間」的組合特徵，所以選 C。",
        "optionAnalysis": {
            "A": "One-hot 編碼是把單一類別欄位轉成 0／1 指示欄，例如把星期一到星期日拆成七欄。它能表示「星期幾」，但若只分別編碼星期與時間，並不會自動產生「星期一早上八點」這種組合關係。",
            "B": "正規化是把數值縮放到相近尺度，例如把溫度與收入轉成可比較的範圍，避免數值尺度差異影響訓練。它不負責建立兩個欄位之間的交互作用。",
            "C": "特徵交叉會建立「星期幾 × 時間」的新特徵，讓模型直接區分平日尖峰、平日離峰與假日時段，因此最符合本題。",
            "D": "寬深模型是一種結合 wide 線性部分與 deep 神經網路部分的模型架構：wide 部分擅長記住既有特徵組合，deep 部分用來泛化到未見組合。若題目問推薦系統或同時兼顧記憶與泛化的模型架構，才較適合選它；本題只問要用哪種特徵工程技巧把兩欄結合。",
        },
        "trap": "One-hot 是表示單一類別，正規化是調整數值尺度，特徵交叉才是明確建立欄位組合；寬深模型則是模型架構，不是這題要找的特徵工程操作。",
    },
    "aiap-elementary-114-04-ai-foundation-003": {
        "summary": "正確答案是 D。ETL 的三個字母依序是 Extract、Transform、Load。",
        "concept": "Extract 從來源擷取資料；Transform 清理、排序、轉換格式或整併資料；Load 再把處理後資料寫入資料倉儲等目標系統。",
        "answerReason": "資料清理與排序都是在載入目標系統前改變資料內容或格式，屬於 Transform，因此選 D。",
        "optionAnalysis": {
            "A": "E 是 Extract，工作是從資料庫、檔案或 API 等來源讀取資料；把資料寫入目標儲存庫是 Load，不是 Extract。",
            "B": "ETL 的名稱同時表示典型處理順序：先擷取、再轉換、最後載入。若先載入再轉換，通常稱為 ELT；不能把 ETL 任意改排成 TEL 還視為相同流程。",
            "C": "L 是 Load，意思是把已轉換的資料載入目標資料庫或資料倉儲，與「將目標儲存庫反加密」無關。",
            "D": "T 是 Transform，包含資料清理、排序、格式統一、欄位轉換與彙整，所以此敘述正確。",
        },
        "trap": "不要只背三個英文字母；要把每階段的資料流向連起來：來源讀出、途中整理、寫入目標。",
    },
    "aiap-elementary-114-04-ai-foundation-004": {
        "summary": "正確答案是 C。L1 與 L2 都是在損失函數加入權重懲罰，以限制模型複雜度。",
        "concept": "L1 使用權重絕對值總和，容易讓部分係數變成 0，形成稀疏模型；L2 使用權重平方和，通常讓係數平滑縮小但不會大量精確歸零。",
        "answerReason": "L1 的懲罰項是權重絕對值總和，會壓縮不重要的權重並控制模型複雜度，因此選 C。",
        "optionAnalysis": {
            "A": "權重數量多不代表正確率一定提高；可調參數過多反而可能記住訓練資料雜訊而過度擬合。L1 的目的之一正是讓不重要的權重歸零，降低有效特徵數。",
            "B": "Lasso 對應 L1 正則化；L2 正則化通常稱為 Ridge。這個選項把兩者名稱對調了。",
            "C": "L1 在損失函數加入權重絕對值的懲罰，促使部分權重縮小甚至變成 0，以限制模型複雜度並達到特徵選擇效果。",
            "D": "L2 會把權重平滑地往 0 壓縮，但通常不會讓大量權重精確等於 0；較容易產生稀疏、零權重解的是 L1，因此此敘述方向相反。",
        },
        "trap": "記法：L1／Lasso 容易留下少數非零權重；L2／Ridge 傾向讓所有權重一起縮小。",
    },
}


def build_explanation(
    question_id: str,
    prompt: str,
    options: list[dict[str, str]],
    answer: str,
    source_title: str,
    source_url: str,
) -> dict:
    explanation = {
        "summary": "",
        "concept": "",
        "answerReason": "",
        # 未完成實質撰寫的選項解析保持空白，前端不顯示；禁止用模板廢話充數。
        "optionAnalysis": {},
        "trap": "",
        "references": [
            {
                "title": source_title,
                "url": source_url,
                "locator": "官方公告試題（題號與答案）",
                "checkedAt": CHECKED_AT,
            },
            {
                "title": "iPAS AI 應用規劃師官方學習資源",
                "url": OFFICIAL_RESOURCE_URL,
                "locator": "初級學習指引",
                "checkedAt": CHECKED_AT,
            },
        ],
        "editorialNote": "本站尚未完成本題的實質詳解，目前只顯示官方答案。",
        "author": "Codex（AI 輔助初稿）",
        "authoredAt": CHECKED_AT,
    }
    override = EXPLANATION_OVERRIDES.get(question_id)
    if override:
        explanation.update(override)
        explanation["editorialNote"] = (
            "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。"
        )
    if question_id == "aiap-elementary-114-04-ai-foundation-002":
        explanation["references"].extend(
            [
                {
                    "title": "Google Machine Learning Crash Course－Feature crosses",
                    "url": "https://developers.google.com/machine-learning/crash-course/categorical-data/feature-crosses",
                    "locator": "特徵交叉的用途與使用情境",
                    "checkedAt": CHECKED_AT,
                },
                {
                    "title": "Google Research－Wide & Deep Learning for Recommender Systems",
                    "url": "https://research.google/pubs/wide-deep-learning-for-recommender-systems/",
                    "locator": "記憶與泛化的模型架構",
                    "checkedAt": CHECKED_AT,
                },
            ]
        )
    return explanation


def parse_source(source: dict) -> list[dict]:
    if not source["path"].exists():
        raise FileNotFoundError(f"Missing official PDF: {source['path']}")

    reader = PdfReader(source["path"])
    pages = [clean_page(page.extract_text() or "") for page in reader.pages]
    combined_parts = []
    page_starts = []
    cursor = 0
    for page_number, page in enumerate(pages, start=1):
        page_starts.append((cursor, page_number))
        combined_parts.append(page)
        cursor += len(page) + 1
    combined = "\n".join(combined_parts)

    question_pattern = re.compile(
        r"(?m)^\s*([ABCD\uff21\uff22\uff23\uff24])\s+([0-9]{1,2})[.]\s+"
    )
    matches = list(question_pattern.finditer(combined))
    if len(matches) != 50:
        found = [match.group(2) for match in matches]
        raise ValueError(f"{source['sourceId']}: expected 50 questions, found {found}")

    questions = []
    for index, match in enumerate(matches):
        answer = match.group(1).translate(ANSWER_TRANSLATION)
        number = int(match.group(2))
        end = matches[index + 1].start() if index + 1 < len(matches) else len(combined)
        body = combined[match.end() : end]
        option_matches = list(
            re.finditer(r"(?m)^\s*[\(\uff08]([A-D])[\)\uff09]", body)
        )
        labels = [option.group(1) for option in option_matches]
        if labels != ["A", "B", "C", "D"]:
            raise ValueError(
                f"{source['sourceId']} Q{number}: invalid option labels {labels}"
            )

        prompt = normalize_text(body[: option_matches[0].start()])
        options = []
        for option_index, option_match in enumerate(option_matches):
            option_end = (
                option_matches[option_index + 1].start()
                if option_index + 1 < len(option_matches)
                else len(body)
            )
            options.append(
                {
                    "label": option_match.group(1),
                    "text": normalize_text(body[option_match.end() : option_end]),
                }
            )

        source_page = 1
        for start, page_number in page_starts:
            if start <= match.start():
                source_page = page_number
            else:
                break

        source_title = (
            f"114 年第四次初級 AI 應用規劃師"
            f"－{source['subjectLabel']}公告試題"
        )
        question_id = (
            f"aiap-elementary-114-04-"
            f"{source['subjectCode']}-{number:03d}"
        )
        questions.append(
            {
                "id": question_id,
                "sourceId": source["sourceId"],
                "sourceType": "official-exam",
                "level": "elementary",
                "subjectCode": source["subjectCode"],
                "subjectLabel": source["subjectLabel"],
                "rocYear": 114,
                "session": "4",
                "officialQuestionNumber": number,
                "sourcePage": source_page,
                "prompt": prompt,
                "options": options,
                "officialAnswer": [answer],
                "scoring": "single",
                "sourceUrl": source["url"],
                "answerSourceUrl": source["url"],
                "extractionStatus": "verified",
                "explanationStatus": (
                    "draft" if question_id in EXPLANATION_OVERRIDES else "missing"
                ),
                "explanation": build_explanation(
                    question_id, prompt, options, answer, source_title, source["url"]
                ),
            }
        )

    expected_numbers = list(range(1, 51))
    actual_numbers = [question["officialQuestionNumber"] for question in questions]
    if actual_numbers != expected_numbers:
        raise ValueError(
            f"{source['sourceId']}: question numbers are not exactly 1..50"
        )
    return questions


def main() -> None:
    questions = []
    for source in SOURCES:
        questions.extend(parse_source(source))

    if len(questions) != 100:
        raise ValueError(f"Expected 100 questions, got {len(questions)}")
    ids = [question["id"] for question in questions]
    if len(ids) != len(set(ids)):
        raise ValueError("Question IDs are not unique")

    OUTPUT.write_text(
        json.dumps(questions, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {len(questions)} official questions to {OUTPUT}")


if __name__ == "__main__":
    main()
