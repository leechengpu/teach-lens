"""主分析 pipeline：上傳音檔 → 轉錄 → 分段 → 角色 → 分類 → 指標 → 回饋"""

from __future__ import annotations
from . import transcribe_engine, claude, analyze, anonymize, db


def run_pipeline(
    audio_file_path: str,
    teacher_id: int,
    title: str,
    grade: str,
    subject: str,
    topic: str,
    consent_signed: bool,
    consent_text: str,
    audio_duration: float,
    progress_cb=None,
) -> int:
    """
    完整 pipeline；回傳 session_id
    progress_cb: 可選 callback(stage, percent)，給 Streamlit progress bar
    """
    if not consent_signed:
        raise ValueError("未勾選同意書，無法處理錄音檔")

    def _p(stage: str, pct: int):
        if progress_cb:
            progress_cb(stage, pct)

    # 0. 建 session
    _p("建立 session", 5)
    session_id = db.insert_session(
        teacher_id=teacher_id,
        title=title,
        grade=grade,
        subject=subject,
        topic=topic,
        audio_filename=audio_file_path.rsplit("/", 1)[-1],
        audio_duration=audio_duration,
        consent_signed=consent_signed,
        consent_text=consent_text,
    )

    try:
        # 1. Whisper 轉錄
        _p("Whisper 語音轉錄中", 15)
        db.update_session_status(session_id, "transcribing")
        raw_segments = transcribe_engine.transcribe(audio_file_path)

        # 2. 匿名化（在落地任何資料前先做）
        _p("學生姓名匿名化", 30)
        anon_segments, name_map = anonymize.anonymize_transcript(raw_segments)

        # 3. LLM 事件分段
        _p("LLM 事件分段（講授/提問/學生發言/過渡）", 45)
        db.update_session_status(session_id, "analyzing")
        events = claude.segment_events(anon_segments)

        # 4. 語意角色推論
        _p("語意角色推論（取代 speaker diarization）", 60)
        merged_for_roles = analyze.merge_segments(anon_segments, events, [], [])
        roles = claude.infer_roles(merged_for_roles)

        # 5. 提問分類
        _p("提問分類（Bloom 修訂版）", 75)
        question_segs = [s for e, s in zip(events, anon_segments)
                         if e["event_type"] == "QUESTION"]
        classifications = claude.classify_questions(question_segs)

        # 6. 合併、計算指標
        _p("五維指標計算", 85)
        merged = analyze.merge_segments(anon_segments, events, roles, classifications)
        db.insert_transcripts(session_id, merged)

        metrics = analyze.compute_metrics(merged)
        db.insert_metrics(session_id, metrics)

        # 7. AI 教練回饋
        _p("AI 教練「證據—判讀—建議」生成", 95)
        feedbacks = claude.generate_coaching_feedback(metrics, merged)
        for fb in feedbacks:
            db.insert_feedback(
                session_id=session_id,
                dimension=fb.get("dimension", "general"),
                evidence=fb.get("evidence", ""),
                interpretation=fb.get("interpretation", ""),
                suggestion=fb.get("suggestion", ""),
                citation=fb.get("citation", ""),
            )

        db.update_session_status(session_id, "done")
        _p("分析完成", 100)
        return session_id

    except Exception as e:
        db.update_session_status(session_id, "failed")
        raise
