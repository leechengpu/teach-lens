"""五維指標診斷報告（Plotly 視覺化）"""

from __future__ import annotations
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from lib import db
from lib.theme import inject_theme

st.set_page_config(page_title="診斷報告｜TeachLens", page_icon="📊", layout="wide")
inject_theme()
st.title("📊 五維課堂語言診斷報告")

sessions = db.list_sessions()
if not sessions:
    st.info("尚無分析紀錄。請先到「📤 上傳與分析」上傳一段錄音。")
    st.stop()

# === Session 選擇 ===
options = {f"#{s['id']} {s['title'] or '未命名'} ({s['created_at'][:16]})": s["id"]
           for s in sessions}
choice = st.selectbox("選擇要查看的 session", list(options.keys()))
session_id = options[choice]

session = db.get_session(session_id)
metrics = db.get_metrics(session_id)
transcripts = db.get_transcripts(session_id)

if not metrics:
    st.warning(f"Session #{session_id} 尚未完成分析（status: {session['status']}）")
    st.stop()

# === Header ===
col1, col2, col3, col4 = st.columns(4)
col1.metric("年級", session["grade"] or "—")
col2.metric("學科", session["subject"] or "—")
col3.metric("時長（秒）", round(session["audio_duration"] or 0))
col4.metric("逐字稿句數", len(transcripts))

st.divider()

# === 1. Talk Time Ratio (Flanders) ===
st.subheader("🗣️ 維度 1｜師生發話比")
st.caption("學理依據：Flanders (1970) Interaction Analysis Categories")

teacher = metrics["teacher_talk_sec"] or 0
student = metrics["student_talk_sec"] or 0
transition = metrics["transition_sec"] or 0
total = teacher + student + transition or 1

col1, col2 = st.columns([2, 1])
with col1:
    fig = go.Figure(data=[go.Pie(
        labels=["教師發話", "學生發話", "過渡"],
        values=[teacher, student, transition],
        hole=0.4,
        marker_colors=["#2E86AB", "#A23B72", "#F18F01"],
    )])
    fig.update_layout(height=300, margin=dict(t=10, b=10, l=10, r=10))
    st.plotly_chart(fig, use_container_width=True)
with col2:
    st.metric("教師發話比", f"{teacher / total * 100:.1f}%")
    st.metric("學生發話比", f"{student / total * 100:.1f}%")
    if teacher / total > 0.7:
        st.warning("⚠️ 教師發話 > 70%（Flanders 講述型課堂）")
    elif teacher / total < 0.5:
        st.success("✅ 學生中心傾向課堂")

st.divider()

# === 2. Question Types ===
st.subheader("❓ 維度 2｜提問類型")
st.caption("學理依據：Wragg & Brown (2001) Questioning in the Primary School")

closed = metrics["closed_q_count"]
open_q = metrics["open_q_count"]
followup = metrics["followup_q_count"]

col1, col2, col3 = st.columns(3)
col1.metric("封閉題", closed)
col2.metric("開放題", open_q)
col3.metric("追問", followup)

if closed + open_q + followup > 0:
    df = pd.DataFrame({
        "類型": ["封閉題", "開放題", "追問"],
        "次數": [closed, open_q, followup],
    })
    fig = px.bar(df, x="類型", y="次數", color="類型",
                 color_discrete_sequence=["#E63946", "#2A9D8F", "#F4A261"])
    fig.update_layout(height=250, showlegend=False, margin=dict(t=10, b=10))
    st.plotly_chart(fig, use_container_width=True)

st.divider()

# === 3. Wait Time (Rowe) ===
st.subheader("⏱️ 維度 3｜等待時間")
st.caption("學理依據：Rowe (1972, 1986) Wait Time I & II — 提問後 < 1 秒會限制學生思考深度")

col1, col2, col3 = st.columns(3)
col1.metric("平均等待（秒）", f"{metrics['wait_time_avg']:.2f}")
col2.metric("中位數（秒）", f"{metrics['wait_time_median']:.2f}")
col3.metric("< 1 秒次數", metrics["wait_time_under_1s"])

if metrics["wait_time_avg"] < 1.0 and (closed + open_q + followup) > 0:
    st.error("🚨 平均等待 < 1 秒，落入 Rowe 警示區")
elif metrics["wait_time_avg"] >= 3.0:
    st.success("✅ 等待時間 ≥ 3 秒，符合 Rowe 建議")

st.divider()

# === 4. Bloom Distribution ===
st.subheader("🧠 維度 4｜Bloom 認知層級")
st.caption("學理依據：Anderson & Krathwohl (2001) 修訂版 Bloom 認知分類學")

bloom_data = pd.DataFrame({
    "層級": ["L1 記憶", "L2 理解", "L3 應用", "L4 分析", "L5 評鑑", "L6 創造"],
    "次數": [
        metrics["bloom_l1_remember"], metrics["bloom_l2_understand"],
        metrics["bloom_l3_apply"], metrics["bloom_l4_analyze"],
        metrics["bloom_l5_evaluate"], metrics["bloom_l6_create"],
    ],
    "類別": ["低階", "低階", "中階", "中階", "高階", "高階"],
})
fig = px.bar(bloom_data, x="層級", y="次數", color="類別",
             color_discrete_map={"低階": "#E63946", "中階": "#F4A261", "高階": "#2A9D8F"})
fig.update_layout(height=300, margin=dict(t=10, b=10))
st.plotly_chart(fig, use_container_width=True)

low = bloom_data["次數"][:2].sum()
high = bloom_data["次數"][4:].sum()
total_q = bloom_data["次數"].sum()
if total_q > 0 and high / total_q < 0.2:
    st.warning(f"⚠️ 高階提問僅 {high}/{total_q}（< 20%），建議增加分析/評鑑/創造類提問")

st.divider()

# === 5. Dialogue Pattern ===
st.subheader("💬 維度 5｜對話結構")
st.caption("學理依據：Mehan (1979) IRE Sequence、Wells (1999) Dialogic Inquiry")

col1, col2, col3 = st.columns(3)
col1.metric("IRE（教師主導終結）", metrics["pattern_ire_count"])
col2.metric("IRF（教師追問）", metrics["pattern_irf_count"])
col3.metric("Dialogic（學生接續）", metrics["pattern_dialogic"])

st.divider()

# === 逐字稿檢視 ===
with st.expander("📜 完整逐字稿（已匿名化）", expanded=False):
    df_t = pd.DataFrame(transcripts)[
        ["segment_idx", "start_sec", "end_sec", "role", "event_type", "text", "bloom_level"]
    ]
    st.dataframe(df_t, use_container_width=True, hide_index=True)

# === 資料管理 ===
st.divider()
st.subheader("🔒 此筆資料管理")
col1, col2 = st.columns(2)
with col1:
    if st.button("⚠️ 永久刪除這筆資料", type="secondary"):
        db.hard_delete_session(session_id)
        st.success("已刪除。請重新整理頁面。")
        st.stop()
with col2:
    st.caption("行使資料刪除權；連同音檔元資料、逐字稿、分析結果、AI 回饋全部清除")

# === AI 限制提醒（固定） ===
st.divider()
st.caption("""
⚠ **AI 提醒**：本標註結果由 LLM 推論產生，僅供反思參考。
最終教學判讀應由教師本人或專業觀課者確認。本工具不得用於教師評鑑或績效考核。
""")
