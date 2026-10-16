---
id: RULE-0010
title: Local development conventions, on a workstation or in Coder
type: rule
status: accepted
scope: repo
---

# RULE-0010 — Local development conventions, on a workstation or in Coder

**Rule.** Development happens locally, on a developer's own workstation or in a Coder workspace, and the two are one environment. Treat both as disposable: everything needed to rebuild either is in the repository.

- **Environment.** `$CODER=true` identifies a Coder workspace. Branch on it only where the two genuinely differ, which today is GitHub authentication ([RULE-0009](RULE-0009-use-gh-for-github.md)). Never branch on a hostname or a path.
- **Python.** The version in `.python-version`, in the project's `.venv`, made by uv. Never the system `python3`. `make` builds `.venv` on first use.
- **Backing services.** Run in containers, started and stopped by `make` targets. Never install a database or any other backing service directly on the machine.
- **Dependencies.** Install into the project's own virtual environment or `node_modules`, never system-wide. A dependency that is not in a lock file does not exist. Python uses uv; never `pip install` into the environment. Node uses pnpm; never `npm install` in a workspace package.
- **Configuration.** Load variables from the local `.env`, which is never committed:
  ```bash
  set -a; source .env; set +a
  ```
- **Long-running processes.** Start servers and workers in the tool's background mode, not with `nohup` or `setsid`, which get reaped when the command returns and die silently. Confirm a server is up by requesting it, not by checking for a listening socket.
- **Ports.** Declared in one place in the repository. Before stopping a process, check its working directory is this checkout. Another checkout's server on the same port is not yours to kill.
- **Scratch files.** Nothing temporary is written into the repository. Use a scratch directory outside it.
- **Cloud access.** Use workload identity and a secret manager. Never a downloaded key file. See [RULE-0014](RULE-0014-no-secrets-in-the-repository.md).

**Why.** An environment that carries hidden state produces work that only builds there, and the next one starts broken. Two environments that drift apart produce work that builds on one and not the other.

**Enforced by.** `.gitignore` covers `.env` and local artefacts; CI builds from a clean checkout, which fails on anything that only exists in one environment.
