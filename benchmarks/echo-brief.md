# Echo-Infinity — paper-to-page brief

Read 2026-11-05. [Paper](https://arxiv.org/abs/2606.04527), [author project](https://echo-team-joy-future-academy-jd.github.io/Echo-Infinity/). Local source: `outputs/benchmarks/echo-infinity/sources/paper.pdf` (21 pages).

## Reading and evidence

Substantive text, equations, experimental protocol and appendices read across pp.1–11 and 15–21; pp.12–14 are bibliography, not an independently verified literature review. Paper title uses **Learning Evolving Memory**; website uses **Learnable Evolving Memory**. Use the paper title for bibliographic identity.

- pp.1–4: two bottlenecks are growing history caches and temporal position indices outside the training range. Figure 2 (p.3) is the memory taxonomy; Figure 3 (p.4) is the method overview. Website figure numbering differs, so cite the PDF numbering when using the PDF.
- pp.5–6, Eq.4: memory queries update from evicted KVs using attention and a sigmoid gate; projections feed memory into each layer. The bounded relative RoPE schedule is shared during training and inference. Constant active context/per-step cost does not mean constant total generation cost or lossless memory.
- pp.7–8 and Appendix B (p.15): Wan2.1-T2V-1.3B, 832×480, 16 fps output. Training first adapts on 5-second clips, then tunes on 60-second sequences with one prompt switch. Default memory has three latent frames, 4,680 query tokens. Training uses 64 H200s; throughput measured on one H100. Do not confuse latent memory frames with output video frames.
- Table 1 p.6: 30s quality/semantic/user preference and 240s quality/user preference. Echo: 85.61/82.01/59.53 and 81.23/71.67; throughput 18.5 fps. LongLive 20.7 fps, MemFlow 18.7, Memorize-and-Generate 21.7, Infinity-RoPE 17.0. Echo is not the fastest row.
- pp.8–9: 240s evaluation uses 128 MovieGen prompts; day-scale qualitative rollouts use 15 sampled prompts. The 24-hour claim is not a measured aggregate day-scale consistency score. Table 2 includes prompt-interval CLIP scores that Echo does not win in every interval.
- Table 3 p.9: 5s total 84.57 with memory updates disabled, 85.35 enabled. Table 4 p.11 and Table 5 p.17 have mixed ablation metrics; avoid saying every component wins every metric.
- pp.17–18: forced-choice user study, 30 researchers × 50 prompts = 1,500 votes per duration. 30s clips viewed in full; 240s clips require first/final 10s and at least 40 additional middle seconds. Preference is share selected among all compared methods, not a pairwise win rate.
- pp.11 and 18: highly dynamic hour-scale scenes can be less stable; targeted interactive optimization and efficient hour/day-scale quantitative evaluation remain open. pp.19–21 cover impacts and additional qualitative figures including six timed prompts.

## Direction and content selection

Choose a light gallery with ink-blue typography and a small cyan accent. This is the autonomous benchmark choice authorized by the user, not a new permanent default. A large four-minute underwater result leads; a compact 30-second scene provides variety. The six-prompt example receives a visible timeline. Comparisons precede the method. Long-form author-hosted videos remain optional links with explicit part boundaries; do not download YouTube media or imply a short local clip spans a day.

Transfer from Helios: keep a meaningful mobile demo above the long author block, put method labels above comparison players, keep generation throughput separate from encoded playback fps, and derive seeking points from actual file durations. New question: can a four-method grid retain useful inspection size, especially on a phone? Freeze the first version before answering this through browser inspection.

Original-site exposure: the author page was previously visually reviewed for the skill's reference library. Its markup/data are now read to obtain attribution and prompt mappings. This is not a blind comparison. All trial HTML/CSS and controls are original study code; author media stay local and are excluded from the skill release.
