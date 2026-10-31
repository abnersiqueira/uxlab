<!-- Derived from bama by Dave Ebbelaar (MIT), skills/design/ux-design/accessibility.md, upstream commit f0c2cdb. Adapted for web by uxlab. See NOTICE. -->

# Accessibility audit

How to check step 7 of [SKILL.md](../SKILL.md) on a running build, and the
HTML, ARIA, and CSS that fix what it finds. Native elements (`button`,
`a`, `input`, `select`, `dialog`) do most of this on their own. Custom
controls need the work. WCAG criteria and inclusive design in depth:
`accessibility-i18n/accessibility-inclusive-design`.

## Contents

- Run the audit
- Keyboard
- Screen readers
- Custom controls
- Color and contrast
- Motion and transparency
- Text size

## Run the audit

1. Start the app with the project's dev command and open each new view.
2. Run the browser devtools accessibility audit (or the project's
   automated checker) on each new view. Read the accessibility tree for
   each new control: role, name, and state.
3. Put the mouse away. Run the whole flow with Tab, Shift-Tab, arrows,
   Enter, Esc, and Space.
4. Turn on a screen reader and run the flow again, listening. Use a mobile
   screen reader too when the view has a touch layout.
5. One at a time: emulate `prefers-reduced-motion: reduce`,
   `prefers-contrast: more`, and `forced-colors: active` in devtools, zoom
   the browser to 200%, and narrow the viewport to 320 px. Look at each
   new view in the light and dark theme.

Done when the audit shows no issues for the new views and both runs
finish the flow without the mouse.

## Keyboard

- Every step of the flow is reachable with the keyboard, in reading order.
  DOM order matches visual order; no positive `tabindex`.
- The default button responds to Enter (it is the form's submit button),
  Cancel to Esc.
- A new item gets focus so people can type at once.
- Focus is always visible: style `:focus-visible`, never remove the
  outline without a replacement.
- A modal keeps focus inside while open and returns it to the control
  that opened it on close. `dialog.showModal()` does both.

```js
// After adding a row, focus its title field.
list.lastElementChild.querySelector("input").focus();
```

## Screen readers

- The accessible name matches the words on screen. An icon-only button
  takes its name as `aria-label`; the tooltip describes what it does.
- A row reads as one item. Its actions sit in one menu button named for
  the row ("Actions for Pay rent").
- Decorative images stay silent: `alt=""`, or `aria-hidden="true"` on
  inline SVG.

```html
<button type="button" aria-label="New task" aria-describedby="tip-new" aria-keyshortcuts="N">
  <svg aria-hidden="true" focusable="false"><!-- plus icon --></svg>
</button>
<div role="tooltip" id="tip-new">Add a task to this list (N)</div>
```

- Section titles are headings (`h2`, `h3`) inside landmarks (`header`,
  `nav`, `main`), so screen readers can jump between them.
- When content changes without a click (a sync finishes, a filter empties
  the list), announce it from a live region that exists before the
  change: `<p role="status">No tasks left</p>`.
- A chart gets a one-line summary as its name ("Spending rose 12% in
  October").
- Voice control says what people see: the accessible name starts with the
  visible label.
- No view that hides itself on a timer is the only way to act. An Undo
  toast also has a shortcut or a lasting place (history, trash).

## Custom controls

Use the native element when it can be styled to fit (`input
type="range"`, `input type="checkbox"`). A custom control answers four
questions: what it is (role and name), what it is set to (value), what
people can do (keyboard actions), and what changed (feedback). A control
that only works with a drag also offers keys or buttons, so keyboard and
voice users reach it. Full state and ARIA matrices per component:
`design-systems/component-patterns-code`.

```html
<div role="slider" tabindex="0" aria-label="Volume"
     aria-valuemin="0" aria-valuemax="100" aria-valuenow="40" aria-valuetext="40%"></div>
```

```js
const steps = { ArrowUp: 10, ArrowRight: 10, ArrowDown: -10, ArrowLeft: -10, PageUp: 25, PageDown: -25 };
dial.addEventListener("keydown", (e) => {
  if (e.key === "Home") setLevel(0);
  else if (e.key === "End") setLevel(100);
  else if (e.key in steps) setLevel(Math.min(100, Math.max(0, level + steps[e.key])));
  else return;
  e.preventDefault();
});
// setLevel updates aria-valuenow and aria-valuetext; the screen reader
// speaks the new value. During a drag, update them as the value moves.
```

A two-axis control (a color square, a position pad) moves on both axes
with the arrow keys, in a fixed step that stops at the edges, and its
`aria-valuetext` states both values.

## Color and contrast

- Status color always comes with an icon or a word.
- Body text contrast is at least 4.5 to 1 against its background, in the
  light and dark theme. Aim for 7 to 1 for small text in custom colors.
  Borders of controls and the focus ring reach 3 to 1.
- Honor `prefers-contrast: more` and `forced-colors: active` in custom
  views. In forced colors, backgrounds drop out, so a meaning carried by a
  fill needs a border or an icon.

```css
@media (prefers-contrast: more) {
  :root { --color-border: var(--color-border-strong); }
}
@media (forced-colors: active) {
  .status-badge { border: 1px solid CanvasText; }
}
```

## Motion and transparency

Replace slides, springs, and parallax with a fade when reduced motion is
requested. Never animate a blur or a change in depth (scale toward the
viewer) under reduced motion. Never make people wait for an animation: it
can be interrupted. Give translucent, blurred surfaces a solid fallback.

```css
.drawer { transition: transform 200ms var(--ease-out); }

@media (prefers-reduced-motion: reduce) {
  .drawer { transition: opacity 150ms linear; transform: none; }
}
@media (prefers-reduced-transparency: reduce) {
  .glass { backdrop-filter: none; background: var(--color-surface); }
}
```

## Text size

- Body text is 16 px (14 px in dense product views) and nothing is under
  12 px. Set sizes from the type tokens in `rem`, so the browser's text
  size setting applies.
- Truncated text shows its full value in a tooltip that opens on hover
  and focus, or in the detail view.

```css
.truncate { min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
```

- People must be able to enlarge text to 200%. At 200% zoom and at a 320
  px wide viewport the page reflows: nothing clips, nothing overlaps, and
  only data tables and similar two-axis content scroll sideways.
