"""Checks staged code before a commit: format, lint, then types. Implements RULE-0019.

Install with `make hooks`. It checks the staged files as they are in the working tree, and never rewrites them.
One hook serves the workspace's root repo and each app repo; it works out which one it was called from.
Add each app to the lists below in the same change that adds the app.
"""

import subprocess
import sys
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parents[2]
# .NET apps, directory to the solution holding the app and its tests.
DOTNET_PROJECTS: dict[str, str] = {"online-delivery-api": "OnlineDelivery.sln"}
# Node apps formatted by their own Prettier and linted by their own ESLint.
NODE_PROJECTS: tuple[str, ...] = ("online-delivery-app",)
DOTNET_SUFFIXES = (".cs", ".csproj", ".sln", ".editorconfig")
PRETTIER_SUFFIXES = (".js", ".jsx", ".mjs", ".cjs", ".ts", ".tsx", ".css", ".json", ".html")
ESLINT_SUFFIXES = (".js", ".jsx", ".mjs", ".cjs", ".ts", ".tsx")


def git(*args: str) -> str:
    return subprocess.run(["git", *args], capture_output=True, text=True, check=True).stdout


def staged() -> list[str]:
    """Staged paths, relative to the workspace root."""
    top = Path(git("rev-parse", "--show-toplevel").strip()).resolve()
    prefix = top.relative_to(WORKSPACE).as_posix()
    names = [f for f in git("diff", "--cached", "--name-only", "--diff-filter=ACMR", "-z").split("\0") if f]
    return [f if prefix == "." else f"{prefix}/{f}" for f in names]


def run(label: str, cmd: list[str], cwd: Path) -> bool:
    print(f"pre-commit: {label}", flush=True)
    try:
        return subprocess.run(cmd, cwd=cwd).returncode == 0
    except FileNotFoundError:
        print(f"pre-commit: {cmd[0]} is not on PATH; install it first (RULE-0010)", file=sys.stderr)
        return False


def under(app: str, files: list[str], suffixes: tuple[str, ...]) -> list[str]:
    """Files inside an app that end with one of the suffixes, relative to that app."""
    return [f.removeprefix(app + "/") for f in files if f.startswith(app + "/") and f.endswith(suffixes)]


def main() -> int:
    files = staged()
    checks: list[tuple[str, list[str], Path]] = []

    py = [f for f in files if f.endswith(".py")]
    if py:
        checks.append(("ruff format", ["uv", "run", "ruff", "format", "--check", "--quiet", *py], WORKSPACE))
        checks.append(("ruff lint", ["uv", "run", "ruff", "check", "--quiet", *py], WORKSPACE))

    # The context gate takes a second, so any markdown change runs all of it, AGENTS.md files in the apps included.
    if any(f.endswith(".md") for f in files):
        checks.append(("harness-check", [sys.executable, "harness/gates/harness_check.py", "check"], WORKSPACE))

    for app, proj in DOTNET_PROJECTS.items():
        cs = under(app, files, DOTNET_SUFFIXES)
        if cs:
            include = [f for f in cs if f.endswith(".cs")]
            fmt = ["dotnet", "format", proj, "--verify-no-changes"] + (["--include", *include] if include else [])
            checks.append((f"dotnet format {app}", fmt, WORKSPACE / app))
            build = ["dotnet", "build", proj, "-warnaserror", "--nologo", "-v", "q"]
            checks.append((f"dotnet build {app}", build, WORKSPACE / app))

    for app in NODE_PROJECTS:
        bin_dir = WORKSPACE / app / "node_modules/.bin"
        pretty = under(app, files, PRETTIER_SUFFIXES)
        if pretty:
            prettier = [str(bin_dir / "prettier"), "--check", "--log-level", "warn", *pretty]
            checks.append((f"prettier {app}", prettier, WORKSPACE / app))
        lintable = under(app, files, ESLINT_SUFFIXES)
        if lintable:
            checks.append((f"eslint {app}", [str(bin_dir / "eslint"), *lintable], WORKSPACE / app))

    failed = [label for label, cmd, cwd in checks if not run(label, cmd, cwd)]
    if failed:
        print(
            f"\nCommit refused (RULE-0019): {', '.join(failed)}.\n"
            "Formatting is fixed by `make fmt`. Fix the rest, stage it, and commit again. Never use --no-verify.",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
