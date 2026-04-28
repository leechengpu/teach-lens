"""OpenAI Whisper API wrapper｜語音轉錄

Demo 模式：未設 OPENAI_API_KEY 時自動回傳 tests/demo_transcript.json 預錄資料。
"""

from __future__ import annotations
import json
import os
from pathlib import Path

DEMO_TRANSCRIPT_PATH = Path(__file__).resolve().parent.parent / "tests" / "demo_transcript.json"


def is_api_available() -> bool:
    return bool(os.getenv("OPENAI_API_KEY"))


def load_demo_transcript() -> list[dict]:
    """無 API key 時用的預錄逐字稿"""
    return json.loads(DEMO_TRANSCRIPT_PATH.read_text(encoding="utf-8"))


def transcribe(audio_file_path: str, language: str = "zh") -> list[dict]:
    """
    回傳格式：
    [{"segment_idx": 0, "start_sec": 0.0, "end_sec": 3.2, "text": "..."}]
    """
    if not is_api_available():
        return load_demo_transcript()

    try:
        from openai import OpenAI
    except ImportError:
        raise RuntimeError("openai package not installed; run: pip install openai")

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    with open(audio_file_path, "rb") as f:
        response = client.audio.transcriptions.create(
            model="whisper-1",
            file=f,
            language=language,
            response_format="verbose_json",
            timestamp_granularities=["segment"],
        )

    segments = []
    for idx, seg in enumerate(response.segments):
        segments.append({
            "segment_idx": idx,
            "start_sec": float(seg.start),
            "end_sec": float(seg.end),
            "text": seg.text.strip(),
        })
    return segments


def estimate_wer_baseline(audio_file_path: str, ground_truth: str) -> float:
    """
    粗略 WER 估算（為 W1 P0 任務：跑你 4-25 觀課錄音的基線）
    回傳 0.0-1.0 之間的 Word Error Rate。
    """
    segments = transcribe(audio_file_path)
    hypothesis = "".join(s["text"] for s in segments)

    # 中文以「字」為單位計算（不是 word）
    ref = list(ground_truth.replace(" ", ""))
    hyp = list(hypothesis.replace(" ", ""))

    # Levenshtein distance（簡化版）
    m, n = len(ref), len(hyp)
    if m == 0:
        return 1.0 if n > 0 else 0.0

    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if ref[i - 1] == hyp[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])

    return dp[m][n] / m
