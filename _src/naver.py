"""네이버 블로그 붙여넣기용 페이지 생성: posts/*.html의 본문을 인라인 스타일 HTML로 바꿔 naver/<slug>.html에 저장.
네이버 에디터는 class·<style>을 지우므로 모든 서식을 style 속성으로 넣는다."""
import os, html
from bs4 import BeautifulSoup

SITE = 'https://krsobang.github.io'
RED = '#c00000'
GRAY = '#5d6670'
LINE = '#d9dde2'


def _abs(src, slug):
    if src.startswith('http'):
        return src
    return SITE + '/' + src.replace('../', '')


def convert(p):
    """p: build.py가 읽은 글(meta dict + body). 네이버용 본문 HTML 문자열을 돌려준다."""
    out = []
    # 상단: 칩 줄 + 한 줄 요약 + 왜 + 타일(표)
    chips = [p['category']] + ([p['effective']] if p.get('effective') else []) + ['기준일 ' + p['date']]
    out.append(f'<p style="color:{GRAY};font-size:13px">' + ' · '.join(html.escape(c) for c in chips) + '</p>')
    if p.get('subtitle'):
        out.append(f'<p style="color:{GRAY}">{html.escape(p["subtitle"])}</p>')
    if p.get('oneline'):
        out.append(f'<p style="border-left:4px solid {RED};background:#f6f7f9;padding:12px 14px;font-size:17px"><b>한 줄 요약</b> — {_inline(p["oneline"])}</p>')
    if p.get('why'):
        out.append(f'<p><b>왜?</b> {_inline(p["why"])}</p>')
    tiles = [p[k] for k in ('tile1', 'tile2', 'tile3') if p.get(k)]
    if tiles:
        cells = ''
        for t in tiles:
            k, v, s = (t.split('|') + ['', ''])[:3]
            cells += (f'<td style="border:1px solid {LINE};padding:10px 12px;vertical-align:top;width:33%">'
                      f'<span style="color:{GRAY};font-size:13px">{k}</span><br>'
                      f'<b style="font-size:20px">{_inline(v)}</b><br><span style="color:{GRAY};font-size:13px">{s}</span></td>')
        out.append(f'<table style="border-collapse:collapse;width:100%"><tr>{cells}</tr></table>')

    soup = BeautifulSoup(p['body'], 'html.parser')
    for d in soup.find_all('details'):          # 접힌 내용은 펼쳐서
        sm = d.find('summary')
        q = sm.get_text() if sm else ''
        if sm:
            sm.decompose()
        new = soup.new_tag('div')
        b = soup.new_tag('p'); b.string = 'Q. ' + q; b['style'] = 'font-weight:bold;margin-bottom:2px'
        new.append(b)
        for c in list(d.contents):
            new.append(c)
        d.replace_with(new)
    for tl in soup.select('.tl'):               # 타임라인 → 한 줄
        steps = [' '.join(st.get_text(' ').split()) for st in tl.select('.st')]
        np_ = soup.new_tag('p'); np_['style'] = 'background:#f6f7f9;padding:10px 12px'
        np_.append(BeautifulSoup(' → '.join(f'<b>{html.escape(s)}</b>' for s in steps), 'html.parser'))
        tl.replace_with(np_)
    for el in soup.select('.rule'):
        el['style'] = f'border:3px solid {RED};padding:12px 14px;margin:12px 0'
    for el in soup.select('.red'):
        el['style'] = f'color:{RED};font-weight:bold'
    for el in soup.select('td.chg'):
        el['style'] = 'background:#fdf2f2'
    for el in soup.select('.note'):
        el['style'] = f'color:{GRAY};font-size:13px'
    for el in soup.find_all('h2'):
        el.name = 'p'
        el['style'] = 'font-size:19px;font-weight:bold;border-bottom:1px solid #cfd4da;padding-bottom:4px;margin-top:28px'
    for t in soup.find_all('table'):
        t['style'] = 'border-collapse:collapse;width:100%'
    for c in soup.find_all(['td', 'th']):
        base = f'border:1px solid {LINE};padding:8px 10px;vertical-align:top;text-align:left'
        if c.name == 'th':
            base += ';background:#f4f6f8;font-weight:bold'
        c['style'] = base + (';' + c['style'] if c.get('style') and c.get('style') not in base else '')
    for im in soup.find_all('img'):
        im['src'] = _abs(im['src'], p['slug'])
        im['style'] = 'max-width:100%'
        im.attrs.pop('loading', None)
    for a in soup.find_all('a'):
        if a.get('href', '').startswith('../'):
            a['href'] = SITE + '/' + a['href'][3:]
    for el in soup.find_all(True):
        el.attrs.pop('class', None)
    out.append(str(soup))
    if p.get('tags'):
        out.append('<p style="color:#1d4f7a">' + ' '.join('#' + t.strip().replace(' ', '') for t in p['tags'].split(',') if t.strip()) + '</p>')
    return '\n'.join(out)


def _inline(s):
    return (s.replace('<span class="red">', f'<span style="color:{RED};font-weight:bold">'))


PAGE = '''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex"><title>네이버 복사용 — {title}</title>
<style>body{{margin:0;background:#eef0f3;font:16px/1.7 "Malgun Gothic","Noto Sans KR",sans-serif;color:#1f2328}}
.bar{{position:sticky;top:0;background:#1f2328;color:#fff;padding:10px 16px;display:flex;flex-wrap:wrap;gap:8px;align-items:center;z-index:2}}
.bar b{{margin-right:auto}}button{{font:inherit;border:0;border-radius:6px;padding:8px 14px;cursor:pointer;background:#03c75a;color:#fff;font-weight:bold}}
button.t{{background:#fff;color:#1f2328}}.msg{{font-size:13px;color:#b9f6ca;min-width:120px}}
.box{{max-width:760px;margin:16px auto;background:#fff;padding:22px 26px;border:1px solid #cfd4da}}.how{{max-width:760px;margin:12px auto 0;font-size:14px;color:#5d6670;padding:0 16px}}</style></head><body>
<div class="bar"><b>네이버 복사용</b><button class="t" onclick="cp('t')">① 제목 복사</button><button onclick="cp('c')">② 본문 복사</button><span class="msg" id="m"></span></div>
<div class="how">네이버 글쓰기 → ① 제목 칸에 붙여넣기 → ② 본문에 붙여넣기 → 카테고리 「{cat}」 선택 → 그림이 안 붙었으면 아래 그림을 저장해 올리기 → <b>AI 활용 설정</b> 확인 후 발행</div>
<div class="box"><div id="t" style="font-size:24px;font-weight:bold">{title}</div></div>
<div class="box" id="c">{body}</div>
<script>
async function cp(id){{const el=document.getElementById(id);const m=document.getElementById('m');
try{{const h=new Blob([el.innerHTML],{{type:'text/html'}}),t=new Blob([el.innerText],{{type:'text/plain'}});
await navigator.clipboard.write([new ClipboardItem({{'text/html':h,'text/plain':t}})]);m.textContent=(id=='t'?'제목':'본문')+' 복사됨';}}
catch(e){{const r=document.createRange();r.selectNodeContents(el);const s=getSelection();s.removeAllRanges();s.addRange(r);
try{{document.execCommand('copy');m.textContent='복사됨';}}catch(_){{m.textContent='Ctrl+C를 누르세요';}}}}}}
</script></body></html>'''


def write(root, p):
    os.makedirs(os.path.join(root, 'naver'), exist_ok=True)
    page = PAGE.format(title=html.escape(p['title']), cat=html.escape(p['category']), body=convert(p))
    open(os.path.join(root, 'naver', p['slug'] + '.html'), 'w', encoding='utf-8').write(page)
