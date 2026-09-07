"""Shared Aegis control helpers for MCP server + Cursor hooks."""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

_DONE_WORDS = re.compile(
    r"\b(done|finished|complete|completed|shipped)\b",
    re.IGNORECASE,
)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def repo_root_from_hooks() -> Path:
    # .cursor/hooks -> repo root
    return Path(__file__).resolve().parents[2]


def aegis_dir(root: Path | None = None) -> Path:
    r = root or repo_root_from_hooks()
    d = r / "var" / "aegis"
    d.mkdir(parents=True, exist_ok=True)
    return d


def receipts_dir(root: Path | None = None) -> Path:
    d = aegis_dir(root) / "receipts"
    d.mkdir(parents=True, exist_ok=True)
    return d


def freeze_path(root: Path | None = None) -> Path:
    return aegis_dir(root) / "freeze.json"


def parse_claimed_paths(claimed_paths: str) -> list[str]:
    parts = re.split(r"[;,\n]+", claimed_paths or "")
    return [p.strip() for p in parts if p.strip()]


def load_receipt(receipt_id: str, root: Path | None = None) -> dict[str, Any] | None:
    rid = (receipt_id or "").strip()
    if not rid:
        return None
    safe = re.sub(r"[^a-zA-Z0-9_\-]", "_", rid)
    path = receipts_dir(root) / f"{safe}.jsonl"
    if not path.is_file():
        return None
    out: dict[str, Any] = {}
    try:
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(obj, dict):
                out.update(obj)
    except OSError:
        return None
    if not out:
        return None
    out["id"] = rid
    return out


def append_hook_event(event: dict[str, Any], root: Path | None = None) -> Path:
    path = aegis_dir(root) / "hook-events.jsonl"
    row = dict(event)
    row.setdefault("ts", utc_now())
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, ensure_ascii=False, default=str) + "\n")
    return path


def no_fake_done_check(
    claim_text: str,
    claimed_paths: str = "",
    receipt_id: str = "",
    root: Path | None = None,
) -> dict[str, Any]:
    paths = parse_claimed_paths(claimed_paths)
    existing_paths = [p for p in paths if Path(p).exists()]
    any_path_exists = bool(existing_paths)

    receipt_pass = False
    receipt_state = "missing"
    rid = (receipt_id or "").strip()
    if rid:
        rec = load_receipt(rid, root)
        if rec is None:
            receipt_state = "missing"
        else:
            verdict = str(rec.get("verdict") or "").upper()
            status = str(rec.get("status") or "").lower()
            if verdict == "PASS" and status == "finished":
                receipt_pass = True
                receipt_state = "PASS"
            elif verdict == "FAIL":
                receipt_state = "FAIL"
            elif status:
                receipt_state = status
            else:
                receipt_state = "present_no_pass"

    has_done_claim = bool(_DONE_WORDS.search(claim_text or ""))

    if any_path_exists or receipt_pass:
        decision = "ALLOW"
        reason = (
            "at least one claimed path exists"
            if any_path_exists
            else f"receipt_id {rid} resolves to PASS"
        )
    elif has_done_claim and not any_path_exists and not receipt_pass:
        decision = "BLOCK"
        reason = (
            "claim uses done/finished/complete/shipped without existing path "
            "and without a PASS receipt"
        )
    else:
        decision = "FLAG"
        reason = "weak evidence: no done-word block, but no existing path and no PASS receipt"

    return {
        "ok": True,
        "decision": decision,
        "reason": reason,
        "claimed_paths": paths,
        "existing_paths": existing_paths,
        "receipt_id": rid or None,
        "receipt_state": receipt_state,
        "has_done_claim": has_done_claim,
    }


def write_aegis_freeze(reason: str, claim_text: str = "", root: Path | None = None) -> Path:
    fp = freeze_path(root)
    payload = {
        "schema_version": 1,
        "frozen": True,
        "reason": reason,
        "claim_text": (claim_text or "")[:500],
        "ts": utc_now(),
        "source": "aegis-hook",
    }
    fp.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return fp


def read_aegis_freeze(root: Path | None = None) -> dict[str, Any]:
    fp = freeze_path(root)
    if not fp.is_file():
        return {"frozen": False, "freeze": None, "freeze_path": str(fp)}
    try:
        data = json.loads(fp.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {"frozen": False, "freeze": None, "freeze_path": str(fp), "error": "read_failed"}
    if not isinstance(data, dict):
        data = {"raw": data}
    return {"frozen": bool(data.get("frozen")), "freeze": data, "freeze_path": str(fp)}
