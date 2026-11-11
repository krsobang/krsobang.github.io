import json
CON='#9fa5ad'; FR='#3b4652'; MOT='#2f6db5'; PUMP='#c0392b'; SPR='#6b8fb8'; ST='#e3a21a'
def B(a,b,c): return {"type":"box","min":a,"max":b,"color":c}
def P(a,b,d,c=None):
    o={"type":"pipe","from":a,"to":b,"dia":d}
    if c: o["color"]=c
    return o
objs=[]
# pad & base frame
objs.append(B([1.4,0,1.1],[4.7,0.15,2.7],CON))
objs.append(B([1.7,0.30,1.45],[4.3,0.40,2.35],FR))
# springs (isolators)
for x in (1.85,4.15):
    for z in (1.6,2.2):
        objs.append(P([x,0.15,z],[x,0.30,z],0.11,SPR))
# motor, coupling, pump
objs.append(P([1.95,0.64,1.9],[2.95,0.64,1.9],0.46,MOT))
objs.append(B([2.05,0.40,1.75],[2.85,0.43,2.05],FR))
objs.append(P([2.95,0.64,1.9],[3.15,0.64,1.9],0.08,'steel'))
objs.append(P([3.15,0.64,1.9],[3.55,0.64,1.9],0.52,PUMP))
objs.append(B([3.2,0.40,1.8],[3.5,0.43,2.0],FR))
# suction (axial, +x) with flex
objs.append(P([3.55,0.64,1.9],[3.75,0.64,1.9],0.2))
objs.append({"type":"flex","pts":[[3.75,0.64,1.9],[3.95,0.64,1.9],[4.15,0.64,1.9]],"dia":0.21})
objs.append(P([4.15,0.64,1.9],[5.9,0.64,1.9],0.2))
# discharge (up) with flex
objs.append(P([3.35,0.9,1.9],[3.35,1.05,1.9],0.16))
objs.append({"type":"flex","pts":[[3.35,1.05,1.9],[3.35,1.25,1.9],[3.35,1.45,1.9]],"dia":0.17})
objs.append(P([3.35,1.45,1.9],[3.35,2.4,1.9],0.16))
objs.append({"type":"sphere","pos":[3.35,2.4,1.9],"r":0.09})
objs.append(P([3.35,2.4,1.9],[3.35,2.4,0.05],0.16))
# stoppers: (foot plate + upright) around base, gap 0.05 (exaggerated)
def stop_x(x0,x1,z):  # stopper facing base end in x
    objs.append(B([x0,0.15,z-0.12],[x1,0.18,z+0.12],ST)); 
def stoppers():
    # ends (x)
    for (fx0,fx1,ux0,ux1) in ((1.45,1.65,1.6,1.65),(4.35,4.55,4.35,4.4)):
        for z in (1.9,):
            objs.append(B([fx0,0.15,z-0.12],[fx1,0.18,z+0.12],ST))
            objs.append(B([ux0,0.18,z-0.12],[ux1,0.45,z+0.12],ST))
            for zz in (z-0.08,z+0.08):
                bx=(fx0+ux0)/2 if fx0<ux0 else (fx1+ux1)/2
                bx = fx0+0.04 if fx0<1.5 else fx1-0.04
                objs.append({"type":"rod","from":[bx,0.15,zz],"to":[bx,0.22,zz],"dia":0.025,"color":"dark"})
    # sides (z)
    for x in (2.4,3.7):
        for (fz0,fz1,uz0,uz1) in ((1.15,1.35,1.35,1.40),(2.45,2.65,2.40,2.45)):
            objs.append(B([x-0.12,0.15,fz0],[x+0.12,0.18,fz1],ST))
            objs.append(B([x-0.12,0.18,uz0],[x+0.12,0.45,uz1],ST))
            bz = fz0+0.05 if fz0<1.3 else fz1-0.05
            for xx in (x-0.08,x+0.08):
                objs.append({"type":"rod","from":[xx,0.15,bz],"to":[xx,0.22,bz],"dia":0.025,"color":"dark"})
stoppers()
spec={"w":1600,"h":1000,"title":"그림 1. 방진장치 위 가압송수장치 — 내진스토퍼와 가요성이음장치 (비축척 입체 개념도)",
 "note":"방진장치(스프링) 때문에 앵커볼트로 직접 고정할 수 없는 경우의 예(제5조제1항). 스토퍼와 본체 사이 틈은 보이도록 크게 그렸습니다. AI 작성 비축척 — 생략: 밸브류·압력계·제어반·배관 지지대, 스토퍼·방진장치 제품 형상, 앵커 상세.",
 "camera":{"pos":[7.4,3.0,6.6],"target":[3.0,0.6,1.8],"fov":38},
 "room":{"x":[0,6],"y":[0,3.0],"z":[0,4],"ceiling":False},
 "objects":objs,
 "labels":[
  {"text":"가압송수장치(펌프)","at":[3.35,0.85,2.1],"dx":120,"dy":-260},
  {"text":"전동기","at":[2.3,0.85,1.95],"dx":-250,"dy":-70},
  {"text":"내진스토퍼 (본체와 3 mm 이상 이격)","at":[4.38,0.42,1.9],"dx":170,"dy":-60,"style":"red"},
  {"text":"내진스토퍼","at":[2.4,0.40,2.43],"dx":-250,"dy":-80,"style":"red"},
  {"text":"방진장치 (스프링)","at":[4.15,0.22,2.2],"dx":150,"dy":110},
  {"text":"가요성이음장치 — 흡입측","at":[3.95,0.64,1.9],"dx":200,"dy":-170,"style":"red"},
  {"text":"가요성이음장치 — 토출측","at":[3.35,1.25,1.9],"dx":-260,"dy":-110,"style":"red"},
  {"text":"기초(패드) — 구조안전성 확인","at":[1.6,0.1,2.6],"dx":-200,"dy":30,"style":"light"},
  {"text":"앵커볼트","at":[2.32,0.2,2.6],"dx":-250,"dy":150}
 ]}
json.dump(spec,open('fig1.json','w'),ensure_ascii=False)
