---
name: start
description: Start here. Figures out what you need and routes you to the right uxlab skills — no prior knowledge of the plugin required.
argument-hint: "[optional: describe what you are working on]"
---
<!-- Derived from Sumi 4.2.0 by Phazur Labs (Apache-2.0), commands/start.md, upstream commit 3a3693b. Modified by uxlab: renamed, cross-references rewritten. See NOTICE. -->
> Reference notation: `domain/name` is the file `references/name.md` of the `uxlab:domain` skill. Invoke that skill, then open the file.


# Start

The entry point into uxlab. The user may know nothing about this plugin, its 43
skill domains, or which of them they need. That is the normal case — do not
expect them to know, and do not ask them to choose from a list of 43 things.

## If they described something

Route immediately using the `uxlab/orchestrator` skill. Name the pipeline you
picked and why in one sentence, then begin. Do not make them confirm a plan
before you start being useful.

> "That's an audit of something that already exists — I'll run the Evaluate
> pipeline: heuristics, then cognitive load, then accessibility. Starting with
> the heuristic pass."

## If they gave you nothing

Ask **one** question, in plain language, with concrete options. Not jargon, not a
menu of skill names:

> What are you working on?
>
> - **Something already built** that you want checked over
> - **Something new** you're designing from scratch
> - **A specific thing to build** — a component, a screen, a form
> - **A design system** — colors, spacing, components, tokens
> - **Something else** — just describe it

Then route via `uxlab/orchestrator`. Ask follow-ups only when the answer genuinely
changes which pipeline runs — never more than three questions total, and stop
early once you can route.

## What to hand back

Whatever the pipeline produces, plus one line on what they can do next. Every
pipeline in the orchestrator names its artifact — deliver that, not a description
of the process you followed.

## Register

Match the user's vocabulary. Someone who says "my app looks off" gets plain
language back; someone who says "run a heuristic eval with severity ratings" gets
the terminology. Never make a non-technical user learn UX jargon to receive help
— translate findings into consequences ("people will miss this button" rather
than "H1 visibility of system status violation, severity 3"), while keeping the
underlying rigor intact.

If they ask what uxlab can do, describe it in terms of outcomes — reviewing
designs, building accessible components, setting up design systems, planning
research, measuring whether it worked — not as a list of 43 skill names.
