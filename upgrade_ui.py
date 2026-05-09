#!/usr/bin/env python3
"""Upgrade report UI: collapsible sidebar, accordion TOC, dark/light theme."""

import re

path = r'E:\xhy\blog\reports\laifen-i2.html'

with open(path, 'r', encoding='utf-8') as f:
    html = f.read()

# ====================================================================
# 1. Replace full CSS with theme-variable based CSS
# ====================================================================
old_css_end = '</style>'

# Close the old style block FIRST, then open a new one (not nested!)
new_css = '''</style>
<style>
/* ===== Theme Variables ===== */
:root {
  --bg-body: #f0f2f5;
  --bg-card: #ffffff;
  --bg-card-alt: #f8f9fb;
  --text-primary: #1a1a2e;
  --text-secondary: #444444;
  --text-muted: #8899aa;
  --border-color: #e8ecf0;
  --hero-bg: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
  --sidebar-bg: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
  --sidebar-text: #c0c8d4;
  --sidebar-text-muted: #8899aa;
  --sidebar-hover: rgba(255,255,255,0.05);
  --accent: #4fc3f7;
  --accent-dim: rgba(79,195,247,0.15);
  --shadow: 0 1px 3px rgba(0,0,0,0.06);
  --table-th-bg: #1a1a2e;
  --table-th-color: #ffffff;
  --mermaid-bg: #fafbfc;
  --blockquote-bg: #f0f8ff;
  --stat-bg: #f8f9fb;
  --tag-blue-bg: #e3f2fd;
  --tag-blue-color: #1565c0;
  --navbar-bg: rgba(26,26,46,0.95);
  --stat-negative: #c62828;
  --stat-warning: #e65100;
  --stat-positive: #2e7d32;
}
[data-theme="dark"] {
  --bg-body: #0d1117;
  --bg-card: #161b22;
  --bg-card-alt: #1c2333;
  --text-primary: #e6edf3;
  --text-secondary: #c0c8d4;
  --text-muted: #6a7a8a;
  --border-color: #30363d;
  --hero-bg: linear-gradient(135deg, #0d1117 0%, #161b22 50%, #1c2333 100%);
  --sidebar-bg: linear-gradient(180deg, #0d1117 0%, #161b22 100%);
  --sidebar-text: #8b949e;
  --sidebar-text-muted: #6a7a8a;
  --accent: #58a6ff;
  --accent-dim: rgba(88,166,255,0.15);
  --shadow: 0 1px 3px rgba(0,0,0,0.3);
  --table-th-bg: #1c2333;
  --table-th-color: #e6edf3;
  --mermaid-bg: #1c2333;
  --blockquote-bg: #0d1117;
  --stat-bg: #1c2333;
  --tag-blue-bg: rgba(88,166,255,0.15);
  --tag-blue-color: #58a6ff;
  --navbar-bg: rgba(13,17,23,0.95);
  --stat-negative: #f85149;
  --stat-warning: #d18616;
  --stat-positive: #56d364;
}

body { font-family: -apple-system, "PingFang SC", "Microsoft YaHei", sans-serif; background: var(--bg-body); color: var(--text-primary); line-height: 1.8; transition: background 0.3s, color 0.3s; }

/* ===== Sidebar ===== */
.sidebar { position: fixed; left: 0; top: 42px; width: 260px; height: calc(100vh - 42px); background: var(--sidebar-bg); color: #fff; overflow-y: auto; z-index: 100; padding: 16px 0; transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1), background 0.3s; }
.sidebar.collapsed { transform: translateX(-260px); }
.sidebar-header { display: flex; align-items: center; justify-content: space-between; padding: 0 16px 12px 20px; border-bottom: 1px solid rgba(255,255,255,0.06); margin-bottom: 8px; }
.sidebar-header h2 { font-size: 13px; color: var(--sidebar-text-muted); text-transform: uppercase; letter-spacing: 2px; margin: 0; padding: 0; border: none; }
.sidebar-toggle-btn { background: none; border: none; color: var(--sidebar-text-muted); cursor: pointer; font-size: 16px; padding: 4px; border-radius: 4px; line-height: 1; }
.sidebar-toggle-btn:hover { color: #fff; background: var(--sidebar-hover); }

/* TOC Accordion */
.toc-section { border-bottom: 1px solid rgba(255,255,255,0.04); }
.toc-head { display: flex; align-items: center; padding: 7px 16px 7px 20px; cursor: pointer; color: var(--sidebar-text); font-size: 13px; transition: all 0.2s; border-left: 3px solid transparent; user-select: none; }
.toc-head:hover { color: #fff; background: var(--sidebar-hover); border-left-color: var(--accent); }
.toc-head .arrow { margin-left: auto; font-size: 10px; color: var(--sidebar-text-muted); transition: transform 0.2s; }
.toc-head.open .arrow { transform: rotate(90deg); }
.toc-head.open { border-left-color: var(--accent); color: var(--accent); }
.toc-sub { display: none; }
.toc-sub.open { display: block; }
.toc-sub a { display: block; padding: 5px 16px 5px 32px; color: var(--sidebar-text-muted); text-decoration: none; font-size: 12px; transition: all 0.2s; border-left: 3px solid transparent; }
.toc-sub a:hover { color: #fff; background: var(--sidebar-hover); border-left-color: var(--accent); }
.toc-sub a.active { color: var(--accent); border-left-color: var(--accent); }

/* Overlay (mobile) */
.sidebar-overlay { display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.4); z-index: 99; }

/* Skinny toggle button */
.skinny-toggle { position: fixed; left: 0; top: 50%; transform: translateY(-50%); z-index: 101; background: var(--navbar-bg); border: none; color: var(--accent); cursor: pointer; width: 28px; height: 48px; border-radius: 0 6px 6px 0; font-size: 14px; display: none; align-items: center; justify-content: center; transition: background 0.3s; }
.skinny-toggle:hover { background: #1a1a2e; }

/* Theme toggle */
.theme-toggle { position: fixed; bottom: 20px; left: 14px; z-index: 102; background: var(--navbar-bg); border: 1px solid rgba(255,255,255,0.1); color: var(--accent); cursor: pointer; width: 36px; height: 36px; border-radius: 50%; font-size: 16px; display: flex; align-items: center; justify-content: center; transition: left 0.3s, background 0.3s; }
.sidebar.collapsed ~ .theme-toggle { left: 14px; }

/* ===== Main ===== */
.main { margin-left: 260px; transition: margin-left 0.3s cubic-bezier(0.4, 0, 0.2, 1); }
.main.expanded { margin-left: 0; }

/* ===== Hero ===== */
.hero { background: var(--hero-bg); color: #fff; padding: 60px 50px; position: relative; overflow: hidden; transition: background 0.3s; }
.hero::after { content: ""; position: absolute; right: -100px; top: -100px; width: 400px; height: 400px; border-radius: 50%; background: rgba(79,195,247,0.08); }
.hero h1 { font-size: 36px; font-weight: 700; margin-bottom: 10px; letter-spacing: 1px; }
.hero .subtitle { font-size: 16px; color: #8899aa; }
.hero .meta { margin-top: 20px; display: flex; gap: 30px; font-size: 13px; color: #8899aa; flex-wrap: wrap; }
.hero .meta span { display: flex; align-items: center; gap: 6px; }

/* ===== Content ===== */
.content { max-width: 1100px; padding: 40px 50px 80px; }

/* ===== Cards ===== */
.card { background: var(--bg-card); border-radius: 12px; padding: 30px 35px; margin-bottom: 28px; box-shadow: var(--shadow); border: 1px solid var(--border-color); transition: background 0.3s, border-color 0.3s; }
.card h2 { font-size: 22px; color: var(--text-primary); margin-bottom: 20px; padding-bottom: 12px; border-bottom: 3px solid var(--accent); display: flex; align-items: center; gap: 10px; }
.card h3 { font-size: 17px; color: var(--text-secondary); margin: 24px 0 12px; }
.card h4 { font-size: 15px; color: var(--text-secondary); margin: 16px 0 8px; }
.card ul, .card ol { padding-left: 20px; margin: 8px 0 16px; }
.card li { margin-bottom: 6px; font-size: 14px; color: var(--text-primary); }
.card li::marker { color: var(--accent); }

/* ===== Tables ===== */
table { width: 100%; border-collapse: collapse; margin: 12px 0 20px; font-size: 13px; }
th { background: var(--table-th-bg); color: var(--table-th-color); padding: 10px 14px; text-align: left; font-weight: 600; white-space: nowrap; }
td { padding: 9px 14px; border-bottom: 1px solid var(--border-color); color: var(--text-primary); }
tr:nth-child(even) td { background: var(--bg-card-alt); }
tr:hover td { background: var(--accent-dim); }
th:first-child { border-radius: 6px 0 0 0; }
th:last-child { border-radius: 0 6px 0 0; }

/* ===== Image Grid ===== */
.img-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px; margin: 16px 0; }
.img-grid figure { margin: 0; border-radius: 8px; overflow: hidden; border: 1px solid var(--border-color); background: var(--bg-card-alt); }
.img-grid img { width: 100%; height: 200px; object-fit: cover; display: block; }
.img-grid figcaption { padding: 8px 12px; font-size: 12px; color: var(--text-muted); text-align: center; }

/* ===== Tags ===== */
.tag { display: inline-block; padding: 2px 10px; border-radius: 4px; font-size: 12px; font-weight: 500; margin: 2px; }
.tag-blue { background: var(--tag-blue-bg); color: var(--tag-blue-color); }
.tag-green { background: #e8f5e9; color: #2e7d32; }
.tag-red { background: #fce4ec; color: #c62828; }
.tag-orange { background: #fff3e0; color: #e65100; }
.tag-purple { background: #f3e5f5; color: #6a1b9a; }
[data-theme="dark"] .tag-green { background: rgba(46,125,50,0.2); color: #56d364; }
[data-theme="dark"] .tag-red { background: rgba(198,40,40,0.2); color: #f85149; }
[data-theme="dark"] .tag-orange { background: rgba(230,81,0,0.2); color: #d18616; }
[data-theme="dark"] .tag-purple { background: rgba(106,27,154,0.2); color: #bc8cff; }

/* ===== Quick Stats ===== */
.stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 16px; margin: 16px 0; }
.stat-card { background: var(--stat-bg); border-radius: 10px; padding: 16px; text-align: center; border: 1px solid var(--border-color); }
.stat-card .num { font-size: 28px; font-weight: 700; color: var(--text-primary); line-height: 1.2; }
.stat-card .label { font-size: 12px; color: var(--text-muted); margin-top: 4px; }
.stat-card.negative .num { color: #c62828; }
.stat-card.warning .num { color: #e65100; }
.stat-card.positive .num { color: #2e7d32; }

/* ===== Mermaid ===== */
.mermaid-wrap { background: var(--mermaid-bg); border-radius: 8px; padding: 16px; margin: 16px 0; overflow-x: auto; border: 1px solid var(--border-color); text-align: center; transition: background 0.3s; }
.mermaid-wrap svg { max-width: 100%; height: auto; }

/* ===== Blockquote ===== */
blockquote { border-left: 4px solid var(--accent); background: var(--blockquote-bg); padding: 12px 18px; margin: 12px 0 20px; border-radius: 0 6px 6px 0; font-size: 14px; color: var(--text-secondary); }

/* ===== SWOT ===== */
.swot-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin: 16px 0; }
.swot-card { padding: 20px; border-radius: 10px; border: 1px solid; }
.swot-card h4 { margin: 0 0 10px; font-size: 15px; }
.swot-card ul { padding-left: 16px; margin: 0; }
.swot-card li { font-size: 13px; margin-bottom: 4px; }
.swot-s { background: #e8f5e9; border-color: #a5d6a7; }
.swot-s h4 { color: #2e7d32; }
.swot-w { background: #fce4ec; border-color: #ef9a9a; }
.swot-w h4 { color: #c62828; }
.swot-o { background: #e3f2fd; border-color: #90caf9; }
.swot-o h4 { color: #1565c0; }
.swot-t { background: #fff3e0; border-color: #ffcc80; }
.swot-t h4 { color: #e65100; }
[data-theme="dark"] .swot-s { background: rgba(46,125,50,0.15); border-color: #2e7d32; }
[data-theme="dark"] .swot-w { background: rgba(198,40,40,0.15); border-color: #c62828; }
[data-theme="dark"] .swot-o { background: rgba(21,101,192,0.15); border-color: #1565c0; }
[data-theme="dark"] .swot-t { background: rgba(230,81,0,0.15); border-color: #e65100; }
[data-theme="dark"] .swot-s h4 { color: #56d364; }
[data-theme="dark"] .swot-w h4 { color: #f85149; }
[data-theme="dark"] .swot-o h4 { color: #58a6ff; }
[data-theme="dark"] .swot-t h4 { color: #d18616; }

/* ===== Timeline ===== */
.timeline { position: relative; padding: 0; margin: 16px 0; }
.timeline::before { content: ""; position: absolute; left: 16px; top: 0; bottom: 0; width: 2px; background: var(--border-color); }
.tl-item { padding: 4px 0 4px 40px; position: relative; }
.tl-item::before { content: ""; position: absolute; left: 11px; top: 12px; width: 12px; height: 12px; border-radius: 50%; background: var(--accent); border: 2px solid var(--bg-card); box-shadow: 0 0 0 2px var(--accent); }
.tl-item .tl-time { font-size: 12px; color: var(--text-muted); }
.tl-item .tl-text { font-size: 14px; color: var(--text-primary); }
.tl-item.red::before { background: #ef5350; box-shadow: 0 0 0 2px #ef5350; }

/* ===== Badges ===== */
.badge { display: inline-block; padding: 1px 8px; border-radius: 3px; font-size: 11px; font-weight: 600; }
.badge-yes { background: #e8f5e9; color: #2e7d32; }
.badge-no { background: #fce4ec; color: #c62828; }

/* ===== Misc ===== */
.matrix-wrap { overflow-x: auto; }
.matrix-wrap table th:first-child { min-width: 120px; }
.rating { color: #f5a623; letter-spacing: 1px; }
	[data-theme="dark"] .rating { color: #e8b830; }
.topic-tags { margin: 12px 0; }
.topic-tags .tag { font-size: 11px; }

/* ===== Blog nav ===== */
.blog-nav { background: var(--navbar-bg); padding: 10px 24px; display: flex; align-items: center; gap: 10px; position: sticky; top: 0; z-index: 200; }
.blog-nav a { color: var(--accent); text-decoration: none; font-size: 13px; }
.blog-nav a:hover { color: #fff; }
.blog-nav .sep { color: var(--text-muted); font-size: 12px; }
.blog-nav .current { font-size: 12px; color: var(--text-muted); }

/* ===== Scrollbar ===== */
.sidebar::-webkit-scrollbar { width: 4px; }
.sidebar::-webkit-scrollbar-thumb { background: var(--text-muted); border-radius: 2px; }

/* ===== Responsive ===== */
@media (max-width: 768px) {
  .sidebar { transform: translateX(-260px); }
  .sidebar.open { transform: translateX(0); }
  .sidebar-overlay.open { display: block; }
  .main { margin-left: 0 !important; }
  .skinny-toggle { display: flex !important; }
  .hero { padding: 30px 20px; }
  .hero h1 { font-size: 24px; }
  .content { padding: 20px; }
  .card { padding: 20px; }
  .swot-grid { grid-template-columns: 1fr; }
  .stats { grid-template-columns: repeat(2, 1fr); }
  .img-grid { grid-template-columns: 1fr; }
}
@media (min-width: 769px) {
  .skinny-toggle { display: flex; }
  .sidebar.collapsed ~ .skinny-toggle { display: flex; }
}
</style>'''

idx = html.index(old_css_end)
html = html[:idx] + new_css + html[idx:]

# ====================================================================
# 2. Remove the duplicate inline blog-nav style block
# ====================================================================
dup = '''<style>
.blog-nav { background: rgba(26,26,46,0.95); padding: 10px 24px; display: flex; align-items: center; gap: 10px; border-bottom: 1px solid #334; position: sticky; top: 0; z-index: 200; }
.blog-nav a { color: #4fc3f7; text-decoration: none; font-size: 13px; }
.blog-nav a:hover { color: #fff; }
.blog-nav .sep { color: var(--text-muted); font-size: 12px; }
.blog-nav .current { font-size: 12px; color: #667; }
.sidebar { top: 42px !important; height: calc(100vh - 42px) !important; }
</style>'''
html = html.replace(dup, '')

# ====================================================================
# 3. Replace sidebar with accordion version
# ====================================================================
old_sidebar_start = '<!-- Sidebar -->'
old_sidebar_end = '<!-- Main -->'

new_sidebar = '''<!-- Sidebar -->
<nav class="sidebar" id="toc">
  <div class="sidebar-header">
    <h2>目录</h2>
    <button class="sidebar-toggle-btn" onclick="toggleSidebar()" title="收起侧栏">◀</button>
  </div>

  <div class="toc-section">
    <div class="toc-head open" onclick="toggleSub(this)"><span>一、产品基本信息</span><span class="arrow">▶</span></div>
    <div class="toc-sub open">
      <a href="#basic">产品基本信息</a>
    </div>
  </div>
  <div class="toc-section">
    <div class="toc-head" onclick="toggleSub(this)"><span>二、目标用户画像</span><span class="arrow">▶</span></div>
    <div class="toc-sub">
      <a href="#user">人群 / 场景 / 痛点</a>
    </div>
  </div>
  <div class="toc-section">
    <div class="toc-head" onclick="toggleSub(this)"><span>三、核心功能与技术规格</span><span class="arrow">▶</span></div>
    <div class="toc-sub">
      <a href="#spec">硬件 / 芯片方案 / 功能</a>
    </div>
  </div>
  <div class="toc-section">
    <div class="toc-head" onclick="toggleSub(this)"><span>四、市场全景数据</span><span class="arrow">▶</span></div>
    <div class="toc-sub">
      <a href="#market-global">4.1 全球市场</a>
      <a href="#market-china">4.2 中国市场</a>
      <a href="#market-channel">4.3 线上渠道</a>
      <a href="#market-share">4.4 品牌份额</a>
      <a href="#market-history">4.5 徕芬销售数据</a>
      <a href="#market-compare">4.6 竞品对比</a>
      <a href="#market-background">4.7 竞品背景</a>
    </div>
  </div>
  <div class="toc-section">
    <div class="toc-head" onclick="toggleSub(this)"><span>五、设计与用户体验</span><span class="arrow">▶</span></div>
    <div class="toc-sub">
      <a href="#design">外观 / 交互 / 品质感</a>
    </div>
  </div>
  <div class="toc-section">
    <div class="toc-head" onclick="toggleSub(this)"><span>六、渠道与营销策略</span><span class="arrow">▶</span></div>
    <div class="toc-sub">
      <a href="#channel">渠道 / 营销 / 品牌危机</a>
    </div>
  </div>
  <div class="toc-section">
    <div class="toc-head" onclick="toggleSub(this)"><span>七、用户口碑分析</span><span class="arrow">▶</span></div>
    <div class="toc-sub">
      <a href="#reputation">好评 / 差评 / 评分</a>
    </div>
  </div>
  <div class="toc-section">
    <div class="toc-head" onclick="toggleSub(this)"><span>八、成本与供应链</span><span class="arrow">▶</span></div>
    <div class="toc-sub">
      <a href="#supply">BOM / 供应链 / 亏损</a>
    </div>
  </div>
  <div class="toc-section">
    <div class="toc-head" onclick="toggleSub(this)"><span>九、公司经营与财务状况</span><span class="arrow">▶</span></div>
    <div class="toc-sub">
      <a href="#company">财务 / 专利 / 高管流失</a>
    </div>
  </div>
  <div class="toc-section">
    <div class="toc-head" onclick="toggleSub(this)"><span>十、SWOT 分析</span><span class="arrow">▶</span></div>
    <div class="toc-sub">
      <a href="#swot">SWOT 矩阵</a>
    </div>
  </div>
  <div class="toc-section">
    <div class="toc-head" onclick="toggleSub(this)"><span>十一、总结与建议</span><span class="arrow">▶</span></div>
    <div class="toc-sub">
      <a href="#summary">结论 / 建议 / 行动项</a>
    </div>
  </div>
  <div class="toc-section">
    <div class="toc-head" onclick="toggleSub(this)"><span>十二、参考资料</span><span class="arrow">▶</span></div>
    <div class="toc-sub">
      <a href="#ref">来源与链接</a>
    </div>
  </div>
</nav>

<!-- Sidebar Overlay (mobile) -->
<div class="sidebar-overlay" id="sidebarOverlay" onclick="toggleSidebar()"></div>

<!-- Skinny toggle -->
<button class="skinny-toggle" id="skinnyToggle" onclick="toggleSidebar()" title="切换侧栏">☰</button>

<!-- Theme toggle -->
<button class="theme-toggle" id="themeToggle" onclick="toggleTheme()" title="切换主题">\U0001f319</button>

<!-- Main -->'''

s = html.index(old_sidebar_start)
e = html.index(old_sidebar_end)
html = html[:s] + new_sidebar + html[e:]

# ====================================================================
# 4. Inject JavaScript before </body>
# ====================================================================
js = '''<script>
// Sidebar toggle
function toggleSidebar() {
  var sidebar = document.getElementById('toc');
  var main = document.querySelector('.main');
  var overlay = document.getElementById('sidebarOverlay');
  var isMobile = window.innerWidth <= 768;
  if (isMobile) {
    sidebar.classList.toggle('open');
    overlay.classList.toggle('open');
  } else {
    sidebar.classList.toggle('collapsed');
    main.classList.toggle('expanded');
  }
}

// Accordion: toggle sub-items
function toggleSub(el) {
  el.classList.toggle('open');
  var sub = el.nextElementSibling;
  if (sub) sub.classList.toggle('open');
}

// Highlight active section on scroll
(function() {
  var sections = document.querySelectorAll('.card[id]');
  var tocLinks = document.querySelectorAll('.toc-sub a');
  if (!sections.length) return;
  window.addEventListener('scroll', function() {
    var current = '';
    sections.forEach(function(section) {
      var top = section.getBoundingClientRect().top;
      if (top <= 200) current = section.getAttribute('id');
    });
    tocLinks.forEach(function(link) {
      link.classList.remove('active');
      if (link.getAttribute('href') === '#' + current) link.classList.add('active');
    });
  });
})();

// Theme toggle
function toggleTheme() {
  var html = document.documentElement;
  var btn = document.getElementById('themeToggle');
  if (html.getAttribute('data-theme') === 'dark') {
    html.removeAttribute('data-theme');
    btn.textContent = '\U0001f319';
    localStorage.setItem('theme', 'light');
  } else {
    html.setAttribute('data-theme', 'dark');
    btn.textContent = '\\u2600\\ufe0f';
    localStorage.setItem('theme', 'dark');
  }
  if (typeof mermaid !== 'undefined') {
    document.querySelectorAll('.mermaid').forEach(function(el, i) {
      el.textContent = mermaidSources[i] || el.textContent;
      el.removeAttribute('data-processed');
    });
    mermaid.run({ nodes: document.querySelectorAll('.mermaid') });
  }
}

// Load saved theme
(function() {
  var saved = localStorage.getItem('theme');
  var btn = document.getElementById('themeToggle');
  if (saved === 'dark') {
    document.documentElement.setAttribute('data-theme', 'dark');
    btn.textContent = '\\u2600\\ufe0f';
  } else {
    btn.textContent = '\U0001f319';
  }
})();

// Responsive: on resize, close mobile sidebar
window.addEventListener('resize', function() {
  if (window.innerWidth > 768) {
    document.getElementById('toc').classList.remove('open');
    document.getElementById('sidebarOverlay').classList.remove('open');
  }
});
</script>'''

html = html.replace('</body>', js + '\n</body>')

# ====================================================================
# 5. Insert mermaid source storage before mermaid.initialize()
# ====================================================================
mermaid_store = '''// Store original mermaid source texts for re-rendering
var mermaidSources = [];
(function() {
  document.querySelectorAll('.mermaid').forEach(function(el, i) {
    mermaidSources[i] = el.textContent;
  });
})();

'''

if "var mermaidSources" not in html and "mermaid.initialize(" in html:
    html = html.replace('mermaid.initialize(', mermaid_store + 'mermaid.initialize(')
    print('  - Mermaid source storage inserted')

# ====================================================================
# 6. Also fix the sidebar position CSS override from blog-nav
# ====================================================================
# Remove any leftover !important overrides
html = html.replace('''.sidebar { top: 42px !important; height: calc(100vh - 42px) !important; }''', '')

with open(path, 'w', encoding='utf-8') as f:
    f.write(html)

print('OK - UI upgrade complete')
print(f'  - Collapsible sidebar (toggle button)')
print(f'  - Accordion TOC (click to expand/collapse)')
print(f'  - Dark/Light theme toggle (persisted)')
