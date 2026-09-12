#!/usr/bin/env python3
from bs4 import BeautifulSoup
from pathlib import Path
p=Path(__file__).resolve().parents[1]/'index.html'
s=BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser')
urls={'Calista Luxury Resort':'https://calista.com.tr/ru/','Delphin Be Grand Resort':'https://www.delphinhotel.com/ru/delphin-be-grand-resort/','Papillon Belvil':'https://papillon.com.tr/ru/papillon-belvil-3/','Delphin Imperial Antalya':'https://www.delphinhotel.com/ru/delphin-imperial/obshchaya-informatsiya','Concorde De Luxe Resort':'https://www.concordehotels.com/ru/oteli/concorde-de-luxe-resort'}
for c in s.select('article.hotel-card'):
 h=c.select_one('.photo-caption h3')
 if not h: continue
 name=h.get_text(' ',strip=True)
 if name in urls:
  for a in c.select('a.hotel-site-link'): a['href']=urls[name]
p.write_text(str(s),encoding='utf-8')
print('site links synchronized',len(urls))
