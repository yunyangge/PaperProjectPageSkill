# Video and comparison patterns

Give video interaction particular care. Choose modules by the scientific question and available data. Do not activate all patterns on every page.

## Data before layout

Use stable media IDs and comparison-group IDs. Keep records for file/URL, poster, task, method, prompt ID and text, display label, aspect ratio, duration/fps when known, and source/settings. Unknown values remain unknown. Multiple methods compared on a prompt share a group; visually similar clips alone are not enough.

Distinguish these views:

- **Showcase:** representative examples demonstrating variety; selection may be curated and should not imply aggregate superiority.
- **Controlled comparison:** methods evaluated with the stated common input and protocol. Keep differences in settings visible.
- **Ablation:** variants changing a specified factor. Labels and supporting evidence must identify that factor.
- **Input/output:** preserve the input alongside the generated result, using task-appropriate image, audio, text, or video controls.

## Gallery

Make the gallery an understandable demonstration, not just a dense video wall. Feature a dominant example when it helps introduce the capability, then group supporting clips by what they show. Supply short viewing cues. Keep full prompts expandable while leaving task and interpretation labels visible. Follow [showcase-composition.md](showcase-composition.md) for hierarchy and page rhythm.

Favor a small visible set with explicit filters/categories and a useful way to expose the rest. Give cards a predictable layout; group compatible aspect ratios or intentionally use different-size tiles. Contain scientific media rather than cropping meaningful content. Include task/duration labels only when verified.

Cards should offer a visible route to play, pause, inspect, and read the prompt. A poster remains useful before playback and after a load failure. Hover preview can supplement controls on pointer devices; touch and keyboard users need an equivalent path. Sound must remain user initiated.

## Same-prompt comparisons

Keep the shared prompt, method labels, and relevant settings visible near the group. Use aligned columns or a responsive grouped layout. On mobile, preserve the relation between input and outputs; do not turn the group into indistinguishable unlabeled cards.

Useful group controls: play/pause all, restart all, optional speed selection, and a shared timeline when the clips share meaningful time alignment. Hide unnecessary controls. A long-video comparison may benefit from elapsed time or selected aligned checkpoints, but never invent physical time from unknown fps.

Do not claim frame synchronization merely because several `play()` calls happen together. Use **coordinated playback** as the default promise. When temporal alignment is important, implement a shared clock/leader, coordinated seeking and drift correction, and test with actual clips. Document any limitation caused by different fps, encodes, or browser scheduling.

For different durations, choose and disclose the behavior: stop at the common endpoint, or let finished tiles remain on their last frame. Looping each clip independently is inappropriate when it would make the comparison misleading. Never alter speed or trim one method silently to make it look better.

## Playback state and failure handling

- Each comparison group owns its own player state. Controls in one group must not pause or seek an unrelated group.
- Wait for media readiness before seeking or coordinated start. Handle rejected playback promises as visible states, not unhandled errors.
- Rapid prompt/category switches must invalidate stale load callbacks. Pause detached/hidden players and release resources as appropriate.
- A failed tile should expose a useful poster/error state and retry/open-video action without freezing the other clips forever.
- Manual pauses and automatic visibility pauses must be distinguishable; scrolling back should not unexpectedly override the user's pause.
- For a coordinated seek, preserve the intended paused/playing state and clamp target time to each clip's valid interval.
- Register event handlers once and clean them up when rebuilding a group. Avoid timers that continue running after navigation or removal.

## Prompts and metadata

Long prompts are expandable text, not hover-only content. Use an accessible button/details control, clear expanded state, and preserve line breaks where meaningful. A short preview can keep the gallery scannable; expansion must reveal the complete supplied prompt.

For multi-prompt or interactive examples, preserve the ordered prompt sequence and timing when supplied. Do not display a joined paragraph in a way that implies a single prompt. Keep seed, resolution, guidance, and other protocol details available when needed for interpretation.

## Loading and presentation

- Avoid downloading every large clip on initial load. Stage media loading by visible/selected groups; usually use posters and `preload="none"` or `metadata` according to need.
- Do not assume a `loading="lazy"` attribute on video provides the intended resource policy. Implement and verify actual deferred source/loading behavior when needed.
- Autoplay, if useful, is muted and inline. Use explicit control for sound and pause/motion reduction. Respect reduced-motion preference for decorative background loops and moving gallery belts.
- Compress/resize previews appropriately while preserving meaningful details and temporal behavior. Keep originals when needed. Record transformations used in scientific comparisons.
- Background galleries need an overlay and fallback cover so titles remain readable. Never make a decorative video the only route to an essential result.

## Behavioral acceptance checks

Use actual local media when available. Verify:

1. Play/pause/restart and seeking work, both for one card and a comparison group.
2. Switching a prompt changes all relevant methods and the prompt text; rapid repeated switching leaves no stale video or sound.
3. Hidden groups stop consuming playback resources; manual pause is respected on return.
4. A missing/unsupported clip yields a recoverable error without breaking other tiles.
5. Different durations, aspect ratios, and slow metadata loading behave as designed.
6. Prompt expansion, category selection, and controls work with keyboard and on a narrow touchscreen layout.
7. Initial page load does not request the whole video catalog; decorative animation can be reduced or paused.

Report these as implemented-and-tested, implemented-but-untested, or unavailable. Do not claim playback correctness from HTML inspection alone.
