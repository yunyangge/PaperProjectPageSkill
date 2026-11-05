"""Original-site layout snapshot and deliberate missing-media test, local only."""
from pathlib import Path
from urllib.parse import urljoin
import hashlib
import json
import re
import shutil
import requests
from bs4 import BeautifulSoup

CASE=Path(__file__).resolve().parents[1]/'outputs/benchmarks/sage-grpo'
BASE='https://dungeonmassster.github.io/SAGE-GRPO-Page/'

def main():
    fault=CASE/'fault-test';fault.mkdir(exist_ok=True)
    soup=BeautifulSoup((CASE/'revised/index.html').read_text(encoding='utf-8'),'html.parser')
    data=json.loads(soup.select_one('#media-data').string)
    data['media'][0]['file']='../assets/intentionally-missing.mp4'
    soup.select_one('#media-data').string=json.dumps(data).replace('</','<\\/')
    (fault/'index.html').write_text(str(soup),encoding='utf-8')
    for name in ['sage.css','player.js']:shutil.copy2(CASE/'revised'/name,fault/name)
    dest=CASE/'original-snapshot';dest.mkdir(exist_ok=True)
    missing=[]
    def localize(url):
        suffix=Path(url.split('?',1)[0]).suffix
        if 'fonts.googleapis.com' in url:suffix='.css'
        name='resource-'+hashlib.sha256(url.encode()).hexdigest()[:12]+suffix
        target=dest/name
        if not target.exists():
            for attempt in range(3):
                try:r=requests.get(url,timeout=40);r.raise_for_status();break
                except requests.RequestException:
                    if attempt==2:raise RuntimeError('Cannot fetch snapshot dependency: '+url)
            if suffix=='.css':
                def rewrite(m):
                    item=m[1].strip(' \"\'')
                    return m[0] if item.startswith('data:') else 'url('+localize(urljoin(url,item))+')'
                target.write_text(re.sub(r'url\(([^)]+)\)',rewrite,r.content.decode('utf-8')),encoding='utf-8')
            else:target.write_bytes(r.content)
        return name
    soup=BeautifulSoup((CASE/'sources/original.html').read_text(encoding='utf-8'),'html.parser')
    policy=soup.new_tag('meta',attrs={'http-equiv':'Content-Security-Policy','content':"default-src 'self' data:; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline'; media-src 'none'; frame-src 'none'"})
    soup.head.insert(0,policy)
    for tag,attr in [('link','href'),('script','src'),('img','src')]:
        for node in soup.select(f'{tag}[{attr}]'):
            url=urljoin(BASE,node[attr])
            try:node[attr]=localize(url)
            except RuntimeError:
                missing.append(url)  # Preserve the failed original dependency, do not substitute a new library.
    media={m['source']:m for m in json.loads((CASE/'media.json').read_text(encoding='utf-8'))['media']}
    for video in soup.select('video[src]'):
        match=media.get(urljoin(BASE,video['src']))
        if match:
            video['poster']=match['poster'];video['width']=match['width'];video['height']=match['height']
    (dest/'index.html').write_text(str(soup),encoding='utf-8')
    (dest/'SNAPSHOT-NOTE.txt').write_text('Author HTML/CSS/JS and image/font dependencies retained; external dependency URLs localized. Video playback blocked by CSP. The ten selected clips receive local frame-1s posters and probed intrinsic dimensions; uncollected videos remain unavailable. Compare opening and selected groups only; this is not a full original playback audit. All author material is ignored local research input.',encoding='utf-8')
    (dest/'missing-dependencies.json').write_text(json.dumps(missing,indent=2),encoding='utf-8')
    print('Created SAGE layout snapshot and missing-video fixture.')

if __name__=='__main__':main()
