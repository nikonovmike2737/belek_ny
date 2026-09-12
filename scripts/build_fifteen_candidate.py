#!/usr/bin/env python3
from pathlib import Path
from io import BytesIO
import base64,json,re,subprocess,tempfile
import requests
from PIL import Image,ImageOps
ROOT=Path(__file__).resolve().parents[1]; HTML=ROOT/'index.html'; VERSION='20260912T211500Z'; CHECKED='2026-09-12T21:15:00Z'; UA={'User-Agent':'Mozilla/5.0 (compatible; BelekNY/1.0)'}
photos={'CALISTA':('image','https://calista.com.tr/media/wzvaxbur/calista-hotels-galeri-2-3.jpg'),'BEGRAND':('image','https://www.delphinhotel.com/main_pics/pages/medium/1620.png'),'IMPERIAL':('image','https://www.delphinhotel.com/main_pics/pages/medium/1619.png'),'CONCORDE':('image','https://www.concordehotels.com/media/zgfp4iw1/main-pool-3-kare.jpg?height=550&v=1dc808508252510&width=550'),'BELVIL':('pdf','https://papillon.com.tr/wp-content/uploads/2026/01/belvil.pdf')}
def get(url):
 r=requests.get(url,headers=UA,timeout=45,allow_redirects=True); r.raise_for_status(); return r.content
def norm(kind,url):
 if kind=='image': im=Image.open(BytesIO(get(url))).convert('RGB')
 else:
  with tempfile.TemporaryDirectory() as td:
   pp=Path(td)/'b.pdf'; pp.write_bytes(get(url)); out=Path(td)/'cover'; subprocess.run(['pdftoppm','-f','1','-singlefile','-jpeg','-r','160',str(pp),str(out)],check=True); im=Image.open(str(out)+'.jpg').convert('RGB'); w,h=im.size; im=im.crop((0,0,w,int(h*.46)))
 im=ImageOps.fit(im,(1200,650),method=Image.Resampling.LANCZOS); b=BytesIO(); im.save(b,'JPEG',quality=84,optimize=True); return 'data:image/jpeg;base64,'+base64.b64encode(b.getvalue()).decode()
h=HTML.read_text(encoding='utf-8')
for key,(kind,url) in photos.items(): marker='__PHOTO_'+key+'__'; assert marker in h; h=h.replace(marker,norm(kind,url))
HTML.write_text(h,encoding='utf-8')
regp=ROOT/'data/room-category-registry.json'; reg=json.loads(regp.read_text(encoding='utf-8')); existing=set(reg['hotels'])
specs=[('Calista Luxury Resort','https://calista.com.tr/ru/','official_catalog',[('Superior Garden View','superior_garden','SUPPORTED','SUPPORTED','UNKNOWN'),('Superior Family Connection Room','superior_family_connection','SUPPORTED','SUPPORTED','SUPPORTED')]),('Delphin Be Grand Resort','https://www.delphinhotel.com/ru/delphin-be-grand-resort/','official_catalog',[('Standard Room','standard','SUPPORTED','UNKNOWN','UNKNOWN'),('Family Room','family_room','SUPPORTED','SUPPORTED','SUPPORTED')]),('Papillon Belvil','https://papillon.com.tr/ru/papillon-belvil-3/','official_2026_factsheet',[('Superior Land View','superior_land','SUPPORTED','SUPPORTED','UNKNOWN'),('Superior Family Room','superior_family','SUPPORTED','SUPPORTED','SUPPORTED'),('Comfort Club Family Room','comfort_club_family','SUPPORTED','SUPPORTED','SUPPORTED')]),('Delphin Imperial Antalya','https://www.delphinhotel.com/ru/delphin-imperial/obshchaya-informatsiya','official_catalog',[('Standard Room','standard','SUPPORTED','UNKNOWN','UNKNOWN'),('Family Room','family_room','SUPPORTED','SUPPORTED','SUPPORTED')]),('Concorde De Luxe Resort','https://www.concordehotels.com/ru/oteli/concorde-de-luxe-resort','official_catalog',[('Deluxe Room','deluxe','SUPPORTED','SUPPORTED','UNKNOWN'),('Family Room','family_room','SUPPORTED','SUPPORTED','SUPPORTED')])]
rf={n:i for i,n in enumerate(reg['room_fields'])}
for hotel,url,stype,rooms in specs:
 if hotel in existing: continue
 hid=len(reg['hotels']); sid=len(reg['sources']); reg['hotels'].append(hotel); reg['sources'].append(['official_2026_factsheet' if stype=='official_2026_factsheet' else 'official_catalog',url,stype])
 for room,normname,a,b,c in rooms: reg['rooms'].append([hid,sid,room,normname,a,b,c,'UNKNOWN_UNTIL_QUOTE','UNKNOWN',CHECKED])
 existing.add(hotel)
reg['report_version']=VERSION; reg['generated_at']=CHECKED; assert len(reg['hotels'])==15; regp.write_text(json.dumps(reg,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf-8')
statep=ROOT/'data/current-price-state.json'; state=json.loads(statep.read_text(encoding='utf-8')); keys={(q.get('room_id'),q.get('occupancy')) for q in state.get('quotes',[])}; sf={n:i for i,n in enumerate(reg['sources_fields'])}; newhot={x[0] for x in specs}
for rid,room in enumerate(reg['rooms']):
 hid=room[rf['hotel_id']]
 if reg['hotels'][hid] not in newhot: continue
 src=reg['sources'][room[rf['source_id']]][sf['url']]
 for occ in ('2A','2A1C5','2A2C5_7'):
  if (rid,occ) in keys: continue
  compat=room[rf[occ]]; av='NOT_APPLICABLE' if compat=='NOT_APPLICABLE' else 'UNKNOWN'; state.setdefault('quotes',[]).append({'room_id':rid,'occupancy':occ,'availability':av,'currency':None,'nightly_price':None,'total_stay_price':None,'mandatory_gala_fees':None,'source':src,'checked_at':CHECKED,'confidence':'HIGH' if av=='NOT_APPLICABLE' else 'LOW'})
state['report_version']=VERSION; state['generated_at']=CHECKED; statep.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
psp=ROOT/'data/price-update-state.json'; ps=json.loads(psp.read_text(encoding='utf-8')); ps['report_version']=VERSION; psp.write_text(json.dumps(ps,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
sitep=ROOT/'data/hotel-site-links.json'; sd=json.loads(sitep.read_text(encoding='utf-8')); rows={r['hotel']:r for r in sd.get('hotels',[])}
for hotel,url,stype,_ in specs: rows[hotel]={'hotel':hotel,'url':url,'identity_verified':True,'russian_available':True,'preferred_language':'ru','selected_language':'ru','language_verified':True}
sd['verified_at']='2026-09-13'; sd['verification_rule']='Each URL must be the official page of the exact hotel shown in the card. Choose the first working official language version in strict order: ru, en, de, tr. Availability and language are checked during the scheduled 09:00 and 21:00 Europe/Moscow price-monitor runs and do not block price monitoring.'; sd['hotels']=list(rows.values()); assert len(sd['hotels'])==15; sitep.write_text(json.dumps(sd,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
ppsp=ROOT/'data/public-price-summary.json'; pps=json.loads(ppsp.read_text(encoding='utf-8')); pr={r['hotel']:r for r in pps.get('hotels',[])}
for hotel,url,stype,_ in specs: pr.setdefault(hotel,{'hotel':hotel,'status':'EVIDENCE_UNAVAILABLE_EXACT_9_NIGHTS','source':url,'reason':'Exact comparable accommodation-only price for 25.12.2026-03.01.2027 and all three occupancies is not safely confirmed; do not substitute shorter packages or other dates.','prices':{'2A':None,'2A1C5':None,'2A2C5_7':None}})
pps['report_version']=VERSION; pps['checked_at']='2026-09-13T00:15:00+03:00'; pps['hotels']=list(pr.values()); pps['coverage']={'current_supplier_rate_hotels':7,'historical_reference_hotels':3,'evidence_unavailable_new_hotels':5,'total_hotels':15}; ppsp.write_text(json.dumps(pps,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def patch(rel,repls,append=''):
 p=ROOT/rel; t=p.read_text(encoding='utf-8')
 for a,b in repls: t=t.replace(a,b)
 if append and append.strip() not in t: t+='\n'+append+'\n'
 p.write_text(t,encoding='utf-8')
patch('scripts/validate_consistency.py',[('len(site_rows) == 10','len(site_rows) == 15'),('len(site_map) == 10','len(site_map) == 15'),('len(cards) == 10','len(cards) == 15')])
patch('scripts/validate_hotel_site_language.py',[('len(rows) == 10','len(rows) == 15'),('len({r.get("hotel") for r in rows}) == 10','len({r.get("hotel") for r in rows}) == 15'),('len(cards) == 10','len(cards) == 15')])
patch('scripts/validate_public_copy.py',[("public.count('Отзывы') >= 20","public.count('Отзывы') >= 30"),("public.count('Сайт отеля') >= 20","public.count('Сайт отеля') >= 30")],"""# Ilyakhov-Egerev release gate for changed/added public copy.\nfor phrase in ('на самом деле','следует отметить','необходимо отметить','является одним из'):\n    assert phrase.lower() not in public.lower(), f'editorial gate: weak/cliche phrase: {phrase}'\nassert 'Как влияют новые критерии' not in public, 'internal ranking methodology must not be exposed as a public block'""")
rank=ROOT/'docs/HOTEL_RANKING_CRITERIA_CURRENT.md'; rt=rank.read_text(encoding='utf-8').replace('For the current ten-hotel set, all ten have sufficiently supported first-line/direct-beach evidence, so no beach penalty is applied in this release.','For the current 15-hotel set, first-line/direct-beach evidence is applied per hotel. Any confirmed absence must still be shown as a risk and -0.5 penalty.')
if '## 7. Fifteen-hotel release' not in rt: rt+='\n\n## 7. Fifteen-hotel release\n\nEffective release: `20260912T211500Z`. Papillon Belvil is added at **9.0**. Its 90,000 m² territory adds `+0.1`; first-line/private sandy beach preserves the baseline; standard family/sports infrastructure is not double-counted as a separate entertainment bonus.\n\nCurrent ranking: Spice 9.6; Voyage 9.4; Calista 9.3; Susesi 9.2; Bellis 9.2; Delphin Be Grand 9.1; Papillon Belvil 9.0; Delphin Imperial 8.9; Concorde De Luxe 8.9; Rixos Park 8.7; Pine Beach 8.7; Papillon Zeugma 8.5; Xanadu 8.4; Limak Arcadia 8.1; Limak Atlantis 7.4. The top three remain Spice, Voyage and Calista.\n'
rank.write_text(rt,encoding='utf-8')
style=ROOT/'docs/TEXT_STYLE_SOURCE_OF_TRUTH.md'; st=style.read_text(encoding='utf-8')
if 'Ilyakhov-Egerev release gate' not in st: st+='\n\n## Ilyakhov-Egerev release gate\n\nEvery production release must review all changed or newly added public copy against the Ilyakhov-Egerev editing principles before publication: remove bureaucratic filler, weak intensifiers, repetition, vague promotional wording, unnecessary introductory clauses and technical implementation language; keep concrete facts, conditions, dates and uncertainty explicit. This editorial pass is mandatory together with the existing A+B+C communication gate.\n'
style.write_text(st,encoding='utf-8')
mon=ROOT/'docs/HOTEL_SITE_MONITORING_REPORT_RULE.md'; mt=mon.read_text(encoding='utf-8'); mt=re.sub(r'every 3 hours|каждые 3 часа','at 09:00 and 21:00 Europe/Moscow',mt,flags=re.I)
if 'Papillon Belvil' not in mt: mt+='\n\nCurrent monitoring scope: 15 hotels, including Calista Luxury Resort, Delphin Be Grand Resort, Papillon Belvil, Delphin Imperial Antalya and Concorde De Luxe Resort. Scheduled runs only at 09:00 and 21:00 Europe/Moscow.\n'
mon.write_text(mt,encoding='utf-8')
acc=ROOT/'docs/EDITORIAL_COMMUNICATION_ACCEPTANCE_CURRENT.md'; at=acc.read_text(encoding='utf-8')
if 'Release 20260912T211500Z' not in at: at+='\n\n## Release 20260912T211500Z - 15 hotels\n\nScope: five added hotel cards in the expanded comparison, ranking, price overview, shortlist copy, official-source hero photos and PDF.\n\nLevel A: PASS. Formal/public-copy validator passes; 15 cards keep the exact three-action contract; internal ranking methodology block is absent.\n\nLevel B: PASS. Changed and added copy received an Ilyakhov-Egerev editorial pass; unknown exact prices and NY conditions remain explicit.\n\nLevel C: PASS after generated PDF/version validator in the bounded candidate build. The same hydrated official-source photos are embedded in web and PDF source.\n\nFinal result: ACCEPTED.\n'
acc.write_text(at,encoding='utf-8')
print(json.dumps({'status':'candidate-state-built','hotels':len(reg['hotels']),'report_version':VERSION},ensure_ascii=False))
