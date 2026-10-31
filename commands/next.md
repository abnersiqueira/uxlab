---
name: next
description: "Context-aware suggestion of what to do next based on what you've generated so far."
argument-hint: "[optional: current focus]"
---
<!-- Derived from Sumi 4.2.0 by Phazur Labs (Apache-2.0), commands/next.md, upstream commit 3a3693b. Modified by uxlab: renamed, cross-references rewritten. See NOTICE. -->

# Next — What Should I Do Now?

A compact navigation aid that suggests the best next command based on context. Not an analysis -- a wayfinding tool. Keep output short and action-oriented.

## Command Reference

The 37 commands organized by tier:

**MAKE** (20): `/uxlab:fix`, `/uxlab:style`, `/uxlab:palette`, `/uxlab:type`, `/uxlab:layout`, `/uxlab:wireframe`, `/uxlab:screen`, `/uxlab:component`, `/uxlab:page`, `/uxlab:tokens`, `/uxlab:form`, `/uxlab:nav`, `/uxlab:animate`, `/uxlab:icon`, `/uxlab:dark`, `/uxlab:responsive`, `/uxlab:onboard`, `/uxlab:generate`, `/uxlab:remix`, `/uxlab:figma`

**REVIEW** (7): `/uxlab:audit`, `/uxlab:roast`, `/uxlab:grade`, `/uxlab:qa`, `/uxlab:a11y`, `/uxlab:before-after`, `/uxlab:ai-audit`

**PLAN** (6): `/uxlab:brief`, `/uxlab:research`, `/uxlab:benchmark`, `/uxlab:map`, `/uxlab:measure`, `/uxlab:preflight`

**Utility** (4): `/uxlab:start`, `/uxlab:help`, `/uxlab:next`, `/uxlab:status`

## Common Progressions

These are typical sequences, not mandatory order:

```
/uxlab:fix → /uxlab:before-after → /uxlab:grade            (slop → cuisine fast track)
/uxlab:style → /uxlab:screen → /uxlab:fix → /uxlab:grade         (build and polish)
/uxlab:brief → /uxlab:style → /uxlab:screen                (fast track)
/uxlab:style → /uxlab:tokens → /uxlab:screen               (system-first)
/uxlab:screen → /uxlab:roast → /uxlab:remix                (iterate loop)
/uxlab:audit → /uxlab:a11y → /uxlab:roast → /uxlab:grade         (full review)
/uxlab:style → /uxlab:screen → /uxlab:qa → /uxlab:preflight      (ship track)
/uxlab:qa project → /uxlab:fix                        (codebase cleanup)
```

## Protocol

### Step 1: Detect Context

- Scan conversation for the most recent uxlab command(s) run
- Identify what outputs exist (style decisions, screens, audits, etc.)
- If no commands have been run, recommend `/uxlab:fix` (if AI code visible) or `/uxlab:style`
- Utility commands (`/uxlab:next`, `/uxlab:status`, `/uxlab:help`) don't count as steps

### Step 2: Recommend Next Command

Based on what exists and what's missing, suggest the highest-value next command.

**Priority logic**:
1. If user just pasted AI-generated code → `/uxlab:fix`
2. If `/uxlab:fix` was just run → `/uxlab:before-after` (show the transformation)
3. If `/uxlab:before-after` was run → `/uxlab:grade` (get the score)
4. If no style direction exists → `/uxlab:style [sector]`
5. If style exists but no screens → `/uxlab:screen [type]`
6. If screens exist but no review → `/uxlab:roast`
7. If review done with issues → `/uxlab:fix` or `/uxlab:remix`
8. If quality is good → `/uxlab:grade` (get the score)
9. If ready to ship → `/uxlab:preflight`
10. If nothing exists and user is exploring → `/uxlab:brief`

### Step 3: Handle Edge Cases

- **Everything looks done**: Suggest `/uxlab:preflight` or celebrate. Recommend `/uxlab:status` for full review.
- **User jumped around**: Note what's missing without judgment. Just mention it as available.
- **No context at all**: Recommend `/uxlab:fix` if AI-generated code is visible, `/uxlab:style [sector]` for builders, or `/uxlab:brief` for planners.

## Output Format

```
## Next Step

You just ran: `/[last-command]` -- [short description of what it produced]

---

### Recommended

> **`/[next-command]`** [optional args]
> [One sentence: what this does and why it follows naturally from what you just did]

---

### Other Options
- `/[option-1]` -- [why you might want this instead]
- `/[option-2]` -- [why you might want this instead]
- `/[option-3]` -- [why you might want this instead]

### Worth Revisiting
[Only if something valuable was skipped]
- `/[skipped]` -- [brief reason it's worth doing]

---
See all commands: `/uxlab:help` | See progress: `/uxlab:status`
```

The output should be compact -- 15-25 lines maximum. Get the user to the next command fast.
