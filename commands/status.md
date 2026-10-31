---
name: status
description: "Progress dashboard — see what you've generated, what's available, and suggested next moves."
argument-hint: "[optional: project path]"
---
<!-- Derived from Sumi 4.2.0 by Phazur Labs (Apache-2.0), commands/status.md, upstream commit 3a3693b. Modified by uxlab: renamed, cross-references rewritten. See NOTICE. -->

# Status — Progress Dashboard

A visual progress tracker showing what uxlab commands have been run in this session. Clean, scannable, motivating.

## Command Registry

All 37 commands organized by tier:

**MAKE (20 commands)**:
`/uxlab:fix`, `/uxlab:style`, `/uxlab:palette`, `/uxlab:type`, `/uxlab:layout`, `/uxlab:wireframe`, `/uxlab:screen`, `/uxlab:component`, `/uxlab:page`, `/uxlab:tokens`, `/uxlab:form`, `/uxlab:nav`, `/uxlab:animate`, `/uxlab:icon`, `/uxlab:dark`, `/uxlab:responsive`, `/uxlab:onboard`, `/uxlab:generate`, `/uxlab:remix`, `/uxlab:figma`

**REVIEW (7 commands)**:
`/uxlab:audit`, `/uxlab:roast`, `/uxlab:grade`, `/uxlab:qa`, `/uxlab:a11y`, `/uxlab:before-after`, `/uxlab:ai-audit`

**PLAN (6 commands)**:
`/uxlab:brief`, `/uxlab:research`, `/uxlab:benchmark`, `/uxlab:map`, `/uxlab:measure`, `/uxlab:preflight`

**Utility (4 commands)**:
`/uxlab:start`, `/uxlab:help`, `/uxlab:next`, `/uxlab:status`

## Protocol

### Step 1: Detect Completed Commands

- Scan conversation context for which uxlab commands have been run
- Mark each as complete or not run
- Calculate per-tier and overall completion
- Identify the recommended next command

### Step 2: Display Dashboard

Render the progress map with completion status.

### Step 3: Adapt

- Checkmarks for completed, empty boxes for not run
- Bold or highlight the recommended next command
- Show tier completion as progress indicators
- If commands were run out of typical order, show them as complete without judgment
- If nothing has been run, show the full map with encouragement to begin

## Output Format

```
## uxlab Progress

### MAKE — Design and Build
  [ ] /uxlab:fix           Anti-slop transformation
  [ ] /uxlab:style         Visual identity
  [ ] /uxlab:palette       Color system
  [ ] /uxlab:type          Typography system
  [ ] /uxlab:layout        Layout patterns
  [ ] /uxlab:wireframe     Low-fidelity wireframes
  [ ] /uxlab:screen        Production screens
  [ ] /uxlab:component     Production components
  [ ] /uxlab:page          Full page compositions
  [ ] /uxlab:tokens        Design token system
  [ ] /uxlab:form          Form design
  [ ] /uxlab:nav           Navigation system
  [ ] /uxlab:animate       Motion design
  [ ] /uxlab:icon          Icon system
  [ ] /uxlab:dark          Dark mode
  [ ] /uxlab:responsive    Responsive design
  [ ] /uxlab:onboard       Onboarding flow
  [ ] /uxlab:generate      AI generation
  [ ] /uxlab:remix         Evidence-based redesign
  MAKE: 0/19

### REVIEW — Evaluate and Improve
  [ ] /uxlab:audit         Full design audit
  [ ] /uxlab:roast         Quick critique + slop detection
  [ ] /uxlab:grade         Design Quality Score (0-100)
  [ ] /uxlab:qa            Design QA + codebase consistency
  [ ] /uxlab:a11y          Accessibility audit + auto-fix
  [ ] /uxlab:before-after  Transformation comparison
  REVIEW: 0/6

### PLAN — Research and Strategy
  [ ] /uxlab:brief         Problem definition
  [ ] /uxlab:research      User research & testing
  [ ] /uxlab:benchmark     Competitive analysis
  [ ] /uxlab:map           Information architecture
  [ ] /uxlab:measure       Metrics plan
  [ ] /uxlab:preflight     Launch readiness
  PLAN: 0/6

──────────────────────────────────────
Overall: 0/37 commands  |  Next → /uxlab:style
──────────────────────────────────────

Run /uxlab:next for guidance  |  /uxlab:help for full map
```

### Adaptation Rules

- **NEXT marker**: Place `<-- NEXT` on the recommended next command (use priority logic from `/uxlab:next` protocol: `/uxlab:fix` first if slop detected, then `/uxlab:style` for new projects, then uncompleted commands in tier order)
- **`/uxlab:fix` completed**: Show checkmark with slop score note, e.g. `[x] /uxlab:fix  Anti-slop transformation  (slop: 7→2)`
- **`/uxlab:grade` completed**: Show DQS score next to checkmark, e.g. `[x] /uxlab:grade  Design Quality Score  (DQS: 74/100)`
- **`/uxlab:before-after` completed**: Show grade change, e.g. `[x] /uxlab:before-after  Transformation comparison  (42→78 DQS)`
- **All commands run**: Replace footer with congratulatory message
- **No commands run**: Show full empty map with: "Ready to start? Try `/uxlab:style [your sector]` or `/uxlab:fix` to clean up existing UI."
- **Partial completion**: Show counts per tier and overall

The output should fit on one screen. No commentary beyond the dashboard -- the visual format communicates progress clearly.
