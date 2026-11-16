import re,sys,os,matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle,Rectangle,Polygon,Ellipse
from matplotlib.lines import Line2D
base,out=sys.argv[1],sys.argv[2]
def parse(f):
    t=open(os.path.join(base,f),encoding='utf-8',errors='ignore').read()
    ap={m.group(1):(m.group(2),[float(x) for x in m.group(3).split('X')]) for m in re.finditer(r'%ADD(\d+)([A-Z]),([\d.X]+)\*%',t)}
    cur=None;pos=None;items=[];poly=None;sec=None
    for l in t.splitlines():
        m=re.match(r'G04 (\w+) Start',l)
        if m: sec=m.group(1);continue
        m=re.match(r'G54D(\d+)\*',l)
        if m: cur=ap.get(m.group(1));continue
        if l.startswith('G36'): poly=[];continue
        if l.startswith('G37'):
            if poly: items.append(('poly',poly))
            poly=None;continue
        m=re.match(r'G01X(-?\d+)Y(-?\d+)D0([123])\*',l)
        if m:
            x,y=int(m.group(1))/1e5,int(m.group(2))/1e5;op=m.group(3)
            if poly is not None:
                (poly.append((x,y)) if op!='2' or not poly else poly.append((x,y)))
            elif op=='2': pos=(x,y)
            elif op=='1' and pos: items.append(('line',pos,(x,y),cur,sec));pos=(x,y)
            elif op=='3': items.append(('flash',(x,y),cur,sec));pos=(x,y)
    return items
def draw(ax,items,col,alpha=0.85):
    for it in items:
        if it[0]=='poly':
            ax.add_patch(Polygon(it[1],closed=True,fc=col,ec='none',alpha=alpha*0.5))
        elif it[0]=='line':
            _,a,b,ap,sec=it
            if ap is None: continue
            w=ap[1][0]; 
            ax.add_line(Line2D([a[0],b[0]],[a[1],b[1]],lw=max(w*PX,0.3),color=col,alpha=alpha*(0.35 if sec=='Copper' else 1),solid_capstyle='round'))
        else:
            _,p,ap,sec=it
            if ap is None: continue
            k,d=ap
            if k=='C': ax.add_patch(Circle(p,d[0]/2,fc=col,ec='none',alpha=alpha))
            elif k=='R': ax.add_patch(Rectangle((p[0]-d[0]/2,p[1]-d[1]/2),d[0],d[1],fc=col,ec='none',alpha=alpha))
            else: ax.add_patch(Ellipse(p,d[0],d[1],fc=col,ec='none',alpha=alpha))
def holes(ax,f):
    t=open(os.path.join(base,f),encoding='utf-8',errors='ignore').read()
    tools={a:float(b) for a,b in re.findall(r'^T(\d+)C([\d.]+)',t,re.M)};cur=None
    for l in t.splitlines():
        m=re.match(r'^T(\d+)$',l)
        if m:cur=m.group(1);continue
        m=re.match(r'^X(-?\d+)Y(-?\d+)',l)
        if m and cur:
            ax.add_patch(Circle((int(m.group(1))/1e5,int(m.group(2))/1e5),tools[cur]/2,fc='black',ec='white',lw=0.3))
top=parse('Gerber_TopLayer.GTL');bot=parse('Gerber_BottomLayer.GBL');sil=parse('Gerber_TopSilkscreenLayer.GTO');outl=parse('Gerber_BoardOutlineLayer.GKO')
xs=[];ys=[]
for it in outl:
    if it[0]=='line': xs+= [it[1][0],it[2][0]];ys+=[it[1][1],it[2][1]]
x0,x1,y0,y1=min(xs),max(xs),min(ys),max(ys)
W,H=x1-x0,y1-y0
fig,ax=plt.subplots(figsize=(10,10*H/W if H/W<2.2 else 22),dpi=110)
PX=72*fig.get_figwidth()/ (W*1.0)/ 25.4*1.0 /1.0  # mm -> points approx
PX=72*fig.get_size_inches()[0]/(W+4)  # points per mm
draw(ax,bot,'#3b6cff',0.9);draw(ax,top,'#ff3b3b',0.9);draw(ax,sil,'#ffd400',0.9);draw(ax,outl,'#ff00ff',1)
for f in ('Drill_PTH_Through.DRL','Drill_PTH_Through_Via.DRL','Drill_NPTH_Through.DRL'):
    if os.path.exists(os.path.join(base,f)): holes(ax,f)
ax.set_xlim(x0-2,x1+2);ax.set_ylim(y0-2,y1+2);ax.set_aspect('equal');ax.set_facecolor('#101030')
ax.set_title(os.path.basename(base)+f'  {W:.2f} x {H:.2f} mm  (merah=top, biru=bottom, kuning=silk, hitam=lubang)',fontsize=8)
fig.savefig(out,bbox_inches='tight');print('saved',out)
