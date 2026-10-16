"""Commit message check. Implements RULE-0006. Install with `make hooks`."""

import re
import sys

MAX_SUBJECT = 72
TAG = re.compile(r"^(\[[^\]]+\]\s*|[a-z]+(\([^)]*\))?!?:\s)")
TRAILER = re.compile(r"^co-authored-by:", re.IGNORECASE)


def main(path: str) -> int:
    with open(path, encoding="utf-8") as f:
        lines = [line.rstrip("\n") for line in f if not line.startswith("#")]
    text = [line for line in lines if line.strip()]
    if not text:
        return 0
    subject = text[0]
    if subject.startswith(("Merge ", "Revert ", "fixup! ", "squash! ", "amend! ")):
        return 0

    errors = []
    if len(subject) > MAX_SUBJECT:
        errors.append(f"subject is {len(subject)} characters; keep it under {MAX_SUBJECT}")
    if subject.endswith("."):
        errors.append("subject ends with a full stop")
    if TAG.match(subject):
        errors.append("subject starts with a prefix tag")
    if any(TRAILER.match(line.strip()) for line in lines):
        errors.append("message carries a Co-authored-by trailer")

    for e in errors:
        print(f"commit-msg: {e} (RULE-0006)", file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
