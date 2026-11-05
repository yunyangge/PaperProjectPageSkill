# Echo-Infinity — second iteration and transfer check

Observed 2026-11-05. Local baseline, revision and screenshots: `outputs/benchmarks/echo-infinity/`. [Paper brief](echo-brief.md). Seven unchanged author videos total about 119 MB: one 239.81s gallery result, one 29.81s result, one 59.81s multi-prompt result, and four 239.81s comparison files. All are 832×480 at 16 fps. Full source URLs, sizes, hashes and prompt mappings are in the ignored `media.json`.

## Baseline → revision

The baseline is frozen. It applies the first Helios iteration to a different light-gallery design: a substantial first demo, authors after it on mobile, labels before comparison videos, and common-time checkpoints. It has four simultaneous comparison tiles and a collapsible six-prompt list.

Actual browser measurements, not user-study scores:

| Check | Baseline | Revision |
| --- | --- | --- |
| Comparison tile width, 1440×900 viewport | about 279 px, four columns | about 576 px, Echo plus selected baseline |
| Comparison tile width, 390×844 viewport | about 149 px, two columns | about 310 px, labeled stacked pair |
| First hero video top, mobile | about 360 px | about 360 px |
| Mobile horizontal overflow | none: content width 375 px | none: content width 375 px |
| Six successive prompts | complete list on demand | current prompt + six timed jumps, complete list retained |
| Method switch at an inspected time | not available | preserves time for the same input, remains paused |

The four-column overview shows breadth but makes suit and motion detail small. The revision retains all three baselines behind an explicit selector while enlarging the pair. This sacrifices simultaneous four-way viewing; it is a useful inspection mode, not a universal ban on four-column galleries. The choice needs another case with subtle differences to test transfer.

The desktop hero's initial play button fell below the viewport despite the poster being visible. The revised hero has an unobtrusive accessible play button on the poster. Original-site comparison also exposed weaker project identity in our opening: the revision replaces the generic lead phrase with the full project name. Palette and hierarchy stay consistent rather than adding unrelated decoration.

## Playback findings

The standard Python static server on port 8766 did **not** support byte ranges. A seek to 230s on partially buffered four-minute media returned both players to 0 while the UI reported success. Fully buffered short clips in the earlier case had not exposed this. We added a loopback-only range-capable study server (`serve_media.py`, port 8767) and changed the player to confirm the actual time after `seeked` before reporting success. An invalid seek now reports that the clip cannot reach the requested time.

Verified in the browser:

- Initial page: five rendered video elements, no attached video source URLs; only posters load.
- Hero play starts actual media. Navigation away pauses it through the existing visibility observer.
- Both selected comparison videos seek to **230.0s**, paused; switching LongLive → MemFlow retains **230.0s**.
- Coordinated playback advanced both to approximately **230.25s**. It is not advertised as frame-locked.
- Rapid LongLive → Memorize-and-Generate → MemFlow switching leaves only the correct pair, paused at the retained time.
- Both finish at **239.8125s**, pause, and show the completed state.
- Multi-prompt chapter 4 selects **30s** and the supplied 30–40s prompt. Chapter 6 activated with Enter selects **50s** and the 50–60s prompt. Expanding the sequence reveals all six prompts.
- Comparison players remain paused when working in the separate prompt module.
- On the unsuitable non-range server, actual times remain 0 and the revised UI reports failure rather than success.
- The shared seeking fix was transferred back to Helios: both players reached **40s**, with successful paused status.
- No console errors in the normal revised Echo page during the checked interactions. Range server bounded, suffix and unsatisfiable range requests returned the expected 206/206/416 responses.

Not all acceptance cases were repeated here: the deliberate missing-video fixture was exercised in Helios, not this case; no bandwidth-throttled network, screen reader, or other browser engine was tested. Native controls and explicit chapter buttons were exercised, not every keyboard interaction. YouTube hour/day playback was not verified or downloaded.

## Original-site comparison and limits

The live site loaded far enough to inspect DOM/layout measurements: 104 video elements and no document-width overflow at desktop. Its screenshot call then timed out. This is an observation about this inspection environment, **not a measured live-site performance verdict**.

For visual comparison, a separate local snapshot retains the author's HTML/CSS/JS, fonts and 75 original posters. Video and iframe playback are deliberately disabled; YouTube thumbnails remain remote. Snapshot screenshots were successfully inspected at 1440×900 and 390×844. This supports layout comparison, not original playback verification.

- The original's angled, softly faded moving gallery gives a stronger immediate impression of variety and a distinctive visual identity. Its large project name is more recognizable than our baseline heading. These are strengths worth retaining when breadth is the purpose.
- Its mobile opening devotes most of the first viewport to title, full authors, affiliations and resources over a faded gallery. Our opening provides a large direct-view poster and play control earlier, with readable authors below. The latter favors focused inspection; it does not establish an overall aesthetic winner.
- Original comparison tiles measured about 292 px desktop / 147.5 px mobile, near our baseline's density. The original exposes prompt enlargement and many more examples; our revision trades that simultaneous breadth for a large selectable pair and explicit shared-time navigation.
- Original content covers more prompts and durations. Our smaller curated local study cannot substantiate equal coverage or better scientific performance.

## Skill changes supported here

Helios rules successfully transferred to a light page without importing its dark style: mobile reflow, labels before videos, and separating generation throughput from playback fps. New narrow guidance covers inspection size versus overview density, retaining meaningful time across method switches, visible timed prompts, split long-form hosting, first-viewport play affordance, and late-seek verification on a suitable media server. SAGE-GRPO remains the next transfer case; the full three-paper goal is not yet complete.
