---
name: write-like-human
description: Use when writing or editing English prose that a person will read or publish as their own - blog posts, emails, READMEs, social posts, reviews, essays, cover letters, announcements, docs. Also use when the user says text sounds like AI, ChatGPT or "slop", or complains about em dashes, curly quotes or characters they can't type on a keyboard.
---

# Write Like a Human

## Overview

AI text is recognizable by two things: characters a person would never type, and a predictable shape (staged reveals, bold labels, punchy closers, tidy triplets). Swapping words fixes neither. This skill gives you a writing recipe, a pattern catalog, and a script that checks characters and stock phrases.

## Rule 1: Keyboard characters only

Every character must be one you can type on a standard US keyboard: printable ASCII, newlines and tabs.

| Instead of | Write |
|---|---|
| em dash, en dash | a period, comma, colon or parentheses. `-` only in ranges (2019-2024) |
| curly quotes and apostrophes | `"` and `'` |
| ellipsis character | three periods `...`, and use it rarely |
| non-breaking or thin space, zero-width chars | a normal space, or nothing |
| bullet dots, arrows, multiplication sign | `-`, `->` or words, `x` |
| emoji, check marks, stars | nothing |

Leave text untouched where it is not yours to change: code, commands, quotations, and accented letters in names the user wrote that way (Zoe vs Zoë: follow the user).

## Rule 2: The recipe

1. **Know who is speaking.** Write as the person the text belongs to: their knowledge, their opinions, first person where natural. Specifics make text human: numbers, names, what actually happened. Never invent experiences, facts or quotes to sound authentic. If a detail is missing, leave it out, ask, or put a `[placeholder]` the user will fill in. Invented details are fine only when the user asked for fiction or a sample text.
2. **Open with the point.** The first sentence carries information, not a setup or a greeting ritual.
3. **Write paragraphs.** Use a list only for content that is a list (steps, options someone will scan). No bold label at the start of a paragraph. Messages (emails, posts, replies) get no headers. Documents like READMEs keep the structure readers expect, with prose inside each section.
4. **Let content set the rhythm.** Long sentences where the thought is long, short where it is short. Not every paragraph needs three sentences or a quotable last line. Join clauses with a period or a plain conjunction (and, but, so), not a semicolon. People almost never type semicolons outside code.
5. **Stop when you are done.** The last sentence is the last useful thing. No summary, moral, mic-drop line or "let me know what you think".
6. **Plain words.** "use", "is", "helps", "important". If a word sounds like a brochure, replace it.

## Rule 3: Check before you deliver

1. Save the draft to a file and run, from this skill's directory:
   `python3 scripts/check_text.py path/to/draft.md`
   Fix every `ERROR`. `--fix` swaps quotes, ellipses and spaces for you. Dashes need a rewritten sentence.
2. For every `WARN`, rewrite unless the word is the plain, correct one in context ("journey" about an actual trip).
3. Read the draft once against [references/patterns.md](references/patterns.md). The script cannot see structure, and structure is where most AI tells live.

No way to run scripts? Search the text yourself for the characters in the Rule 1 table, then do step 3.

## Common mistakes

| Mistake | Why it fails |
|---|---|
| Replacing every em dash with ` - ` | Same rhythm, different glyph. Rewrite the sentence. |
| Swapping "delve" for "dig into" | The structure around it is still the tell. |
| Overcorrecting into flat, choppy fragments | People write long sentences too. Uniform shortness is its own tell. |
| Adding a fake anecdote "to sound human" | Invented facts are worse than slop. |
| Applying this to code, logs or quoted material | Those must stay exact. |
