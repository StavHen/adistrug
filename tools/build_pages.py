#!/usr/bin/env python3
"""Make one real page per section so Google can index each one.

site/index.html is the only file to edit by hand. This script copies it to
site/work.html, site/flashes.html, ... with that page's own title,
description and address, shows that section first, fills the plain image
lists for search engines that don't run JavaScript, and rewrites sitemap.xml.
Run it after every change to site/index.html:  python3 tools/build_pages.py
"""
import html, re, sys
from datetime import date
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent / 'site'
BASE = 'https://adistrug.co.il'
NAME = 'Adi Strug'
PAGES = {  # view: (tab/title text, meta description)
    'work': ('עבודות', 'עבודות קעקוע שלי: קעקועים עדינים בקו דק (פיין ליין), פרחים, פלואו, כיתובים ועוד. בסטודיו שלי בגבעתיים.'),
    'flashes': ('פלאשים זמינים', 'פלאשים זמינים לקעקוע שמחפשים בית חם. עיצובים עדינים בקו דק, בסטודיו שלי בגבעתיים.'),
    'reviews': ('המלצות', 'הודעות שקיבלתי מלקוחות אחרי הקעקוע. קעקועים עדינים בקו דק בגבעתיים.'),
    'talk': ('בואו נדבר', 'ספרו לי על הרעיון לקעקוע, וההודעה תיפתח בוואטסאפ מוכנה לשליחה. את המועד נתאם יחד בשיחה.'),
    'studio': ('סטודיו בגבעתיים', 'הסטודיו שלי בגבעתיים: ימים ראשון עד שישי, שעות בתיאום. שאלות נפוצות לפני קעקוע.'),
    'privacy': ('פרטיות', 'מדיניות הפרטיות של האתר.'),
    'terms': ('תקנון', 'התקנון לקראת התור: מקדמה וביטולים, איחורים, תיקונים ומה חשוב לדעת לפני קעקוע.'),
    'accessibility': ('הצהרת נגישות', 'הצהרת הנגישות של האתר.'),
}

def sub1(pattern, repl, s):
    out, n = re.subn(pattern, repl, s, count=1, flags=re.S)
    if n != 1:
        sys.exit(f'build_pages: pattern not found: {pattern}')
    return out

src = (SITE / 'index.html').read_text(encoding='utf-8')

# plain image lists inside <noscript>: never shown to visitors with JavaScript
works = re.findall(r"\['(\d{3})','([^']*)'\]", src.split('const WORKS = [', 1)[1].split('].map', 1)[0])
flash_n = len(re.findall(r'\d+', src.split('const FLASHES = [', 1)[1].split(']', 1)[0]))
works_ns = '<noscript><ul>' + ''.join(f'<li><img src="img/{i}.jpg" alt="קעקוע {html.escape(t)}" loading="lazy"></li>' for i, t in works) + '</ul></noscript>'
flash_ns = '<noscript><ul>' + ''.join(f'<li><img src="img/f/f{k:02d}.jpg" alt="פלאשים זמינים לקעקוע, דף מס׳ {k}" loading="lazy"></li>' for k in range(1, flash_n + 1)) + '</ul></noscript>'
src = sub1(r'<!-- works:noscript -->.*?<!-- /works:noscript -->', lambda m: f'<!-- works:noscript -->{works_ns}<!-- /works:noscript -->', src)
src = sub1(r'<!-- flashes:noscript -->.*?<!-- /flashes:noscript -->', lambda m: f'<!-- flashes:noscript -->{flash_ns}<!-- /flashes:noscript -->', src)
(SITE / 'index.html').write_text(src, encoding='utf-8')

for view, (label, desc) in PAGES.items():
    title = f'{label} · {NAME}'
    url = f'{BASE}/{view}'
    s = src
    s = sub1(r'<title>.*?</title>', f'<title>{html.escape(title)}</title>', s)
    s = sub1(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{html.escape(desc)}">', s)
    s = sub1(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{url}">', s)
    s = sub1(r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{url}">', s)
    s = sub1(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{html.escape(title)}">', s)
    s = sub1(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{html.escape(desc)}">', s)
    s = sub1(r'<section class="view" data-view="home">', '<section class="view" data-view="home" hidden>', s)
    s = sub1(rf'<section class="view" data-view="{view}" hidden>', f'<section class="view" data-view="{view}">', s)
    s = s.replace('<!-- Edit THIS file only.', '<!-- GENERATED from index.html by tools/build_pages.py: do not edit. Edit index.html only.', 1)
    (SITE / f'{view}.html').write_text(s, encoding='utf-8')

# sitemap: every page, with its images
img = lambda p: f'    <image:image><image:loc>{BASE}/{p}</image:loc></image:image>'
images = {'': ['img/adi-4.jpg'], 'work': [f'img/{i}.jpg' for i, _ in works],
          'flashes': [f'img/f/f{k:02d}.jpg' for k in range(1, flash_n + 1)]}
today = date.today().isoformat()
rows = ['<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">']
for view in [''] + list(PAGES):
    rows += ['  <url>', f'    <loc>{BASE}/{view}</loc>', f'    <lastmod>{today}</lastmod>'] + [img(p) for p in images.get(view, [])] + ['  </url>']
rows += ['</urlset>', '']
(SITE / 'sitemap.xml').write_text('\n'.join(rows), encoding='utf-8')
print(f'build_pages: {len(PAGES)} pages, {len(works)} works, {flash_n} flashes')
