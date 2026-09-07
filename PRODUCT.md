# Aegis — Product (one page)

**Lock (Viss, 2026-09-07):** Aegis is a **local MCP app / plugin ball**. Markdown in `pack/` is **design notes and contracts only** — not the installable product.

## Who buys

Developers and web coders (builders) who run coding agents locally and need them — and the humans directing them — to stop forgetting, inventing completion, and leaving no audit trail.

## What they install

**ONE local MCP package ball** (not a rules/skills dump into `.cursor`):

| Layer | Role |
|-------|------|
| **MCP tools** | The product — local MCP servers registered on the machine (stdio). Reliability behaviors (receipt, no-fake-done, verify-done) ship as **MCP tools**, not as `.md` / `.mdc` copies. |
| **Install** | Agent-assisted **one-shot** that registers those MCP servers into Cursor MCP config only |

**Not the product:** `pack/rules/*.mdc`, `pack/hooks/*.md`, `pack/skills/**`, `pack/commands/*.md` — these are **specs / contracts** for behaviors that must be implemented (or already partially stubbed) as MCP tooling. Do not treat copying them into `.cursor` as shipping Aegis.

**Dimensional / 8811** memory is a **spine MCP piece inside the ball**, not the entire product. CueBank sits in the family tree; **sell-push for CueBank / 8812 stays frozen**.

## Problem

Agents drop context, claim work is finished when it is not, and leave no trusted trail. Aegis attacks that with **callable MCP tools** on the builder's machine — receipts, fake-done gates, verify-done — not with markdown rules alone.

## What we do not sell (yet / frozen)

- Customer cloud hosting
- Invented harnesses
- CueBank / 8812 sell-push
- Narrow "Dimensional MCP only" framing as the whole SKU
- "Install = copy rules/skills/commands into `.cursor`" as the SKU

## Out of band (do not touch from this product tree)

- Google Drive moves / sync as a deliverable
- Zeus restart
- Video factory workstreams

## Install model

Agent-assisted **local** install of **MCP servers only**. See `install/README.md`. V1 core map: `CORE.md`, `BUNDLE.md`, `pack/mcp/v1-manifest.json`. Behavior contracts → MCP: `pack/SPEC.md`.