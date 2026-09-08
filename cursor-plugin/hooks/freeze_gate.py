#!/usr/bin/env python3
"""preToolUse — deny mutating tools while Aegis freeze is on."""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "mcp-server"))
import aegis_core as ac  # noqa: E402

AGENT_DENY = "AEGIS FREEZE: mutating tools blocked. Send another message to clear."
USER_DENY = "Aegis freeze is ON — send another message to continue."
_ALLOW = frozenset({"Read", "Grep", "Glob", "GetMcpTools", "FetchMcpResource", "ReadLints"})


def _tool_name(payload: dict) -> str:
    for key in ("tool_name", "toolName", "name"):
        v = payload.get(key)
        if isinstance(v, str) and v.strip():
            return v.strip()
    return ""


def main() -> int:
    raw = sys.stdin.buffer.read().decode("utf-8-sig", errors="replace")
    try:
        payload = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        payload = {}
    if not isinstance(payload, dict):
        payload = {}
    st = ac.read_aegis_freeze()
    if not st.get("frozen") or _tool_name(payload) in _ALLOW:
        print(json.dumps({"permission": "allow"}))
        return 0
    print(
        json.dumps(
            {
                "permission": "deny",
                "user_message": USER_DENY,
                "agent_message": AGENT_DENY,
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
