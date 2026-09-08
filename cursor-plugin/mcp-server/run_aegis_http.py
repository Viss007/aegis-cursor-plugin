"""Start Aegis MCP over streamable HTTP (Context7-style icons path)."""
from __future__ import annotations

import os
import runpy
import sys
from pathlib import Path

os.environ.setdefault("AEGIS_TRANSPORT", "streamable-http")
os.environ.setdefault("AEGIS_HOST", "127.0.0.1")
os.environ.setdefault("AEGIS_PORT", "18715")
os.environ.setdefault("PYTHONUNBUFFERED", "1")

here = Path(__file__).resolve().parent
sys.path.insert(0, str(here))
from plugin_paths import agent_tools, prepend_sys_path  # noqa: E402

at = agent_tools()
if at is not None:
    os.environ.setdefault("VISS_REPO_ROOT", str(at.parent))
    os.environ.setdefault("WORKSPACE_ROOT", str(at.parent))

prepend_sys_path(sys)
SERVER = here / "server.py"
if not SERVER.is_file():
    sys.stderr.write(f"Aegis server missing: {SERVER}\n")
    raise SystemExit(2)
sys.argv[0] = str(SERVER)
runpy.run_path(str(SERVER), run_name="__main__")
