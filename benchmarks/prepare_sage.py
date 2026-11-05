"""Prepare attributable SAGE-GRPO study media without redistributing it."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import json
import requests
import pymupdf
from bs4 import BeautifulSoup
import prepare_helios as media_tools

ROOT=Path(__file__).resolve().parents[1]
CASE=ROOT/'outputs/benchmarks/sage-grpo'
BASE='https://dungeonmassster.github.io/SAGE-GRPO-Page/'

def main():
    assets=CASE/'assets';assets.mkdir(exist_ok=True)
    soup=BeautifulSoup((CASE/'sources/original.html').read_text(encoding='utf-8'),'html.parser')
    grid=soup.find('video',src='./assets/Visual_Results/Compare_with_Baseline/case1_baseline.mp4').find_parent('div',class_='grid')
    prompts=[span.parent.get_text(' ',strip=True).removeprefix('Prompt:').strip() for span in grid.find_all('span') if span.get_text(strip=True)=='Prompt:']
    assert len(prompts)==3
    records=[];groups=[]
    for i,(title,cue) in enumerate([
        ('After the sprint','Watch the breathing, posture and recovery across the full clip.'),
        ('Newton and the apple','Watch the apple, contact with the head, and the following reaction.'),
        ('Five children in a field','Count the children through the sequence; watch limbs and group motion.')],1):
        ids=[]
        for method,label in [('baseline','HunyuanVideo-1.5'),('ours_full','SAGE-GRPO')]:
            ident=f'case{i}-{method}';ids.append(ident)
            records.append(dict(id=ident,title=label,method=label,prompt=prompts[i-1],source=BASE+f'assets/Visual_Results/Compare_with_Baseline/case{i}_{method}.mp4'))
        groups.append(dict(id=f'case{i}',label=title,cue=cue,prompt=prompts[i-1],media=ids))
    for method,label in [('dancegrpo','DanceGRPO'),('flowgrpo','FlowGRPO'),('cps','CPS'),('ours','SAGE-GRPO')]:
        records.append(dict(id='rl-'+method,title=label,method=label,prompt='Full prompt not supplied in this author gallery section.',source=BASE+f'assets/Visual_Results/Compare_with_Other_methods_20steps/showcase1_{method}.mp4'))
    media_tools.ASSETS=assets
    with ThreadPoolExecutor(max_workers=3) as pool:records=list(pool.map(media_tools.prepare,records))
    data=dict(project='SAGE-GRPO',source_page=BASE,retrieved='2026-11-05',usage='Local design study. Author video files unchanged; do not redistribute.',media=records,comparisons=groups)
    (CASE/'media.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    doc=pymupdf.open(CASE/'sources/paper.pdf')
    for page in [5,6,7,8,15,17]:doc[page-1].get_pixmap(matrix=pymupdf.Matrix(1.4,1.4),annots=False).save(CASE/f'sources/page-{page}.png')
    # Retry the citation index once; never infer an influence count from page design.
    try:
        r=requests.get('https://api.semanticscholar.org/graph/v1/paper/ARXIV:2603.21872',params={'fields':'title,year,citationCount,influentialCitationCount,url,externalIds'},timeout=25)
        r.raise_for_status();(CASE/'sources/semantic_scholar.json').write_text(json.dumps(r.json(),indent=2),encoding='utf-8')
        print(json.dumps({'citation_index':r.json()}))
    except requests.RequestException as e:print('Citation retry: '+str(e))
    print(json.dumps([dict(id=r['id'],seconds=r['duration'],size=[r['width'],r['height']],fps=r['fps'],MB=round(r['bytes']/1e6,1)) for r in records]))

if __name__=='__main__':main()
