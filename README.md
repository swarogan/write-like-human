# write-like-human

A Claude skill that makes Claude write English prose the way a person would type it.

It enforces keyboard-only characters: no em dashes, curly quotes, ellipsis characters, non-breaking spaces, arrows or emoji. If you can't type it on a US keyboard, it doesn't go in the text.

It also carries a catalog of the structural habits that give AI text away, each with a rewrite: bold lead-in labels, staged reveals, not-X-but-Y framing, mic-drop endings, reflexive triplets, pre-emptive concessions, engagement bait, and semicolons in casual prose.

Finally, `scripts/check_text.py` flags every non-keyboard character with its line and column, fixes the ones with a safe 1:1 swap, and warns about stock phrases. It needs only the Python 3 standard library.

Most anti-slop skills ban the em dash and stop there. This one treats the whole character set as a hard rule and checks it with a script instead of trusting the model to notice.

## Before and after

Same prompt ("a ~250-word review of a mechanical keyboard you used for a month"), same model, without and with the skill.

Without:

```
**Build.** The aluminum case is heavy and doesn't flex at all. ...
**Sound.** After lubing nothing and changing nothing, the stock sound is a deep, muted thock. ...
**Verdict.** ... I'm keeping it, and I've stopped browsing for replacements, which is the best compliment I can give.
```

With:

```
I used the Keychron Q1 with brown switches as my only keyboard for a month, at the office and
at home, and I would buy it again. It is heavy, around 1.6 kg, so it stays on my desk and has
never once slid when I type fast.
...
At around 190 dollars it is not cheap, but nothing broke or rattled in a month of daily use.
```

In the baseline run, six texts produced 17 checker warnings. With the skill, the same six prompts produced none, and the structural tells were gone too: no bold labels, no staged "Here is why", no aphoristic closers.

## Install

Claude Code, as a personal skill:

```
git clone https://github.com/swarogan/write-like-human ~/.claude/skills/write-like-human
```

Claude Code, as a plugin:

```
/plugin marketplace add swarogan/write-like-human
/plugin install write-like-human@write-like-human
```

Claude.ai: zip the folder and upload it under Settings > Capabilities > Skills.

The skill triggers on its own when Claude writes emails, posts, READMEs, essays and similar text. You can also ask for it by name.

## Using the checker by itself

```
python3 scripts/check_text.py draft.md            # report problems
python3 scripts/check_text.py --fix draft.md      # also swap quotes, ellipses, odd spaces in place
python3 scripts/check_text.py --strict draft.md   # exit 1 on phrase warnings too
cat draft.md | python3 scripts/check_text.py -    # read from stdin
```

Exit code 0 means no character errors. Dashes are reported but never auto-fixed, because turning an em dash into a hyphen keeps the same rhythm. The sentence needs rewriting.

Code is left alone: semicolons inside fenced blocks, indented blocks and inline code don't count.

## Layout

```
SKILL.md                  rules and workflow (what Claude reads first)
references/patterns.md    pattern catalog with rewrites
scripts/check_text.py     character and phrase checker
tests/                    unit tests for the checker
.claude-plugin/           plugin and marketplace manifests
```

Run the tests with `python3 -m unittest discover -s tests`.

## Scope

English only. The character rule works for any language, but the phrase list and patterns are English. Phrase warnings are signals, not proof: people use stock words too. The skill asks Claude to rewrite them unless the word is the plain, correct one.

## Credits

The pattern catalog draws on Wikipedia's "Signs of AI writing" page and on earlier skills, especially [blader/humanizer](https://github.com/blader/humanizer), [hardikpandya/stop-slop](https://github.com/hardikpandya/stop-slop) and [conorbronsdon/avoid-ai-writing](https://github.com/conorbronsdon/avoid-ai-writing).

## License

MIT
