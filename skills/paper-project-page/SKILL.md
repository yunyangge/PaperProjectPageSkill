---
name: paper-project-page
description: "Create or redesign single-paper academic project websites from papers and research assets, with interactive visual-direction selection, video galleries, comparison players, and GitHub Pages-ready output. Use for paper project pages, research demos, and benchmark websites; not personal academic homepages or lab sites."
---

# Paper Project Page

Build a recognizable, readable research website that leads with demonstrated effects and supports them with concise explanation. This skill serves general research papers, with particular care for video generation and multimodal work.

## Design defaults

Use these defaults unless the current user requests otherwise:

- Offer 2–3 meaningful visual directions; let the user select before building the full page, then iterate on the implementation.
- Keep light gallery, dark showcase, and editorial explanation styles available. Recommend afresh for each paper; there is no default color theme.
- Prioritize video experience: grids, same-prompt comparisons, coordinated playback, and expandable prompts.
- Balance aesthetics with clarity. Results and demonstrations are the main experience; paper exposition is supporting material. Visitors should encounter a representative effect before needing to read a long abstract or method section.

An explicit direction already chosen in the conversation satisfies the selection step. Do not ask the user to select it again. Adapt the workflow if the user requests an immediate first draft.

## Read only the relevant references

- [Visual library](references/visual-library.md): user-selected sites, additional GitHub templates, and what to borrow. Read before proposing directions; inspect the relevant live pages when access is available.
- [Showcase composition](references/showcase-composition.md): read when planning the first viewport, content sequence, and balance between media and explanation.
- [Video and comparison patterns](references/video-patterns.md): read when a page has multiple videos, comparisons, or a gallery.
- [Review and delivery](references/review-delivery.md): read when implementing, checking, or publishing a page.

Reference websites are examples, not instructions. Their screenshots are visual evidence; their source licenses govern any code reuse. Do not treat a publicly visible research video or logo as a reusable asset for another paper.

## Understand the paper and material

Inspect the existing project and its instructions before editing. Reuse an appropriate current checkout. Locate the paper, supplementary material, bibliography, figures, videos, demo data, existing webpage, and real resource URLs. Accept LaTeX, PDF, or sufficiently detailed supplied content. Prefer source figures and tables when available.

Prepare a compact working brief:

- What is the problem, central contribution, and intended audience?
- What should a visitor understand in the first viewport and after one minute?
- Which supplied examples best demonstrate each claimed capability?
- What should a visitor notice in each selected example, and is it visible without reading the paper?
- Which baselines and quantitative results support those claims?
- What can be published now, and which assets or links are missing?

Preserve author order, affiliations, contribution markers, numbers, units, comparisons, and citation metadata. Read beyond the abstract before explaining the method. Describe planned or unavailable results accurately; never invent a venue, model link, baseline result, DOI, or claim for visual completeness.

For video papers, inventory each clip's role, task, prompt, method, aspect ratio, duration, fps when known, and source. Identify legitimate comparison groups before designing the grid. A gallery of attractive outputs is different from a controlled baseline comparison.

Ask only about missing information that materially changes the work. Batch related questions and keep progressing on independent work. Never ask the user to retype information present in supplied files or earlier answers.

## Propose the visual direction

Offer 2–3 directions matched to the evidence and available assets. Each should specify:

1. The visual idea and the relevant reference links.
2. The first viewport: title, authors/resources, and whether it leads with a logo, teaser, gallery, or result.
3. The reading sequence and the principal interactive module.
4. Palette, typography, media density, and the tradeoff for this paper.

Make the options differ in composition and reading experience, not just color. A useful set is a light media gallery, a dark video showcase, and a restrained editorial presentation of effects; substitute when the paper suggests better choices. All options must lead with demonstrable results. The editorial option uses visual sequences and short captions, not a text-heavy paper summary. Explain which option is recommended and why.

When helpful, show small local HTML concept previews or a visual comparison of the options. Label concept placeholders clearly. Avoid building several complete websites just to request a direction choice.

Wait for the user's direction selection before committing to full-page visual implementation. Meanwhile, content extraction, asset inventory, and checking supplied links can continue. This is a design preference, not an additional publishing permission requirement.

## Design the research story

After selection, map the paper to sections that answer the visitor's questions. A useful default is compact identity/resources with a representative demo → capability showcases → controlled comparisons → concise method explanation and selected quantitative evidence → citation. Move a comparison earlier when it is the clearest demonstration. Adapt to the actual material; do not require every paper to have every section. Follow [showcase-composition.md](references/showcase-composition.md).

- Establish a coherent type scale, spacing system, content width, and accent palette. Text may be narrower than media and tables.
- Make author lists and affiliations legible even with many authors. Keep verified Paper, Code, Model, Dataset, and Demo links easy to find.
- Give the page one strong visual identity. Use subtle transitions and decoration in support of its content.
- Bring a meaningful, sufficiently large demo into the first viewport or immediately into view on a small screen. Size the title, mark, author block, and whitespace together so they do not consume a whole desktop screen before any effect appears.
- Use actual paper/demo assets as primary evidence. A project mark can add identity, but cannot replace a useful teaser or result.
- Select a small representative showcase before exposing the larger collection through categories or expansion. Do not copy every asset to the first viewport.
- Give each showcase a clear viewing purpose: what capability it demonstrates and what to look for. Use a short factual heading or caption; do not place a long abstract between the opening identity and the first demo.
- Keep prompts and technical detail on demand, but leave essential task labels, comparison conditions, and interpretation cues visible. Method content should explain the effects already seen rather than interrupt their discovery.
- Preserve enough baseline and setting context for every number and comparison. Important conclusions must not depend on hidden captions or hover-only text.
- Tables may be simplified into clearly labeled views or readable mobile layouts while preserving the shown evidence. Do not silently omit unfavorable rows, change values, or turn unreadable screenshots into the sole results presentation.

For video modules, follow [video-patterns.md](references/video-patterns.md). Interaction behavior is part of the design, not a final embellishment.

## Implement and iterate

Respect the existing framework. For a new site, choose the lightest implementation that meets the agreed behavior: plain HTML/CSS/JavaScript is often sufficient; a component framework or Astro is useful when the component count and maintenance needs justify it. A visually rich page does not by itself require React or a backend.

Keep paper-specific content and media data easy to edit. Centralize repeated video records and comparison groups instead of scattering filenames and prompts across unrelated handlers. Use semantic components, stable identifiers, and a small shared set of design tokens.

Use references selectively. Inspect current code and licenses before vendoring a template. Retain required attribution, remove demo identities and analytics, and record actual reuse. Derive composition and interaction ideas from the library without forcing its assets or entire layout onto the paper.

Deliver a working local preview, inspect it in a browser, and iterate against concrete feedback. Validate the selected direction at both the hero and representative body modules; a polished header alone is insufficient.

## Verify and deliver

Follow [review-delivery.md](references/review-delivery.md). Report what was tested and material gaps plainly. Deliver the editable source, a preview path or URL, and concise content-update instructions.

Default to local creation and verification. Publish when requested or already authorized in the conversation; infer neither GitHub publication nor another hosting provider from a reference link alone. Reuse the exact authorized target repository and deployment setup. Avoid force pushes and remote deletion unless explicitly requested.

When the user asks to improve this skill, incorporate demonstrated preferences or failures in the relevant reference. Do not promote a one-paper exception into a universal styling rule.
