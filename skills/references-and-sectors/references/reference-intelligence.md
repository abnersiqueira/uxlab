<!-- Derived from Sumi 4.2.0 by Phazur Labs (Apache-2.0), skills/reference-intelligence/SKILL.md, upstream commit 3a3693b. Modified by uxlab: consolidated into a domain skill, renamed, cross-references rewritten. See NOTICE. -->
# Reference Intelligence — look before you design

Every other uxlab skill encodes taste from memory. This one goes and **looks**. A
senior studio doesn't design a fintech landing page from recollection; it pulls
ten current winners onto a wall, pulls them apart, agrees what to steal, builds,
then pins the build next to the wall and asks whether it belongs there.

That loop has four steps and uxlab owns all of them:

| Step | What happens | Where it lives |
|------|--------------|----------------|
| **Scout** | Find 8-12 candidates from real sources | `scripts/awwwards.mjs`, Mobbin MCP, MotionSites MCP |
| **Capture** | Screenshot the LIVE sites and measure their DNA | `scripts/capture.sh` → `.uxlab/refs/<slug>/` |
| **Board** | Synthesize what to steal / avoid into one direction | `.uxlab/refs/board.md` + `board.json` |
| **Compare** | Grade a build side by side with the board | `critic` agent, `/uxlab:grade`, `/uxlab:roast` |

## Source routing

| The ask is… | Primary source | Secondary |
|-------------|----------------|-----------|
| Marketing site, landing page, portfolio, brand, campaign | **Awwwards** | MotionSites for motion recipes |
| App screen, dashboard, settings, product UI | **Mobbin** | Awwwards `app-style` / `ui-design` tags |
| A flow (onboarding, checkout, signup, paywall, search) | **Mobbin** (flows) | — |
| Motion, scroll storytelling, WebGL, transitions | **Awwwards** (`gsap`, `three-js`, `webgl`, `transitions`, `scrolling`) | **MotionSites** |
| "Make it look like <url>" | That URL, straight into `capture.sh` | Awwwards category of that site |

Adapters, one per source:
- `reference-intelligence/awwwards-adapter.md` — listings, the 192 category tags, sector → tag map, etiquette
- `reference-intelligence/mobbin-adapter.md` — MCP auth, query shapes, what may be stored
- `reference-intelligence/motionsites-adapter.md` — prompt library, free-tier limit, upgrade message rule
- `reference-intelligence/dna-schema.md` — what `capture.sh` measures and how to read it
- `reference-intelligence/board-synthesis.md` — combining references without cloning one; `board.json` schema
- `reference-intelligence/comparison-protocol.md` — how the critic grades a build against the board

## Non-negotiables

1. **Real, not recalled.** A reference must be a URL that was fetched this session (or a cached
   fetch under `.uxlab/refs/`), a Mobbin result from the MCP, or a MotionSites prompt. Never
   present a site as an Awwwards winner from memory.
2. **Capture the live site, not the thumbnail.** Awwwards and Mobbin are indexes. The DNA comes
   from the site itself.
3. **One script call, not click-by-click browsing.** Capture runs as ONE `scripts/capture.sh`
   invocation over all picks. Never drive the browser step by step to study a site.
4. **Small and on-demand.** 8-12 candidates per run, 3-5 kept. No bulk crawling of Awwwards;
   reuse a cached listing under `.uxlab/refs/` if it is under 7 days old.
5. **Steal traits, never layouts.** The board takes at most ONE signature trait from each
   reference (see `board-synthesis.md`). A build that is recognisably one reference is a fail.
6. **Screenshots stay local.** Third-party captures are study material. Suggest adding
   `.uxlab/refs/**/*.jpg` to `.gitignore`; never publish or deploy them.
7. **The user curates.** Present the shortlist and let them keep 3-5. Art direction is a choice,
   not a computation.

## Running the scripts

Scripts live in the plugin, not the project. Resolve the plugin root once:

```bash
UXLAB="${CLAUDE_PLUGIN_ROOT:-$(dirname "$(dirname "$(find ~/.claude/plugins -path '*uxlab*/scripts/capture.sh' -print -quit)")")}"
node "$UXLAB/scripts/awwwards.mjs" technology --awarded --limit 10 --out .uxlab/refs/awwwards-technology.json
"$UXLAB/scripts/capture.sh" --from .uxlab/refs/awwwards-technology.json --pick slug-a,slug-b,slug-c
"$UXLAB/scripts/capture.sh" https://linear.app https://stripe.com   # direct URLs
```

`capture.sh` drives the browser through `browser-harness` (load that skill for setup). Third-party
sites load in the browser it is attached to; set `BU_NAME` or `BU_CDP_URL` to use an isolated one. It takes ~40-60s per site (desktop + phone, scroll steps).
Run it in the background for more than 3 sites.

## Output: `.uxlab/refs/`

```
.uxlab/refs/
├── awwwards-<listing>.json   # scout results (cache)
├── mobbin.json               # Mobbin picks: app, screen/flow, url, why
├── motion.json               # MotionSites prompts used
├── <slug>/dna.json           # measured DNA, desktop + phone
├── <slug>/desktop-0..3.jpg   # scroll-step captures
├── <slug>/phone-0..2.jpg
├── board.md                  # human-readable Reference Board
└── board.json                # machine-readable direction every command consumes
```

`board.json` is the contract. `/uxlab:style` turns its `direction` into tokens and its references
into the `references` array of `.uxlab/style.json` (per `references-and-sectors/design-memory`, only `/uxlab:style` writes
that file). `/uxlab:page`, `/uxlab:screen` and `/uxlab:component` build against it; `/uxlab:grade` and `/uxlab:roast`
compare against it.

## Related skills
- `visual-design/visual-design-mastery` — the 10-dimension scoring the comparison uses
- `layout-and-flows/screen-flow-patterns` — the screen/flow taxonomy used to phrase Mobbin queries
- `references-and-sectors/sector-style-intelligence` — sector norms; its "Inspiration Links" seed Mobbin queries
- `motion/interaction-motion-design`, `motion/animation-recipe-library` — translating captured motion stacks into code
