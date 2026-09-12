#!/usr/bin/env python3
from pathlib import Path
from bs4 import BeautifulSoup
import base64, hashlib, re
ROOT=Path(__file__).resolve().parents[1]
html=(ROOT/'index.html').read_text(encoding='utf-8')
soup=BeautifulSoup(html,'html.parser')

toggle=soup.find(id='mobileMenuToggle'); menu=soup.find(id='mobileMenu'); script=soup.find(id='mobile-menu-script')
assert toggle is not None, 'mobile burger button missing'
assert menu is not None and menu.name=='nav', 'mobile navigation panel missing'
assert script is not None, 'mobile navigation script missing'
assert 'mobile-menu-toggle' in (toggle.get('class') or []), 'mobile burger class missing'
assert toggle.get('aria-expanded')=='false', 'mobile burger aria-expanded missing'
assert toggle.get('aria-controls')=='mobileMenu', 'mobile burger aria-controls missing'
assert toggle.get('aria-label')=='Открыть меню', 'mobile burger accessible label missing'
expected=[('#ranking','Рейтинг'),('#cards','Отели'),('#prices','Стоимость'),('#extras','Услуги'),('#gastro','Еда'),('#shortlist','Рекомендация')]
for href,label in expected:
 a=menu.find('a',href=href); assert a and a.get_text(' ',strip=True)==label, f'mobile navigation item missing: {label}'
 assert soup.find(id=href[1:]) is not None, f'mobile navigation target missing: {href}'
desktop=soup.find('nav',class_='nav'); assert desktop is not None, 'desktop navigation markup missing'
for href,label in expected:
 a=desktop.find('a',href=href); assert a and a.get_text(' ',strip=True)==label, f'desktop navigation item missing: {label}'
favicon=soup.find('link',rel=lambda x:x and 'icon' in x)
assert favicon and favicon.get('href','').startswith('data:image/png;base64,'), 'approved embedded favicon missing'
favicon_bytes=base64.b64decode(favicon['href'].split(',',1)[1],validate=True)
assert hashlib.sha256(favicon_bytes).hexdigest()=='c5021df59ae2bea0ff4808dd20cdd028b7aab51a8168f5befcf64c0ba3e74b54','favicon does not match approved artwork'
compact=re.sub(r'\s+','',html)
for token,msg in [('html{scroll-padding-top:76px}','mobile scroll-padding-top missing'),('.section[id]{scroll-margin-top:76px}','mobile section scroll-margin-top missing'),('.mobile-menu-toggle{display:inline-flex','mobile burger must be visible on mobile'),('.nav{display:none}','desktop navigation must be hidden on mobile'),('.mobile-menu-toggle,.mobile-menu-panel{display:none!important}','mobile menu must be hidden in print/PDF')]: assert token in compact,msg
assert 'compare-toggle' not in html and 'compareDock' not in html and 'compareModal' not in html, 'Compare UI must stay removed'
cards=soup.select('article.hotel-card'); assert len(cards)==15, f'expected 15 hotel cards, found {len(cards)}'
for card in cards:
 name=(card.select_one('.photo-caption h3').get_text(' ',strip=True) if card.select_one('.photo-caption h3') else 'unknown')
 collapsed=card.select_one('.hotel-actions-collapsed'); expanded=card.select_one('.hotel-actions-expanded'); assert collapsed and expanded,f'{name}: hotel action rows missing'
 for row,button in ((collapsed,'Подробнее'),(expanded,'Свернуть')):
  buttons=row.find_all('button'); assert len(buttons)==1 and buttons[0].get_text(' ',strip=True)==button,f'{name}: {button} action missing'
  reviews=row.select('a.reviews-link'); sites=row.select('a.hotel-site-link'); assert len(reviews)==1 and len(sites)==1,f'{name}: Reviews/Site action missing'
  assert reviews[0].get_text(' ',strip=True)=='Отзывы' and 'tripadvisor.ru/' in reviews[0].get('href',''),f'{name}: Russian Tripadvisor action invalid'
  assert sites[0].get_text(' ',strip=True)=='Сайт отеля',f'{name}: hotel site label invalid'
  for a in (reviews[0],sites[0]): assert a.get('target')=='_blank',f'{name}: external action must open new tab'
for token,msg in [('.hotel-actions{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));','hotel actions must use fixed three columns'),('@media(max-width:620px){.hotel-actions{grid-template-columns:repeat(3,minmax(0,1fr));','mobile hotel actions must stay in one row'),('.hotel-card.is-open>.hotel-body>.hotel-actions-collapsed{display:none}','collapsed row must hide when open'),('details.open=!details.open','hotel toggle logic missing'),("if(event.target.closest('a'))closeMenu()",'mobile menu must close after selection'),("if(event.key==='Escape')closeMenu()",'mobile menu must close on Escape')]: assert token in compact,msg
assert "window.matchMedia('(min-width:681px)')" in html, 'mobile menu must reset on desktop'
print('{"status":"PASS","mobile_navigation":true,"items":6,"hotel_actions":"three-horizontal","cards":15,"compare":"removed"}')
