"""Aegis plugin MCP entry — runs the live control server."""
from __future__ import annotations

import runpy
import sys
from pathlib import Path

SERVER = Path(r"C:\Users\Vismantas\Desktop\viss-workspace\agent_tools\aegis-mcp\server.py")
if not SERVER.is_file():
    sys.stderr.write(f"Aegis server missing: {SERVER}\n")
    raise SystemExit(2)
# Ensure agent_tools on path for mcp_common
at = SERVER.parent.parent
if str(at) not in sys.path:
    sys.path.insert(0, str(at))
sys.argv[0] = str(SERVER)
runpy.run_path(str(SERVER), run_name="__main__")
