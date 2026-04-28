/* global React, TLNav, Icons, StatusCard, StepFlow, Callout, Sparkline */
// Variant B — 大膽、深色 hero、幾何裝飾
// Dark hero band, abstract decoration, body switches to light.

function HomeB({ tweaks }) {
  const t = tweaks || {};
  const radius = (t.radius ?? 12) + 'px';
  return (
    <div className="tl" data-theme={t.dark ? 'dark' : 'light'}
         data-density={t.density || 'regular'}
         style={{ '--tl-radius': radius, minHeight: 1320, paddingBottom: 80 }}>
      <div style={{ background: '#0d1117', color: '#f4f3ef' }}>
        <TLNav current="home" variant="dark"/>

        {/* hero with geometric decoration */}
        <section style={{ position:'relative', overflow:'hidden' }}>
          <DecorBg/>
          <div style={{ position:'relative', maxWidth: 1180, margin: '0 auto', padding: '96px 36px 120px', display:'grid', gridTemplateColumns:'1.1fr .9fr', gap: 56, alignItems:'center' }}>
            <div>
              <div style={{ display:'inline-flex', alignItems:'center', gap: 10, padding: '6px 14px',
                borderRadius: 999, background: 'rgba(255,255,255,.06)', border: '1px solid rgba(255,255,255,.12)',
                fontSize: 12.5, marginBottom: 28, color: 'rgba(255,255,255,.85)' }}>
                <span style={{ width: 6, height: 6, borderRadius: '50%', background: '#7ee3a8',
                  boxShadow: '0 0 0 3px rgba(126,227,168,.18)' }}/>
                <span>2026 東華大學 AI 教育博覽會</span>
                <span style={{ color: 'rgba(255,255,255,.4)' }}>·</span>
                <span style={{ color: 'rgba(255,255,255,.55)' }}>AI 系統開發組</span>
              </div>

              <h1 style={{ fontSize: 60, fontWeight: 600, lineHeight: 1.08, letterSpacing: '-0.025em', marginBottom: 24 }}>
                把一節課<br/>
                變成<span style={{
                  background: 'linear-gradient(110deg, #5fb6dc 0%, #c468a0 50%, #f4a261 100%)',
                  WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent', backgroundClip: 'text',
                }}>可閱讀的證據</span>
              </h1>
              <p style={{ fontSize: 18, lineHeight: 1.7, color: 'rgba(255,255,255,.72)', marginBottom: 36, maxWidth: 540 }}>
                教學透鏡用 AI 把課堂錄音轉成五個維度的語言診斷，
                陪你看見自己沒注意到的提問習慣、回饋語氣與節奏。
              </p>
              <div style={{ display:'flex', gap: 12, marginBottom: 48 }}>
                <button className="tl-btn tl-btn--primary tl-btn--lg">
                  開始分析一堂課 <Icons.ArrowRight size={16}/>
                </button>
                <button className="tl-btn tl-btn--lg" style={{
                  background: 'rgba(255,255,255,.06)', color: '#fff',
                  border: '1px solid rgba(255,255,255,.16)' }}>
                  查看範例報告
                </button>
              </div>

              {/* 4 句定位 — inline as bullets */}
              <ul style={{ listStyle:'none', padding: 0, margin: 0, display:'grid', gridTemplateColumns:'1fr 1fr', gap: '14px 28px', maxWidth: 540 }}>
                {[
                  '不取代教師判斷',
                  '不評鑑教師個人',
                  '每項指標可被驗證',
                  '學生資料去識別化',
                ].map((s,i) => (
                  <li key={i} style={{ display:'flex', alignItems:'center', gap: 10, fontSize: 14, color: 'rgba(255,255,255,.85)' }}>
                    <span style={{
                      width: 22, height: 22, borderRadius: 6,
                      background: 'rgba(95,182,220,.15)',
                      color: '#7ec3df',
                      display:'inline-flex', alignItems:'center', justifyContent:'center',
                    }}>
                      <Icons.Check size={13} stroke={2.4}/>
                    </span>
                    {s}
                  </li>
                ))}
              </ul>
            </div>

            {/* hero visual: 5-dimension mini diagnostic preview */}
            <HeroPreview/>
          </div>
        </section>
      </div>

      {/* light body — system status */}
      <section style={{ maxWidth: 1180, margin: '0 auto', padding: '64px 36px 24px' }}>
        <div style={{ display:'flex', alignItems:'baseline', justifyContent:'space-between', marginBottom: 20 }}>
          <div>
            <div className="tl-micro" style={{ color: 'var(--tl-ink-4)', marginBottom: 4 }}>System Status · 即時</div>
            <h2 className="tl-h2" style={{ color: 'var(--tl-ink)' }}>三個服務，一齊運轉</h2>
          </div>
          <span className="tl-chip tl-chip--ok"><span className="tl-dot tl-dot--ok"/>全部正常</span>
        </div>
        <div style={{ display:'grid', gridTemplateColumns:'repeat(3, 1fr)', gap: 18 }}>
          <StatusCard icon={<Icons.Mic size={16} stroke={1.8}/>} label="轉錄引擎"
            value="98.2%" sub="Whisper large-v3 · CER 1.8%"
            spark={[92,94,93,96,95,97,98]} status="ok" trend="0.4%" accent="blue"/>
          <StatusCard icon={<Icons.Brain size={16} stroke={1.8}/>} label="Claude API"
            value="412ms" sub="Sonnet 4.5 · 平均回應延遲"
            spark={[420,460,410,440,400,395,412]} status="ok" accent="blue"/>
          <StatusCard icon={<Icons.Bar size={16} stroke={1.8}/>} label="已分析課堂"
            value="2,847" sub="本週 +186 · 累計 1,290 hr"
            spark={[180,210,260,240,280,310,340]} status="ok" trend="14%" accent="plum"/>
        </div>
      </section>

      {/* steps */}
      <section style={{ maxWidth: 1180, margin: '0 auto', padding: '56px 36px 72px' }}>
        <div style={{ marginBottom: 36, maxWidth: 720 }}>
          <div className="tl-micro" style={{ color: 'var(--tl-plum)', marginBottom: 8 }}>How it works</div>
          <h2 className="tl-h2" style={{ color: 'var(--tl-ink)', marginBottom: 10 }}>從錄音到診斷，只需五個步驟</h2>
          <p className="tl-body">
            一節 40 分鐘的課，平均 6–8 分鐘完成全流程分析。所有中介資料在分析結束 24 小時後自動清除。
          </p>
        </div>
        <div className="tl-card" style={{ padding: '44px 32px',
          background: 'linear-gradient(180deg, var(--tl-surface) 0%, var(--tl-surface-2) 200%)' }}>
          <StepFlow active={1} steps={[
            { title: '上傳錄音',     desc: '支援 mp3 / m4a / wav，最長 60 分鐘' },
            { title: '自動轉錄',     desc: 'Whisper 多人語者分離 + 校對' },
            { title: '五維建模',     desc: 'Claude 依教學論框架建模' },
            { title: '生成報告',     desc: '可下載 PDF / 嵌入學習歷程' },
            { title: 'AI 教練回饋', desc: '證據—判讀—建議三段式' },
          ]}/>
        </div>
      </section>

      {/* ethics callout */}
      <section style={{ maxWidth: 1180, margin: '0 auto', padding: '0 36px 96px' }}>
        <div style={{ display:'grid', gridTemplateColumns: '1.1fr .9fr', gap: 18 }}>
          <Callout tone="blue" icon={<Icons.Shield size={22} stroke={1.8}/>}
            title="輔助而不取代：教學透鏡的倫理範疇">
            系統<strong>不</strong>對教師進行評鑑、排名或績效判定。所有錄音僅用於本次分析，
            不會用於模型訓練。逐字稿與報告歸教師本人所有，可隨時下載或永久刪除。
          </Callout>
          <Callout tone="plum" icon={<Icons.Lock size={22} stroke={1.8}/>}
            title="學生隱私的處理方式">
            學生姓名與聲紋特徵會在分析前自動去識別化；逐字稿僅保留發言角色（T / S1 / S2…）。
            分析結束 24 小時後，所有中介音檔自動清除。
          </Callout>
        </div>
      </section>
    </div>
  );
}

function DecorBg() {
  return (
    <svg style={{ position:'absolute', inset: 0, width:'100%', height:'100%', pointerEvents:'none' }}
         preserveAspectRatio="xMidYMid slice" viewBox="0 0 1200 700">
      <defs>
        <radialGradient id="g1" cx="20%" cy="30%" r="60%">
          <stop offset="0%" stopColor="#2E86AB" stopOpacity="0.32"/>
          <stop offset="100%" stopColor="#2E86AB" stopOpacity="0"/>
        </radialGradient>
        <radialGradient id="g2" cx="85%" cy="60%" r="50%">
          <stop offset="0%" stopColor="#A23B72" stopOpacity="0.28"/>
          <stop offset="100%" stopColor="#A23B72" stopOpacity="0"/>
        </radialGradient>
        <pattern id="grid" width="48" height="48" patternUnits="userSpaceOnUse">
          <path d="M48 0H0V48" fill="none" stroke="rgba(255,255,255,.04)" strokeWidth="1"/>
        </pattern>
      </defs>
      <rect width="1200" height="700" fill="url(#grid)"/>
      <rect width="1200" height="700" fill="url(#g1)"/>
      <rect width="1200" height="700" fill="url(#g2)"/>
      {/* abstract concentric rings */}
      <g transform="translate(960 380)" fill="none" stroke="rgba(255,255,255,.06)">
        <circle r="60"/><circle r="120"/><circle r="200"/><circle r="290"/>
      </g>
      {/* dots */}
      {[[200,120],[1080,160],[140,560],[1140,600],[640,80],[260,640]].map(([x,y],i)=>(
        <circle key={i} cx={x} cy={y} r="2" fill="rgba(255,255,255,.25)"/>
      ))}
    </svg>
  );
}

function HeroPreview() {
  return (
    <div style={{ position:'relative' }}>
      {/* tilted card */}
      <div style={{
        background: '#fafaf7', color: '#1c1b18', borderRadius: 16,
        padding: 22, boxShadow: '0 30px 80px -20px rgba(0,0,0,.6), 0 1px 0 rgba(255,255,255,.1) inset',
        border: '1px solid rgba(255,255,255,.08)',
        transform: 'perspective(1200px) rotateY(-8deg) rotateX(3deg)',
        transformStyle: 'preserve-3d',
      }}>
        <div style={{ display:'flex', alignItems:'center', justifyContent:'space-between', marginBottom: 14 }}>
          <div>
            <div style={{ fontSize: 11, color: '#9b9890', textTransform:'uppercase', letterSpacing: '.06em', fontWeight: 600 }}>Diagnostic Report</div>
            <div style={{ fontSize: 14, fontWeight: 600, marginTop: 2 }}>五年級 · 自然 · 浮力與密度</div>
          </div>
          <span className="tl-chip tl-chip--ok" style={{ height: 22, fontSize: 11 }}>已完成</span>
        </div>

        {/* radar-like 5 dim bars */}
        <div style={{ display:'flex', flexDirection:'column', gap: 10, marginBottom: 14 }}>
          {[
            { l: '提問品質',     v: 0.78, c: '#2E86AB' },
            { l: '回饋語言',     v: 0.62, c: '#5e9ec1' },
            { l: '教學節奏',     v: 0.84, c: '#8e6fa7' },
            { l: '學生發言佔比', v: 0.41, c: '#A23B72', warn: true },
            { l: '學科語言',     v: 0.71, c: '#c25e8b' },
          ].map((b,i)=>(
            <div key={i}>
              <div style={{ display:'flex', justifyContent:'space-between', fontSize: 12, marginBottom: 5 }}>
                <span style={{ color: '#3a3833', fontWeight: 500 }}>{b.l}</span>
                <span className="tl-mono" style={{ color: b.warn ? '#E63946' : '#6b6862', fontWeight: 600 }}>
                  {(b.v*100).toFixed(0)}{b.warn && ' ⚠'}
                </span>
              </div>
              <div style={{ height: 6, background: '#e8e6df', borderRadius: 999, overflow:'hidden' }}>
                <div style={{ width: `${b.v*100}%`, height: '100%',
                  background: b.warn ? 'linear-gradient(90deg,#E63946,#f06b76)' : `linear-gradient(90deg, ${b.c}, ${b.c}cc)`,
                  borderRadius: 999, transition: 'width .6s' }}/>
              </div>
            </div>
          ))}
        </div>

        <div style={{ padding: '12px 14px', background: '#fdecee', border: '1px solid #f4b8be',
          borderRadius: 10, fontSize: 12.5, color: '#7a1a25', display:'flex', gap: 8, alignItems:'flex-start' }}>
          <Icons.Alert size={14} stroke={2}/>
          <div>
            <strong>發現 1 項警示：</strong>學生發言佔比偏低（41%）。AI 教練已生成具體建議。
          </div>
        </div>
      </div>

      {/* floating chip */}
      <div style={{
        position:'absolute', top: -16, right: -16,
        background: '#0d1117', color: '#fff',
        border: '1px solid rgba(255,255,255,.14)',
        borderRadius: 12, padding: '12px 14px',
        boxShadow: '0 16px 36px -8px rgba(0,0,0,.6)',
        display:'flex', alignItems:'center', gap: 10,
      }}>
        <Icons.Sparkles size={16} stroke={1.8} style={{ color: '#f4a261' }}/>
        <div>
          <div style={{ fontSize: 11, color: 'rgba(255,255,255,.55)', fontWeight: 500 }}>AI 教練建議</div>
          <div style={{ fontSize: 12.5, fontWeight: 500, marginTop: 1 }}>「給學生 3 秒等候時間」</div>
        </div>
      </div>
    </div>
  );
}

window.HomeB = HomeB;
