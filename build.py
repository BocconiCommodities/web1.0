"""Generate BSCS from articles/, events/ and featured.yml on every GitHub push."""
from pathlib import Path
from datetime import date,datetime
import json,re,yaml,mistune,base64,mimetypes
ROOT=Path(__file__).parent
CATEGORIES=['Mining & Metals','Energy','Agriculture','Shipping & Logistics','ESG','Physical Trading','Quant','Portfolio Management']
markdown=mistune.create_markdown(escape=True,plugins=['table','strikethrough','url'])
def ydate(value):
    if isinstance(value,(date,datetime)):return value.strftime('%Y-%m-%d')
    return str(value)
def read_articles():
    entries=[]
    for p in sorted((ROOT/'articles').glob('*.md')):
        raw=p.read_text(encoding='utf8');match=re.match(r'\A---\s*\n(.*?)\n---\s*\n(.*)\Z',raw,re.S)
        if not match:raise ValueError(f'{p} missing YAML frontmatter')
        meta=yaml.safe_load(match.group(1))
        if meta.get('demo',False):continue # do not publish demonstration articles
        for key in ['title','category','date','author','description','image']:
            if key not in meta:raise ValueError(f'{p}: missing {key}')
        if meta['category'] not in CATEGORIES:raise ValueError(f'{p}: invalid category')
        slug=p.stem
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',slug):raise ValueError(f'Invalid slug: {slug}')
        entries.append(dict(slug=slug,cat=meta['category'],title=meta['title'],date=ydate(meta['date']),author=meta['author'],desc=meta['description'],img=meta['image'],featured=bool(meta.get('featured',False)),demo=False,body=markdown(match.group(2))))
    return sorted(entries,key=lambda x:x['date'],reverse=True)
def read_events():
    entries=[]
    for p in sorted((ROOT/'events').glob('*.yml')):
        x=yaml.safe_load(p.read_text(encoding='utf8'))
        for key in ['title','date','dateLabel','format','time','desc','image','url']:
            if key not in x:raise ValueError(f'{p} missing {key}')
        image=x['image']
        local_image=ROOT/image
        if local_image.is_file():
            mime=mimetypes.guess_type(local_image.name)[0] or 'image/jpeg'
            image='data:'+mime+';base64,'+base64.b64encode(local_image.read_bytes()).decode('ascii')
        entries.append(dict(slug=p.stem,title=x['title'],date=ydate(x['date']),dateLabel=x['dateLabel'],format=x['format'],time=x['time'],desc=x['desc'],img=image,url=x['url']))
    return sorted(entries,key=lambda x:x['date'],reverse=True)
def json_safe(x):return json.dumps(x,ensure_ascii=False).replace('</',r'<\/')
articles=read_articles();events=read_events()
choice=yaml.safe_load((ROOT/'featured.yml').read_text(encoding='utf8'))
if choice.get('type') not in ('event','article'):raise ValueError('featured.yml type must be event or article')
if not choice.get('slug'):raise ValueError('featured.yml needs slug')
template=(ROOT/'template.html').read_text(encoding='utf8')
for var,value in [('articles',articles),('events',events),('featuredChoice',choice)]:
    pattern={'articles':r'const articles=.*?;(?=\s*const events=)', 'events':r'const events=.*?;(?=\s*const featuredChoice=)', 'featuredChoice':r'const featuredChoice=.*?;(?=\s*const archiveMode=)'}[var]
    template,n=re.subn(pattern,lambda m:'const '+var+'='+json_safe(value)+';',template,count=1,flags=re.S)
    if n!=1:raise ValueError(f'Cannot locate {var} in template.html')
for name in ['index.html','archive.html','events.html']:(ROOT/name).write_text(template,encoding='utf8')
print(f'Generated website with {len(articles)} real articles and {len(events)} events; featured {choice["type"]}: {choice["slug"]}')
