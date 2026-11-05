"""Static artifact checks; browser playback and visual inspection remain separate."""
import argparse
import json
from pathlib import Path
from urllib.parse import urlsplit, unquote
from bs4 import BeautifulSoup

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('cases',nargs='+')
    args=parser.parse_args()
    root=Path(__file__).resolve().parents[1]/'outputs/benchmarks'
    for case in args.cases:
        folder=root/case/'revised'
        page=BeautifulSoup((folder/'index.html').read_text(encoding='utf-8'),'html.parser')
        ids=[n['id'] for n in page.select('[id]')]
        assert len(ids)==len(set(ids)),case+': duplicate ids'
        for node in page.select('[src],[href]'):
            url=node.get('src') or node.get('href')
            parsed=urlsplit(url)
            if parsed.scheme:continue
            if parsed.path:assert (folder/unquote(parsed.path)).exists(),url
            elif parsed.fragment:assert parsed.fragment in ids,url
        data=json.loads(page.select_one('#media-data').string)
        media_ids={m['id'] for m in data['media']}
        assert len(media_ids)==len(data['media'])
        for media in data['media']:
            for key in ['file','poster']:assert (folder/media[key]).is_file(),media[key]
        for group in data['comparisons']:assert set(group['media'])<=media_ids
        print(case+': local assets, anchors, IDs and media references passed')

if __name__=='__main__':main()
