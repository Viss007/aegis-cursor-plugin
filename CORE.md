# Aegis - Core MCP set

**Date:** 2026-09-07
**Status:** LOCKED by Viss (2026-09-07 21:41 Europe/Vilnius)
**Rule:** names only from verified BUNDLE.md disk inventory. Nothing invented.

## V1 core (in the ball)

| # | Name | Why in core |
|---|------|-------------|
| 1 | `8811-retrieval` | Memory spine (Dimensional) inside the ball |
| 2 | `failure-ledger-mcp` | Trusted trail of failures |
| 3 | `trust-freeze-mcp` | Freeze / trust gate when things go wrong |
| 4 | `enforcer-mcp` | Enforce rules so agents stay honest |
| 5 | `hooks-status-mcp` | Hook health / status for the loop |
| 6 | `env-check-mcp` | Local env truth before claiming ready |
| 7 | `babysitter-mcp` | Watch agent jobs so they don't silently die |
| 8 | `runtime-mcp` | Runtime truth for local agent ops |

## Explicitly not V1 (candidates later)

`instrumentation-mcp`, `grok-enforce-mcp`, `parent-pinger-mcp`, `powershell-mcp`, `pc-ops-mcp`, plus the rest of the candidates.

## Out of scope (locked)

Zeus MCP, video MCPs, Google Drive, CueBank sell.

## Next

Vendor only this V1 set under `pack/mcp/` + define one-shot install. Do not ship all 53.
