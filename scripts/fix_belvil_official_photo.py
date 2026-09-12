#!/usr/bin/env python3
from bs4 import BeautifulSoup
from pathlib import Path
from io import BytesIO
import base64
import subprocess
import tempfile
import requests
from PIL import Image, ImageOps

ROOT=Path(__file__).resolve().parents[1]
p=ROOT/'index.html'
factsheet='https://papillon.com.tr/wp-content/uploads/2026/01/belvil.pdf'
headers={'User-Agent':'Mozilla/5.0 (compatible; BelekNY/1.0)'}
r=requests.get(factsheet,headers=headers,timeout=45,allow_redirects=True)
r.raise_for_status()

# Official 2026 factsheet page 3 contains the useful wide aerial with the hotel,
# territory, pools, beach and sea. Page 1 is a brand splash and is not suitable.
with tempfile.TemporaryDirectory() as td:
    pdf=Path(td)/'belvil.pdf'; pdf.write_bytes(r.content)
    out=Path(td)/'page3'
    subprocess.run(['pdftoppm','-f','3','-singlefile','-jpeg','-r','160',str(pdf),str(out)],check=True)
    im=Image.open(str(out)+'.jpg').convert('RGB')
    w,h=im.size
    im=im.crop((0,0,w,int(h*.35)))
    im=ImageOps.fit(im,(1200,650),method=Image.Resampling.LANCZOS)
    b=BytesIO(); im.save(b,'JPEG',quality=86,optimize=True)

data='data:image/jpeg;base64,'+base64.b64encode(b.getvalue()).decode()
s=BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser')
card=None
for c in s.select('article.hotel-card'):
    title=c.select_one('.photo-caption h3')
    if title and title.get_text(' ',strip=True)=='Papillon Belvil':
        card=c
        break
assert card is not None, 'Papillon Belvil card missing'
img=card.find('img'); assert img is not None
img['src']=data
img['alt']='Papillon Belvil: общий вид отеля, территории и пляжа'
p.write_text(str(s),encoding='utf-8')
print('Papillon Belvil official factsheet aerial PASS','embedded=',len(b.getvalue()))
