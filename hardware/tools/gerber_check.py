import re,sys,os,collections
base=sys.argv[1]
def drill(f):
    t=open(os.path.join(base,f),encoding='utf-8',errors='ignore').read()
    tools=dict(re.findall(r'^T(\d+)C([\d.]+)',t,re.M))
    unit='METRIC' if 'METRIC' in t else 'INCH'
    cnt=collections.Counter(); cur=None
    for l in t.splitlines():
        m=re.match(r'^T(\d+)$',l)
        if m: cur=m.group(1); continue
        if re.match(r'^X-?[\d.]+Y-?[\d.]+',l) and cur: cnt[cur]+=1
    return unit,{tools[k]:cnt[k] for k in tools}
for f in ('Drill_PTH_Through.DRL','Drill_PTH_Through_Via.DRL','Drill_NPTH_Through.DRL'):
    if os.path.exists(os.path.join(base,f)): print(f,drill(f))
# apertures & min track in copper
for f in ('Gerber_TopLayer.GTL','Gerber_BottomLayer.GBL'):
    t=open(os.path.join(base,f),encoding='utf-8',errors='ignore').read()
    ap=re.findall(r'%ADD(\d+)([A-Z]),([\d.]+)(?:X([\d.]+))?\*%',t)
    circ=sorted({float(a[2]) for a in ap if a[1]=='C'})
    unit='MM' if '%MOMM' in t else 'IN'
    print(f,unit,'circle apertures (track/via ring widths):',circ[:6],'...',circ[-3:])
# outline bbox
t=open(os.path.join(base,'Gerber_BoardOutlineLayer.GKO'),encoding='utf-8',errors='ignore').read()
fs=re.search(r'%FSLAX(\d)(\d)Y(\d)(\d)\*%',t); dec=int(fs.group(2))
xs=[int(x)/10**dec for x in re.findall(r'X(-?\d+)Y',t)]; ys=[int(y)/10**dec for y in re.findall(r'Y(-?\d+)D',t)]
unit='MM' if '%MOMM' in t else 'IN'
if xs and ys: print('outline',unit,'x',min(xs),max(xs),'y',min(ys),max(ys),'size',round(max(xs)-min(xs),3),round(max(ys)-min(ys),3))
