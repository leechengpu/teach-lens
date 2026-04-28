"""SQLite 操作層"""

from __future__ import annotations
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterable

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "teachlens.db"
SCHEMA_PATH = Path(__file__).resolve().parent.parent / "schemas" / "create_tables.sql"


def ensure_db_initialized() -> None:
    """雲端首次啟動時自動建表（Streamlit Cloud 容器無持久檔案系統）"""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not DB_PATH.exists():
        with sqlite3.connect(DB_PATH) as conn:
            conn.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
            conn.commit()


@contextmanager
def get_conn():
    ensure_db_initialized()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def insert_session(
    teacher_id: int,
    title: str,
    grade: str,
    subject: str,
    topic: str,
    audio_filename: str,
    audio_duration: float,
    consent_signed: bool,
    consent_text: str,
) -> int:
    with get_conn() as conn:
        cur = conn.execute(
            """
            INSERT INTO sessions (
                teacher_id, title, grade, subject, topic,
                audio_filename, audio_duration, consent_signed, consent_text, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'uploaded')
            """,
            (teacher_id, title, grade, subject, topic,
             audio_filename, audio_duration, int(consent_signed), consent_text),
        )
        return cur.lastrowid


def get_or_create_teacher(nickname: str, role: str) -> int:
    with get_conn() as conn:
        row = conn.execute(
            "SELECT id FROM teachers WHERE nickname = ? AND role = ?",
            (nickname, role),
        ).fetchone()
        if row:
            return row["id"]
        cur = conn.execute(
            "INSERT INTO teachers (nickname, role) VALUES (?, ?)",
            (nickname, role),
        )
        return cur.lastrowid


def update_session_status(session_id: int, status: str) -> None:
    with get_conn() as conn:
        conn.execute(
            "UPDATE sessions SET status = ? WHERE id = ?",
            (status, session_id),
        )


def insert_transcripts(session_id: int, segments: Iterable[dict]) -> None:
    with get_conn() as conn:
        conn.executemany(
            """
            INSERT INTO transcripts (
                session_id, segment_idx, start_sec, end_sec, text,
                role, event_type, question_kind, bloom_level
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [
                (session_id, s["segment_idx"], s["start_sec"], s["end_sec"], s["text"],
                 s.get("role"), s.get("event_type"),
                 s.get("question_kind"), s.get("bloom_level"))
                for s in segments
            ],
        )


def insert_metrics(session_id: int, metrics: dict) -> None:
    with get_conn() as conn:
        cols = ", ".join(metrics.keys())
        placeholders = ", ".join(["?"] * len(metrics))
        conn.execute(
            f"INSERT OR REPLACE INTO metrics (session_id, {cols}) VALUES (?, {placeholders})",
            (session_id, *metrics.values()),
        )


def insert_feedback(session_id: int, dimension: str,
                    evidence: str, interpretation: str,
                    suggestion: str, citation: str) -> None:
    with get_conn() as conn:
        conn.execute(
            """
            INSERT INTO feedbacks (session_id, dimension, evidence, interpretation, suggestion, citation)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (session_id, dimension, evidence, interpretation, suggestion, citation),
        )


def list_sessions(teacher_id: int | None = None) -> list[dict]:
    sql = "SELECT * FROM sessions WHERE deleted_at IS NULL"
    params: tuple = ()
    if teacher_id is not None:
        sql += " AND teacher_id = ?"
        params = (teacher_id,)
    sql += " ORDER BY created_at DESC"
    with get_conn() as conn:
        return [dict(r) for r in conn.execute(sql, params).fetchall()]


def get_session(session_id: int) -> dict | None:
    with get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM sessions WHERE id = ? AND deleted_at IS NULL",
            (session_id,),
        ).fetchone()
        return dict(row) if row else None


def get_transcripts(session_id: int) -> list[dict]:
    with get_conn() as conn:
        return [
            dict(r) for r in conn.execute(
                "SELECT * FROM transcripts WHERE session_id = ? ORDER BY segment_idx",
                (session_id,),
            ).fetchall()
        ]


def get_metrics(session_id: int) -> dict | None:
    with get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM metrics WHERE session_id = ?",
            (session_id,),
        ).fetchone()
        return dict(row) if row else None


def get_feedbacks(session_id: int) -> list[dict]:
    with get_conn() as conn:
        return [
            dict(r) for r in conn.execute(
                "SELECT * FROM feedbacks WHERE session_id = ? ORDER BY id",
                (session_id,),
            ).fetchall()
        ]


def soft_delete_session(session_id: int) -> None:
    """軟刪除：標記 deleted_at；30 天後由清理 job 實際刪除（CASCADE）"""
    with get_conn() as conn:
        conn.execute(
            "UPDATE sessions SET deleted_at = CURRENT_TIMESTAMP, status = 'deleted' WHERE id = ?",
            (session_id,),
        )


def hard_delete_session(session_id: int) -> None:
    """硬刪除（評審現場示範用）：立即清除所有相關資料"""
    with get_conn() as conn:
        conn.execute("DELETE FROM sessions WHERE id = ?", (session_id,))
