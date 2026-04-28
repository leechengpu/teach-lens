"""轉錄引擎 Router｜統一入口

優先順序：
1. mlx-whisper（macOS Apple Silicon 本機加速；最快）
2. OpenAI Whisper API（雲端可用；雲端部署主力）
3. Demo 模式（無 key 時用預錄逐字稿）

可用環境變數 TRANSCRIBE_ENGINE 強制指定：
  - "mlx" / "openai" / "demo"
"""

from __future__ import annotations
import os
from . import mlx_whisper_engine, openai_whisper


def get_active_engine() -> str:
    """回傳目前實際使用的引擎名稱"""
    forced = os.getenv("TRANSCRIBE_ENGINE", "").lower()
    if forced == "mlx" and mlx_whisper_engine.is_available():
        return "mlx"
    if forced == "openai" and openai_whisper.is_api_available():
        return "openai"
    if forced == "demo":
        return "demo"

    # Auto-detect
    if mlx_whisper_engine.is_available():
        return "mlx"
    if openai_whisper.is_api_available():
        return "openai"
    return "demo"


def get_engine_label() -> str:
    """給 UI 顯示用的人類可讀標籤"""
    engine = get_active_engine()
    return {
        "mlx": "🚀 MLX Whisper（本機 Apple Silicon 加速）",
        "openai": "☁️ OpenAI Whisper API（雲端）",
        "demo": "ℹ️ Demo 模式（預錄逐字稿）",
    }[engine]


def transcribe(audio_file_path: str, language: str = "zh") -> list[dict]:
    """
    統一轉錄入口；自動依環境選引擎。
    回傳格式：[{"segment_idx": int, "start_sec": float, "end_sec": float, "text": str}]
    """
    engine = get_active_engine()

    if engine == "mlx":
        return mlx_whisper_engine.transcribe(audio_file_path, language=language)
    if engine == "openai":
        return openai_whisper.transcribe(audio_file_path, language=language)
    # demo
    return openai_whisper.load_demo_transcript()
