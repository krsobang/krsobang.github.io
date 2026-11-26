import json, math
def B(a,b,c): return {"type":"box","min":a,"max":b,"color":c}
def P(a,b,d=.114,c=None):
    o={"type":"pipe","from":a,"to":b,"dia":d}
    if c: o["color"]=c
    return o
def R(a,b,d=.025,c='steel'): return {"type":"rod","from":a,"to":b,"dia":d,"color":c}
def cpl_x(x,y,z,d=.114):  # 그루브 커플링(지진분리이음) 축 x
    return [P([x-.05,y,z],[x+.05,y,z],d*1.4,'dark'),R([x,y-d*.8,z],[x,y+d*.8,z],.022,'dark')]
def cpl_y(x,y,z,d=.114):
    return [P([x,y-.05,z],[x,y+.05,z],d*1.4,'dark'),R([x-d*.8,y,z],[x+d*.8,y,z],.022,'dark')]
YEL='#d9a21b'
def brace4(x,y,z,top,sgn=-1):  # 4방향 버팀대: 횡(z)·종(x) 사선봉 + 클램프
    o=[P([x-.05,y,z],[x+.05,y,z],.16,YEL)]
    h=top-y
    o.append(R([x,y,z],[x,top,z+h],.035,YEL)); o.append(B([x-.08,top-.03,z+h-.08],[x+.08,top,z+h+.08],YEL))
    o.append(R([x,y,z],[x+sgn*h,top,z],.035,YEL)); o.append(B([x+sgn*h-.08,top-.03,z-.08],[x+sgn*h+.08,top,z+.08],YEL))
    return o
def dump(n,s): json.dump(s,open(n,'w'),ensure_ascii=False)

# ---- 건축물 지진분리이음(Exp. J) 교차부 장면 ----
def joint_scene():
    o=[B([0,2.95,0],[3.0,3.2,4],'concrete'),B([3.15,2.95,0],[6.2,3.2,4],'concrete'),
       B([3.0,3.1,0],[3.15,3.2,4],'dark'),B([3.0,0,0],[3.15,2.95,0.06],'dark')]
    y,z=2.45,2.0
    o+= [P([0.3,y,z],[2.6,y,z]),P([3.55,y,z],[5.9,y,z])]
    o+= cpl_x(2.62,y,z)+cpl_x(3.53,y,z)
    o.append({"type":"flex","pts":[[2.67,y,z],[2.76,y,z],[2.84,2.05,z],[3.075,1.8,z],[3.31,2.05,z],[3.39,y,z],[3.48,y,z]],"dia":.1})
    for xx in (0.7,5.5): o.append(R([xx,y,z],[xx,2.95,z]))
    o+= brace4(1.7,y,z,2.95,-1)+brace4(4.45,y,z,2.95,1)
    return o
room={"x":[0,6.2],"y":[0,3.2],"z":[0,4]}
o=joint_scene()
dump('fig1.json',{"w":1600,"h":1000,
 "title":"그림 1. 건축물 지진분리이음과 소화배관이 교차하는 부분 — 지진분리장치와 4방향 버팀대 (비축척 입체 개념도)",
 "note":"원문: 지진분리장치는 구경에 관계없이 건축물 지진분리이음과 소화배관이 교차하는 부분 등에 설치(제8조제1호), 전후좌우 방향 변위 수용(제2호), 전단·후단 1.8 m 이내 4방향 흔들림 방지 버팀대(제3호), 장치 자체에는 버팀대 설치 불가(제4호). 장치 형상(U자 플렉시블 + 커플링)·배관 100A·버팀대 위치는 예시. AI 작성 비축척 — 생략: 반자, 보, 타 설비, 행거 상세.",
 "camera":{"pos":[6.0,1.2,7.6],"target":[3.1,2.2,1.6],"fov":44},
 "room":room,"objects":o,
 "dims":[{"from":[1.7,2.2,2.25],"to":[2.6,2.2,2.25],"text":"1.8 m 이내","dy":60},
         {"from":[3.55,2.2,2.25],"to":[4.45,2.2,2.25],"text":"1.8 m 이내","dy":60}],
 "labels":[{"text":"건축물 지진분리이음 (구조 분리선)","at":[3.075,3.0,0.4],"dx":-330,"dy":-90},
  {"text":"지진분리장치 (커플링·플렉시블 조인트 등 집합체)","at":[3.075,1.8,2.0],"dx":-380,"dy":150,"style":"red"},
  {"text":"4방향 흔들림 방지 버팀대 (전단)","at":[1.7,2.75,2.3],"dx":-260,"dy":-70},
  {"text":"4방향 흔들림 방지 버팀대 (후단)","at":[4.45,2.75,2.3],"dx":80,"dy":-80},
  {"text":"장치 자체에는 버팀대 설치 불가","at":[3.3,2.2,2.0],"dx":300,"dy":240,"style":"red"}]})

base=lambda objs,cam,rm=room:{"style":"real","camera":cam,"objects":objs,"dims":[],"labels":[],"room":rm}
# p1 지진분리이음 확대
o=[P([0.6,1.6,1.6],[2.95,1.6,1.6]),P([3.05,1.6,1.6],[5.4,1.6,1.6])]+cpl_x(3.0,1.6,1.6)
dump('poster/p1.json',base(o,{"pos":[3.9,2.1,2.6],"target":[3.0,1.6,1.6],"fov":36},{"x":[0,6],"y":[0,3],"z":[0,3.2]}))
# p2 지진분리장치 확대
o=[P([0.8,2.0,1.6],[2.6,2.0,1.6]),P([3.55,2.0,1.6],[5.3,2.0,1.6])]+cpl_x(2.62,2.0,1.6)+cpl_x(3.53,2.0,1.6)
o.append({"type":"flex","pts":[[2.67,2,1.6],[2.76,2,1.6],[2.84,1.6,1.6],[3.075,1.35,1.6],[3.31,1.6,1.6],[3.39,2,1.6],[3.48,2,1.6]],"dia":.1})
dump('poster/p2.json',base(o,{"pos":[4.3,2.3,3.4],"target":[3.07,1.75,1.6],"fov":38},{"x":[0,6],"y":[0,3],"z":[0,3.2]}))
# p3 수직직선배관 상·하부 단부 0.6 m 이내 (층 사이 3 m 수직배관)
x,z=1.6,1.4
o=[P([x,0.15,z],[x,2.85,z]),P([x,0.15,z],[x+1.6,0.15,z]),P([x,2.85,z],[x+1.6,2.85,z])]
o+=cpl_y(x,0.55,z,.15)+cpl_y(x,2.45,z,.15)
sp=base(o,{"pos":[2.6,1.5,6.0],"target":[0.7,1.45,1.4],"fov":50},{"x":[0,4],"y":[0,3.0],"z":[0,3]})
sp["dims"]=[{"from":[x+.25,0.15,z],"to":[x+.25,0.75,z],"text":"0.6 m 이내","dx":40},{"from":[x+.25,2.85,z],"to":[x+.25,2.25,z],"text":"0.6 m 이내","dx":40}]
dump('poster/p3.json',sp)
# p4 짧은 수직직선배관 (0.9~2.1 m → 1개)
o=[P([0.6,2.4,z],[1.6,2.4,z]),P([1.6,2.4,z],[1.6,0.9,z]),P([1.6,0.9,z],[3.2,0.9,z])]+cpl_y(1.6,1.65,z)
sp=base(o,{"pos":[4.2,1.9,4.4],"target":[1.8,1.6,1.4],"fov":44},{"x":[0,4],"y":[0,3.0],"z":[0,3]})
sp["dims"]=[{"from":[1.85,0.9,z],"to":[1.85,2.4,z],"text":"0.9~2.1 m","dx":40}]
dump('poster/p4.json',sp)
# p5 지진분리장치 위치 (넓게)
dump('poster/p5.json',base(joint_scene(),{"pos":[5.6,1.7,5.2],"target":[4.0,2.3,1.8],"fov":46}))
# p6 버팀대 확대
o=joint_scene()
sp=base(o,{"pos":[3.9,1.5,5.0],"target":[3.9,2.4,2.0],"fov":46})
sp["dims"]=[{"from":[1.7,2.15,2.2],"to":[2.6,2.15,2.2],"text":"1.8 m 이내","dy":40},{"from":[3.55,2.15,2.2],"to":[4.45,2.15,2.2],"text":"1.8 m 이내","dy":40}]
dump('poster/p6.json',sp)

Pst={"w":1200,"title":"지진분리이음과 지진분리장치,","highlight":"어디에 무엇을?","subtitle":"이음은 축·회전·각도 변위, 장치는 건물 사이 모든 방향 변위",
"badge":"소방시설의 내진설계 기준 제3조제7호·제8호 · 제6조제1항 · 제7조 · 제8조 · 소방청고시 제2026-1호(2026. 3. 1. 시행)",
"rows":[
 {"h":320,"panels":[
   {"n":1,"title":"지진분리이음 (정의)","span":6,"scene":"p1.json","callout_pos":"overlay",
    "callouts":[{"label":"축방향 변위·회전","value":"각도 변위 1° 이상"},{"label":"구경 200 mm 이상","value":"0.5° 이상"}]},
   {"n":2,"title":"지진분리장치 (정의)","span":6,"scene":"p2.json","callout_pos":"overlay",
    "callouts":[{"label":"커플링·플렉시블 조인트 등 집합체","value":"모든 방향 변위 허용"}]}]},
 {"h":330,"panels":[
   {"n":3,"title":"지진분리이음 — 수직직선배관","span":6,"scene":"p3.json","callout_pos":"overlay",
    "callouts":[{"label":"구경 65 mm 이상","value":"상·하부 단부 0.6 m 이내"}]},
   {"n":4,"title":"길이가 짧으면","span":6,"scene":"p4.json","callout_pos":"overlay",
    "callouts":[{"label":"0.9 m 미만","value":"설치 안 할 수 있음"},{"label":"0.9 ~ 2.1 m","value":"하나 설치 가능"}]}]},
 {"h":360,"panels":[{"n":5,"title":"지진분리장치 — 설치 위치 (구경 무관)","span":12,"scene":"p5.json","callout_w":360,"callout_top":30,
   "callouts":[{"label":"제8조제1호 · 제6조제1항제2호","value":"건축물 지진분리이음 교차부"},{"label":"건축물 간 연결배관 중","value":"지상 노출 배관 인입 위치"}]}]},
 {"h":330,"panels":[{"n":6,"title":"장치 앞뒤 버팀대","span":12,"scene":"p6.json","callout_w":360,"callout_top":30,
   "callouts":[{"label":"전단·후단 1.8 m 이내","value":"4방향 흔들림 방지 버팀대"},{"label":"제8조제4호","value":"장치 자체에는 설치 불가"}]}]}],
"footer":"AI(Claude) 작성 비축척 3D 개념도 · 수치는 국가법령정보센터 원문(2026. 11. 27. 확인)에 있는 것만 표시 · 장치 형상은 예시 · 소방 실무 기준 노트"}
json.dump(Pst,open('poster/poster.json','w'),ensure_ascii=False,indent=1)
