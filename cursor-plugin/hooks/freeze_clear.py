#!/usr/bin/env python3
"""beforeSubmitPrompt — clear Aegis freeze on the next human message."""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "mcp-server"))
import aegis_core as ac  # noqa: E402


def main() -> int:
    fp = ac.freeze_path()
    payload = {
        "schema_version": 1,
        "frozen": False,
        "reason": "cleared_on_submit",
        "claim_text": "",
        "ts": ac.utc_now(),
        "source": "aegis_freeze_clear_on_submit",
    }
    try:
        fp.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    except OSError:
        pass
    print(json.dumps({}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
