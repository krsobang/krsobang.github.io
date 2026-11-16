"""요약 인포그래픽(포스터) 렌더러.
사용법: python3 _src/fig3d/poster.py poster.json out.png

poster.json 예:
{
  "w": 1200,
  "title": "내진 앵커볼트", "highlight": "최대허용하중",   # 흰 글씨 + 노란 강조
  "subtitle": "제조사 설계하중 그대로 쓰면 안 됩니다",
  "badge": "소방시설의 내진설계 기준 제3조의2제3항 · 소방청고시 제2026-1호",
  "rows": [  # 각 행의 높이(px)와 패널들(span: 12칸 중 몇 칸)
    {"h": 360, "panels": [
      {"n": 1, "title": "대상 확인", "span": 7, "scene": "p1.json",   # 3D 장면(spec) — bare 로 렌더
       "callouts": [{"label": "수조·펌프·함·제어반등", "value": "정착부 기준"}],
       "tags": [{"text": "제어반", "x": 0.6, "y": 0.4}]},           # 사진 위 남색 이름표(0~1 좌표)
      {"n": 2, "title": "...", "span": 5, "image": "x.png", "callouts": [...]}
    ]}
  ],
  "footer": "AI 작성 비축척 개념도 · 수치는 원문 확인값만 · 소방 실무 기준 노트"
}
panel.callout_pos: "right"(기본, 패널 오른쪽 세로 칼럼) | "overlay"(사진 위 좌상단 박스들)
"""
import sys, json, os, asyncio, subprocess, tempfile, base64, html
from playwright.async_api import async_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
E = html.escape


def render_scene(spec_path, w, h, out):
    spec = json.load(open(spec_path, encoding='utf-8'))
    spec.update({'w': w, 'h': h, 'bare': True})
    spec.setdefault('style', 'real')
    tmp = out + '.spec.json'
    json.dump(spec, open(tmp, 'w', encoding='utf-8'), ensure_ascii=False)
    r = subprocess.run([sys.executable, os.path.join(HERE, 'render.py'), tmp, out], capture_output=True, text=True)
    os.remove(tmp)
    if r.returncode != 0:
        print(r.stdout, r.stderr); sys.exit(r.returncode)


def data_uri(p):
    return 'data:image/png;base64,' + base64.b64encode(open(p, 'rb').read()).decode()


CSS = """
*{box-sizing:border-box}body{margin:0;background:#0b1626;font-family:"Noto Sans CJK KR","Malgun Gothic",sans-serif}
#p{width:%(w)dpx;padding:26px 22px 18px;background:radial-gradient(circle at 50%% 0%%,#1d3556 0,#0b1626 70%%)}
.hd{text-align:center;margin:6px 0 18px}
.t{font-size:%(tf)dpx;font-weight:900;color:#fff;letter-spacing:-2px;line-height:1.05;text-shadow:0 4px 0 #000,0 0 24px rgba(0,0,0,.6)}
.t b{color:#ffe234}
.st{font-size:%(sf)dpx;font-weight:800;color:#d9e6f5;margin-top:10px}
.bd{display:inline-block;margin-top:10px;font-size:15px;color:#9fb6cf;border:1px solid #3a5577;border-radius:20px;padding:4px 14px}
.row{display:grid;grid-template-columns:repeat(12,1fr);gap:12px;margin-bottom:12px}
.pn{position:relative;border:2px solid #2d4a70;border-radius:10px;overflow:hidden;background:#13243a}
.pn .img{position:absolute;inset:0;background-size:cover;background-position:center}
.pn .ttl{position:absolute;left:0;top:0;right:0;padding:10px 14px 18px;background:linear-gradient(#0b1626ee,#0b162600);display:flex;align-items:center;gap:10px;z-index:2}
.num{width:38px;height:38px;border-radius:50%%;background:#2f8be6;color:#fff;font-weight:900;font-size:24px;display:flex;align-items:center;justify-content:center;border:2px solid #fff;flex:none}
.ttl span{color:#fff;font-size:27px;font-weight:900;text-shadow:0 2px 3px #000}
.col{position:absolute;top:10px;right:10px;bottom:10px;display:flex;flex-direction:column;gap:8px;z-index:2}
.co{background:#0d1b2ddd;border:1.5px solid #4d6c94;border-radius:8px;padding:8px 12px;color:#e8eef6;font-size:16px;font-weight:700;line-height:1.3}
.co .v{display:block;color:#ffe234;font-size:26px;font-weight:900;margin-top:2px}
.ov{position:absolute;left:14px;bottom:14px;display:flex;flex-direction:column;gap:8px;z-index:2;max-width:55%%}
.tag{position:absolute;transform:translate(-50%%,-50%%);background:#1f3150;color:#fff;font-size:15px;font-weight:800;padding:4px 10px;border-radius:6px;border:1px solid #9fb6cf;white-space:nowrap;z-index:2}
.cap{position:absolute;left:0;right:0;bottom:0;padding:16px 12px 8px;text-align:center;color:#fff;font-weight:800;font-size:18px;background:linear-gradient(#0b162600,#0b1626e6);z-index:2}
.ft{text-align:center;color:#7f93ab;font-size:14px;margin-top:6px}
"""


def build_html(P, imgs):
    w = P.get('w', 1200)
    out = ['<!doctype html><html><head><meta charset="utf-8"><style>', CSS % {'w': w, 'tf': P.get('title_size', 92), 'sf': P.get('sub_size', 34)}, '</style></head><body><div id="p">']
    out.append('<div class="hd"><div class="t">%s <b>%s</b></div>' % (E(P.get('title', '')), E(P.get('highlight', ''))))
    if P.get('subtitle'): out.append('<div class="st">%s</div>' % E(P['subtitle']))
    if P.get('badge'): out.append('<div class="bd">%s</div>' % E(P['badge']))
    out.append('</div>')
    for ri, row in enumerate(P['rows']):
        out.append('<div class="row" style="height:%dpx">' % row['h'])
        for pi, pn in enumerate(row['panels']):
            out.append('<div class="pn" style="grid-column:span %d">' % pn.get('span', 12))
            if (ri, pi) in imgs: out.append('<div class="img" style="background-image:url(%s)"></div>' % imgs[(ri, pi)])
            if pn.get('title'):
                out.append('<div class="ttl">%s<span>%s</span></div>' % ('<div class="num">%s</div>' % pn['n'] if pn.get('n') else '', E(pn['title'])))
            cos = pn.get('callouts', [])
            if cos:
                cls = 'ov' if pn.get('callout_pos') == 'overlay' else 'col'
                st = '' if cls == 'ov' else ' style="width:%dpx;padding-top:%dpx"' % (pn.get('callout_w', 240), pn.get('callout_top', 0))
                out.append('<div class="%s"%s>' % (cls, st))
                for c in cos:
                    out.append('<div class="co">%s%s</div>' % (E(c.get('label', '')), '<span class="v">%s</span>' % E(c['value']) if c.get('value') else ''))
                out.append('</div>')
            for t in pn.get('tags', []):
                out.append('<div class="tag" style="left:%.1f%%;top:%.1f%%">%s</div>' % (t['x'] * 100, t['y'] * 100, E(t['text'])))
            if pn.get('caption'): out.append('<div class="cap">%s</div>' % E(pn['caption']))
            out.append('</div>')
        out.append('</div>')
    out.append('<div class="ft">%s</div></div></body></html>' % E(P.get('footer', 'AI 작성 비축척 개념도 · 수치는 공식 원문에서 확인한 값만 표시')))
    return ''.join(out)


async def shoot(html_text, out, w):
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={'width': w, 'height': 800}, device_scale_factor=1.5)
        await pg.set_content(html_text)
        await pg.wait_for_timeout(300)
        await (await pg.query_selector('#p')).screenshot(path=out)
        await b.close()


def main(pj, out):
    P = json.load(open(pj, encoding='utf-8'))
    base = os.path.dirname(os.path.abspath(pj))
    w = P.get('w', 1200)
    col = (w - 44 - 11 * 12) / 12
    imgs = {}
    with tempfile.TemporaryDirectory() as td:
        for ri, row in enumerate(P['rows']):
            for pi, pn in enumerate(row['panels']):
                pw = int(col * pn.get('span', 12) + 12 * (pn.get('span', 12) - 1))
                if pn.get('scene'):
                    o = os.path.join(td, f'p{ri}_{pi}.png')
                    render_scene(os.path.join(base, pn['scene']), pw, row['h'], o)
                    imgs[(ri, pi)] = data_uri(o)
                elif pn.get('image'):
                    imgs[(ri, pi)] = data_uri(os.path.join(base, pn['image']))
        asyncio.run(shoot(build_html(P, imgs), out, w))
    print('ok', out)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
