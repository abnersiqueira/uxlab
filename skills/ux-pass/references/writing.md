<!-- Derived from bama by Dave Ebbelaar (MIT), skills/design/ux-design/writing.md, upstream commit f0c2cdb. Adapted for web by uxlab. See NOTICE. -->

# Writing patterns

Patterns for the words in a web product. Each one has a rule and a before
and after. Examples use sentence case; keep title case only when the
product already uses it.

## Contents

- Voice
- Names
- Buttons and menu items
- Titles
- Empty states
- Errors
- Dialogs
- Confirmations
- Undo
- Settings
- Fields and placeholders
- Permissions
- Progress
- Tooltips
- Counts and plurals
- Words to cut

## Voice

Pick three words for the product's voice and keep them in the glossary
file under `## Voice` (or in `DESIGN.md`), for example "calm, direct,
brief". Tone changes with the moment: plain and serious for errors, a
little warmer for a finished goal.

- Talk to people as "you". Never "the user".
- Use verbs that fit mouse, touch, and keyboard: "select", "choose",
  "open". Avoid "click" and "tap".
- No idioms or jokes that do not translate. Explain a technical term the
  first time, or drop it.

## Names

A good name fits the product's other words, sets the right expectation,
and works in every language and market.

- Name a feature by what it does for the person, not by the technology:
  "Enhance dialogue", not "Isolate vocals" or "Voice separation".
- A toggle gets a verb phrase that answers "what" and "for whom".
- Avoid clever names that raise questions. A label must not sound like a
  judgment when its value is low or zero ("Spending power: $0").
- Where trust matters (money, health, privacy), use the industry word
  ("Balance", not "Current funds").
- Reuse words already in the product. A new name for an old idea is a bug.
- Test each name in sentences: "Turn on Enhance dialogue", "Search for
  it in Recent". If the sentence sounds odd, the name is wrong.

To find a name: write who it is for, then three lists of words, what the
feature makes people think, feel, and do. Group them into themes, cut what
fails the rules above, and try the rest in sentences.

## Buttons and menu items

Start with a verb. Name the object when the verb alone is unclear.

| Before | After |
| --- | --- |
| OK | Save |
| Let's go! | Create project |
| New | New task |
| Export | Export… (it opens a dialog first) |
| Click here to learn more | Learn about smart lists |

- One case on every button and menu item.
- An ellipsis means "asks for more before it acts". Leave it off commands
  that act at once.
- Multi-step flows start with "Get started", move with "Continue", and end
  with "Done". Keep the same words in every flow.
- A link names its destination, never "here" or "this".

## Titles

Page titles name the content, not the product. The browser tab title
starts with the same words, with the product name last. Modal titles name
the task.

| Before | After |
| --- | --- |
| Taskly | Today (tab: "Today · Taskly") |
| Edit | Rename project |
| Settings page | Settings |

## Empty states

Say what the page is for and give the first action as a button.

| Before | After |
| --- | --- |
| Nothing here. | No tasks yet. Tasks you add appear here. [Add task] |
| Your inbox is empty! 🎉 | All done. New tasks land here first. |

Keep critical information out of empty states. They disappear.

## Errors

Say what happened and how to fix it, next to the problem, without blame.

| Before | After |
| --- | --- |
| Oops! Something went wrong. | Unable to save the task. Check your connection and try again. |
| Invalid name. | Use letters and numbers only. |
| Password too short. | Choose a password with at least 8 characters. |
| Error 401 | Your session ended. Sign in again. |
| We're having trouble loading this. | Unable to load tasks. |

Say what to do, not what is forbidden: "Use only letters for your name",
not "Numbers are not allowed".

When the same error keeps happening to many people, change the design, not
the message.

## Dialogs

- A title that is a full sentence ends with a period. A fragment has no
  period: "Unable to export". A question ends with a question mark:
  "Delete 3 tasks?"
- At most two lines. Never "Error", "Warning", or an error code as the title.
- The message never explains the buttons. The buttons name the action.

## Confirmations

Ask only for rare actions that cannot be undone. The title is a question
with the verb. The button repeats the verb.

| Before | After |
| --- | --- |
| Are you sure? [Yes] [No] | Delete 3 tasks? [Delete] [Cancel] |
| Warning! This cannot be undone. [OK] | Empty trash? You can't undo this action. [Empty trash] [Cancel] |

## Undo

Name every undoable action, so the toast and any history read "Task
completed. [Undo]" and the Undo button's accessible name is "Undo complete
task", not just "Undo".

## Settings

Label the setting by what it does. Describe the on state only; people
infer the off state. Link to a setting instead of describing where it is.

| Before | After |
| --- | --- |
| Enable notifications for tasks that are due if the app is not open | Notify me when a task is due |
| Sync | Keep tasks the same on all my devices |

## Fields and placeholders

Every field has a visible label. The placeholder shows an example or the
format, never the only label. Labels, validation, and field layout in
depth: `forms-and-content/form-design-encyclopedia`.

| Before | After |
| --- | --- |
| (placeholder only) Email | Label "Email", placeholder "name@example.com" |
| Enter date | Label "Due date", placeholder "DD/MM/YYYY" |

## Permissions

Ask for a browser permission (notifications, camera, microphone,
location) at the moment of first use, never on page load, unless the
product cannot work at all without it.

Before the browser prompt, show one short view that explains how and why
in one complete sentence, in the active voice, ending with a period. It
has one button, "Continue", which fires the browser prompt. No Cancel, no
Allow: the browser prompt is where people decide.

| Before | After |
| --- | --- |
| This app needs access to improve your experience | Get a notification when someone assigns you a task. |
| Microphone access required | Recordings use the microphone to capture your voice. |

A site cannot ask again after people block a permission. Show the reason
in the product's own settings row, with short steps to allow it in the
browser's site settings.

## Progress

Say what is happening, with a count when there is one.

| Before | After |
| --- | --- |
| Loading... | Importing 12 contacts... |
| Processing | Summarizing your notes... |
| Please wait | Exporting "Q3 report"... |

## Tooltips

These rules cover tooltips on controls. An information tooltip (the full
text of a truncated value, a chart value, why a control is disabled) just
shows that information.

Say what the control does, starting with a verb, then add its shortcut in
parentheses, with the modifier for the person's OS: "(N)", "(⌘K)" or
"(Ctrl+K)". Do not repeat the control's name: the tooltip adds what the
name does not say. Sentence case, no period, at most 60 to 75 characters.
Skip tooltips on buttons whose text label already says it all.

| Before | After |
| --- | --- |
| (none) | Add a task to this list (N) |
| New task (N) | Add a task to this list (N) |
| Click this button to create a new task in the current list | Add a task to this list (N) |

## Counts and plurals

Use plural rules from the i18n library (ICU message format), so counts
read right in every language. Never build a plural by adding "s".

```text
{count, plural, one {# task left} other {# tasks left}}
```

## Words to cut

- "we", "our": unclear who that is. "Unable to sync", not "We couldn't sync".
- "Oops", "Uh-oh", "Whoops": sound insincere in an error.
- "Simply", "just", "easily": they blame people who find it hard.
- "Please": once in a while is fine, every message is noise.
- "Your", "my": "Favorites" already means yours.
- Code words: entity, record, payload, null, undefined, NaN, token, 404.
