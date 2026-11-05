"""Generate the original Echo study page. Baseline is write-once."""
from pathlib import Path
import argparse
import html
import json
import shutil
import pymupdf

ROOT=Path(__file__).resolve().parents[1]
CASE=ROOT/'outputs/benchmarks/echo-infinity'

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--version',choices=['baseline','revised'],default='revised')
    args=parser.parse_args()
    dest=CASE/args.version
    if args.version=='baseline' and (dest/'index.html').exists():
        raise SystemExit('Baseline is frozen.')
    dest.mkdir(exist_ok=True)
    (CASE/'review').mkdir(exist_ok=True)
    data=json.loads((CASE/'media.json').read_text(encoding='utf-8'))
    original=data['comparisons'][0]
    if args.version=='revised':
        data['comparisons']=[dict(original,id=m,label=next(r['title'] for r in data['media'] if r['id']==m),media=[original['media'][0],m]) for m in original['media'][1:]]
    tabs=''.join(f'<button data-prompt="{i}" aria-pressed="{str(i==0).lower()}">{html.escape(c["label"])}</button>' for i,c in enumerate(data['comparisons']))
    doc=pymupdf.open(CASE/'sources/paper.pdf')
    doc[3].get_pixmap(matrix=pymupdf.Matrix(2,2),clip=pymupdf.Rect(70,74,540,258),annots=False).save(CASE/'assets/method.png')
    hour=data['youtube']['1h']; day=data['youtube']['24h']
    longform=f'''<article><span class="duration">01 h</span><h3>A garden chase</h3><p>One author-hosted hour-long video.</p><a href="https://www.youtube.com/watch?v={hour['youtubeId']}">Watch the 1-hour result ↗</a><details><summary>Read the prompt</summary><p>{html.escape(hour['prompt'])}</p></details></article><article><span class="duration">24 h</span><h3>A watercolor cat</h3><p>Two consecutive 12-hour parts. Uploads are compressed by the authors.</p><div class="resources">'''
    for part in day['parts']:
        longform+=f'<a href="https://www.youtube.com/watch?v={part["youtubeId"]}">Part {part["n"]} ↗</a>'
    longform+=f'</div><details><summary>Read the prompt</summary><p>{html.escape(day["prompt"])}</p></details></article>'
    document='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Echo-Infinity — Learning Evolving Memory</title><meta name="description" content="Explore Echo-Infinity's long video outputs, timed prompts and author-provided comparisons."><link rel="stylesheet" href="echo.css"></head><body class="__VERSION__">
<a class="skip" href="#showcase">Skip to results</a><nav><div class="wrap nav-inner"><a class="wordmark" href="#top">echo<span>∞</span></a><div><a href="#comparison">Compare</a><a href="#interactive">Interact</a><a href="#method">Method</a><a href="https://arxiv.org/abs/2606.04527">Paper ↗</a></div></div></nav>
<main id="top" class="wrap"><header class="hero"><div class="intro"><p class="eyebrow">Echo-Infinity / video generation</p><h1>A scene unfolds.<br><em>Memory evolves.</em></h1><p class="subtitle">Learning Evolving Memory for Real-Time Infinite Video Generation</p><div class="resources"><a class="primary" href="https://arxiv.org/abs/2606.04527">Read paper ↗</a><a href="https://github.com/Echo-Team-Joy-Future-Academy-JD/Echo-Infinity">Code ↗</a><a href="#longform">Hour-scale results ↓</a></div></div>
<div class="hero-media" id="showcase"><div data-media="reef"></div></div>
<div class="hero-note"><span class="eyebrow">Watch across time</span><p>Follow a moving camera through a coral-lined world. This four-minute author showcase opens the gallery.</p><div class="mini-stats"><b>1.3B</b><span>Wan2.1 backbone</span><b>18.5 FPS</b><span>reported generation throughput<br>one H100 · 832 × 480</span></div><p class="fine">Files below play at 16 fps. The paper reports up to 24-hour rollouts; this local clip is 3:59.81.</p></div>
<div class="authors"><p>Yuxuan Bian¹ · Zeyue Xue² · Songchun Zhang³ · Shiyi Zhang⁴ · Weiyang Jin⁵ · Yaowei Li⁶<br>Junhao Zhuang⁴ · Haoran Li⁷ · Jie Huang² · Haoyang Huang² · Nan Duan²† · Qiang Xu¹†</p><details><summary>Affiliations & author notes</summary><p>¹ The Chinese University of Hong Kong · ² Joy Future Academy, JD · ³ The Hong Kong University of Science and Technology · ⁴ Tsinghua University · ⁵ The University of Hong Kong · ⁶ Peking University · ⁷ University of Science and Technology of China<br>† Corresponding authors.</p></details></div></header>
<section id="comparison"><div class="section-head"><div><p class="eyebrow">01 / Compare the trajectory</p><h2>Same prompt.<br>Four ways forward.</h2></div><p>Follow the astronaut’s suit, body and surroundings through the sequence. Inspect early and late behavior using the same playback time.</p></div><div class="compare-panel"><div class="compare-toolbar"><div class="prompt-tabs" aria-label="Comparison method">__TABS__</div><div class="play-actions"><button data-action="play">Play together</button><button data-action="restart">Replay</button></div></div><div class="checkpoint-row"><span>Jump to a shared time</span><div class="checkpoints"></div></div><div class="compare-grid"></div><div class="timeline"><label for="time">Time</label><input id="time" type="range" min="0" max="239.8" step="0.1"><output></output></div><p role="status" class="status"></p><p class="fine">Author-provided same-prompt outputs · all 832 × 480 / 16 fps. Per-file seeds are not supplied in the gallery. Group playback stops at the common endpoint; it is coordinated, not frame-locked.</p><details><summary>Read shared prompt</summary><p class="shared-prompt"></p></details></div></section>
<section id="interactive"><div class="section-head"><div><p class="eyebrow">02 / A change of instruction</p><h2>Six prompts.<br>One continuous minute.</h2></div><p>Standing, running, jumping, then stopping. Inspect how the result follows successive ten-second instructions.</p></div><div class="interactive-layout"><div data-media="interactive"></div><div class="prompt-story"><h3>Prompt sequence</h3><p class="fine">Author-supplied schedule: six × 10s. Encoded video ends at 59.81s.</p><div class="chapters"></div><p class="active-prompt"></p><details><summary>Read all six prompts</summary><ol class="all-prompts"></ol></details></div></div></section>
<section id="longform"><div class="section-head"><div><p class="eyebrow">03 / Different horizons</p><h2>From a moment<br>to a day.</h2></div><p>Browse a short scene here, or open the authors’ full-length videos. Each link keeps its own prompt and duration.</p></div><div class="horizons"><div data-media="coast"></div><div class="long-links">__LONGFORM__</div></div><p class="fine">Hour/day-scale results are qualitative demonstrations. The paper notes reduced stability in highly dynamic scenes and leaves targeted day-scale quantitative evaluation open.</p></section>
<section id="method"><div class="section-head"><div><p class="eyebrow">04 / Behind the continuity</p><h2>Keep what matters.</h2></div><p>A fixed-capacity memory learns from evicted history; a bounded position schedule keeps generation inside the trained temporal range.</p></div><figure class="method"><img src="../assets/method.png" alt="Echo-Infinity memory-query attention and gated update, with growth and mature phases of the relative RoPE schedule." loading="lazy"><figcaption>Figure 3 · paper p.4. Memory is updated by attention and a gate, then reused as keys and values.</figcaption></figure><div class="method-notes"><p><b>Learn a memory.</b> Queries consolidate the history that leaves the local window. Active memory cost stays independent of generated length.</p><p><b>Bound the positions.</b> Relative RoPE is shared during training and inference. This avoids extrapolating temporal position IDs beyond the trained range.</p></div></section>
<section id="evidence"><div class="section-head"><div><p class="eyebrow">05 / Reported evidence</p><h2>Long-horizon quality.</h2></div><p>240s quality scores from Table 1. All rows retained for this selected metric; the paper contains the full multi-metric evaluation.</p></div><div class="table-wrap"><table><thead><tr><th>Method</th><th>240s quality ↑</th><th>Throughput FPS ↑</th></tr></thead><tbody><tr><td>LongLive</td><td>79.79</td><td>20.7</td></tr><tr><td>MemFlow</td><td>79.31</td><td>18.7</td></tr><tr><td>Memorize-and-Generate</td><td>75.49</td><td>21.7</td></tr><tr><td>∞-RoPE</td><td>79.99</td><td>17.0</td></tr><tr class="ours"><td>Echo-Infinity</td><td>81.23</td><td>18.5</td></tr></tbody></table></div><p class="fine">Paper-reported, not reproduced here. 128 MovieGen prompts; six VBench-Long quality metrics with official weights. Appendix B reports five seeds per prompt and one H100 for throughput. Quality and speed express different tradeoffs.</p></section>
<section class="citation"><h2>Echo-Infinity, 2026.</h2><details><summary>Citation</summary><pre>@article{bian2026echoinfinity,
  title={Echo-Infinity: Learning Evolving Memory for Real-Time Infinite Video Generation},
  author={Bian, Yuxuan and Xue, Zeyue and Zhang, Songchun and Zhang, Shiyi and Jin, Weiyang and Li, Yaowei and Zhuang, Junhao and Li, Haoran and Huang, Jie and Huang, Haoyang and Duan, Nan and Xu, Qiang},
  journal={arXiv preprint arXiv:2606.04527},
  year={2026}
}</pre></details></section></main><footer class="wrap">Independent local design study for PaperProjectPageSkill. Not the official website. Paper, figure, prompts and videos belong to the authors; clip source links accompany each result. <a href="https://echo-team-joy-future-academy-jd.github.io/Echo-Infinity/">Official project ↗</a></footer><script id="media-data" type="application/json">__DATA__</script><script src="player.js" defer></script></body></html>'''
    document=document.replace('__VERSION__',args.version).replace('__TABS__',tabs).replace('__LONGFORM__',longform).replace('__DATA__',json.dumps(data,ensure_ascii=False).replace('</','<\\/'))
    if args.version=='revised':
        document=document.replace('<h1>A scene unfolds.<br>', '<h1>Echo-Infinity.<br>')
        document=document.replace('<div class="prompt-tabs"', '<span class="fine">Compare Echo-Infinity with</span><div class="prompt-tabs"')
        document=document.replace('class="compare-toolbar"','class="compare-toolbar revised-toolbar"')
    (dest/'index.html').write_text(document,encoding='utf-8')
    shutil.copy2(ROOT/'benchmarks/web/echo.css',dest/'echo.css')
    player=(ROOT/'benchmarks/web/player.js').read_text(encoding='utf-8').replace('[0,20,40,59]','[0,60,120,230]').replace('Inspect both videos','Inspect compared videos')
    if args.version=='revised':
        # Preserve the inspected moment when switching the baseline for this one prompt.
        player=player.replace('let epoch=0, group=[]', 'let comparisonTime=0;\nlet epoch=0, group=[]')
        player=player.replace('timeline.value=v.currentTime;', 'comparisonTime=v.currentTime;timeline.value=v.currentTime;')
        player=player.replace('async function seek(value,restart=false) {','async function seek(value,restart=false) {\n  comparisonTime=value;')
        player=player.replace('b.onclick=()=>select(i)', 'b.onclick=()=>{const retained=comparisonTime;select(i);if(retained>0)seek(retained);} ')
    player+='\n'+(ROOT/'benchmarks/web/echo-prompts.js').read_text(encoding='utf-8')
    if args.version=='baseline':
        player=(ROOT/'benchmarks/web/echo-player-baseline.js').read_text(encoding='utf-8')
    (dest/'player.js').write_text(player,encoding='utf-8')
    print(dest/'index.html')

if __name__=='__main__':main()
