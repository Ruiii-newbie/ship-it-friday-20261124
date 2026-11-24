#!/usr/bin/env python3
"""Ship It Friday — emit the one-line commit message.

The message is assembled from fragments so the punchline lands in
order, then written to the entry file the gate reads.
"""

import os
import sys


FRAGMENTS = (
    "fix: Friday 4:59pm deploy",
    "— CI is green (I am the CI),",
    "prod is just my laptop with more users",
)

MAX_CHARS = 159


def build_message(parts):
    """Join fragments into the single commit-message line."""
    words = []
    for part in parts:
        words.extend(part.split())
    return " ".join(words)


def validate(text):
    # The gate reads one UTF-8 line, 1-159 chars; strip any stray
    # whitespace the fragments may have introduced at the edges.
    text = text.strip()
    if not 1 <= len(text) <= MAX_CHARS:
        raise ValueError("entry must be 1-%d chars, got %d" % (MAX_CHARS, len(text)))
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    return text


def entry_path(argv):
    if len(argv) > 1:
        return argv[1]
    return os.environ.get("ENTRY_OUT", "/output/entry.txt")


def main(argv):
    text = validate(build_message(FRAGMENTS))
    out = entry_path(argv)
    parent = os.path.dirname(out)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(out, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
