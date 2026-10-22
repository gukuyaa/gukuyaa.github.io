#!/usr/bin/env python3
"""把洛谷专栏（collection）或单篇文章迁移成 Hugo 文章。

用法：
    python3 scripts/luogu_import.py https://www.luogu.com.cn/article/collection/12345
    python3 scripts/luogu_import.py https://www.luogu.com.cn/article/abc123xyz
    python3 scripts/luogu_import.py 12345 --limit 5 --dry-run

洛谷页面里的 <script id="lentille-context"> 保存着文章原始 Markdown，
本脚本直接解析它，所以公式（$...$ / $$...$$）和代码块能原样保留。
"""

import argparse
import http.cookiejar
import json
import os
import re
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

BASE = 'https://www.luogu.com.cn'
UA = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36')
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
CHROME_PROFILE = None
ROOT = Path(__file__).resolve().parent.parent
POSTS_DIR = ROOT / 'content' / 'posts'
IMG_DIR = ROOT / 'static' / 'images' / 'luogu'

CATEGORY_NAMES = {
    1: '学习·资料',
    2: '生活·游记',
    3: '闲话·其他',
    4: '算法·理论',
    5: '科技·工程',
    6: '文化·漫谈',
    7: '站务·公告',
}


def make_opener():
    jar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
    opener.addheaders = [
        ('User-Agent', UA),
        ('Accept-Language', 'zh-CN,zh;q=0.9'),
        ('Referer', BASE + '/'),
    ]
    return opener


def get(opener, url, tries=3):
    """洛谷会先返回 302 + C3VK cookie，cookie jar 会自动跟随。"""
    last = None
    for _ in range(tries):
        try:
            with opener.open(url, timeout=30) as resp:
                return resp.read().decode('utf-8', 'replace')
        except Exception as exc:  # noqa: BLE001
            last = exc
            time.sleep(1.5)
    raise RuntimeError(f'请求失败 {url}: {last}')


def chrome_html(url, timeout=120):
    """用无头 Chrome 打开页面（带上登录态配置），拿到渲染后的 HTML。"""
    cmd = [CHROME, '--headless=new', '--disable-gpu', '--no-sandbox',
           f'--user-data-dir={CHROME_PROFILE}', '--virtual-time-budget=20000',
           '--dump-dom', url]
    proc = subprocess.run(cmd, capture_output=True, timeout=timeout)
    return proc.stdout.decode('utf-8', 'replace')


def page_html(opener, url):
    if CHROME_PROFILE:
        return chrome_html(url)
    return get(opener, url)


def parse_context(html):
    m = re.search(
        r'<script id="lentille-context" type="application/json">(.*?)</script>',
        html, re.S)
    if not m:
        raise RuntimeError('页面中没有 lentille-context，可能被风控拦截或页面结构变了')
    return json.loads(m.group(1))


def fetch_collection(opener, collection_id, max_pages=100):
    articles, seen, total = [], set(), 0
    for page in range(1, max_pages + 1):
        url = f'{BASE}/article/collection/{collection_id}?page={page}'
        data = parse_context(page_html(opener, url)).get('data') or {}
        coll = data.get('collection') or {}
        listing = data.get('articles') or {}
        total = listing.get('count') or 0
        result = listing.get('result') or []
        if not result:
            break
        for item in result:
            lid = item.get('lid')
            if lid and lid not in seen:
                seen.add(lid)
                articles.append({'lid': lid, 'title': item.get('title'),
                                 'collection': coll.get('name')})
        if total and len(articles) >= total:
            break
        time.sleep(0.5)
    return articles, (total or len(articles))


def fetch_article(opener, lid):
    data = parse_context(page_html(opener, f'{BASE}/article/{lid}')).get('data') or {}
    article = data.get('article')
    if not article:
        raise RuntimeError(f'文章 {lid} 不存在或无权访问')
    return article


IMG_MD_RE = re.compile(r'!\[([^\]]*)\]\((https?://[^)\s]+)\)')
IMG_HTML_RE = re.compile(r'<img[^>]+src="(https?://[^"]+)"')


def download_images(opener, markdown, lid):
    """把外链图片下载到 static/images/luogu/<lid>/，并替换为站内路径。"""
    urls = [u for _, u in IMG_MD_RE.findall(markdown)]
    urls += IMG_HTML_RE.findall(markdown)
    out_dir = IMG_DIR / lid
    saved = {}
    for url in dict.fromkeys(urls):
        parsed = urllib.parse.urlparse(url)
        name = os.path.basename(parsed.path) or 'image'
        name = re.sub(r'[^A-Za-z0-9._-]', '_', name)
        local_path = out_dir / name
        if local_path.exists() and local_path.stat().st_size > 0:
            saved[url] = name
            continue
        out_dir.mkdir(parents=True, exist_ok=True)
        try:
            with opener.open(url, timeout=30) as resp:
                local_path.write_bytes(resp.read())
            saved[url] = name
        except Exception as exc:  # noqa: BLE001
            print(f'  ! 图片下载失败 {url}: {exc}')
    for url, name in saved.items():
        markdown = markdown.replace(url, f'/images/luogu/{lid}/{name}')
    return markdown, len(saved)


def yaml_escape(text):
    text = str(text).replace('\\', '\\\\').replace('"', '\\"')
    return f'"{text}"'


def make_summary(markdown, limit=80):
    text = re.sub(r'```.*?```', ' ', markdown, flags=re.S)
    text = re.sub(r'\$\$.*?\$\$', ' ', text, flags=re.S)
    text = re.sub(r'!\[[^\]]*\]\([^)]*\)', ' ', text)
    text = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', text)
    text = re.sub(r'[#>*`_~\-]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text[:limit] + '…' if len(text) > limit else text


def fmt_date(ts):
    return time.strftime('%Y-%m-%dT%H:%M:%S+08:00', time.gmtime(ts + 8 * 3600))


def build_post(article, markdown, collection_name):
    lid = article['lid']
    title = article.get('title') or lid
    category = CATEGORY_NAMES.get(article.get('category'), '算法竞赛')
    tags = ['洛谷']
    if collection_name:
        tags.append(collection_name)
    tags.append(category)
    tags = list(dict.fromkeys(tags))
    front = [
        '---',
        f'title: {yaml_escape(title)}',
        f'date: {fmt_date(article.get("time") or int(time.time()))}',
        'draft: false',
        f'math: {"true" if "$" in markdown else "false"}',
        'tags: [' + ', '.join(yaml_escape(t) for t in tags) + ']',
        f'categories: [{yaml_escape(category)}]',
        f'summary: {yaml_escape(make_summary(markdown))}',
        f'slug: "luogu-{lid}"',
        f'source: {yaml_escape("https://www.luogu.com.cn/article/" + lid)}',
        '---',
        '',
    ]
    return '\n'.join(front) + markdown.rstrip() + '\n'


def main():
    parser = argparse.ArgumentParser(description='迁移洛谷专栏到 Hugo')
    parser.add_argument('targets', nargs='+',
                        help='专栏链接/ID 或单篇文章链接（可一次传多个）')
    parser.add_argument('--limit', type=int, default=0, help='最多迁移 N 篇')
    parser.add_argument('--force', action='store_true', help='覆盖已存在的文章')
    parser.add_argument('--dry-run', action='store_true', help='只抓取和打印，不写文件')
    parser.add_argument('--no-images', action='store_true', help='不下载图片')
    parser.add_argument('--out', default=str(POSTS_DIR), help='输出目录')
    parser.add_argument('--chrome-profile', default=None,
                        help='使用带洛谷登录态的 Chrome 配置目录抓取（用于非公开文章）')
    args = parser.parse_args()

    global CHROME_PROFILE
    CHROME_PROFILE = args.chrome_profile

    opener = make_opener()
    articles = []
    seen = set()
    for raw in args.targets:
        raw = raw.strip()
        m = re.search(r'/article/collection/(\d+)', raw)
        if m or re.fullmatch(r'\d+', raw):
            cid = m.group(1) if m else raw
            batch, total = fetch_collection(opener, cid)
            print(f'专栏 {cid} 共 {total} 篇，列表抓到 {len(batch)} 篇')
        else:
            lid = raw.rstrip('/').split('/')[-1]
            batch = [{'lid': lid, 'title': None, 'collection': None}]
        for item in batch:
            if item['lid'] not in seen:
                seen.add(item['lid'])
                articles.append(item)
    print(f'待迁移文章：{len(articles)} 篇')

    if args.limit:
        articles = articles[:args.limit]

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    done = skipped = 0
    for idx, item in enumerate(articles, 1):
        lid = item['lid']
        try:
            article = fetch_article(opener, lid)
        except Exception as exc:  # noqa: BLE001
            print(f'[{idx}/{len(articles)}] 跳过 {lid}: {exc}')
            skipped += 1
            continue
        markdown = (article.get('content') or '').strip()
        if not markdown:
            print(f'[{idx}/{len(articles)}] 跳过 {lid}: 正文为空（可能需要登录）')
            skipped += 1
            continue
        if not args.no_images:
            markdown, n_img = download_images(opener, markdown, lid)
            if n_img:
                print(f'  下载图片 {n_img} 张')
        post = build_post(article, markdown, item.get('collection'))
        out = out_dir / f'luogu-{lid}.md'
        print(f'[{idx}/{len(articles)}] {article.get("title")} -> {out}')
        if args.dry_run:
            continue
        if out.exists() and not args.force:
            print('  已存在，跳过（用 --force 覆盖）')
            skipped += 1
            continue
        out.write_text(post, encoding='utf-8')
        done += 1
        time.sleep(0.8)

    print(f'完成：写入 {done} 篇，跳过 {skipped} 篇')


if __name__ == '__main__':
    sys.exit(main())
