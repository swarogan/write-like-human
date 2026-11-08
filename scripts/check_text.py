#!/usr/bin/env python3
"""Flag characters you can't type on a standard US keyboard and common AI-writing phrases.

Usage:
    python3 check_text.py FILE [FILE ...]      check files
    python3 check_text.py -                    check stdin
    python3 check_text.py --fix FILE           also replace characters that have a safe 1:1 swap
    python3 check_text.py --strict FILE        exit 1 on phrase warnings too

Exit code: 0 clean, 1 problems found (character errors, or any warning with --strict).
Standard library only.
"""

import argparse
import re
import sys
import unicodedata

# Characters with an unambiguous keyboard replacement. --fix applies these.
SAFE_FIXES = {
    "‘": "'", "’": "'", "‚": "'", "‛": "'", "′": "'",
    "“": '"', "”": '"', "„": '"', "‟": '"', "″": '"',
    "«": '"', "»": '"',
    "…": "...",
    " ": " ", " ": " ", " ": " ", " ": " ", " ": " ",
    " ": " ", " ": " ", "　": " ",
    "​": "", "‌": "", "‍": "", "⁠": "", "﻿": "", "­": "",
    "•": "-", "·": "-", "●": "-", "▪": "-",
    "→": "->", "←": "<-", "⇒": "=>", "↔": "<->",
    "×": "x", "−": "-", "‑": "-", "‐": "-",
    "≤": "<=", "≥": ">=", "≠": "!=", "≈": "~",
}

# Dashes need a rewrite, not a swap: a mechanical "-" just hides the AI rhythm.
REWRITE_HINTS = {
    "—": "em dash: rewrite with a period, comma, colon or parentheses",
    "–": "en dash: use '-' in ranges (2019-2024), otherwise rewrite the sentence",
    "―": "horizontal bar: rewrite the sentence",
}

# (regex, message). Case-insensitive. Word boundaries matter: keep \b.
PHRASES = [
    (r"\bdelv(e|es|ed|ing)\b", "stock AI verb 'delve'"),
    (r"\btapestr(y|ies)\b", "stock AI noun 'tapestry'"),
    (r"\btestament to\b", "'a testament to'"),
    (r"\b(leverag(e|es|ed|ing)|utiliz(e|es|ed|ing))\b", "use 'use'"),
    (r"\bseamless(ly)?\b", "'seamless': say what actually works"),
    (r"\brobust\b", "'robust': say what it survives"),
    (r"\b(multifaceted|myriad|plethora)\b", "inflated quantity word"),
    (r"\b(foster(s|ed|ing)?|underscor(e|es|ed|ing))\b", "stock AI verb"),
    (r"\b(pivotal|paramount|crucial)\b", "inflated importance word"),
    (r"\bintricate\b", "'intricate'"),
    (r"\bembark(s|ed|ing)? on\b", "'embark on'"),
    (r"\bnavigat(e|es|ed|ing) (the|these|this) (complexit|challeng|landscape|world)", "'navigate the complexities'"),
    (r"\b(elevat|unlock|unleash|harness|empower)(e|es|ed|ing|s)?\b", "marketing verb"),
    (r"\bgame[- ]changer\b", "'game-changer'"),
    (r"\bcutting[- ]edge\b", "'cutting-edge'"),
    (r"\bever[- ](evolving|changing)\b", "'ever-evolving'"),
    (r"\b(vibrant|bustling|nestled)\b", "travel-brochure adjective"),
    (r"\bmeticulous(ly)?\b", "'meticulous'"),
    (r"\bholistic\b", "'holistic'"),
    (r"\bsynerg(y|ies)\b", "'synergy'"),
    (r"\bin today'?s (fast[- ]paced|digital|ever|modern|rapidly)", "'In today's fast-paced world' opener"),
    (r"\bit'?s not (just|only|merely|simply|about) [^.!?\n]{1,60}?[,;]\s*it'?s\b", "'it's not X, it's Y' contrast"),
    (r"\bnot (just|only|merely) [^.!?\n]{1,50}?,? but (also )?", "'not just X but Y' contrast"),
    (r"\b(let'?s )?dive (in|into)\b", "'dive in'"),
    (r"\b(in conclusion|in summary|to sum up|all in all)\b", "summary signpost"),
    (r"\bit'?s (worth|important to) (noting|note|mention)", "'it's worth noting'"),
    (r"\bit is (worth|important to) (noting|note|mention)", "'it is important to note'"),
    (r"\bat the end of the day\b", "'at the end of the day'"),
    (r"\bhere'?s the (thing|kicker|catch|truth)\b", "staged reveal"),
    (r"\bthe (best|real|good) (part|news)\?", "staged reveal question"),
    (r"\bwhether you'?re an? [^.!?\n]{1,40}? or\b", "'whether you're a X or a Y'"),
    (r"\bhope this (email|message|note) finds you well\b", "stock email opener"),
    (r"\b(feel free to|don'?t hesitate to)\b", "stock email closer"),
    (r"\bbuckle up\b", "'buckle up'"),
    (r"\b(stands|serves) as an?\b", "'serves as a' (just say 'is')"),
    (r"\bplays? an? (crucial|pivotal|vital|key|important) role\b", "'plays a key role'"),
    (r"\b(great|excellent|fantastic) question\b", "sycophantic opener"),
    (r"(^|\n)\s*(moreover|furthermore|additionally|ultimately|notably|importantly),", "transition-word opener"),
    (r"\bembrace the\b", "'embrace the'"),
    (r"\bjourney\b", "'journey' (for anything that isn't travel)"),
    (r"\b(landscape|realm)\b", "'landscape/realm' used figuratively?"),
    (r"\bhere(?:'s| is) (why|how|what)\b[^.!?\n]{0,15}[.:]", "staged reveal ('Here's why.')"),
    (r"\b(excited|thrilled|delighted|proud) to (share|announce|introduce)\b", "launch-post opener"),
    (r"\bmy (view|take|answer|point) is simple\b", "announcing an opinion instead of stating it"),
    (r"\b(i'?d|i would) love to hear\b", "engagement-bait closer"),
    (r"\bwhat do you think\?", "engagement-bait closer"),
    (r"\bgenuinely\b", "'genuinely' (filler intensifier)"),
    (r"\bnone of this means\b", "pre-emptive concession"),
    (r"\bthe best (compliment|thing) i can (give|say)\b", "mic-drop closer"),
    (r"\blet me be (clear|honest)\b", "announcing honesty"),
    (r"\b(the result|the catch|the problem|the answer|the twist)\?", "staged reveal question"),
    (r"^\s*[-*]?\s*\*\*[^*\n]{1,40}[.:]\*\*", "bold lead-in label on a paragraph"),
    (r"(#\w+\s*){3,}$", "hashtag pile"),
]
PHRASE_RES = [(re.compile(p, re.IGNORECASE), m) for p, m in PHRASES]
INLINE_CODE = re.compile(r"`[^`]*`")


def describe(ch):
    try:
        return unicodedata.name(ch)
    except ValueError:
        return "U+%04X" % ord(ch)


def is_keyboard(ch):
    return ch in "\n\t\r" or 0x20 <= ord(ch) <= 0x7E


def check(text, label):
    """Return (errors, warnings) as lists of 'label:line:col: message' strings."""
    errors, warnings = [], []
    in_fence = False
    for lineno, line in enumerate(text.splitlines(), 1):
        if line.lstrip().startswith(("```", "~~~")):
            in_fence = not in_fence
            continue
        is_code = in_fence or line.startswith(("    ", "\t"))
        if not is_code:
            # Semicolons in prose: AI uses them far more than people do. Code is exempt.
            prose = INLINE_CODE.sub(lambda m: " " * len(m.group(0)), line)
            for m in re.finditer(";", prose):
                warnings.append("%s:%d:%d: semicolon: split into two sentences, or join with a comma and 'and/but/so'" % (label, lineno, m.start() + 1))
        for col, ch in enumerate(line, 1):
            if is_keyboard(ch):
                continue
            where = "%s:%d:%d" % (label, lineno, col)
            name = describe(ch)
            if ch in REWRITE_HINTS:
                errors.append("%s: %r %s" % (where, ch, REWRITE_HINTS[ch]))
            elif ch in SAFE_FIXES:
                rep = SAFE_FIXES[ch]
                errors.append("%s: %s -> %r (auto-fixable)" % (where, name, rep))
            elif unicodedata.category(ch)[0] in "LM":
                # Accented letters in names (Zoë, São Paulo) are a judgment call.
                warnings.append("%s: non-ASCII letter %r (%s): fine in a proper name, otherwise use ASCII" % (where, ch, name))
            else:
                errors.append("%s: %r %s: not on a keyboard, rewrite without it" % (where, ch, name))
        # Normalize curly quotes first so "it’s not" still matches "it's not".
        plain = apply_fixes(line)
        for rx, msg in ([] if is_code else PHRASE_RES):
            for m in rx.finditer(plain):
                warnings.append("%s:%d:%d: %s: %r" % (label, lineno, m.start() + 1, msg, m.group(0).strip()))
    return errors, warnings


def apply_fixes(text):
    return "".join(SAFE_FIXES.get(ch, ch) for ch in text)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="+", help="files to check, or - for stdin")
    ap.add_argument("--fix", action="store_true", help="rewrite files in place with safe 1:1 character swaps")
    ap.add_argument("--strict", action="store_true", help="exit 1 on phrase warnings too")
    ap.add_argument("--quiet", action="store_true", help="print only the summary line")
    args = ap.parse_args(argv)

    total_err = total_warn = 0
    for path in args.files:
        if path == "-":
            text, label = sys.stdin.read(), "<stdin>"
        else:
            with open(path, encoding="utf-8") as f:
                text, label = f.read(), path
        if args.fix and path != "-":
            fixed = apply_fixes(text)
            if fixed != text:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(fixed)
                text = fixed
        errors, warnings = check(text, label)
        if not args.quiet:
            for e in errors:
                print("ERROR " + e)
            for w in warnings:
                print("WARN  " + w)
        total_err += len(errors)
        total_warn += len(warnings)

    print("%d character error(s), %d phrase warning(s)" % (total_err, total_warn))
    failed = total_err > 0 or (args.strict and total_warn > 0)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
