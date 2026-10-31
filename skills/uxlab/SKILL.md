---
name: uxlab
description: Start here for UX/UI design work that spans more than one domain (audit, redesign, new product, launch) or when the user asks where to start. Routes to the right uxlab skill and command in order, with stage gates.
---

# uxlab

UX/UI design intelligence for web products: this router, `ux-pass`, and 11 domain skills holding 45 references, plus 38 commands (`/uxlab:start` picks one).

Notation: `domain/name` is the file `references/name.md` of the `uxlab:domain` skill. Sub-files sit in `references/name/`.

## Route by request

| Request | Open |
|---|---|
| Audit, review or critique an existing interface | `ux-evaluation`, then `/uxlab:audit` |
| Design one feature before building it | `ux-pass` |
| Plan research or define UX metrics | `ux-research` |
| Set type, color, spacing, hierarchy | `visual-design` |
| Tokens, components, theming | `design-systems` |
| Compose a page, pick navigation, map flows | `layout-and-flows` |
| Forms, interface text, loading/empty/error states | `forms-and-content` |
| Animation and micro-interaction | `motion` |
| WCAG, ARIA, RTL, localization | `accessibility-i18n` |
| Charts, dashboards, data tables | `data-viz` |
| Mobile, platform-native, AI features | `platforms-and-ai` |
| Real references, sector direction, shared design memory | `references-and-sectors` |

A request that touches several rows follows [orchestrator](references/orchestrator.md): it orders the skills and sets the gate between stages for redesign, launch, audit and new-product runs.
