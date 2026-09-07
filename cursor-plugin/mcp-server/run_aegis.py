"""Aegis plugin MCP entry — prefer bundled server.py, else workspace live server."""
from __future__ import annotations

import runpy
import sys
from pathlib import Path

here = Path(__file__).resolve().parent
bundled = here / "server.py"
fallback = Path(r"C:\Users\Vismantas\Desktop\viss-workspace\agent_tools\aegis-mcp\server.py")
SERVER = bundled if bundled.is_file() else fallback
if not SERVER.is_file():
    sys.stderr.write(f"Aegis server missing: {SERVER}\n")
    raise SystemExit(2)
at = Path(r"C:\Users\Vismantas\Desktop\viss-workspace\agent_tools")
if str(at) not in sys.path:
    sys.path.insert(0, str(at))
# also allow importing sibling aegis_core
if str(here) not in sys.path:
    sys.path.insert(0, str(here))
sys.argv[0] = str(SERVER)
runpy.run_path(str(SERVER), run_name="__main__")
