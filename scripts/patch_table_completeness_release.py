#!/usr/bin/env python3
from pathlib import Path
import html,re
from bs4 import BeautifulSoup
R=Path(__file__).resolve().parents[1]; P=R/'index.html'; s=P.read_text(encoding='utf-8')
OLD='20260912T211500Z'; NEW='20260913T070254Z'
assert OLD in s
s=s.replace(OLD,NEW)
s=re.sub(r'("updated_at"\s*:\s*")[^"]+("\s*,\s*"room_registry")',r'\g<1>2026-09-13T07:02:54Z\g<2>',s,count=1)
HOTELS=['Calista Luxury Resort','Delphin Be Grand Resort','Papillon Belvil','Delphin Imperial Antalya','Concorde De Luxe Resort']
def spans(xs,k): return ''.join(f'<span class="svc {k}">{html.escape(x)}</span>' for x in xs)
def er(n,f,p,c): return f'<tr><td class="hotel-name">{html.escape(n)}</td><td class="free-cell"><div class="service-list">{spans(f,"free")}</div></td><td class="paid-cell"><div class="service-list">{spans(p,"paid")}</div></td><td class="check-cell"><div class="service-list">{spans(c,"check")}</div></td></tr>'
EX=[
('Calista Luxury Resort',['Cally Kids Club','крытые и подогреваемые бассейны','теннисные корты','настольный теннис','пляжный волейбол','баскетбол','фитнес, хаммам и сауна'],['уроки тенниса и профессиональные ракетки','освещение корта','боулинг','спа-процедуры','рестораны по меню'],['работа аквапарка зимой','новогодняя программа и праздничный ужин 2026-2027']),
('Delphin Be Grand Resort',['мини-клуб 4-12 лет','крытый бассейн','6 теннисных кортов','теннисный инвентарь под депозит','освещение кортов по бронированию','настольный теннис','дартс','фитнес'],['спа-процедуры'],['боулинг и бильярд: условия оплаты зимой','работа луна-парка зимой','новогодняя программа и праздничный ужин 2026-2027']),
('Papillon Belvil',['Papy Kids Club','крытый и подогреваемый бассейн','теннис','пляжный волейбол','баскетбол','стрельба из лука','настольный теннис'],['индивидуальные спортивные занятия и тренеры'],['работа аквапарка зимой','теннисный инвентарь и освещение','новогодняя программа и праздничный ужин 2026-2027']),
('Delphin Imperial Antalya',['мини-клуб 4-12 лет','крытый бассейн','теннисный корт','настольный теннис','дартс','фитнес'],['спа-процедуры'],['боулинг и бильярд: условия оплаты зимой','работа луна-парка зимой','новогодняя программа и праздничный ужин 2026-2027']),
('Concorde De Luxe Resort',['Moppet Kids Club','крытый бассейн','теннисный корт, ракетка и мяч','фитнес','мини-гольф','настольный теннис','баскетбол','волейбол'],['боулинг','освещение корта и уроки тенниса','спа-процедуры'],['работа аквапарка зимой','зимнее расписание детского клуба','новогодняя программа и праздничный ужин 2026-2027'])]
def gs(t,c): return f'<span class="gastro-status {c}">{html.escape(t)}</span>'
def gr(n,l,lc,b,bc,e,links):
 a=' '+', '.join(f'<a href="{html.escape(u,quote=True)}" target="_blank" rel="noopener noreferrer">{html.escape(t)}</a>' for t,u in links) if links else ''
 return f'<tr><td class="hotel-name">{html.escape(n)}</td><td>{gs(l,lc)}</td><td>{gs(b,bc)}</td><td class="evidence">{html.escape(e)}{a}</td></tr>'
GA=[
('Calista Luxury Resort','не подтверждено','gastro-unknown','Пахлава есть, фисташковая не подтверждена','gastro-part','В открытых источниках не нашли подтверждения печёночного шашлыка. Свежие отзывы подтверждают пахлаву, но не конкретно фисташковую.',[('рестораны Calista','https://calista.com.tr/ru/dining'),('свежие отзывы','https://www.tripadvisor.com/Hotel_Feature-g312725-d664753-zft9165-Calista_Luxury_Resort.html')]),
('Delphin Be Grand Resort','Кебабы есть, печёночный не подтверждён','gastro-part','не подтверждено','gastro-unknown','В отеле есть турецкий ресторан Sultan, а свежие отзывы упоминают кебабы. Печёночный шашлык и именно фисташковую пахлаву подтвердить не удалось.',[('рестораны Delphin Be Grand','https://www.delphinhotel.com/en/delphin-be-grand-resort/restaurants')]),
('Papillon Belvil','не подтверждено','gastro-unknown','не подтверждено','gastro-unknown','Главный ресторан заявляет международную кухню и тематические вечера, но открытых данных именно по печёночному шашлыку и фисташковой пахлаве нет.',[('Belle Vue','https://papillon.com.tr/tr/gastro-journey/papillon-belvil/belle-vue/')]),
('Delphin Imperial Antalya','не подтверждено','gastro-unknown','не подтверждено','gastro-unknown','В отеле есть ресторан османской и турецкой кухни, но опубликованные материалы не подтверждают два конкретных блюда.',[('Delphin Imperial','https://www.delphinhotel.com/ru/delphin-imperial/obshchaya-informatsiya')]),
('Concorde De Luxe Resort','не подтверждено','gastro-unknown','не подтверждено','gastro-unknown','В актуальном описании питания нет подтверждения этих двух блюд. До бронирования нужен запрос конкретного меню на новогоднюю неделю.',[('Concorde De Luxe','https://www.concordehotels.com.tr/')])]
def add(sid,rows,make):
 global s
 m=re.search(rf'<section\b[^>]*\bid=["\']{sid}["\'][^>]*>',s,re.I); assert m
 a=s.find('<tbody',m.end()); z=s.find('</tbody>',a); chunk=s[a:z]
 missing=[x for x in rows if x[0] not in chunk]
 if missing: s=s[:z]+'\n'+'\n'.join(make(*x) for x in missing)+'\n'+s[z:]
add('extras',EX,er); add('gastro',GA,gr)
P.write_text(s,encoding='utf-8')
soup=BeautifulSoup(s,'html.parser')
for sid in ['prices','extras','gastro']:
 t=soup.find(id=sid).find('table'); names=[r.find_all(['td','th'])[0].get_text(' ',strip=True) for r in t.find_all('tr')[1:]]
 assert len(names)==15,(sid,len(names));
 for h in HOTELS: assert any(h in n for n in names),(sid,h)
assert soup.find(id='booking-readiness') is None
blocks=['hero' if 'hero' in (x.get('class') or []) else x.get('id') for x in soup.find('main').find_all('section',recursive=False)]
assert blocks==['hero','ranking','cards','prices','extras','gastro','pdf-download','shortlist'],blocks
print('table completeness PASS; report_version',NEW)
