"""Layout-only author-source snapshot: media playback is deliberately disabled."""
from pathlib import Path
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import re
import requests
from bs4 import BeautifulSoup

ROOT=Path(__file__).resolve().parents[1]
CASE=ROOT/'outputs/benchmarks/echo-infinity'
BASE='https://echo-team-joy-future-academy-jd.github.io/Echo-Infinity/'

def main():
    dest=CASE/'original-snapshot';dest.mkdir(exist_ok=True)
    def localize(url):
        suffix=Path(url.split('?',1)[0]).suffix
        if 'fonts.googleapis.com' in url:suffix='.css'
        name='resource-'+hashlib.sha256(url.encode()).hexdigest()[:12]+suffix
        path=dest/name
        if not path.exists():
            r=requests.get(url,timeout=40);r.raise_for_status()
            if suffix=='.css':
                def replace(m):
                    item=m[1].strip(' \"\'')
                    return m[0] if item.startswith('data:') else 'url('+localize(urljoin(url,item))+')'
                path.write_text(re.sub(r'url\(([^)]+)\)',replace,r.content.decode('utf-8')),encoding='utf-8')
            else:path.write_bytes(r.content)
        return name
    soup=BeautifulSoup((CASE/'sources/original.html').read_text(encoding='utf-8'),'html.parser')
    policy=soup.new_tag('meta',attrs={'http-equiv':'Content-Security-Policy','content':"default-src 'self' data:; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https://i.ytimg.com; media-src 'none'; frame-src 'none'"})
    soup.head.insert(0,policy)
    for link in soup.select('link[href]'):
        if 'preconnect' in link.get('rel',[]):link.decompose();continue
        link['href']=localize(urljoin(BASE,link['href']))
    for script in soup.select('script[src]'):script['src']=localize(urljoin(BASE,script['src']))
    for img in soup.select('img[src]'):img['src']=localize(urljoin(BASE,img['src']))
    # Post-load image paths are explicitly constructed by the author's saved main.js.
    paths=[f'assets/posters/{length}/{i}.jpg' for length,n in [('240s',10),('30s',11),('60s',4),('5s',10)] for i in range(1,n+1)]
    paths += [f'assets/posters/compare/{length}/{i}/{m}.jpg' for length,n in [('240s',3),('30s',3),('60s',1),('5s',3)] for i in range(1,n+1) for m in ['ours','longlive','memflow','memorize']]
    def fetch(path):
        target=dest/path;target.parent.mkdir(parents=True,exist_ok=True)
        if target.exists():return
        r=requests.get(urljoin(BASE,path),timeout=40);r.raise_for_status();target.write_bytes(r.content)
    with ThreadPoolExecutor(max_workers=5) as pool:list(pool.map(fetch,paths))
    (dest/'index.html').write_text(str(soup),encoding='utf-8')
    note='Author HTML/CSS/JS retained, dependency URLs localized, 75 original posters downloaded. Video/iframe playback deliberately blocked by CSP for layout inspection after live screenshots timed out. YouTube thumbnails remain remote and may fail. This is not a live performance or playback audit. No transformations to the original layout or animations. Original material is local research input, not distributed.'
    (dest/'SNAPSHOT-NOTE.txt').write_text(note,encoding='utf-8')
    print('Snapshot ready; '+str(len(paths))+' local posters.')

if __name__=='__main__':main()
