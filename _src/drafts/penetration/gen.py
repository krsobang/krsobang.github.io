import json, math
def B(a,b,c): return {"type":"box","min":a,"max":b,"color":c}
def P(a,b,d=.1,c=None):
    o={"type":"pipe","from":a,"to":b,"dia":d}
    if c: o["color"]=c
    return o
def R(a,b,d=.02,c='steel'): return {"type":"rod","from":a,"to":b,"dia":d,"color":c}
def ring_x(x0,x1,y,z,r,n=28,d=.012,c='steel'):   # 슬리브(축 x) — 얇은 관벽을 봉 여러 개로
    return [R([x0,y+r*math.cos(2*math.pi*i/n),z+r*math.sin(2*math.pi*i/n)],[x1,y+r*math.cos(2*math.pi*i/n),z+r*math.sin(2*math.pi*i/n)],d,c) for i in range(n)]
def ring_y(y0,y1,x,z,r,n=28,d=.012,c='steel'):   # 슬리브(축 y)
    return [R([x+r*math.cos(2*math.pi*i/n),y0,z+r*math.sin(2*math.pi*i/n)],[x+r*math.cos(2*math.pi*i/n),y1,z+r*math.sin(2*math.pi*i/n)],d,c) for i in range(n)]
def joint_x(x,y,z,d):  # 지진분리이음(그루브 커플링 모양)
    return [P([x-.05,y,z],[x+.05,y,z],d*1.35,'dark'),R([x,y-d*.75,z],[x,y+d*.75,z],.02,'dark')]
def joint_y(x,y,z,d):
    return [P([x,y-.05,z],[x,y+.05,z],d*1.35,'dark'),R([x-d*.75,y,z],[x+d*.75,y,z],.02,'dark')]
def dump(n,spec): json.dump(spec,open(n,'w'),ensure_ascii=False)

# ---------- fig1: 벽 관통부 입체 (콘크리트 벽 + 슬리브 + 이격) ----------
def wall_scene(full=True):
    o=[B([2.8,0,0],[3.0,3.0,4.0],'concrete')]
    y,z=2.2,1.6
    o.append(P([0.6,y,z],[5.4,y,z],.114))                 # 100A 배관
    o+=ring_x(2.76,3.04,y,z,.112)                            # 200A 슬리브(예)
    for xx in (1.4,4.6): o.append(R([xx,y,z],[xx,3.0,z],.02,'dark'))  # 행거
    return o
o=wall_scene()
dump('fig1.json',{"w":1600,"h":1000,
 "title":"그림 1. 벽을 관통하는 배관 — 슬리브 구경과 배관 주위 이격 (비축척 입체 개념도)",
 "note":"원문: 벽·바닥·기초를 관통하는 배관 주위에는 이격거리 확보(제6조제3항). 관통구·슬리브 호칭구경은 배관 호칭구경 25~100 mm 미만이면 +50 mm 이상, 100 mm 이상이면 +100 mm 이상(제1호). 그림은 배관 100A·슬리브 200A 예시. 예외: 각 면에서 300 mm 이내 지진분리이음, 또는 내화성능이 요구되지 않는 석고보드 등(단서). AI 작성 비축척 — 생략: 내화채움재, 흔들림 방지 버팀대, 보·반자.",
 "camera":{"pos":[6.2,2.6,5.6],"target":[3.0,2.0,1.6],"fov":40},
 "room":{"x":[0,6],"y":[0,3.0],"z":[0,4]},"objects":o,
 "dims":[{"from":[3.06,2.2-.112,1.6],"to":[3.06,2.2+.112,1.6],"text":"슬리브 호칭구경 ≥ 배관 + 100 mm (100 mm 이상 배관)","dx":40,"dy":70}],
 "labels":[{"text":"콘크리트 벽 (관통부)","at":[2.9,1.0,3.4],"dx":40,"dy":-30},
  {"text":"배관 100A (예)","at":[4.6,2.2,1.6],"dx":30,"dy":60},
  {"text":"배관 주위 이격 확보 (제6조제3항)","at":[2.8,2.3,1.6],"dx":-360,"dy":-60,"style":"red"}]})

# ---------- 포스터 장면 ----------
cam_w={"pos":[5.0,2.8,4.2],"target":[2.9,2.0,1.4],"fov":40}
room={"x":[0,6],"y":[0,3.0],"z":[0,4]}
base=lambda objs,cam=cam_w,rm=room:{"style":"real","camera":cam,"objects":objs,"dims":[],"labels":[],"room":rm}
dump('poster/p1.json',base(wall_scene(),{"pos":[5.6,2.7,5.0],"target":[2.6,2.0,1.4],"fov":46}))
# p2 슬리브 확대(정면쪽)
o=[B([2.8,1.4,0.6],[3.0,3.0,2.6],'concrete')]
o.append(P([1.6,2.2,1.6],[4.4,2.2,1.6],.114)); o+=ring_x(2.76,3.04,2.2,1.6,.112)
dump('poster/p2.json',base(o,{"pos":[4.2,2.45,2.3],"target":[2.95,2.2,1.6],"fov":36}))
# p3 석고보드 칸막이 관통 + 면에서 300 mm 이내 지진분리이음
o=[B([2.8,0,0],[2.9,3.0,4.0],'#ecebe6')]   # 석고보드 칸막이(예)
o.append(P([0.8,2.2,1.6],[5.2,2.2,1.6],.114))
o+=joint_x(3.15,2.2,1.6,.114)
sp=base(o,{"pos":[4.6,2.7,3.4],"target":[3.0,2.1,1.5],"fov":40}); sp["dims"]=[{"from":[2.9,2.42,1.6],"to":[3.15,2.42,1.6],"text":"300 mm 이내","dy":-30}]
dump('poster/p3.json',sp)
# p4 방화구획 관통 — 신축성 있는 내화채움(주황 고리)
o=[B([2.8,0,0],[3.0,3.0,4.0],'concrete')]
o.append(P([0.8,2.2,1.6],[5.2,2.2,1.6],.114)); o+=ring_x(2.76,3.04,2.2,1.6,.112)
for r in (.068,.082,.096): o+=ring_x(3.0,3.035,2.2,1.6,r,n=36,d=.016,c='#e8812a')
dump('poster/p4.json',base(o,{"pos":[4.3,2.5,2.4],"target":[2.95,2.2,1.6],"fov":36}))
# p5 2층 이상 — 각 층 바닥 0.3 m, 천장 0.6 m 이내 지진분리이음
o=[B([0,2.9,0],[4,3.15,4],'concrete')]     # 중간층 슬래브
x,z,d=1.6,1.6,.114
o.append(P([x,0,z],[x,6.0,z],d))
for yy in (0.25,2.35,3.4,5.45): o+=joint_y(x,yy,z,d*1.3)
sp=base(o,{"pos":[4.6,3.0,5.4],"target":[1.6,3.0,1.6],"fov":50},{"x":[0,4],"y":[0,6.0],"z":[0,4]})
sp["dims"]=[{"from":[1.85,0,1.6],"to":[1.85,0.3,1.6],"text":"0.3 m 이내","dx":50},{"from":[1.85,2.9,1.6],"to":[1.85,2.3,1.6],"text":"0.6 m 이내","dx":50},
 {"from":[1.85,3.15,1.6],"to":[1.85,3.45,1.6],"text":"0.3 m 이내","dx":50},{"from":[1.85,6.0,1.6],"to":[1.85,5.4,1.6],"text":"0.6 m 이내","dx":50}]
dump('poster/p5.json',sp)
# p6 중간층 바닥 관통 — 슬리브 구경 기준 미만
o=[B([0.4,1.3,0.4],[2.8,1.55,2.8],'concrete')]
o.append(P([1.6,0,1.6],[1.6,3.0,1.6],d)); o+=ring_y(1.27,1.58,1.6,1.6,.075)
dump('poster/p6.json',base(o,{"pos":[3.4,2.6,3.6],"target":[1.6,1.4,1.6],"fov":40},{"x":[0,3.2],"y":[0,3.0],"z":[0,3.2]}))

Pst={"w":1200,"title":"벽 관통 배관,","highlight":"틈을 남기세요","subtitle":"관통구·슬리브는 배관보다 크게 — 지진 때 벽과 배관이 따로 움직입니다",
"badge":"소방시설의 내진설계 기준 제6조제3항 · 제7조 · 제11조제6호 · 소방청고시 제2026-1호(2026. 3. 1. 시행)",
"rows":[
 {"h":380,"panels":[{"n":1,"title":"대상 — 벽·바닥·기초를 관통하는 배관","span":12,"scene":"p1.json","callout_w":320,"callout_top":40,
   "callouts":[{"label":"제6조제3항","value":"배관 주위 이격 확보"},{"label":"건물 구조부재 간 상대변위 대비","value":"제6조①1"}],
   "tags":[{"text":"콘크리트 벽","x":0.38,"y":0.55},{"text":"배관","x":0.6,"y":0.38}]}]},
 {"h":330,"panels":[
   {"n":2,"title":"슬리브 구경","span":6,"scene":"p2.json","callout_pos":"overlay",
    "callouts":[{"label":"배관 25~100 mm 미만","value":"+50 mm 이상"},{"label":"배관 100 mm 이상","value":"+100 mm 이상"}]},
   {"n":3,"title":"예외 (단서)","span":6,"scene":"p3.json","callout_pos":"overlay",
    "callouts":[{"label":"각 면에서","value":"300 mm 이내 지진분리이음"},{"label":"또는 내화성능 불요 석고보드 등"}],
    "tags":[{"text":"지진분리이음","x":0.75,"y":0.28}]}]},
 {"h":330,"panels":[
   {"n":4,"title":"방화구획 관통","span":6,"scene":"p4.json","callout_pos":"overlay",
    "callouts":[{"label":"틈새는 내화채움 인정 구조 중","value":"신축성 있는 것"}],
    "tags":[{"text":"내화채움(예)","x":0.6,"y":0.75}]},
   {"n":5,"title":"2층 이상 건물","span":6,"scene":"p5.json","callout_pos":"overlay",
    "callouts":[{"label":"65 mm 이상 배관 지진분리이음","value":"바닥 0.3 m · 천장 0.6 m 이내"}]}]},
 {"h":300,"panels":[{"n":6,"title":"이격을 지키면 / 못 지키면","span":12,"scene":"p6.json","callout_w":380,"callout_top":30,
   "callouts":[{"label":"제7조③ 제6조③1호 이격 만족","value":"지진분리이음 생략 가능"},{"label":"제11조6호 중간층 관통, 슬리브 구경 미만","value":"4방향 버팀대 생략 가능"}],
   "tags":[{"text":"중간층 바닥","x":0.35,"y":0.62}]}]}],
"footer":"AI(Claude) 작성 비축척 3D 개념도 · 수치는 국가법령정보센터 원문(2026. 11. 24. 확인)에 있는 것만 표시 · 소방 실무 기준 노트"}
json.dump(Pst,open('poster/poster.json','w'),ensure_ascii=False,indent=1)
