-- TeachLens SQLite Schema v0.1
-- 設計原則：每個 session 是一次上傳；transcripts/metrics/feedbacks 為 1:N

PRAGMA foreign_keys = ON;

-- 教師（最小化資訊；此 MVP 不做帳號系統）
CREATE TABLE IF NOT EXISTS teachers (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    nickname        TEXT NOT NULL,           -- 自取暱稱（不存真實姓名）
    role            TEXT,                    -- 職前 / 在職 / 輔導員
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 一次上傳 = 一個 session
CREATE TABLE IF NOT EXISTS sessions (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    teacher_id      INTEGER NOT NULL,
    title           TEXT,                    -- 教師自訂（如「四年級自然 水的三態 微試教」）
    grade           TEXT,                    -- 年級（如「四年級」）
    subject         TEXT,                    -- 學科
    topic           TEXT,                    -- 單元/主題
    audio_filename  TEXT,                    -- 原始檔名（去識別化前）
    audio_duration  REAL,                    -- 秒
    consent_signed  INTEGER NOT NULL DEFAULT 0,  -- 1 = 已勾選同意書（gate 機制）
    consent_text    TEXT,                    -- 同意書當時的全文（保留法律證據）
    status          TEXT DEFAULT 'uploaded', -- uploaded / transcribing / analyzing / done / deleted / failed
    deleted_at      TIMESTAMP,               -- 軟刪除（30 天後實際清除）
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (teacher_id) REFERENCES teachers(id)
);

-- 句級逐字稿（Whisper 轉錄後 + LLM 分段角色）
CREATE TABLE IF NOT EXISTS transcripts (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id      INTEGER NOT NULL,
    segment_idx     INTEGER NOT NULL,        -- 句序
    start_sec       REAL NOT NULL,
    end_sec         REAL NOT NULL,
    text            TEXT NOT NULL,           -- 已匿名化（學生 → S1/S2，教師 → T）
    role            TEXT,                    -- T / S / TRANSITION（LLM 推論）
    event_type      TEXT,                    -- LECTURE / QUESTION / STUDENT_RESPONSE / TRANSITION
    question_kind   TEXT,                    -- CLOSED / OPEN / FOLLOW_UP（NULL if not question）
    bloom_level     INTEGER,                 -- 1-6（Anderson & Krathwohl 修訂版）
    FOREIGN KEY (session_id) REFERENCES sessions(id) ON DELETE CASCADE
);

-- 五維指標（聚合後）
CREATE TABLE IF NOT EXISTS metrics (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id          INTEGER NOT NULL UNIQUE,
    -- 1. Talk Time Ratio
    teacher_talk_sec    REAL,
    student_talk_sec    REAL,
    transition_sec      REAL,
    -- 2. Question Types
    closed_q_count      INTEGER DEFAULT 0,
    open_q_count        INTEGER DEFAULT 0,
    followup_q_count    INTEGER DEFAULT 0,
    -- 3. Wait Time（提問到下一個發話的平均秒數）
    wait_time_avg       REAL,
    wait_time_median    REAL,
    wait_time_under_1s  INTEGER DEFAULT 0,   -- 等待 < 1 秒的提問次數（Rowe 警示區）
    -- 4. Bloom Level Distribution（提問層級分布）
    bloom_l1_remember   INTEGER DEFAULT 0,
    bloom_l2_understand INTEGER DEFAULT 0,
    bloom_l3_apply      INTEGER DEFAULT 0,
    bloom_l4_analyze    INTEGER DEFAULT 0,
    bloom_l5_evaluate   INTEGER DEFAULT 0,
    bloom_l6_create     INTEGER DEFAULT 0,
    -- 5. Dialogue Pattern (IRE / IRF / Dialogic 比例)
    pattern_ire_count   INTEGER DEFAULT 0,
    pattern_irf_count   INTEGER DEFAULT 0,
    pattern_dialogic    INTEGER DEFAULT 0,
    --
    computed_at         TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES sessions(id) ON DELETE CASCADE
);

-- AI 教練三段式回饋
CREATE TABLE IF NOT EXISTS feedbacks (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id      INTEGER NOT NULL,
    dimension       TEXT NOT NULL,           -- talk_ratio / question_types / wait_time / bloom / dialogue_pattern
    evidence        TEXT NOT NULL,           -- 引用具體片段 + timestamp
    interpretation  TEXT NOT NULL,           -- 學理判讀
    suggestion      TEXT NOT NULL,           -- 改寫建議（含具體話術）
    citation        TEXT,                    -- 引用之研究文獻（如 "Rowe, 1986"）
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES sessions(id) ON DELETE CASCADE
);

-- 試用回饋問卷（W3-W4 試用驗證資料）
CREATE TABLE IF NOT EXISTS feedback_surveys (
    id                     INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id             INTEGER NOT NULL,
    teacher_role           TEXT,             -- 職前 / 在職 / 輔導員
    q1_usefulness          INTEGER,          -- Likert 1-5：本工具對我的反思有幫助
    q2_accuracy            INTEGER,          -- Likert 1-5：分析結果與我的自我感受一致
    q3_actionable          INTEGER,          -- Likert 1-5：建議具體可實踐
    q4_willingness         INTEGER,          -- Likert 1-5：我願意持續使用
    q5_recommend           INTEGER,          -- Likert 1-5：我會推薦給同事
    open_feedback          TEXT,             -- 開放回答
    created_at             TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES sessions(id) ON DELETE CASCADE
);

-- Index
CREATE INDEX IF NOT EXISTS idx_sessions_teacher ON sessions(teacher_id);
CREATE INDEX IF NOT EXISTS idx_sessions_status ON sessions(status);
CREATE INDEX IF NOT EXISTS idx_transcripts_session ON transcripts(session_id);
CREATE INDEX IF NOT EXISTS idx_metrics_session ON metrics(session_id);
CREATE INDEX IF NOT EXISTS idx_feedbacks_session ON feedbacks(session_id);
