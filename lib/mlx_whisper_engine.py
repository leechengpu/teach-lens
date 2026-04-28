"""MLX Whisper 引擎｜macOS Apple Silicon 本機加速

僅在 macOS arm64 環境可用。Linux/Intel/雲端會自動 fallback 到 OpenAI Whisper API。

預設模型：mlx-community/whisper-large-v3-turbo
- 速度：1 分鐘音檔 < 5 秒（M2/M3）
- 品質：與 large-v3 相當
- 首次執行會自動從 HuggingFace 下載（約 1.5GB）
"""

from __future__ import annotations
import os
import platform


def is_available() -> bool:
    """偵測 mlx-whisper 是否可用（套件存在 + macOS arm64）"""
    if platform.system() != "Darwin" or platform.machine() != "arm64":
        return False
    try:
        import mlx_whisper  # noqa: F401
        return True
    except ImportError:
        return False


def transcribe(audio_file_path: str, language: str = "zh",
               model: str | None = None) -> list[dict]:
    """
    回傳格式與 lib.openai_whisper.transcribe 一致：
    [{"segment_idx": 0, "start_sec": 0.0, "end_sec": 3.2, "text": "..."}]
    """
    import mlx_whisper

    model_repo = model or os.getenv(
        "MLX_WHISPER_MODEL",
        "mlx-community/whisper-large-v3-turbo",
    )

    result = mlx_whisper.transcribe(
        audio_file_path,
        path_or_hf_repo=model_repo,
        language=language,
        word_timestamps=False,
        verbose=False,
    )

    segments = []
    for idx, seg in enumerate(result.get("segments", [])):
        segments.append({
            "segment_idx": idx,
            "start_sec": float(seg.get("start", 0.0)),
            "end_sec": float(seg.get("end", 0.0)),
            "text": seg.get("text", "").strip(),
        })
    return segments
