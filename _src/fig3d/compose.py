"""번호 패널 인포그래픽 합성기.
사용법: python3 _src/fig3d/compose.py compose.json out.png
compose.json 예:
{"title":"큰 제목","subtitle":"부제","cols":2,
 "panels":[{"num":1,"title":"패널 제목","img":"a.png",
            "callouts":["핵심 값 <b>0.75 m 미만</b>","설명 문장"],"span":2}],
 "footer":"AI 작성 비축척 개념도 — 생략: ..."}
- img: 3D 장면 렌더(render.py) PNG 경로(compose.json 기준 상대/절대)
- callouts: 패널 오른쪽(또는 아래) 요약 상자, <b>는 핵심 숫자(빨강 강조)
- span: 가로로 차지할 칸 수(기본 1)"""
import sys, json, os, base64, asyncio, html
from playwright.async_api import async_playwright

CSS = '''
*{box-sizing:border-box}body{margin:0;background:#f4f6f9;font:16px/1.5 "Noto Sans CJK KR","Noto Sans CJK TC","Malgun Gothic",sans-serif;color:#1f2d45}
#wrap{width:1600px;padding:28px 30px 20px;background:#f4f6f9}
h1{margin:0;font-size:46px;font-weight:900;color:#14284b;letter-spacing:-1px}
h1 em{font-style:normal;color:#c00000}
.sub{margin:4px 0 18px;font-size:22px;font-weight:700;color:#3a4a66}
.grid{display:grid;gap:14px}
.p{background:#fff;border:1px solid #cfd6e0;border-radius:10px;overflow:hidden;display:flex;flex-direction:column}
.hd{display:flex;align-items:center;gap:12px;padding:10px 14px;background:#14284b;color:#fff;font-size:24px;font-weight:800}
.n{flex:none;width:36px;height:36px;border-radius:50%;background:#fff;color:#14284b;font-size:22px;font-weight:900;display:flex;align-items:center;justify-content:center}
.bd{display:flex;flex:1}
.bd img{display:block;flex:1;min-width:0;object-fit:cover;width:100%}
.co{flex:none;width:300px;padding:12px;display:flex;flex-direction:column;gap:10px;background:#eef2f7}
.c{background:#fff;border:1px solid #cfd6e0;border-left:5px solid #c00000;border-radius:6px;padding:9px 12px;font-size:19px;font-weight:600;line-height:1.4}
.c b{color:#c00000;font-size:26px;font-weight:900;display:block}
.stack .bd{flex-direction:column}.stack .co{width:auto;flex-direction:row}.stack .c{flex:1}
.ft{margin-top:12px;font-size:14px;color:#5b6a82}
'''

def uri(p, base):
    p = p if os.path.isabs(p) else os.path.join(base, p)
    return 'data:image/png;base64,' + base64.b64encode(open(p, 'rb').read()).decode()

def build(spec, base):
    cols = spec.get('cols', 2)
    h = [f'<style>{CSS}</style><div id="wrap">']
    h.append(f'<h1>{spec["title"]}</h1>')
    if spec.get('subtitle'):
        h.append(f'<div class="sub">{html.escape(spec["subtitle"])}</div>')
    h.append(f'<div class="grid" style="grid-template-columns:repeat({cols},1fr)">')
    for p in spec['panels']:
        span = p.get('span', 1)
        cls = 'p stack' if p.get('stack') else 'p'
        h.append(f'<div class="{cls}" style="grid-column:span {span}">')
        h.append(f'<div class="hd"><span class="n">{p.get("num","")}</span>{html.escape(p["title"])}</div><div class="bd">')
        h.append(f'<img src="{uri(p["img"], base)}">')
        if p.get('callouts'):
            h.append('<div class="co">' + ''.join(f'<div class="c">{c}</div>' for c in p['callouts']) + '</div>')
        h.append('</div></div>')
    h.append('</div>')
    if spec.get('footer'):
        h.append(f'<div class="ft">{html.escape(spec["footer"])}</div>')
    h.append('</div>')
    return '<!doctype html><meta charset="utf-8">' + ''.join(h)

async def main(sp, out):
    spec = json.load(open(sp, encoding='utf-8'))
    base = os.path.dirname(os.path.abspath(sp))
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={'width': 1600, 'height': 900}, device_scale_factor=1.25)
        await pg.set_content(build(spec, base))
        await pg.wait_for_timeout(300)
        await (await pg.query_selector('#wrap')).screenshot(path=out)
        await b.close()
    print('ok', out)

if __name__ == '__main__':
    asyncio.run(main(sys.argv[1], sys.argv[2]))
