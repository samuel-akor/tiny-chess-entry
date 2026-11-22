import json,os,sys,urllib.request as u,urllib.error as e
E=os.getenv("MAKEFUN_ENV_URL")or sys.exit()
V={c:100for c in"Pp"}|{c:320for c in"Nn"}|{c:330for c in"Bb"}|{c:500for c in"Rr"}|{c:900for c in"Qq"}|{c:20000for c in"Kk"}
P={'P':[0]*8+[50]*8+[10,10,20,30,30,20,10,10]+[5,5,10,25,25,10,5,5]+[0,0,0,20,20,0,0,0]+[5,-5,-10,0,0,-10,-5,5]+[5,10,10,-20,-20,10,10,5]+[0]*8,'N':[-50,-40,-30,-30,-30,-30,-40,-50,-40,-20,0,0,0,0,-20,-40,-30,0,10,15,15,10,0,-30,-30,5,15,20,20,15,5,-30,-30,0,15,20,20,15,0,-30,-30,5,10,15,15,10,5,-30,-40,-20,0,5,5,0,-20,-40,-50,-40,-30,-30,-30,-30,-40,-50],'B':[-20,-10,-10,-10,-10,-10,-10,-20,-10,0,0,0,0,0,0,-10,-10,0,5,10,10,5,0,-10,-10,5,5,10,10,5,5,-10,-10,0,10,10,10,10,0,-10,-10,10,10,10,10,10,10,-10,-10,5,0,0,0,0,5,-10,-20,-10,-10,-10,-10,-10,-10,-20],'R':[0]*8+[5,10,10,10,10,10,10,5]+[-5,0,0,0,0,0,0,-5]*5+[0]*8,'Q':[-20,-10,-10,-5,-5,-10,-10,-20,-10,0,0,0,0,0,0,-10,-10,0,5,5,5,5,0,-10,-5,0,5,5,5,5,0,-5,0,0,5,5,5,5,0,-5,-10,5,5,5,5,5,0,-10,-10,0,5,0,0,0,0,-10,-20,-10,-10,-5,-5,-10,-10,-20],'K':[-30,-40,-40,-50,-50,-40,-40,-30]*4+[-20,-30,-30,-40,-40,-30,-30,-20]+[-10,-20,-20,-20,-20,-20,-20,-10]+[20,20,0,0,0,0,20,20]+[20,30,10,0,0,10,30,20]}
def B(fen):
 b={};r=7;fl=0
 for c in fen.split()[0]:
  if c=="/":r-=1;fl=0
  elif c.isdigit():fl+=int(c)
  else:b[chr(fl+97)+str(r+1)]=c;fl+=1
 return b
def S(b,t):
 s=0
 for sq,p in b.items():
  u=p.upper();i="abcdefgh".index(sq[0])+(8-int(sq[1]))*8;v=V[u]+P[u][i^(0 if p.isupper()else 56)]
  s+=v if p.isupper()else -v
 return s if t=="w"else -s
def M(b,m,t):
 b=b.copy();fr,to=m[:2],m[2:4];p=b.pop(fr);b[to]=m[4]if len(m)==5 else p
 if p in"Pp"and abs(int(fr[1])-int(to[1]))==2:return b,chr((("abcdefgh".index(fr[0])+("abcdefgh".index(to[0])))//2)+97)+str((int(fr[1])+int(to[1]))//2)
 if p in"Kk"and abs(ord(fr[0])-ord(to[0]))==2:
  if to[0]=="g":b["f"+fr[1]],b["h"+fr[1]]=b.pop("f"+fr[1]),b.pop("h"+fr[1])
  else:b["d"+fr[1]],b["a"+fr[1]]=b.pop("d"+fr[1]),b.pop("a"+fr[1])
 return b,None
def O(b,ms):
 return sorted(ms,key=lambda m:V.get(b.get(m[2:4],'.').upper(),0)*10-V.get(b.get(m[:2],'.').upper(),0),reverse=True)
def Q(b,t,a,bt,n,mx):
 if n[0]>=mx:return S(b,t)
 s=S(b,t)
 if s>=bt:return bt
 if s>a:a=s
 for m in [x for x in t["legal_moves"]if b.get(x[2:4],'.')!='.']:
  nb,_=M(b,m,t);sc=-Q(nb,"b"if t=="w"else"w",-bt,-a,n,mx)
  if sc>=bt:return bt
  if sc>a:a=sc
 return a
def A(b,lms,t,d,a,bt,n,mx):
 if n[0]>=mx:return None,0
 if d==0:return lms[0],S(b,t)
 n[0]+=1
 bm,bs=None,-20001 if t=="w"else 20001
 for m in O(b,lms):
  nb,_=M(b,m,t)
  if d==1:_,sc=lms[0],S(nb,t)
  else:_,sc=A(nb,[],"b"if t=="w"else"w",d-1,-bt,-a,n,mx);sc=-sc
  if t=="w":
   if sc>bs:bm,bs=m,sc
   if sc>a:a=sc
  else:
   if sc<bs:bm,bs=m,sc
   if sc<bt:bt=sc
  if a>=bt:break
 return bm,bs
def P(p,d):
 try:
  with u.urlopen(u.Request(E+p,data=json.dumps(d).encode(),headers={"content-type":"application/json"}))as r:return json.load(r)
 except e.HTTPError as x:sys.exit(f"{p}: HTTP {x.code} {x.read().decode(errors='replace')}")
while 1:
 g=P("/game",{})
 if g["status"]=="done":break
 while g["status"]=="your_move":
  b=B(g["fen"]);t="w"if g["colour"]=="white"else"b";l=g["legal_moves"];n=[0];mx=50000
  bm,bs=A(b,l,t,3,-20001,20001,n,mx)
  if bm is None:bm=l[0]
  g=P("/move",{"game":g["game"],"move":bm})
 if g["status"]=="over":print(f"game {g['game']}: {g['outcome']} by {g['reason']}",file=sys.stderr)
print(f"done: {g.get('wins')} won, {g.get('draws')} drawn, {g.get('losses')} lost",file=sys.stderr)