"""五維指標計算｜Flanders × Rowe × Bloom × Mehan"""

from __future__ import annotations
from statistics import median, mean


def compute_metrics(segments: list[dict]) -> dict:
    """
    輸入：已完成事件分段、角色推論、提問分類的 segments
    輸出：metrics dict（直接寫入 DB metrics 表）
    """
    return {
        # 1. Talk Time Ratio
        **_talk_time_ratio(segments),
        # 2. Question Types
        **_question_types(segments),
        # 3. Wait Time (Rowe)
        **_wait_time(segments),
        # 4. Bloom Distribution
        **_bloom_distribution(segments),
        # 5. Dialogue Pattern (IRE/IRF/Dialogic)
        **_dialogue_pattern(segments),
    }


def _talk_time_ratio(segments: list[dict]) -> dict:
    teacher = sum(s["end_sec"] - s["start_sec"] for s in segments if s.get("role") == "T")
    student = sum(s["end_sec"] - s["start_sec"] for s in segments if s.get("role") == "S")
    transition = sum(s["end_sec"] - s["start_sec"] for s in segments
                     if s.get("event_type") == "TRANSITION")
    return {
        "teacher_talk_sec": round(teacher, 2),
        "student_talk_sec": round(student, 2),
        "transition_sec": round(transition, 2),
    }


def _question_types(segments: list[dict]) -> dict:
    closed = open_q = followup = 0
    for s in segments:
        kind = s.get("question_kind")
        if kind == "CLOSED":
            closed += 1
        elif kind == "OPEN":
            open_q += 1
        elif kind == "FOLLOW_UP":
            followup += 1
    return {
        "closed_q_count": closed,
        "open_q_count": open_q,
        "followup_q_count": followup,
    }


def _wait_time(segments: list[dict]) -> dict:
    """
    對於每個 QUESTION，計算其結束到下一個 STUDENT_RESPONSE / LECTURE 起始的時間差
    （Rowe Wait Time I：提問後等待）
    """
    waits = []
    for i, s in enumerate(segments):
        if s.get("event_type") != "QUESTION":
            continue
        next_seg = next((segments[j] for j in range(i + 1, len(segments))
                         if segments[j].get("event_type") in ("STUDENT_RESPONSE", "LECTURE")), None)
        if next_seg:
            wait = next_seg["start_sec"] - s["end_sec"]
            if wait >= 0:  # 安全護欄（重疊不算）
                waits.append(wait)

    if not waits:
        return {"wait_time_avg": 0.0, "wait_time_median": 0.0, "wait_time_under_1s": 0}

    return {
        "wait_time_avg": round(mean(waits), 2),
        "wait_time_median": round(median(waits), 2),
        "wait_time_under_1s": sum(1 for w in waits if w < 1.0),
    }


def _bloom_distribution(segments: list[dict]) -> dict:
    counts = {f"bloom_l{i}_{name}": 0 for i, name in enumerate(
        ["remember", "understand", "apply", "analyze", "evaluate", "create"], start=1)}
    name_lookup = {1: "bloom_l1_remember", 2: "bloom_l2_understand",
                   3: "bloom_l3_apply", 4: "bloom_l4_analyze",
                   5: "bloom_l5_evaluate", 6: "bloom_l6_create"}
    for s in segments:
        lvl = s.get("bloom_level")
        if lvl and lvl in name_lookup:
            counts[name_lookup[lvl]] += 1
    return counts


def _dialogue_pattern(segments: list[dict]) -> dict:
    """
    IRE: Initiation (T) → Response (S) → Evaluation (T 短評)
    IRF: Initiation (T) → Response (S) → Feedback (T 追問)
    Dialogic: 多回合 S↔S 或 S↔T 互動，無明顯 T 終結
    """
    ire = irf = dialogic = 0
    n = len(segments)
    for i in range(n - 2):
        a, b, c = segments[i], segments[i + 1], segments[i + 2]
        if (a.get("event_type") == "QUESTION"
                and b.get("event_type") == "STUDENT_RESPONSE"):
            if c.get("role") == "T" and c.get("event_type") == "QUESTION":
                irf += 1  # 教師追問
            elif c.get("role") == "T":
                ire += 1  # 教師評鑑或結束
            elif c.get("role") == "S":
                dialogic += 1  # 學生接續
    return {
        "pattern_ire_count": ire,
        "pattern_irf_count": irf,
        "pattern_dialogic": dialogic,
    }


def merge_segments(
    transcripts: list[dict],
    events: list[dict],
    roles: list[dict],
    questions: list[dict],
) -> list[dict]:
    """把各 LLM 任務結果合併到單一 segments list"""
    by_idx = {t["segment_idx"]: dict(t) for t in transcripts}
    for e in events:
        by_idx[e["segment_idx"]]["event_type"] = e["event_type"]
    for r in roles:
        by_idx[r["segment_idx"]]["role"] = r["role"]
    for q in questions:
        seg = by_idx[q["segment_idx"]]
        seg["question_kind"] = q["openness"]
        seg["bloom_level"] = q["bloom_level"]
    return [by_idx[k] for k in sorted(by_idx.keys())]
