"""Prepare attributed local research media; do not redistribute with the skill."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import hashlib
import json
import re
import subprocess
import requests
import pymupdf
import imageio_ffmpeg
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
CASE = ROOT / 'outputs/benchmarks/helios'
ASSETS = CASE / 'assets'
BASE = 'https://pku-yuangroup.github.io/Helios-Page/'

def prepare(record):
    target = ASSETS / (record['id'] + '.mp4')
    if not target.exists():
        response = requests.get(record['source'], timeout=120)
        response.raise_for_status()
        target.write_bytes(response.content)
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    probe = subprocess.run([ffmpeg,'-hide_banner','-i',str(target)],capture_output=True,text=True).stderr
    (ASSETS / (record['id'] + '.probe.txt')).write_text(probe,encoding='utf-8')
    duration = re.search(r'Duration: (\d+):(\d+):([\d.]+)',probe)
    size = re.search(r'Video:.*? (\d{2,5})x(\d{2,5})',probe)
    fps = re.search(r'([\d.]+) fps',probe)
    if not duration or not size: raise ValueError('Cannot probe '+record['id'])
    h,m,s = map(float,duration.groups())
    record.update({'duration':3600*h+60*m+s,'width':int(size[1]),'height':int(size[2]),
                   'fps':float(fps[1]) if fps else None,'bytes':target.stat().st_size,
                   'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),
                   'file':'../assets/'+target.name,'poster':'../assets/'+record['id']+'.jpg'})
    subprocess.run([ffmpeg,'-v','error','-y','-ss','1','-i',str(target),'-frames:v','1','-q:v','2',str(ASSETS/(record['id']+'.jpg'))],check=True)
    return record

def main():
    ASSETS.mkdir(exist_ok=True)
    html=(CASE/'sources/original.html').read_text(encoding='utf-8')
    soup=BeautifulSoup(html,'html.parser')
    records=[]
    for slug,path,title,cue in [
        ('reef','text_to_video_showcases/checkpoint-10000_1.mp4','A scene that keeps moving','Watch the fish, coral and camera motion across the full sequence.'),
        ('museum','text_to_video_short_showcases/16_720_ori725.mp4','Motion and fine detail','Watch the camera move around the stacked television screens.'),
        ('train','text_to_video_short_showcases/19_720_ori725.mp4','A different visual language','Watch the illustrated passenger and the changing reflections.')]:
        tag=soup.find('video',attrs={'data-src':'videos/'+path})
        prompt=tag.parent.select_one('.prompt').get_text(' ',strip=True)
        records.append({'id':slug,'source':BASE+'videos/'+path,'title':title,'cue':cue,'prompt':prompt,'task':'Text-to-video','method':'Helios (author showcase; variant not specified)'})
    block=html.split('const promptData_Long = {',1)[1].split('function renderLong',1)[0]
    comparisons=[]
    for key,label in [('prompt1','Desert explorer'),('prompt3','Tokyo street')]:
        part=block.split(key+': {',1)[1].split('suffix:',1)
        prompt=re.search(r'text: "(.*?)",',part[0],re.S)[1]
        suffix=re.search(r'"(\d+)"',part[1])[1]
        ids=[]
        for method,name in [('helios','Helios'),('rollingforcing','Rolling Forcing')]:
            slug=f'{key}-{method}'
            ids.append(slug)
            records.append({'id':slug,'source':BASE+f'videos/long_video_comparison/{method}_{suffix}.mp4','title':name,'prompt':prompt,'task':'Long-video comparison','method':name})
        comparisons.append({'id':key,'label':label,'prompt':prompt,'media':ids})
    with ThreadPoolExecutor(max_workers=3) as pool:
        records=list(pool.map(prepare,records))
    manifest={'project':'Helios','source_page':BASE,'retrieved':'2026-11-05',
              'usage':'Local research study only; media rights remain with their authors. No source video transformations.',
              'media':records,'comparisons':comparisons}
    (CASE/'media.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    doc=pymupdf.open(CASE/'sources/paper.pdf')
    for page in [5,16,19,31,39]:
        doc[page-1].get_pixmap(matrix=pymupdf.Matrix(1.5,1.5),annots=False).save(CASE/f'sources/page-{page}.png')
    print(json.dumps([{'id':r['id'],'seconds':r['duration'],'size':[r['width'],r['height']],'fps':r['fps'],'MB':round(r['bytes']/1e6,1)} for r in records]))

if __name__=='__main__': main()
