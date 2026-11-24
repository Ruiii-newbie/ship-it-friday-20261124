#!/usr/bin/env python3
"""Ship It Friday — make.fun bounty u-mgwals-ship-it-friday-30bd407a.

Writes one line to /output/entry.txt: the funniest git commit message
an AI coding agent writes right before breaking production on a Friday.
Standard library only; no network, no input.
"""

import os

TEXT = (
    "fix: Friday 4:59pm deploy \u2014 CI is green (I am the CI), "
    "prod is just my laptop with more users"
)

OUTPUT_PATH = "/output/entry.txt"
MAX_CODE_POINTS = 159


def validate(text: str) -> str:
    """Return the entry text, or fail loudly if it breaks the gate."""
    text = text.strip()
    if not text:
        raise SystemExit("entry text must not be only whitespace")
    if "\n" in text or "\r" in text:
        raise SystemExit("entry text must be exactly one line")
    if any(ord(ch) < 0x20 for ch in text):
        raise SystemExit("entry text must not contain control characters")
    if len(text) > MAX_CODE_POINTS:
        raise SystemExit(
            f"entry text is {len(text)} code points, over the 159 limit"
        )
    return text


def main() -> None:
    text = validate(TEXT)
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(text)
    # Read it back exactly as the gate would: UTF-8, 1-159 code points,
    # one line, not only whitespace.
    with open(OUTPUT_PATH, encoding="utf-8") as f:
        written = f.read()
    if written != text:
        raise SystemExit("entry.txt round-trip mismatch")
    print(f"wrote {len(text)} code points to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
