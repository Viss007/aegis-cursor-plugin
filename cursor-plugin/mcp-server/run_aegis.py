"""Aegis plugin MCP entry — bundled server.py. Optional agent_tools via env or sibling layout."""
from __future__ import annotations

import runpy
import sys
from pathlib import Path

here = Path(__file__).resolve().parent
bundled = here / "server.py"
if not bundled.is_file():
    sys.stderr.write(f"Aegis server missing: {bundled}\n")
    raise SystemExit(2)

from plugin_paths import prepend_sys_path  # noqa: E402

prepend_sys_path(sys)
sys.argv[0] = str(bundled)
runpy.run_path(str(bundled), run_name="__main__")
