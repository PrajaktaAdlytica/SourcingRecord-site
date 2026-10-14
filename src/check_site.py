from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit
from collections import Counter
import json,xml.etree.ElementTree as ET,re
R=Path(__file__).resolve().parents[1];D=R/'dist'
class Page(HTMLParser):
 def __init__(self):super().__init__();self.ids=[];self.refs=[];self.h1=0;self.scripts=[];self.desc=False;self.tokens=[]
 def handle_starttag(self,t,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.append(a['id'])
  if t=='h1':self.h1+=1
  if t=='meta' and a.get('name')=='description':self.desc=bool(a.get('content'))
  for k in ('href','src'):
   if a.get(k):self.refs.append(a[k])
  if t=='script' and a.get('src'):self.scripts.append(a['src'])
 def handle_data(self,d):self.tokens.append(d)
errors=[];summary=[]
for p in sorted(D.rglob('index.html')):
 x=Page();x.feed(p.read_text());route='/'+str(p.parent.relative_to(D));route='/' if route=='/.' else route
 if x.h1!=1:errors.append([route,'h1-count',x.h1])
 if not x.desc:errors.append([route,'missing-description'])
 dup=[k for k,v in Counter(x.ids).items() if v>1]
 if dup:errors.append([route,'duplicate-ids',dup])
 for target in x.refs:
  u=urlsplit(target)
  if u.scheme or u.netloc:continue
  if u.path:
   file=D/u.path.lstrip('/') if u.path.startswith('/') else p.parent/u.path
   if not file.suffix:file=file/'index.html'
   if not file.exists():errors.append([route,'missing-local-target',target])
  elif u.fragment and u.fragment not in x.ids:errors.append([route,'missing-anchor',target])
 text=' '.join(x.tokens)
 if 'RESEARCH-STAGE CONCEPT' not in text:errors.append([route,'missing-concept-disclosure'])
 summary.append({'route':route,'words':len(text.split()),'headings':x.h1,'metadata':x.desc})
for p in D.rglob('*.svg'):
 try:ET.parse(p)
 except Exception as ex:errors.append([str(p),'invalid-svg',str(ex)])
for name in ['site.js','demo.js','demo-engine.js']:
 s=(D/'assets'/name).read_text()
 if re.search(r'\b(fetch|XMLHttpRequest|sendBeacon|localStorage|sessionStorage)\b',s):errors.append([name,'unexpected-transmission-or-persistence-api'])
assert len(summary)==25
assert not errors,errors
(R/'src/route-verification.json').write_text(json.dumps({'routes':summary,'errors':errors,'transmission':'No networking or browser persistence APIs in application JS','forms':'Local-only preview; no pilot_request/consent_submit acknowledgement event emitted','status':'passed'},indent=2))
print(f'25/25 pages: local links, anchors, one H1, descriptions, unique IDs and SVG parsing passed. No network/persistence APIs in application JS.')
