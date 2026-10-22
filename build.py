"""Build BSCS GitHub Pages website from independent Markdown research articles."""
from pathlib import Path
from datetime import datetime
import html, json, re
import yaml, mistune

ROOT=Path(__file__).parent
CATEGORIES=['Mining & Metals','Energy','Agriculture','Shipping & Logistics','ESG','Physical Trading','Quant','Portfolio Management']
renderer=mistune.create_markdown(escape=True,plugins=['table','strikethrough','url'])

def load_article(path):
    content=path.read_text(encoding='utf-8')
    m=re.match(r'\A---\s*\n(.*?)\n---\s*\n(.*)\Z',content,re.S)
    if not m: raise ValueError(f'{path}: missing YAML frontmatter')
    meta=yaml.safe_load(m.group(1))
    needed=['title','category','date','author','description','image','featured','demo']
    for key in needed:
        if key not in meta: raise ValueError(f'{path}: missing {key}')
    if meta['category'] not in CATEGORIES: raise ValueError(f'{path}: invalid category {meta["category"]}')
    date=str(meta['date'])
    datetime.strptime(date,'%Y-%m-%d')
    slug=path.stem
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',slug): raise ValueError('Invalid filename '+slug)
    return dict(slug=slug,cat=meta['category'],title=meta['title'],date=date,author=meta['author'],desc=meta['description'],img=meta['image'],featured=bool(meta['featured']),demo=bool(meta['demo']),body=renderer(m.group(2)))

articles=sorted([load_article(p) for p in (ROOT/'articles').glob('*.md')],key=lambda a:a['date'],reverse=True)
template=(ROOT/'template.html').read_text(encoding='utf-8')
# Keep the one-page layout and update only the independent Markdown article data.
# This avoids resetting navigation, section order or responsive styling.
article_json=json.dumps(articles,ensure_ascii=False).replace('</','<\\/')
template,count=re.subn(r'const articles=\[.*?\];(?=\s*function )',lambda m:'const articles='+article_json+';',template,count=1,flags=re.S)
if count!=1:
    raise ValueError('Could not find the articles data block in template.html')
(ROOT/'index.html').write_text(template,encoding='utf-8')
print(f'Built index.html with {len(articles)} independent articles')
