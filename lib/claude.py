"""Anthropic Claude API wrapper｜LLM 分析任務

Demo 模式：未設 ANTHROPIC_API_KEY 時，分段/分類/角色推論回傳啟發式預設值；
回饋生成回傳預錄範例。
"""

from __future__ import annotations
import json
import os
import re
from pathlib import Path

PROMPT_DIR = Path(__file__).resolve().parent.parent / "prompts"
DEMO_FEEDBACK_PATH = Path(__file__).resolve().parent.parent / "tests" / "demo_feedback.json"

MODEL_FAST = "claude-sonnet-4-6"      # 分段、分類、角色推論
MODEL_DEEP = "claude-opus-4-7"         # 整合性反饋生成


def is_api_available() -> bool:
    return bool(os.getenv("ANTHROPIC_API_KEY"))


def _load_prompt(filename: str) -> str:
    return (PROMPT_DIR / filename).read_text(encoding="utf-8")


def _client():
    try:
        from anthropic import Anthropic
    except ImportError:
        raise RuntimeError("anthropic package not installed; run: pip install anthropic")
    return Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def _call_json(system_prompt: str, user_content: str, model: str = MODEL_FAST) -> list | dict:
    """呼叫 Claude 並解析 JSON 回應（容錯：抽 ```json 區塊）"""
    response = _client().messages.create(
        model=model,
        max_tokens=8192,
        system=system_prompt,
        messages=[{"role": "user", "content": user_content}],
    )
    if not response.content:
        raise RuntimeError(
            f"Claude 回空 content。model={model}, stop_reason={response.stop_reason}, "
            f"usage={response.usage}"
        )
    raw_text = response.content[0].text
    text = raw_text
    match = re.search(r"```(?:json)?\s*(.*?)```", text, re.DOTALL)
    if match:
        text = match.group(1)
    text = text.strip()
    if not text:
        raise RuntimeError(
            f"Claude 回空字串。model={model}, stop_reason={response.stop_reason}, "
            f"raw 前 500 字={raw_text[:500]!r}"
        )
    return json.loads(text)


# === 任務 1：事件分段 ===
def segment_events(transcripts: list[dict]) -> list[dict]:
    if not is_api_available():
        return _heuristic_segment(transcripts)

    prompt = _load_prompt("01_transcript_segmentation.md")
    payload = json.dumps(
        [{"segment_idx": t["segment_idx"], "text": t["text"]} for t in transcripts],
        ensure_ascii=False,
    )
    return _call_json(prompt, payload, MODEL_FAST)


def _heuristic_segment(transcripts: list[dict]) -> list[dict]:
    """無 API 時的啟發式分段"""
    results = []
    for t in transcripts:
        text = t["text"]
        if "?" in text or "？" in text or any(w in text for w in ["為什麼", "怎麼", "什麼", "嗎", "呢"]):
            event_type = "QUESTION"
        elif len(text) < 12:
            event_type = "STUDENT_RESPONSE"
        elif text.startswith(("好", "來", "我們", "現在")):
            event_type = "TRANSITION"
        else:
            event_type = "LECTURE"
        results.append({
            "segment_idx": t["segment_idx"],
            "event_type": event_type,
            "confidence": 0.65,
        })
    return results


# === 任務 2：提問分類 ===
def classify_questions(question_segments: list[dict]) -> list[dict]:
    if not question_segments:
        return []
    if not is_api_available():
        return _heuristic_classify(question_segments)

    prompt = _load_prompt("02_question_classification.md")
    payload = json.dumps(
        [{"segment_idx": s["segment_idx"], "text": s["text"]} for s in question_segments],
        ensure_ascii=False,
    )
    return _call_json(prompt, payload, MODEL_FAST)


def _heuristic_classify(question_segments: list[dict]) -> list[dict]:
    """簡易啟發式：含「為什麼/如何/評論/比較」→ open + 較高 Bloom"""
    results = []
    for s in question_segments:
        text = s["text"]
        if any(w in text for w in ["為什麼", "怎麼會", "解釋", "說明"]):
            openness, level, name = "OPEN", 2, "Understand"
        elif any(w in text for w in ["比較", "區辨", "找出", "分析"]):
            openness, level, name = "OPEN", 4, "Analyze"
        elif any(w in text for w in ["設計", "創造", "提出"]):
            openness, level, name = "OPEN", 6, "Create"
        else:
            openness, level, name = "CLOSED", 1, "Remember"
        results.append({
            "segment_idx": s["segment_idx"],
            "text": text,
            "openness": openness,
            "bloom_level": level,
            "bloom_name": name,
        })
    return results


# === 任務 3：語意角色推論 ===
def infer_roles(transcripts_with_events: list[dict]) -> list[dict]:
    if not is_api_available():
        return _heuristic_infer_roles(transcripts_with_events)

    prompt = _load_prompt("03_dialogue_role_inference.md")
    payload = json.dumps(
        [{"segment_idx": t["segment_idx"], "text": t["text"], "event_type": t.get("event_type")}
         for t in transcripts_with_events],
        ensure_ascii=False,
    )
    return _call_json(prompt, payload, MODEL_FAST)


def _heuristic_infer_roles(segs: list[dict]) -> list[dict]:
    """事件類型映射：QUESTION/LECTURE/TRANSITION → T；STUDENT_RESPONSE → S"""
    results = []
    for s in segs:
        et = s.get("event_type", "LECTURE")
        if et == "STUDENT_RESPONSE":
            role = "S"
        elif et in ("QUESTION", "LECTURE", "TRANSITION"):
            role = "T"
        else:
            role = "T"
        results.append({
            "segment_idx": s["segment_idx"],
            "role": role,
            "confidence": 0.7,
            "reason": "event_type mapping (heuristic)",
        })
    return results


# === 任務 4：教練回饋 ===
def generate_coaching_feedback(metrics: dict, sample_segments: list[dict]) -> list[dict]:
    if not is_api_available():
        return _load_demo_feedback()

    prompt = _load_prompt("04_coaching_feedback.md")
    payload = json.dumps({
        "metrics": metrics,
        "sample_segments": sample_segments[:20],  # 控制 token
    }, ensure_ascii=False)
    return _call_json(prompt, payload, MODEL_DEEP)


def _load_demo_feedback() -> list[dict]:
    if DEMO_FEEDBACK_PATH.exists():
        return json.loads(DEMO_FEEDBACK_PATH.read_text(encoding="utf-8"))
    # 兜底：給一份示範回饋讓 UI 不爆
    return [
        {
            "dimension": "wait_time",
            "evidence": "[Demo 模式] 本堂課 12 個提問中，9 次 (75%) 等待時間 < 1 秒。",
            "interpretation": "Rowe (1972, 1986) 等待時間研究指出，< 1 秒等待會限制學生思考深度。",
            "suggestion": "下次課堂選 2-3 個關鍵提問，刻意默數 3 秒後再追問。",
            "citation": "Rowe, M. B. (1986). Wait time. Journal of Teacher Education, 37(1), 43-50.",
        },
    ]
