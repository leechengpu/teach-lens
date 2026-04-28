/* global React, TLNav, Icons, StatusCard, StepFlow, Callout, DIMENSIONS, Sparkline */
// Variant A — 保守、Linear 式留白
// Light theme, generous whitespace, restrained accents.

function HomeA({ tweaks }) {
  const t = tweaks || {};
  return (
    <div className="tl" data-theme={t.dark ? 'dark' : 'light'}
         data-density={t.density || 'regular'}
         style={{ '--tl-radius': (t.radius ?? 12) + 'px', minHeight: 1280, paddingBottom: 80 }}>
      <TLNav current="home" variant={t.dark ? 'dark' : 'light'}/>

      {/* hero */}
      <section style={{ maxWidth: 1180, margin: '0 auto', padding: '88px 36px 64px', textAlign: 'center' }}>
        <div style={{ display:'inline-flex', alignItems:'center', gap: 8, padding: '6px 14px',
          borderRadius: 999, background: 'var(--tl-surface)', border: '1px solid var(--tl-line)',
          color: 'var(--tl-ink-3)', fontSize: 12.5, marginBottom: 28,
          boxShadow: 'var(--tl-shadow-1)' }}>
          <span className="tl-dot tl-dot--ok"/>
          <span style={{ color:'var(--tl-ink-2)', fontWeight: 500 }}>2026 東華大學 AI 教育博覽會 · AI 系統開發組</span>
        </div>

        <h1 className="tl-display" style={{ marginBottom: 22 }}>
          看見課堂裡<br/>
          <span style={{
            background: 'linear-gradient(120deg, var(--tl-blue) 0%, var(--tl-plum) 90%)',
            WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent', backgroundClip: 'text',
          }}>每一句話的教學意圖</span>
        </h1>
        <p className="tl-lead" style={{ maxWidth: 720, margin: '0 auto 36px' }}>
          教學透鏡是一套以 AI 為輔助的課堂語言診斷系統，協助師資培育生與在職教師
          將一節課的錄音轉為可讀的五維診斷報告，並提供具學理依據的具體改進建議。
        </p>

        <div style={{ display:'flex', justifyContent:'center', gap: 12, marginBottom: 56 }}>
          <button className="tl-btn tl-btn--primary tl-btn--lg">
            開始分析一堂課 <Icons.ArrowRight size={16}/>
          </button>
          <button className="tl-btn tl-btn--ghost tl-btn--lg">
            查看範例報告
          </button>
        </div>

        {/* 4 句定位 */}
        <div style={{ display:'grid', gridTemplateColumns:'repeat(4, 1fr)', gap: 0,
          maxWidth: 1080, margin: '0 auto', textAlign: 'left',
          borderTop: '1px solid var(--tl-line)', borderBottom: '1px solid var(--tl-line)',
          background: 'var(--tl-surface)', borderRadius: 12, overflow: 'hidden',
          border: '1px solid var(--tl-line)' }}>
          {[
            { kbd: '01', t: '不取代教師判斷', d: '系統提供觀察指標，最終詮釋與行動由教師決定。' },
            { kbd: '02', t: '不評鑑教師個人', d: '焦點在「這節課的語言互動」，不對人作排名。' },
            { kbd: '03', t: '可被驗證的證據', d: '每項指標都對應到逐字稿時間戳，可追溯。' },
            { kbd: '04', t: '尊重學生隱私',  d: '學生姓名與聲紋特徵會在分析前去識別化。' },
          ].map((it, i) => (
            <div key={i} style={{
              padding: '24px 26px',
              borderRight: i < 3 ? '1px solid var(--tl-line)' : 'none',
            }}>
              <div className="tl-mono" style={{ fontSize: 12, color: 'var(--tl-blue)', fontWeight: 600, marginBottom: 10 }}>
                {it.kbd}
              </div>
              <div style={{ fontSize: 15, fontWeight: 600, color: 'var(--tl-ink)', marginBottom: 6 }}>{it.t}</div>
              <div style={{ fontSize: 13, color: 'var(--tl-ink-3)', lineHeight: 1.65 }}>{it.d}</div>
            </div>
          ))}
        </div>
      </section>

      {/* 系統狀態 3 卡 */}
      <section style={{ maxWidth: 1180, margin: '0 auto', padding: '0 36px 64px' }}>
        <div style={{ display:'flex', alignItems:'baseline', justifyContent:'space-between', marginBottom: 18 }}>
          <div>
            <div className="tl-micro" style={{ color: 'var(--tl-ink-4)', marginBottom: 4 }}>System Status</div>
            <h2 className="tl-h3" style={{ color: 'var(--tl-ink)' }}>系統即時狀態</h2>
          </div>
          <span style={{ fontSize: 12, color: 'var(--tl-ink-3)' }}>
            最後更新 2 分鐘前 · <a href="#" style={{ color:'var(--tl-blue)', textDecoration:'none' }}>狀態頁</a>
          </span>
        </div>
        <div style={{ display:'grid', gridTemplateColumns:'repeat(3, 1fr)', gap: 16 }}>
          <StatusCard icon={<Icons.Mic size={16} stroke={1.8}/>} label="轉錄引擎"
            value="98.2%" sub="Whisper large-v3 · 中文 · CER 1.8%"
            spark={[92,94,93,96,95,97,98]} status="ok" trend="0.4%" accent="blue"/>
          <StatusCard icon={<Icons.Brain size={16} stroke={1.8}/>} label="Claude API"
            value="412ms" sub="Sonnet 4.5 · 平均回應延遲"
            spark={[420,460,410,440,400,395,412]} status="ok" accent="blue"/>
          <StatusCard icon={<Icons.Bar size={16} stroke={1.8}/>} label="已分析課堂"
            value="2,847" sub="本週 +186 · 累計分析時長 1,290 hr"
            spark={[180,210,260,240,280,310,340]} status="ok" trend="14%" accent="plum"/>
        </div>
      </section>

      {/* 5 步驟流程 */}
      <section style={{ maxWidth: 1180, margin: '0 auto', padding: '24px 36px 72px' }}>
        <div style={{ marginBottom: 36 }}>
          <div className="tl-micro" style={{ color: 'var(--tl-ink-4)', marginBottom: 4 }}>How it works</div>
          <h2 className="tl-h2" style={{ color: 'var(--tl-ink)', marginBottom: 8 }}>從錄音到診斷，五個步驟</h2>
          <p className="tl-body" style={{ maxWidth: 640 }}>
            一節 40 分鐘的課，平均 6–8 分鐘完成全流程分析。所有中介資料在分析結束 24 小時後自動清除。
          </p>
        </div>
        <div className="tl-card" style={{ padding: '40px 32px' }}>
          <StepFlow active={1} steps={[
            { title: '上傳錄音',     desc: '支援 mp3 / m4a / wav，最長 60 分鐘' },
            { title: '自動轉錄',     desc: 'Whisper 多人語者分離 + 校對' },
            { title: '五維建模',     desc: 'Claude 依教學論框架建模' },
            { title: '生成報告',     desc: '可下載 PDF / 嵌入學習歷程' },
            { title: 'AI 教練回饋', desc: '證據—判讀—建議三段式' },
          ]}/>
        </div>
      </section>

      {/* 倫理 callout */}
      <section style={{ maxWidth: 1180, margin: '0 auto', padding: '0 36px 96px' }}>
        <Callout tone="blue" icon={<Icons.Shield size={22} stroke={1.8}/>}
          title="倫理範疇與系統邊界">
          教學透鏡的設計遵循「<strong>輔助而不取代</strong>」原則。系統<strong>不</strong>對教師進行評鑑、排名或績效判定，
          所有錄音僅用於本次分析、不會用於模型訓練；逐字稿與分析結果歸教師本人所有，
          可隨時下載或永久刪除。詳見&nbsp;
          <a href="#" style={{ color: 'var(--tl-blue)', fontWeight: 500, textDecoration:'underline', textUnderlineOffset: 3 }}>
            倫理與隱私政策
          </a>
          。
        </Callout>
      </section>
    </div>
  );
}
window.HomeA = HomeA;
