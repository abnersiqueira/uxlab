<!-- Derived from Sumi 4.2.0 by Phazur Labs (Apache-2.0), skills/sumi-orchestrator/SKILL.md, upstream commit 3a3693b. Modified by uxlab: consolidated into a domain skill, renamed, cross-references rewritten. See NOTICE. -->
# uxlab Orchestrator

uxlab holds 43 skills and 37 commands. Most real requests need three to six skills
in a particular order, and running them in the wrong order wastes work — you
cannot critique a flow before you know who it is for, and you cannot set metrics
before you know what good looks like.

This skill is the router. Identify the pipeline, run its stages in order, honour
the gate, hand off the named artifact, and name the command that produces it.

## Two bands: stages and depth

Not every skill is a stage. A **stage** is a decision that gates the next
decision. A **depth skill** is a library you open once you already know what you
are building — 500+ layout blocks, 1000+ microcopy templates, 200+ animation
recipes, 500+ palettes. Loading a library before you have a decision to make just
burns context.

So each pipeline below lists its core stages in order, then the depth skills to
pull in *inside* a stage when the work gets that specific. Keep core stages at six
or fewer. If a pipeline seems to need more, one of them is depth.

## Routing

Match the user's request to a pipeline. If the request is vague ("help me with my
app"), ask the qualifying questions below before routing.

| The user wants to… | Pipeline | Command |
|---|---|---|
| Find what's wrong with something that exists | **Evaluate** | `/uxlab:audit`, `/uxlab:roast` |
| Fix AI-generated UI that works but looks wrong | **Fix** | `/uxlab:fix` |
| Design something that doesn't exist yet | **Create** | `/uxlab:inspo` → `/uxlab:style` → `/uxlab:screen` |
| Build or ship an actual component | **Implement** | `/uxlab:component` |
| Compose a whole page | **Compose** | `/uxlab:inspo` → `/uxlab:page`, `/uxlab:layout` |
| Generate design assets with AI | **Generate** | `/uxlab:generate` |
| Start or scale a design system | **Systematize** | `/uxlab:tokens` |
| Move a design into code | **Handoff** | `/uxlab:figma` |
| Understand why people aren't finishing | **Convert** | — |
| Ship to new countries or languages | **Localize** | — |
| Design an AI or agent feature | **AI Surface** | `/uxlab:ai-audit` |
| Know whether any of it worked | **Measure** | `/uxlab:measure` |

### Qualifying questions

Ask at most three, and only what the request hasn't already answered:

1. **Does it exist yet?** Nothing built → Create. Something built → Evaluate.
   Built by an AI and looks off → Fix.
2. **What platform?** Web/desktop, mobile, native, or ambient/voice/spatial. This
   selects the platform skill layered into every pipeline.
3. **What decision hangs on this?** Ship/no-ship, roadmap priority, or a specific
   fix. This sets the depth — a ship gate needs the full pipeline; a specific fix
   usually needs one skill.

## Pipelines

Each stage names the skill to invoke. **Gate** is the condition to satisfy before
moving on — if it fails, stay in the stage or step back, don't push forward.

### Evaluate — something exists and may be broken

1. `ux-evaluation/nng-ux-heuristics` — heuristic pass, severity 0–4 on every finding
2. `ux-evaluation/cognitive-psychology-ux` — cognitive load, decision architecture, attention
3. `accessibility-i18n/accessibility-inclusive-design` — WCAG 2.2, ARIA, keyboard, contrast
4. `ux-evaluation/ui-pattern-intelligence` — anti-patterns, pattern matching, AI-slop detection
5. `ux-evaluation/ux-ethics-content-strategy` — dark patterns, manipulation, interface copy
6. `ux-evaluation/design-critique-case-studies` — structure the findings into a critique

**Depth:** `visual-design/visual-design-mastery` when the complaint is "it looks cheap";
`forms-and-content/micro-copy-intelligence` when the findings are about strings;
`forms-and-content/conversion-optimization-patterns` for a funnel; `data-viz/data-visualization-mastery` for
charts; `platforms-and-ai/platform-visual-standards` for native.
**Gate:** every finding carries a severity rating and a location. Unrated
findings are opinions, and opinions don't survive a prioritization meeting.
**Artifact:** severity-ranked defect list.

### Fix — AI-generated UI that runs but looks wrong

1. `ux-evaluation/ui-pattern-intelligence` — detect the slop patterns and name them
2. `visual-design/visual-design-mastery` — score it and cite the canonical rules it breaks
3. `visual-design/ui-visual-design-system` — replace arbitrary values with a system
4. `design-systems/component-patterns-code` — rewrite it properly
5. `accessibility-i18n/accessibility-inclusive-design` — the states and labels the generator skipped
6. `forms-and-content/micro-copy-intelligence` — replace placeholder and robotic strings

**Depth:** `visual-design/color-palette-library`, `visual-design/typography-pairing-recipes`,
`visual-design/shadow-elevation-density`, `motion/animation-recipe-library`.
**Gate:** no hardcoded value that a token could carry, and every state the
generator skipped now exists. Report the before/after score delta.
**Artifact:** corrected code plus the score delta that justifies it.

### Create — designing something new

1. `ux-research/ux-research-methods` — what do we actually know about these users
2. `ux-evaluation/cognitive-psychology-ux` — the constraints the design must respect
3. `references-and-sectors/sector-style-intelligence` — what credible looks like in this category; then
   `references-and-sectors/reference-intelligence` — what award-level looks like right now, sourced and captured
4. `layout-and-flows/screen-flow-patterns` — which screens exist and what connects them
5. `visual-design/ui-visual-design-system` — type, color, hierarchy, spacing
6. `motion/interaction-motion-design` — how it moves and responds
7. `forms-and-content/performance-states-patterns` — empty, loading, error, offline, success
8. `accessibility-i18n/accessibility-inclusive-design` — before it's built, not after

**Depth:** `layout-and-flows/navigation-pattern-encyclopedia`, `forms-and-content/form-design-encyclopedia`,
`forms-and-content/micro-copy-intelligence`, `ux-evaluation/ui-pattern-intelligence`.
**Short form:** stages 3, 4, 5, 8 when the decision doesn't need the full run.
This is the one pipeline that exceeds six stages — say so before starting it, and
offer the short form.
**Gate:** every screen has all its states specified. A design that only shows the
happy path is a mockup, not a design.
**Artifact:** design specification with a state matrix.

### Implement — building the real thing

1. `design-systems/design-systems-architecture` — which tokens and components already exist
2. `visual-design/ui-visual-design-system` — visual spec for anything new
3. `design-systems/component-patterns-code` — production code, full state matrix, ARIA
4. `forms-and-content/micro-copy-intelligence` — every component ships strings; robotic labels are
   the loudest slop tell and the cheapest thing to fix
5. `accessibility-i18n/accessibility-inclusive-design` — verify against the built artifact
6. `forms-and-content/performance-states-patterns` — perceived performance and state handling

**Depth, routed by component type:** form → `forms-and-content/form-design-encyclopedia`; nav →
`layout-and-flows/navigation-pattern-encyclopedia`; chart or dense table →
`data-viz/data-visualization-mastery`; media → `visual-design/image-media-patterns`; icon →
`visual-design/icon-illustration-systems`; motion → `motion/animation-recipe-library`; breakpoints →
`layout-and-flows/responsive-block-patterns`; native → `platforms-and-ai/platform-visual-standards`.
**Gate:** keyboard-navigable, screen-reader-labelled, every state rendered.
**Artifact:** component code plus its state and a11y checklist.

### Compose — building a whole page

1. `references-and-sectors/sector-style-intelligence` — the register the page has to hit; `references-and-sectors/reference-intelligence`
   when the bar is award-level (live Awwwards winners → Reference Board)
2. `layout-and-flows/page-composition-engine` — block order, spacing rhythm, visual pacing
3. `layout-and-flows/layout-block-intelligence` — the individual sections
4. `forms-and-content/micro-copy-intelligence` — headlines and body that carry the argument
5. `layout-and-flows/responsive-block-patterns` — how each block transforms on small screens
6. `forms-and-content/performance-states-patterns` — loading behaviour and perceived speed

**Depth:** `visual-design/image-media-patterns`, `motion/animation-recipe-library`,
`forms-and-content/conversion-optimization-patterns`, `visual-design/typography-pairing-recipes`.
**Gate:** every block has a job in the page's narrative and a mobile form. No
block is decoration.
**Artifact:** page composition with block order and responsive behaviour.

### Generate — AI-generated design assets

1. `references-and-sectors/sector-style-intelligence` — the direction to generate toward
2. `platforms-and-ai/ai-design-generation` — the MCP models, prompts, and pipelines
3. `visual-design/visual-design-mastery` — score what came back
4. `ux-evaluation/ui-pattern-intelligence` — check it against real patterns, not plausible ones
5. `design-systems/component-patterns-code` — turn the accepted output into real code

**Depth:** `visual-design/icon-illustration-systems`, `visual-design/image-media-patterns`,
`visual-design/color-palette-library`.
**Gate:** nothing leaves this pipeline without a visual-quality score and a named
verdict — accept, regenerate, or hand-build. Generation's failure mode is exactly
the one uxlab exists to fix, so the gate is the point of the pipeline.
**Artifact:** generated assets plus the score and verdict for each.

### Systematize — starting or scaling a design system

1. `design-systems/design-systems-architecture` — token tiers, governance, versioning
2. `design-systems/design-token-presets` — start from a vetted vertical preset, not a blank file
3. `visual-design/color-palette-library` — the scale the semantic tokens alias
4. `visual-design/typography-pairing-recipes` — the type scale
5. `design-systems/component-patterns-code` — reference implementations
6. `design-systems/figma-design-tool-workflows` — keep design and code in sync

**Depth:** `visual-design/shadow-elevation-density`, `visual-design/ui-visual-design-system`,
`visual-design/visual-design-mastery`, `platforms-and-ai/platform-visual-standards`.
**Gate:** tokens are a single source of truth in W3C DTCG format, one change
propagates everywhere without hand-editing, and every component consumes a
semantic alias rather than a primitive directly.
**Artifact:** token file, component inventory, governance model.

### Handoff — design to code

1. `design-systems/figma-design-tool-workflows` — Auto Layout, variables, Dev Mode, MCP
2. `design-systems/design-systems-architecture` — map Figma variables onto real tokens
3. `design-systems/component-patterns-code` — generate the platform code
4. `layout-and-flows/responsive-block-patterns` — a frame set is fixed-width; responsive rules are
   the part that never survives handoff unless someone writes them down

**Gate:** generated code consumes tokens, not hardcoded values, and every
breakpoint transformation is specified rather than inferred.
**Artifact:** platform code traceable back to the source design.

### Convert — people arrive and don't finish

1. `forms-and-content/conversion-optimization-patterns` — funnel friction, CTA, pricing, checkout
2. `ux-evaluation/cognitive-psychology-ux` — the decision architecture underneath it
3. `forms-and-content/form-design-encyclopedia` — where forms are the drop-off
4. `forms-and-content/micro-copy-intelligence` — the strings that carry or kill the decision
5. `ux-evaluation/ux-ethics-content-strategy` — the ethics check, as a gate
6. `ux-research/ux-metrics-measurement` — how you would know it worked

**Gate:** every recommendation names the funnel step it affects and the metric
that would move — and clears stage 5. This is the pipeline where uxlab could most
easily be turned into a manipulation engine, so the dark-pattern check is a gate,
not a courtesy. A lift that depends on deceiving someone is not a finding, it is
a liability.
**Artifact:** ranked funnel-friction list with a test plan.

### Localize — new markets

1. `accessibility-i18n/cross-cultural-i18n-ux` — RTL, CJK, expansion, locale formats, color meaning
2. `visual-design/typography-pairing-recipes` — CJK, Arabic, and Cyrillic coverage is a font
   problem before it is a layout problem
3. `visual-design/ui-visual-design-system` — logical properties, flexible containers
4. `accessibility-i18n/accessibility-inclusive-design` — language attributes, reading order

**Depth:** `layout-and-flows/responsive-block-patterns`, `forms-and-content/micro-copy-intelligence`.
**Gate:** layout survives 40% text expansion and RTL mirroring.
**Artifact:** localization readiness report.

### AI Surface — designing an AI or agent feature

1. `platforms-and-ai/agentic-ai-generative-ux` — agent patterns, confidence, guardrails
2. `platforms-and-ai/ai-spatial-voice-ux` — conversational, voice, multimodal patterns
3. `forms-and-content/micro-copy-intelligence` — an agent's trustworthiness is almost entirely its
   strings
4. `ux-evaluation/ux-ethics-content-strategy` — consent, control, accountability
5. `ux-evaluation/cognitive-psychology-ux` — trust calibration and automation bias

**Depth:** `forms-and-content/performance-states-patterns` for streaming and latency,
`platforms-and-ai/ambient-calm-zero-ui` for screenless surfaces.
**Gate:** the user can tell what the AI did, why, and how to undo it.
**Artifact:** AI interaction spec with trust and recovery affordances.

### Measure — did it work

1. `ux-research/ux-metrics-measurement` — HEART, SUS, task success, statistical validity
2. `ux-research/ux-research-methods` — the study design that produces those numbers
3. `data-viz/data-visualization-mastery` — every one of these plans ends in a dashboard,
   and an unreadable dashboard is an unused one

**Depth:** `forms-and-content/conversion-optimization-patterns`.
**Gate:** every metric has a baseline. A metric without a baseline cannot show
improvement.
**Artifact:** measurement plan with baselines and instrumentation.

## Layers

### Platform

Layer the matching platform skill into whichever pipeline is running:

- Mobile or responsive → `platforms-and-ai/mobile-ux-design` + `platforms-and-ai/platform-visual-standards`
- Desktop, enterprise, dashboards, data-dense → `data-viz/desktop-app-design` +
  `data-viz/data-visualization-mastery`
- Ambient, wearable, automotive, screenless → `platforms-and-ai/ambient-calm-zero-ui`
- Native iOS or Android specifically → `platforms-and-ai/platform-visual-standards`

### Process

If the user asks what the process is called, wants a design sprint, or needs a
Double Diamond framing for stakeholders → `ux-research/design-process-methods`.

### Packaging

If the artifact is leaving the team — client, executive, portfolio — package it
with `references-and-sectors/business-design-templates`.

### Memory

Any pipeline spanning more than one command relies on `.uxlab/` to carry decisions
between them. `references-and-sectors/design-memory` holds that contract — the canonical schema, which
command owns which subtree, and the merge rules. Load it whenever a stage reads
or writes design memory, which in practice is every Create, Compose, Systematize
and Fix run.

## How this relates to the commands

- **Commands do not invoke pipelines.** A command has a fixed output contract.
  Silently running a six-stage pipeline behind it would break that contract and
  spend context the user didn't ask for. Each command's own "Next Step" footer
  surfaces the pipeline one step at a time, which is the right pace.
- **This skill does not invoke commands.** It names skills, because skills carry
  the knowledge. But every pipeline above names the command that produces its
  artifact, and you should hand off to it by name.
- **The chain is `/uxlab:start` → orchestrator → pipeline → command.** This is why
  `/uxlab:start` never has to list 37 commands.
- **Convert and Localize have no command yet.** Run them as pipelines and say so.

## Operating rules

- **Announce the pipeline before running it.** The user should know which stages
  are coming and roughly what each costs them in time.
- **One stage at a time.** Each skill's content stays in context once loaded, so
  running six at once is both slower and worse than running them in sequence.
  This is also why depth skills are opened inside a stage, not up front.
- **Report gate failures.** "Stage 3 failed the gate — 12 findings have no
  severity rating" is useful. Silently continuing is not.
- **Short-circuit narrow requests.** "What's a good tap target size?" is one
  skill, not a pipeline. Don't run process for its own sake.
- **Stop when the decision is answerable.** The pipeline serves the decision, not
  the other way around.

## Cross-references

Each pipeline's stages have their own reference files, listed inside each skill.
Load references only when the stage's SKILL.md points to them — they are large
and they persist in context once read.
