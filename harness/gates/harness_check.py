#!/usr/bin/env python3
"""Harness gate: validates the markdown context tree.

Zero dependencies. Subcommands:
  check     run every gate (exit 1 on failure)
  registry  regenerate context/registry.yaml
  index     regenerate context/INDEX.md
  id        print the next free ID for a type
  new       scaffold an artefact and log it
  linkfix   turn bare artefact references into links
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONTEXT = ROOT / "context"
REGISTRY = CONTEXT / "registry.yaml"
INDEX = CONTEXT / "INDEX.md"

# type -> (directory, required frontmatter keys)
TYPES = {
    "ADR": ("context/adr", ("id", "title", "type", "status")),
    "BPM": ("context/bpm", ("id", "title", "type", "domain", "status", "actors", "triggers")),
    "US": ("context/stories", ("id", "title", "type", "domain", "status", "bpm", "actor")),
    "SPEC": ("context/specs", ("id", "title", "type", "domain", "status", "bpm")),
    "NFR": ("context/nfr", ("id", "title", "type", "domain", "status", "budget", "enforced_by")),
    "RULE": ("harness/rules", ("id", "title", "type", "status", "scope")),
    "SKILL": ("harness/skills", ("id", "title", "type", "status")),
    "PROC": ("harness/proc", ("id", "title", "type", "status")),
    "EVAL": ("evals", ("id", "title", "type", "domain", "status", "metric", "threshold")),
}
STATUSES = ("draft", "review", "accepted", "implemented", "superseded")
ID_RE = re.compile(r"\b(ADR|BPM|US|SPEC|NFR|RULE|SKILL|PROC|EVAL)-(\d{4})\b")
AC_RE = re.compile(r"\bAC-(\d{4})-(\d{2})\b")
INLINE_CODE_RE = re.compile(r"`[^`]*`")
AGENTS_MAX_LINES = 120
# Never walked: vcs data, dependencies and build output of the .NET and React apps.
SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__", "bin", "obj", "dist"}

errors: list[str] = []
warnings: list[str] = []


def fail(where: str, msg: str) -> None:
    errors.append(f"{where}: {msg}")


def warn(where: str, msg: str) -> None:
    warnings.append(f"{where}: {msg}")


# --- minimal frontmatter parser (the subset this repo uses) -----------------


def parse_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, text
    raw, body = text[4:end], text[end + 5 :]
    data: dict = {}
    key = None
    for line in raw.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith("  - ") and key:
            data.setdefault(key, [])
            if isinstance(data[key], list):
                data[key].append(line[4:].strip().strip("'\""))
            continue
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        key, value = key.strip(), value.strip()
        if value.startswith("[") and value.endswith("]"):
            inner = value[1:-1].strip()
            data[key] = [v.strip().strip("'\"") for v in inner.split(",") if v.strip()]
        elif value == "":
            data[key] = []
        else:
            data[key] = value.strip("'\"")
    return data, body


def load_artifacts() -> dict[str, dict]:
    found: dict[str, dict] = {}
    for kind, (rel, _required) in TYPES.items():
        directory = ROOT / rel
        if not directory.is_dir():
            continue
        for path in sorted(directory.rglob("*.md")):
            if path.name in ("AGENTS.md", "CHANGELOG.md", "README.md"):
                continue
            if not path.name.startswith(kind + "-"):
                fail(path.relative_to(ROOT).as_posix(), f"filename must start with {kind}-NNNN-")
                continue
            text = path.read_text(encoding="utf-8")
            meta, body = parse_frontmatter(text)
            rec = {"kind": kind, "path": path, "meta": meta, "body": body, "text": text}
            aid = meta.get("id", "")
            if not aid:
                fail(path.relative_to(ROOT).as_posix(), "missing frontmatter id")
                continue
            if not path.name.startswith(aid + "-"):
                fail(path.relative_to(ROOT).as_posix(), f"filename does not match id {aid}")
            if aid in found:
                fail(aid, f"duplicate id in {path.name} and {found[aid]['path'].name}")
            found[aid] = rec
    return found


# --- gates ------------------------------------------------------------------


def gate_frontmatter(arts: dict) -> None:
    for rec in arts.values():
        where, meta = rec["path"].relative_to(ROOT).as_posix(), rec["meta"]
        for key in TYPES[rec["kind"]][1]:
            if not meta.get(key):
                fail(where, f"missing frontmatter '{key}'")
        if meta.get("status") not in STATUSES:
            fail(where, f"status '{meta.get('status')}' not one of {'|'.join(STATUSES)}")
        if meta.get("type", "").upper() != rec["kind"]:
            fail(where, f"type '{meta.get('type')}' does not match {rec['kind']}")


def gate_links(arts: dict) -> None:
    """Every reference must resolve. Frontmatter and prose are checked; an id inside a
    fenced block or inline code is illustrating something, not pointing at it, so it is not."""
    for rec in arts.values():
        where = rec["path"].relative_to(ROOT).as_posix()
        scanned = [(0, str(v)) for v in rec["meta"].values()]
        scanned += [(i, INLINE_CODE_RE.sub(" ", line)) for i, line in walk_prose(rec["text"])]
        for _i, line in scanned:
            for match in ID_RE.finditer(line):
                ref = match.group(0)
                if ref not in arts:
                    fail(where, f"reference {ref} does not resolve")
            for match in AC_RE.finditer(line):
                parent = "US-" + match.group(1)
                if parent not in arts:
                    fail(where, f"{match.group(0)} has no story {parent}")


def parse_acs(rec: dict) -> list[tuple[str, str]]:
    """Return (ac_id, verified_by) from the story's acceptance-criteria table."""
    out = []
    for line in rec["body"].splitlines():
        stripped = line.strip()
        if not stripped.startswith("| `AC-"):
            continue
        cells = [c.strip().strip("`") for c in stripped.strip("|").split("|")]
        if len(cells) >= 2:
            out.append((cells[0], cells[-1]))
    return out


def gate_coverage(arts: dict) -> None:
    for aid, rec in arts.items():
        where = rec["path"].relative_to(ROOT).as_posix()
        if rec["kind"] == "US":
            acs = parse_acs(rec)
            if not acs:
                fail(where, "story has no acceptance-criteria table")
            expected = "AC-" + aid.split("-")[1] + "-"
            for ac_id, verified in acs:
                if not ac_id.startswith(expected):
                    fail(where, f"{ac_id} does not belong to {aid}")
                if not verified or verified in ("", "-", "TODO"):
                    fail(where, f"{ac_id} has no verified_by binding")
        if rec["kind"] == "BPM" and rec["meta"].get("status") in ("accepted", "implemented"):
            if not rec["meta"].get("stories"):
                warn(where, "accepted BPM has no stories yet")


def gate_status(arts: dict) -> None:
    for rec in arts.values():
        where = rec["path"].relative_to(ROOT).as_posix()
        if rec["meta"].get("status") == "superseded" and not rec["meta"].get("superseded_by"):
            fail(where, "superseded artefact must name superseded_by")
        if rec["meta"].get("status") in ("accepted", "implemented"):
            for ref in rec["meta"].get("constrained_by", []) or []:
                target = arts.get(ref)
                if target and target["meta"].get("status") == "superseded":
                    fail(where, f"links superseded {ref}")


def gate_agents_and_changelogs() -> None:
    skip = SKIP_DIRS
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in skip]
        if "AGENTS.md" not in filenames:
            continue
        d = Path(dirpath)
        where = (d.relative_to(ROOT) / "AGENTS.md").as_posix()
        lines = (d / "AGENTS.md").read_text(encoding="utf-8").splitlines()
        if len(lines) > AGENTS_MAX_LINES:
            fail(where, f"{len(lines)} lines exceeds the {AGENTS_MAX_LINES}-line budget")
        if "CHANGELOG.md" not in filenames:
            fail((d.relative_to(ROOT)).as_posix() or ".", "directory has AGENTS.md but no CHANGELOG.md")


def gate_names() -> None:
    listfile = ROOT / "harness/gates/banned_names.local.txt"
    names = []
    if listfile.exists():
        names += [n.strip() for n in listfile.read_text().splitlines() if n.strip() and not n.startswith("#")]
    names += [n.strip() for n in os.environ.get("HARNESS_BANNED_NAMES", "").split(",") if n.strip()]
    if not names:
        warn("gate:names", "no banned-name list configured (RULE-0001 unenforced locally)")
        return
    for path in ROOT.rglob("*.md"):
        if SKIP_DIRS & set(path.parts):
            continue
        low = path.read_text(encoding="utf-8", errors="ignore").lower()
        for name in names:
            if name.lower() in low:
                fail(path.relative_to(ROOT).as_posix(), "contains a banned name (RULE-0001)")


# --- artefact references must be links (RULE-0015) ---------------------------

PROTECT_RE = re.compile(r"\[[^\]]*\]\([^)]*\)|`[^`]*`")
BARE_REF_EXEMPT = ("CHANGELOG.md",)  # RULE-0015: changelogs may name ids plainly
GENERATED_MD = ("INDEX.md",)  # regenerated, never hand-checked
LINK_RE = re.compile(r"\[((?:ADR|BPM|US|SPEC|NFR|RULE|SKILL|PROC|EVAL)-\d{4})\]\(([^)]+)\)")


def id_map(arts: dict) -> dict[str, str]:
    return {aid: rec["path"].relative_to(ROOT).as_posix() for aid, rec in arts.items()}


def markdown_files() -> list[Path]:
    skip = SKIP_DIRS
    out = []
    for path in ROOT.rglob("*.md"):
        if skip & set(path.parts) or path.name in GENERATED_MD:
            continue
        out.append(path)
    return out


def walk_prose(text: str):
    """Yield (index, line) for lines outside frontmatter and fenced code blocks."""
    lines = text.split("\n")
    in_fm = lines and lines[0].strip() == "---"
    in_fence = False
    for i, line in enumerate(lines):
        if in_fm:
            if i > 0 and line.strip() == "---":
                in_fm = False
            continue
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        yield i, line


def self_id_of(path: Path) -> str:
    m = re.match(r"^([A-Z]+-\d{4})-", path.name)
    return m.group(1) if m else ""


def link_line(line: str, self_id: str, cur_dir: str, ids: dict[str, str]) -> str:
    held: list[str] = []

    def mask(m):
        held.append(m.group(0))
        return f"\x00{len(held) - 1}\x00"

    masked = PROTECT_RE.sub(mask, line)

    def sub(m):
        ref = m.group(0)
        if ref == self_id or ref not in ids:
            return ref
        return f"[{ref}]({os.path.relpath(ids[ref], cur_dir)})"

    masked = ID_RE.sub(sub, masked)
    return re.sub(r"\x00(\d+)\x00", lambda m: held[int(m.group(1))], masked)


def bare_refs(line: str, self_id: str) -> list[str]:
    masked = PROTECT_RE.sub(lambda m: " ", line)
    return [m.group(0) for m in ID_RE.finditer(masked) if m.group(0) != self_id]


def gate_linkstyle(arts: dict) -> None:
    ids = id_map(arts)
    for path in markdown_files():
        where = path.relative_to(ROOT).as_posix()
        self_id = self_id_of(path)
        for i, line in walk_prose(path.read_text(encoding="utf-8")):
            for ref in () if path.name in BARE_REF_EXEMPT else bare_refs(line, self_id):
                if ref in ids:
                    fail(f"{where}:{i + 1}", f"{ref} must be a link (RULE-0015) — run `make linkfix`")
                else:
                    fail(f"{where}:{i + 1}", f"reference {ref} does not resolve")
            for ref, target in LINK_RE.findall(line):
                if ref not in ids:
                    fail(f"{where}:{i + 1}", f"link text {ref} does not resolve")
                elif not (path.parent / target).resolve().is_file():
                    fail(f"{where}:{i + 1}", f"{ref} links to a path that does not exist: {target}")


def linkfix(arts: dict) -> int:
    ids = id_map(arts)
    changed = 0
    for path in markdown_files():
        text = path.read_text(encoding="utf-8")
        lines = text.split("\n")
        self_id = self_id_of(path)
        cur_dir = path.parent.relative_to(ROOT).as_posix() or "."
        touched = False
        for i, line in walk_prose(text):
            new = link_line(line, self_id, cur_dir, ids)
            if new != line:
                lines[i] = new
                touched = True
        if touched:
            path.write_text("\n".join(lines), encoding="utf-8")
            changed += 1
    print(f"linked references in {changed} files")
    return 0


# --- changelog format (RULE-0016) -------------------------------------------

CL_DATE_RE = re.compile(r"^## (\d{4})-(\d{2})-(\d{2})\s*$")
CL_GROUPS = ("Added", "Changed", "Superseded", "Removed", "Fixed")


def gate_changelog_format() -> None:
    skip = SKIP_DIRS
    for path in ROOT.rglob("CHANGELOG.md"):
        if skip & set(path.parts):
            continue
        where = path.relative_to(ROOT).as_posix()
        previous = None
        seen_date = False
        groups_here: set[str] = set()
        for i, line in enumerate(path.read_text(encoding="utf-8").split("\n"), 1):
            if line.startswith("## "):
                m = CL_DATE_RE.match(line)
                if not m:
                    fail(f"{where}:{i}", "entry heading must be `## YYYY-MM-DD` (RULE-0016)")
                    continue
                current = m.groups()
                if previous and current >= previous:
                    fail(
                        f"{where}:{i}",
                        f"{'-'.join(current)} is not older than the entry above "
                        f"it — changelogs run newest first (RULE-0016)",
                    )
                previous = current
                seen_date = True
                groups_here = set()
            elif line.startswith("### "):
                group = line[4:].strip()
                if group not in CL_GROUPS:
                    fail(f"{where}:{i}", f"'{group}' is not one of {', '.join(CL_GROUPS)} (RULE-0016)")
                if not seen_date:
                    fail(f"{where}:{i}", "a group heading must follow a dated entry (RULE-0016)")
                elif group in groups_here:
                    fail(
                        f"{where}:{i}",
                        f"'{group}' appears twice under the same date — merge them into one group (RULE-0016)",
                    )
                else:
                    groups_here.add(group)


# --- changelog coverage (RULE-0016) -----------------------------------------

# Which log records a change to each tree. A directory not listed here has no log.
CHANGELOG_FOR = {
    "context/adr": "context/adr/CHANGELOG.md",
    "context/bpm": "context/CHANGELOG.md",
    "context/stories": "context/CHANGELOG.md",
    "context/specs": "context/CHANGELOG.md",
    "context/nfr": "context/CHANGELOG.md",
    "harness/rules": "harness/CHANGELOG.md",
    "harness/skills": "harness/CHANGELOG.md",
    "harness/proc": "harness/CHANGELOG.md",
    "evals": "evals/CHANGELOG.md",
}
# `ADR-0001..ADR-0022`, with or without the link syntax around each end.
CL_RANGE_RE = re.compile(r"\b([A-Z]+)-(\d{4})\b(?:\]\([^)]*\))?\.\.(?:\[)?\1-(\d{4})\b")


def changelog_ids(path: Path) -> set[str]:
    """Ids a log names, expanding `X-0001..X-0022` to every id it covers."""
    if not path.exists():
        return set()
    text = path.read_text(encoding="utf-8")
    found = set(ID_RE.findall(text))
    found = {f"{kind}-{num}" for kind, num in found}
    for kind, start, end in CL_RANGE_RE.findall(text):
        for n in range(int(start), int(end) + 1):
            found.add(f"{kind}-{n:04d}")
    return found


def gate_changelog_coverage(arts: dict) -> None:
    """An artefact nobody wrote down is an artefact nobody can find again."""
    cache: dict[str, set[str]] = {}
    for aid, rec in arts.items():
        rel = rec["path"].relative_to(ROOT).parent.as_posix()
        log = CHANGELOG_FOR.get(rel)
        if not log:
            continue
        if log not in cache:
            cache[log] = changelog_ids(ROOT / log)
        if aid not in cache[log]:
            fail(
                rec["path"].relative_to(ROOT).as_posix(),
                f"never named in {log} — add an entry in the same commit (RULE-0016)",
            )


def gate_todo(arts: dict) -> None:
    """Scaffolding may carry TODO. Anything past `draft` may not."""
    for rec in arts.values():
        if rec["meta"].get("status") == "draft":
            continue
        for i, line in walk_prose(rec["text"]):
            if TODO in line:
                fail(
                    f"{rec['path'].relative_to(ROOT).as_posix()}:{i}",
                    f"{TODO} left in a '{rec['meta'].get('status')}' artefact — fill it in or set status back to draft",
                )
                break
        for key, val in rec["meta"].items():
            if isinstance(val, str) and TODO in val:
                fail(
                    rec["path"].relative_to(ROOT).as_posix(),
                    f"frontmatter '{key}' is still {TODO} in a '{rec['meta'].get('status')}' artefact",
                )


def gate_generated(arts: dict) -> None:
    if REGISTRY.exists() and REGISTRY.read_text() != render_registry(arts):
        fail("context/registry.yaml", "stale — run `make registry`")
    if INDEX.exists() and INDEX.read_text() != render_index(arts):
        fail("context/INDEX.md", "stale — run `make index`")


# --- generated files --------------------------------------------------------


def render_registry(arts: dict) -> str:
    out = ["# Generated by `make registry`. Do not edit by hand.", "artifacts:"]
    for aid in sorted(arts, key=lambda a: (a.split("-")[0], a)):
        rec = arts[aid]
        title = rec["meta"].get("title", "").replace('"', "'")
        out += [
            f"  - id: {aid}",
            f"    type: {rec['kind']}",
            f'    title: "{title}"',
            f"    status: {rec['meta'].get('status', '')}",
            f"    path: {rec['path'].relative_to(ROOT).as_posix()}",
        ]
    return "\n".join(out) + "\n"


def render_index(arts: dict) -> str:
    out = ["# Context index", "", "Generated by `make index`. Every artefact in the harness, by type.", ""]
    for kind in TYPES:
        rows = sorted((a for a in arts.values() if a["kind"] == kind), key=lambda r: r["meta"]["id"])
        if not rows:
            continue
        out += [f"## {kind}", "", "| ID | Title | Domain | Status |", "|---|---|---|---|"]
        for rec in rows:
            m = rec["meta"]
            link = rec["path"].relative_to(ROOT).as_posix()
            out.append(
                f"| [{m['id']}]({os.path.relpath(link, 'context')}) | {m.get('title', '')} "
                f"| {m.get('domain', '—')} | {m.get('status', '')} |"
            )
        out.append("")
    return "\n".join(out)


# --- scaffolding ------------------------------------------------------------

# Placeholder for a required field the author still has to answer.
TODO = "TODO"

SKELETONS = {
    "ADR": "## Decision\n\nTODO. One or two sentences, what we are doing.\n\n## Why\n\n- TODO\n\n"
    "## Instead of\n\nTODO. The alternative, and why not. Not optional.\n\n"
    "## Consequences\n\n- TODO, including what it costs.\n",
    "BPM": "## Purpose\n\nTODO. One sentence.\n\n## Flow\n\n1. TODO\n\n"
    "## Decision points\n\n- TODO\n\n## Failure modes\n\n- TODO\n\n## Outcome\n\nTODO.\n",
    "US": "**As** TODO **I want** TODO **so that** TODO.\n\n## Acceptance criteria\n\n"
    "| Id | Criterion | Verified by |\n|---|---|---|\n"
    "| `AC-{num}-01` | Given TODO, when TODO, then TODO | `test:TODO` |\n",
    "SPEC": "## Entities\n\n| Entity | Holds | Key |\n|---|---|---|\n| TODO | TODO | TODO |\n\n"
    "## Rules\n\n- TODO\n\n## Must never\n\n- TODO\n",
    "NFR": "TODO. What this constrains, and why it is worth a number.\n\n"
    "**How it is checked.** TODO.\n\n**What a failure means.** TODO.\n",
    "RULE": "**Rule.** TODO.\n\n**Why.** TODO.\n\n**Enforced by.** TODO.\n",
    "SKILL": "1. TODO\n\n**Gate.** TODO.\n",
    "PROC": "1. TODO\n\n**The one thing not to do.** TODO.\n",
    "EVAL": "**Question.** TODO.\n\n**Dataset.** TODO.\n\n**Metrics.** TODO.\n\n**Why it gates.** TODO.\n",
}


def slugify(title: str) -> str:
    out = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return re.sub(r"-{2,}", "-", out)


def scaffold(kind: str, title: str, arts: dict) -> int:
    """Create an artefact with correct frontmatter, a body skeleton and a log entry."""
    kind = kind.upper()
    if kind not in TYPES:
        print(f"unknown type {kind} — one of {', '.join(TYPES)}", file=sys.stderr)
        return 2
    if not title.strip():
        print('TITLE is required: make new TYPE=BPM TITLE="Short sentence"', file=sys.stderr)
        return 2
    aid = next_id(kind, arts)
    rel, required = TYPES[kind]
    path = ROOT / rel / f"{aid}-{slugify(title)}.md"
    if path.exists():
        print(f"{path} already exists", file=sys.stderr)
        return 2

    defaults = {"id": aid, "title": title, "type": kind.lower(), "status": "draft"}
    lines = ["---"]
    for key in required:
        lines.append(f"{key}: {defaults.get(key, TODO)}")
    lines += ["---", "", f"# {aid} — {title}", ""]
    body = SKELETONS[kind].replace("{num}", aid.split("-")[1])
    path.write_text("\n".join(lines) + "\n" + body, encoding="utf-8")

    log = CHANGELOG_FOR.get(path.parent.relative_to(ROOT).as_posix())
    logged = log_addition(ROOT / log, aid, path, title) if log else False
    print(f"created {path.relative_to(ROOT)}")
    print(f"logged  {log}" if logged else "no changelog for this directory")
    print("next    fill every TODO, set status, then `make fix && make harness-check`")
    return 0


def log_addition(log: Path, aid: str, path: Path, title: str) -> bool:
    """Add today's `### Added` line, creating the dated entry if it is not there."""
    import datetime

    today = datetime.date.today().isoformat()
    href = os.path.relpath(path, log.parent)
    bullet = f"- [{aid}]({href}): {title[0].lower() + title[1:]}"
    lines = log.read_text(encoding="utf-8").split("\n")
    di = next((i for i, line in enumerate(lines) if line.strip() == f"## {today}"), None)
    if di is None:
        first = next((i for i, line in enumerate(lines) if line.startswith("## ")), len(lines))
        lines[first:first] = [f"## {today}", "", "### Added", bullet, ""]
        log.write_text("\n".join(lines), encoding="utf-8")
        return True
    end = next((i for i in range(di + 1, len(lines)) if lines[i].startswith("## ")), len(lines))
    gi = next((i for i in range(di, end) if lines[i].strip() == "### Added"), None)
    if gi is None:
        lines[di + 1 : di + 1] = ["", "### Added", bullet]
    else:
        gend = next((i for i in range(gi + 1, end) if lines[i].startswith("###") or lines[i].startswith("## ")), end)
        while gend > gi + 1 and lines[gend - 1].strip() == "":
            gend -= 1
        lines[gend:gend] = [bullet]
    log.write_text("\n".join(lines), encoding="utf-8")
    return True


def next_id(kind: str, arts: dict) -> str:
    used = [int(a.split("-")[1]) for a in arts if a.startswith(kind + "-")]
    return f"{kind}-{(max(used) + 1 if used else 1):04d}"


def main() -> int:
    cmd = sys.argv[1] if len(sys.argv) > 1 else "check"
    arts = load_artifacts()
    if cmd == "registry":
        REGISTRY.write_text(render_registry(arts))
        print(f"wrote {REGISTRY.relative_to(ROOT)}")
        return 0
    if cmd == "index":
        INDEX.write_text(render_index(arts))
        print(f"wrote {INDEX.relative_to(ROOT)}")
        return 0
    if cmd == "linkfix":
        return linkfix(arts)
    if cmd == "id":
        kind = (sys.argv[2] if len(sys.argv) > 2 else "").upper()
        if kind not in TYPES:
            print(f"usage: id <{'|'.join(TYPES)}>")
            return 2
        print(next_id(kind, arts))
        return 0
    if cmd == "new":
        kind = sys.argv[2] if len(sys.argv) > 2 else ""
        title = " ".join(sys.argv[3:])
        return scaffold(kind, title, arts)

    gate_frontmatter(arts)
    gate_links(arts)
    gate_coverage(arts)
    gate_status(arts)
    gate_agents_and_changelogs()
    gate_names()
    gate_linkstyle(arts)
    gate_changelog_format()
    gate_changelog_coverage(arts)
    gate_todo(arts)
    gate_generated(arts)

    for w in warnings:
        print(f"warn  {w}")
    for e in errors:
        print(f"FAIL  {e}")
    print(f"\n{len(arts)} artefacts · {len(errors)} errors · {len(warnings)} warnings")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
