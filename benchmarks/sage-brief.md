# SAGE-GRPO — paper-to-page brief

Read 2026-11-05. [Paper](https://arxiv.org/abs/2603.21872), [author project](https://dungeonmassster.github.io/SAGE-GRPO-Page/). The PDF's bibliographic title is **Manifold-Aware Exploration for Reinforcement Learning in Video Generation**; SAGE-GRPO is its method name. First arXiv submission is 2026-03-23; the PDF front matter says preprint March 24. Do not invent a venue.

## Reading and selection

Read substantive text/equations on pp.1–8 and appendices pp.12–17; pp.9–11 are bibliography, not independently verified references. Figures/tables are rendered separately for inspecting the actual visual evidence.

- pp.1–3: video GRPO exploration can inject excess noise, lowering rollout quality and making reward-guided updates unreliable. The contribution combines a precise SDE, timestep gradient balancing, and a dual trust region. Figure 2 gives geometric intuition; this is not a guarantee that every result has no artifacts.
- pp.4–5 / Eq.5–9: integrate variance with a logarithmic correction; the gradient equalizer normalizes estimated per-timestep gradient scales. Figure 3 compares rewards with/without balancing. Figure 5 (p.5) is the full framework.
- pp.5–6 / Eq.14: moving-anchor and step-wise KL constraints control accumulated drift and individual updates. “Long-horizon” here concerns optimization, not hour-long generated videos; do not import duration claims from Helios/Echo.
- p.6: HunyuanVideo-1.5 backbone, 81-frame training samples, per-GPU batch 2 and 4 accumulation steps. Original VideoAlign is the frozen reward model. These settings do not establish the encoded duration/fps of every public showcase; probe the files.
- Table 2 p.7: two reward settings, A (1,1,1) and B (0.5,0.5,1). Variants include no KL, Fixed KL and SAGE's Dual Moving KL. Results are mixed across settings/metrics; SAGE's strongest Setting B row does not justify universal superiority across all configurations. Preserve setting and KL labels if showing this table. Avoid rebuilding its Overall column from component scores without resolving the aggregation details.
- pp.6–7 / Figure 6: three paired baseline examples focus on a runner, Newton's apple, and five children. Use these as the main visible comparisons because the public page supplies complete prompts. The viewing cues describe what to inspect, not a predetermined win.
- pp.7–8 / Table 3: 29 evaluators, 32 prompts, all at iteration 100, sampling steps 40, Setting B. Pairwise SAGE win rates (VQ/MQ/semantic) are DanceGRPO 85.9/75.8/79.2%, FlowGRPO 83.8/79.2/71.9%, CPS 80.2/70.8/67.9%. This is pairwise preference, unlike Echo's multi-method forced-choice percentage. It is not HunyuanVideo-original comparison and not the public 20-step showcase protocol.
- p.8 / Figures 7–8: gradient/KL strategy and weight-schedule ablations support optimization behavior. pp.12–14 derive the variance/gradient relationship, including schedule boundary sensitivity. pp.15–17 add emotion examples and five-way KL comparisons. Appendix Eq.42/43 contains sign/direction conventions that this design study does not independently validate; omit implementation advice derived from them.
- No separate limitations section was found. State the demonstrated scope instead: this evaluation is on one named backbone/reward setup; galleries are selected qualitative samples, not aggregate estimates.

## Direction and transfer

Choose an editorial, warm-ivory/forest-green design. Put a named baseline/output pair in the opening and let visitors change among the three supplied prompts; keep the method explanation later. This tests the skill's third visual direction while retaining effects-first priority. Use ordinary playback and replay first; no minute-scale checkpoint strip for a roughly few-second clip. Test whether a clearly labeled half-speed mode helps inspect motion without silently changing playback speed.

A separate RL-method pair can expose all three baselines at the author-labeled **20 sampling steps**. Its gallery omits full prompts and per-file seeds; disclose that instead of inventing them or calling the comparison fully controlled. Keep the **40-step** human study separate.

Baseline transfer: large inspection pairs, visible method labels, mobile reflow, complete expandable prompts, actual seek confirmation, and explicit loading. Do not automatically retain time when switching to a different prompt. Test each group's independent state if a second comparator is added.

The original page was already inspected in reference-library work and its markup is used to map files/prompts; this is not blind testing. No original HTML/CSS is used as the generated page's template.
