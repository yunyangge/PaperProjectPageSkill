# Review and delivery

## Review the page as research communication

Verify that the first viewport establishes the paper/project identity, readable authors, a concise capability statement, real resource links, and a meaningful demonstration. On narrow screens, the demonstration should follow the essential identity/resources without an intervening long text block. Capability showcases and interpretable comparisons should be easy to find before extended method exposition.

Apply the acceptance questions in [showcase-composition.md](showcase-composition.md). Review aesthetics and clarity together: a visually striking opening fails if the actual effect is too small to inspect, its meaning is unclear, or the controls are hard to discover.

Check claims and captions against the supplied paper/data. Match comparison settings, baseline labels, units, and the direction of improvement. Preserve the distinction between a qualitative showcase and measured superiority. Make missing publication metadata or unreleased resources explicit in a small appropriate way; do not fill them with plausible inventions.

## Visual inspection

Inspect the actual rendered page at desktop and narrow mobile widths. Review the hero, a gallery/comparison, method content, results table or chart, and citation/footer. Check wrapping author lists, long titles, captions, figure aspect ratios, sticky navigation offsets, expanded prompts, and empty/loading/error states.

Keep text and controls readable over media. Scientific figures generally need their full extent visible. For tables, choose a layout that preserves comprehension on mobile; use labeling, grouping, and accessible overflow where justified instead of clipping cells. A horizontal carousel must have visible navigation and a mobile route to all items.

Inspect meaningful interactions in the browser; follow the behavioral checks in [video-patterns.md](video-patterns.md). Screenshots establish composition, not playback correctness. If a browser or media codec limitation blocks a check, name it and distinguish it from a defect in the implementation.

## Technical checks

- Run the project's relevant build/lint checks, if present.
- Check internal anchors, local assets, resource links, and duplicate IDs.
- Verify keyboard access, visible focus, semantic buttons, image text alternatives, and useful media labels. Add captions/transcripts when the supplied speech/content requires them and assets are available.
- Verify that the catalog uses the intended staged-loading behavior and does not start all videos at once.
- For long-video navigation, verify a late seek on incompletely buffered media with a range-capable preview server; confirm the actual frame/time reached. See the specific checks in [video-patterns.md](video-patterns.md).
- Confirm there are no new console errors from the page implementation; separate third-party or network failures in the report.
- Verify metadata: title, description, preview image and canonical URL when known. Never put guessed production URLs into published metadata.
- Remove sample authors, template prompts, test-only markers, inherited analytics IDs, and dead resource buttons before publication.

## GitHub Pages readiness

A local preview working at `/` does not prove that a project site works at `/<repository>/`. Inspect the repository's actual Pages configuration and framework build settings, then test asset paths and routing with its intended base path. Use a suitable local HTTP server for module or fetch-based pages; file-open behavior is not an adequate deployment check.

Keep secrets out of static source and browser bundles. Do not copy private or unpublished assets into a public deployment without the user's authorization. Retain applicable source and asset attribution. Prefer the existing deployment workflow to creating a competing one.

The task can finish with a verified local site when publication was not requested. If publication is authorized, use the actual destination/branch, inspect existing remote state, deploy, and verify the resulting URL. Do not substitute another hosting product for GitHub Pages without the user's direction.

## Handoff

Give the user:

- The local source location and working preview, or the verified deployed URL.
- A short account of the selected visual direction and the important working modules.
- Where to edit paper metadata, resource links, prompts, and media records.
- A concise validation summary and any material limitations.

When collecting feedback, ask about a visible choice such as hero density, gallery size, typography, or comparison behavior. Preserve choices already accepted and revise the affected modules. Do not reopen the entire design decision unless the user requests it.
