"""Save public project markup and inventory assets, without borrowing styles."""
from pathlib import Path
from urllib.parse import urljoin
import json
import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1] / 'outputs' / 'benchmarks'
SITES = {
    'helios': 'https://pku-yuangroup.github.io/Helios-Page/',
    'echo-infinity': 'https://echo-team-joy-future-academy-jd.github.io/Echo-Infinity/',
    'sage-grpo': 'https://dungeonmassster.github.io/SAGE-GRPO-Page/',
}

def inventory(slug, url):
    folder = ROOT / slug / 'sources'
    response = requests.get(url, timeout=45)
    response.raise_for_status()
    response.encoding = 'utf-8'
    (folder / 'original.html').write_text(response.text, encoding='utf-8')
    soup = BeautifulSoup(response.text, 'html.parser')
    records = []
    for tag in soup.find_all(['video', 'img', 'script']):
        source = tag.get('src') or tag.get('data-src')
        if not source and tag.name == 'video':
            child = tag.find('source')
            if child: source = child.get('src') or child.get('data-src')
        heading = tag.find_previous(['h1','h2','h3','h4'])
        records.append({'tag':tag.name,'source':urljoin(url,source) if source else None,
                        'id':tag.get('id'),'heading':heading.get_text(' ',strip=True) if heading else None,
                        'attributes':tag.attrs,'context':tag.parent.get_text(' ',strip=True)[:2400]})
    (folder / 'media-inventory.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'slug':slug,'asset_count':len(records)}))

if __name__ == '__main__':
    for slug,url in SITES.items(): inventory(slug,url)
