---
id: RULE-0018
title: Documentation servers are reached only through MCP tools
type: rule
status: accepted
scope: repo
---

# RULE-0018 — Documentation servers are reached only through MCP tools

**Rule.** The documentation servers in `.mcp.json` are used only through the MCP tools the agent's session loads from that file. Never call a server's endpoint directly: no `curl`, no hand-built JSON-RPC, no scratch script. If a server's tools are missing or it failed to connect, say so and stop. Do not work around it.

| Server | Covers | Rule that requires it |
|---|---|---|
| — | None configured yet. The app does not use shadcn/ui, so its server was removed | [RULE-0017](RULE-0017-external-apis-from-the-documentation.md) |

A new server is added to `.mcp.json`, to `enabledMcpjsonServers` in `.claude/settings.json` and to this table in the same change.

A server that runs locally is a pinned dev dependency, and `.mcp.json` starts its binary from `node_modules`. Never start one with `npx`: a first run downloads the package inside the client's start-up timeout, and a download cut short leaves a broken cache that fails every later start.

**Why.** The tools are what the harness can see, approve and log. A direct call bypasses all three, and it produces answers nobody can trace back to a source. A server that is down is a fact to report, not a problem to route around.

**Enforced by.** Review. The project's `.claude/settings.json` names the servers to enable, so every agent working here gets the same set.
