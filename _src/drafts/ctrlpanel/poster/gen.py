import json
def B(a,b,c): return {"type":"box","min":a,"max":b,"color":c}
def R(a,b,d=.03,c='dark'): return {"type":"rod","from":a,"to":b,"dia":d,"color":c}
def dump(n,objs,cam,room=None,dims=None):
    s={"style":"real","camera":cam,"objects":objs,"dims":dims or [],"labels":[]}
    if room: s["room"]=room
    json.dump(s,open(n,'w'),ensure_ascii=False)
def wallbox(x0,y0,w,h,d=0.16,col='#d9dcd6',bolts=True):
    o=[B([x0,y0,0],[x0+w,y0+h,d],col),B([x0+0.04,y0+0.04,d],[x0+w-0.04,y0+h-0.04,d+0.012],'#e9ebe6'),
       B([x0+0.12,y0+h-0.25,d+0.012],[x0+w-0.12,y0+h-0.1,d+0.02],'#20262c')]
    for i,c in enumerate(['#e0443a','#3cc35b','#f2c230']):
        o.append({"type":"sphere","pos":[x0+0.15+i*0.1,y0+h-0.36,d+0.02],"r":0.018,"color":c})
    if bolts:
        for x in (x0+0.06,x0+w-0.06):
            for y in (y0+0.06,y0+h-0.06):
                o+= [R([x,y,-0.06],[x,y,d+0.03],.03,'steel'),{"type":"sphere","pos":[x,y,d+0.03],"r":0.02,"color":"steel"}]
    return o
# p1: 대상 — 감시제어반·동력제어반(바닥) + 수신기(벽)
o=[{"type":"control_panel","pos":[3.6,0,0.42]},{"type":"control_panel","pos":[5.0,0,0.42],"color":"#c9cfd6"}]
o+=wallbox(1.4,1.0,0.7,0.9)
dump('p1.json',o,{"pos":[6.6,1.7,5.2],"target":[3.0,1.1,0.4],"fov":44},{"x":[0,7],"y":[0,3.0],"z":[0,4]})
# p2: 고정 부재 — 기둥(구조부재)에 부착한 반, 옆 칸막이벽
o=[B([2.0,0,0],[2.6,3.0,0.6],'concrete')]
o+=[B([2.6,0,0.15],[5.5,3.0,0.25],'#e8e3d6')]  # 경량 칸막이벽(비구조) 예
o+=[B([2.0+0.0,1.0,0.6],[2.6,1.9,0.76],'#d9dcd6'),B([2.04,1.04,0.76],[2.56,1.86,0.772],'#e9ebe6')]
for x in (2.06,2.54):
    for y in (1.06,1.84): o+=[R([x,y,0.5],[x,y,0.79],.03,'steel')]
dump('p2.json',o,{"pos":[4.6,1.8,3.6],"target":[2.6,1.3,0.4],"fov":44},{"x":[0,6],"y":[0,3.0],"z":[0,4],"left":False})
# p3: 지진하중 → 앵커 — 바닥 반 앵커 확대
o=[B([0,0,0],[3,0.0,3],'concrete'),{"type":"control_panel","pos":[1.5,0,1.2],"w":0.9,"d":0.5}]
for x in (1.0,2.0):
    for z in (0.92,1.48): o+=[R([x,-0.02,z],[x,0.16,z],.04),B([x-0.05,0.1,z-0.05],[x+0.05,0.13,z+0.05],'#222831')]
dump('p3.json',o,{"pos":[4.0,2.0,4.6],"target":[1.5,0.85,1.2],"fov":44})
# p4: 450 N 단서 — 내력벽에 볼트 4개
o=wallbox(0.9,0.9,0.8,0.95)
dump('p4.json',o,{"pos":[2.5,1.6,2.3],"target":[1.3,1.35,0.1],"fov":40},{"x":[0,3],"y":[0,2.6],"z":[0,3]})
# p5: 바닥 설치 — 기초 패드 + 전도 방지
o=[B([0.6,0,0.3],[2.6,0.15,1.2],'concrete'),{"type":"control_panel","pos":[1.6,0.15,0.75],"w":1.5,"d":0.5}]
for x in (0.9,2.3):
    for z in (0.52,0.98): o.append(R([x,0.05,z],[x,0.3,z],.04))
dump('p5.json',o,{"pos":[5.0,2.0,4.6],"target":[1.4,0.9,0.7],"fov":44},{"x":[-1,5],"y":[0,3],"z":[-1,4],"left":False})
# p6: 기능 유지 — 가스계 제어반(벽) + 저장용기
o=wallbox(0.6,1.0,0.6,0.8)
for i in range(4):
    x=2.0+i*0.38
    o+=[{"type":"pipe","from":[x,0,0.45],"to":[x,1.45,0.45],"dia":0.27,"color":"#c62f28"},{"type":"pipe","from":[x,1.45,0.45],"to":[x,1.6,0.45],"dia":0.08,"color":"steel"}]
o.append(B([1.75,1.1,0.2],[3.45,1.16,0.7],'#3b4652'))
dump('p6.json',o,{"pos":[4.6,1.7,3.8],"target":[2.0,1.0,0.3],"fov":42},{"x":[0,5],"y":[0,3],"z":[0,4]})
P={"w":1200,"title":"수신기·제어반도","highlight":"내진 대상","subtitle":"구조부재에 고정하고, 넘어지지 않게, 지진 뒤에도 작동하게",
"badge":"소방시설의 내진설계 기준 제14조 · 제3조제25호 · 제3조의2 · 소방청고시 제2026-1호(2026. 3. 1. 시행)",
"rows":[
 {"h":400,"panels":[{"n":1,"title":"제어반등이 뭔가요","span":12,"scene":"p1.json","callout_w":300,"callout_top":50,
   "callouts":[{"label":"제3조제25호","value":"수신기(중계반 포함)"},{"label":"","value":"동력제어반 · 감시제어반 등"}],
   "tags":[{"text":"수신기(벽)","x":0.4,"y":0.3},{"text":"감시제어반","x":0.52,"y":0.22},{"text":"동력제어반","x":0.66,"y":0.22}]}]},
 {"h":340,"panels":[
   {"n":2,"title":"어디에 고정","span":6,"scene":"p2.json","callout_pos":"overlay",
    "callouts":[{"label":"구조부재인","value":"내력벽·바닥·기둥 등"}],
    "tags":[{"text":"기둥","x":0.3,"y":0.75},{"text":"칸막이벽(예)","x":0.7,"y":0.6}]},
   {"n":3,"title":"하중 계산 → 앵커","span":6,"scene":"p3.json","callout_pos":"overlay",
    "callouts":[{"label":"지진하중","value":"제3조의2제2항"},{"label":"앵커볼트","value":"제3조의2제3항"}]}]},
 {"h":330,"panels":[
   {"n":4,"title":"450 N 단서","span":6,"scene":"p4.json","callout_w":230,"callout_top":40,
    "callouts":[{"label":"하중 450 N 이하 + 내력벽·기둥","value":"Ø8 mm↑ 볼트 4개↑"}]},
   {"n":5,"title":"바닥에 세우면","span":6,"scene":"p5.json","callout_pos":"overlay",
    "callouts":[{"label":"지진하중에 의해","value":"전도 없게"},{"label":"기초(패드) 구조안전성 확인 (제3조의2제4항)"}],
    "tags":[{"text":"기초 패드","x":0.62,"y":0.9}]}]},
 {"h":300,"panels":[{"n":6,"title":"지진 뒤에도 작동","span":12,"scene":"p6.json","callout_w":320,"callout_top":40,
   "callouts":[{"label":"제14조제3호","value":"기능 유지"},{"label":"가스계·분말 제어반등","value":"제14조 적용 (제18조②)"}],
   "tags":[{"text":"가스계 제어반","x":0.42,"y":0.3},{"text":"저장용기","x":0.55,"y":0.35}]}]}],
"footer":"AI(Claude) 작성 비축척 3D 개념도 · 수치는 국가법령정보센터 원문(2026. 11. 19. 확인)에 있는 것만 표시 · 소방 실무 기준 노트"}
json.dump(P,open('poster.json','w'),ensure_ascii=False,indent=1)
