import json
def B(a,b,c): return {"type":"box","min":a,"max":b,"color":c}
def R(a,b,d=.03,c='dark'): return {"type":"rod","from":a,"to":b,"dia":d,"color":c}
def P(a,b,d=.1,c=None):
    o={"type":"pipe","from":a,"to":b,"dia":d}
    if c: o["color"]=c
    return o
def dump(n,objs,cam,room=None,dims=None,labels=None,floor=None):
    s={"style":"real","camera":cam,"objects":objs,"dims":dims or [],"labels":labels or []}
    if room: s["room"]=room
    if floor: s["floor_color"]=floor
    json.dump(s,open(n,'w'),ensure_ascii=False)
# p1: 외벽 소방관 진입창 (클린룸 외벽)
o=[B([0,0,-0.3],[9,4.2,0],'#d9dde2')]
for x in (1.2,4.5,7.8):
    o.append({"type":"window","pos":[x,1.0,0.0],"w":1.0,"h":1.2})
    o.append(B([x-0.25,2.35,0.0],[x+0.25,2.6,0.02],'#e0443a'))
o.append(B([0,0,0],[9,0.05,3],'#7d8790'))
dump('p1.json',o,{"pos":[7.5,2.0,7.5],"target":[2.6,1.6,0],"fov":44},{"x":[0,9],"y":[0,4.2],"z":[-0.3,4],"ceiling":False,"left":False},
  labels=[{"text":"소방관 진입창","at":[4.5,2.2,0.05],"dx":-30,"dy":-60,"style":"red"}])
# p2: 덕트 장애물 위·아래 헤드
o=[]
o.append(B([0.5,1.6,1.0],[4.5,2.1,2.0],'#b8c0c8'))           # 공정 덕트
for x in (1.2,3.8): o.append(R([x,2.1,1.5],[x,3.2,1.5],.03,'steel'))  # 덕트 지지대
o.append(P([0,2.85,1.5],[5,2.85,1.5],.07))                    # 천장 가지배관
for x in (1.5,3.5):
    o.append(R([x,2.85,1.5],[x,2.95,1.5],.04,'brass')); o.append({"type":"head_upright","pos":[x,3.12,1.5],"s":2.4})
o.append(P([0,1.4,2.3],[5,1.4,2.3],.06))                      # 덕트 아래 가지배관
for x in (1.5,3.5):
    o.append(R([x,1.4,2.3],[x,1.3,2.3],.04,'brass')); o.append({"type":"head_pendent","pos":[x,1.12,2.3],"s":2.4})
dump('p2.json',o,{"pos":[4.6,1.9,6.8],"target":[1.2,2.0,1.6],"fov":44},{"x":[0,5],"y":[0,3.2],"z":[0,4]},
  labels=[{"text":"공정 덕트","at":[0.8,1.85,2.0],"dx":-20,"dy":-60,"style":"light"}])
# p3: 긴급차단 설비 — 유수검지장치 1차측 개폐밸브·2차측 배수밸브
o=[P([1.5,0,0.8],[1.5,3.0,0.8],.16)]
o.append(B([1.32,1.1,0.62],[1.68,1.6,0.98],'#c62f28'))       # 유수검지장치
o.append(B([1.36,0.55,0.66],[1.64,0.8,0.94],'#2d343b'))       # 1차 측 개폐밸브
o.append(R([1.5,0.68,0.94],[1.5,0.68,1.15],.03,'steel')); o.append({"type":"sphere","pos":[1.5,0.68,1.17],"r":0.09,"color":"#e0443a"})
o.append(P([1.5,2.0,0.8],[2.6,2.0,0.8],.06)); o.append(B([2.2,1.92,0.72],[2.36,2.08,0.88],'#2d343b'))   # 2차 측 배수
o.append(P([2.6,2.0,0.8],[2.6,0.3,0.8],.06))
o.append({"type":"control_panel","pos":[3.9,0,0.8],"w":0.7,"h":1.7})
dump('p3.json',o,{"pos":[5.4,1.8,4.6],"target":[2.4,1.3,0.8],"fov":42},{"x":[0,5],"y":[0,3],"z":[0,3]},
  labels=[{"text":"1차 측 개폐밸브","at":[1.4,0.68,0.94],"dx":-90,"dy":40,"style":"red"},{"text":"2차 측 배수밸브","at":[2.28,2.0,0.88],"dx":40,"dy":-50,"style":"red"},{"text":"별도 제어반","at":[3.9,1.6,1.05],"dx":40,"dy":-30}])
# p4: 펌프 토출 배관 (유속)
o=[{"type":"pump_set","pos":[0.6,0,1.2],"l":2.2}]
o.append(P([2.15,1.04,1.2],[2.15,2.2,1.2],.2)); o.append(P([2.15,2.2,1.2],[5.5,2.2,1.2],.2))
dump('p4.json',o,{"pos":[5.6,2.0,5.0],"target":[2.6,1.0,1.2],"fov":42},{"x":[0,5.5],"y":[0,3],"z":[0,3]})
# p5: 호스릴 소화전 25 m
o=[{"type":"hydrant_box","pos":[5.5,0.9,0.0]},{"type":"flex","pts":[[5.5,0.9,0.25],[5.0,0.05,1.0],[3.5,0.05,1.8],[1.5,0.05,2.6]],"dia":0.05}]
dump('p5.json',o,{"pos":[2.0,2.6,6.2],"target":[4.6,0.7,1.2],"fov":46},{"x":[0,7],"y":[0,3],"z":[0,5]},
  dims=[{"from":[5.5,0.03,0.3],"to":[0.8,0.03,3.0],"text":"수평거리 25 m 이하","dy":-30}])
# p6: 물류자동화 레일(장애물) 옆 헤드
o=[P([0,2.7,1.0],[6,2.7,1.0],.07)]
for x in (1.0,3.0,5.0):
    o.append(R([x,2.7,1.0],[x,2.8,1.0],.04,'brass')); o.append({"type":"head_upright","pos":[x,2.97,1.0],"s":2.4})
o.append(B([0,2.25,1.35],[6,2.4,1.75],'#f0b81c'))               # 물류 레일
for x in (0.6,3.0,5.4): o.append(R([x,2.4,1.55],[x,3.0,1.55],.04,'steel'))
o.append(B([2.6,1.7,1.3],[3.4,2.25,1.8],'#6f7a85'))              # 이송 대차
dump('p6.json',o,{"pos":[6.4,1.6,5.6],"target":[3.0,2.3,1.3],"fov":42},{"x":[0,6],"y":[0,3.0],"z":[0,4]},
  labels=[{"text":"물류 이송 레일","at":[4.6,2.3,1.75],"dx":30,"dy":60,"style":"light"}])
PS={"w":1200,"title":"반도체 공장 성능위주설계","highlight":"2025. 12. 개정","subtitle":"가이드라인 「7. 반도체 분야」 소방시설 항목, 무엇이 늘었나",
"badge":"소방청 「소방시설등 성능위주설계 평가 운영 표준 가이드라인」 2025. 12. 1. 반도체 분야 일부 개정 · 법적 구속력 없음(원문)",
"rows":[
 {"h":330,"panels":[
  {"n":1,"title":"소방관 진입창","span":6,"scene":"p1.json","callout_pos":"overlay",
   "callouts":[{"label":"수평거리 40 m 이내마다 설치 기준","value":"완화 적용 가능"},{"label":"클린룸·외조기실 등","value":"설치 안 할 수 있음"}]},
  {"n":2,"title":"장애물 위·아래 헤드","span":6,"scene":"p2.json","callout_pos":"overlay",
   "callouts":[{"label":"장애물 최상부·최하단 반영","value":"단서 신설"},{"label":"불연·난연 장애물 하단이 바닥에서","value":"1.2 m 이하면 제외"}]}]},
 {"h":330,"panels":[
  {"n":3,"title":"긴급차단 설비(신설)","span":7,"scene":"p3.json","callout_w":240,"callout_top":56,
   "callouts":[{"label":"생산지역 습식 스프링클러","value":"설치 가능"},{"label":"전용 방재실 별도 제어반","value":"수동 작동"}]},
  {"n":4,"title":"배관 유속(신설)","span":5,"scene":"p4.json","callout_pos":"overlay",
   "callouts":[{"label":"수리계산으로 구경 정할 때","value":"10 ㎧ 초과 금지"}]}]},
 {"h":320,"panels":[
  {"n":5,"title":"호스릴 소화전(신설)","span":6,"scene":"p5.json","callout_pos":"overlay","callout_top":250,
   "callouts":[{"label":"호스릴 옥내소화전·미분무","value":"25 m(보행 40 m)"}]},
  {"n":6,"title":"물류자동화 구역(신설)","span":6,"scene":"p6.json","callout_pos":"overlay",
   "callouts":[{"label":"장애물 폭 3배 이격 곤란 시","value":"8.2 ℓ/㎡·min 이상"}]}]}],
"footer":"AI(Claude) 작성 비축척 3D 개념도 · 문구·수치는 소방청 법령자료실 게시 가이드라인 PDF 원문(2026. 11. 17. 확인)에 있는 것만 · 생략: 소화가스 과압배출구, 특별피난계단 대책, 건축·시뮬레이션 항목 · 소방 실무 기준 노트"}
json.dump(PS,open('poster.json','w'),ensure_ascii=False,indent=1)
