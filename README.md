# 教學透鏡 TeachLens

> 上傳一段微試教錄音，5 分鐘內看見原本看不見的自己。

師資培育用 AI 課堂語言診斷系統 — 為 2026 國立東華大學第一屆 AI 教育博覽會（AI 系統開發組）設計。

## 系統定位（四句賣點）

1. TeachLens 不是逐字稿工具，是建立在 **Flanders、Rowe、Bloom** 學理基礎上的課堂語言診斷系統。
2. TeachLens 不給空泛 AI 評語，而是用時間戳記提供「**證據—判讀—建議**」可追溯回饋。
3. TeachLens 不只看單堂課，而是陪伴職前教師從講述型走向啟發型的 **TPACK** 成長歷程。
4. TeachLens 不取代觀課教師，而是讓師資培育擁有可量化、可反思、可累積的數據語言。

## 教育學理基礎

| 系統指標 | 學理依據 |
|---------|----------|
| 師生發話比、互動節奏 | Flanders (1970) Interaction Analysis Categories (FIAC) |
| 等待時間 (Wait Time) | Rowe (1972, 1986) Wait Time I & II |
| 提問層次 | Anderson & Krathwohl (2001) Bloom 修訂版 |
| 整體框架 | Mishra & Koehler (2006) TPACK + UNESCO AI CFT (2024) |

## 五維診斷指標（MVP）

1. **Talk Time Ratio** — 教師 vs 學生發話時間比
2. **Question Types** — 封閉題 / 開放題 / 追問 占比
3. **Wait Time** — 提問後平均等待時間（秒）
4. **Bloom Level Distribution** — 記憶 / 理解 / 應用 / 分析 / 評鑑 / 創造
5. **Dialogue Pattern** — IRE / IRF / Dialogic 比例

## MVP 範疇（W1-W5）

✅ 上傳 mp3/wav/m4a（3-8 分鐘）
✅ Whisper 轉錄 + 句級時間戳
✅ LLM 自動分段（講授 / 提問 / 學生發言 / 過渡）— 用語意角色推論取代 speaker diarization
✅ 五維指標計算 + Plotly 儀表板
✅ AI 教練「證據—判讀—建議」三段式回饋
⬜ 多堂課縱向追蹤（W5+ / 未來擴充）
⬜ 校本/輔導團匯總視角（未來擴充）

## 快速開始（本機）

```bash
./init.sh                              # 一次性建環境（venv + DB）
source .venv/bin/activate
streamlit run app.py                   # 開啟 http://localhost:8501
```

**API Key 設定**（可選；沒設會走 Demo 模式）：

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
export OPENAI_API_KEY="sk-..."         # 用於 Whisper 轉錄（雲端用）
```

**🚀 macOS Apple Silicon 本機加速**（強烈建議；轉錄速度 10x 以上）：

```bash
source .venv/bin/activate
pip install -r requirements-mac.txt    # 安裝 mlx-whisper
```

系統會自動偵測並啟用 MLX 引擎；首次執行會從 HuggingFace 下載
`whisper-large-v3-turbo` 模型（約 1.5GB）。1 分鐘音檔轉錄 < 5 秒（M2/M3 實測）。

**轉錄引擎自動選擇順序**：
1. mlx-whisper（macOS arm64 + 套件已裝） → 本機加速
2. OpenAI Whisper API（OPENAI_API_KEY 已設） → 雲端可用
3. Demo 模式 → 預錄逐字稿（無 key 也能展示）

可用 `TRANSCRIBE_ENGINE=openai|mlx|demo` 強制指定。

## 部署到 Streamlit Community Cloud

1. Fork / Clone 此 repo 到自己的 GitHub 帳號
2. 到 <https://share.streamlit.io> → `New app` → 選此 repo / `main` / `app.py`
3. `Advanced settings → Secrets` 填入：
   ```toml
   ANTHROPIC_API_KEY = "sk-ant-..."
   OPENAI_API_KEY = "sk-..."
   ```
4. 按 `Deploy`，1-2 分鐘完成

雲端啟動時會自動從 `schemas/create_tables.sql` 建 SQLite DB，不用手動 init。

> **Streamlit Cloud 限制**：每次重啟會清檔案系統，DB 為示範用，不存長期資料。正式版請改 PostgreSQL + S3。

## 專案結構

```
teach-lens/
├── README.md
├── app.py                       # Streamlit 主入口（首頁 + 同意書 gate）
├── init.sh                      # 一次性環境建置
├── requirements.txt
├── runtime.txt                  # Streamlit Cloud Python 版本
├── .streamlit/config.toml       # 主題 + 設定
├── schemas/create_tables.sql    # SQLite schema
├── prompts/                     # LLM system prompts
│   ├── 01_transcript_segmentation.md
│   ├── 02_question_classification.md
│   ├── 03_dialogue_role_inference.md
│   └── 04_coaching_feedback.md
├── lib/                         # 核心邏輯
│   ├── transcribe.py           # Whisper 轉錄
│   ├── analyze.py              # 五維指標計算
│   ├── claude.py               # Anthropic API wrapper
│   ├── openai_whisper.py       # OpenAI Whisper API wrapper
│   ├── anonymize.py            # 學生姓名匿名化
│   └── db.py                   # SQLite 操作
├── pages/                       # Streamlit 多頁面
│   ├── 1_📤_上傳與分析.py
│   ├── 2_📊_診斷報告.py
│   ├── 3_🎓_AI教練回饋.py
│   ├── 4_📈_成長軌跡.py
│   └── 5_🔒_倫理與隱私.py
├── tests/                       # Demo 種子資料
│   ├── demo_data.sql
│   ├── demo_transcript.json    # 預錄逐字稿（無 API key 時用）
│   └── demo_audio/             # 測試音檔
├── docs/                        # 學理依據與引用文獻
└── data/                        # SQLite DB（gitignore）
```

## 倫理機制（六條可驗證設計）

| 原則 | 系統實作 |
|------|---------|
| 錄音前告知與同意 | 上傳介面強制勾選同意書，未勾選不可上傳 |
| 學生資料去識別化 | 逐字稿生成時自動將人名替換為 S1/S2/S3，教師為 T |
| 資料刪除權 | 每筆資料附「永久刪除」按鈕，連同音檔/逐字稿/分析全清 |
| 用途限定 | 首頁明示「僅供職前教師自我反思，不得用於評鑑」 |
| AI 限制提醒 | 每份報告底部固定附註「AI 結果僅供參考，最終判讀由教師確認」 |
| 著作權與資料保存 | 音檔處理後 30 天自動刪除原始檔；明示不用於模型訓練 |

**MVP 範疇限定**：本階段僅開放「微試教 / 試教演練」場景使用，無真實學生課堂錄音。涉及學生之真實課堂須另行取得家長集體同意書，為下階段擴充項目。

## 作者

李政蒲｜東華大學科學教育研究所博士生｜114 學年度花蓮縣候用校長｜花蓮縣國教輔導團數學領域輔導員

## 授權

個人專案，未公開授權。
