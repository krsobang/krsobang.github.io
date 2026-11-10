"""3D 실내 장면 그림 렌더러.
사용법: python3 _src/fig3d/render.py spec.json out.png
spec.json 형식은 _src/fig3d/README.md 참고. three.js 장면을 Playwright로 열어 PNG로 저장한다."""
import sys, json, os, threading, http.server, socketserver, functools, asyncio
from playwright.async_api import async_playwright

HERE = os.path.dirname(os.path.abspath(__file__))


def serve():
    h = functools.partial(http.server.SimpleHTTPRequestHandler, directory=HERE)
    h.log_message = lambda *a, **k: None
    s = socketserver.TCPServer(('127.0.0.1', 0), h)
    threading.Thread(target=s.serve_forever, daemon=True).start()
    return s


def check_no_pipe_through_beam(spec):
    """규칙: 배관·행거봉은 보를 관통할 수 없다. 보 상자와 겹치면 렌더를 중단한다."""
    beams = [o for o in spec.get('objects', []) if o.get('type') == 'beam']
    bad = []
    for o in spec.get('objects', []):
        if o.get('type') not in ('pipe', 'rod'):
            continue
        a, b = o['from'], o['to']
        r = o.get('dia', 0.05) / 2
        for bm in beams:
            lo, hi = bm['min'], bm['max']
            for i in range(0, 201):
                t = i / 200
                pt = [a[k] + (b[k] - a[k]) * t for k in range(3)]
                if all(lo[k] - r < pt[k] < hi[k] + r for k in range(3)):
                    bad.append((o['type'], o['from'], o['to'])); break
            else:
                continue
            break
    if bad:
        print('규칙 위반: 배관/행거가 보를 관통함 ->', bad); sys.exit(2)


async def main(spec_path, out):
    spec = json.load(open(spec_path, encoding='utf-8'))
    check_no_pipe_through_beam(spec)
    srv = serve(); port = srv.server_address[1]
    async with async_playwright() as p:
        b = await p.chromium.launch(args=['--use-gl=swiftshader', '--enable-webgl', '--ignore-gpu-blocklist'])
        pg = await b.new_page(viewport={'width': spec.get('w', 1600), 'height': spec.get('h', 1000)}, device_scale_factor=1.25)
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.add_init_script('window.SPEC=' + json.dumps(spec, ensure_ascii=False) + ';')
        await pg.goto(f'http://127.0.0.1:{port}/scene.html')
        try:
            await pg.wait_for_function('window.DONE===true', timeout=30000)
        except Exception:
            print('render failed:', errs); sys.exit(1)
        await pg.wait_for_timeout(200)
        await (await pg.query_selector('#wrap')).screenshot(path=out)
        await b.close()
    srv.shutdown()
    print('ok', out)


if __name__ == '__main__':
    asyncio.run(main(sys.argv[1], sys.argv[2]))
