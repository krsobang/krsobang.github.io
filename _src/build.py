"""정적 블로그 빌드: _src/posts/*.html -> posts/, index.html, category/, sitemap.xml"""
import json, re, os, glob, html, datetime
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S=json.load(open(os.path.join(ROOT,'_src','site.json'),encoding='utf-8'))
CSS='''
:root{--fg:#1f2328;--muted:#5d6670;--line:#e2e5e9;--accent:#1d4f7a;--red:#c00000;--bg:#fff;--soft:#f6f7f9}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){--fg:#e6e8eb;--muted:#a3abb4;--line:#30363d;--accent:#7fb2e5;--bg:#16191d;--soft:#1e2227}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:17px/1.75 "Malgun Gothic","Apple SD Gothic Neo","Noto Sans KR",sans-serif}
a{color:var(--accent)}header.site{border-bottom:1px solid var(--line)}header.site .in,main,footer .in{max-width:780px;margin:0 auto;padding:0 16px}
header.site .in{display:flex;flex-wrap:wrap;align-items:baseline;gap:6px 18px;padding-top:14px;padding-bottom:10px}
header.site .brand{font-weight:700;font-size:1.15em;color:var(--fg);text-decoration:none}nav a{color:var(--muted);text-decoration:none;font-size:.92em;margin-right:12px}nav a:hover{color:var(--accent)}
main{padding-top:22px;padding-bottom:40px}h1{font-size:1.6em;line-height:1.35;margin:.2em 0 .3em}h2{font-size:1.15em;margin-top:1.8em;border-bottom:1px solid var(--line);padding-bottom:4px}
.meta{color:var(--muted);font-size:.9em}.rule{border:3px solid var(--red);padding:14px 16px;margin:14px 0;border-radius:2px}.rule p{margin:.4em 0}
table{border-collapse:collapse;width:100%;margin:10px 0;font-size:.95em}th,td{border:1px solid var(--line);padding:6px 8px;text-align:left}th{background:var(--soft)}
img{max-width:100%;height:auto;background:#fff;border:1px solid var(--line)}figure{margin:16px 0}.note{font-size:.88em;color:var(--muted)}
.ai{display:inline-block;font-size:.8em;border:1px solid var(--line);border-radius:3px;padding:1px 6px;color:var(--muted);margin-left:6px}
ul.list{list-style:none;padding:0}ul.list li{padding:14px 0;border-bottom:1px solid var(--line)}ul.list a.t{font-weight:700;font-size:1.08em;text-decoration:none;color:var(--fg)}ul.list a.t:hover{color:var(--accent)}
.cat{font-size:.82em;color:var(--accent);margin-right:8px}footer{border-top:1px solid var(--line);color:var(--muted);font-size:.85em}footer .in{padding-top:14px;padding-bottom:24px}
'''
def parse(path):
    t=open(path,encoding='utf-8').read()
    m=re.match(r'<!--meta\n(.*?)\n-->\n',t,re.S)
    meta={}
    for line in m.group(1).splitlines():
        k,v=line.split(':',1); meta[k.strip()]=v.strip()
    meta['body']=t[m.end():]; return meta
def cat_slug(c): return {'소방 법개정':'law','질의·해석사례':'qa','소방시설 지침':'guide','각종서류':'forms','소방 내진':'seismic'}[c]
def page(title,inner,rel,desc=''):
    navs=''.join(f'<a href="{rel}category/{cat_slug(c)}.html">{html.escape(c)}</a>' for c in S['categories'])
    return f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title><meta name="description" content="{html.escape(desc or S['description'])}"><style>{CSS}</style></head><body>
<header class="site"><div class="in"><a class="brand" href="{rel}index.html">{html.escape(S['title'])}</a><nav>{navs}</nav></div></header>
<main>{inner}</main><footer><div class="in">공식 원문(국가법령정보센터·소방청·국립소방연구원)을 기준으로 작성합니다. 적용 전 해당 시점의 원문을 확인하세요.</div></footer></body></html>'''
def item(p,rel):
    return f'<li><span class="cat">{html.escape(p["category"])}</span><span class="meta">{p["date"]}</span><br><a class="t" href="{rel}posts/{p["slug"]}.html">{html.escape(p["title"])}</a><div class="meta">{html.escape(p.get("summary",""))}</div></li>'
def main():
    posts=sorted((parse(f) for f in glob.glob(os.path.join(ROOT,'_src','posts','*.html'))),key=lambda p:p['date'],reverse=True)
    os.makedirs(os.path.join(ROOT,'posts'),exist_ok=True); os.makedirs(os.path.join(ROOT,'category'),exist_ok=True)
    for p in posts:
        ai='<span class="ai">AI 활용 그림 포함</span>' if p.get('ai_images')=='true' else ''
        inner=f'<div class="meta"><a href="../category/{cat_slug(p["category"])}.html">{html.escape(p["category"])}</a> · {p["date"]}{ai}</div><h1>{html.escape(p["title"])}</h1>{p["body"]}'
        open(os.path.join(ROOT,'posts',p['slug']+'.html'),'w',encoding='utf-8').write(page(p['title']+' | '+S['title'],inner,'../',p.get('summary','')))
    open(os.path.join(ROOT,'index.html'),'w',encoding='utf-8').write(page(S['title'],f'<p class="meta">{html.escape(S["description"])}</p><ul class="list">'+''.join(item(p,'') for p in posts)+'</ul>',''))
    for c in S['categories']:
        ps=[p for p in posts if p['category']==c]
        inner=f'<h1>{html.escape(c)}</h1>'+('<ul class="list">'+''.join(item(p,'../') for p in ps)+'</ul>' if ps else '<p class="meta">아직 글이 없습니다.</p>')
        open(os.path.join(ROOT,'category',cat_slug(c)+'.html'),'w',encoding='utf-8').write(page(c+' | '+S['title'],inner,'../'))
    if S.get('base_url'):
        b=S['base_url'].rstrip('/')
        urls=[b+'/']+[f'{b}/posts/{p["slug"]}.html' for p in posts]
        open(os.path.join(ROOT,'sitemap.xml'),'w').write('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{u}</loc></url>' for u in urls)+'</urlset>')
        open(os.path.join(ROOT,'robots.txt'),'w').write(f'User-agent: *\nAllow: /\nSitemap: {b}/sitemap.xml\n')
    print(f'built {len(posts)} posts')
if __name__=='__main__': main()
