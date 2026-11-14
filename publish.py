"""Publish an order's video and/or gift message (encrypted; the order code is the key).
  python publish.py G002-K7QXM --video path/to/timelapse.mp4 --message "Merry Christmas Mom! Love, Ana"
  python publish.py G002-K7QXM --message "..."          (message now, video later)
  python publish.py G002-K7QXM --video https://youtu.be/XXXX
Then:  git add -A && git commit -m "order update" && git push
Nothing on the site lists the codes; without the exact code a page can't be found or read."""
import argparse,base64,hashlib,json,os,re,sys
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
ITER=200000
def norm(c): return re.sub(r'[^A-Z0-9]','',c.upper())
def ident(code): return hashlib.sha256(('glow-id:'+code).encode()).hexdigest()[:32]
def key(code): return hashlib.pbkdf2_hmac('sha256',code.encode(),b'glow-lamps-v1',ITER,32)
b64=lambda b: base64.b64encode(b).decode()
def enc(k,data):
    iv=os.urandom(12); return iv,AESGCM(k).encrypt(iv,data,None)
ap=argparse.ArgumentParser(); ap.add_argument('code'); ap.add_argument('--video'); ap.add_argument('--message')
a=ap.parse_args(); code=norm(a.code); i=ident(code); k=key(code)
os.makedirs('data',exist_ok=True); os.makedirs('v',exist_ok=True)
p=f'data/{i}.json'; rec={}
if os.path.exists(p):
    d=json.load(open(p)); rec=json.loads(AESGCM(k).decrypt(base64.b64decode(d['iv']),base64.b64decode(d['ct']),None))
if a.message is not None: rec['message']=a.message
if a.video:
    if re.match(r'https?://',a.video): rec.update(video=a.video,kind='url'); rec.pop('viv',None)
    else:
        viv,ct=enc(k,open(a.video,'rb').read()); open(f'v/{i}.bin','wb').write(ct)
        rec.update(video=f'v/{i}.bin',kind='enc',viv=b64(viv))
iv,ct=enc(k,json.dumps(rec).encode())
json.dump({'iv':b64(iv),'ct':b64(ct)},open(p,'w'))
print('published',code,{x:rec[x] for x in rec if x!='viv'})
