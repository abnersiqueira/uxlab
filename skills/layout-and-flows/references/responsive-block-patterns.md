<!-- Derived from Sumi 4.2.0 by Phazur Labs (Apache-2.0), skills/responsive-block-patterns/SKILL.md, upstream commit 3a3693b. Modified by uxlab: consolidated into a domain skill, renamed, cross-references rewritten. See NOTICE. -->
# Responsive Block Patterns — Cross-Breakpoint Design Intelligence

## Mental model

Responsive design is not resizing. It is deciding, per component, which of four
things happens as space runs out: it **reflows**, it **stacks**, it
**transforms** into a different component, or it **disappears**.

- **Container queries beat media queries** for anything reusable. A card should
  respond to its container, not the viewport, or it breaks the moment you put it
  in a sidebar.
- **Fluid before stepped.** `clamp()` handles the continuum; breakpoints handle
  the genuine transformations. Six breakpoints usually means someone was using
  them to do `clamp()`'s job.
- **Design the transformation, not the two end states.** A table becoming a card
  list is a decision about what to drop; specifying only "table" and "cards"
  leaves that decision to whoever implements it.
- **Touch targets do not scale down.** 44px is 44px at every breakpoint.

## Constants

```css
--bp-sm:  640px;   /* large phone            */
--bp-md:  768px;   /* tablet portrait        */
--bp-lg: 1024px;   /* tablet landscape, small laptop */
--bp-xl: 1280px;   /* desktop                */
--bp-2xl:1536px;   /* wide desktop           */
```

The `clamp()` master formula: `clamp(min, preferred + relative, max)`, where
preferred is in `rem` and relative is in `vw`.

## Index

| Need | Reference |
|---|---|
| What a given component does at each breakpoint | `breakpoint-transformation-catalog.md` |
| Adaptive card, morphing nav, table-to-cards | `container-query-patterns.md` |
| Container query syntax and units | `container-query-patterns.md` |
| Fluid type scale, fluid space scale | `fluid-scaling-system.md` |
| The `clamp()` formula and when it beats breakpoints | `fluid-scaling-system.md` |
| Responsive typography, images, tables, nav as code | `responsive-component-patterns.md` |
| Column progressions, collapsing sidebar, holy grail | `responsive-layout-recipes.md` |

## Reference architecture

| File | Covers | Lines |
|---|---|---|
| `responsive-block-patterns/responsive-component-patterns.md` | component-level responsive code | 1878 |
| `responsive-block-patterns/container-query-patterns.md` | container query recipes | 1728 |
| `responsive-block-patterns/responsive-layout-recipes.md` | whole-layout recipes | 1524 |
| `responsive-block-patterns/fluid-scaling-system.md` | clamp(), fluid scales | 842 |
| `responsive-block-patterns/breakpoint-transformation-catalog.md` | 60+ components x breakpoint | 707 |

## What every reference file contains

1. The transformation type — reflow, stack, transform, or hide
2. The breakpoint or container size that triggers it, and why that value
3. Complete CSS, container-query-first where it applies
4. What is deliberately dropped at the smallest size
5. Touch target and thumb-reach implications

## Routing

For **what each component does at each breakpoint** — 60+ components across
navigation, content, input and layout with their transformation type: read
`responsive-block-patterns/breakpoint-transformation-catalog.md`.

For **container queries** — fundamentals plus adaptive cards, morphing
navigation, table-to-card transformation and the rest: read
`responsive-block-patterns/container-query-patterns.md`.

For **fluid scaling** — the `clamp()` master formula, complete fluid type and
space scales, and fluid padding: read `responsive-block-patterns/fluid-scaling-system.md`.

For **component-level responsive code** — responsive typography, images, tables,
navigation and the other patterns as production CSS: read
`responsive-block-patterns/responsive-component-patterns.md`.

For **whole-layout recipes** — column progressions, collapsing sidebars, holy
grail and the rest: read `responsive-block-patterns/responsive-layout-recipes.md`.

For **odds and ends** — the patterns that had no home in the files above when this skill was converted to a router: read `responsive-block-patterns/responsive-supplementary.md`.

## Cross-References

- `layout-and-flows/layout-block-intelligence`, `design-systems/component-patterns-code`, `platforms-and-ai/mobile-ux-design`, `layout-and-flows/page-composition-engine`
- `platforms-and-ai/platform-visual-standards` (iOS 26, Material 3 breakpoint conventions)
- `forms-and-content/form-design-encyclopedia` (responsive form patterns)
- `layout-and-flows/navigation-pattern-encyclopedia` (responsive nav transformations)
- `visual-design/typography-pairing-recipes` (fluid type scales)
- `data-viz/data-visualization-mastery` (responsive chart patterns)
