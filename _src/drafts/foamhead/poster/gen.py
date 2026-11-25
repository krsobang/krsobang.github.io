import json, math
def B(a,b,c): return {"type":"box","min":a,"max":b,"color":c}
def R(a,b,d=.03,c='dark'): return {"type":"rod","from":a,"to":b,"dia":d,"color":c}
def P(a,b,d=.07): return {"type":"pipe","from":a,"to":b,"dia":d}
def dump(n,objs,cam,room=None,dims=None,labels=None,**kw):
    s={"style":"real","camera":cam,"objects":objs,"dims":dims or [],"labels":labels or []}
    if room: s["room"]=room
    s.update(kw); json.dump(s,open(n,'w'),ensure_ascii=False)
def car(x,z,c='#3c6fb0'):
    o=[B([x,0.3,z],[x+4.2,0.95,z+1.8],c),B([x+1.0,0.95,z+0.15],[x+3.2,1.45,z+1.65],'#9fb7cf')]
    for dx in (0.8,3.4):
        o.append(R([x+dx,0.32,z-0.02],[x+dx,0.32,z+0.18],.64,'#1f2328')); o.append(R([x+dx,0.32,z+1.62],[x+dx,0.32,z+1.82],.64,'#1f2328'))
    return o
def head(x,y,z,s=2.6,pipe_y=None):
    o=[]
    if pipe_y is not None: o.append(R([x,pipe_y,z],[x,y-0.30*s*0.4,z],.035,'brass'))
    o.append({"type":"head_upright","pos":[x,y,z],"s":s}); return o
H=3.0; py=2.55
# p1 적용 대상: 지하주차장
o=car(0.6,1.2)+car(5.4,1.2,'#b23b32')
for z in (1.0,3.4):
    o.append(P([0,py,z],[10,py,z]))
    for x in (1.2,3.6,6.0,8.4): o+=head(x,2.75,z,2.4,py)
for x in (2.4,7.2): o.append(R([x,py,1.0],[x,H,1.0],.02))
dump('p1.json',o,{"pos":[5,1.7,10.5],"target":[5,1.7,1.5],"fov":46},{"x":[0,10],"y":[0,H],"z":[0,4.5]},
     labels=[{"text":"포헤드(상향식, 형상 단순화)","at":[6.0,2.8,3.4],"dx":40,"dy":-30},{"text":"차고·주차장","at":[2.7,1.5,2.1],"dx":0,"dy":-20,"style":"light"}])
# p2 바닥면적마다 1개
o=[]
for i in range(3):
    for j in range(3):
        cx,cz=0.5+1.5+i*3.0,0.3+1.5+j*3.0
        o.append({"type":"plane","min":[cx-1.45,0.01,cz-1.45],"max":[cx+1.45,0.012,cz+1.45],"color":"#ffe234" if (i,j)==(1,1) else "#2f8be6","opacity":0.35 if (i,j)==(1,1) else 0.12})
        o+=head(cx,2.75,cz,2.4,py)
for j in range(3): o.append(P([0,py,0.3+1.5+j*3.0],[10,py,0.3+1.5+j*3.0]))
d=[{"from":[3.5,0.02,9.6],"to":[6.5,0.02,9.6],"text":"3 m","dx":0,"dy":24},{"from":[6.9,0.02,3.3],"to":[6.9,0.02,6.3],"text":"3 m","dx":34,"dy":0}]
dump('p2.json',o,{"pos":[5,8.5,13.5],"target":[5,0.6,4.8],"fov":44},{"x":[0,10],"y":[0,H],"z":[0,9.6],"ceiling":False,"left":False},d,
     [{"text":"9 ㎡ 예시(3 m × 3 m)","at":[5,0.05,4.8],"dx":0,"dy":40}])
# p3 정방형 간격 S
S=2*2.1*math.cos(math.radians(45)); o=[]
pts=[(2,1.5),(2+S,1.5),(2,1.5+S),(2+S,1.5+S)]
for (x,z) in pts:
    o.append({"type":"pipe","from":[x,0.01,z],"to":[x,0.02,z],"dia":4.2,"color":"#2f8be6","opacity":0.13})
    o+=head(x,1.2,z,2.4)
d=[{"from":[2,1.2,0.9],"to":[2+S,1.2,0.9],"text":"S ≈ 2.97 m","dx":0,"dy":-30}]
o.append(R([2,0.03,1.5],[2+2.1*math.cos(math.radians(45)),0.03,1.5+2.1*math.sin(math.radians(45))],.04,'#c00000'))
dump('p3.json',o,{"pos":[3.5,8.0,9.5],"target":[3.5,0.4,2.6],"fov":46},{"x":[-1,8],"y":[0,3],"z":[-1,6],"ceiling":False,"left":False},d,
     [{"text":"r = 2.1 m","at":[2.6,0.05,2.1],"dx":-60,"dy":20}])
# p4 벽과 거리 S/2
o=[B([0,0,-0.2],[6,3,0],'wall')]
o.append(P([0.3,py,S/2],[6,py,S/2]))
for x in (1.0,1.0+S,1.0+2*S): o+=head(x,2.75,S/2,2.6,py)
d=[{"from":[1.0,2.95,0],"to":[1.0,2.95,S/2],"text":"S/2 이하(≈1.48 m)","dx":90,"dy":-10}]
dump('p4.json',o,{"pos":[5.5,1.6,6.5],"target":[2.6,2.4,0.6],"fov":46},{"x":[0,6],"y":[0,H],"z":[0,4],"left":False},d,
     [{"text":"벽(방호구역 경계)","at":[4.6,1.3,0.0],"dx":0,"dy":0,"style":"light"}])
# p5 보가 있는 부분
o=[{"type":"beam","min":[1.6,2.4,0],"max":[2.2,H,4]}]
o.append(P([0.4,2.3,1.6],[5.2,2.3,1.6]))
o+=head(3.9,2.62,1.6,2.6,2.3)
o.append(R([3.0,2.3,1.6],[3.0,H,1.6],.02))
d=[{"from":[2.2,2.62,1.6],"to":[3.9,2.62,1.6],"text":"수평 1.5 m 이상","dx":0,"dy":-40},
   {"from":[4.4,2.4,1.6],"to":[4.4,2.62,1.6],"text":"수직 0.15~0.3 m 미만","dx":-60,"dy":70,"ext":[[[3.95,2.62,1.6],[4.5,2.62,1.6]],[[2.2,2.4,1.6],[4.5,2.4,1.6]]]}]
dump('p5.json',o,{"pos":[3.4,1.6,7.0],"target":[3.0,2.4,1.6],"fov":40},{"x":[0,6],"y":[0,H],"z":[0,4],"left":False},d,
     [{"text":"보","at":[1.9,2.7,3.0],"dx":-40,"dy":20,"style":"light"}])
# p6 방사량: 포로 덮인 바닥
o=car(1.0,1.0)
o.append({"type":"smoke","pos":[3.0,0.25,1.9],"n":40,"r":0.45,"sx":2.2,"sz":1.4,"seed":7})
o.append(P([0,py,1.9],[6.5,py,1.9]))
for x in (1.2,3.6,6.0): o+=head(x,2.75,1.9,2.4,py)
dump('p6.json',o,{"pos":[3.2,2.0,8.0],"target":[3.2,1.2,1.5],"fov":46},{"x":[0,6.5],"y":[0,H],"z":[0,4]},
     labels=[{"text":"포(거품) 방사 — 개념 표현","at":[4.8,0.6,2.6],"dx":30,"dy":40}])
Pj={"w":1200,"title":"포헤드,","highlight":"몇 ㎡마다 몇 m 간격?","subtitle":"포워터스프링클러헤드 8 ㎡ · 포헤드 9 ㎡ · 유효반경 2.1 m · 벽은 간격의 1/2",
"badge":"포소화설비의 화재안전기술기준(NFTC 105) 2.9.2 · 국립소방연구원공고 제2024-37호(2024. 7. 1. 시행)",
"rows":[
 {"h":360,"panels":[
  {"n":1,"title":"어디에 쓰나 (2.1.1)","span":6,"scene":"p1.json","callout_pos":"overlay",
   "callouts":[{"label":"차고·주차장 · 특수가연물 공장·창고","value":"항공기격납고"}]},
  {"n":2,"title":"바닥면적마다 1개 이상","span":6,"scene":"p2.json","callout_pos":"overlay",
   "callouts":[{"label":"포워터스프링클러헤드","value":"8 ㎡"},{"label":"포헤드","value":"9 ㎡"}]}]},
 {"h":330,"panels":[
  {"n":3,"title":"정방형 배치 간격","span":6,"scene":"p3.json","callout_pos":"overlay",
   "callouts":[{"label":"2.9.2.5.1 S = 2 × r × cos45°","value":"r = 2.1 m"}]},
  {"n":4,"title":"벽·방호구역 경계","span":6,"scene":"p4.json","callout_pos":"overlay",
   "callouts":[{"label":"2.9.2.6 헤드 상호간 거리의","value":"1/2 이하"}]}]},
 {"h":330,"panels":[
  {"n":5,"title":"보가 있는 부분","span":6,"scene":"p5.json","callout_pos":"overlay",
   "callouts":[{"label":"표 2.9.2.4 수평 1.5 m 이상이면 수직","value":"0.15~0.3 m 미만"}]},
  {"n":6,"title":"1분당 방사량 (주차장)","span":6,"scene":"p6.json","callout_pos":"overlay",
   "callouts":[{"label":"표 2.9.2.3 합성계면활성제포, 바닥 1 ㎡당","value":"8.0 L 이상"}]}]}],
"footer":"AI(Claude) 작성 비축척 3D 개념도 · 포헤드 형상은 단순화 · 조문·수치는 국가법령정보센터 원문(2026. 11. 26. 확인), ≈ 값은 원문 식으로 계산한 값 · 생략: 수원·혼합장치·개방밸브·배관 상세"}
json.dump(Pj,open('poster.json','w'),ensure_ascii=False,indent=1)
