# 學理引用文獻｜TeachLens

> 系統設計的每個指標都「有出處」。本文件作為說明書「教育學理基礎」一頁的依據備查。

## 一、課堂語言研究經典

### Flanders, N. A. (1970). *Analyzing Teaching Behavior*. Addison-Wesley.
**對應指標**：師生發話比、互動節奏

Flanders Interaction Analysis Categories (FIAC) 將課堂語言分為 10 類，是課堂觀察的奠基性工具。本系統將其當代 AI 化重構：以 LLM 自動標註替代人工編碼，但保留 FIAC 對「教師主導 / 學生主動 / 靜默」三大分類的核心架構。

### Mehan, H. (1979). *Learning Lessons: Social Organization in the Classroom*. Harvard University Press.
**對應指標**：對話結構模式（IRE）

Mehan 提出 Initiation-Response-Evaluation (IRE) 是教師主導課堂最普遍的對話結構。本系統用此判讀課堂以「教師主導終結」為主，還是有 IRF 追問、Dialogic 學生接續。

### Cazden, C. B. (2001). *Classroom Discourse: The Language of Teaching and Learning* (2nd ed.). Heinemann.
**對應指標**：整體課堂語言架構

Cazden 將課堂語言研究系統化，是 LLM 提示詞設計時的學理底層參考。

### Sinclair, J., & Coulthard, M. (1975). *Towards an Analysis of Discourse*. Oxford University Press.
**對應指標**：語意角色推論

Sinclair-Coulthard 模型描述教師發話特徵（較長、含教學詞彙、含問句）vs 學生發話特徵（較短、回應導向）。本系統 prompt 03（語意角色推論）的啟發式來源。

### Wells, G. (1999). *Dialogic Inquiry: Towards a Sociocultural Practice and Theory of Education*. Cambridge University Press.
**對應指標**：對話結構模式（Dialogic）

Wells 主張 Dialogic Inquiry（多回合學生互動）才是促進深度學習的關鍵，與 Mehan IRE 形成對照。

---

## 二、提問與等待時間研究

### Rowe, M. B. (1972). Wait-time and rewards as instructional variables, their influence on language, logic, and fate control.
### Rowe, M. B. (1986). Wait time: Slowing down may be a way of speeding up. *Journal of Teacher Education*, 37(1), 43-50.
**對應指標**：等待時間（Wait Time）

Rowe 的研究指出：教師提問後若等待 < 1 秒就追問或自答，學生回答長度、推論性、互動量都顯著偏低。延長到 3 秒以上，全部指標明顯改善。本系統「等待時間 < 1 秒警示區」直接源自這篇。

### Anderson, L. W., & Krathwohl, D. R. (2001). *A Taxonomy for Learning, Teaching, and Assessing: A Revision of Bloom's Taxonomy of Educational Objectives*. Longman.
**對應指標**：Bloom 認知層級分布

Anderson & Krathwohl 修訂版 Bloom 將原先的「Knowledge」改為「Remember」，加入「Create」為最高層，並把「動詞」與「名詞」分離。本系統採此修訂版（非 1956 原版）。

### Wragg, E. C., & Brown, G. (2001). *Questioning in the Primary School*. Routledge.
**對應指標**：提問類型分類（封閉/開放/追問）

針對小學現場提供具體分類指引，對應 prompt 02 的判讀規則。

### Webb, N. L. (2002). *Depth-of-Knowledge Levels for Four Content Areas*.
**對應指標**：（MVP 簡化版未採用，Webb DOK 與 Bloom 層級重複時取 Bloom）

備案；若 W4 後 N≥10 堂課數據成熟，可考慮加入。

---

## 三、教師專業發展與反思實踐

### Schön, D. A. (1983). *The Reflective Practitioner: How Professionals Think in Action*. Basic Books.
**對應整體系統定位**

本系統定位為 Reflective Practice 工具，不取代教師判斷，協助「行動後反思」（reflection-on-action）。

### Hattie, J. (2009). *Visible Learning: A Synthesis of Over 800 Meta-Analyses Relating to Achievement*. Routledge.
**對應 AI 教練回饋設計**

Hattie 的研究強調反饋必須具體、可追溯、可行動。本系統「證據—判讀—建議」三段式直接呼應這個原則。

### Michaels, S., & O'Connor, C. (2015). Conceptualizing Talk Moves as Tools.
**對應對話結構分析**

Talk Moves 提供具體的學術討論引導語（如「誰可以再補充？」「你的理由是什麼？」），是建議段落具體話術的來源。

---

## 四、教學科技整合框架

### Mishra, P., & Koehler, M. J. (2006). Technological Pedagogical Content Knowledge: A framework for teacher knowledge. *Teachers College Record*, 108(6), 1017-1054.
**對應整體系統定位**

TPACK 是師資培育領域近 20 年最主流的數位教學素養框架。本系統定位為「協助職前教師發展 TPK（科技教學知識）的反思工具」。

**註**：本作品作者博論主軸採用 PK-GenAI-TPACK 擴充框架（2024-2026），是 TPACK 在生成式 AI 時代的延伸。

### UNESCO (2024). *AI Competency Framework for Teachers (AI CFT)*.
**對應倫理機制與系統定位**

UNESCO AI CFT 五原則：
1. 以人為本（Human-centered）
2. AI for social good
3. 多元觀點
4. 可持續性
5. 倫理透明

本系統倫理機制設計直接對齊第 1 條（教師主導）與第 5 條（透明可審）。

---

## 五、敘事探究與實踐性知識（與作者博論連動）

### Elbaz, F. (1981). The teacher's "practical knowledge": Report of a case study. *Curriculum Inquiry*, 11(1), 43-71.
### Connelly, F. M., & Clandinin, D. J. (1988). *Teachers as Curriculum Planners: Narratives of Experience*. Teachers College Press.

本系統累積的「課堂語言數據 + 教師反思」可作為實踐性知識（practical knowledge / personal practical knowledge）發展的可視化記錄，呼應作者博論「國小自然科教師 AI 教學素養發展之敘事探究」（v4.0, 2026-04-24）的研究主軸。

---

## 六、引用建議優先序（說明書 10 頁版）

若版面有限，建議引用優先序：
1. **Flanders (1970)** — 師生發話比的學理出處
2. **Rowe (1972, 1986)** — 等待時間指標的唯一正當性來源
3. **Anderson & Krathwohl (2001)** — Bloom 修訂版
4. **Mishra & Koehler (2006)** — TPACK 整體框架
5. **UNESCO AI CFT (2024)** — 倫理與政策對接
6. **Mehan (1979)** — IRE / 對話結構

七層學理護甲足以應付決審任何學理質疑。
