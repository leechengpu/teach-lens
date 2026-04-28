"""AI 教練三段式回饋｜證據—判讀—建議"""

from __future__ import annotations
import streamlit as st
from lib import db
from lib.theme import inject_theme

st.set_page_config(page_title="AI 教練回饋｜TeachLens", page_icon="🎓", layout="wide")
inject_theme()
st.title("🎓 AI 教練「證據—判讀—建議」三段式回饋")

sessions = db.list_sessions()
if not sessions:
    st.info("尚無分析紀錄。")
    st.stop()

options = {f"#{s['id']} {s['title'] or '未命名'} ({s['created_at'][:16]})": s["id"]
           for s in sessions}
choice = st.selectbox("選擇 session", list(options.keys()))
session_id = options[choice]

feedbacks = db.get_feedbacks(session_id)

if not feedbacks:
    st.warning("此 session 尚無回饋。請確認分析已完成。")
    st.stop()

DIM_LABELS = {
    "talk_ratio": "🗣️ 師生發話比",
    "question_types": "❓ 提問類型",
    "wait_time": "⏱️ 等待時間",
    "bloom": "🧠 Bloom 認知層級",
    "dialogue_pattern": "💬 對話結構",
    "general": "📋 整體觀察",
}

for fb in feedbacks:
    label = DIM_LABELS.get(fb["dimension"], fb["dimension"])
    st.subheader(label)

    with st.container():
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**🔍 證據（Evidence）**")
            st.info(fb["evidence"])
        with col2:
            st.markdown("**🧭 判讀（Interpretation）**")
            st.markdown(fb["interpretation"])
        with col3:
            st.markdown("**💡 建議（Suggestion）**")
            st.success(fb["suggestion"])

    if fb["citation"]:
        st.caption(f"📖 引用：{fb['citation']}")

    st.divider()

# === AI 限制提醒（固定） ===
st.warning("""
⚠ **AI 提醒**：本標註結果由 LLM 推論產生，僅供反思參考。
最終教學判讀應由教師本人或專業觀課者確認。本工具不得用於教師評鑑或績效考核。
""")

# === 反思問卷（試用驗證資料蒐集） ===
st.divider()
st.subheader("📝 反思問卷（試用回饋，可選）")
st.caption("協助我們蒐集試用驗證資料；填寫採匿名化處理")

with st.form("survey", clear_on_submit=True):
    role = st.selectbox("您的身份", ["職前教師（師資生）", "在職教師", "輔導員", "其他"])
    q1 = st.slider("1. 本工具對我的反思有幫助", 1, 5, 3)
    q2 = st.slider("2. 分析結果與我的自我感受一致", 1, 5, 3)
    q3 = st.slider("3. 建議具體可實踐", 1, 5, 3)
    q4 = st.slider("4. 我願意持續使用", 1, 5, 3)
    q5 = st.slider("5. 我會推薦給同事", 1, 5, 3)
    open_fb = st.text_area("開放回饋（可選）")

    if st.form_submit_button("提交"):
        from lib.db import get_conn
        with get_conn() as conn:
            conn.execute(
                """
                INSERT INTO feedback_surveys (
                    session_id, teacher_role,
                    q1_usefulness, q2_accuracy, q3_actionable, q4_willingness, q5_recommend,
                    open_feedback
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (session_id, role, q1, q2, q3, q4, q5, open_fb),
            )
        st.success("✅ 已收到您的回饋，謝謝！")
