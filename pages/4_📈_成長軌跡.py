"""縱向成長軌跡（W5+ / 未來擴充功能）"""

from __future__ import annotations
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from lib import db
from lib.theme import inject_theme

st.set_page_config(page_title="成長軌跡｜TeachLens", page_icon="📈", layout="wide")
inject_theme()
st.title("📈 縱向教學成長軌跡")

st.info("""
📌 **本功能為下階段擴充**

完整縱向追蹤需要 N≥5 堂課的累積資料，目前展示為「資料聚合骨架」。
MVP 階段聚焦於單堂課診斷與三段式回饋。
""")

sessions = db.list_sessions()
if len(sessions) < 2:
    st.warning(f"目前僅有 {len(sessions)} 堂課資料，至少需要 2 堂才能展示趨勢。")
    st.caption("請先到「📤 上傳與分析」累積更多資料。")
    st.stop()

# === 資料聚合 ===
rows = []
for s in sessions:
    m = db.get_metrics(s["id"])
    if not m:
        continue
    teacher = m["teacher_talk_sec"] or 0
    student = m["student_talk_sec"] or 0
    total = teacher + student or 1
    open_total = (m["open_q_count"] or 0)
    closed_total = (m["closed_q_count"] or 0)
    q_total = open_total + closed_total or 1
    rows.append({
        "session_id": s["id"],
        "title": s["title"] or f"Session #{s['id']}",
        "created": s["created_at"][:10],
        "教師發話比": round(teacher / total * 100, 1),
        "學生發話比": round(student / total * 100, 1),
        "開放題占比": round(open_total / q_total * 100, 1),
        "平均等待時間": m["wait_time_avg"] or 0,
        "高階提問比": round(
            sum(m[f"bloom_l{i}_{n}"] or 0 for i, n in [(4, "analyze"), (5, "evaluate"), (6, "create")])
            / max(1, sum(m[f"bloom_l{i}_{n}"] or 0 for i, n in [
                (1, "remember"), (2, "understand"), (3, "apply"),
                (4, "analyze"), (5, "evaluate"), (6, "create")])) * 100, 1
        ),
    })

if not rows:
    st.info("尚無已完成分析的 session。")
    st.stop()

df = pd.DataFrame(rows).sort_values("session_id")
st.dataframe(df, use_container_width=True, hide_index=True)

st.divider()
st.subheader("📊 跨堂趨勢圖")

fig = go.Figure()
for col, color in [
    ("學生發話比", "#A23B72"),
    ("開放題占比", "#2A9D8F"),
    ("高階提問比", "#F18F01"),
]:
    fig.add_trace(go.Scatter(
        x=df["session_id"], y=df[col], name=col, mode="lines+markers",
        line=dict(color=color, width=3),
    ))
fig.update_layout(
    xaxis_title="Session #",
    yaxis_title="占比 (%)",
    height=400,
)
st.plotly_chart(fig, use_container_width=True)

st.divider()
st.caption("""
🎯 **TPACK 成長對齊**：理想趨勢為「學生發話比」「開放題占比」「高階提問比」三線同步上升，
代表教師逐步從講述型走向探究型課堂風格。對應 Mishra & Koehler (2006) TPACK 框架中
TPK（科技教學知識）的反思精進歷程。
""")
