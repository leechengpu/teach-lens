"""倫理機制說明 + 全資料管理"""

from __future__ import annotations
import streamlit as st
from lib import db
from lib.theme import inject_theme

st.set_page_config(page_title="倫理與隱私｜TeachLens", page_icon="🔒", layout="wide")
inject_theme()
st.title("🔒 倫理機制與隱私保護")

st.subheader("📋 六條可驗證設計")
st.markdown("""
| # | 倫理原則 | 系統實作機制 |
|---|----------|--------------|
| 1 | 錄音前告知與同意 | 上傳介面強制勾選同意書，未勾選不可上傳；同意書全文留存於 DB（法律證據） |
| 2 | 學生資料去識別化 | 逐字稿生成時 `lib/anonymize.py` 自動將人名替換為 S1/S2/S3，教師為 T |
| 3 | 資料刪除權 | 「📊 診斷報告」頁附「永久刪除」按鈕；CASCADE 刪除音檔元資料/逐字稿/指標/回饋 |
| 4 | 用途限定 | 首頁明示「僅供職前教師自我反思，不得用於教師評鑑或績效考核」 |
| 5 | AI 限制提醒 | 每份報告底部固定附註「AI 結果僅供參考，最終判讀由教師確認」 |
| 6 | 著作權與資料保存 | 音檔處理後 30 天自動刪除原始檔；明示**不用於模型訓練** |
""")

st.divider()

st.subheader("🚧 MVP 範疇限定")
st.warning("""
本系統 MVP 階段**僅開放「微試教 / 試教演練」場景**，禁止上傳真實學生課堂錄音。

**為什麼？** 真實課堂錄音含學生聲音資料，須額外取得：
- 家長集體同意書
- 學校研究倫理審查
- 必要時走 IRB 流程

這些是下階段擴充功能；MVP 不做不對應的事，是有意識的工程決策。
""")

st.divider()

st.subheader("🗑️ 全部我的資料管理")
st.caption("行使資料控制權")

sessions = db.list_sessions()
if not sessions:
    st.info("目前無任何資料。")
else:
    st.write(f"共 {len(sessions)} 筆資料：")
    for s in sessions:
        col1, col2, col3, col4 = st.columns([1, 4, 2, 1])
        col1.write(f"#{s['id']}")
        col2.write(s["title"] or "未命名")
        col3.caption(s["created_at"][:16])
        if col4.button("刪除", key=f"del_{s['id']}", type="secondary"):
            db.hard_delete_session(s["id"])
            st.rerun()

st.divider()

st.subheader("📖 對應評審「設計正確規範」評分標準（25%）")
st.markdown("""
本系統倫理機制設計直接對應：
- **UNESCO AI Competency Framework for Teachers (AI CFT, 2024)** 第 1 條（以人為本）+ 第 5 條（倫理透明）
- **教育部資安規範**：學生個資保護
- **GDPR 個人資料保護**：刪除權、用途限定原則
- **學術研究倫理**：知情同意、最小化資料蒐集
""")
