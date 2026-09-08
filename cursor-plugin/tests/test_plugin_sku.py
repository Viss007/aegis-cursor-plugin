"""RED/GREEN: Aegis plugin SKU is portable and ships hooks."""
from __future__ import annotations

import json
import pathlib
import unittest

PLUGIN = pathlib.Path(__file__).resolve().parents[1]
MCP = PLUGIN / "mcp-server"


def _read(name: str) -> str:
    return (MCP / name).read_text(encoding="utf-8-sig")


class AegisPluginSkuTests(unittest.TestCase):
    def test_launchers_have_no_autobotas_user_path(self) -> None:
        banned = r"C:\Users\Vismantas"
        for name in ("run_aegis.py", "run_aegis_http.py", "ensure_aegis_http.ps1"):
            blob = _read(name)
            self.assertNotIn(banned, blob, msg=name)

    def test_plugin_json_points_at_hooks(self) -> None:
        plugin_json = json.loads((PLUGIN / ".cursor-plugin" / "plugin.json").read_text(encoding="utf-8"))
        self.assertIn("hooks", plugin_json)
        hooks_rel = plugin_json["hooks"].replace("\\", "/")
        self.assertTrue((PLUGIN / hooks_rel.lstrip("./")).is_file())

    def test_hooks_json_has_wall_events(self) -> None:
        hooks_path = PLUGIN / "hooks" / "hooks.json"
        self.assertTrue(hooks_path.is_file())
        data = json.loads(hooks_path.read_text(encoding="utf-8"))
        self.assertEqual(data.get("version"), 1)
        events = data.get("hooks") or {}
        self.assertIn("afterAgentResponse", events)
        self.assertIn("preToolUse", events)


if __name__ == "__main__":
    unittest.main()
