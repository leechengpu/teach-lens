"""學生姓名匿名化｜倫理機制核心模組

設計原則：
1. 在逐字稿落地前就執行（不寫入 DB 前先匿名化）
2. 教師 → T；學生 → S1, S2, S3（依出現序）
3. 偵測到的人名同時也被替換為 S{序號}
4. 此模組不依賴外部 API；純 Python，可離線執行
"""

from __future__ import annotations
import re

# 常見台灣姓氏（用於正則啟發；非完整清單）
COMMON_SURNAMES = "陳林黃張李王吳劉蔡楊許鄭謝郭洪邱曾廖賴徐周葉蘇莊呂江何蕭羅高潘簡朱鍾游彭詹胡施沈余趙盧梁韓馬唐方紀傅"

# 教師自稱關鍵字（多為老師主動提及學生姓名）
TEACHER_ADDRESSING = ["小朋友", "同學", "你", "妳"]


def detect_name_candidates(text: str) -> list[str]:
    """偵測可能的中文姓名（保守策略：2-3 字、首字為常見姓氏）"""
    pattern = rf"[{COMMON_SURNAMES}][一-鿿]{{1,2}}"
    candidates = re.findall(pattern, text)
    # 去重保序
    seen = set()
    result = []
    for name in candidates:
        if name not in seen:
            seen.add(name)
            result.append(name)
    return result


def anonymize_transcript(segments: list[dict]) -> tuple[list[dict], dict]:
    """
    對逐字稿做匿名化，回傳 (匿名化後 segments, 對照表)
    對照表僅在 session 內有效，不寫入 DB。
    """
    name_to_label: dict[str, str] = {}
    student_counter = 1

    for seg in segments:
        names = detect_name_candidates(seg["text"])
        for name in names:
            if name not in name_to_label:
                name_to_label[name] = f"S{student_counter}"
                student_counter += 1

    # 替換
    new_segments = []
    for seg in segments:
        new_text = seg["text"]
        # 由長到短替換，避免「李小明」被「李小」先匹配
        for name in sorted(name_to_label.keys(), key=len, reverse=True):
            new_text = new_text.replace(name, name_to_label[name])
        new_segments.append({**seg, "text": new_text})

    return new_segments, name_to_label


def is_safe_to_persist(text: str) -> bool:
    """寫入 DB 前最後一道閘門：偵測是否仍含疑似真實姓名"""
    candidates = detect_name_candidates(text)
    return len(candidates) == 0
