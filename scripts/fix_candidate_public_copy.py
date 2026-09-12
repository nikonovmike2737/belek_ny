#!/usr/bin/env python3
from bs4 import BeautifulSoup
from pathlib import Path
from io import BytesIO
import base64
import re
import subprocess
import tempfile
import requests
from PIL import Image, ImageOps

ROOT=Path(__file__).resolve().parents[1]
p=ROOT/'index.html'
s=BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser')
changed=0
for node in list(s.find_all(string=True)):
    if node.parent and node.parent.name in {'script','style','noscript','template'}:
        continue
    text=str(node)
    new=re.sub(r'\s+/\s+', ' и ', text)
    if new!=text:
        node.replace_with(new); changed+=1

# Replace the generic Papillon cover with an actual resort/territory/beach aerial
# from the official 2026 Papillon Belvil factsheet. Page 3 carries the useful
# aerial; page 1 is only a brand splash and is not acceptable for the hotel card.
card=None
for c in s.select('article.hotel-card'):
    h=c.select_one('.photo-caption h3')
    if h and h.get_text(' ',strip=True)=='Papillon Belvil':
        card=c
        break
assert card is not None, 'Papillon Belvil card missing'
url='https://papillon.com.tr/wp-content/uploads/2026/01/belvil.pdf'
r=requests.get(url,headers={'User-Agent':'Mozilla/5.0 (compatible; BelekNY/1.0)'},timeout=45,allow_redirects=True)
r.raise_for_status()
with tempfile.TemporaryDirectory() as td:
    pdf=Path(td)/'belvil.pdf'; pdf.write_bytes(r.content)
    out=Path(td)/'page3'
    subprocess.run(['pdftoppm','-f','3','-singlefile','-jpeg','-r','160',str(pdf),str(out)],check=True)
    im=Image.open(str(out)+'.jpg').convert('RGB')
    w,h=im.size
    # Keep only the photo area, excluding QR/title/factsheet text.
    im=im.crop((0,0,w,int(h*.35)))
    im=ImageOps.fit(im,(1200,650),method=Image.Resampling.LANCZOS)
    buf=BytesIO(); im.save(buf,'JPEG',quality=84,optimize=True)
    src='data:image/jpeg;base64,'+base64.b64encode(buf.getvalue()).decode()
img=card.find('img')
assert img is not None
img['src']=src
img['alt']='Papillon Belvil: общий вид отеля, территории и пляжа'

p.write_text(str(s),encoding='utf-8')
print('public copy spaced-slash cleanup',changed,'Papillon Belvil official aerial PASS')
