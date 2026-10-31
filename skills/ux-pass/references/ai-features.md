<!-- Derived from bama by Dave Ebbelaar (MIT), skills/design/ux-design/ai-features.md, upstream commit f0c2cdb. Adapted for web by uxlab. See NOTICE. -->

# AI features

Rules for a feature that uses a model: a summary, generated text, a
suggestion, a smart sort. A model is sometimes wrong, so the design plans
for that. Agents, chat, and generative interfaces in depth:
`platforms-and-ai/agentic-ai-generative-ux`.

## Contents

- Say where AI is used
- Keep people in control
- Show progress
- Privacy and models
- When it fails
- Check

## Say where AI is used

- Mark generated content, for example a sparkle icon from the product's
  icon set and the word "Summary". Never pass it off as written by a
  person.
- Say what the feature does in plain words in its first view, not in a
  separate help page.

## Keep people in control

- Edit, Undo, and Retry sit next to every result. Accepting is one click;
  so is throwing it away.
- Show a preview before anything changes. Confirm before an action that
  cannot be undone, and never let a model start a destructive action on
  its own.
- Offer a few alternatives when people are choosing (three titles, not
  one).
- When people correct a result, use the correction and show that you did.
- Optional thumbs up or down for feedback, never a prompt that interrupts.

## Show progress

Say what the model is doing, specifically. Show partial results as they
stream in when the format allows.

| Before | After |
| --- | --- |
| Processing... | Summarizing key themes from 14 notes... |
| Thinking... | Drafting a reply to Anna... |

## Privacy and models

- Prefer a model that keeps personal data under the product's control
  (in the browser or on the product's own servers) when the data is
  personal.
- When data goes to a third-party model provider, say what goes, where,
  and why, before the first use.
- Check that the feature is available (plan, permission, provider status)
  before showing it.
- Ask how the feature could be misused and who it could harm. Drop it when
  the risk is bigger than the value. Ethics review method:
  `ux-evaluation/ux-ethics-content-strategy`.

## When it fails

- The model is unavailable (provider down, rate limited, not in the plan,
  offline): the feature explains why and the product still works without
  it. Every AI action has a manual path.
- A refused or blocked request says so plainly and shows an example of an
  input that works: "Unable to use that description. Try: a short note
  about a meeting."
- A wrong result costs one click to undo, never a person's work.

## Check

Done when generated content is marked, every result has Edit, Undo, and
Retry, progress text names the task, the feature works or explains itself
with the model unavailable, and nothing destructive runs without a
confirmation.
