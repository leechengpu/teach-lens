"""上傳音檔 + 同意書 gate + 跑分析 pipeline"""

from __future__ import annotations
import tempfile
import streamlit as st
from pathlib import Path
from lib import db, transcribe
from lib.theme import inject_theme

st.set_page_config(page_title="上傳與分析｜TeachLens", page_icon="📤", layout="wide")
inject_theme()
st.title("📤 上傳微試教錄音")

CONSENT_TEXT = """
我同意以下事項：

1. 我已取得本錄音檔中所有發話者的明示同意
2. 本錄音為「**微試教 / 試教演練**」場景，**非真實學生課堂錄音**
3. 我了解 TeachLens 為自我反思工具，**不得用於教師評鑑或績效考核**
4. 我同意本系統將進行：
   - Whisper 自動轉錄
   - LLM 事件分段、提問分類、語意角色推論
   - 學生姓名自動匿名化（即使是試演中的虛構姓名）
5. 我了解音檔處理後 **30 天自動刪除原始檔**，僅保留去識別化逐字稿與分析結果
6. 我可隨時於「📊 診斷報告」頁面行使資料**永久刪除權**
7. 我了解 AI 分析結果僅供反思參考，**最終教學判讀由我本人負責**
"""

# === Step 1: 教師暱稱 ===
st.subheader("Step 1｜教師資訊（不存真實姓名）")
col1, col2 = st.columns(2)
with col1:
    nickname = st.text_input("自取暱稱", value="", placeholder="例如：阿政、Alex")
with col2:
    role = st.selectbox("身份", ["職前教師（師資生）", "在職教師", "輔導員", "其他"])

# === Step 2: 課堂資訊 ===
st.subheader("Step 2｜課堂資訊")
col1, col2 = st.columns(2)
with col1:
    title = st.text_input("課堂標題", placeholder="例如：四年級自然 水的三態 微試教")
    grade = st.selectbox("年級", ["", "一年級", "二年級", "三年級", "四年級", "五年級", "六年級", "其他"])
with col2:
    subject = st.selectbox("學科", ["", "國語", "英文", "數學", "自然", "社會", "其他"])
    topic = st.text_input("單元/主題", placeholder="例如：水的三態變化")

# === Step 3: 同意書 gate ===
st.subheader("Step 3｜資料使用同意書（必填）")
with st.expander("展開閱讀完整同意書", expanded=False):
    st.markdown(CONSENT_TEXT)

consent = st.checkbox("✅ 我已閱讀並同意上述全部條款", value=False)

# === Step 4: 上傳音檔 ===
st.subheader("Step 4｜上傳錄音檔")
uploaded = st.file_uploader(
    "選擇 mp3 / wav / m4a 檔（建議 3-8 分鐘）",
    type=["mp3", "wav", "m4a"],
    disabled=not consent,
    help="未勾選同意書無法上傳",
)

# === Step 5: 開始分析 ===
if uploaded and consent and nickname and title:
    st.divider()
    st.subheader("Step 5｜開始分析")
    st.audio(uploaded)

    if st.button("🚀 開始分析", type="primary"):
        # 暫存音檔
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded.name).suffix) as tmp:
            tmp.write(uploaded.getvalue())
            tmp_path = tmp.name

        # 估算時長（約略，未實際解析）
        audio_duration_estimate = uploaded.size / (16000 * 2)  # 假設 16k/16bit

        teacher_id = db.get_or_create_teacher(nickname, role)

        progress = st.progress(0, text="準備中...")

        def update(stage: str, pct: int):
            progress.progress(pct / 100, text=f"{stage} ({pct}%)")

        try:
            session_id = transcribe.run_pipeline(
                audio_file_path=tmp_path,
                teacher_id=teacher_id,
                title=title,
                grade=grade,
                subject=subject,
                topic=topic,
                consent_signed=True,
                consent_text=CONSENT_TEXT,
                audio_duration=audio_duration_estimate,
                progress_cb=update,
            )
            progress.empty()
            st.success(f"✅ 分析完成！session_id = {session_id}")
            st.balloons()
            st.markdown(f"👉 前往「📊 診斷報告」頁面查看結果（選擇 session #{session_id}）")
        except Exception as e:
            progress.empty()
            st.error(f"❌ 分析失敗：{e}")
            st.exception(e)
elif consent and uploaded and not (nickname and title):
    st.warning("請填妥教師暱稱與課堂標題後才能開始分析")
elif uploaded and not consent:
    st.error("請先勾選資料使用同意書")
