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
script_start=template.index('const articles=')
script_end=template.index('function renderBoard()',script_start)
new_script=r'''const articles=__ARTICLES__;
function showPage(page){
 if(!document.getElementById(page)?.classList.contains('page'))page='home';
 document.querySelectorAll('.page').forEach(p=>p.classList.toggle('active',p.id===page));
 document.querySelectorAll('.nav-link').forEach(n=>n.classList.toggle('selected',n.dataset.page===page));
 document.getElementById('navigation').classList.remove('open');
 if(location.hash!=='#'+page)history.replaceState(null,'','#'+page);
 window.scrollTo(0,0);
}
document.querySelectorAll('[data-page]').forEach(x=>x.addEventListener('click',e=>{e.preventDefault();showPage(x.dataset.page)}));
document.getElementById('menuButton').onclick=()=>document.getElementById('navigation').classList.toggle('open');
function escapeHTML(s){return String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}
function articleCard(a){return `<article class="article-tile" tabindex="0" role="link" data-article="${a.slug}"><div class="article-thumb"><img loading="lazy" src="${escapeHTML(a.img)}" alt="${escapeHTML(a.cat)}"></div><div class="article-meta">${escapeHTML(a.cat)} / ${escapeHTML(a.date)}${a.demo?' / DEMO':''}</div><h3>${escapeHTML(a.title)}</h3><p>${escapeHTML(a.desc)}</p></article>`}
function wireArticles(){document.querySelectorAll('[data-article]').forEach(x=>{const open=()=>openArticle(x.dataset.article);x.addEventListener('click',open);x.addEventListener('keydown',e=>{if(e.key==='Enter')open()})})}
function openArticle(slug){
 let a=articles.find(a=>a.slug===slug);if(!a)return;
 document.getElementById('articleView').innerHTML=`<div class="article-back"><button type="button" id="articleBack">← All articles</button></div><header class="reading-head"><div class="article-meta">${escapeHTML(a.cat)} / ${escapeHTML(a.date)}</div><h1 class="serif">${escapeHTML(a.title)}</h1><p>${escapeHTML(a.desc)}</p><div class="reading-byline">By ${escapeHTML(a.author)}</div></header><img class="reading-cover" src="${escapeHTML(a.img)}" alt="${escapeHTML(a.title)}">${a.demo?'<div class="demo-notice">DEMONSTRATION ARTICLE — This is fictional sample content created solely to preview the BSCS website. It is not published research or investment advice.</div>':''}<div class="reading-prose">${a.body}</div><div class="article-back"><button type="button" id="articleBackBottom">← Back to articles</button></div>`;
 showPage('article-reader');history.replaceState(null,'','#article/'+encodeURIComponent(slug));
 document.getElementById('articleBack').onclick=()=>showPage('articles');
 document.getElementById('articleBackBottom').onclick=()=>showPage('articles');
}
function renderHome(){
 const featured=articles.find(a=>a.featured)||articles[0];
 document.getElementById('homeFeatured').innerHTML=featured?`<article class="home-feature" data-article="${featured.slug}" role="link" tabindex="0"><div class="home-feature-image"><img src="${escapeHTML(featured.img)}" alt="${escapeHTML(featured.cat)}"></div><div class="home-feature-text"><span class="overline">${escapeHTML(featured.cat)}${featured.demo?' / DEMO':''}</span><h3 class="serif">${escapeHTML(featured.title)}</h3><p>${escapeHTML(featured.desc)}</p><span class="feature-read">Read article →</span></div></article>`:'<p>No articles published yet.</p>';
 document.getElementById('homeArticles').innerHTML=articles.filter(a=>a.slug!==featured?.slug).slice(0,3).map(articleCard).join('');wireArticles();
}
function renderArticles(cat='All'){
 let cats=['All','Mining & Metals','Energy','Agriculture','Shipping & Logistics','ESG','Physical Trading','Quant','Portfolio Management'];
 document.getElementById('articleFilters').innerHTML=cats.map(c=>`<button class="filter ${cat===c?'active':''}" data-filter="${c}">${c}</button>`).join('');
 document.querySelectorAll('[data-filter]').forEach(b=>b.onclick=()=>renderArticles(b.dataset.filter));
 document.getElementById('articleGrid').innerHTML=articles.filter(a=>cat==='All'||a.cat===cat).map(articleCard).join('')||'<p>No articles in this category yet.</p>';wireArticles();
}
'''.replace('__ARTICLES__',json.dumps(articles,ensure_ascii=False).replace('</','<\\/'))
template=template[:script_start]+new_script+template[script_end:]
template=template.replace("renderArticles();renderBoard();showPage(location.hash.slice(1)||'home');wireArticles();document.getElementById('closeModal').onclick=()=>document.getElementById('articleModal').classList.remove('show');document.getElementById('articleModal').onclick=e=>{if(e.target.id==='articleModal')e.target.classList.remove('show')};document.addEventListener('keydown',e=>{if(e.key==='Escape')document.getElementById('articleModal').classList.remove('show')});", "renderHome();renderArticles();renderBoard();const initialHash=decodeURIComponent(location.hash.slice(1));if(initialHash.startsWith('article/'))openArticle(initialHash.slice(8));else showPage(initialHash||'home');window.addEventListener('hashchange',()=>{const h=decodeURIComponent(location.hash.slice(1));if(h.startsWith('article/'))openArticle(h.slice(8));else showPage(h||'home')});")
# Add reading page before main ends, without affecting original layout.
reader='<div class="page" id="article-reader"><div class="wrap"><article id="articleView" class="reading-layout"></article></div></div>'
template=template.replace('</main>',reader+'</main>')
css='''<style>
.reading-layout{max-width:880px;margin:0 auto;padding:45px 0 115px}.article-back button{background:none;border:0;color:#235475;font-weight:600;padding:10px 0;cursor:pointer}.reading-head{padding:23px 0 30px}.reading-head h1{font-size:clamp(36px,5.2vw,68px);line-height:1.16;margin:16px 0}.reading-head p{font-size:18px;color:#627080}.reading-byline{font-size:13px;font-weight:600;color:#435d72}.reading-cover{width:100%;max-height:420px;object-fit:cover;display:block}.demo-notice{margin:25px 0;padding:16px 20px;background:#edf1f2;border-left:4px solid #071c35;color:#173650;font-size:13px;font-weight:600}.reading-prose{max-width:730px;margin:38px auto 55px;font-size:17px;line-height:1.85;color:#243649}.reading-prose h2{font:normal 30px/1.3 'Libre Baskerville',serif;color:#071c35;margin:35px 0 14px}.reading-prose h3{font-size:22px;margin:28px 0 12px}.reading-prose p{margin:0 0 20px}.reading-prose table{width:100%;border-collapse:collapse;font-size:14px;display:block;overflow-x:auto}.reading-prose th,.reading-prose td{border-bottom:1px solid #ced5db;padding:12px;text-align:left}.reading-prose img{max-width:100%;height:auto}.reading-prose a{color:#165b8a;text-decoration:underline}.article-tile,.home-feature{cursor:pointer}@media(max-width:650px){.reading-layout{padding:28px 0 65px}.reading-head h1{font-size:35px}.reading-head p{font-size:16px}.reading-prose{font-size:15px}.reading-prose h2{font-size:25px}}
</style>'''
template=template.replace('</head>',css+'</head>')
# Suppress unused old modal and placeholder disclaimer.
template=template.replace('<p class="small-note">Editorial placeholders for the website preview. Articles have not been published.</p>','')
(ROOT/'index.html').write_text(template,encoding='utf-8')
print(f'Built index.html with {len(articles)} independent articles')
