"""TeachLens｜教學透鏡｜首頁（基於 Claude Design HomeB 變體）"""

from __future__ import annotations
import streamlit as st
from lib import db, claude, transcribe_engine
from lib.theme import inject_theme, render_callout, ICON_SHIELD, ICON_LOCK

st.set_page_config(
    page_title="教學透鏡 TeachLens",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

db.ensure_db_initialized()
inject_theme()

sessions_count = len(db.list_sessions())
engine_label = transcribe_engine.get_engine_label()
claude_status = "已連接" if claude.is_api_available() else "Demo 模式"

# === 1. 深色 Hero ===
# 注意：所有 HTML 都 left-justify（不可縮排），否則 Streamlit 會當 code block

bars = []
for label, v, color, warn in [
    ("師生發話比", 0.74, "#2E86AB", False),
    ("提問類型", 0.62, "#5e9ec1", False),
    ("等待時間", 0.41, "#A23B72", True),
    ("Bloom 認知層級", 0.71, "#8e6fa7", False),
    ("對話結構", 0.55, "#c25e8b", False),
]:
    warn_cls = " warn" if warn else ""
    warn_mark = " ⚠" if warn else ""
    fill_style = (
        f"width:{v*100}%"
        if warn
        else f"width:{v*100}%; background:linear-gradient(90deg, {color}, {color}cc)"
    )
    bars.append(
        f'<div class="tl-bar-row">'
        f'<div class="tl-bar-label">'
        f'<span style="color:#3a3833; font-weight:500">{label}</span>'
        f'<span class="tl-bar-value{warn_cls}">{int(v*100)}{warn_mark}</span>'
        f'</div>'
        f'<div class="tl-bar-track">'
        f'<div class="tl-bar-fill{warn_cls}" style="{fill_style}"></div>'
        f'</div>'
        f'</div>'
    )
bars_html = "".join(bars)

hero_html = (
    '<div class="tl-hero">'
    '<div class="tl-hero-decor"></div>'
    '<div class="tl-hero-inner">'
    '<div>'
    '<div class="tl-badge">'
    '<span class="tl-badge-dot"></span>'
    '<span>2026 東華大學 AI 教育博覽會</span>'
    '<span style="color: rgba(255,255,255,.4)">·</span>'
    '<span style="color: rgba(255,255,255,.55)">AI 系統開發組</span>'
    '</div>'
    '<h1>把一節課<br>變成<span class="tl-grad">可閱讀的證據</span></h1>'
    '<p class="tl-hero-lead">教學透鏡用 AI 把課堂錄音轉成五個維度的語言診斷，'
    '陪你看見自己沒注意到的提問習慣、回饋語氣與節奏。</p>'
    '<div class="tl-cta-row">'
    '<a href="?page=上傳與分析" class="tl-cta-primary" target="_self">'
    '開始分析一堂課 '
    '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
    '</a>'
    '<a href="?page=診斷報告" class="tl-cta-ghost" target="_self">查看範例報告</a>'
    '</div>'
    '<ul class="tl-bullets">'
    '<li><span class="tl-bullets-check">✓</span>不取代教師判斷</li>'
    '<li><span class="tl-bullets-check">✓</span>不評鑑教師個人</li>'
    '<li><span class="tl-bullets-check">✓</span>每項指標可被驗證</li>'
    '<li><span class="tl-bullets-check">✓</span>學生資料去識別化</li>'
    '</ul>'
    '</div>'
    '<div class="tl-hero-preview">'
    '<div class="tl-hero-floating">'
    '<span style="color:#f4a261">✦</span>'
    '<div>'
    '<div class="tl-hero-floating-label">AI 教練建議</div>'
    '<div class="tl-hero-floating-text">「給學生 3 秒等候時間」</div>'
    '</div>'
    '</div>'
    '<div class="tl-hero-preview-card">'
    '<div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:14px">'
    '<div>'
    '<div style="font-size:11px; color:#9b9890; text-transform:uppercase; letter-spacing:.06em; font-weight:600">Diagnostic Report</div>'
    '<div style="font-size:14px; font-weight:600; margin-top:2px">五年級 · 自然 · 浮力與密度</div>'
    '</div>'
    '<span class="tl-chip tl-chip--ok"><span class="tl-dot tl-dot--ok"></span>已完成</span>'
    '</div>'
    f'<div style="display:flex; flex-direction:column; gap:10px; margin-bottom:14px">{bars_html}</div>'
    '<div style="padding:12px 14px; background:#fdecee; border:1px solid #f4b8be; border-radius:10px; font-size:12.5px; color:#7a1a25">'
    '<strong>發現 1 項警示：</strong>等待時間平均 0.8 秒（&lt; Rowe 1986 建議的 3 秒）。AI 教練已生成具體建議。'
    '</div>'
    '</div>'
    '</div>'
    '</div>'
    '</div>'
)
st.markdown(hero_html, unsafe_allow_html=True)

# === 2. System Status ===
st.markdown(
    '<div style="margin-top:64px; display:flex; align-items:baseline; justify-content:space-between; margin-bottom:20px">'
    '<div>'
    '<div class="tl-section-eyebrow">System Status · 即時</div>'
    '<h2 style="margin:0">三個服務，一齊運轉</h2>'
    '</div>'
    '<span class="tl-chip tl-chip--ok"><span class="tl-dot tl-dot--ok"></span>全部正常</span>'
    '</div>',
    unsafe_allow_html=True,
)

col1, col2, col3 = st.columns(3, gap="medium")
engine_short = engine_label.split("（")[0].replace("🚀 ", "").replace("☁️ ", "").replace("ℹ️ ", "").strip()
with col1:
    st.metric(label="🎙️ 轉錄引擎", value=engine_short, delta="自動偵測引擎", delta_color="off")
with col2:
    st.metric(label="🧠 Claude API", value=claude_status, delta="Sonnet 4.6 + Opus 4.7", delta_color="off")
with col3:
    st.metric(label="📊 已分析課堂", value=f"{sessions_count}", delta="累計 session", delta_color="off")

# === 3. 5 步驟流程 ===
st.markdown(
    '<div style="margin-top:56px">'
    '<div class="tl-section-eyebrow" style="color:var(--tl-plum)">How it works</div>'
    '<h2 style="margin:0 0 10px">從錄音到診斷，只需五個步驟</h2>'
    '<p class="tl-hero-lead" style="color:var(--tl-ink-2); max-width:720px">'
    '一節 40 分鐘的微試教，平均 6–8 分鐘完成全流程分析。所有中介資料在分析結束 24 小時後自動清除。'
    '</p>'
    '</div>',
    unsafe_allow_html=True,
)

steps = [
    ("1", "上傳錄音", "支援 mp3 / m4a / wav，建議 3-8 分鐘", "is-current"),
    ("2", "自動轉錄", "Whisper（mlx 或 OpenAI API）+ 句級時間戳", ""),
    ("3", "五維建模", "Flanders / Rowe / Bloom 學理框架", ""),
    ("4", "生成報告", "Plotly 互動視覺化 + 證據追溯", ""),
    ("5", "AI 教練回饋", "證據—判讀—建議三段式", ""),
]
steps_html = "".join(
    f'<div class="tl-step">'
    f'<div class="tl-step-dot {state}">{n}</div>'
    f'<div class="tl-step-title">{title}</div>'
    f'<div class="tl-step-desc">{desc}</div>'
    f'</div>'
    for n, title, desc, state in steps
)
st.markdown(
    f'<div class="tl-step-flow" style="margin-top:24px">'
    f'<div class="tl-steps">{steps_html}</div>'
    f'</div>',
    unsafe_allow_html=True,
)

# === 4. 倫理 Callout 雙列 ===
st.markdown('<div style="margin-top:32px"></div>', unsafe_allow_html=True)
ec1, ec2 = st.columns([1.1, 0.9], gap="medium")
with ec1:
    render_callout(
        tone="blue",
        icon_svg=ICON_SHIELD,
        title="輔助而不取代：教學透鏡的倫理範疇",
        body_html="系統<strong>不</strong>對教師進行評鑑、排名或績效判定。所有錄音僅用於本次分析，不會用於模型訓練。逐字稿與報告歸教師本人所有，可隨時下載或永久刪除。",
    )
with ec2:
    render_callout(
        tone="plum",
        icon_svg=ICON_LOCK,
        title="學生隱私的處理方式",
        body_html="學生姓名與聲紋特徵會在分析前自動去識別化；逐字稿僅保留發言角色（T / S1 / S2…）。分析結束 24 小時後，所有中介音檔自動清除。",
    )

# === 5. Footer ===
st.markdown(
    '<div style="margin-top:80px; padding-top:32px; border-top:1px solid var(--tl-line); color:var(--tl-ink-3); font-size:13px">'
    '<strong>作者</strong>：李政蒲｜東華大學科學教育研究所博士生｜114 學年度花蓮縣候用校長｜花蓮縣國教輔導團數學領域輔導員<br>'
    '<strong>指導教授</strong>：蔡仁哲 助理教授<br>'
    '<strong>承辦窗口</strong>：陳世文 教授（東華師培中心副主任）'
    '</div>',
    unsafe_allow_html=True,
)
