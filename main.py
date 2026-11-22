import json,os,sys,urllib.request as u,urllib.error as e
E=os.getenv("MAKEFUN_ENV_URL")or sys.exit()
V={c:100for c in"Pp"}|{c:320for c in"Nn"}|{c:330for c in"Bb"}|{c:500for c in"Rr"}|{c:900for c in"Qq"}|{c:20000for c in"Kk"}
def B(fen):
 b={};r=7;fl=0
 for c in fen.split()[0]:
  if c=="/":r-=1;fl=0
  elif c.isdigit():fl+=int(c)
  else:b[chr(fl+97)+str(r+1)]=c;fl+=1
 return b
def S(b,t):return sum(V[p]if p.isupper()else-V[p]for p in b.values())*(1if t=="w"else-1)
def M(b,m,t):
 b=b.copy();fr,to=m[:2],m[2:4];p=b.pop(fr);b[to]=m[4]if len(m)==5 else p
 if p in"Pp"and abs(int(fr[1])-int(to[1]))==2:return b,chr((("abcdefgh".index(fr[0])+("abcdefgh".index(to[0])))//2)+97)+str((int(fr[1])+int(to[1]))//2)
 if p in"Kk"and abs(ord(fr[0])-ord(to[0]))==2:
  if to[0]=="g":b["f"+fr[1]],b["h"+fr[1]]=b.pop("f"+fr[1]),b.pop("h"+fr[1])
  else:b["d"+fr[1]],b["a"+fr[1]]=b.pop("d"+fr[1]),b.pop("a"+fr[1])
 return b,None
def A(b,lms,t,d,a,b_,n,mx):
 if n[0]>=mx:return None,0
 if d==0:return lms[0],S(b,t)
 n[0]+=1
 bm,bs=None, -20001 if t=="w" else 20001
 for m in lms:
  nb,_=M(b,m,t);ot="b"if t=="w"else"w"
  _,s=A(nb,g["legal_moves"],ot,d-1,-b_,-a,n,mx) if d>1 else (None,S(nb,t))
  s=-s if d>1 else s
  if t=="w":
   if s>bs:bm,bs=m,s
   if s>a:a=s
  else:
   if s<bs:bm,bs=m,s
   if s<b_:b_=s
  if a>=b_:break
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