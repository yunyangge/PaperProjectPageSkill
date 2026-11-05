# SAGE-GRPO — third case and transfer evaluation

Observed 2026-11-05. [Paper brief](sage-brief.md). Local baseline, revision, source snapshot and screenshots are under `outputs/benchmarks/sage-grpo/`. Ten unchanged author clips total about 6.2 MB. The three baseline/output pairs are 864×480, 24 fps, 5.04s; the four RL-method clips are 864×480, 24 fps, 3.38s. Source URLs, complete supplied prompts and file hashes are retained in the local manifest.

## What transferred

The editorial ivory/green page uses large paired results before author details, method explanation and quantitative support. It carries forward Helios's mobile reflow and visible labels, and Echo's selectable comparison pair and actual seek confirmation. It does not import either case's palette or minute-scale checkpoints. The baseline is frozen, including its player implementation.

The primary group changes among three supplied prompts and resets time. The second group changes the competing method for one author-paired example and retains the inspected time. That section lacks a complete prompt and seeds; the page says so. Its 20-step gallery is kept separate from the paper's 40-step preference study. Table 3 preserves all three named baselines and all three reported dimensions; it is not described as preference over the unaligned backbone.

## Baseline → revision

At a 390×844 viewport (375 px content width), the baseline's first video began around y=598 and showed the original model. The revision replaces a tall row of example buttons with a labeled selector and puts the SAGE result first visually on mobile: its top is around y=546, with a roughly 318 px wide video. Both method labels remain explicit. Desktop retains the familiar baseline/result pair, roughly 569 px per video at 1440×900. No horizontal document overflow was observed. The preference table also fits the mobile width and was visually checked.

Short motion differences benefit from optional **Speed: 0.5×**, applied equally to both clips, with 1× as the default. The first implementation changed `playbackRate` before loading, but loading reset it to 1×. The correction sets both default and current rates and carries the selected rate into replacement clips. This is a tested case-specific option, not a requirement to slow every research video.

## Checked behavior

- Initial render has four video elements with deferred sources and visible posters.
- Ordinary paired play advances both actual media clocks; the 5.04s pair stopped around 5.02s with completed status. Playback is coordinated, not claimed to be frame-locked.
- Selecting 0.5× before first load produces actual 0.5 playback rates on both clips. Changing to Newton's prompt resets to zero and retains 0.5×; the unrelated RL group remains at 1× and paused.
- Rapid children → runner → children changes leave the matching case-3 sources and complete expanded prompt.
- The RL pair plays while the primary group is paused. Switching DanceGRPO → FlowGRPO while paused around 0.25s preserves 0.24s on both files, within the slider's 0.04s step.
- Keyboard ArrowDown selects the next example; Enter on Play together starts the selected pair. This is a targeted check, not a full accessibility audit.
- A deliberately missing baseline produces a visible retry/open-original state. The available SAGE clip still plays individually (observed 0.24s); the separate RL pair also plays (about 0.23s). Scrolling away pauses the off-screen clip through visibility handling.
- No errors attributable to the normal revised page were captured. The fixture's intended missing-file error and original snapshot's unavailable icon library are separate findings.
- Framework figure and mobile results table were inspected. Local assets, anchors, unique IDs and manifest references pass the shared artifact check.

Untested: screen readers, other browser engines, throttled networks and all native video-control combinations. Mobile CSS changes visual card order while DOM order remains baseline-first; keyboard reading-order polish remains a limitation, not a completed accessibility claim.

## Original-site comparison

The live original's desktop opening was captured and inspected. It has a distinctive circular logo, purple/navy identity, complete authors and prominent resources, followed by explanatory material. The first video was around y=3387 at desktop; that position describes this captured page, not a general performance score. A subsequent mobile inspection timed out in this environment.

A separate local snapshot retains source HTML, CSS, fonts and available image assets, with playback blocked. Its mobile opening and first baseline comparison were inspected. The original's pair is spacious, has clear baseline/ours headings, a subtle emphasis on the proposed method and a shared prompt directly underneath. These are useful strengths. Our revision brings such a pair into the opening and adds explicit coordinated controls and selectable examples, trading the original's immediately visible collection for a smaller inspection view.

Snapshot limits: selected clips use locally generated posters; uncollected videos lack their remote metadata. The source's Lucide dependency returned 404 and was recorded, so icon rendering is incomplete. The snapshot cannot verify original playback, loading performance or the complete gallery's final layout. No claim is made that the redesign is objectively more beautiful or scientifically better.

## Lessons retained

The cross-case evidence supports large inspection views, device-specific composition, visible labels and honest comparison settings without forcing one style. SAGE adds a conditional mobile check: a comparison-led opening should expose the proposed result, not only a tall baseline card. Compact selectors and optional equal-rate slow review are choices to consider when the material calls for them. They are not universal layout or playback mandates.
