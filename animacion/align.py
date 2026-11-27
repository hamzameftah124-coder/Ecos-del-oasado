import re, json, subprocess, numpy as np, librosa, soundfile as sf, os, sys
W="work"; SR=16000; HOP=640  # 40 ms
text=open(f"{W}/guion.txt").read()
# tokens: words with attached punctuation; paragraph breaks
paras=[p.strip() for p in text.split("\n\n") if p.strip()]
words=[]
for pi,p in enumerate(paras):
    for tok in p.split():
        words.append({"t":tok,"para":pi})
def clean(t): return re.sub(r"[^\wáéíóúüñÁÉÍÓÚÜÑ]","",t)
speed=int(sys.argv[1]) if len(sys.argv)>1 else 150
os.makedirs(f"{W}/syn",exist_ok=True)
cache={}
def syn(w):
    if w in cache: return cache[w]
    fn=f"{W}/syn/{abs(hash(w))}.wav"
    subprocess.run(["espeak-ng","-v","es","-s",str(speed),"-w",fn,w],check=True)
    y,_=librosa.load(fn,sr=SR)
    yt,_=librosa.effects.trim(y,top_db=35)
    cache[w]=yt; return yt
ref=[]; bounds=[]; pos=0
for i,wd in enumerate(words):
    y=syn(clean(wd["t"]).lower())
    bounds.append((pos,pos+len(y))); ref.append(y); pos+=len(y)
    t=wd["t"]; gap=0.0
    if i+1<len(words) and words[i+1]["para"]!=wd["para"]: gap=0.7
    elif re.search(r"[.…:?!]$",t): gap=0.45
    elif t.endswith(","): gap=0.2
    else: gap=0.03
    g=np.zeros(int(gap*SR)); ref.append(g); pos+=len(g)
ref=np.concatenate(ref)
print("ref dur",len(ref)/SR)
parts=[];offs=[];o=0
for p in ["p1","p2","p3"]:
    y,_=librosa.load(f"{W}/{p}.wav",sr=SR); parts.append(y); offs.append(o); o+=len(y)
real=np.concatenate(parts); print("real dur",len(real)/SR)
def feat(y):
    m=librosa.feature.mfcc(y=y,sr=SR,n_mfcc=14,hop_length=HOP,n_fft=1024)[1:]
    e=librosa.feature.rms(y=y,hop_length=HOP,frame_length=1024)
    e=np.log(e+1e-4); e=(e-e.mean())/e.std()
    m=(m-m.mean(1,keepdims=True))/(m.std(1,keepdims=True)+1e-6)
    return np.vstack([m,2*e]).astype(np.float32)
A=feat(ref); B=feat(real)
print(A.shape,B.shape,flush=True)
D,wp=librosa.sequence.dtw(X=A,Y=B,metric="euclidean",subseq=False,global_constraints=True,band_rad=0.08)
wp=wp[::-1]
# map ref frame -> real frame (first match)
mp=np.full(A.shape[1],-1)
for a,b in wp:
    if mp[a]<0: mp[a]=b
for i in range(1,len(mp)):
    if mp[i]<0: mp[i]=mp[i-1]
out=[]
tot=[len(x)/SR for x in parts]
for wd,(s,e) in zip(words,bounds):
    fs=min(s//HOP,len(mp)-1); fe=min(max(e//HOP-1,fs),len(mp)-1)
    ts=mp[fs]*HOP/SR; te=mp[fe]*HOP/SR+HOP/SR
    out.append({"w":wd["t"],"para":wd["para"],"s":ts,"e":te})
json.dump({"words":out,"offs":[x/SR for x in offs],"durs":tot},open(f"{W}/align.json","w"),ensure_ascii=False)
print("done")
