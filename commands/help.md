---
name: help
description: "Command map and quick start — see all 38 commands, starter recipes, Design Quality Score, anti-slop engine, and tips for best results. Start with /uxlab:start if you are new."
argument-hint: "[optional: command or topic]"
---
<!-- Derived from Sumi 4.2.0 by Phazur Labs (Apache-2.0), commands/sumi.md, upstream commit 3a3693b. Modified by uxlab: renamed, cross-references rewritten. See NOTICE. -->
> Reference notation: `domain/name` is the file `references/name.md` of the `uxlab:domain` skill. Invoke that skill, then open the file.


# uxlab — Your Design Intelligence System

Welcome to uxlab v4.2.0. 38 commands. 45 skills. 4 team agents. Vibe coded slop into visual cuisine.

**New here?** Run `/uxlab:start` instead. It asks one question and routes you — no need to read this map.

## Quick Start

```
# The fast track — style it, build it, ship it
/uxlab:style [sector]  →  /uxlab:screen [type]  →  /uxlab:fix  →  ship

# The quality track — fix slop, prove it, ship it
/uxlab:fix  →  /uxlab:before-after  →  /uxlab:grade  →  ship

# The studio track — look at real award winners first, then build and grade against them
/uxlab:inspo [brief]  →  /uxlab:style  →  /uxlab:page  →  /uxlab:grade

# The full track — plan, design, review, ship
/uxlab:brief  →  /uxlab:style  →  /uxlab:screen  →  /uxlab:roast  →  /uxlab:fix  →  /uxlab:preflight
```

---

## Hero Commands

| Command | What It Does |
|---------|-------------|
| `/uxlab:fix` | Anti-slop engine — transforms AI-generated UI into production quality |
| `/uxlab:style` | Complete visual identity with 10 zero-config starter recipes |
| `/uxlab:grade` | Design Quality Score (0-100) like Lighthouse for design |
| `/uxlab:before-after` | Visual proof of design transformation |
| `/uxlab:screen` + `/uxlab:component` | Platform-aware code (web/iOS/Android) |

---

## All 38 Commands

### MAKE — Design and Build (20)

Generate visual design systems, screens, components, and production-ready code.

| Command | What It Does |
|---------|-------------|
| `/uxlab:fix` | Anti-slop engine — 60+ detection patterns, full code transformation |
| `/uxlab:style` | Sector-aware visual direction — palette, typography, spacing, mood |
| `/uxlab:palette` | Deep color system with oklch, APCA contrast, dark mode mapping |
| `/uxlab:type` | Typography system — font pairing, scale, fluid sizing |
| `/uxlab:layout` | Layout section/block patterns — hero, features, pricing, CTA, dashboard |
| `/uxlab:wireframe` | Low-fidelity wireframes and layout exploration |
| `/uxlab:screen` | Full production screens with all states (empty, loading, error, success) |
| `/uxlab:component` | Production components with accessibility baked in |
| `/uxlab:page` | Full page compositions with block stacking and visual rhythm |
| `/uxlab:tokens` | Complete design token system (color, type, spacing, motion, elevation) |
| `/uxlab:form` | Form design — inputs, validation, multi-step, accessibility |
| `/uxlab:nav` | Navigation system — top bar, sidebar, tabs, command palette, mega menu |
| `/uxlab:animate` | Motion design — entrance, micro-interaction, page transition, scroll |
| `/uxlab:icon` | Icon and illustration systems with SVG implementation |
| `/uxlab:dark` | Dark mode — color mapping, contrast verification, seamless toggle |
| `/uxlab:responsive` | Cross-breakpoint design — container queries, fluid scaling, grids |
| `/uxlab:onboard` | Onboarding flow with activation metrics and progressive disclosure |
| `/uxlab:generate` | AI-powered screen generation (Stitch MCP, Fal.ai) |
| `/uxlab:remix` | Evidence-based redesign of weak areas |
| `/uxlab:figma` | Figma design-to-code via MCP — extracts tokens, components, layout |

### REVIEW — Evaluate and Improve (7)

Audit existing designs for quality, accessibility, and usability problems.

| Command | What It Does |
|---------|-------------|
| `/uxlab:audit` | Nielsen's 10 heuristics + Laws of UX + Gestalt + cognitive load analysis |
| `/uxlab:roast` | Liz Lerman critique with dimensional scoring + AI slop detection |
| `/uxlab:grade` | Design Quality Score (0-100) — Lighthouse-style scoring with badge generation |
| `/uxlab:qa` | Design QA — spec vs. implementation comparison. `/uxlab:qa project` scans full codebase |
| `/uxlab:a11y` | WCAG 2.2 accessibility audit. `/uxlab:a11y fix` generates corrected code |
| `/uxlab:before-after` | Visual proof of design transformation — side-by-side comparison |
| `/uxlab:ai-audit` | AI and agent interface audit — trust, control, recovery, disclosure |

### PLAN — Research and Strategy (7)

Research users, analyze competitors, plan metrics, and prepare for launch.

| Command | What It Does |
|---------|-------------|
| `/uxlab:brief` | Problem definition — persona, HMW questions, constraints, success criteria |
| `/uxlab:inspo` | Real references — live Awwwards winners, Mobbin flows, MotionSites recipes → captured DNA → Reference Board |
| `/uxlab:research` | User research AND usability testing — interviews, surveys, test plans |
| `/uxlab:benchmark` | Competitive analysis — 10-dimension scorecard, gap analysis, roadmap |
| `/uxlab:map` | Information architecture — sitemap, navigation, content hierarchy |
| `/uxlab:measure` | Metrics plan — HEART framework, OKRs, experimentation, dashboards |
| `/uxlab:preflight` | Pre-launch checklist AND post-launch plan — the full launch playbook |

### Utility (4)

| Command | What It Does |
|---------|-------------|
| `/uxlab:start` | Zero-knowledge entry point. One question, then it routes you. |
| `/uxlab:help` | You're here. Command map, quick start, tips. |
| `/uxlab:next` | Context-aware suggestion of what to do next |
| `/uxlab:status` | Progress dashboard of what you've generated |

---

---

## Renamed in v4.0.0

uxlab 3.1.0 and Chef uxlab were one lineage that had forked. v4.0.0 merges them.
Where both shipped a command for the same job, the richer one survived. If you
were using a 3.1.0 name, here is where it went:

| 3.1.0 name | Now |
|---|---|
| `/accessibility-check` | `/uxlab:a11y` |
| `/ux-audit` | `/uxlab:audit` |
| `/design-review` | `/uxlab:audit` (see its domain roll-up section) |
| `/cognitive-check` | `/uxlab:audit cognitive` |
| `/design-critique` | `/uxlab:roast` |
| `/component-build` | `/uxlab:component` |
| `/generate-design-tokens` | `/uxlab:tokens` |
| `/ux-metrics-plan` | `/uxlab:measure` |
| `/figma-to-code` | `/uxlab:figma` |
| `/ai-ux-audit` | `/uxlab:ai-audit` |


## Starter Recipes

One word. Zero config. Complete visual identity.

```
/uxlab:style saas         →  Linear DNA
/uxlab:style fintech      →  Stripe DNA
/uxlab:style ecommerce    →  Shopify DNA
/uxlab:style healthcare   →  One Medical DNA
/uxlab:style creative     →  Awwwards DNA
/uxlab:style education    →  Duolingo DNA
/uxlab:style social       →  Discord DNA
/uxlab:style devtools     →  GitHub DNA
/uxlab:style landing      →  Vercel DNA
/uxlab:style mobile       →  iOS/Android adaptive
```

---

## Workflows by Goal

**"Fix my AI-generated code"**
`/uxlab:fix` → `/uxlab:before-after`

**"Build a screen fast"**
`/uxlab:style [sector]` → `/uxlab:screen [type]`

**"Get a design quality score"**
`/uxlab:grade` (or `/uxlab:grade vs stripe`)

**"Complete design system"**
`/uxlab:style` → `/uxlab:tokens` → `/uxlab:screen` → `/uxlab:component`

**"Review existing design"**
`/uxlab:audit` → `/uxlab:roast` → `/uxlab:a11y` → `/uxlab:grade`

**"Start from scratch"**
`/uxlab:brief` → `/uxlab:research` → `/uxlab:style` → `/uxlab:screen`

**"Ship by Friday"**
`/uxlab:style` → `/uxlab:screen` → `/uxlab:fix` → `/uxlab:qa` → `/uxlab:preflight`

**"Scan my whole codebase"**
`/uxlab:qa project`

---

## What's New in v4.2.0

- **Reference Engine** (`/uxlab:inspo`) — sources live Awwwards winners (jury score, tags, live URL), Mobbin screens and flows (MCP) and MotionSites motion recipes. It captures the real sites on desktop and phone, measures their DNA (type scale, tracking, palette by painted area, section rhythm, grid, radius, motion stack), and writes a Reference Board to `.uxlab/refs/`.
- **The team** — four subagents: `scout` sources references, `art-director` sets direction, `ux-architect` designs flows from real Mobbin patterns, and `critic` grades your build side by side with the board.
- **Calibrated grading** — with a board present, `/uxlab:grade` and `/uxlab:roast` score the build next to the best reference and report per-dimension deltas.

## What's New in v4.0.0

- **Anti-Slop Engine** (`/uxlab:fix`) — 60+ detection patterns, full code transformation. Turns AI-generated UI into production quality.
- **Design Quality Score** (`/uxlab:grade`) — 0-100 Lighthouse-style scoring with badge generation. Benchmark against any product.
- **Before/After** (`/uxlab:before-after`) — Visual proof of design transformation with side-by-side comparison.
- **Platform-Aware Generation** — `/uxlab:screen` and `/uxlab:component` auto-detect iOS/Android/web and generate platform-native code.
- **Starter Recipes** — 10 zero-config design systems. One word each. Instant visual identity.
- **Project-Wide QA** — `/uxlab:qa project` scans entire codebase for design drift and inconsistency.
- **Cognitive Load Analysis** — `/uxlab:audit` now includes Laws of UX and Gestalt evaluation alongside Nielsen's heuristics.
- **Design Memory v2** — Auto-detects existing Tailwind config and CSS custom properties. `.uxlab/` carries context across all commands.
- **WCAG Auto-Fix** — `/uxlab:a11y fix` generates corrected code for every accessibility finding.
- **AI Slop Detection** — `/uxlab:roast` and `/uxlab:audit` now flag AI-generated UI patterns (default spacing, placeholder copy, generic icons).

---

## Tips for Best Results

1. **Start with `/uxlab:style`**. Takes 2 minutes, makes everything 10x better.
2. **Run `/uxlab:fix` on any AI-generated code**. It's the fastest path to production quality.
3. **Use `/uxlab:grade` before every PR**. If it scores below 70, run `/uxlab:fix`.
4. **The more context you give, the better the output**. Paste screenshots, code, URLs, Figma exports.
5. **Commands compose**. `/uxlab:style` → `/uxlab:screen` → `/uxlab:fix` → `/uxlab:grade` builds on each step.
6. **Design memory carries across commands**. Run `/uxlab:style` once, benefit everywhere.
7. **Be specific about screen types**. `/uxlab:screen dashboard` beats `/uxlab:screen`. `/uxlab:screen settings mobile iOS` beats `/uxlab:screen settings`.
8. **REVIEW commands work on anything**. Paste a screenshot, a URL, a code snippet, a Figma export.

---

## 45 Skills (Auto-Invoked)

Skills activate automatically when relevant. You never need to call them directly.

**Routing**: `uxlab/orchestrator` — picks the pipeline and runs its stages in order. This is what `/uxlab:start` talks to.

**Core UX**: `ux-research/design-process-methods`, `ux-evaluation/nng-ux-heuristics`, `ux-research/ux-research-methods`, `ux-evaluation/cognitive-psychology-ux`, `ux-research/ux-metrics-measurement`, `ux-evaluation/ux-ethics-content-strategy`

**Platform**: `platforms-and-ai/mobile-ux-design`, `data-viz/desktop-app-design`, `platforms-and-ai/platform-visual-standards`, `accessibility-i18n/cross-cultural-i18n-ux`

**Visual**: `references-and-sectors/reference-intelligence`, `visual-design/ui-visual-design-system`, `visual-design/visual-design-mastery`, `visual-design/color-palette-library`, `visual-design/typography-pairing-recipes`, `visual-design/shadow-elevation-density`, `visual-design/image-media-patterns`, `visual-design/icon-illustration-systems`

**Patterns**: `layout-and-flows/screen-flow-patterns`, `ux-evaluation/ui-pattern-intelligence`, `layout-and-flows/layout-block-intelligence`, `layout-and-flows/page-composition-engine`, `layout-and-flows/navigation-pattern-encyclopedia`, `forms-and-content/form-design-encyclopedia`, `layout-and-flows/responsive-block-patterns`

**Interaction**: `motion/interaction-motion-design`, `motion/animation-recipe-library`, `forms-and-content/performance-states-patterns`, `platforms-and-ai/ambient-calm-zero-ui`

**Systems**: `design-systems/design-systems-architecture`, `design-systems/component-patterns-code`, `design-systems/design-token-presets`, `data-viz/data-visualization-mastery`

**AI & Generation**: `platforms-and-ai/ai-spatial-voice-ux`, `platforms-and-ai/agentic-ai-generative-ux`, `platforms-and-ai/ai-design-generation`, `design-systems/figma-design-tool-workflows`

**Strategy**: `references-and-sectors/sector-style-intelligence`, `forms-and-content/conversion-optimization-patterns`, `forms-and-content/micro-copy-intelligence`, `ux-evaluation/design-critique-case-studies`, `accessibility-i18n/accessibility-inclusive-design`, `references-and-sectors/business-design-templates`

---

Start building. `/uxlab:style [your sector]` is a good first move. Or paste your code and run `/uxlab:fix`.
