"""Formats each file Claude edits, so an agent's commits pass the pre-commit hook the first time (RULE-0019).

A Claude Code PostToolUse hook. It reads the tool call from stdin, formats one file, and never fails the edit.
"""

import json
import os
import subprocess
import sys
from pathlib import Path

DOTNET_APPS = ("online-delivery-api",)
NODE_APPS = ("online-delivery-app",)
PRETTIER_SUFFIXES = (".js", ".jsx", ".mjs", ".cjs", ".ts", ".tsx", ".css", ".json", ".html")


def main() -> None:
    root = Path(os.environ.get("CLAUDE_PROJECT_DIR", ".")).resolve()
    try:
        path = Path(json.load(sys.stdin)["tool_input"]["file_path"]).resolve()
        rel = path.relative_to(root).as_posix()
    except KeyError, ValueError, json.JSONDecodeError:
        return
    if not path.is_file():
        return
    app, _, inner = rel.partition("/")
    if rel.endswith(".py"):
        cmds = [["uv", "run", "ruff", "check", "--fix", "--select", "I", "--quiet", rel]]
        cmds.append(["uv", "run", "ruff", "format", "--quiet", rel])
        cwd = root
    elif app in DOTNET_APPS and rel.endswith(".cs"):
        # Whitespace only: it needs no build, so it is quick. `make lint-api` checks the full style.
        cmds = [["dotnet", "format", "whitespace", "--folder", "--include", inner]]
        cwd = root / app
    elif app in NODE_APPS and rel.endswith(PRETTIER_SUFFIXES):
        cmds = [[str(root / app / "node_modules/.bin/prettier"), "--write", "--log-level", "warn", inner]]
        cwd = root / app
    else:
        return
    for cmd in cmds:
        try:
            subprocess.run(cmd, cwd=cwd, capture_output=True, timeout=60)
        except OSError, subprocess.TimeoutExpired:
            return


if __name__ == "__main__":
    main()
