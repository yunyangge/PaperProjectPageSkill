"""Original editorial SAGE-GRPO page; the first generated baseline is frozen."""
from pathlib import Path
import argparse
import html
import json
import shutil
import pymupdf

ROOT=Path(__file__).resolve().parents[1]
CASE=ROOT/'outputs/benchmarks/sage-grpo'

def panel(ident,groups,keep=False,revised=False):
    tabs=''.join(f'<button data-prompt="{i}" aria-pressed="{str(i==0).lower()}">{html.escape(g["label"])}</button>' for i,g in enumerate(groups))
    if revised:
        options=''.join(f'<option value="{i}">{html.escape(g["label"])}</option>' for i,g in enumerate(groups))
        tabs+=f'<label class="mobile-select" for="{ident}-select">{"Baseline" if keep else "Example"}<select id="{ident}-select">{options}</select></label>'
    speed='<button class="speed" aria-pressed="false" title="Review speed applies to both clips">Speed: 1×</button>' if revised else ''
    return f'''<div class="compare-panel" data-group="{ident}" data-keep-time="{str(keep).lower()}"><div class="compare-toolbar"><div class="prompt-tabs">{tabs}</div><div class="play-actions"><button data-action="play">Play together</button><button data-action="restart">Replay</button>{speed}</div></div><p class="viewing-cue"></p><div class="compare-grid"></div><div class="timeline"><label for="{ident}-time">Time</label><input id="{ident}-time" type="range" min="0" step="0.04"><output></output></div><p class="status" role="status"></p><details><summary>Read shared prompt</summary><p class="shared-prompt"></p></details></div>'''

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--version',choices=['baseline','revised'],default='revised');args=parser.parse_args()
    dest=CASE/args.version
    if args.version=='baseline' and (dest/'index.html').exists():raise SystemExit('Baseline is frozen.')
    dest.mkdir(exist_ok=True);(CASE/'review').mkdir(exist_ok=True)
    data=json.loads((CASE/'media.json').read_text(encoding='utf-8'))
    data['groups']={'primary':data['comparisons'],'rl':[
        dict(id='rl-'+m,label=label,media=['rl-'+m,'rl-ours'],prompt='Full prompt not supplied in this author gallery section.',cue='Author-paired example at 20 sampling steps. Inspect expression and movement; per-file seeds and complete prompt are not supplied.')
        for m,label in [('dancegrpo','DanceGRPO'),('flowgrpo','FlowGRPO'),('cps','CPS')]]}
    # Keep the generic artifact checker aware of every group.
    data['comparisons']=data['groups']['primary']+data['groups']['rl']
    doc=pymupdf.open(CASE/'sources/paper.pdf')
    doc[4].get_pixmap(matrix=pymupdf.Matrix(2,2),clip=pymupdf.Rect(54,66,556,267),annots=False).save(CASE/'assets/method.png')
    text='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>SAGE-GRPO — Manifold-Aware Exploration</title><meta name="description" content="Inspect paired SAGE-GRPO video results, motion and prompt alignment, followed by the method and reported user preferences."><link rel="stylesheet" href="sage.css"></head><body class="__VERSION__"><a class="skip" href="#comparison">Skip to comparisons</a>
<nav class="wrap"><a class="brand" href="#top">SAGE<span>—</span>GRPO</a><div><a href="#rl">RL methods</a><a href="#method">Method</a><a href="https://arxiv.org/abs/2603.21872">Paper ↗</a></div></nav>
<main class="wrap" id="top"><header><div class="hero-title"><div><p class="eyebrow">Stable Alignment via Exploration / 2026</p><h1>SAGE<span>—</span>GRPO</h1></div><p class="statement">Better exploration.<br><em>See what changes.</em></p></div><p class="paper-title">Manifold-Aware Exploration for Reinforcement Learning in Video Generation</p><div class="resources"><a class="primary" href="https://arxiv.org/abs/2603.21872">Read the paper ↗</a><a href="https://github.com/dungeonmassster/SAGE-GRPO">Code ↗</a><a href="#evidence">Reported evidence ↓</a></div></header>
<section id="comparison" class="opening"><div class="section-line"><span>01 / The original model → SAGE-GRPO</span><span>Same supplied prompt · full clips</span></div>__PRIMARY__<p class="conditions">All selected files: 864 × 480, 24 fps, 5.04s. Source-gallery sampling settings and seeds are not specified for these pairs. Playback stops at the common endpoint; coordinated playback is not frame-locked.</p></section>
<div class="authors"><p>Mingzhe Zheng*¹² · Weijie Kong*² · Yue Wu‡² · Dengyang Jiang¹ · Yue Ma¹ · Xuanhua He¹<br>Bin Lin² · Kaixiong Gong² · Zhao Zhong² · Liefeng Bo² · Qifeng Chen†¹ · Harry Yang†¹</p><p>¹ HKUST · ² Tencent Hunyuan</p><details><summary>Author notes</summary><p>* Equal contribution · † Corresponding authors · ‡ Project leader. Work done during internship at Tencent Hunyuan.</p></details></div>
<section id="rl"><div class="section-head"><div><p class="eyebrow">02 / Other alignment methods</p><h2>Look closer<br>at the motion.</h2></div><p>Select a method to compare with SAGE. These are the authors’ 20-step gallery examples, separate from the 40-step preference study below.</p></div><div class="group-label">Compare SAGE-GRPO with</div>__RL__<p class="conditions">Author-paired sample · 20 sampling steps · 864 × 480 · 24 fps · 3.38s. Complete prompt and per-file seeds are unavailable in this section. Original files and proportions are preserved.</p></section>
<section id="method"><div class="section-head"><div><p class="eyebrow">03 / What changes in training</p><h2>Explore.<br>Balance. Anchor.</h2></div><p>SAGE-GRPO changes how reinforcement learning explores and updates the video model, from noise injection to policy constraints.</p></div><div class="method-copy"><article><span>01</span><h3>Precise exploration</h3><p>Integrate the sampling noise variance with a logarithmic correction to reduce excess injected noise.</p></article><article><span>02</span><h3>Balanced updates</h3><p>Equalize estimated gradient scales across diffusion timesteps, so a few noise levels do not dominate learning.</p></article><article><span>03</span><h3>A moving reference</h3><p>Combine a periodically refreshed anchor with step-wise KL constraints to control drift during training.</p></article></div><figure class="method-figure"><a href="../assets/method.png"><img src="../assets/method.png" alt="SAGE-GRPO framework: manifold-aware sampling, gradient equalization and moving-anchor plus step-wise constraints." loading="lazy"></a><figcaption>Figure 5 · paper p.5. Open the diagram for a larger view.</figcaption></figure></section>
<section id="evidence"><div class="section-head"><div><p class="eyebrow">04 / Reported user preferences</p><h2>Three views<br>of quality.</h2></div><p>Pairwise win rates for SAGE-GRPO in Table 3. 29 evaluators, 32 prompts; iteration 100, 40 sampling steps, alignment-focused Setting B.</p></div><div class="table-wrap"><table><thead><tr><th>SAGE-GRPO vs.</th><th>Visual quality</th><th>Motion quality</th><th>Semantic alignment</th></tr></thead><tbody><tr><th>DanceGRPO</th><td>85.9%</td><td>75.8%</td><td>79.2%</td></tr><tr><th>FlowGRPO</th><td>83.8%</td><td>79.2%</td><td>71.9%</td></tr><tr><th>CPS</th><td>80.2%</td><td>70.8%</td><td>67.9%</td></tr></tbody></table></div><p class="conditions">Paper-reported values, not reproduced in this design study. These are pairwise preferences against the named RL methods, not preference over the original HunyuanVideo model. Table 2 in the paper separately compares automatic metrics under two reward settings and several KL variants.</p><p class="scope"><b>Scope.</b> The study evaluates the named HunyuanVideo-1.5 / VideoAlign setup. The galleries above contain selected qualitative examples; they do not establish aggregate performance on other models or prompts.</p></section>
<section class="citation"><h2>Read the details.</h2><p><a href="https://arxiv.org/abs/2603.21872">Full paper and appendix ↗</a></p><details><summary>Citation</summary><pre>@article{zheng2026manifold,
  title={Manifold-Aware Exploration for Reinforcement Learning in Video Generation},
  author={Zheng, Mingzhe and Kong, Weijie and Wu, Yue and Jiang, Dengyang and Ma, Yue and He, Xuanhua and Lin, Bin and Gong, Kaixiong and Zhong, Zhao and Bo, Liefeng and Chen, Qifeng and Yang, Harry},
  journal={arXiv preprint arXiv:2603.21872},
  year={2026}
}</pre></details></section></main><footer class="wrap">Independent local design study for PaperProjectPageSkill, not the official SAGE-GRPO website. Paper, figure, prompts and videos belong to their authors. <a href="https://dungeonmassster.github.io/SAGE-GRPO-Page/">Official project ↗</a></footer><script id="media-data" type="application/json">__DATA__</script><script src="player.js" defer></script></body></html>'''
    # The Code URL is taken from the downloaded author page, not a guessed repository name.
    from bs4 import BeautifulSoup
    source=BeautifulSoup((CASE/'sources/original.html').read_text(encoding='utf-8'),'html.parser')
    code=next(a['href'] for a in source.select('a[href]') if 'github.com/' in a['href'] and 'Code' in a.get_text())
    text=text.replace('https://github.com/dungeonmassster/SAGE-GRPO',html.escape(code,quote=True))
    text=text.replace('__PRIMARY__',panel('primary',data['groups']['primary'],revised=args.version=='revised')).replace('__RL__',panel('rl',data['groups']['rl'],keep=True,revised=args.version=='revised')).replace('__VERSION__',args.version).replace('__DATA__',json.dumps(data,ensure_ascii=False).replace('</','<\\/'))
    (dest/'index.html').write_text(text,encoding='utf-8')
    shutil.copy2(ROOT/'benchmarks/web/sage.css',dest/'sage.css')
    player=(ROOT/'benchmarks/web/player.js').read_text(encoding='utf-8')
    player=player.replace("const root=document.querySelector('#comparison');",'function mountComparison(root,comparisons) {')
    player=player.replace('data.comparisons[index]','comparisons[index]')
    player=player.replace("const config=comparisons[index];", "const config=comparisons[index];\n  root.querySelector('.viewing-cue').textContent=config.cue;")
    player=player.replace("b.onclick=()=>select(i)","b.onclick=()=>switchSelection(i)")
    # Seeking helper must remain accessible inside each mounted group only.
    player=player.replace('select(0);','''const speed=root.querySelector('.speed');
let rate=1;
if(speed){speed.onclick=()=>{rate=rate===1?.5:1;group.forEach(v=>{v.defaultPlaybackRate=rate;v.playbackRate=rate;});speed.setAttribute('aria-pressed',String(rate===.5));speed.textContent=rate===.5?'Speed: 0.5×':'Speed: 1×';};}
function switchSelection(i){const prior=root.dataset.keepTime==='true'?Number(timeline.value):0;select(i);if(prior>0)seek(prior);const menu=root.querySelector('select');if(menu)menu.value=String(i);}
const menu=root.querySelector('select');if(menu)menu.onchange=()=>switchSelection(Number(menu.value));
select(0);
}
document.querySelectorAll('[data-group]').forEach(root=>mountComparison(root,data.groups[root.dataset.group]));''')
    player=player.replace("end=Math.min(...config.media.map(id=>records.get(id).duration));", "end=Math.min(...config.media.map(id=>records.get(id).duration));group.forEach(v=>{v.defaultPlaybackRate=rate;v.playbackRate=rate;v.controlsList='noplaybackrate';});")
    # Each group needs a local helper; all mounts are created after function declarations.
    if args.version=='baseline':player=(ROOT/'benchmarks/web/sage-player-baseline.js').read_text(encoding='utf-8')
    (dest/'player.js').write_text(player,encoding='utf-8')
    print(dest/'index.html')

if __name__=='__main__':main()
