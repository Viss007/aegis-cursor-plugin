# Aegis - Bundle manifest

**Lock (2026-09-07):** Aegis is **ONE local package ball** — MCP tooling + hooks + rules + skills + commands + install. Ultimate reliability toolkit for agents and humans. Local install. No customer cloud.

Dimensional / 8811 is a **spine piece inside the ball**, not the whole product.

Inventory below is from disk on Autobotas (`agent_tools\`). **Do not invent tools that are not listed.**

**V1 core locked (2026-09-07):** exactly 8 slots linked into `pack/mcp/` via directory junctions (`mklink /J`). Manifest: `pack/mcp/v1-manifest.json`.

---

## Planned layers (the ball)

| Layer | Pack path | Status now |
|-------|-----------|------------|
| Rules | `pack/rules/` | **Present:** `receipt-protocol.mdc` |
| Hooks | `pack/hooks/` | **Present:** `no-fake-done.md` (contract; runner stub) |
| Skills | `pack/skills/` | **Present:** `agent-reliability-spine/SKILL.md` |
| Commands | `pack/commands/` | **Present:** `verify-done.md` |
| MCP tools | `pack/mcp/` | **V1 linked-in-pack:** 8 junctions + `v1-manifest.json` (see below) |
| Install | `install/` | **One-shot outline** in `install/README.md` (local Cursor user config; no cloud) |

Optional pack folders (`pack/agents/`, `pack/prompts/`): **not created** — no empty junk until content exists.

---

## Spine (inside the ball, not the SKU)

| Name on disk | Role | Mark |
|--------------|------|------|
| `8811-retrieval` | Dimensional / 8811 memory spine (folder under `agent_tools\`; not a `*-mcp` name) | **linked-in-pack** (`pack/mcp/8811-retrieval/`) |

---

## Verified local MCP-like dirs (`agent_tools\`)

**Selection rule (verified by listing dirs):** folder name matches `*-mcp` / `mcp-server` / exact `mcp`, **or** top-level `server.py` / `index.mjs` present.

**Count: 53**

Marks:

- **in-pack** / **linked-in-pack** — shipped under `Aegis/pack/mcp/` as part of the ball (vendored copy **or** junction `src` → `agent_tools\<name>`)
- **candidate** — on disk; eligible to map into the ball later (reliability / builder / local ops)
- **out-of-scope** — frozen or excluded by lock (CueBank sell, Zeus restart, video factory, or not reliability-ball)

### Mark legend applied this lock

| Mark | Criteria used |
|------|----------------|
| linked-in-pack | Junction under `pack/mcp/<name>/src` + `SOURCE.md` (V1 core) |
| in-pack | Vendored tree under `pack/mcp/` (none yet beyond links) |
| out-of-scope | Zeus-named MCP; video-factory media MCPs (`runway`, `udio`, `partner-film`, `podcast-ai`); not for this ball while locks hold |
| candidate | Everything else in the verified list (still must be mapped before install) |

### Full list (names only)

| # | Name | Mark |
|---|------|------|
| 1 | `automation-mcp` | candidate |
| 2 | `babysitter-mcp` | linked-in-pack |
| 3 | `brave-search-mcp` | candidate |
| 4 | `byok-mcp` | candidate |
| 5 | `chatgpt-read-mcp` | candidate |
| 6 | `cursor-cli-8808` | candidate |
| 7 | `cursor-ide-mcp` | candidate |
| 8 | `cursor-nudge-mcp` | candidate |
| 9 | `cvbankas-mcp` | candidate |
| 10 | `design-desk-mcp` | candidate |
| 11 | `devis-mcp` | candidate |
| 12 | `enforcer-mcp` | linked-in-pack |
| 13 | `env-check-mcp` | linked-in-pack |
| 14 | `failure-ledger-mcp` | linked-in-pack |
| 15 | `garden-broker-mcp` | candidate |
| 16 | `github-mcp-server` | candidate |
| 17 | `gmail-lead-mcp` | candidate |
| 18 | `gmail-sandbox-mcp` | candidate |
| 19 | `godmode-8807` | candidate |
| 20 | `godmode-mcp` | candidate |
| 21 | `godmode-operator-mcp` | candidate |
| 22 | `grok-cli-mcp` | candidate |
| 23 | `grok-enforce-mcp` | candidate |
| 24 | `grok-voice-mcp` | candidate |
| 25 | `health-desk-mcp` | candidate |
| 26 | `health-portal-cookies-mcp` | candidate |
| 27 | `hooks-status-mcp` | linked-in-pack |
| 28 | `instrumentation-mcp` | candidate |
| 29 | `invoice-mcp` | candidate |
| 30 | `leo-ai-mcp` | candidate |
| 31 | `local-llm-mcp` | candidate |
| 32 | `mcp` | candidate |
| 33 | `mobile-desk-mcp` | candidate |
| 34 | `outdoor-weather-mcp` | candidate |
| 35 | `parent-pinger-mcp` | candidate |
| 36 | `partner-film-mcp` | out-of-scope |
| 37 | `pc-ops-mcp` | candidate |
| 38 | `pocket-mcp` | candidate |
| 39 | `podcast-ai-mcp` | out-of-scope |
| 40 | `powershell-mcp` | candidate |
| 41 | `preset-libraries-mcp` | candidate |
| 42 | `roast-desk-mcp` | candidate |
| 43 | `runtime-mcp` | linked-in-pack |
| 44 | `runway-mcp` | out-of-scope |
| 45 | `serena-mcp` | candidate |
| 46 | `speak-mcp` | candidate |
| 47 | `trust-freeze-mcp` | linked-in-pack |
| 48 | `udio-mcp` | out-of-scope |
| 49 | `voice-agent-mcp` | candidate |
| 50 | `voice-rex-mcp` | candidate |
| 51 | `web-development-mcp` | candidate |
| 52 | `zed-pty-mcp` | candidate |
| 53 | `zeus-8803-mcp` | out-of-scope |

### Counts by mark

| Mark | Count |
|------|------:|
| linked-in-pack (of the 53 MCP-like dirs) | 7 |
| linked-in-pack spine (outside the 53) | 1 (`8811-retrieval`) |
| **V1 total linked-in-pack** | **8** |
| candidate | 41 |
| out-of-scope | 5 |
| **total verified MCP-like** | **53** |

### V1 locked core (exactly these 8)

| Name | Pack slot | Method | Status |
|------|-----------|--------|--------|
| `8811-retrieval` | `pack/mcp/8811-retrieval/` | junction | linked |
| `failure-ledger-mcp` | `pack/mcp/failure-ledger-mcp/` | junction | linked |
| `trust-freeze-mcp` | `pack/mcp/trust-freeze-mcp/` | junction | linked |
| `enforcer-mcp` | `pack/mcp/enforcer-mcp/` | junction | linked |
| `hooks-status-mcp` | `pack/mcp/hooks-status-mcp/` | junction | linked |
| `env-check-mcp` | `pack/mcp/env-check-mcp/` | junction | linked |
| `babysitter-mcp` | `pack/mcp/babysitter-mcp/` | junction | linked |
| `runtime-mcp` | `pack/mcp/runtime-mcp/` | junction | linked |

### Reliability-first shortlist (remaining candidates — next mapping pass)

Not a new invention list — names already on disk, still **candidate** after V1 lock:

- `instrumentation-mcp`
- `grok-enforce-mcp`
- `parent-pinger-mcp`
- `powershell-mcp`
- `pc-ops-mcp`

(V1 eight already linked-in-pack — do not re-list as pending.)

---

## Explicitly frozen / do-not-touch

- CueBank / 8812 **sell** frozen (no sell-push; no CueBank MCP invent from this tree)
- Google Drive — leave alone
- Zeus **restart** — leave alone (`zeus-8803-mcp` out-of-scope for this lock)
- Video factory — leave alone (`runway-mcp`, `udio-mcp`, `partner-film-mcp`, `podcast-ai-mcp` out-of-scope)

---

## Next (see STATUS.md)

1. Agent-assisted install per `install/README.md` (register V1 MCPs + copy rules/hooks/skills/commands into Cursor user config).
2. Optional: map remaining reliability candidates into pack decisions.
3. Do not deploy; do not Drive; do not CueBank sell; do not restart Zeus.
