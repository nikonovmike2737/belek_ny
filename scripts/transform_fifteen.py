#!/usr/bin/env python3
from bs4 import BeautifulSoup
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'index.html'
OUT=ROOT/'index.html'
html=SRC.read_text(encoding='utf-8')
oldver=re.search(r'data-report-version=["\']([^"\']+)',html).group(1)
newver='20260912T211500Z'
html=html.replace(oldver,newver)
soup=BeautifulSoup(html,'html.parser')
for el in list(soup.find_all(string=re.compile('Как влияют новые критерии'))):
    candidate=el.find_parent(['section','div'])
    if candidate and candidate.get_text(' ',strip=True).startswith('Как влияют новые критерии'):
        if candidate.get('id') != 'ranking' and len(candidate.get_text(' ',strip=True)) < 5000: candidate.decompose()
repls={'Для четырёх новых отелей точную сопоставимую стоимость проживания на все 9 ночей для трёх составов семьи пока не удалось подтвердить безопасным источником, поэтому цифры не подставляем.':'Для пяти новых отелей точную сопоставимую стоимость проживания на все 9 ночей для трёх составов семьи пока не удалось подтвердить безопасным источником. Поэтому цифры не подставляем.','12 сентября отдельно перепроверены финалисты, три исторических ценовых разрыва и четыре новых отеля.':'12 сентября отдельно перепроверены финалисты и три исторических ценовых разрыва. Для пяти новых отелей точные 9-ночные цены пока не подтверждены.','После добавления четырёх отелей финальная тройка меняется: Calista входит в тройку благодаря сильной зимней инфраструктуре, спорту, большой территории и первой линии. Susesi остаётся очень сильным вариантом, но опускается на четвёртое место.':'После добавления пяти отелей финальная тройка остаётся прежней: Spice, Voyage и Calista. Papillon Belvil входит в верхнюю часть рейтинга, но пока не вытесняет Calista: у него сильная семейная инфраструктура и спорт, а точная цена и программа Нового года 2026-2027 ещё не подтверждены.','Для Calista, Delphin Be Grand, Delphin Imperial и Concorde De Luxe точную цену на наши 9 ночей пока не удалось подтвердить.':'Для Calista, Delphin Be Grand, Papillon Belvil, Delphin Imperial и Concorde De Luxe точную цену на наши 9 ночей пока не удалось подтвердить.','Delphin Be Grand и Imperial усилили выбор по зимней инфраструктуре, Concorde - по бассейнам, детскому клубу и спорту.':'Delphin Be Grand и Imperial усилили выбор по зимней инфраструктуре, Concorde - по бассейнам и спорту, а Papillon Belvil - по семейной инфраструктуре, территории и спорту.','четыре новых отеля':'пять новых отелей','четырёх новых отелей':'пяти новых отелей'}
for node in list(soup.find_all(string=True)):
    t=str(node); nt=t
    for a,b in repls.items(): nt=nt.replace(a,b)
    nt=nt.replace('официальная и разрешённая форма бронирования подтвердил,','официальная форма бронирования показала,').replace('Безопасного статического точная цена','Безопасно проверить точную цену').replace('Новогодний праздничный ужин в обычную бронь не включена.','Новогодний праздничный ужин в обычную бронь не включён.').replace('с праздничный ужин','с праздничным ужином').replace('Точная цена на 25 декабря - 3 января пока не подтверждён.','Точная цена на 25 декабря - 3 января пока не подтверждена.').replace('Точная цена для трёх составов пока не подтверждён.','Точная цена для трёх составов пока не подтверждена.').replace('подтверждает зимние бассейны, детский клуб и официальная форма бронирования.','подтверждает зимние бассейны и детский клуб; на сайте есть форма бронирования.')
    if nt!=t: node.replace_with(nt)
cards=soup.select('article.hotel-card'); byname={c.select_one('.photo-caption h3').get_text(' ',strip=True):c for c in cards}
for name,marker in {'Calista Luxury Resort':'__PHOTO_CALISTA__','Delphin Be Grand Resort':'__PHOTO_BEGRAND__','Delphin Imperial Antalya':'__PHOTO_IMPERIAL__','Concorde De Luxe Resort':'__PHOTO_CONCORDE__'}.items():
    c=byname[name]; img=c.find('img'); img['src']=marker; img['alt']=f'{name}: общий вид отеля и территории'
base=byname['Concorde De Luxe Resort']; card=BeautifulSoup(str(base),'html.parser').select_one('article.hotel-card'); card['class']=['hotel-card','tone-upgrade']
img=card.find('img'); img['src']='__PHOTO_BELVIL__'; img['alt']='Papillon Belvil: общий вид территории, бассейнов и пляжа'
card.select_one('.rank-badge').string='#7'; card.select_one('.score-badge').string='9.0 из 10'; cap=card.select_one('.photo-caption'); cap.select_one('.verdict').string='сильный семейный кандидат'; cap.select_one('h3').string='Papillon Belvil'; cap.select_one('.price-badge').string='Точная цена на 9 ночей пока не подтверждена'
body=card.select_one('.hotel-body'); body.select_one('p.lead').string='Сильный семейный кандидат на первой линии: территория 90 000 м², песчаный пляж, крытый подогреваемый бассейн, детский клуб и развитый спорт.'
why=body.select_one('.why'); why.clear(); st=soup.new_tag('strong'); st.string='Почему подходит вашей компании:'; why.append(st); why.append(' Здесь удобно совмещать детскую программу и спорт взрослых. Большая территория даёт место для прогулок, а крытые бассейны снижают зависимость от зимней погоды.')
body.select_one('.snapshot-label').string='Точная сопоставимая цена на 25 декабря 2026 года - 3 января 2027 года пока не подтверждена. Проверяем дважды в день.'
for pbox in body.select('.pricing-cards .pbox'): pbox.select_one('.night').string='цена пока не подтверждена'; pbox.select_one('.total').string='9 ночей: проверяем'
pc=body.select_one('.pricing-cards'); pc['data-price-snapshot-date']='2026-09-13'; pc['data-price-status']='EVIDENCE_UNAVAILABLE_EXACT_9_NIGHTS'; qt=body.select_one('.quick-tags'); qt.clear(); sp=soup.new_tag('span'); sp.string='средняя территория: 90 000 м²'; qt.append(sp)
review='https://www.tripadvisor.ru/Hotel_Review-g312725-d551332-Reviews-Papillon_Belvil_Hotel-Belek_Serik_District_Turkish_Mediterranean_Coast.html#REVIEWS'; site='https://papillon.com.tr/ru/papillon-belvil-3/'
for a in card.select('a.reviews-link'): a['href']=review; a['aria-label']='Отзывы о Papillon Belvil на Tripadvisor'
for a in card.select('a.hotel-site-link'): a['href']=site
sections=card.select('.detail-grid section'); content=[('Дети 3-10',['Papy Kids Club: мини-клуб 4-6 лет и программы для детей постарше','Для детей 1-3 лет есть отдельный формат вместе с родителем','Крытый детский бассейн работает круглый год']),('Спорт',['Теннис','Профессиональное футбольное поле','Fit Club и фитнес','Командные и дневные спортивные активности']),('Что реально есть зимой',['Крытый подогреваемый бассейн 228 м² работает круглый год','Крытый детский бассейн работает круглый год','Зимняя концепция включает детский клуб и спортивные активности','Основной аквапарк и часть открытых водных зон остаются сезонными']),('Что платно или требует проверки',['Программа Нового года 2026-2027 пока не подтверждена','Включение праздничного ужина в конкретный 9-ночный тариф нужно подтвердить','Точная цена на наши 9 ночей для трёх составов пока не подтверждена','Условия оплаты и отмены фиксируем только вместе с конкретным тарифом'])]
for sec,(title,chips) in zip(sections,content):
    sec.select_one('h4').string=title; ch=sec.select_one('.chips'); ch.clear();
    for text in chips: el=soup.new_tag('span',attrs={'class':'chip'}); el.string=text; ch.append(el)
    if title=='Что платно или требует проверки': ch['class']=['chips','chips-warn']
pros=card.select('.proscons > div')
for div,title,items in [(pros[0],'Сильные стороны для этой поездки',['Первая линия и собственный песчаный пляж','Территория 90 000 м² подходит для прогулок','Крытый подогреваемый бассейн и детский крытый бассейн работают круглый год','Сильный набор спорта и детских программ']),(pros[1],'Риски и ограничения',['Точная цена на 25 декабря - 3 января пока не подтверждена','Программа Нового года 2026-2027 и условия праздничного ужина пока не подтверждены','Часть аквапарка и открытых водных развлечений сезонная'])]:
    div.select_one('h4').string=title; ul=div.select_one('ul'); ul.clear();
    for text in items: li=soup.new_tag('li'); li.string=text; ul.append(li)
byname['Delphin Be Grand Resort'].insert_after(card)
ranking=[('Spice Hotel & Spa',9.6),('Voyage Belek Golf & Spa',9.4),('Calista Luxury Resort',9.3),('Susesi Luxury Resort',9.2),('Bellis Deluxe Hotel',9.2),('Delphin Be Grand Resort',9.1),('Papillon Belvil',9.0),('Delphin Imperial Antalya',8.9),('Concorde De Luxe Resort',8.9),('Rixos Park Belek',8.7),('Pine Beach Belek',8.7),('Papillon Zeugma Relaxury',8.5),('Xanadu Resort',8.4),('Limak Arcadia Sport Resort',8.1),('Limak Atlantis Deluxe',7.4)]
allcards=soup.select('article.hotel-card'); byname2={c.select_one('.photo-caption h3').get_text(' ',strip=True):c for c in allcards}; parent=allcards[0].parent
for name,score in ranking: parent.append(byname2[name].extract())
for idx,(name,score) in enumerate(ranking,1): c=byname2[name]; c.select_one('.rank-badge').string=f'#{idx}'; c.select_one('.score-badge').string=f'{score:.1f} из 10'
for h in soup.find_all('h2'):
    if h.get_text(' ',strip=True)=='Что известно о каждом отеле':
        eyebrow=h.find_previous('div',class_='eyebrow');
        if eyebrow: eyebrow.string='15 отелей'
price_sec=soup.find(id='prices'); table=price_sec.find('table'); tbody=table.find('tbody') or table
if not any('Papillon Belvil' in tr.get_text(' ',strip=True) for tr in table.find_all('tr')):
    tr=soup.new_tag('tr'); td=soup.new_tag('td'); td.string='Papillon Belvil *15'; tr.append(td)
    for _ in range(6): td=soup.new_tag('td'); td.string='точная цена пока не подтверждена'; tr.append(td)
    tbody.append(tr)
ps=price_sec.select_one('.price-sources')
if ps and 'Papillon Belvil:' not in ps.get_text(' ',strip=True):
    p=soup.new_tag('p'); p.append('*15 Papillon Belvil: '); a=soup.new_tag('a',href=site,target='_blank',rel='noopener noreferrer'); a.string='официальный источник'; p.append(a); p.append('. Официальные материалы подтверждают территорию 90 000 м², песчаный пляж на первой линии, семейные категории, крытый подогреваемый бассейн и детскую инфраструктуру. Точную сопоставимую цену на 25 декабря - 3 января для трёх составов семьи пока не подтверждаем; короткие или другие даты не подставляем.'); ps.append(p)
for node in list(soup.find_all(string=True)):
    t=str(node); nt=t.replace('Для Calista, Delphin Be Grand, Delphin Imperial и Concorde De Luxe','Для Calista, Delphin Be Grand, Papillon Belvil, Delphin Imperial и Concorde De Luxe').replace('Аудит 12 сентября 2026 года.','Аудит 13 сентября 2026 года.');
    if nt!=t: node.replace_with(nt)
short=soup.find(id='shortlist')
if short:
    sub=short.select_one('.section-head .sub');
    if sub: sub.string='После добавления пяти отелей финальная тройка остаётся прежней: Spice, Voyage и Calista. Papillon Belvil получает 9,0 и входит в верхнюю часть рейтинга, но пока не вытесняет Calista: точная цена и программа Нового года 2026-2027 ещё не подтверждены.'
for tag in soup.find_all(attrs={'data-report-version':True}): tag['data-report-version']=newver
marker=soup.find(id='pdf-report-version-marker')
if marker: marker.string=newver
for meta in soup.find_all('meta'):
    if meta.get('name')=='report-version': meta['content']=newver
OUT.write_text(str(soup),encoding='utf-8')
assert len(soup.select('article.hotel-card'))==15
assert 'Как влияют новые критерии' not in soup.get_text(' ',strip=True)
print('transform PASS',OUT.stat().st_size,newver)
