import json
CON='#8f9aa6'; NB='#aeb8c3'; WOOD='#c9a66b'
objs=[];dims=[];labels=[]
panels=[(0.4,1.4,CON,NB,'2 m 미만','① 2.12.1.5.1','천장: 불연재료','반자: 불연재료'),
        (4.0,0.8,CON,WOOD,'1 m 미만','② 2.12.1.6','천장: 불연재료','반자: 불연재료 외'),
        (7.6,0.45,WOOD,WOOD,'0.5 m 미만','③ 2.12.1.7','천장: 불연재료 외','반자: 불연재료 외')]
W=3.0; RB=2.6; T=0.05; z=1.0
for x0,gap,cc,bc,dt,tag,tl,bl in panels:
    x1=x0+W; top=RB+T
    objs.append({"type":"box","min":[x0,RB,0.4],"max":[x1,top,1.6],"color":bc})
    objs.append({"type":"box","min":[x0,top+gap,0.4],"max":[x1,top+gap+0.25,1.6],"color":cc})
    py=top+min(0.18,gap*0.45)
    objs.append({"type":"pipe","from":[x0+0.2,py,z],"to":[x1-0.7,py,z],"dia":0.06})
    for hx in (x0+0.8,x0+1.9):
        objs.append({"type":"flex","pts":[[hx,py,z],[hx,py-0.05,z],[hx,RB+0.0,z],[hx,RB-0.04,z]],"dia":0.035})
        objs.append({"type":"head_pendent","pos":[hx,RB-0.04-0.48,z],"s":1.6})
    dims.append({"from":[x1-0.3,top,1.7],"to":[x1-0.3,top+gap,1.7],"text":dt,"dx":62,"dy":0})
    labels.append({"text":"이 사이 헤드 설치 제외 가능","at":[x0+1.35,top+gap/2+0.03,1.6],"dx":0,"dy":0,"style":"red"}) if gap>0.7 else None
    labels.append({"text":tag,"at":[x0+W/2,top+gap+0.25,z],"dx":0,"dy":-40,"style":"light"})
    labels.append({"text":tl,"at":[x0+0.9,top+gap+0.12,1.6],"dx":0,"dy":0})
    labels.append({"text":bl,"at":[x0+2.45,RB+0.02,1.6],"dx":0,"dy":38})
spec={"w":1800,"h":820,"title":"그림 1. 천장과 반자 사이 — 헤드를 설치하지 않을 수 있는 거리 (NFTC 103 2.12.1.5~2.12.1.7, 비축척 단면)",
 "note":"빨간 화살표 구간(천장~반자 사이) 안에 헤드를 두지 않을 수 있다는 뜻이며, 반자 아래 실내 헤드는 그대로 둡니다. ①에는 2.12.1.5.2(사이 벽 불연·2 m 이상·가연물 없음)도 따로 있습니다. 거리 측정점은 원문에 따로 없습니다. AI 작성 비축척 — 생략: 행거, 조명·덕트 등 반자 속 설비.",
 "camera":{"ortho":5.1,"pos":[5.6,3.05,9],"target":[5.6,3.05,0]},
 "objects":objs,"dims":dims,"labels":labels}
json.dump(spec,open('fig1.json','w'),ensure_ascii=False)
