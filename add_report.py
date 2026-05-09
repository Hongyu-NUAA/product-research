#!/usr/bin/env python3
"""
博客报告添加工具
用法:
  1. 将报告 .md 文件放到 product-research/ 目录下
  2. 运行: python add_report.py <Markdown文件名.md>
  3. 博客会自动更新

示例: python add_report.py 产品调研报告_某某产品.md
"""

import sys
import os
import re
import shutil
import markdown
from datetime import datetime

BLOG_DIR = os.path.dirname(os.path.abspath(__file__))
MD_SOURCE_DIR = os.path.join(BLOG_DIR, "..", ".claude", "skills", "product-research")
REPORTS_DIR = os.path.join(BLOG_DIR, "reports")
IMAGES_DST = os.path.join(BLOG_DIR, "images")


def slugify(filename):
    """将文件名转为英文 slug"""
    name = os.path.splitext(os.path.basename(filename))[0]
    name = re.sub(r'^产品调研报告_', '', name)
    # 提取中英文和数字，用短横连接
    name = re.sub(r'[^\w\s一-鿿]', ' ', name)
    name = re.sub(r'\s+', '-', name.strip())
    return name.lower() if name else 'report'


def extract_title(text):
    for line in text.split('\n'):
        if line.startswith('# '):
            return line.replace('# ', '').strip().strip('"').strip('>').strip()
    return "未命名报告"


def extract_meta(text):
    """提取日期、摘要、标签"""
    date = ''
    m = re.search(r'调研日期[：:]\s*(\S+)', text)
    if m:
        date = m.group(1)

    # 摘要
    summary = ''
    lines = text.split('\n')
    for line in lines:
        if line.startswith('> ') and not line.startswith('> **') and not line.startswith('> -'):
            s = line.replace('> ', '').strip()
            if s and len(s) > 10:
                summary = s[:200]
                break

    # 标签
    tags = []
    kw_map = {'电动牙刷': '电动牙刷', '吹风机': '吹风机', '剃须刀': '剃须刀',
              '手机': '智能手机', '耳机': '音频', '智能': '智能硬件', '家电': '家电'}
    for kw, tag in kw_map.items():
        if kw in text:
            tags.append(tag)
    if not tags:
        tags = ['消费电子']

    return {'date': date, 'summary': summary, 'tags': tags}


def convert_report(md_file):
    """将 markdown 转为 HTML 并添加博客样式"""
    filename = os.path.basename(md_file)
    slug = slugify(filename)

    with open(md_file, 'r', encoding='utf-8') as f:
        md = f.read()

    title = extract_title(md)
    meta = extract_meta(md)
    has_mermaid = '```mermaid' in md

    # 处理 markdown
    mermaid_blocks = []
    def save_mb(m):
        mermaid_blocks.append(m.group(0))
        return f'%%MERMAID_{len(mermaid_blocks)-1}%%'

    md = re.sub(r'```mermaid\n(.*?)```', save_mb, md, flags=re.DOTALL)
    html_body = markdown.markdown(md, extensions=['fenced_code', 'tables', 'codehilite', 'nl2br'])

    for i, block in enumerate(mermaid_blocks):
        code = re.sub(r'```mermaid\n(.*?)```', r'\1', block, flags=re.DOTALL)
        html_body = html_body.replace(
            f'%%MERMAID_{i}%%',
            f'<div class="mermaid-wrap"><div class="mermaid">{code.strip()}</div></div>'
        )

    # 修复图片路径
    html_body = re.sub(r'src="(?!http|../)images/', 'src="../images/', html_body)

    # 生成 HTML
    tags_html = ''.join(f'<span class="tag tag-blue">{t}</span>' for t in meta['tags'])
    mermaid_script = ('<script src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"></script>'
                      if has_mermaid else '')
    mermaid_init = (
        '<script>mermaid.initialize({startOnLoad:true,theme:"neutral",securityLevel:"loose",'
        'fontFamily:"-apple-system,\'PingFang SC\',\'Microsoft YaHei\',sans-serif"});</script>'
        if has_mermaid else '')

    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — 产品调研报告</title>
{mermaid_script}
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: -apple-system, "PingFang SC", "Microsoft YaHei", sans-serif;
  background: #f0f2f5; color: #1a1a2e; line-height: 1.8; }}

.blog-nav {{ background: #1a1a2e; padding: 10px 24px; display: flex; align-items: center;
  gap: 10px; position: sticky; top: 0; z-index: 200; }}
.blog-nav a {{ color: #4fc3f7; text-decoration: none; font-size: 13px; }}
.blog-nav a:hover {{ color: #fff; }}
.blog-nav .sep {{ color: #334; font-size: 12px; }}
.blog-nav .current {{ font-size: 12px; color: #667; }}

.hero {{ background: linear-gradient(135deg, #1a1a2e, #16213e); color: #fff;
  padding: 36px 40px; }}
.hero h1 {{ font-size: 26px; font-weight: 700; margin-bottom: 8px; }}
.hero .meta {{ display: flex; gap: 20px; font-size: 13px; color: #8899aa; flex-wrap: wrap; }}
.tag {{ display: inline-block; padding: 2px 10px; border-radius: 4px; font-size: 12px; margin: 2px; }}
.tag-blue {{ background: rgba(79,195,247,0.15); color: #4fc3f7; }}

.content {{ max-width: 900px; margin: 0 auto; padding: 30px 40px 60px; }}
.content h2 {{ font-size: 22px; color: #1a1a2e; margin: 32px 0 16px; padding-bottom: 10px;
  border-bottom: 3px solid #4fc3f7; }}
.content h3 {{ font-size: 17px; color: #0f3460; margin: 24px 0 10px; }}
.content table {{ width: 100%; border-collapse: collapse; margin: 12px 0 20px; font-size: 13px; }}
.content th {{ background: #1a1a2e; color: #fff; padding: 10px 14px; text-align: left; }}
.content td {{ padding: 9px 14px; border-bottom: 1px solid #e8ecf0; }}
.content tr:nth-child(even) td {{ background: #f8f9fb; }}
.content blockquote {{ border-left: 4px solid #4fc3f7; background: #f0f8ff;
  padding: 12px 18px; margin: 12px 0 20px; border-radius: 0 6px 6px 0; }}
.content img {{ max-width: 100%; border-radius: 8px; margin: 12px 0; border: 1px solid #e8ecf0; }}
.content ul, .content ol {{ padding-left: 20px; margin: 8px 0 16px; }}
.content li {{ margin-bottom: 6px; }}
.mermaid-wrap {{ background: #fafbfc; border-radius: 8px; padding: 16px; margin: 16px 0;
  overflow-x: auto; border: 1px solid #e8ecf0; text-align: center; }}

.footer {{ text-align: center; padding: 40px 20px; font-size: 13px; color: #8899aa; }}

@media (max-width: 768px) {{
  .content {{ padding: 20px; }}
  .hero {{ padding: 24px 20px; }}
}}
</style>
</head>
<body>

<div class="blog-nav">
  <a href="../index.html">← 返回首页</a>
  <span class="sep">|</span>
  <span class="current">产品调研报告作品集</span>
</div>

<div class="hero">
  <h1>{title}</h1>
  <div class="meta">
    <span>📅 {meta['date'] or '未标注'}</span>
    {tags_html}
  </div>
</div>

<div class="content">
{html_body}
</div>

<div class="footer">
  <p>© 2026 · 产品调研报告作品集 · <a href="../index.html" style="color:#4fc3f7;">返回首页</a></p>
</div>

{mermaid_init}
</body>
</html>'''

    # 保存
    out_path = os.path.join(REPORTS_DIR, f'{slug}.html')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'  ✓ 报告已生成: reports/{slug}.html')
    return {'title': title, 'slug': slug, 'date': meta['date'],
            'summary': meta['summary'], 'tags': meta['tags'], 'filename': filename}


def update_index(new_report):
    """将新报告添加到首页"""
    index_path = os.path.join(BLOG_DIR, 'index.html')
    if not os.path.exists(index_path):
        print('  ⚠ 首页不存在，请先创建 blog/index.html')
        return

    with open(index_path, 'r', encoding='utf-8') as f:
        idx = f.read()

    # 构建新卡片 HTML
    tags_html = ''.join(f'<span class="tag tag-blue">{t}</span>' for t in new_report['tags'])
    card = f'''  <a href="reports/{new_report['slug']}.html" class="report-card">
    <div class="thumb">
      <span style="font-size:48px;">📄</span>
    </div>
    <div class="card-body">
      <h3>{new_report['title']}</h3>
      <div class="card-meta">
        <span class="card-date">📅 {new_report['date'] or '未标注'}</span>
        {tags_html}
      </div>
      <p>{new_report['summary'][:150] or '暂无摘要'}</p>
    </div>
  </a>

  <!-- 新报告在这里追加 -->'''

    # 替换占位符
    if '<!-- 新报告在这里追加 -->' in idx:
        idx = idx.replace('<!-- 新报告在这里追加 -->', card)
    else:
        # 在第一个 report-card 之前插入
        idx = idx.replace('<a href="reports/', card + '<a href="reports/')

    # 更新报告数量
    count_match = re.search(r'<div class="stat-num">(\d+)</div>', idx)
    if count_match:
        old_count = int(count_match.group(1))
        idx = idx.replace(
            f'<div class="stat-num">{old_count}</div>',
            f'<div class="stat-num">{old_count + 1}</div>',
            1
        )

    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(idx)
    print(f'  ✓ 首页已更新（报告数 +1）')


def copy_images():
    shutil.copytree(
        os.path.join(MD_SOURCE_DIR, 'images'),
        IMAGES_DST,
        dirs_exist_ok=True
    )


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('用法: python add_report.py <文件名.md>')
        print('示例: python add_report.py 产品调研报告_某某产品.md')
        sys.exit(1)

    md_name = sys.argv[1]
    md_path = os.path.join(MD_SOURCE_DIR, md_name)

    if not os.path.exists(md_path):
        # 尝试直接用给定的路径
        md_path = md_name
        if not os.path.exists(md_path):
            print(f'  ✗ 找不到文件: {md_path}')
            sys.exit(1)

    print(f'📄 处理报告: {os.path.basename(md_path)}')
    copy_images()
    report = convert_report(md_path)
    update_index(report)
    print(f'\n✅ 完成！打开 blog/index.html 查看')
