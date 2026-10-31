<!-- Derived from bama by Dave Ebbelaar (MIT), skills/design/design-system, upstream commit f0c2cdb. Adapted for web by uxlab. See NOTICE. -->

# Design system workflow

A design system is a short list of **tokens** in code and one page that
says which token to use when. Every screen uses tokens, never raw values.
Then a change in one place changes the whole product, and an agent can
review a screen against one page.

Start from what the browser and the component library already give:
native controls, the library's default theme, the user's light or dark
preference. Tokens cover what the product decides: the accent, surfaces
and text colors, type, spacing, radii, layout widths, motion, and
overlays. Token tiers, naming, and governance:
`design-systems/design-systems-architecture`. A ready starting set:
`design-systems/design-token-presets`. Visual craft for parts of your own
(color, type, icons): `visual-design/ui-visual-design-system`.

Look for the base before writing one: a `tokens.css`, a Tailwind v4
`@theme` block in the main stylesheet, a `tokens.json`, or the component
library's theme file. With none, create one stylesheet of CSS custom
properties on `:root` and import it first.

Light and dark follow the person's system setting (`prefers-color-scheme`).
Add a System, Light, Dark switch only when the owner asks for one, with
System as the default.

## 1. Pick the accent

Read the look or brand section of `BRIEF.md`, `PRODUCT.md`, or
`DESIGN.md`. With no color named, keep the component library's default
accent.

For a brand color, define three shades: `light` (accent text in the dark
theme), `base` (fills, focus ring, selection), and `deep` (accent text in
the light theme). Put dark text on `base` when white text on it is under
4.5 to 1 (yellow, mint, cyan).

The accent marks the primary action, selection, focus, and links. Use
brand color beyond that sparingly: the logo, an empty state, one hero
element in the content. Keep it off most controls.

Optional theming: when people or workspaces pick their own accent, each
choice is a full set of the three shades plus `on-accent`, switched by an
attribute on the root (`data-accent="teal"`), and every choice passes the
contrast checks.

To compare colors, take screenshots of two or three key screens with two
or three candidate accents and show the user the images.

Check: buttons, toggles, selection, focus ring, and links show the accent
in the light and dark theme, and accent text and text on accent fills
reach 4.5 to 1 in both.

## 2. Collect

New product with no screens yet? Skip this step: write the token file with
the defaults below before the first screen.

Existing product: read every component and stylesheet. List each raw value
you find: hex, rgb, hsl, and oklch colors, opacities, border radii,
paddings, margins, gaps, widths, font sizes and weights, durations and
easing curves, shadows, z-indexes, one-off button styles, and Tailwind
arbitrary values (`p-[13px]`). Group them. Most products have 3 to 5 of
each where 1 or 2 are meant.

## 3. Write the tokens

One group per row, in one token file or `@theme` block. Add each token
when the product first needs it:

| Group | Holds |
| --- | --- |
| Accent | `--color-accent`, `--color-on-accent` (text and icons on accent fills), `--color-accent-text` (accent-colored text: deep shade in the light theme, light shade in the dark theme) |
| Spacing | the spacing scale; rules in the layout grid reference of `layout-and-flows` |
| Surfaces and text | `--color-surface`, `--color-surface-hover`, `--color-border` (hairline), `--color-text`, `--color-text-muted`, one warning color |
| Radius | `--radius-xs` 6 px chips and key caps, `sm` 8 controls, `row` 10 row hover fills, `md` 12 cards, `lg` 18 popovers and dialogs, `xl` 26 large floating surfaces |
| Type | `--font-sans` (the text font stack), `--font-heading`, `--font-mono`, and a type scale in `rem` |
| Layout | `--content-width`, fixed column, side panel, and dialog widths |
| Motion | `hover`, `quick` (presses, small flips), `ui`, `select` (selection moving through a live list), `appear`, `dismiss`, `glide`, `number-roll`, `list-change`, each a duration and an easing; loops (`pulse`) that stop under reduced motion |
| Components | shared variants in the component library, not in the token file: button and hover-fill styles, toggles, chips |
| Overlay | one primitive each for dialog, popover, and drawer, one entrance, one exit, and the shadow and z-index tokens they use |

Colors adapt to light and dark in the token, so components never branch
on the theme:

```css
:root {
  color-scheme: light dark;
  --color-accent: light-dark(oklch(0.55 0.19 255), oklch(0.68 0.16 255));
  --color-accent-text: light-dark(oklch(0.47 0.19 255), oklch(0.80 0.11 255));
  --color-on-accent: oklch(1 0 0);
}
[data-theme="light"] { color-scheme: light; }
[data-theme="dark"] { color-scheme: dark; }
@media (prefers-contrast: more) {
  :root { --color-accent-text: light-dark(oklch(0.38 0.19 255), oklch(0.88 0.08 255)); }
}
```

With Tailwind v4, declare the same names in `@theme` so utilities
(`bg-accent`, `rounded-md`) read them.

## 4. Write the usage page

One section per group above. Each section says which token to use when,
and the rules that go with it. Keep it under 100 lines. Put it where the
project keeps design docs: a `## Tokens` section in `DESIGN.md` when it
exists, else `DESIGN-SYSTEM.md` beside the token file. Rules that transfer
to most products:

- Never hard-code an accent value. Use `var(--color-accent)` or its
  utility.
- Every custom color has four values: light, dark, and a stronger one of
  each for `prefers-contrast: more`.
- Use each semantic token for its job only (never the border color as
  text, a text color as a fill). Their values change with the theme.
- A custom font only for headings. Body and captions stay in the text
  font stack, and every loaded font includes its bold weight, so bold text
  never renders as synthesized bold.
- Accent-colored text uses `--color-accent-text`. Text on an accent fill
  uses `--color-on-accent`, never a fixed white.
- Style native controls or the library's accessible primitives. Never
  rebuild a control from `div`s: it loses the keyboard, focus, and screen
  reader support.
- Inner corners are concentric: inner radius = outer radius - inset.
- Every animation goes through the motion tokens, so reduced motion and
  any in-product motion setting apply everywhere.
- Search results and switchers (command palette results, tab changes) do
  not animate. Speed wins.
- Hover never moves a selection. Only a click or a key does.
- Units ("KB/s", "%") never animate. Only the number does, in
  `tabular-nums`.
- Never animate a view's first render. Overlays start one frame later (or
  from `@starting-style`), then animate opacity, scale, and a few pixels of
  travel.
- Leave room around a floating surface for its shadow (about 3 times the
  shadow blur); a parent with `overflow: hidden` clips it.
- One primary button per page or card.

## 5. Migrate

Replace raw values screen by screen, one commit per screen. After each,
run the app and compare screenshots before and after (the project's visual
tests, if it has them). The screen looks the same or better, never worse.

## 6. Point agents at it

Add one line to the project's agent instructions file (`AGENTS.md` or
`CLAUDE.md`; create it if missing): "Design rules: `<path to the usage
page>`. Use its tokens; never raw colors, radii, or durations."

Done when this finds no hits outside the token file (adjust `src/` and the
file name to the project):

```bash
grep -rnE '#[0-9a-fA-F]{3,8}\b|rgba?\(|hsla?\(|oklch\(|radius: *[1-9]|(transition|animation)[^;]*\b[0-9.]+m?s\b|cubic-bezier\(|-\[(#|[0-9])' src/ \
  | grep -v 'tokens.css'
```

(hex strings in data and comments are fine), and the usage page has a
section for every token group.
