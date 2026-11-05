"""Build an original, local-only paper page from the frozen research brief."""
from pathlib import Path
import json
import shutil
import argparse
import pymupdf
from bs4 import BeautifulSoup

ROOT=Path(__file__).resolve().parents[1]
CASE=ROOT/'outputs/benchmarks/helios'

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--version',choices=['baseline','revised'],default='revised')
    args=parser.parse_args()
    DEST=CASE/args.version
    if args.version=='baseline' and (DEST/'index.html').exists():
        raise SystemExit('Baseline is frozen; use --version revised.')
    DEST.mkdir(exist_ok=True)
    media=json.loads((CASE/'media.json').read_text(encoding='utf-8'))
    doc=pymupdf.open(CASE/'sources/paper.pdf')
    doc[4].get_pixmap(matrix=pymupdf.Matrix(2,2),clip=pymupdf.Rect(82,73,532,270),annots=False).save(CASE/'assets/method.png')
    shutil.copy2(ROOT/'benchmarks/web/helios.css',DEST/'helios.css')
    player='player-baseline.js' if args.version=='baseline' else 'player.js'
    shutil.copy2(ROOT/'benchmarks/web'/player,DEST/'player.js')
    html='''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Helios — Real Real-Time Long Video Generation</title>
<meta name="description" content="Explore minute-scale Helios video generation, author-provided comparisons, and the method behind a 14B real-time model.">
<link rel="stylesheet" href="helios.css"></head><body>
<a class="skip" href="#showcase">Skip to videos</a>
<nav aria-label="Page navigation"><div class="wrap nav-inner"><a class="wordmark" href="#top">HELIOS</a><div class="nav-links"><a href="#showcase">Showcase</a><a href="#comparison">Compare</a><a href="#method">Method</a><a href="https://arxiv.org/abs/2603.04379">Paper ↗</a></div></div></nav>
<main class="wrap" id="top">
<header class="hero"><div><span class="eyebrow">14B · Autoregressive video generation</span><h1>Helios<span style="color:var(--accent)">.</span></h1>
<p class="subtitle">Real real-time.<br>Minute-scale video.</p><p class="lede">A unified model for text, image and video conditioning. Explore a full minute of generation, then compare the motion over time.</p>
<div class="authors">Shenghai Yuan<sup>1,2,◦</sup> · Yuanyang Yin<sup>2,4,◦</sup><br>Zongjian Li<sup>1</sup> · Xinwei Huang<sup>2</sup><br>Xiao Yang<sup>3,§</sup> · Li Yuan<sup>1,†</sup>
<div class="affiliations">¹ Peking University · ² ByteDance China<br>³ Canva · ⁴ Chengdu Anu Intelligence</div><details><summary>Author notes</summary><p>◦ Work done during internship at ByteDance. § Project leader. † Corresponding author.</p></details></div>
<div class="resources"><a href="https://arxiv.org/abs/2603.04379">Read paper ↗</a><a href="https://github.com/PKU-YuanGroup/Helios">Code ↗</a><a href="https://pku-yuangroup.github.io/Helios-Page/">Author website ↗</a></div></div>
<div data-media="reef"></div></header>
<div class="metrics"><div><b>14B</b><span>model parameters</span></div><div><b>19.53 FPS</b><span>end-to-end generation throughput</span></div><div><b>1 × H100</b><span>384 × 640 evaluation resolution</span></div></div>
<p class="metric-note">Helios-Distilled · paper §5.1 / Table 3 · includes text encoder and VAE. Showcase files play at 24 fps; the author gallery does not specify their model variant.</p>
<section class="section" id="showcase"><div class="section-head"><div><span class="section-number">01 / Explore the outputs</span><h2>Keep the scene alive.</h2></div><p>Two more ways to inspect motion and appearance. These are selected author showcases, not aggregate quality measurements.</p></div><div class="gallery"><div data-media="museum"></div><div data-media="train"></div></div></section>
<section class="section" id="comparison"><div class="section-head"><div><span class="section-number">02 / Look across time</span><h2>One prompt.<br>Two trajectories.</h2></div><p>Compare scene continuity and motion in paired results from the author website. Let the full minute play, or seek to a later point.</p></div>
<div class="compare-panel"><div class="compare-toolbar"><div class="prompt-tabs" aria-label="Comparison prompt"><button data-prompt="0" aria-pressed="true">Desert explorer</button><button data-prompt="1" aria-pressed="false">Tokyo street</button></div><div class="play-actions"><button data-action="play">Play together</button><button data-action="restart">Replay</button></div></div>
<div class="compare-grid"></div><div class="timeline"><label for="comparison-time">Time</label><input id="comparison-time" type="range" min="0" max="60" step="0.1" value="0"><output for="comparison-time">0:00</output></div><p class="status" role="status"></p>
<p class="comparison-note">Same author-supplied prompt; source resolutions differ (640 × 384 vs 832 × 480). Seeds and per-clip sampling settings are not supplied here. Original proportions and playback speed are preserved. Group playback stops at the common endpoint.</p><details><summary>Read shared prompt</summary><p class="shared-prompt"></p></details></div></section>
<section class="section" id="method"><div class="section-head"><div><span class="section-number">03 / Behind the motion</span><h2>Continue. Stabilize. Compress.</h2></div><p>The model turns generation into continuation from a compact history. Three parts work together to sustain long sequences.</p></div>
<div class="method-layout"><figure><div class="method-figure"><img src="../assets/method.png" alt="Helios architecture showing historical and noisy contexts, multi-term memory patchification, guidance attention, and pyramid prediction." loading="lazy"></div><figcaption><span class="meta">Figure 4, paper p.5. View the paper for the full-resolution diagram.</span></figcaption></figure><div class="method-copy"><article><h3>01 — Reuse the history</h3><p>Unified History Injection conditions each new chunk on the past, with a common representation for text, image and video inputs.</p></article><article><h3>02 — Train for imperfect context</h3><p>Relative positions, a first-frame anchor and frame-aware corruption address position, color and restoration drift.</p></article><article><h3>03 — Spend less per frame</h3><p>Multi-scale history and noisy-context compression reduce tokens. Hierarchical distillation reduces 50 sampling steps to 3.</p></article></div></div></section>
<section class="section" id="evidence"><div class="section-head"><div><span class="section-number">04 / Reported evidence</span><h2>The speed–quality tradeoff.</h2></div><p>The three Helios stages trade computation for speed. Selected rows from Table 3; these figures are paper-reported, not reproduced in this study.</p></div>
<div class="table-wrap"><table><thead><tr><th scope="col">Model</th><th scope="col">Parameters</th><th scope="col">Generation FPS ↑</th><th scope="col">Short-video total ↑</th></tr></thead><tbody><tr><th scope="row">Helios-Base</th><td>14B</td><td>0.54</td><td>6.35</td></tr><tr><th scope="row">Helios-Mid</th><td>14B</td><td>1.05</td><td>6.25</td></tr><tr><th scope="row">Helios-Distilled</th><td>14B</td><td>19.53</td><td>6.00</td></tr></tbody></table></div>
<p class="evidence-note">Table 3 evaluates 81-frame quality on 240 prompts. Throughput uses each model’s default length at 384 × 640 on one H100, including officially supported acceleration. The total aggregates five discretized metric ratings; see Appendix A for weights. Full baselines remain in the paper.</p>
<p class="evidence-note"><strong>Limits:</strong> stitching boundaries may flicker. The paper evaluates up to 384 × 640 and does not design a dedicated long-video memory mechanism (§8).</p></section>
<section class="section" id="cite"><span class="section-number">05 / Cite this work</span><h2>Helios, 2026.</h2><pre class="citation">@article{yuan2026helios,
  title={Helios: Real Real-Time Long Video Generation Model},
  author={Yuan, Shenghai and Yin, Yuanyang and Li, Zongjian and
          Huang, Xinwei and Yang, Xiao and Yuan, Li},
  journal={arXiv preprint arXiv:2603.04379},
  year={2026}
}</pre></section>
</main><footer><div class="wrap"><p>Independent local design study for PaperProjectPageSkill. Not an official Helios website. Paper, figure and videos belong to the original authors; videos are presented unchanged and credited through their source links. Original page implementation by this study.</p><a href="https://pku-yuangroup.github.io/Helios-Page/">Visit the official project ↗</a></div></footer>
<script type="application/json" id="media-data">__MEDIA__</script><script src="player.js" defer></script></body></html>'''
    html=html.replace('__MEDIA__',json.dumps(media,ensure_ascii=False).replace('</','<\\/'))
    if args.version=='revised':
        soup=BeautifulSoup(html,'html.parser')
        hero=soup.select_one('.hero')
        authors=hero.select_one('.authors').extract()
        hero.append(authors)
        hero.select_one('.lede').string='A 14B model for minute-scale video. Watch scene and motion evolve, then compare the full sequence.'
        hero.select_one('.resources a:last-child').decompose()
        compare=soup.select_one('.compare-panel')
        checkpoints=soup.new_tag('div',attrs={'class':'checkpoint-row'})
        label=soup.new_tag('span');label.string='Inspect later frames'
        buttons=soup.new_tag('div',attrs={'class':'checkpoints','aria-label':'Comparison time checkpoints'})
        checkpoints.extend([label,buttons])
        compare.select_one('.compare-grid').insert_before(checkpoints)
        style=soup.new_tag('style')
        style.string='''.hero{grid-template-areas:"intro video" "authors video";row-gap:0}.hero>div:first-child{grid-area:intro}.hero>[data-media]{grid-area:video}.hero>.authors{grid-area:authors;margin-top:22px}.compare-grid figcaption{margin:0 0 10px}.checkpoint-row{display:flex;justify-content:space-between;align-items:center;gap:12px;margin-bottom:18px;font-size:12px;color:var(--muted)}.checkpoints{display:flex;gap:8px}.checkpoints button{background:transparent;color:var(--text);border:1px solid #555a60;padding:7px 14px;border-radius:3px}.checkpoints button:hover{border-color:var(--accent);color:var(--accent)}@media(max-width:700px){.hero>div:first-child{order:0}.hero>[data-media]{order:1}.hero>.authors{order:2;margin:0}.hero{gap:22px}.hero h1{font-size:66px}.hero .subtitle{margin:14px 0}.hero .lede{margin:12px 0}.hero .resources{margin-top:16px}.checkpoint-row{align-items:start;flex-direction:column;gap:8px}.checkpoints{width:100%;justify-content:space-between}.checkpoints button{min-height:40px;padding:8px 14px}.compare-toolbar button{min-height:42px}.compare-grid figcaption{display:flex;flex-direction:column}.compare-grid{gap:18px}}'''
        soup.head.append(style)
        html=str(soup)
    (DEST/'index.html').write_text(html,encoding='utf-8')
    print(DEST/'index.html')

if __name__=='__main__': main()
