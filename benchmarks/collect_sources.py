"""Collect primary paper PDFs and independent citation-index candidates."""
from pathlib import Path
import hashlib
import json
import requests
import pymupdf

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'outputs' / 'benchmarks'
CASES = [
    ('helios','2603.04379','Helios: Real Real-Time Long Video Generation Model'),
    ('echo-infinity','2606.04527','Echo-Infinity: Learning Evolving Memory for Real-Time Infinite Video Generation'),
    ('sage-grpo','2603.21872','Manifold-Aware Exploration for Reinforcement Learning in Video Generation'),
]

def collect(case):
    slug, arxiv, title = case
    folder = OUT / slug / 'sources'
    folder.mkdir(parents=True, exist_ok=True)
    record = {'slug':slug,'title':title,'arxiv':arxiv,'checked_date':'2026-11-05','errors':[]}
    url = 'https://arxiv.org/pdf/' + arxiv
    record['pdf_url'] = url
    try:
        pdf = folder / 'paper.pdf'
        if not pdf.exists():
            response = requests.get(url,timeout=90)
            response.raise_for_status()
            if not response.content.startswith(b'%PDF'): raise ValueError('Not a PDF')
            pdf.write_bytes(response.content)
        document = pymupdf.open(pdf)
        record['pages'] = len(document)
        record['sha256'] = hashlib.sha256(pdf.read_bytes()).hexdigest()
        text = '\n\n'.join(f'--- PDF PAGE {i+1} ---\n{page.get_text()}' for i,page in enumerate(document))
        (folder/'paper.txt').write_text(text,encoding='utf-8')
        for i in range(min(3,len(document))):
            document[i].get_pixmap(matrix=pymupdf.Matrix(1.5,1.5), annots=False).save(folder/f'page-{i+1}.png')
    except Exception as exc: record['errors'].append('PDF: '+str(exc))
    for provider,url,params in [
        ('openalex','https://api.openalex.org/works',{'search':title,'per-page':3}),
        ('semantic_scholar',f'https://api.semanticscholar.org/graph/v1/paper/ARXIV:{arxiv}',{'fields':'title,year,citationCount,influentialCitationCount,url,externalIds'}),
    ]:
        try:
            response=requests.get(url,params=params,timeout=35)
            response.raise_for_status()
            data=response.json()
            (folder/f'{provider}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
            record[provider]=([{'id':r['id'],'title':r['title'],'cited_by_count':r['cited_by_count'],'doi':r.get('doi')} for r in data.get('results',[])] if provider=='openalex' else data)
        except Exception as exc: record['errors'].append(provider+': '+str(exc))
    (folder/'provenance.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
    return record

if __name__=='__main__':
    records = [collect(case) for case in CASES]
    (OUT/'sources.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(records,ensure_ascii=False,indent=2))
