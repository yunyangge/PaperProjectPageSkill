# Paper-to-page improvement study

Status: active; resumed with revised sample selection on 2026-11-05 (Asia/Shanghai).

Objective: use influential video-generation papers to generate original project pages from their PDFs, compare the generated pages with the authors' sites, revise the skill from observed failures, and test the revisions in subsequent pages.

## Protocol

1. Prioritize recent projects aligned with the user's examples, then assess relevant capabilities, available media and public adoption. Verify paper identity, first-publication date and public project/media sources. Citation counts are supporting evidence, not an eligibility threshold for new work; record source/count/date and matched version when available. Do not label a project highly cited without verification.
2. Read the PDF and produce a brief with page/figure/table evidence. Freeze a baseline skill snapshot.
3. Build a first page from the paper and attributed research media. Inspect media metadata without using the original site's CSS/layout as a template. Record any original-site exposure honestly.
4. Inspect baseline desktop/mobile rendering and interactions, then inspect the authors' page at comparable viewport sizes.
5. Record concrete differences: first useful effect, information hierarchy, media legibility, meaningful comparisons, prompts, reading burden, visual cohesion, loading and controls. Do not invent user-study scores.
6. Revise the generated page and skill, preserving before/after artifacts. Apply each proposed general rule to another paper before treating it as a broadly useful default.
7. Keep paper-specific styling decisions in case notes. Publish only original instructions/code and appropriately licensed artifacts; third-party PDFs/media remain local research inputs unless redistribution is cleared.

Primary cases: Helios, Echo-Infinity and SAGE-GRPO. Supplementary reference: Rolling Forcing. See [the revised selection](recent-projects.md) for verified paper identities, dates and intended evaluation roles. The previous AnimateDiff / Tune-A-Video / VideoCrafter2 selection is superseded because it is too old for the user's target aesthetic. Its local inputs are retained as historical collection artifacts, not current benchmark evidence.

The user resumed the generation loop after the sample revision. Sample selection alone does not establish PDF reading, trial page generation or comparative evaluation as completed.

The user authorized an autonomous improvement loop. For this benchmark the agent selects and records a suitable direction; ordinary skill use retains the user's direction-selection step.

## Completion evidence

- Three verified recent papers relevant to the user's examples and full PDF reading briefs; report available influence evidence separately.
- Three working pages with actual attributed media, inspected at desktop/mobile sizes.
- Original-site observations and baseline/revision comparisons.
- At least two evidence-driven skill-improvement iterations, including transfer to a different case.
- Interaction checks, limits, and final repository/installed-skill synchronization.

Large local inputs and generated trial artifacts live in `outputs/benchmarks/` (ignored by Git). Reproducible study notes and scripts live here.

## Current case evidence

- [Recent sample selection](recent-projects.md)
- [Helios paper brief](helios-brief.md)
- [Helios baseline/revision observations and verification limits](helios-review.md)
- [Echo-Infinity paper brief](echo-brief.md)
- [Echo-Infinity second iteration and transfer checks](echo-review.md)

Helios and Echo-Infinity have working local baselines and revisions with actual media. Echo tests the first iteration in a different light-gallery design and adds a second iteration for larger comparison views, timed prompts and reliable late seeking. SAGE-GRPO's PDF and source markup have been collected; its page and transfer evaluation are pending.

## Local reproduction

Python dependencies for these optional research scripts: requests, pymupdf, beautifulsoup4, imageio-ffmpeg. They are not installer dependencies for the skill. On the author's Windows workspace, use `conda run -n py310 python` for every command below.

1. Run `benchmarks/collect_sources.py` to collect PDFs and available citation-index records.
2. Run `benchmarks/inventory_media.py` to inventory the authors' published assets.
3. Run `benchmarks/prepare_helios.py` to fetch the selected original videos and probe their metadata.
4. Run `benchmarks/generate_helios.py --version baseline` once to freeze the first draft, then `benchmarks/generate_helios.py --version revised` for the current version. Baseline generation refuses to overwrite an existing baseline.
5. Optionally run `benchmarks/prepare_review_fixtures.py` for the deliberate failure test and original-source layout snapshot. The snapshot's note describes its differences from the live site.
6. Run `benchmarks/prepare_echo.py`, then `benchmarks/generate_echo.py --version baseline` once and `benchmarks/generate_echo.py --version revised`. `benchmarks/prepare_echo_snapshot.py` builds an optional layout-only original-source snapshot, with playback disabled and limitations documented beside it.
7. Run `benchmarks/serve_media.py --port 8767` to serve `outputs/benchmarks/` on loopback with byte-range support. Inspect `/helios/revised/` and `/echo-infinity/revised/`. Ordinary Python `http.server` did not support late seeking on incompletely buffered long videos in this study. Keep each parent `assets/` directory with its page. Study pages and third-party media are not published by the skill installer.
