---
name: ux-pass
description: UX pass for one feature of a web product: names, flow, surface (inline, popover, drawer, modal, page, toast), states, words, tooltips, accessibility and AI features. Use before building a screen, an action or text, to review a built screen, for naming and wording questions, or when someone asks "should this be a modal?".
argument-hint: "[feature, story or screen]"
---
<!-- Derived from bama by Dave Ebbelaar (MIT), skills/design/ux-design, upstream commit f0c2cdb. Adapted for web by uxlab. See NOTICE. -->

# UX pass

A feature that works can still confuse people. This pass decides what
things are called, how a person moves through the feature, where it opens,
and what it says, before any code exists.

Run it once per feature that adds a screen, an action, or words. The output
is a `UX:` block in the ticket, spec, or PR description the user points to,
plus new terms in the project's glossary file. To review a built screen, run
the same steps against the running page or its screenshots and list what
fails, most serious first. For a heuristic sweep on top, see
`ux-evaluation/nng-ux-heuristics`.

## 0. Read

Read whichever of `BRIEF.md`, `PRODUCT.md`, `DESIGN.md`, `GLOSSARY.md`, and
`CONTEXT.md` exist, the ticket or spec, and its reference screenshots. When
a fact the pass needs is in none of them (who the feature is for, what the
product calls its things), ask the user once.

Check: you know who the feature is for and where the `UX:` block goes.

## 1. Name it

Every thing in the product has exactly one name, and every name lives in the
glossary. With no glossary file in the project, put the table in the `UX:`
block under `Terms`.

```markdown
| Term | Means | Not |
| --- | --- | --- |
| Task | One thing to do, with an optional due date | to-do, item, entry |
| Complete | Mark a task done; it leaves the list | check, finish, close |
```

- Name the things first (the nouns in the brief), then the actions on them.
- Use the user's words, not the code's: "Task", not "TaskEntity" or "record".
- Use the web's standard words for standard actions: Settings, Sign out,
  Cancel, Undo, Archive or Move to trash (when it can come back), Delete
  (when it cannot).
- One word per idea across buttons, menus, titles, tooltips, and errors.
- Name a feature for what it does for the person, not the technology. A
  toggle gets a verb phrase that says what and for whom ("Enhance
  dialogue", not "Isolate vocals"). Say the name in a sentence out loud.
  Method: [writing.md](references/writing.md#names).

Check: every noun and verb the feature puts on screen is in the glossary,
and no glossary term has a second name anywhere.

## 2. Map the flow

Write the flow as one line, from every way in to a clear end.

```text
"New task" in the page header, shortcut N, command palette "New task" -> title field has focus -> Enter saves, row appears -> focus stays for the next task
```

- List every entry point: header or top bar button, sidebar link, keyboard
  shortcut, command palette, row menu, drag and drop, a direct URL.
- Cut steps: fill in good defaults, ask only for what you cannot guess
  (the reasoning behind this: `ux-evaluation/cognitive-psychology-ux`).
- Every step has a way back: Esc cancels, Undo reverts, the browser Back
  button returns to the previous view.
- The end is visible: the new row, a checkmark, the modal closing, a toast.

Check: the flow fits on one line, and each step names its way back.

## 3. Pick the surface

Go down this list and use the first one that fits. Lighter is better.

| The feature | Use |
| --- | --- |
| Changes one value on something already on screen | Inline (editable field, toggle, select in the row) |
| Shows details of the selection while people keep working | Detail side panel |
| A few related choices tied to one control | Popover |
| Input people repeat while they watch the result, or a tool kept open beside the work | Non-modal drawer |
| One short task that must finish or cancel before going on | Modal dialog |
| A long or self-contained task, or one people keep open beside the main view | Its own page, with its own URL |
| A place people come back to, like a list or a collection | Sidebar page |
| A rare action that destroys data and cannot be undone | Confirm dialog |
| A problem people must act on right now | Alert dialog |

- Show one modal at a time. Never open a popover from a popover, or a
  modal from a modal.
- A modal's title names its task: "Rename project", not "Edit".
- Enter confirms, Esc cancels, and the confirm button names the action.
- Ask before closing or navigating away only when people would lose what
  they typed.
- Information that needs no action goes inline or in a toast, never in a
  dialog.

Details and markup for each surface: [presentation.md](references/presentation.md).

Check: the `UX:` block names the surface and the table row that picked it.

## 4. Cover the states

Every view the feature touches has words and a look for each state:

- **Empty**: what it is for, plus the first action as a button.
- **Loading**: only when it can take longer than half a second. Show
  cached content or a skeleton first. A bar when the length is known, with
  words for what is happening ("Importing 12 contacts"), and Cancel when
  it is safe.
- **Error**: inline, next to the problem, with the fix.
- **Too much**: long names truncate with the full text in a tooltip; a
  thousand rows still scroll smoothly (paginate or virtualize).
- **Done**: visible feedback in the same view, and Undo where it applies.

State patterns in depth: `forms-and-content/performance-states-patterns`.

Check: each state has a fixture, seed data, a component story, or a URL
that shows it.

## 5. Write the words

- Buttons and menu items start with a verb: "Add task", "Export…".
- Add an ellipsis when the command asks for more input before it acts.
- Pick one case for buttons, menu items, and page titles, and keep it
  everywhere: sentence case is the web norm; keep title case only when the
  product already uses it. Sentence case for labels, descriptions, and
  messages.
- Errors say what happened and how to fix it, without blame. Write
  "Unable to load tasks", never "We're having trouble".
- Confirmations repeat the action: "Delete 3 tasks?" with buttons "Delete"
  and "Cancel", never "Yes" and "No".

Patterns and before and after examples: [writing.md](references/writing.md).
Microcopy by component: `forms-and-content/micro-copy-intelligence`.

A feature that uses AI (a summary, generated text, a model's suggestion)
also follows [ai-features.md](references/ai-features.md).

Check: read every string aloud. Each one is short, uses glossary terms
only, and a new user could say what each button does.

## 6. Add tooltips and hints

- Every icon-only button gets an accessible name and a tooltip: what it
  does, starting with a verb, then its shortcut ("Add a task to this list
  (N)"). Not its name again. Rules: [writing.md](references/writing.md#tooltips).
- A tooltip opens on hover and on keyboard focus, closes on Esc, and stays
  open while the pointer is over it.
- Touch has no hover. Anything people need from a tooltip is also visible
  as helper text under the field, or one tap away behind an info button.
- Hover can reveal secondary actions on a row. The same actions are also
  in the row menu, appear on keyboard focus, and stay visible on touch
  screens.
- Hover feedback shows at once and never shifts the layout.
- Information people need is always visible. Hover only adds detail.

Check: hover and Tab to every icon-only control on the running page. Each
one shows a tooltip both ways, and on a touch viewport the same
information is reachable without hover.

## 7. Check accessibility

- The whole flow works with the keyboard alone, in a logical focus order,
  with a visible focus ring.
- A screen reader reads every control with the same words as the screen.
- Meaning never rests on color alone: add an icon or a word.
- Body text is 14 to 16 px, nothing is under 12 px, and the page still
  works at 200% zoom and in forced colors (high contrast) mode.
- With reduced motion requested, slides and bounces become fades.
- Every custom control has a role, a name, a value, keyboard actions, and
  feedback.

The audit steps and the markup that fixes what they find:
[accessibility.md](references/accessibility.md).

Check: you ran the flow keyboard-only and with a screen reader, and the
browser's accessibility audit shows no issues for the new views.

## 8. Write the UX block

Add the result to the ticket, spec, or PR description, under its
acceptance criteria:

```markdown
UX:
- Flow: "New task" in the header, shortcut N -> title field -> Enter saves -> focus stays
- Surface: inline row at the top of the list (changes one value on screen)
- States: empty "No tasks yet" with "Add task"; error "Give the task a title." under the field
- Words: "Add task", tooltip "Add a task to this list (N)", toast "Task added" with "Undo"
- Access: Enter saves, Esc cancels; screen reader reads "New task title"
```

Done when the ticket has a `UX:` block, every term it uses is in the
glossary, and steps 1 to 7 pass on the running build or its screenshots.
