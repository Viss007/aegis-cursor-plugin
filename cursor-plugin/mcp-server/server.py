from __future__ import annotations

import json
import re
import sys
import uuid
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

_AT = Path(__file__).resolve().parents[1]
if str(_AT) not in sys.path:
    sys.path.insert(0, str(_AT))

from mcp.server.fastmcp import FastMCP, Icon
from mcp_common.jsonutil import dumps, err
from mcp_common.paths import hooks_dir, repo_root


def _aegis_icons() -> list[Icon]:
    """Match Context7 shape: one HTTPS PNG in serverInfo.icons (MCP row uses this)."""
    https_png = "https://raw.githubusercontent.com/Viss007/aegis-cursor-plugin/main/assets/logo.png"
    return [Icon(src=https_png, mimeType="image/png", sizes=["512x512", "any"])]


mcp = FastMCP(
    "Aegis",
    icons=_aegis_icons(),
    website_url="https://github.com/Viss007/aegis-cursor-plugin",
    instructions=(
        "Aegis control layer â€” receipts, verify-done, no-fake-done, "
        "memory pull, freeze-on-lie. Local only."
    ),
)

_DONE_WORDS = re.compile(
    r"\b(done|finished|complete|completed|shipped)\b",
    re.IGNORECASE,
)
_DIMENSIONAL_URL = "http://127.0.0.1:8811/api/dimensional"


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _aegis_dir() -> Path:
    return repo_root() / "var" / "aegis"


def _receipts_dir() -> Path:
    d = _aegis_dir() / "receipts"
    d.mkdir(parents=True, exist_ok=True)
    return d


def _freeze_path() -> Path:
    d = _aegis_dir()
    d.mkdir(parents=True, exist_ok=True)
    return d / "freeze.json"


def _receipt_path(receipt_id: str) -> Path:
    safe = re.sub(r"[^a-zA-Z0-9_\-]", "_", (receipt_id or "").strip())
    return _receipts_dir() / f"{safe}.jsonl"


def _receipt_events_path(receipt_id: str) -> Path:
    safe = re.sub(r"[^a-zA-Z0-9_\-]", "_", (receipt_id or "").strip())
    return _receipts_dir() / f"{safe}.events.jsonl"


def _append_jsonl(path: Path, row: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, ensure_ascii=False, default=str) + "\n")


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    rows: list[dict[str, Any]] = []
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict):
            rows.append(obj)
    return rows


def _load_receipt(receipt_id: str) -> dict[str, Any] | None:
    rid = (receipt_id or "").strip()
    if not rid:
        return None
    rows = _read_jsonl(_receipt_path(rid))
    if not rows:
        return None
    # Prefer last status-bearing row; merge chronologically.
    out: dict[str, Any] = {}
    for row in rows:
        out.update(row)
    out["id"] = rid
    return out


def _looks_like_local_path(s: str) -> bool:
    t = (s or "").strip()
    if not t:
        return False
    if "://" in t and not t.lower().startswith("file:"):
        return False
    if t.lower().startswith("file:"):
        return True
    # Windows drive, UNC, or absolute/relative filesystem-ish
    if re.match(r"^[A-Za-z]:[\\/]", t):
        return True
    if t.startswith("\\\\") or t.startswith("/") or t.startswith(".\\") or t.startswith("./"):
        return True
    if "\\" in t or "/" in t:
        return True
    return False


def _path_from_claim(s: str) -> Path:
    t = (s or "").strip()
    if t.lower().startswith("file:"):
        t = t[5:]
        if t.startswith("///"):
            t = t[3:]
        elif t.startswith("//"):
            t = t[1:]
    return Path(t)


def _parse_claimed_paths(claimed_paths: str) -> list[str]:
    raw = claimed_paths or ""
    parts = re.split(r"[;,\n]+", raw)
    return [p.strip() for p in parts if p.strip()]


def _post_dimensional(action: str, params: dict[str, Any]) -> dict[str, Any]:
    """POST verified 8811 shape from dimensional_client / mcp_http_fallback."""
    body = {"action": action, "params": params or {}}
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        _DIMENSIONAL_URL,
        data=data,
        method="POST",
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            parsed = json.loads(resp.read().decode("utf-8", errors="replace"))
            return parsed if isinstance(parsed, dict) else {"raw": parsed}
    except urllib.error.HTTPError as exc:
        try:
            parsed = json.loads(exc.read().decode("utf-8", errors="replace"))
            if isinstance(parsed, dict):
                return parsed
        except Exception:  # noqa: BLE001
            pass
        return {"status": "error", "error": str(exc), "http_status": getattr(exc, "code", None)}
    except Exception as exc:  # noqa: BLE001
        return {"status": "error", "error": str(exc), "code": "transport_error"}


@mcp.tool()
def receipt_begin(intent: str, target: str, done_when: str) -> str:
    """Start a receipt trail: Intent / Target / Done-when. Writes JSONL under var/aegis/receipts/."""
    receipt_id = uuid.uuid4().hex
    path = _receipt_path(receipt_id)
    row = {
        "id": receipt_id,
        "ts": _utc_now(),
        "intent": intent,
        "target": target,
        "done_when": done_when,
        "status": "started",
        "event": "begin",
    }
    try:
        _append_jsonl(path, row)
    except OSError as exc:
        return err(f"receipt_begin write failed: {exc}")
    return dumps(
        {
            "ok": True,
            "receipt_id": receipt_id,
            "path": str(path),
            "status": "started",
        }
    )


@mcp.tool()
def receipt_log(receipt_id: str, tool_name: str, detail: str = "") -> str:
    """Append a while-act tool event to an existing receipt. FAIL if unknown id."""
    rid = (receipt_id or "").strip()
    if not rid or _load_receipt(rid) is None:
        return err(f"unknown receipt_id: {receipt_id!r}", receipt_id=receipt_id)
    event_path = _receipt_events_path(rid)
    main_path = _receipt_path(rid)
    row = {
        "id": rid,
        "ts": _utc_now(),
        "event": "log",
        "tool_name": tool_name,
        "detail": detail or "",
    }
    try:
        _append_jsonl(event_path, row)
        _append_jsonl(main_path, row)
    except OSError as exc:
        return err(f"receipt_log write failed: {exc}")
    return dumps(
        {
            "ok": True,
            "receipt_id": rid,
            "path": str(main_path),
            "events_path": str(event_path),
            "tool_name": tool_name,
        }
    )


@mcp.tool()
def receipt_finish(
    receipt_id: str,
    path_or_url: str,
    proving_numbers: str,
    verdict: str,
) -> str:
    """Finish receipt with PASS|FAIL. PASS + local path requires Path.exists()."""
    rid = (receipt_id or "").strip()
    existing = _load_receipt(rid)
    if existing is None:
        return err(f"unknown receipt_id: {receipt_id!r}", receipt_id=receipt_id)

    v = (verdict or "").strip().upper()
    if v not in ("PASS", "FAIL"):
        return err(
            f"verdict must be PASS or FAIL (got {verdict!r})",
            receipt_id=rid,
        )

    path_check: dict[str, Any] | None = None
    if v == "PASS" and _looks_like_local_path(path_or_url):
        p = _path_from_claim(path_or_url)
        exists = p.exists()
        path_check = {"path": str(p), "exists": exists}
        if not exists:
            # Do not invent PASS â€” record FAIL and return err-shaped FAIL.
            row_fail = {
                "id": rid,
                "ts": _utc_now(),
                "event": "finish",
                "path_or_url": path_or_url,
                "proving_numbers": proving_numbers,
                "verdict": "FAIL",
                "status": "finished",
                "reason": "PASS rejected: local path does not exist",
                "path_check": path_check,
            }
            try:
                _append_jsonl(_receipt_path(rid), row_fail)
            except OSError as exc:
                return err(f"receipt_finish write failed: {exc}", path_check=path_check)
            return err(
                "PASS rejected: local path does not exist",
                ok=False,
                receipt_id=rid,
                verdict="FAIL",
                status="finished",
                path_check=path_check,
                path=str(_receipt_path(rid)),
            )

    row = {
        "id": rid,
        "ts": _utc_now(),
        "event": "finish",
        "path_or_url": path_or_url,
        "proving_numbers": proving_numbers,
        "verdict": v,
        "status": "finished",
    }
    if path_check is not None:
        row["path_check"] = path_check
    try:
        _append_jsonl(_receipt_path(rid), row)
    except OSError as exc:
        return err(f"receipt_finish write failed: {exc}")
    return dumps(
        {
            "ok": True,
            "receipt_id": rid,
            "path": str(_receipt_path(rid)),
            "verdict": v,
            "status": "finished",
            "path_check": path_check,
        }
    )


@mcp.tool()
def no_fake_done(
    claim_text: str,
    claimed_paths: str = "",
    receipt_id: str = "",
) -> str:
    """Gate done/finished/complete/shipped claims: ALLOW | FLAG | BLOCK."""
    paths = _parse_claimed_paths(claimed_paths)
    existing_paths = [p for p in paths if Path(p).exists()]
    any_path_exists = bool(existing_paths)

    receipt_pass = False
    receipt_state = "missing"
    rid = (receipt_id or "").strip()
    if rid:
        rec = _load_receipt(rid)
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

    return dumps(
        {
            "ok": True,
            "decision": decision,
            "reason": reason,
            "claimed_paths": paths,
            "existing_paths": existing_paths,
            "receipt_id": rid or None,
            "receipt_state": receipt_state,
            "has_done_claim": has_done_claim,
        }
    )


@mcp.tool()
def verify_done(claimed_path: str, receipt_id: str = "") -> str:
    """Verify claimed path exists and optional receipt is PASS. Result PASS only if both ok."""
    p = Path((claimed_path or "").strip())
    exists = p.exists() if str(p) else False

    rid = (receipt_id or "").strip()
    if not rid:
        receipt_state = "missing"
        receipt_required = False
        receipt_ok = True  # no receipt_id required
    else:
        receipt_required = True
        rec = _load_receipt(rid)
        if rec is None:
            receipt_state = "missing"
            receipt_ok = False
        else:
            verdict = str(rec.get("verdict") or "").upper()
            if verdict == "PASS":
                receipt_state = "PASS"
                receipt_ok = True
            elif verdict == "FAIL":
                receipt_state = "FAIL"
                receipt_ok = False
            else:
                receipt_state = "missing" if not verdict else verdict
                receipt_ok = False

    result = "PASS" if exists and receipt_ok else "FAIL"
    return dumps(
        {
            "ok": True,
            "claimed_path": str(p),
            "exists": "yes" if exists else "no",
            "receipt_id": rid or None,
            "receipt": receipt_state,
            "receipt_required": receipt_required,
            "result": result,
        }
    )


@mcp.tool()
def memory_pull(query: str, limit: int = 5) -> str:
    """Pull memory via local 8811 POST /api/dimensional (verified client shape)."""
    q = (query or "").strip()
    if not q:
        return err("query is required")
    lim = max(1, min(int(limit or 5), 50))

    # Prefer existing client helper on disk (grok-phone-mcp/dimensional_client.py).
    client_used = None
    result: dict[str, Any] | None = None
    try:
        gp = _AT / "8811-retrieval" / "grok-phone-mcp"
        if str(gp) not in sys.path:
            sys.path.insert(0, str(gp))
        from dimensional_client import dimensional  # type: ignore

        client_used = "dimensional_client.dimensional"
        # pre_hook is the documented first-call memory pull; search is shard recall.
        result = dimensional("pre_hook", {"query": q})
    except Exception as import_exc:  # noqa: BLE001
        # Fallback: same verified body as dimensional_client / mcp_http_fallback.
        try:
            result = _post_dimensional("pre_hook", {"query": q})
            client_used = "urllib:/api/dimensional"
        except Exception as post_exc:  # noqa: BLE001
            return err(
                "memory_pull blocked: could not call verified 8811 API",
                import_error=str(import_exc),
                post_error=str(post_exc),
                verified_shape={
                    "url": _DIMENSIONAL_URL,
                    "body": {"action": "pre_hook", "params": {"query": "<query>"}},
                    "source": "agent_tools/8811-retrieval/grok-phone-mcp/dimensional_client.py",
                },
            )

    assert result is not None
    # Truncate heavy lists client-side to honor limit without inventing API fields.
    trimmed = dict(result)
    for key in ("hits", "results", "notes", "items", "recall_candidates", "context_lines"):
        val = trimmed.get(key)
        if isinstance(val, list) and len(val) > lim:
            trimmed[key] = val[:lim]
            trimmed[f"{key}_truncated"] = True
    op = trimmed.get("operator_recall")
    if isinstance(op, dict):
        for key in ("hits", "results", "notes", "items", "candidates"):
            val = op.get(key)
            if isinstance(val, list) and len(val) > lim:
                op = dict(op)
                op[key] = val[:lim]
                op[f"{key}_truncated"] = True
                trimmed["operator_recall"] = op

    status = str(trimmed.get("status") or "").lower()
    # Be honest if transport error / API error
    if trimmed.get("code") == "transport_error" or status == "error":
        return dumps(
            {
                "ok": False,
                "error": trimmed.get("error") or "8811 memory_pull failed",
                "client": client_used,
                "url": _DIMENSIONAL_URL,
                "action": "pre_hook",
                "limit": lim,
                "result": trimmed,
            }
        )

    return dumps(
        {
            "ok": True,
            "client": client_used,
            "url": _DIMENSIONAL_URL,
            "action": "pre_hook",
            "query": q,
            "limit": lim,
            "result": trimmed,
        }
    )


@mcp.tool()
def freeze_on_lie(reason: str, claim_text: str = "") -> str:
    """Freeze on lie: write var/aegis/freeze.json; try babysitter set_freeze if available."""
    fp = _freeze_path()
    payload = {
        "schema_version": 1,
        "frozen": True,
        "reason": reason,
        "claim_text": claim_text or "",
        "ts": _utc_now(),
        "source": "aegis-mcp",
    }
    try:
        fp.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    except OSError as exc:
        return err(f"freeze write failed: {exc}")

    trust_note = "local aegis freeze.json written; trust-freeze-mcp is read-only"
    babysitter_ok = False
    babysitter_error = None
    try:
        hd = hooks_dir(repo_root())
        if str(hd) not in sys.path:
            sys.path.insert(0, str(hd))
        import babysitter_common as bc  # type: ignore

        if hasattr(bc, "set_freeze"):
            bc.set_freeze(
                reason=reason or "aegis freeze_on_lie",
                source="aegis-mcp",
                set_by="aegis-mcp",
            )
            babysitter_ok = True
            trust_note = (
                "local aegis freeze.json written; also called babysitter_common.set_freeze "
                "(operator-trust freeze.json)"
            )
        else:
            trust_note = (
                "local aegis freeze.json written; babysitter_common present but no set_freeze"
            )
    except Exception as exc:  # noqa: BLE001
        babysitter_error = str(exc)
        trust_note = (
            "local aegis freeze.json is enough â€” babysitter/trust write unavailable: "
            + str(exc)
        )

    return dumps(
        {
            "ok": True,
            "freeze_path": str(fp),
            "frozen": True,
            "reason": reason,
            "claim_text": claim_text or "",
            "babysitter_set_freeze": babysitter_ok,
            "babysitter_error": babysitter_error,
            "note": trust_note,
        }
    )


@mcp.tool()
def freeze_status() -> str:
    """Read var/aegis/freeze.json."""
    fp = _freeze_path()
    if not fp.is_file():
        return dumps(
            {
                "ok": True,
                "freeze_path": str(fp),
                "frozen": False,
                "freeze": None,
                "note": "no freeze.json yet",
            }
        )
    try:
        data = json.loads(fp.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return err(f"freeze_status read failed: {exc}", freeze_path=str(fp))
    if not isinstance(data, dict):
        data = {"raw": data}
    return dumps(
        {
            "ok": True,
            "freeze_path": str(fp),
            "frozen": bool(data.get("frozen")),
            "freeze": data,
        }
    )


if __name__ == "__main__":
    mcp.run()
