import json,os,sys,urllib.request as u,urllib.error as e
E=os.getenv("MAKEFUN_ENV_URL")or sys.exit()
V={c:100for c in"Pp"}|{c:320for c in"Nn"}|{c:330for c in"Bb"}|{c:500for c in"Rr"}|{c:900for c in"Qq"}|{c:20000for c in"Kk"}
def B(f):
 b={};r=7;f=0
 for c in f.split()[0]:
  if c=="/":r-=1;f=0
  elif c.isdigit():f+=int(c)
  else:b[chr(f+97)+str(r+1)]=c;f+=1
 return b
def S(b,t):return sum(V[p]if p.isupper()else-V[p]for p in b.values())*(1if t=="w"else-1)
def M(b,m,t):
 b=b.copy();f,t=m[:2],m[2:4];p=b.pop(f);b[t]=m[4]if len(m)==5 else p
 if p in"Pp"and abs(int(f[1])-int(t[1]))==2:return b,chr((("abcdefgh".index(f[0])+("abcdefgh".index(t[0])))//2)+97)+str((int(f[1])+int(t[1]))//2)
 if p in"Kk"and abs(ord(f[0])-ord(t[0]))==2:
  if t[0]=="g":b["f"+f[1]],b["h"+f[1]]=b.pop("f"+f[1]),b.pop("h"+f[1])
  else:b["d"+f[1]],b["a"+f[1]]=b.pop("d"+f[1]),b.pop("a"+f[1])
 return b,None
def P(p,d):
 try:
  with u.urlopen(u.Request(E+p,data=json.dumps(d).encode(),headers={"content-type":"application/json"}))as r:return json.load(r)
 except e.HTTPError as x:sys.exit(f"{p}: HTTP {x.code} {x.read().decode(errors='replace')}")
while 1:
 g=P("/game",{})
 if g["status"]=="done":break
 while g["status"]=="your_move":
  b=B(g["fen"]);t="w"if g["colour"]=="white"else"b";l=g["legal_moves"];bm=None;bs=-20001
  for m in l:
   nb,_=M(b,m,t);ot="b"if t=="w"else"w";s=-S(nb,ot)
   if s>bs:bm,bs=m,s
  g=P("/move",{"game":g["game"],"move":bm})
 if g["status"]=="over":print(f"game {g['game']}: {g['outcome']} by {g['reason']}",file=sys.stderr)
print(f"done: {g.get('wins')} won, {g.get('draws')} drawn, {g.get('losses')} lost",file=sys.stderr)