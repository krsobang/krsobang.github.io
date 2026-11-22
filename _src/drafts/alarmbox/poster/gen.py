import json
def B(a,b,c): return {"type":"box","min":a,"max":b,"color":c}
def R(a,b,d=.03,c='dark'): return {"type":"rod","from":a,"to":b,"dia":d,"color":c}
def dump(n,objs,cam,room=None,dims=None,labels=None,**kw):
    s={"style":"real","camera":cam,"objects":objs,"dims":dims or [],"labels":labels or []}
    if room: s["room"]=room
    s.update(kw); json.dump(s,open(n,'w'),ensure_ascii=False)
AB=lambda x,y,z,**k: dict({"type":"alarm_box","pos":[x,y,z]},**k)
# p1: 적용 대상 — 3개 층 단면(지하 1층 포함), 층마다 발신기함
o=[]
for y in (-3.2,0,3.2,6.4): o.append(B([-0.3,y-0.25,-0.3],[7.3,y,2.4],'slab'))
o.append(B([-0.3,-3.45,-0.3],[7.3,6.4,-0.05],'wall'))
o.append(B([-3,-0.25,-0.3],[-0.3,0,4],'#7d8a6f'))  # 지반선
o.append(B([-3,-3.45,-0.3],[-0.3,-0.25,4],'#8a7a5f'))
for y in (-3.2,0,3.2): o.append(AB(5.6,y+1.0,-0.05,s=2.2))
for y in (-3.2,0,3.2): o.append(B([1.0,y,0.3],[2.2,y+0.8,1.1],'#9aa3ab'))
lb=[{"text":"지하층","at":[0.9,-1.4,1.5],"dx":0,"dy":0},{"text":"1층","at":[0.9,1.8,1.5],"dx":0,"dy":0},{"text":"2층","at":[0.9,5.0,1.5],"dx":0,"dy":0}]
dump('p1.json',o,{"pos":[6.3,1.8,15.5],"target":[6.3,1.6,0],"fov":40},labels=lb)
# p2: 조작스위치 높이 0.8~1.5 m — 벽면 발신기함 (s=1 실제 크기)
o=[AB(1.5,0.95,0)]
o.append({"type":"plane","min":[0.9,0.8,0.02],"max":[2.1,1.5,0.03],"color":"#ffe234","opacity":0.28})
d=[{"from":[2.35,0,0.2],"to":[2.35,0.8,0.2],"text":"0.8 m","dx":38,"dy":0},
   {"from":[2.75,0,0.2],"to":[2.75,1.5,0.2],"text":"1.5 m","dx":38,"dy":-30}]
dump('p2.json',o,{"pos":[1.9,1.0,4.2],"target":[1.9,0.95,0],"fov":42},{"x":[0,4],"y":[0,2.6],"z":[0,3]},d,
     [{"text":"조작스위치","at":[1.5,0.95+0.62*0.14,0.15],"dx":-120,"dy":10}])
# p3: 수평거리 25 m — 층 바닥 위 반경 표시(비축척 반경 4)
o=[AB(0,1.0,0,s=2.6)]
o.append({"type":"pipe","from":[0,0.015,0],"to":[0,0.03,0],"dia":8.4,"color":"#2f8be6","opacity":0.3})
o.append(R([0,0.04,0.0],[2.97,0.04,2.97],.05,'#c00000'))
dump('p3.json',o,{"pos":[0,7.0,9.0],"target":[0,0.3,1.8],"fov":46},{"x":[-6,6],"y":[0,3],"z":[0,6],"ceiling":False,"left":False},labels=[{"text":"수평거리 25 m 이하","at":[1.6,0.1,1.6],"dx":30,"dy":-20}])
# p4: 복도 보행거리 40 m 이상 → 추가
o=[]
o.append(B([0,0,2.0],[12,0.35,2.15],'wall'))
o.append(AB(1.0,1.0,0.0,s=1.8)); o.append(AB(10.5,1.0,0.0,s=1.8))
o.append(R([1.0,0.03,0.9],[10.5,0.03,0.9],.06,'#c00000'))
dump('p4.json',o,{"pos":[6.0,5.0,9.0],"target":[5.8,0.8,0.8],"fov":44},{"x":[0,12],"y":[0,2.8],"z":[0,2.15],"ceiling":False,"left":False},floor_color='#6f8f80',
     labels=[{"text":"보행거리 40 m 이상","at":[5.8,0.05,0.9],"dx":0,"dy":30},{"text":"추가 발신기","at":[10.5,2.2,0.2],"dx":0,"dy":-10}])
# p5: 위치표시등 — 15° 이상 범위, 10 m 이내 식별
import math
o=[AB(0.6,0.95,0,s=1.4)]
ly=0.95+0.62*0.85*1.4; lz=0.11*1.4+0.02
L=4.0; a=math.radians(15)
o.append(R([0.6,ly,lz],[0.6+L,ly,lz],.03,'#c00000'))
o.append(R([0.6,ly,lz],[0.6+L*math.cos(a),ly,lz+L*math.sin(a)],.03,'#c00000'))
o.append({"type":"plane","min":[0.6,ly-0.01,lz],"max":[0.6+L,ly,lz+L*math.sin(a)],"color":"#ffe234","opacity":0.35})
d=[{"from":[0.6,ly,lz+1.6],"to":[0.6+L,ly,lz+1.6],"text":"10 m 이내(비축척)","dx":0,"dy":-22}]
dump('p5.json',o,{"pos":[2.6,6.0,4.2],"target":[2.4,1.2,0.6],"fov":44},{"x":[-0.5,5],"y":[0,2.8],"z":[0,3],"ceiling":False,"left":False},dims=d,
     labels=[{"text":"부착면(벽)","at":[3.8,2.4,0.0],"dx":0,"dy":0},{"text":"15° 이상","at":[3.9,ly,lz+0.5],"dx":40,"dy":10}])
# p6: 지구음향장치 — 1 m에서 90 dB
o=[B([-0.2,0,-0.15],[3.5,2.8,0],'wall'),AB(0.8,0.95,0,s=1.4)]
by=0.95+0.62*0.56*1.4; bz=0.11*1.4+0.02
d=[{"from":[0.8,by,bz+0.15],"to":[2.6,by,bz+0.15],"text":"1 m","dx":0,"dy":-22}]
o.append({"type":"sphere","pos":[2.75,by,bz+0.15],"r":0.12,"color":"#2f8be6"})
dump('p6.json',o,{"pos":[1.9,1.9,4.8],"target":[1.6,1.6,0.2],"fov":44},dims=d,labels=[{"text":"측정 위치","at":[2.75,by,bz+0.15],"dx":0,"dy":34}])
P={"w":1200,"title":"발신기,","highlight":"어디에 몇 높이로?","subtitle":"층마다 · 수평거리 25 m · 스위치 0.8~1.5 m · 위치표시등은 함 상부 적색등",
"badge":"비상경보설비 및 단독경보형감지기의 화재안전기술기준(NFTC 201) 2.1.5 · 소방청공고 제2022-222호(2022. 12. 1. 시행)",
"rows":[
 {"h":380,"panels":[
  {"n":1,"title":"설치 대상 확인","span":6,"scene":"p1.json","callout_w":240,"callout_top":50,
   "callouts":[{"label":"시행령 별표 4 제2호나목 연면적","value":"400 ㎡ 이상"},{"label":"지하층·무창층 바닥면적","value":"150 ㎡ 이상"},{"label":"(공연장 100 ㎡)"}]},
  {"n":2,"title":"조작스위치 높이","span":6,"scene":"p2.json","callout_pos":"overlay",
   "callouts":[{"label":"2.1.5.1 바닥으로부터","value":"0.8~1.5 m"}]}]},
 {"h":330,"panels":[
  {"n":3,"title":"층마다 · 수평거리","span":6,"scene":"p3.json","callout_pos":"overlay",
   "callouts":[{"label":"2.1.5.2 각 부분에서","value":"25 m 이하"}]},
  {"n":4,"title":"복도·구획된 실","span":6,"scene":"p4.json","callout_pos":"overlay",
   "callouts":[{"label":"2.1.5.2 단서 보행거리","value":"40 m 이상 → 추가"}]}]},
 {"h":330,"panels":[
  {"n":5,"title":"위치표시등","span":6,"scene":"p5.json","callout_pos":"overlay",
   "callouts":[{"label":"2.1.5.3 함 상부 적색등","value":"15° · 10 m"}]},
  {"n":6,"title":"같은 함의 경종(음향장치)","span":6,"scene":"p6.json","callout_pos":"overlay",
   "callouts":[{"label":"2.1.4 중심에서 1 m","value":"90 dB 이상"}]}]}],
"footer":"AI(Claude) 작성 비축척 3D 개념도 · 조문·수치는 국가법령정보센터 원문(2026. 11. 23. 확인)에 있는 것만 표시 · 생략: 수신기·배선·전원 · 소방 실무 기준 노트"}
json.dump(P,open('poster.json','w'),ensure_ascii=False,indent=1)
