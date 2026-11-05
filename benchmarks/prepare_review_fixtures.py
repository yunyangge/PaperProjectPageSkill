"""Build local inspection fixtures; original source stays in ignored outputs."""
from pathlib import Path
import json
import shutil
import re
import hashlib
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

CASE=Path(__file__).resolve().parents[1]/'outputs/benchmarks/helios'

def main():
    fault=CASE/'fault-test';fault.mkdir(exist_ok=True)
    page=BeautifulSoup((CASE/'revised/index.html').read_text(encoding='utf-8'),'html.parser')
    data=json.loads(page.select_one('#media-data').string)
    data['media'][3]['file']='../assets/intentionally-missing.mp4'
    page.select_one('#media-data').string=json.dumps(data).replace('</','<\\/')
    (fault/'index.html').write_text(str(page),encoding='utf-8')
    for file in ['helios.css','player.js']:shutil.copy2(CASE/'revised'/file,fault/file)

    snapshot=CASE/'original-snapshot';snapshot.mkdir(exist_ok=True)
    base='https://pku-yuangroup.github.io/Helios-Page/'
    def localize(url):
        suffix=Path(url.split('?',1)[0]).suffix
        name='resource-'+hashlib.sha256(url.encode()).hexdigest()[:12]+suffix
        target=snapshot/name
        if not target.exists():
            response=requests.get(url,timeout=40);response.raise_for_status()
            if suffix=='.css':
                css=response.content.decode('utf-8')
                def replace(match):
                    item=match[1].strip(' \"\'')
                    if item.startswith('data:'):return match[0]
                    return 'url('+localize(urljoin(url,item))+')'
                css=re.sub(r'url\(([^)]+)\)',replace,css)
                target.write_text(css,encoding='utf-8')
            else:target.write_bytes(response.content)
        return name
    soup=BeautifulSoup((CASE/'sources/original.html').read_text(encoding='utf-8'),'html.parser')
    # Only eliminate remote subresource dependency, retaining layout and inline source.
    policy=soup.new_tag('meta',attrs={'http-equiv':'Content-Security-Policy','content':"default-src 'self' data:; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; frame-src 'none'"})
    soup.head.insert(0,policy)
    for link in soup.find_all('link',href=True):
        link['href']=localize(urljoin(base,link['href']))
    for style in soup.find_all('style'):
        style.string=re.sub(r"url\(['\"]?([^)'\"]+)['\"]?\)",lambda m:'url('+localize(urljoin(base,m[1]))+')',style.string or '')
    for img in soup.find_all('img'):
        source=img.get('src')
        if not source:continue
        response=requests.get(urljoin('https://pku-yuangroup.github.io/Helios-Page/',source),timeout=40)
        response.raise_for_status()
        target=snapshot/Path(source).name;target.write_bytes(response.content);img['src']=target.name
    (snapshot/'index.html').write_text(str(soup),encoding='utf-8')
    (snapshot/'SNAPSHOT-NOTE.txt').write_text('Local rendering of author HTML retrieved 2026-11-05. Layout, CSS/JS, image and font resources retained. Stylesheet/font URLs rewritten to locally downloaded copies. CSP blocks remote resources (including YouTube embeds); missing clips are not evidence of live-site failure. This fixture supports layout inspection only, not a live performance audit.',encoding='utf-8')
    print('Created fault-test and original-snapshot fixtures.')

if __name__=='__main__':main()
