"""Collect selected author media for the local Echo-Infinity design study."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import json
import re
import requests
import pymupdf
import prepare_helios as media_tools

ROOT = Path(__file__).resolve().parents[1]
CASE = ROOT / 'outputs/benchmarks/echo-infinity'
BASE = 'https://echo-team-joy-future-academy-jd.github.io/Echo-Infinity/'

def main():
    assets = CASE / 'assets'
    assets.mkdir(exist_ok=True)
    source = CASE / 'sources/prompts.js'
    if not source.exists():
        r = requests.get(BASE + 'data/prompts.js', timeout=40)
        r.raise_for_status()
        source.write_text(r.content.decode('utf-8'), encoding='utf-8')
    text = source.read_text(encoding='utf-8')
    # Parse data literals only; never execute the downloaded JavaScript.
    raw = text.split('window.PROMPTS = ', 1)[1].split('\n};', 1)[0] + '\n}'
    raw = re.sub(r"(?m)^(\s*)'([^']+)':", r'\1"\2":', raw)
    raw = re.sub(r',\s*([}\]])', r'\1', raw)
    prompts = json.loads(raw)
    youtube = json.loads(text.split('window.YOUTUBE_VIDEOS = ', 1)[1].split('\n};', 1)[0] + '\n}')
    records = []
    for ident, length, case, title, cue in [
        ('reef', '240s', '7', 'Four minutes under water', 'Follow the camera through coral-lined streets; inspect whether the scene stays recognizable.'),
        ('coast', '30s', '10', 'A shorter horizon', 'Watch the reflections, waves and changing light.'),
        ('interactive', '60s', '1', 'Six instructions. One minute.', 'Watch the action change at each ten-second prompt boundary.')]:
        prompt = prompts[length][case]
        records.append(dict(id=ident, source=BASE+f'videos/{length}/{case}.mp4', title=title, cue=cue,
                            prompt=prompt if isinstance(prompt,str) else '', prompts=prompt if isinstance(prompt,list) else [],
                            task=length, method='Echo-Infinity'))
    ids=[]
    for method, title in [('ours','Echo-Infinity'),('longlive','LongLive'),('memflow','MemFlow'),('memorize','Memorize-and-Generate')]:
        ident='astronaut-'+method
        ids.append(ident)
        records.append(dict(id=ident, source=BASE+f'videos/compare/240s/2/{method}.mp4', title=title,
                            prompt=prompts['240s']['5'], task='240s comparison', method=title))
    media_tools.ASSETS = assets
    with ThreadPoolExecutor(max_workers=3) as pool:
        records = list(pool.map(media_tools.prepare, records))
    manifest=dict(project='Echo-Infinity',source_page=BASE,retrieved='2026-11-05',
                  usage='Local research study only; author video files unchanged. Do not redistribute.',
                  media=records,youtube={'1h':youtube['1h'][4],'24h':youtube['24h'][0]},
                  comparisons=[dict(id='astronaut',label='Astronaut in Rio',prompt=prompts['240s']['5'],media=ids)])
    (CASE/'media.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    doc=pymupdf.open(CASE/'sources/paper.pdf')
    for page in [4,6,9,17,20,21]:
        doc[page-1].get_pixmap(matrix=pymupdf.Matrix(1.3,1.3),annots=False).save(CASE/f'sources/page-{page}.png')
    print(json.dumps([dict(id=r['id'],seconds=r['duration'],width=r['width'],height=r['height'],fps=r['fps'],MB=round(r['bytes']/1e6,1)) for r in records]))

if __name__=='__main__': main()
