import json
def B(a,b,c): return {"type":"box","min":a,"max":b,"color":c}
def P(a,b,d=.12,c=None):
    o={"type":"pipe","from":a,"to":b,"dia":d}
    if c: o["color"]=c
    return o
def dump(n,objs,cam,room=None,dims=None,labels=None):
    s={"style":"real","camera":cam,"objects":objs,"dims":dims or [],"labels":labels or []}
    if room: s["room"]=room
    json.dump(s,open(n,'w'),ensure_ascii=False)
SL='#b9c2cc'
# p1: 설비별 펌프·급수배관 분리
o=[{"type":"pump_set","pos":[0.4,0,1.0],"l":2.2},{"type":"pump_set","pos":[0.4,0,2.9],"l":2.2}]
for z in (1.0,2.9):
    o.append(P([1.95,1.04,z],[1.95,2.6,z],.16))
o.append({"type":"sign","pos":[1.2,1.45,0.0],"text":"옥내소화전 펌프","bg":"#ffffff","fg":"#c62f28","w":1.0,"h":0.26})
lb=[{"text":"옥내소화전 펌프·배관","at":[1.95,2.3,1.0],"dx":110,"dy":10,"style":"red"},{"text":"스프링클러 펌프·배관","at":[1.95,1.5,2.9],"dx":170,"dy":70,"style":"red"}]
o.pop()
dump('p1.json',o,{"pos":[6.2,2.4,5.6],"target":[1.6,0.9,2.0],"fov":44},{"x":[0,5],"y":[0,3],"z":[0,4.2],"ceiling":False},None,lb)
# p2: 수직배관 2개 + 각각 유수검지장치
o=[]
for y in (0,1.6,3.2,4.8): o.append(B([0,y-0.2,0],[4,y,2.4],SL))
for x in (1.2,2.8):
    o.append(P([x,-0.2,1.2],[x,4.8,1.2],.16))
    o.append(B([x-0.17,0.35,1.03],[x+0.17,0.8,1.37],'#c62f28'))
o.append(P([1.2,4.0,1.2],[2.8,4.0,1.2],.1))
lb=[{"text":"수직배관 ①","at":[1.2,2.6,1.3],"dx":-90,"dy":-20,"style":"red"},{"text":"수직배관 ②","at":[2.8,2.6,1.3],"dx":40,"dy":-20,"style":"red"},
    {"text":"각각 유수검지장치","at":[2.8,0.6,1.37],"dx":50,"dy":30}]
dump('p2.json',o,{"pos":[2.0,2.6,7.4],"target":[2.0,2.2,1.2],"fov":46},{"x":[-0.5,4.5],"y":[-0.2,5],"z":[0,3],"ceiling":False},None,lb)
# p3: 수원 (지하 수조)
o=[{"type":"tank","pos":[0.6,0,0.6],"w":3.0,"d":1.8,"h":2.0},{"type":"pump_set","pos":[0.8,0,3.4],"l":2.2}]
o.append(P([3.0,0.5,2.4],[3.0,0.5,3.4],.14))
dump('p3.json',o,{"pos":[7.0,2.8,6.6],"target":[2.2,1.0,2.0],"fov":42},{"x":[0,5],"y":[0,3],"z":[0,4.5]},None,
  [{"text":"소화수조(수원)","at":[1.6,2.0,2.4],"dx":-60,"dy":-40}])
# p4: 옥상수조 1/3
o=[B([0,0,0],[5,0.25,4],SL),B([0,-3,0.2],[0.25,0,3.8],'#d9d4c7'),{"type":"tank","pos":[1.2,0.25,0.8],"w":2.2,"d":1.6,"h":1.4}]
o.append(P([2.3,0.4,2.6],[2.3,0.4,3.4],.12)); o.append(P([2.3,0.4,3.4],[2.3,-2.8,3.4],.12))
dump('p4.json',o,{"pos":[6.6,2.2,7.2],"target":[2.3,0.6,2.0],"fov":42},{"x":[0,5.5],"y":[-3,3],"z":[0,4.5],"ceiling":False},None,
  [{"text":"옥상수조","at":[2.3,1.7,2.4],"dx":-40,"dy":-40}])
PS={"w":1200,"title":"고층 수계설비,","highlight":"4가지 강화","subtitle":"건축위원회(심의) 표준 가이드라인 Ⅱ-5~8 항목",
"badge":"소방청 「건축위원회(심의) 표준 가이드라인」(2023. 12.) · 대조: NFTC 604(제2023-44호) · NFTC 102(제2026-34호)",
"rows":[
 {"h":340,"panels":[
  {"n":1,"title":"펌프·급수배관 분리","span":6,"scene":"p1.json","callout_pos":"overlay",
   "callouts":[{"label":"가이드라인 Ⅱ-5","value":"설비별 분리"},{"label":"NFTC 604 2.1.3·2.2.3","value":"고층은 설비 전용"}]},
  {"n":2,"title":"수직배관 이중화","span":6,"scene":"p2.json","callout_pos":"overlay",
   "callouts":[{"label":"NFTC 604 2.1.6·2.2.6 (50층 이상)","value":"수직배관 2개 이상"}]}]},
 {"h":330,"panels":[
  {"n":3,"title":"수원·작동시간","span":6,"scene":"p3.json","callout_pos":"overlay",
   "callouts":[{"label":"NFTC 604 2.1.1 (50층 이상 7.8 ㎥)","value":"개수 × 5.2 ㎥"},{"label":"가이드라인 Ⅱ-7","value":"20 / 40 / 60분"}]},
  {"n":4,"title":"옥상수조","span":6,"scene":"p4.json","callout_pos":"overlay",
   "callouts":[{"label":"유효수량 외에 (NFTC 604 2.1.2·2.2.2)","value":"3분의 1 이상"}]}]}],
"footer":"AI(Claude) 작성 비축척 3D 개념도 · 문구·수치는 가이드라인 PDF·국가법령정보센터 원문(2026. 11. 25. 확인)에 있는 것만 · 생략: 밸브류·제어반·바이패스 배관 상세, 수조 연결배관"}
json.dump(PS,open('poster.json','w'),ensure_ascii=False,indent=1)
