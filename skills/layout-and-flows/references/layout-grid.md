<!-- Derived from bama by Dave Ebbelaar (MIT), skills/design/layout-grid, upstream commit f0c2cdb. Adapted for web by uxlab. See NOTICE. -->

# Layout grid

Agents guess numbers. A guessed `padding: 13px` looks almost right and
makes the whole product feel slightly off. This reference replaces
guessing with one scale and three checks that fail when something is off.
Use it when building or reviewing a custom page, card, row, form, or
dialog, after every change that touched layout, and when something looks
misaligned, cramped, or unevenly spaced.

The scale lives in the project's token file, next to the other tokens
(the design system workflow reference of `design-systems`).

## The rules

1. Every padding, gap, margin, and size comes from the spacing scale:
   `--space-xs` 4 px, `sm` 8, `md` 12, `lg` 16, `xl` 20, `2xl` 24,
   `section` 32. Raw numbers are 0, 1 px, 2 px, or a multiple of 4. With
   Tailwind v4 and `--spacing: 0.25rem`, whole steps (`p-3`, `gap-2`) stay
   on the grid; half steps above `0.5` (`p-2.5`, `gap-1.5`) and arbitrary
   values (`p-[13px]`) do not.
2. Pages have one margin token, `--space-margin`, that steps up the scale
   by breakpoint (for example 16 px on small screens, 24 px from tablet
   up). Cards pad 16. Related controls sit 8 apart, groups 20 to 24,
   sections 32.
3. Each column has one leading edge. Titles, text, cards, and buttons in a
   column start on the same x. Indent on purpose, by a step of the scale.
4. Let the layout do the aligning:
   - Labels with controls: one form layout on every form, labels above
     fields or a grid with `grid-template-columns: max-content 1fr`.
   - Rows and columns of values: CSS grid or a `table`; `subgrid` when
     parts of sibling cards must line up.
   - A label with a value: a `dl` laid out on a grid.
   - Text of different sizes in one row: `align-items: baseline`.
   - Numbers in a column: `font-variant-numeric: tabular-nums`, aligned to
     the end.
   - An icon with text: `inline-flex`, `align-items: center`, a scale gap,
     the icon sized in `em`.
5. Dialogs are 360, 480, or 640 px wide, as a `max-width` that gives way
   to the page margin on small screens. Controls take their height from
   the component's size variant (`sm`, `md`, `lg`), never a one-off height.
6. Nested corners are concentric: inner radius = outer radius - padding.
7. `position: absolute`, `transform: translate`, and negative margins move
   a box outside the layout, so nothing lines up with it. Use them only for
   motion, overlays anchored to a trigger, and drag previews, with
   `/* grid: ok <why> */` on the line.
8. Long text truncates with its full value in a tooltip. Nothing clips.
   A flex or grid child needs `min-width: 0` to truncate.
9. At every breakpoint the grid still holds: columns collapse in a set
   order, margins step by the scale, and nothing scrolls sideways at 320
   px. Breakpoint and container query patterns:
   `layout-and-flows/responsive-block-patterns`.

## Check 1: scan the code

Run it after every change that touched styles. Adjust `src/` to the
project.

```bash
# px values that are not 0, 1, 2, or a multiple of 4
grep -rnoE '\b[0-9]+(\.[0-9]+)?px\b' src/ | awk -F: '{ v = $NF + 0; if (v > 2 && v % 4) print }'
# Tailwind half steps and arbitrary spacing values
grep -rnE '\b-?(p|m|gap|space|inset|top|right|bottom|left|w|h|size)[xytrbl]?-([1-9][0-9]*\.5|\[[0-9.]+(px|rem)\])' src/
```

Fix each hit with a scale token. A value outside spacing (a font size, a
1 px hairline, an icon box) is fine when it comes from its own token.

## Check 2: measure the real layout

Measure what you lay out yourself: the page, its sections, cards, rows in a
card, dialog content. Library tables, forms, and navigation that align
themselves need no probes. While reviewing, mark each part with
`data-probe="name"` and run this in the devtools console:

```js
console.table([...document.querySelectorAll("[data-probe]")].map((el) => {
  const r = el.getBoundingClientRect();
  const area = el.parentElement.closest("[data-probe]") ?? document.body;
  const a = area.getBoundingClientRect();
  const pad = parseFloat(getComputedStyle(area).paddingLeft);
  return { probe: el.dataset.probe, area: area.dataset.probe ?? "body", x: r.left, fromArea: r.left - a.left - pad, y: r.top, right: a.right - r.right };
}));
```

Run it at each breakpoint width the project supports. Check that every
probe:

1. Starts on a whole pixel, so its edges stay sharp.
2. Starts a multiple of 4 px from its area's content edge (`fromArea`).
3. Stays inside its area's padding on both sides.
4. Shares one `x` with the other probes in its column.
5. Sits a multiple of 4 px below the probe above it.
6. Never overlaps another probe in its area.

## Check 3: look at the grid

When a check fails and the cause is not clear, draw an 8 px grid over the
page and outline the probes, then take a screenshot and read it:

```js
const s = document.createElement("style");
s.textContent = `body::after { content: ""; position: fixed; inset: 0; pointer-events: none; z-index: 2147483647;
  background: linear-gradient(90deg, #f0f3 1px, transparent 1px) 0 0 / 8px 8px, linear-gradient(#f0f3 1px, transparent 1px) 0 0 / 8px 8px; }
  [data-probe] { outline: 1px solid #f0f; }`;
document.head.append(s);
```

## Fix a failure

| Finding | Usual cause | Fix |
| --- | --- | --- |
| starts 23 px into its area | a raw padding or margin on one child | remove it, use the container's padding token |
| 2 leading edges | a centered item (`align-items: center`, `margin: auto`), or one child with extra padding | `align-items: start` on the container |
| gap 10 px | `gap: 10px`, a margin on one child, or `gap-2.5` | a scale token on the container's `gap` |
| outside its area's padding | a missing margin, or a fixed width wider than the parent | `padding: var(--space-margin)`, `max-width` instead of `width` |
| overlap | absolute positioning, a transform, a negative margin, or a fixed height | remove it, let the layout size the box |
| x between pixels | a fractional value (`rem` that misses a whole pixel, percentage widths, `translate(-50%)`) | a whole value from the scale |
| sideways scroll at 320 px | a fixed width, a long unbroken string, a wide table | `max-width: 100%`, `overflow-wrap: anywhere`, a scroll container around the table |

Done when both scans in Check 1 find nothing new, Check 2 passes at every
breakpoint on every page you touched, and every custom page and card had
its main parts probed.
