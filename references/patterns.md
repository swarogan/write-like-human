# AI writing patterns

Each entry: what it looks like, then a rewrite. These are signals, not proof. Humans use some of them on purpose. The problem is density and predictability. If a draft has three or more of these, rewrite it, don't patch it.

## Structure

### 1. Bold lead-in labels
Every paragraph opens with a bolded summary.

> **Sound.** The stock sound is a deep, muted thock.

Rewrite: put the topic into the sentence. "Out of the box it sounds deep and muted."

### 2. Staged reveals
A setup line announces that a point is coming: "Here's why.", "The catch?", "The result?", "Here's the thing:".

> Start with integration tests. Here is why.

Rewrite: give the reason. "Start with integration tests, because they survive refactors."

### 3. Not-X-but-Y framing
Defining something by what it isn't, often as a headline: "It's not just a tool, it's a workflow." "Remote work isn't the problem. Bad onboarding is."

Rewrite: state the claim directly. "Bad onboarding hurts remote juniors more than remote work does."

### 4. Mic-drop paragraph endings
A short, aphoristic last line on paragraph after paragraph: "At home, it shows." "The rest can wait." "That's the point."

Rewrite: end on the last piece of information. Keep at most one punchy line per piece, and only if it earns it.

### 5. Reflexive triplets
Lists of three everywhere: three adjectives, three examples, three parallel clauses. "Fast, simple, and reliable."

Rewrite: use the number of items you actually have. Two is fine. Four is fine.

### 6. Symmetric conditional endings
"If they do, X. If they don't, Y." "Teams that A will thrive. Teams that don't will struggle."

Rewrite: say what you think will happen, once.

### 7. Pre-emptive concessions
"None of this means unit tests are worthless." "There is truth in this, but..." placed to look balanced.

Rewrite: if the exception matters, state it as a fact where it applies. Otherwise cut it.

### 8. Announcing instead of saying
"My view is simple.", "Let me be clear.", "Let's break it down.", "It's worth noting that".

Rewrite: delete the announcement and keep what follows.

### 9. Summary endings
A final paragraph that restates the piece, often opening with "In short", "Ultimately" or "In conclusion".

Rewrite: delete it. If something important is only in the summary, move it up.

### 10. Engagement bait
"I'd love to hear your thoughts!", "What do you think?", a pile of hashtags, "Stars and PRs welcome!".

Rewrite: end with something concrete (a link, a date, a next step), or just end.

### 11. Ritual openers
"Excited to share...", "In today's fast-paced world...", "I hope this email finds you well.", "Great question!".

Rewrite: start with the news. "We released branchsweep, a CLI that deletes merged git branches."

### 12. Formatting as decoration
Headers, bullets and bold on a 200-word text. Emoji used as bullets. A table for two facts.

Rewrite: prose. Formatting is for documents people scan, not for messages people read.

### 13. Semicolons
Models join clauses with semicolons far more often than people do, especially in casual text: "The build is fast; the tests are not." Hardly anyone types a semicolon in an email or a post.

Rewrite: two sentences, or a comma with "and", "but", "so". In code, semicolons are fine. The script skips fenced and inline code.

## Vocabulary

Stock words show up because they are safe, not because they fit. Most common: delve, tapestry, testament, leverage, utilize, seamless, robust, multifaceted, myriad, plethora, foster, underscore, pivotal, crucial, paramount, intricate, embark, navigate (complexities), elevate, unlock, unleash, harness, empower, game-changer, cutting-edge, ever-evolving, vibrant, bustling, nestled, meticulous, holistic, synergy, genuinely, journey, landscape, realm.

Rewrite: the plainest word that is true. Often the sentence gets shorter. `scripts/check_text.py` flags these.

Word lists go stale with every model release. Structure is the more reliable signal, so fix structure first.

## Characters

Typed text uses only keyboard characters. A text with em dashes, curly quotes, the single-character ellipsis, non-breaking spaces, arrow symbols or emoji was usually not typed by a person. See the table in SKILL.md. The script catches all of them.

## Not tells

Leave these alone. People write them all the time:

- Contractions, and occasional sentence fragments.
- A real list of steps or options.
- A hyphen in a range or compound word (2019-2024, self-hosted).
- A colon before a list or an explanation.
- Formal tone in a formal email. Formal is not the same as AI.
- One strong closing line in a whole piece.
