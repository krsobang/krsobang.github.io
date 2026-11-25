import math, matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import Circle, Rectangle
fp=[f for f in fm.findSystemFonts() if 'NotoSansCJK' in f and 'Regular' in f]
fm.fontManager.addfont(fp[0]); plt.rcParams['font.family']=fm.FontProperties(fname=fp[0]).get_name()
r=2.1; S=2*r*math.cos(math.radians(45))
fig,ax=plt.subplots(1,2,figsize=(16,6.6),dpi=125)
def base(a,W,Hh,t):
    a.add_patch(Rectangle((0,0),W,Hh,fill=False,lw=3,ec='#1f3150'))
    a.set_xlim(-1.4,W+1.4);a.set_ylim(-1.6,Hh+1.2);a.set_aspect('equal');a.axis('off');a.set_title(t,fontsize=17,color='#1f3150',pad=10)
# 정방형
W=4*S;Hh=3*S;base(ax[0],W,Hh,'① 정방형 배치 — S = 2 × r × cos45° (2.9.2.5.1)')
for i in range(4):
    for j in range(3):
        x,y=S/2+i*S,S/2+j*S
        ax[0].add_patch(Circle((x,y),r,fc='#2f8be6',alpha=.08,ec='#2f8be6',lw=.8))
        ax[0].plot(x,y,'o',ms=9,mfc='#c8302a',mec='k')
ax[0].annotate('',(S/2,S/2+2*S+0.0),(S/2+S,S/2+2*S),arrowprops=dict(arrowstyle='<->',color='#c00000',lw=2))
ax[0].text(S,S/2+2*S+0.25,'S ≈ 2.97 m',ha='center',color='#c00000',fontsize=14,weight='bold')
ax[0].annotate('',(0,S/2),(S/2,S/2),arrowprops=dict(arrowstyle='<->',color='#c00000',lw=2))
ax[0].text(-0.2,S/2+0.35,'S/2 이하(≈1.48 m)',ha='left',va='bottom',color='#c00000',fontsize=12)
ax[0].plot([S/2+S,S/2+S+r*math.cos(.6)],[S/2,S/2+r*math.sin(.6)],color='#1f3150',lw=1.5);ax[0].text(S/2+S+0.9,S/2+0.35,'r = 2.1 m',fontsize=12,color='#1f3150')
ax[0].text(W/2,-1.0,'벽 또는 방호구역 경계(굵은 선)',ha='center',fontsize=12,color='#555')
# 장방형
a,b=3.6,math.sqrt((2*r)**2-3.6**2)
W=3*a;Hh=3*b;base(ax[1],W,Hh,'② 장방형 배치 — 대각선 pt = 2 × r = 4.2 m (2.9.2.5.2)')
for i in range(3):
    for j in range(3):
        x,y=a/2+i*a,b/2+j*b
        ax[1].plot(x,y,'o',ms=9,mfc='#c8302a',mec='k')
x0,y0=a/2,b/2
ax[1].add_patch(Rectangle((x0,y0),a,b,fill=True,fc='#ffe234',alpha=.3,ec='none'))
ax[1].annotate('',(x0,y0),(x0+a,y0+b),arrowprops=dict(arrowstyle='<->',color='#c00000',lw=2))
ax[1].text(x0+a/2+0.15,y0+b/2+0.35,'대각선 4.2 m 이하',color='#c00000',fontsize=13,weight='bold',rotation=math.degrees(math.atan2(b,a)))
ax[1].text(x0+a/2,y0-0.45,f'예: {a:.1f} m',ha='center',fontsize=12);ax[1].text(x0+a+0.2,y0+b/2,f'{b:.2f} m',va='center',fontsize=12)
ax[1].text(W/2,-1.0,'예시 간격(3.6 m)은 계산 예시 — 벽까지는 각 방향 간격의 1/2 이하(의견: 2.9.2.6 적용)',ha='center',fontsize=11,color='#555')
fig.suptitle('그림 1. 포헤드 상호간 거리와 벽까지의 거리 — 평면 개념도 (NFTC 105 2.9.2.5·2.9.2.6, 비축척)',fontsize=19,weight='bold',color='#1f3150')
fig.text(.5,-.02,'S·대각선은 원문 식(r = 2.1 m)으로 계산한 값(S = 2.9698… m). 정방형 S ≈ 2.97 m이면 헤드 1개당 약 8.82 ㎡ — 포헤드(9 ㎡)는 맞지만 포워터스프링클러헤드(8 ㎡)는 넘으므로\n바닥면적 기준도 따로 확인해야 합니다(계산·의견). AI(Claude) 작성 비축척 — 생략: 배관·보·기둥.',ha='center',fontsize=11.5,color='#444')
plt.savefig('fig1.png',bbox_inches='tight',facecolor='white');print(a,b,S)
