#!/usr/bin/env python3
from bs4 import BeautifulSoup
from pathlib import Path
from urllib.parse import urljoin
from io import BytesIO
import base64, html as html_lib, re, requests
from PIL import Image, ImageOps
ROOT=Path(__file__).resolve().parents[1]
p=ROOT/'index.html'
page_url='https://www.papillon.com.tr/TR/papillon-belvil/'
headers={'User-Agent':'Mozilla/5.0 (compatible; BelekNY/1.0)'}
r=requests.get(page_url,headers=headers,timeout=45); r.raise_for_status(); raw=r.text
tokens=('Papillon-Belvil-Drone-Otel-04','papillon-belvil-drone-otel-14-2560px')
candidates=[]
# Parse image/lazy-load attributes first.
page=BeautifulSoup(raw,'html.parser')
for img in page.find_all('img'):
    for attr in ('src','data-src','data-lazy-src','srcset','data-srcset'):
        val=img.get(attr)
        if not val: continue
        vals=val if isinstance(val,list) else [val]
        for vv in vals:
            for item in str(vv).split(','):
                url=item.strip().split()[0]
                if any(t.lower() in url.lower() for t in tokens):
                    candidates.append(urljoin(page_url,html_lib.unescape(url)))
# Catch CSS/JSON/escaped markup references.
for token in tokens:
    pattern=rf'(?:(?:https?:)?//|/)[^\s"\'<>\\]*{re.escape(token)}[^\s"\'<>\\]*'
    for m in re.findall(pattern,raw,flags=re.I):
        u=html_lib.unescape(m).replace('\\/','/')
        if u.startswith('//'): u='https:'+u
        candidates.append(urljoin(page_url,u))
# Remove WP size query noise and duplicates while preserving order.
seen=set(); candidates=[u for u in candidates if not (u in seen or seen.add(u))]
assert candidates, 'No official Papillon Belvil drone image URL found on official page'
best=None
for u in candidates:
    try:
        rr=requests.get(u,headers=headers,timeout=45); rr.raise_for_status()
        im=Image.open(BytesIO(rr.content)).convert('RGB')
        w,h=im.size
        # User requirement: general hotel/territory/beach view. Prefer landscape drone images.
        score=w*h*(2 if w>=h else 0.5)
        if best is None or score>best[0]: best=(score,u,im.copy())
    except Exception as e:
        print('skip image',u,type(e).__name__)
assert best is not None, 'Official Papillon drone image candidates were not downloadable images'
_,selected,im=best
im=ImageOps.fit(im,(1200,650),method=Image.Resampling.LANCZOS)
b=BytesIO(); im.save(b,'JPEG',quality=86,optimize=True)
data='data:image/jpeg;base64,'+base64.b64encode(b.getvalue()).decode()
s=BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser')
card=None
for c in s.select('article.hotel-card'):
    h=c.select_one('.photo-caption h3')
    if h and h.get_text(' ',strip=True)=='Papillon Belvil': card=c; break
assert card is not None, 'Papillon Belvil card missing'
img=card.find('img'); assert img is not None
img['src']=data; img['alt']='Papillon Belvil: общий вид отеля, территории и бассейнов'
p.write_text(str(s),encoding='utf-8')
print('Papillon Belvil official drone photo:',selected,'original=',best[2].size,'embedded=',len(b.getvalue()))
