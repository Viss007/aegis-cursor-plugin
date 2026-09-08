"""Resolve plugin + optional agent_tools without a machine-specific path."""
from __future__ import annotations

import os
from pathlib import Path


def plugin_mcp_dir() -> Path:
    return Path(__file__).resolve().parent


def plugin_root() -> Path:
    return plugin_mcp_dir().parent


def agent_tools() -> Path | None:
    env = (os.environ.get("AEGIS_AGENT_TOOLS") or "").strip()
    if env:
        p = Path(env)
        if p.is_dir():
            return p
    repo = (os.environ.get("VISS_REPO_ROOT") or os.environ.get("WORKSPACE_ROOT") or "").strip()
    if repo:
        p = Path(repo) / "agent_tools"
        if p.is_dir():
            return p
    here = plugin_mcp_dir()
    for up in (3, 2, 1):
        try:
            cand = here.parents[up] / "agent_tools"
        except IndexError:
            continue
        if p_ok(cand):
            return cand
    return None


def p_ok(p: Path) -> bool:
    return p.is_dir() and ((p / "mcp_common").is_dir() or (p / "aegis-mcp").is_dir())


def prepend_sys_path(sys_mod) -> None:
    here = plugin_mcp_dir()
    at = agent_tools()
    if at is not None and str(at) not in sys_mod.path:
        sys_mod.path.insert(0, str(at))
    if str(here) not in sys_mod.path:
        sys_mod.path.insert(0, str(here))
