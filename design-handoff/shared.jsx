/* global React */
// Shared TeachLens UI primitives — icons, nav, sparkline, etc.
// Loaded via <script type="text/babel" src="components/shared.jsx"></script>
// Exports to window so other Babel scripts can use them.

// ── icons (stroke = currentColor) ─────────────────────────────
const Icon = ({ d, size = 18, stroke = 1.6, fill = 'none', children, style }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill={fill} stroke="currentColor"
       strokeWidth={stroke} strokeLinecap="round" strokeLinejoin="round" style={{ flexShrink: 0, ...style }}>
    {d ? <path d={d} /> : children}
  </svg>
);

const Icons = {
  Lens: (p) => (
    <Icon {...p}><circle cx="11" cy="11" r="6.5"/><path d="m20 20-4.2-4.2"/><circle cx="11" cy="11" r="2.2"/></Icon>
  ),
  Mic:  (p) => <Icon {...p}><rect x="9" y="3" width="6" height="12" rx="3"/><path d="M5 11a7 7 0 0 0 14 0M12 18v3"/></Icon>,
  Spark:(p) => <Icon {...p}><path d="M12 3v3M12 18v3M3 12h3M18 12h3M5.6 5.6l2.1 2.1M16.3 16.3l2.1 2.1M5.6 18.4l2.1-2.1M16.3 7.7l2.1-2.1"/></Icon>,
  Bar:  (p) => <Icon {...p}><path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/></Icon>,
  Shield:(p)=> <Icon {...p}><path d="M12 3 4 6v6c0 5 3.5 8 8 9 4.5-1 8-4 8-9V6l-8-3Z"/><path d="m9 12 2 2 4-4"/></Icon>,
  Check:(p) => <Icon {...p}><path d="m5 12 5 5L20 7"/></Icon>,
  ArrowRight:(p)=> <Icon {...p}><path d="M5 12h14M13 6l6 6-6 6"/></Icon>,
  ArrowUp:(p)=> <Icon {...p}><path d="M12 19V5M6 11l6-6 6 6"/></Icon>,
  Upload:(p) => <Icon {...p}><path d="M12 16V4M6 10l6-6 6 6M4 18v2h16v-2"/></Icon>,
  FileText:(p)=> <Icon {...p}><path d="M14 3H6a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"/><path d="M14 3v6h6M8 13h8M8 17h6"/></Icon>,
  Brain:(p) => <Icon {...p}><path d="M8 4a3 3 0 0 0-3 3v1a3 3 0 0 0-2 2.8c0 1.6 1 2.7 2 3 0 1.7 1 3 3 3.2.4 1.7 1.7 3 3 3V4Z"/><path d="M16 4a3 3 0 0 1 3 3v1a3 3 0 0 1 2 2.8c0 1.6-1 2.7-2 3 0 1.7-1 3-3 3.2-.4 1.7-1.7 3-3 3V4Z"/></Icon>,
  MessageDots:(p)=> <Icon {...p}><path d="M21 12a8 8 0 0 1-11.4 7.2L4 21l1.8-5.6A8 8 0 1 1 21 12Z"/><circle cx="9" cy="12" r=".8" fill="currentColor"/><circle cx="12" cy="12" r=".8" fill="currentColor"/><circle cx="15" cy="12" r=".8" fill="currentColor"/></Icon>,
  Clock:(p) => <Icon {...p}><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></Icon>,
  Users:(p) => <Icon {...p}><circle cx="9" cy="8" r="3.5"/><path d="M2.5 20a6.5 6.5 0 0 1 13 0"/><path d="M16 4.5a3.5 3.5 0 0 1 0 7M21.5 20a5.5 5.5 0 0 0-4-5.3"/></Icon>,
  Book: (p) => <Icon {...p}><path d="M4 5a2 2 0 0 1 2-2h13v17H6a2 2 0 0 0-2 2V5Z"/><path d="M19 18H6a2 2 0 0 0-2 2"/></Icon>,
  Lock: (p) => <Icon {...p}><rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/></Icon>,
  Info: (p) => <Icon {...p}><circle cx="12" cy="12" r="9"/><path d="M12 8h.01M11 12h1v5h1"/></Icon>,
  Alert:(p) => <Icon {...p}><path d="M12 3 2.5 20h19L12 3Z"/><path d="M12 10v5M12 18h.01"/></Icon>,
  Sparkles:(p) => <Icon {...p}><path d="m12 3 1.6 4.4L18 9l-4.4 1.6L12 15l-1.6-4.4L6 9l4.4-1.6L12 3Z"/><path d="M19 14l.7 2 2 .7-2 .7-.7 2-.7-2-2-.7 2-.7.7-2Z"/></Icon>,
  Zap:  (p) => <Icon {...p}><path d="M13 2 3 14h7l-1 8 10-12h-7l1-8Z"/></Icon>,
  Github:(p)=> <Icon {...p}><path d="M9 19c-4 1.5-4-2-6-2m12 4v-3.5c0-1 .1-1.4-.5-2 2.8-.3 5.5-1.4 5.5-6a4.6 4.6 0 0 0-1.3-3.2 4.2 4.2 0 0 0-.1-3.2s-1.1-.3-3.5 1.3a12 12 0 0 0-6.2 0C6.5 2.8 5.4 3.1 5.4 3.1a4.2 4.2 0 0 0-.1 3.2A4.6 4.6 0 0 0 4 9.5c0 4.6 2.7 5.7 5.5 6-.6.6-.6 1.2-.5 2V21"/></Icon>,
};

// ── Nav ───────────────────────────────────────────────────────
function TLNav({ width, current = 'home', variant = 'light' }) {
  const items = [
    { id: 'home',    label: '首頁' },
    { id: 'upload',  label: '上傳與分析' },
    { id: 'report',  label: '五維診斷' },
    { id: 'coach',   label: 'AI 教練' },
    { id: 'ethics',  label: '倫理與隱私' },
  ];
  const dark = variant === 'dark';
  return (
    <nav style={{
      display:'flex', alignItems:'center', justifyContent:'space-between',
      height: 64, padding: '0 36px',
      borderBottom: `1px solid ${dark ? 'rgba(255,255,255,.08)' : 'var(--tl-line)'}`,
      background: dark ? 'rgba(15,16,20,.7)' : 'rgba(250,250,247,.7)',
      backdropFilter: 'blur(18px) saturate(160%)',
      WebkitBackdropFilter: 'blur(18px) saturate(160%)',
      position: 'sticky', top: 0, zIndex: 10,
      color: dark ? '#f4f3ef' : 'inherit',
    }}>
      <div style={{ display:'flex', alignItems:'center', gap: 36 }}>
        <Logo dark={dark}/>
        <ul style={{ display:'flex', gap: 4, listStyle:'none', margin:0, padding:0 }}>
          {items.map(it => {
            const active = it.id === current;
            return (
              <li key={it.id}>
                <a href="#" style={{
                  display:'inline-flex', alignItems:'center', height: 32, padding: '0 12px',
                  borderRadius: 8, textDecoration:'none',
                  color: active ? (dark ? '#fff' : 'var(--tl-ink)') : (dark ? 'rgba(255,255,255,.62)' : 'var(--tl-ink-3)'),
                  fontSize: 14, fontWeight: active ? 600 : 500,
                  background: active ? (dark ? 'rgba(255,255,255,.08)' : 'var(--tl-surface-2)') : 'transparent',
                  transition: 'background .15s, color .15s',
                }}
                onMouseEnter={e => { if (!active) e.currentTarget.style.background = dark ? 'rgba(255,255,255,.04)' : 'var(--tl-surface-2)'; }}
                onMouseLeave={e => { if (!active) e.currentTarget.style.background = 'transparent'; }}
                >
                  {it.label}
                </a>
              </li>
            );
          })}
        </ul>
      </div>
      <div style={{ display:'flex', alignItems:'center', gap: 12 }}>
        <span className="tl-mono" style={{ fontSize: 12, color: dark ? 'rgba(255,255,255,.45)' : 'var(--tl-ink-4)' }}>v0.4.2</span>
        <button className="tl-btn tl-btn--ghost" style={{ height: 34, fontSize: 13, padding: '0 14px',
          background: dark ? 'transparent' : undefined,
          color: dark ? '#f4f3ef' : undefined,
          borderColor: dark ? 'rgba(255,255,255,.14)' : undefined,
        }}>說明文件</button>
        <button className="tl-btn tl-btn--primary" style={{ height: 34, fontSize: 13 }}>
          開始分析 <Icons.ArrowRight size={14}/>
        </button>
      </div>
    </nav>
  );
}

function Logo({ dark }) {
  return (
    <a href="#" style={{ display:'inline-flex', alignItems:'center', gap: 9, textDecoration:'none', color:'inherit' }}>
      <span style={{
        width: 28, height: 28, borderRadius: 8,
        background: 'linear-gradient(135deg, var(--tl-blue) 0%, var(--tl-plum) 130%)',
        display:'inline-flex', alignItems:'center', justifyContent:'center',
        boxShadow: '0 1px 0 rgba(255,255,255,.25) inset, 0 4px 10px -4px rgba(46,134,171,.6)',
      }}>
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#fff" strokeWidth="2.4" strokeLinecap="round">
          <circle cx="11" cy="11" r="6"/>
          <path d="m20 20-4.5-4.5"/>
        </svg>
      </span>
      <span style={{ fontSize: 15, fontWeight: 600, letterSpacing:'-0.01em', color: dark ? '#fff' : 'var(--tl-ink)' }}>
        教學透鏡 <span style={{ color: dark ? 'rgba(255,255,255,.5)' : 'var(--tl-ink-4)', fontWeight: 500 }}>TeachLens</span>
      </span>
    </a>
  );
}

// ── Sparkline ─────────────────────────────────────────────────
function Sparkline({ data, w = 110, h = 32, color = 'var(--tl-blue)', fill = true }) {
  const min = Math.min(...data), max = Math.max(...data);
  const range = max - min || 1;
  const px = (i) => (i / (data.length - 1)) * (w - 4) + 2;
  const py = (v) => h - 2 - ((v - min) / range) * (h - 8);
  const pts = data.map((v, i) => [px(i), py(v)]);
  const d = pts.map((p, i) => `${i === 0 ? 'M' : 'L'}${p[0].toFixed(1)} ${p[1].toFixed(1)}`).join(' ');
  const last = pts[pts.length - 1];
  return (
    <svg width={w} height={h} style={{ display:'block', overflow:'visible' }}>
      {fill && (
        <path d={`${d} L${w-2} ${h-2} L2 ${h-2} Z`} fill={color} opacity=".10"/>
      )}
      <path d={d} stroke={color} strokeWidth="1.5" fill="none" strokeLinecap="round" strokeLinejoin="round"/>
      <circle cx={last[0]} cy={last[1]} r="2.6" fill="#fff" stroke={color} strokeWidth="1.5"/>
    </svg>
  );
}

// ── Status card ───────────────────────────────────────────────
function StatusCard({ icon, label, value, sub, trend, status = 'ok', spark, accent = 'blue' }) {
  const statusMap = {
    ok:    { dot: 'tl-dot--ok',    chip: 'tl-chip--ok',    text: '正常' },
    warn:  { dot: 'tl-dot--warn',  chip: 'tl-chip',        text: '異常' },
    amber: { dot: 'tl-dot--amber', chip: 'tl-chip--amber', text: '注意' },
  };
  const accentColor = accent === 'plum' ? 'var(--tl-plum)' : 'var(--tl-blue)';
  const s = statusMap[status];
  return (
    <div className="tl-card is-hoverable" style={{ padding: 22, position:'relative', overflow:'hidden' }}>
      <div style={{ display:'flex', alignItems:'flex-start', justifyContent:'space-between', gap: 12 }}>
        <div style={{ display:'flex', alignItems:'center', gap: 10 }}>
          <span style={{
            width: 32, height: 32, borderRadius: 8,
            background: `color-mix(in oklab, ${accentColor} 12%, transparent)`,
            color: accentColor,
            display:'inline-flex', alignItems:'center', justifyContent:'center',
          }}>{icon}</span>
          <div>
            <div className="tl-micro" style={{ marginBottom: 2 }}>{label}</div>
            <div style={{ display:'flex', alignItems:'center', gap: 6 }}>
              <span className={`tl-dot ${s.dot}`}/>
              <span style={{ fontSize: 12, color: 'var(--tl-ink-3)', fontWeight: 500 }}>{s.text}</span>
            </div>
          </div>
        </div>
        {trend && (
          <span className="tl-mono" style={{ fontSize: 12, color: 'var(--tl-ok)', fontWeight: 600,
            display:'inline-flex', alignItems:'center', gap: 2 }}>
            <Icons.ArrowUp size={11} stroke={2.2}/>{trend}
          </span>
        )}
      </div>
      <div style={{ display:'flex', alignItems:'flex-end', justifyContent:'space-between', marginTop: 18, gap: 12 }}>
        <div>
          <div className="tl-mono" style={{ fontSize: 30, fontWeight: 600, color: 'var(--tl-ink)', letterSpacing:'-0.02em', lineHeight: 1 }}>
            {value}
          </div>
          <div style={{ fontSize: 12, color: 'var(--tl-ink-3)', marginTop: 6 }}>{sub}</div>
        </div>
        {spark && <Sparkline data={spark} color={accentColor}/>}
      </div>
    </div>
  );
}

// ── 5-step horizontal flow (connected dots) ───────────────────
function StepFlow({ steps, active = 0, dark = false, accent }) {
  const stroke = dark ? 'rgba(255,255,255,.14)' : 'var(--tl-line)';
  const ink = dark ? '#f4f3ef' : 'var(--tl-ink)';
  const sub = dark ? 'rgba(255,255,255,.55)' : 'var(--tl-ink-3)';
  const blue = accent || 'var(--tl-blue)';
  return (
    <div style={{ position:'relative', display:'grid', gridTemplateColumns: `repeat(${steps.length}, 1fr)`, gap: 0 }}>
      {/* connector line */}
      <div style={{
        position:'absolute', left: `calc(${100/(steps.length*2)}% )`, right: `calc(${100/(steps.length*2)}% )`,
        top: 13, height: 1, background: stroke, zIndex: 0,
      }}/>
      {steps.map((s, i) => {
        const done = i < active;
        const cur  = i === active;
        return (
          <div key={i} style={{ position:'relative', display:'flex', flexDirection:'column', alignItems:'center', textAlign:'center', padding:'0 10px', zIndex: 1 }}>
            <div style={{
              width: 28, height: 28, borderRadius: '50%',
              background: cur ? blue : (done ? blue : (dark ? '#16181d' : '#fff')),
              border: `1.5px solid ${cur || done ? blue : stroke}`,
              color: cur || done ? '#fff' : sub,
              display:'inline-flex', alignItems:'center', justifyContent:'center',
              fontSize: 12, fontWeight: 600, fontFamily: 'var(--tl-font-mono)',
              boxShadow: cur ? `0 0 0 6px color-mix(in oklab, ${blue} 16%, transparent)` : 'none',
              transition: 'box-shadow .2s',
            }}>
              {done ? <Icons.Check size={14} stroke={2.4}/> : String(i+1).padStart(2,'0').slice(-1)}
            </div>
            <div style={{ marginTop: 14, color: ink, fontSize: 14, fontWeight: 600 }}>{s.title}</div>
            <div style={{ marginTop: 4, color: sub, fontSize: 12.5, lineHeight: 1.55, maxWidth: 180 }}>{s.desc}</div>
          </div>
        );
      })}
    </div>
  );
}

// ── Notion-style callout ──────────────────────────────────────
function Callout({ icon, title, children, tone = 'blue', dark = false }) {
  const map = {
    blue:  { bg: 'var(--tl-blue-50)',  bd: 'color-mix(in oklab, var(--tl-blue) 22%, transparent)',  ic: 'var(--tl-blue)' },
    plum:  { bg: 'var(--tl-plum-50)',  bd: 'color-mix(in oklab, var(--tl-plum) 22%, transparent)',  ic: 'var(--tl-plum)' },
    amber: { bg: 'var(--tl-amber-50)', bd: 'color-mix(in oklab, var(--tl-amber) 26%, transparent)', ic: 'var(--tl-amber)' },
  }[tone];
  return (
    <div style={{
      display:'flex', gap: 16, padding: '20px 22px',
      background: map.bg, border: `1px solid ${map.bd}`,
      borderRadius: 12,
    }}>
      <span style={{ color: map.ic, flexShrink: 0, marginTop: 1 }}>{icon}</span>
      <div style={{ flex: 1 }}>
        <div style={{ fontSize: 14, fontWeight: 600, color: dark ? '#fff' : 'var(--tl-ink)', marginBottom: 6 }}>{title}</div>
        <div style={{ fontSize: 13.5, lineHeight: 1.7, color: dark ? 'rgba(255,255,255,.78)' : 'var(--tl-ink-2)' }}>{children}</div>
      </div>
    </div>
  );
}

// ── 5 dimensions of TeachLens (badges used in homepage previews) ──
const DIMENSIONS = [
  { id:'q', label:'提問品質',     short:'Q', desc:'Bloom 認知層次分布', accent:'var(--tl-blue)' },
  { id:'f', label:'回饋語言',     short:'F', desc:'IRF / 等候時間',     accent:'#5e9ec1' },
  { id:'p', label:'教學節奏',     short:'P', desc:'說話佔比 / 段落切換', accent:'#8e6fa7' },
  { id:'v', label:'學生發言佔比', short:'V', desc:'TTR / 互動模式',      accent:'var(--tl-plum)' },
  { id:'l', label:'學科語言',     short:'L', desc:'術語覆蓋 / 解釋鏈',   accent:'#c25e8b' },
];

Object.assign(window, { Icon, Icons, TLNav, Logo, Sparkline, StatusCard, StepFlow, Callout, DIMENSIONS });
