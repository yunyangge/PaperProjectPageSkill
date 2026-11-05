# Visual reference library

Reviewed 2026-11-05. The first four sites are core design references. They express a range of aesthetics, not a ranked list. No single one is the default. Add new references with source links and the specific decision they improve.

Visual notes below are our interpretation of the rendered pages. These sites have not undergone a full implementation or performance audit. Some remote videos did not load in the inspection browser; do not mistake blank or loading tiles for intentional design or assume all playback behavior was verified.

## Core project-page references

### Helios — dark showcase

- [Page](https://pku-yuangroup.github.io/Helios-Page/)
- Observed: black first viewport, large project mark and centered title, compact pill links, prominent feature/speed videos, prompt-selectable baseline comparisons, task-specific galleries.
- Borrow: strong project identity; group demonstrations by capability; put the setting beside the comparison; let media occupy substantial width.
- Adapt: a long media catalog needs staged loading and navigation. Do not inherit a large logo, oversized empty header, or all-black body when the paper does not benefit from it.

### Rolling Forcing — expressive dark first viewport

- [Page](https://kunhao-liu.github.io/Rolling_Forcing_Webpage/)
- Observed: left-aligned uppercase headline, deep purple background, colored organic shapes, outlined resource pills, then long-video results and comparisons.
- Borrow: distinctive typography and a deliberate asymmetrical opening; clear emphasis on video length and real-time capability.
- Adapt: translate the energy to the new project's identity; the original shapes and purple palette are not mandatory. Keep long prompts accessible without dominating each tile.

### Echo-Infinity — light gallery

- [Page](https://echo-team-joy-future-academy-jd.github.io/Echo-Infinity/)
- Observed: light background, blue/violet accents, anchored top navigation, a softened angled gallery behind the title, and dense media cards carrying duration/task cues and prompt expansion.
- Borrow: show the breadth of outputs early; retain a short claim; separate browsing a gallery from studying a method.
- Adapt: preserve foreground contrast and a useful static cover. Decorative movement must not interfere with reading or eagerly load the entire collection.

### SAGE-GRPO — branded opening, light evidence body

- [Page](https://dungeonmassster.github.io/SAGE-GRPO-Page/)
- Observed: navy/purple opening, centered circular mark, prominent method name, subtitle and authors, followed by a light body with a large explanatory result figure and caption.
- Borrow: a recognizable identity can coexist with a paper-like reading surface. Large, well-captioned figures can connect mechanism and observed effect.
- Adapt: make the transition into the body feel intentional. Do not add dependency/version badges merely to imitate the source.

## Additional GitHub templates

### Clarity — editorial explanation and comparison modules

- [Repository](https://github.com/lorenmt/clarity-template) · [Live guide/demo](https://shikun.io/projects/clarity)
- Observed/repository-documented: modular HTML and Sass styling, several container widths, restrained typography, equations, tables, slide displays, selectable examples, image comparison sliders, and video controls.
- Best use: an explanation-led paper, or an editorial body combined with a more visual first viewport. Borrow width hierarchy and comparison mechanics, not the personal-site navigation.
- Reuse note: repository license labeling and README wording differed during review. Inspect the actual LICENSE and relevant asset terms before copying source. Demo fonts/icons may differ from the free defaults.

### Academic Project Page Template — compact static baseline

- [Repository](https://github.com/eliahuhorwitz/Academic-project-page-template) · [Demo](https://eliahuhorwitz.github.io/Academic-project-page-template/)
- Observed/repository-documented: centered academic header, resource pills, teaser, image/video carousels, poster area, and copyable BibTeX. The source is HTML/CSS with a static asset directory.
- Best use: a small maintainable page or familiar baseline to customize. Its default appearance is deliberately conventional; use another composition when stronger identity is needed.
- This descends from Nerfies; it is not an unrelated style family. Check attribution and remove all example content when reusing.

### Academic Project Astro Template — richer component implementation

- [Repository](https://github.com/RomanHauksson/academic-project-astro-template) · [Demo](https://research-template.roman.technology/)
- Observed/repository-documented: optional image/video cover, MDX content, wide media, formulas, comparison sliders, tabbed content, carousels, and 3D components. The repository includes a GitHub Pages workflow.
- Best use: pages with many reusable modules or ongoing maintenance. Choose it for those needs, not for appearance alone; verify current build prerequisites when adopting it.
- It shares Nerfies ancestry. Treat it as another implementation option, not independent evidence that every research site needs the same layout.

### Nerfies — foundational research interaction reference

- [Source](https://github.com/nerfies/nerfies.github.io) · [Page](https://nerfies.github.io/)
- Observed: restrained centered header, concise result sentence, demonstrations organized by capability, and an interpolation control tied to a method property.
- Best use: learn how an interaction can explain the contribution. Do not copy the full old asset/runtime stack by default.
- The page documents attribution and removal of its original analytics when borrowing source; verify current terms before reuse.

### React + UIKit Academic Project Template — configuration-based alternative

- [Repository](https://github.com/denkiwakame/academic-project-template) · [Demo](https://denkiwakame.github.io/academic-project-template/)
- Repository-documented only in this review: content/metadata in `template.yaml`, Markdown, KaTeX, themes, responsive layout, and GitHub Actions deployment.
- Consider when declarative content editing is important and React already fits the project. The demo was not visually inspected; inspect it before making an aesthetic recommendation.

## How to select references

Match references to the paper's medium, amount of content, and intended reading experience. Three candidate directions might combine:

| Direction | Identity reference | Body/interaction reference | Appropriate when |
| --- | --- | --- | --- |
| Light gallery | Echo-Infinity | Clarity or Astro comparison modules | Many strong visual outputs and tasks |
| Dark showcase | Helios, Rolling Forcing, or SAGE-GRPO | A readable evidence body and purpose-built video groups | Media impact and project identity matter most |
| Editorial presentation | Clarity or a restrained Nerfies-derived header | Large demos, short viewing cues, paired comparisons, then concise method diagrams | The effects benefit from a carefully paced visual explanation |

These are starting points. All three prioritize effects over paper exposition by default. The editorial direction changes typography and sequencing, not the priority of demonstrations. Recommend based on the current paper, and record the user's actual selection in that project's notes. Do not describe inferred tastes as confirmed preferences.
