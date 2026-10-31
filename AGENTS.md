# uxlab

Claude Code plugin: UX/UI design skills, commands and agents for web products. Apache-2.0, derived from Sumi and bama (see `NOTICE`).

## Layout

- `skills/<domain>/SKILL.md`: a small router. Frontmatter description carries the trigger branches; the body is a table that points at reference files.
- `skills/<domain>/references/<name>.md`: the depth. `references/<name>/` holds that reference's sub-files.
- `skills/ux-pass/`: the feature-level UX workflow (ported from bama).
- `commands/`, `agents/`: slash commands (`/uxlab:<name>`) and subagents.
- `scripts/`: `awwwards.mjs` (node, fetch only); `capture.sh` + `capture.py` (browser-harness).
- `tools/`: re-sync scripts for the Sumi-derived files.

## Rules

- `domain/name` notation means `skills/<domain>/references/<name>.md`. Use it for cross-references; do not link across domains with raw paths.
- A new reference file needs a row in its domain `SKILL.md` and the plugin entry stays in `.claude-plugin/plugin.json`. A new skill needs both `plugin.json` `skills` and the `uxlab` router table.
- Every file derived from Sumi or bama keeps its provenance header comment. Edit derived files freely; update `NOTICE` when the kind of change is new.
- Sumi's trademark policy forbids the names "Sumi" and "Phazur" in this product. Mention them only as attribution in `NOTICE`, `README.md` and header comments.
- Browser work goes through browser-harness. Do not add Playwright or Puppeteer.
- Run `claude plugin validate . --strict` after touching `.claude-plugin/` or any frontmatter.

## Re-syncing from Sumi

`tools/sync-sumi.py <sumi-clone> .` regenerates the reference files, commands and agents from a Sumi checkout, then `tools/gen-capture.py <sumi-clone> .` rebuilds `scripts/capture.py`. Hand-written files (every `SKILL.md`, `ux-pass`, the bama ports, README, NOTICE) are never overwritten. Review `git diff` after a sync.
