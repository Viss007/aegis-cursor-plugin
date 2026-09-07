# Aegis - Status

**Date:** 2026-09-07 (Europe/Vilnius)
**Updated:** 2026-09-07 22:10 (Europe/Vilnius)

**State:** control MCP landed (egis-mcp) — receipts / verify-done / no-fake-done / freeze / memory_pull as callable tools.

## Lock (Viss, 2026-09-07) - MCP app

- **Aegis = local MCP app / plugin ball.** `.md` / `.mdc` files are **not** the product.
- Receipt / no-fake-done / verify-done behavior must be integrated into **MCP tooling** (see `pack/SPEC.md`).
- One-shot install **registers MCP servers only** - does **not** copy rules/skills/commands markdown into `.cursor` as the SKU.
- Video factory parked; Google Drive left alone; CueBank sell frozen; no Zeus restart; do not break junctions.
- Renamed to Aegis on 2026-09-07 by Viss.
- V1 core (8) still locked: see `CORE.md` / `pack/mcp/v1-manifest.json`.
- **Control app:** `aegis-mcp` added beside the eight (`role: control`).

## Present

- Framing: `README.md`, `PRODUCT.md` (rewritten MCP-app), `BUNDLE.md`, `CORE.md`
- Install: `install/README.md` (MCP-register only; no md-copy product path)
- Spec: `pack/SPEC.md` - three behaviors → MCP tools
- Design notes still on disk (contracts, not installables):
  - `pack/rules/receipt-protocol.mdc`
  - `pack/hooks/no-fake-done.md`
  - `pack/skills/agent-reliability-spine/SKILL.md`
  - `pack/commands/verify-done.md`
- V1 MCP junctions under `pack/mcp/` (linked to `agent_tools`, not deep-copied)
- **Control MCP:** `agent_tools/aegis-mcp/server.py` junctioned at `pack/mcp/aegis-mcp/src`
  - Tools: `receipt_begin`, `receipt_log`, `receipt_finish`, `no_fake_done`, `verify_done`, `memory_pull`, `freeze_on_lie`, `freeze_status`
  - State: `var/aegis/receipts/`, `var/aegis/freeze.json`

## Next

control MCP landed

## Not present

- Shipped install artifacts beyond junction + register outline
- Metrics / launch claims / customer cloud

## Prior locks

- Core lock (2026-09-07 21:41): V1 eight MCPs - see `CORE.md`
- Bundle direction: full local ball; 8811 is spine inside, not the whole SKU
- MCP-app lock (2026-09-07): markdown is not the product; control tools live in MCP
