# 系統架構｜TeachLens

## 高階架構圖

```
┌─────────────────────────────────────────────────────────────┐
│                  教師端（Streamlit Web App）                  │
│                                                             │
│   📤 上傳     📊 報告     🎓 回饋     📈 軌跡     🔒 倫理    │
│   (M1+M2)    (M3 視覺化)  (M4)        (M5)        (M6)      │
└──────────────────────────┬──────────────────────────────────┘
                           │
                ┌──────────┴──────────┐
                ↓                     ↓
       ┌─────────────────┐   ┌─────────────────┐
       │  匿名化模組      │   │   API 串接層     │
       │ lib/anonymize.py │   │  ┌────────────┐ │
       └─────────────────┘   │  │OpenAI      │ │
                              │  │Whisper API │ │
                              │  └────────────┘ │
                              │  ┌────────────┐ │
                              │  │Anthropic   │ │
                              │  │Claude API  │ │
                              │  │Sonnet 4.6  │ │
                              │  │+ Opus 4.7  │ │
                              │  └────────────┘ │
                              └────────┬────────┘
                                       ↓
                        ┌─────────────────────────────┐
                        │  分析 Pipeline              │
                        │  lib/transcribe.py          │
                        │                             │
                        │  1. Whisper 轉錄            │
                        │  2. 匿名化                  │
                        │  3. LLM 事件分段（prompt 01）│
                        │  4. 語意角色推論（prompt 03）│
                        │  5. 提問分類（prompt 02）    │
                        │  6. 五維指標計算（analyze.py）│
                        │  7. AI 教練回饋（prompt 04） │
                        └──────────────┬──────────────┘
                                       ↓
                        ┌─────────────────────────────┐
                        │  資料層 SQLite               │
                        │  schemas/create_tables.sql   │
                        │                             │
                        │  - teachers                 │
                        │  - sessions（含同意書全文） │
                        │  - transcripts              │
                        │  - metrics（五維指標）       │
                        │  - feedbacks                │
                        │  - feedback_surveys（試用） │
                        └─────────────────────────────┘
```

## 資料流（Data Flow）

```
[音檔 mp3/wav/m4a] 
   │
   ├─→ Whisper API ──→ [句級逐字稿 + timestamp]
   │                          │
   │                          ↓
   │                   匿名化處理（學生 → S1/S2，教師 → T）
   │                          │
   │                          ↓
   │                   ┌──── LLM 並行分析（3 任務）────┐
   │                   ↓                              ↓
   │           [事件分段]                       [語意角色推論]
   │                   │                              │
   │                   └──────┬─────────────┬────────┘
   │                          ↓             ↓
   │                   [提問分類（Bloom）]   [合併到 segments]
   │                          │             │
   │                          └──────┬──────┘
   │                                 ↓
   │                         [五維指標計算]
   │                                 │
   │                                 ↓
   │                         寫入 metrics 表
   │                                 │
   │                                 ↓
   │                         LLM 教練回饋生成
   │                                 │
   │                                 ↓
   │                         寫入 feedbacks 表
   │
   └─→ 30 天後自動刪除原始檔
```

## MVP 範疇

✅ M1 上傳（同意書 gate）
✅ M2 Whisper 轉錄
✅ M3 五維指標 + Plotly 視覺化
✅ M4 三段式 AI 回饋
✅ M5 縱向軌跡（基礎版，N≥2 顯示）
✅ M6 倫理與隱私管理

## 技術選型決策（為什麼這樣選）

| 決策 | 選擇 | 否決方案 | 理由 |
|------|------|----------|------|
| 前端 | Streamlit | Next.js / Vue | 33 天時程 → 最速 demo；教師熟悉 |
| LLM | Claude Sonnet 4.6 + Opus 4.7 | GPT-4 / Gemini | 已有 API key + 中文表現佳 + 學理回饋深度 |
| 轉錄 | OpenAI Whisper API | whisper.cpp local | 雲端免架 GPU；可隨時切 local 強化隱私 |
| 角色判讀 | LLM 語意推論 | speaker diarization | 中文 diarization WER > 30%，現場 demo 易翻車 |
| DB | SQLite | PostgreSQL | Streamlit Cloud 部署簡單；正式版可換 |
| 部署 | Streamlit Community Cloud | AWS/GCP | 免費；33 天上線；評審當場可訪 |

## 雲端部署（決審必達）

```
GitHub Repo (main branch)
        │
        ↓ Streamlit Cloud 自動同步
        │
   share.streamlit.io
        │
        ↓
   公開 URL: https://teach-lens.streamlit.app
        │
        ↓
   評審手機掃 QR Code → 直接體驗
```

每次 git push 後 1-2 分鐘自動重新部署。
