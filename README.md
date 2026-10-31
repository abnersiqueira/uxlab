# uxlab

UX/UI design intelligence for Claude Code, built for web products and SaaS: Nielsen heuristics, cognitive psychology, accessibility, design systems, data visualization, UX writing, motion, and design grounded in real references.

13 skills, 38 commands, 4 agents. Only 13 short skill descriptions load into context; the 246 reference files open on demand.

```
/plugin marketplace add abnersiqueira/uxlab
/plugin install uxlab@uxlab
/uxlab:start
```

`/uxlab:start` asks what you are working on and picks the play. You do not need to learn the skill names.

## Skills

| Skill | Use it to |
|---|---|
| `uxlab` | Route a request that spans several domains; order the work with stage gates |
| `ux-pass` | Run a UX pass on one feature: names, flow, where it opens, states, words, help, accessibility, AI |
| `ux-evaluation` | Audit with Nielsen's heuristics, Laws of UX, dark-pattern checks, critique, AI-slop detection |
| `ux-research` | Plan studies, define metrics, frame the design process |
| `visual-design` | Type, color, spacing, hierarchy, elevation, icons, imagery, visual-quality scoring |
| `design-systems` | Tokens, theming, component code with every state, Figma-to-code |
| `layout-and-flows` | Sections, whole pages, responsive behavior, navigation, screen inventory, grid |
| `forms-and-content` | Forms, microcopy, loading/empty/error states, conversion friction |
| `motion` | Timing, easing, micro-interactions, animation recipes |
| `accessibility-i18n` | WCAG 2.2, ARIA, RTL and localization |
| `data-viz` | Charts, dashboards, data tables |
| `platforms-and-ai` | Mobile, platform standards, AI and agent interfaces |
| `references-and-sectors` | Real references with measured design DNA, sector direction, shared design memory |

Each domain skill is a small router. Its table points at reference files (`references/<name>.md`) that hold the depth. Inside the plugin, `domain/name` means `skills/<domain>/references/<name>.md`.

## Commands

| Group | Commands |
|---|---|
| Start | `start`, `help`, `next`, `status` |
| Audit | `audit`, `roast`, `grade`, `a11y`, `ai-audit`, `qa`, `benchmark` |
| Build | `style`, `tokens`, `palette`, `type`, `dark`, `icon`, `layout`, `responsive`, `nav`, `page`, `screen`, `component`, `form`, `onboard`, `animate`, `wireframe`, `figma`, `generate` |
| Fix | `fix`, `remix`, `before-after` |
| Plan | `brief`, `research`, `map`, `measure`, `preflight` |
| References | `inspo` |

Invoke as `/uxlab:<command>`.

## Agents

`scout` sources real references, `art-director` turns them into a Reference Board, `ux-architect` designs flows from shipped apps, `critic` grades a build against the board.

## Design memory

Commands share decisions through `.uxlab/` in your project (`style.json`, `brief.json`, `refs/`). The contract is in `skills/references-and-sectors/references/design-memory.md`. Add `.uxlab/refs/**/*.jpg` to `.gitignore`: captured third-party screenshots are study material.

## Reference capture

`/uxlab:inspo` captures live sites (desktop and phone screenshots plus measured type, color, spacing, grid and motion stack) with `scripts/capture.sh`, which runs through [browser-harness](https://github.com/browser-use/browser-harness). Install browser-harness first. Third-party sites load in the browser it is attached to, and the capture tab comes to the front while it runs.

To keep third-party sites out of a signed-in profile, or when macOS blocks browser-harness from reading Chrome's `DevToolsActivePort` ("Operation not permitted"), capture through a throwaway Chrome:

```sh
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new \
  --remote-debugging-port=9333 --user-data-dir="$HOME/.cache/uxlab-chrome" about:blank &
BU_NAME=uxlab BU_CDP_URL=http://127.0.0.1:9333 scripts/capture.sh https://example.com --out .uxlab/refs
```

## Provenance and license

Apache-2.0. uxlab combines and modifies [Sumi](https://github.com/phazurlabs/sumi) (Apache-2.0, Phazur Labs) and parts of [bama](https://github.com/daveebbelaar/bama) (MIT, Dave Ebbelaar). See `NOTICE` for what changed. uxlab is not affiliated with either project.
