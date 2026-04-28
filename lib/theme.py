"""TeachLens 視覺主題注入器（基於 Claude Design handoff）"""

from __future__ import annotations
from pathlib import Path
import streamlit as st

CSS_PATH = Path(__file__).resolve().parent.parent / "static" / "teachlens.css"


def inject_theme() -> None:
    """每個 Streamlit page 開頭呼叫一次，注入 TeachLens design tokens + 元件樣式"""
    css = CSS_PATH.read_text(encoding="utf-8")
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def render_callout(*, tone: str, icon_svg: str, title: str, body_html: str) -> None:
    """Notion-style callout（藍/紫雙色）"""
    icon_color_class = {"blue": "blue", "plum": "plum"}.get(tone, "blue")
    st.markdown(
        f"""
        <div class="tl-callout tl-callout--{tone}">
          <div class="tl-callout-icon {icon_color_class}">{icon_svg}</div>
          <div style="flex:1">
            <div class="tl-callout-title">{title}</div>
            <div class="tl-callout-body">{body_html}</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# 常用 SVG icons (24x24, currentColor stroke)
ICON_SHIELD = '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3 4 6v6c0 5 3.5 8 8 9 4.5-1 8-4 8-9V6l-8-3Z"/><path d="m9 12 2 2 4-4"/></svg>'
ICON_LOCK   = '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/></svg>'
ICON_MIC    = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="3" width="6" height="12" rx="3"/><path d="M5 11a7 7 0 0 0 14 0M12 18v3"/></svg>'
ICON_BRAIN  = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M8 4a3 3 0 0 0-3 3v1a3 3 0 0 0-2 2.8c0 1.6 1 2.7 2 3 0 1.7 1 3 3 3.2.4 1.7 1.7 3 3 3V4Z"/><path d="M16 4a3 3 0 0 1 3 3v1a3 3 0 0 1 2 2.8c0 1.6-1 2.7-2 3 0 1.7-1 3-3 3.2-.4 1.7-1.7 3-3 3V4Z"/></svg>'
ICON_BAR    = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/></svg>'
ICON_SPARKLES = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="m12 3 1.6 4.4L18 9l-4.4 1.6L12 15l-1.6-4.4L6 9l4.4-1.6L12 3Z"/><path d="M19 14l.7 2 2 .7-2 .7-.7 2-.7-2-2-.7 2-.7.7-2Z"/></svg>'
