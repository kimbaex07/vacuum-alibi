#!/usr/bin/env python3
"""The Vacuum's Alibi: One Line, 200 Characters.

Writes the robot vacuum's one-line excuse for missing a spot to
``entry.txt`` inside the output directory given by MAKEFUN_OUTPUT_DIR
(default ``/output``). Pure Python standard library only.

The line is a fixed, hand-written string. The program is deterministic:
every run writes byte-identical output.
"""

import os
import sys

# The excuse, in the vacuum's own deadpan voice. One line, well under
# the 200-character cap, punch at the end.
LINE = (
    "I did not miss that spot. My sensors classified the dust bunny "
    "as a protected species, so I have declared the area under your "
    "sofa a conservation zone."
)


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)

    if not (1 <= len(LINE) <= 200):
        print(f"line is {len(LINE)} characters, must be 1-200", file=sys.stderr)
        return 1
    if not LINE.strip():
        print("line is blank", file=sys.stderr)
        return 1
    if "\n" in LINE:
        print("line must be a single line", file=sys.stderr)
        return 1

    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(LINE + "\n")
    os.chmod(path, 0o644)

    # Read it back and confirm the file on disk is exactly what we meant
    # to write, so a silent write failure can never pass as success.
    with open(path, "r", encoding="utf-8", newline="") as fh:
        written = fh.read()
    if written != LINE + "\n":
        print("written file does not match the line", file=sys.stderr)
        return 1
    print(f"wrote {path} ({len(LINE)} characters)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
