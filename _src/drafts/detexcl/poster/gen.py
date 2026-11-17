import json
def B(a,b,c): return {"type":"box","min":a,"max":b,"color":c}
def R(a,b,d=.03,c='dark'): return {"type":"rod","from":a,"to":b,"dia":d,"color":c}
def dump(n,objs,cam,room=None,dims=None,labels=None,**kw):
    s={"style":"real","camera":cam,"objects":objs,"dims":dims or [],"labels":labels or []}
    if room: s["room"]=room
    s.update(kw)
    json.dump(s,open(n,'w'),ensure_ascii=False)
WHITE='#f4f4f2'
# p1: 높은 천장(20 m 이상) — 아트리움, 벽에 불꽃감지기(단서)
o=[]
for x in (1.0,5.0): o.append(B([x-.25,0,0.3],[x+.25,8,0.8],'concrete'))
o.append(B([1.6,0,0],[2.6,2.2,0.05],'#7a5a3a'))   # 문
o.append(B([3.6,6.8,-0.02],[4.0,7.2,0.12],'#c9302c'))  # 불꽃감지기 몸체
o.append({"type":"sphere","pos":[3.8,7.0,0.14],"r":0.07,"color":"#2b2f33"})
dims=[{"from":[5.6,0,1.2],"to":[5.6,8,1.2],"text":"20 m 이상","dx":-70,"dy":0}]
dump('p1.json',o,{"pos":[3.2,3.2,13.5],"target":[3.2,4.2,0.5],"fov":44},{"x":[0,6.2],"y":[0,8],"z":[0,3]},dims)
# p2: 헛간 — 지붕+기둥, 벽 없음, 연기가 바람에 흩어짐
o=[B([0,0,0],[6,0.05,3.5],'#8b7d62')]
for x in (0.2,5.8):
    for z in (0.2,3.3): o.append(B([x-.1,0,z-.1],[x+.1,2.8,z+.1],'#7a5a3a'))
o.append(B([-0.2,2.8,-0.2],[6.2,3.0,3.7],'#6b6f73'))
o+= [B([2.2,0.05,1.3],[3.2,0.8,2.2],'#c9a66b'),B([3.4,0.05,1.5],[4.0,0.6,2.0],'#c9a66b')]
o.append({"type":"heat_detector","pos":[3.0,2.8,1.75],"s":2.5})
o.append({"type":"smoke","pos":[4.6,1.6,1.8],"n":16,"r":0.4,"sx":2.5,"seed":7})
dump('p2.json',o,{"pos":[8.5,3.2,8.0],"target":[3.0,1.4,1.6],"fov":42},floor_color='#6f7a62')
# p3: 욕실 — 욕조·샤워
o=[B([0.2,0,0.1],[2.0,0.55,0.9],WHITE),B([0.3,0.3,0.2],[1.9,0.56,0.8],'#cfe3ef'),
   R([2.8,0,0.15],[2.8,2.0,0.15],.04,'steel'),R([2.8,2.0,0.15],[2.8,2.0,0.45],.03,'steel'),
   {"type":"sphere","pos":[2.8,1.95,0.5],"r":0.09,"color":"steel"},
   {"type":"plane","min":[3.3,0,0.1],"max":[3.32,2.0,1.2],"color":"#bcd4f0"},
   {"type":"smoke","pos":[2.2,1.8,0.8],"n":12,"r":0.3,"sx":2,"seed":3}]
dump('p3.json',o,{"pos":[5.6,2.2,5.2],"target":[1.8,1.2,0.6],"fov":44},{"x":[0,3.8],"y":[0,2.6],"z":[0,3]},floor_color='#8fa3ad')
# p4: 파이프덕트 — 2개 층 관통 샤프트
o=[]
for y in (0,3.0,6.0): o.append(B([-1,y-.25,-1],[4,y,3],'slab'))
o.append({"type":"plane","min":[0.8,0,0.6],"max":[2.2,5.75,1.6],"color":"#bcd4f0"})
for x in (1.1,1.5,1.9): o.append({"type":"pipe","from":[x,-0.2,1.1],"to":[x,5.9,1.1],"dia":0.12,"color":"steel" if x!=1.5 else "red"})
o.append(B([0.75,2.75,0.55],[2.25,3.0,1.65],'#c0392b'))
dims=[{"from":[0.8,6.05,1.7],"to":[2.2,6.05,1.7],"text":"수평단면적 5 ㎡ 이하","dx":0,"dy":-28}]
dump('p4.json',o,{"pos":[6.5,4.2,7.5],"target":[1.5,2.8,1.0],"fov":44},dims=dims)
# p5: 주방 — 조리대·냄비·연기, 천장 열감지기
o=[B([0.3,0,0.1],[3.2,0.9,0.75],'#9aa3ab'),B([1.0,0.9,0.25],[1.5,1.15,0.6],'#5d6670'),
   {"type":"pipe","from":[2.2,0.9,0.42],"to":[2.2,1.15,0.42],"dia":0.4,"color":"steel"},
   B([0.8,2.0,0.05],[2.6,2.3,0.9],'#b8bec4'),
   {"type":"smoke","pos":[1.9,1.6,0.6],"n":14,"r":0.28,"seed":11},
   {"type":"heat_detector","pos":[2.9,2.8,1.6],"s":2.6}]
dump('p5.json',o,{"pos":[5.2,1.9,5.6],"target":[1.9,1.5,0.8],"fov":44},{"x":[0,4],"y":[0,2.8],"z":[0,3]},floor_color='#7d8580')
# p6: 프레스 공장 — 대형 프레스
o=[B([0.8,0,0.6],[3.2,0.5,1.8],'#3b4652'),B([1.0,0.5,0.8],[1.3,2.6,1.6],'#e0a21c'),B([2.7,0.5,0.8],[3.0,2.6,1.6],'#e0a21c'),
   B([0.9,2.6,0.7],[3.1,3.1,1.7],'#e0a21c'),B([1.4,1.4,0.85],[2.6,1.7,1.55],'#5d6670'),B([1.4,0.5,0.85],[2.6,0.75,1.55],'#5d6670'),
   B([3.6,0,0.7],[4.6,0.9,1.5],'#6b7a8a')]
dump('p6.json',o,{"pos":[6.4,2.6,6.4],"target":[2.3,1.4,1.1],"fov":44},{"x":[0,5.2],"y":[0,3.8],"z":[0,3.2]})
P={"w":1200,"title":"이곳 감지기,","highlight":"빼도 될까요?","subtitle":"원문은 \"설치하지 않을 수 있다\" — 의무 면제가 아니라 선택입니다",
"badge":"자동화재탐지설비 및 시각경보장치의 화재안전기술기준(NFTC 203) 2.4.5 · 국립소방연구원공고 제2026-10호(2026. 3. 1. 시행)",
"rows":[
 {"h":380,"panels":[
   {"n":1,"title":"천장·반자 높이 20 m 이상","span":7,"scene":"p1.json","callout_w":250,"callout_top":40,
    "callouts":[{"label":"2.4.5.1","value":"20 m 이상"},{"label":"단, 2.4.1 단서 감지기로 적응성 있으면 제외 대상 아님"}],
    "tags":[{"text":"불꽃감지기(예)","x":0.36,"y":0.3}]},
   {"n":2,"title":"외부와 기류가 통하는 곳","span":5,"scene":"p2.json","callout_pos":"overlay",
    "callouts":[{"label":"2.4.5.2 헛간 등","value":"유효 감지 불가"}],"tags":[{"text":"연기가 흩어짐","x":0.72,"y":0.55}]}]},
 {"h":330,"panels":[
   {"n":3,"title":"목욕실·샤워 화장실","span":6,"scene":"p3.json","callout_pos":"overlay",
    "callouts":[{"label":"2.4.5.5","value":"욕조·샤워시설"}],"tags":[{"text":"수증기","x":0.5,"y":0.3}]},
   {"n":4,"title":"파이프덕트","span":6,"scene":"p4.json","callout_w":230,"callout_top":40,
    "callouts":[{"label":"2.4.5.6 둘 중 하나","value":"2개 층마다 구획"},{"label":"또는","value":"단면 5 ㎡ 이하"}],
    "tags":[{"text":"방화구획","x":0.42,"y":0.5}]}]},
 {"h":330,"panels":[
   {"n":5,"title":"주방 등 평상시 연기","span":6,"scene":"p5.json","callout_pos":"overlay",
    "callouts":[{"label":"2.4.5.7","value":"연기감지기만 제외"}],"tags":[{"text":"열감지기(예)","x":0.72,"y":0.2}]},
   {"n":6,"title":"부식성가스·고온/저온·프레스/주조","span":6,"scene":"p6.json","callout_pos":"overlay",
    "callouts":[{"label":"2.4.5.3 / 2.4.5.4 / 2.4.5.8","value":"원문 요건 확인"}],"tags":[{"text":"프레스(예)","x":0.45,"y":0.2}]}]}],
"footer":"AI(Claude) 작성 비축척 3D 개념도 · 조문·수치는 국가법령정보센터 원문(2026. 11. 18. 확인)에 있는 것만 표시 · 소방 실무 기준 노트"}
json.dump(P,open('poster.json','w'),ensure_ascii=False,indent=1)
