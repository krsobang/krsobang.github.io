import json
def B(a,b,c): return {"type":"box","min":a,"max":b,"color":c}
def X(x,z,y=0,**k): d={"type":"extinguisher","pos":[x,y,z]};d.update(k);return d
def dump(n,objs,cam,room=None,dims=None,labels=None):
    s={"style":"real","camera":cam,"objects":objs,"dims":dims or [],"labels":labels or []}
    if room: s["room"]=room
    json.dump(s,open(n,'w'),ensure_ascii=False)
RM={"x":[0,6],"y":[0,3.0],"z":[0,5]}
RN={"x":[0,6],"y":[0,3.0],"z":[0,5],"ceiling":False}
# p1 높이 1.5 m 이하 + 표지
o=[B([1.55,0.2,0],[2.05,0.25,0.25],'#5d6670'),X(1.8,0.13,0.25,s=1.5),
   {"type":"sign","pos":[1.8,2.15,0.0],"text":"소화기","bg":"#f4f1e4","fg":"#c62f28","w":0.5,"h":0.24}]
dims=[{"from":[2.5,0,0.15],"to":[2.5,1.5,0.15],"text":"1.5 m 이하","dx":70,"ext":[[[1.3,1.5,0.15],[2.6,1.5,0.15]]]}]
dump('p1.json',o,{"pos":[4.2,1.5,4.2],"target":[1.9,1.0,0.3],"fov":44},RM,dims)
# p2 보행거리 — 벽을 돌아가는 동선
o=[B([2.2,0,0],[2.35,3.0,3.0],'#e8e3d6'),X(0.8,0.25,s=1.2),{"type":"sphere","pos":[4.4,0.05,0.8],"r":0.09,"color":"#1f3150"}]
for a,b in [([4.4,0.8],[4.4,3.6]),([4.4,3.6],[0.8,3.6]),([0.8,3.6],[0.8,0.6])]:
    o.append(B([min(a[0],b[0])-0.04,0.005,min(a[1],b[1])-0.04],[max(a[0],b[0])+0.04,0.016,max(a[1],b[1])+0.04],'#c62f28'))
dims=[]
lb=[{"text":"보행거리(벽을 돌아 걷는 길)","at":[4.4,0.02,2.4],"dx":-30,"dy":-150,"style":"red"},{"text":"각 부분","at":[4.4,0.1,0.8],"dx":50,"dy":-30}]
dump('p2.json',o,{"pos":[3.0,6.5,7.6],"target":[2.6,0.3,1.8],"fov":44},RN,dims,lb)
# p3 33 ㎡ 이상 구획 거실
o=[B([2.6,0,0],[2.72,3.0,4.2],'#e8e3d6'),{"type":"door","pos":[2.72,0,3.0],"w":0.9},X(1.2,0.25,s=1.1),X(4.2,0.25,s=1.1)]
o[1]={"type":"box","min":[2.72,0,2.55],"max":[2.77,2.1,3.45],"color":"door"}
lb=[{"text":"구획된 거실(33 ㎡ 이상) 안 소화기","at":[1.2,0.6,0.25],"dx":-20,"dy":110},{"text":"복도 쪽 소화기","at":[4.2,0.6,0.25],"dx":40,"dy":110}]
dump('p3.json',o,{"pos":[2.7,4.8,7.6],"target":[2.7,0.4,1.6],"fov":44},RN,None,lb)
# p4 지시압력계
o=[X(0.7,0.35,s=1.6,gauge="green"),X(1.55,0.35,s=1.6,gauge="low")]
lb=[{"text":"정상(녹색)","at":[0.79,1.08,0.5],"dx":-90,"dy":-30},{"text":"압력 미달","at":[1.64,1.08,0.5],"dx":80,"dy":-30,"style":"red"}]
dump('p4.json',o,{"pos":[1.15,1.3,3.0],"target":[1.15,0.75,0.35],"fov":40},{"x":[-1,3],"y":[0,2.6],"z":[0,3]},None,lb)
# p5 내용연수
o=[X(0.9,0.35,s=1.5,label="분말")]
dump('p5.json',o,{"pos":[1.5,1.2,2.8],"target":[1.25,0.6,0.35],"fov":40},{"x":[-1,3],"y":[0,2.6],"z":[0,3]})
# p6 종합점검 — 수량·적응성
o=[X(0.8,0.3,s=1.1,label="분말"),X(1.4,0.3,s=1.1,label="분말"),X(2.4,0.3,s=1.1,label="CO₂",color="#2b2f36"),
   {"type":"sign","pos":[2.4,1.6,0.0],"text":"사무실","bg":"#ffffff","fg":"#1f2a36","w":0.6,"h":0.22}]
lb=[{"text":"사무실에 이산화탄소 소화기(불량 예)","at":[2.4,0.55,0.4],"dx":60,"dy":-60,"style":"red"}]
dump('p6.json',o,{"pos":[1.4,1.5,3.6],"target":[1.7,0.7,0.3],"fov":42},{"x":[0,4],"y":[0,2.8],"z":[0,4]},None,lb)
P={"w":1200,"title":"소화기 점검,","highlight":"10개 항목","subtitle":"매뉴얼 점검표 1-A-001~010 — 작동점검 8개 + 종합점검만(●) 2개",
"badge":"소방청 「소방시설등 점검관리 매뉴얼」(2025. 9.) 1권 제1절 · 자체점검사항 고시 별지 제4호 · NFTC 101 2.1.1",
"rows":[
 {"h":380,"panels":[
  {"n":1,"title":"높이·표지","span":6,"scene":"p1.json","callout_pos":"overlay",
   "callouts":[{"label":"1-A-002","value":"바닥에서 1.5 m 이하"},{"label":"1-A-005 주차장 표지","value":"1.5 m 이상"}]},
  {"n":2,"title":"배치거리","span":6,"scene":"p2.json","callout_pos":"overlay",
   "callouts":[{"label":"1-A-003 보행거리","value":"소형 20 m · 대형 30 m"}]}]},
 {"h":340,"panels":[
  {"n":3,"title":"구획된 거실","span":6,"scene":"p3.json","callout_pos":"overlay",
   "callouts":[{"label":"1-A-004","value":"33 ㎡ 이상 거실마다"}]},
  {"n":4,"title":"지시압력계","span":6,"scene":"p4.json","callout_pos":"overlay",
   "callouts":[{"label":"1-A-007 (매뉴얼 설명)","value":"녹색 0.7~0.98 MPa"}]}]},
 {"h":320,"panels":[
  {"n":5,"title":"분말 내용연수","span":6,"scene":"p5.json","callout_w":290,"callout_top":40,
   "callouts":[{"label":"1-A-008 (시행령 제19조)","value":"10년"},{"label":"성능확인 합격 시 (품질관리규칙 제2조의2⑥)","value":"3년 / 1년 연장"}]},
  {"n":6,"title":"● 종합점검만","span":6,"scene":"p6.json","callout_pos":"overlay",
   "callouts":[{"label":"1-A-009","value":"설치수량"},{"label":"1-A-010","value":"적응성"}]}]}],
"footer":"AI(Claude) 작성 비축척 3D 개념도 · 문구·수치는 매뉴얼·국가법령정보센터 원문(2026. 11. 20. 확인)에 있는 것만 · 소방 실무 기준 노트"}
json.dump(P,open('poster.json','w'),ensure_ascii=False,indent=1)
