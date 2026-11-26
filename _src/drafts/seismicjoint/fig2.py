import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import Rectangle
fp=[f for f in fm.findSystemFonts() if 'NotoSansCJK' in f and 'Bold' in f] or [f for f in fm.findSystemFonts() if 'NotoSansCJK' in f]
fm.fontManager.addfont(fp[0]); plt.rcParams['font.family']=fm.FontProperties(fname=fp[0]).get_name()
R='#c00000';N='#1f3150';PC='#d84a3c';J='#2d343b'
fig,(a,b)=plt.subplots(1,2,figsize=(18,10.5),dpi=125,gridspec_kw={'width_ratios':[1.5,1]})
def vpipe(ax,x,y0,y1): ax.add_patch(Rectangle((x-1.4,y0),2.8,y1-y0,fc=PC,ec='#7a1d16',lw=1.5))
def hpipe(ax,x0,x1,y): ax.add_patch(Rectangle((x0,y-1.4),x1-x0,2.8,fc=PC,ec='#7a1d16',lw=1.5))
def jt(ax,x,y): ax.add_patch(Rectangle((x-2.6,y-0.9),5.2,1.8,fc=J))
def dim(ax,x,y0,y1,t,c=R):
    ax.annotate('',xy=(x,y0),xytext=(x,y1),arrowprops=dict(arrowstyle='<->',color=c,lw=2)); ax.text(x+1.2,(y0+y1)/2,t,color=c,fontsize=14,va='center')
a.set_xlim(0,120);a.set_ylim(0,80);a.axis('off');a.set_title('(가) 구경 65 mm 이상 수직직선배관 — 길이별 지진분리이음 (제7조제2항제1호)',fontsize=19,color=N,pad=12)
# case1 <0.9
x=14;vpipe(a,x,30,40);hpipe(a,x-10,x,40);hpipe(a,x,x+10,30)
dim(a,x+4,30,40,'0.9 m 미만');a.text(2,18,'0.9 m 미만\n→ 설치하지 아니할 수 있음',fontsize=15,color=N)
# case2 0.9~2.1
x=52;vpipe(a,x,22,48);hpipe(a,x-10,x,48);hpipe(a,x,x+10,22);jt(a,x,35)
dim(a,x+4,22,48,'0.9 ~ 2.1 m');a.text(38,10,'0.9 m ~ 2.1 m\n→ 하나 설치할 수 있음',fontsize=15,color=N)
# case3 long
x=96;vpipe(a,x,6,74);hpipe(a,x-10,x,74);hpipe(a,x,x+10,6);jt(a,x,68);jt(a,x,12)
dim(a,x+4,68,74,'0.6 m 이내');dim(a,x+4,6,12,'0.6 m 이내');a.text(64,40,'그 밖의\n수직직선배관\n→ 상부·하부 단부\n0.6 m 이내',fontsize=15,color=N)
a.text(2,74,'■ 지진분리이음',fontsize=14,color=J)
# (나) 중간 지지부
b.set_xlim(0,80);b.set_ylim(0,80);b.axis('off');b.set_title('(나) 수직직선배관 중간 지지부 (제7조제2항제4호)',fontsize=19,color=N,pad=12)
x=30;vpipe(b,x,4,76);b.add_patch(Rectangle((x-9,38.5),18,3,fc='#9aa3ad',ec='#555',lw=1.5,hatch='//'))
b.text(x+11,40,'중간 지지부',fontsize=15,color='#333',va='center')
jt(b,x,47);jt(b,x,33);dim(b,x-10,41.5,47,'0.6 m 이내');dim(b,x-10,33,38.5,'0.6 m 이내')
b.texts[-1].set_x(x-21); b.texts[-3].set_x(x-21)
b.text(x+11,62,'지지부 윗부분',fontsize=14,color=N);b.text(x+11,22,'지지부 아랫부분',fontsize=14,color=N)
fig.text(0.02,0.02,'원문 요약: 제7조제2항(구경 65 mm 이상) 제1호 — 수직직선배관 상부·하부 단부로부터 0.6 m 이내, 길이 0.9 m 미만은 설치하지 아니할 수 있고 0.9 m ~ 2.1 m는 하나 설치 가능 / 제4호 — 중간 지지부로부터 0.6 m 이내 윗부분·아랫부분.\nAI(Claude) 작성 비축척 단면 개념도 — 배관 길이·이음 위치는 예시. 생략: 2층 이상 건물의 바닥 0.3 m·천장 0.6 m(제2호), 티분기(제3호), 흔들림 방지 버팀대.',fontsize=12,color='#555',wrap=True)
plt.subplots_adjust(left=.02,right=.98,top=.92,bottom=.12,wspace=.06)
plt.savefig('fig2.png',facecolor='white')
