"""Start Aegis MCP over streamable HTTP (Context7-style icons path)."""
from __future__ import annotations

import os
import runpy
import sys
from pathlib import Path

os.environ.setdefault("AEGIS_TRANSPORT", "streamable-http")
os.environ.setdefault("AEGIS_HOST", "127.0.0.1")
os.environ.setdefault("AEGIS_PORT", "8815")
os.environ.setdefault("VISS_REPO_ROOT", r"C:\Users\Vismantas\Desktop\viss-workspace")
os.environ.setdefault("WORKSPACE_ROOT", r"C:\Users\Vismantas\Desktop\viss-workspace")
os.environ.setdefault("PYTHONUNBUFFERED", "1")

here = Path(__file__).resolve().parent
at = Path(r"C:\Users\Vismantas\Desktop\viss-workspace\agent_tools")
if str(at) not in sys.path:
    sys.path.insert(0, str(at))
if str(here) not in sys.path:
    sys.path.insert(0, str(here))

bundled = here / "server.py"
fallback = at / "aegis-mcp" / "server.py"
SERVER = bundled if bundled.is_file() else fallback
sys.argv[0] = str(SERVER)
runpy.run_path(str(SERVER), run_name="__main__")
