<!-- Derived from bama by Dave Ebbelaar (MIT), skills/design/ux-design/presentation.md, upstream commit f0c2cdb. Adapted for web by uxlab. See NOTICE. -->

# Where a feature opens

Rules and markup for each row of the surface table in
[SKILL.md](../SKILL.md#3-pick-the-surface). The markup is plain HTML; the
component library's dialog, popover, and drawer primitives follow the same
rules. Each surface also needs its small-screen form: how layouts change
per breakpoint is in `layout-and-flows/responsive-block-patterns`.

## Contents

- Inline
- Detail side panel
- Popover
- Non-modal drawer
- Modal dialog
- Own page
- Sidebar page or detail
- Confirm dialog
- Alert dialog
- Status instead of a dialog
- Unsaved changes

## Inline

Use for one value on something already on screen. No surface opens, so
nothing needs closing. Save on Enter or when focus leaves the field; Esc
restores the old value.

```html
<input class="row-title" aria-label="Task title" value="Pay rent">
```

## Detail side panel

Use for details of the selection while people keep working in the list.
It stays open across selections and does not block the list. With nothing
selected it says so ("No selection"). A button in the page header toggles
it ("Show details", with a tooltip and shortcut). Its width comes from the
layout tokens; below the tablet breakpoint it becomes a full-screen drawer
or the item's own page.

## Popover

Use for a few related choices tied to one control. It closes when people
click outside, press Esc, or pick an item, and it keeps their changes.
Only an explicit Cancel throws them away. It never warns, never holds a
warning, and opens one at a time. Focus moves into it and returns to its
button. A popover people want to keep open is a non-modal drawer instead.

```html
<button type="button" popovertarget="due-date">Due date</button>
<div id="due-date" popover>
  <label>Due date <input type="date" name="due"></label>
</div>
```

## Non-modal drawer

Use when people give input again and again and watch the result (find and
replace, a filter builder, a style editor), or keep a tool open beside
their work. The page behind stays usable. Its title is a noun ("Filters"),
and its toggle says "Show filters" and "Hide filters", never "drawer" or
"panel".

Prefer sliders, steppers, and selects over typed values in a drawer.

## Modal dialog

Use for one short task that must finish or cancel before going on: a few
fields, one screen, no navigation inside. Buttons sit at the bottom with
the confirm button on the trailing side. Enter submits, Esc cancels.

```html
<dialog id="rename" aria-labelledby="rename-title">
  <form method="dialog">
    <h2 id="rename-title">Rename project</h2>
    <label>Name <input name="name" required></label>
    <footer>
      <button type="button" onclick="this.closest('dialog').close()">Cancel</button>
      <button value="rename">Rename</button> <!-- the only submit button, so Enter renames -->
    </footer>
  </form>
</dialog>
```

- A Done button always comes with Cancel, or with Back in a multi-step
  modal. Never show Cancel, Done, and Back together.
- Open at a width that fits the content (360, 480, or 640 px). On small
  screens it fills the viewport.
- `showModal()` makes the page behind inert; keep its scroll position.
- People repeat the input and watch results? Use a non-modal drawer.

A modal that grows a second screen, a sidebar, or a scroll of settings
wants to be its own page.

## Own page

Use for a long or self-contained task, or something people keep open next
to the main view: an editor, a large preview. It has its own URL, so it
opens in a new tab, survives a reload, and Back returns to where people
came from. The URL holds the state people come back to (the item, the
tab).

## Sidebar page or detail

A place people come back to (Inbox, Today, a project) is a sidebar page.
One item of that list opens in the detail pane, the side panel, or its own
page, not in a modal. Add the page to the navigation and to any list of
pages the project's visual checks visit. Choosing the navigation model:
`layout-and-flows/navigation-pattern-encyclopedia`.

## Confirm dialog

Use only for a rare action that destroys data and cannot be undone. For
undoable actions, act at once and offer Undo in a toast. The title asks
the question, the button repeats the verb, and Cancel sits beside it.

When people chose the action on purpose (Empty trash from a menu), the
confirm button is the default button, so Enter confirms what they asked
for. Keep the danger style for a destructive button people did not ask
for, such as "Discard" when leaving an edited form.

```html
<dialog role="alertdialog" aria-labelledby="empty-title" aria-describedby="empty-msg">
  <form method="dialog">
    <h2 id="empty-title">Empty trash?</h2>
    <p id="empty-msg">You can't undo this action.</p>
    <button value="cancel">Cancel</button>
    <button value="empty" autofocus>Empty trash</button>
  </form>
</dialog>
```

## Alert dialog

Use for a problem people must act on now. The title says what happened.
The message, if any, says what to do.

- Never on page load, never only to inform, and never for a common delete
  that Undo covers.
- The default button sits on the trailing side. Esc cancels. Avoid "OK"
  except for a purely informational alert.
- An alert that repeats for a task people do often gets a "Don't show
  this again" checkbox.
- A warning icon only for a real risk of losing data, never for a routine
  overwrite or Empty trash.

```html
<dialog role="alertdialog" aria-labelledby="export-title" aria-describedby="export-msg">
  <form method="dialog">
    <h2 id="export-title">Unable to export</h2>
    <p id="export-msg">The file is larger than 25 MB. Choose fewer rows and export again.</p>
    <button value="cancel">Cancel</button>
    <button value="choose" autofocus>Choose rows</button>
  </form>
</dialog>
```

## Status instead of a dialog

Information that needs no action goes where it applies. Offline, show the
cached content and a quiet banner.

```html
<p role="status" class="banner">Offline. Changes save when you reconnect.</p>
```

A finished action gets a toast: one line naming what happened, plus Undo
where it applies ("Task deleted. Undo"). It speaks through a live region,
pauses its timer while hovered or focused, and is never the only way to
act. Errors that need a fix stay inline, next to the problem.

## Unsaved changes

Ask before closing or leaving only when people would lose what they typed.
Offer to keep it.

```js
cancel.addEventListener("click", () => {
  if (!form.dirty) dialog.close();
  else confirmDiscard.showModal(); // "Discard this note?" [Discard] [Keep editing]
});
window.addEventListener("beforeunload", (e) => { if (form.dirty) e.preventDefault(); });
```

Client-side routing needs the same check on route change.
