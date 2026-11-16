import re,sys,collections
f=sys.argv[1]
t=open(f,encoding='utf-8',errors='ignore').read()
ap={m.group(1):float(m.group(3)) for m in re.finditer(r'%ADD(\d+)([A-Z]),([\d.]+)',t)}
sec=None; cur=None; draws=collections.defaultdict(collections.Counter)
for l in t.splitlines():
    m=re.match(r'G04 (\w+) Start',l)
    if m: sec=m.group(1); continue
    if l.startswith('G04') and 'End' in l: sec=None; continue
    m=re.match(r'G54D(\d+)\*',l)
    if m: cur=m.group(1); continue
    if l.endswith('D01*') and cur: draws[sec][ap.get(cur)]+=1
print(f.split('/')[-1],{k:dict(sorted(v.items())) for k,v in draws.items()})
