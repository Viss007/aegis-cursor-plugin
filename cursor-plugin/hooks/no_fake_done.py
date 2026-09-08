#!/usr/bin/env python3
"""afterAgentResponse — freeze when the model claims done with no path."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "mcp-server"))
import aegis_core as ac  # noqa: E402

_PATH_RE = re.compile(
    r"(?:[A-Za-z]:[\\/][^\s\"']+|\\\\[^\s\"']+|/(?:Users|home|workspace|tmp|var)[^\s\"']+)",
)


def main() -> int:
    raw = sys.stdin.buffer.read().decode("utf-8-sig", errors="replace")
    try:
        payload = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        payload = {}
    if not isinstance(payload, dict):
        payload = {}
    text = str(payload.get("text", "") or payload.get("response", "") or "")
    claimed = "\n".join(_PATH_RE.findall(text))
    result = ac.no_fake_done_check(text, claimed_paths=claimed)
    if result["decision"] == "BLOCK":
        try:
            ac.write_aegis_freeze(reason=result["reason"], claim_text=text[:500])
        except OSError:
            pass
    print(json.dumps({}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
