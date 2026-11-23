import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import Rectangle
fp=[f for f in fm.findSystemFonts() if 'NotoSansCJK' in f and 'Bold' in f] or [f for f in fm.findSystemFonts() if 'NotoSansCJK' in f]
fm.fontManager.addfont(fp[0]); plt.rcParams['font.family']=fm.FontProperties(fname=fp[0]).get_name()
fig,(a,b)=plt.subplots(1,2,figsize=(18,11),dpi=125,gridspec_kw={'width_ratios':[1.15,1]})
R='#c00000';N='#1f3150'
# (가) 벽 관통 단면
a.set_xlim(0,100);a.set_ylim(0,70);a.axis('off');a.set_title('(가) 벽 관통부 단면 — 슬리브와 이격',fontsize=22,color=N,pad=12)
a.add_patch(Rectangle((44,24),12,41,fc='#c9ced5',ec='#555',lw=2,hatch='//'))
a.add_patch(Rectangle((42,26),16,18,fc='white',ec='#555',lw=2.5))      # 슬리브
a.add_patch(Rectangle((5,30),90,10,fc='#d84a3c',ec='#7a1d16',lw=2))     # 배관
a.annotate('',xy=(60,26),xytext=(60,44),arrowprops=dict(arrowstyle='<->',color=R,lw=2.5))
a.text(61,48,'관통구·슬리브 호칭구경',color=R,fontsize=17,va='center')
a.annotate('',xy=(24,30),xytext=(24,40),arrowprops=dict(arrowstyle='<->',color=N,lw=2.5))
a.text(5,43,'배관 호칭구경',color=N,fontsize=17)
a.text(44,67,'벽 · 바닥 · 기초',fontsize=17,color='#333')
rows=[('배관 호칭구경','관통구·슬리브 호칭구경'),('25 mm ~ 100 mm 미만','배관 + 50 mm 이상'),('100 mm 이상','배관 + 100 mm 이상'),('50 mm 이하 (단서)','배관 + 50 mm 미만의 더 큰 것도 가능')]
for i,(l,r) in enumerate(rows):
    y=19-i*5; w='bold' if i==0 else 'normal'
    a.text(3,y,l,fontsize=16,fontweight=w,color=N if i==0 else '#222'); a.text(40,y,r,fontsize=16,fontweight=w,color=N if i==0 else R)
# (나) 2층 이상 수직배관
b.set_xlim(0,100);b.set_ylim(0,70);b.axis('off');b.set_title('(나) 2층 이상 — 구경 65 mm 이상 수직배관 지진분리이음',fontsize=22,color=N,pad=12)
for y0 in (2,34,66):
    b.add_patch(Rectangle((10,y0),80,3,fc='#c9ced5',ec='#555',lw=2,hatch='//'))
b.add_patch(Rectangle((47,0),6,70,fc='#d84a3c',ec='#7a1d16',lw=2))
def j(y): b.add_patch(Rectangle((45.5,y-0.8),9,1.6,fc='#2d343b'))
for y in (8,29,40,61): j(y)
def dim(y0,y1,t):
    b.annotate('',xy=(60,y0),xytext=(60,y1),arrowprops=dict(arrowstyle='<->',color=R,lw=2.2)); b.text(62,(y0+y1)/2,t,color=R,fontsize=16,va='center')
dim(5,8,'바닥에서 0.3 m 이내'); dim(29,34,'천장에서 0.6 m 이내'); dim(37,40,'바닥에서 0.3 m 이내'); dim(61,66,'천장에서 0.6 m 이내')
b.text(12,52,'2층',fontsize=18,color=N); b.text(12,20,'1층',fontsize=18,color=N)
b.text(14,44,'■ 지진분리이음',fontsize=15,color='#2d343b')
fig.text(0.02,0.015,'원문: 제6조제3항제1호(관통구·슬리브 구경), 제7조제2항제2호(“제6조제3항 본문의 단서에도 불구하고” 2층 이상 건물은 각 층 바닥에서 0.3 m, 천장에서 0.6 m 이내). 이음 위치·층고는 예시.\nAI(Claude) 작성 비축척 단면 개념도 — 생략: 내화채움재, 흔들림 방지 버팀대, 수직직선배관 길이별 예외(제7조제2항제1호 단서).',fontsize=13,color='#555')
plt.subplots_adjust(left=.02,right=.98,top=.92,bottom=.1,wspace=.08)
plt.savefig('fig2.png',facecolor='white')
