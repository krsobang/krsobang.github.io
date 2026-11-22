import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import Circle, Rectangle
import glob
fp=[f for f in fm.findSystemFonts() if 'NotoSansCJK' in f and 'Bold' in f] or [f for f in fm.findSystemFonts() if 'NotoSansCJK' in f]
fm.fontManager.addfont(fp[0]); plt.rcParams['font.family']=fm.FontProperties(fname=fp[0]).get_name()
fig,ax=plt.subplots(figsize=(18,11.5),dpi=125)
ax.add_patch(Rectangle((0,0),60,24,fc='#eef1ec',ec='#333',lw=4))
def wall(x0,y0,x1,y1): ax.plot([x0,x1],[y0,y1],color='#555',lw=4)
wall(0,10,46,10); wall(0,14,60,14)
for x in (15,30): wall(x,0,x,10)
wall(46,0,46,10)
for x in (20,40): wall(x,14,x,24)
# 문(틈) 표현 생략. 끝방(46~60 x 0~10)은 복도 끝에서만 출입
ax.add_patch(Rectangle((46,10),14,4,fc='#eef1ec',ec='none'))
wall(46,10,46,10)
for (x,y,n,c) in ((14,12,'A','#2f8be6'),(38,12,'B','#1e9e4a')):
    ax.add_patch(Circle((x,y),25,fc=c,alpha=.10,ec=c,lw=2.5,ls='--'))
    ax.add_patch(Rectangle((x-0.9,y-0.6),1.8,1.2,fc='#c62f28',ec='#222',zorder=5))
    ax.text(x,y+1.6,f'발신기 {n}',ha='center',fontsize=17,weight='bold',color='#1f3150',zorder=6,bbox=dict(fc='white',ec='#1f3150',boxstyle='round,pad=.25'))
ax.annotate('',xy=(14+25*0.8,12-25*0.6),xytext=(14,12),arrowprops=dict(arrowstyle='<->',color='#c00000',lw=2.5))
ax.text(14+11,12-9.2,'수평거리 25 m',color='#c00000',fontsize=17,weight='bold',rotation=-37,ha='center')
ax.text(52,12,'복도',ha='center',va='center',fontsize=16,color='#555')
ax.text(7,5,'실',fontsize=15,color='#777',ha='center')
ax.text(30,26,'층의 각 부분이 어느 한 발신기에서 수평거리 25 m 이하',ha='center',fontsize=18,weight='bold',color='#1f3150')
ax.set_xlim(-12,72); ax.set_ylim(-14,36); ax.set_aspect('equal'); ax.axis('off')
ax.set_title('그림 2. 한 층 평면 개념도 — 발신기 수평거리 25 m (NFTC 201 2.1.5.2, 평면 예시)',loc='left',fontsize=22,weight='bold',color='#1f2a36')
fig.text(0.02,0.03,"점선 원은 발신기에서 수평거리 25 m 범위(층 60 m × 24 m 예시). 원문 단서: '복도 또는 별도로 구획된 실로서 보행거리가 40 m 이상일 경우에는 추가로 설치'.\n원 안에 들어도 벽을 돌아가는 보행거리가 40 m 이상이면 추가 설치를 검토합니다(보행거리 측정 기준점은 원문에 없음). 벽·문 위치는 예시이며 문은 생략. AI(Claude) 작성 개념도.",fontsize=14,color='#444')
plt.savefig('fig2.png',facecolor='#f5f6f8'); print('ok')
