#!/usr/bin/env python3
from bs4 import BeautifulSoup
from pathlib import Path
import re
p=Path(__file__).resolve().parents[1]/'index.html'
s=BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser')
changed=0
for node in list(s.find_all(string=True)):
    if node.parent and node.parent.name in {'script','style','noscript','template'}:
        continue
    text=str(node)
    new=re.sub(r'\s+/\s+', ' и ', text)
    if new!=text:
        node.replace_with(new); changed+=1
p.write_text(str(s),encoding='utf-8')
print('public copy spaced-slash cleanup',changed)
