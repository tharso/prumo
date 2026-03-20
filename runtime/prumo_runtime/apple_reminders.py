from __future__ import annotations

import json
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

APPLE_REMINDERS_RELATIVE = "_state/apple-reminders-integration.json"


def now_iso(timezone_name: str) -> str:
    return datetime.now(ZoneInfo(timezone_name)).replace(microsecond=0).isoformat()


def raise_workspace_error(message: str) -> None:
    from prumo_runtime.workspace import WorkspaceError

    raise WorkspaceError(message)


def default_apple_reminders_payload() -> dict:
    return {
        "provider": "apple-reminders",
        "strategy": "applescript-local",
        "status": "disconnected",
        "authorization_status": "unknown",
        "last_authenticated_at": "",
        "last_refresh_at": "",
        "last_error": "",
        "lists": [],
    }


def render_apple_reminders_json() -> str:
    return json.dumps(default_apple_reminders_payload(), ensure_ascii=True, indent=2) + "\n"


def load_apple_reminders(workspace: Path) -> dict:
    target = workspace / APPLE_REMINDERS_RELATIVE
    if not target.exists():
        return default_apple_reminders_payload()
    try:
        payload = json.loads(target.read_text(encoding="utf-8"))
    except Exception:
        return default_apple_reminders_payload()
    default_payload = default_apple_reminders_payload()
    return {
        "provider": str(payload.get("provider") or default_payload["provider"]),
        "strategy": str(payload.get("strategy") or default_payload["strategy"]),
        "status": str(payload.get("status") or default_payload["status"]),
        "authorization_status": str(payload.get("authorization_status") or default_payload["authorization_status"]),
        "last_authenticated_at": str(payload.get("last_authenticated_at") or default_payload["last_authenticated_at"]),
        "last_refresh_at": str(payload.get("last_refresh_at") or default_payload["last_refresh_at"]),
        "last_error": str(payload.get("last_error") or default_payload["last_error"]),
        "lists": list(payload.get("lists") or default_payload["lists"]),
    }


def write_apple_reminders(workspace: Path, payload: dict) -> None:
    target = workspace / APPLE_REMINDERS_RELATIVE
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def update_apple_reminders_state(
    workspace: Path,
    *,
    status: str,
    authorization_status: str,
    timezone_name: str,
    lists: list[str] | None = None,
    last_error: str = "",
    authenticated: bool = False,
) -> dict:
    payload = load_apple_reminders(workspace)
    payload.update(
        {
            "strategy": "applescript-local",
            "status": status,
            "authorization_status": authorization_status,
            "last_refresh_at": now_iso(timezone_name),
            "last_error": last_error.strip(),
        }
    )
    if lists is not None:
        payload["lists"] = lists
    if authenticated:
        payload["last_authenticated_at"] = now_iso(timezone_name)
    write_apple_reminders(workspace, payload)
    return payload


def apple_reminders_summary(workspace: Path) -> dict:
    return load_apple_reminders(workspace)


def helper_script_path(workspace: Path) -> Path:
    del workspace
    return Path(__file__).resolve().parent / "helpers" / "apple_reminders.swift"


def applescript_helper_path(workspace: Path) -> Path:
    del workspace
    return Path(__file__).resolve().parent / "helpers" / "apple_reminders.applescript"


def parse_applescript_output(output: str) -> dict[str, Any]:
    status = "error"
    authorization_status = "unknown"
    lists: list[str] = []
    today: list[dict[str, str]] = []
    note = ""
    error = ""
    for raw_line in output.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("STATUS:"):
            status = line.split(":", 1)[1].strip() or status
        elif line.startswith("AUTHORIZATION:"):
            authorization_status = line.split(":", 1)[1].strip() or authorization_status
        elif line.startswith("LIST:"):
            item = line.split(":", 1)[1].strip()
            if item:
                lists.append(item)
        elif line.startswith("ITEM:"):
            display = line.split(":", 1)[1].strip()
            if display:
                today.append({"display": display})
        elif line.startswith("NOTE:"):
            note = line.split(":", 1)[1].strip()
        elif line.startswith("ERROR:"):
            error = line.split(":", 1)[1].strip()
    return {
        "status": status,
        "authorization_status": authorization_status,
        "lists": lists,
        "today": today,
        "note": note,
        "error": error,
    }


def run_applescript_helper(workspace: Path, action: str) -> dict[str, Any]:
    script = applescript_helper_path(workspace)
    if not script.exists():
        raise_workspace_error(f"helper Apple Reminders (AppleScript) ausente: {script}")
    try:
        completed = subprocess.run(
            ["osascript", str(script), action],
            capture_output=True,
            text=True,
            timeout=45,
            check=True,
        )
    except subprocess.TimeoutExpired:
        raise_workspace_error(
            "AppleScript de Reminders passou do limite; ou a permissao ficou pendurada, ou o macOS resolveu fazer ioga."
        )
    except subprocess.CalledProcessError as exc:
        stderr = (exc.stderr or exc.stdout or "").strip()
        raise_workspace_error(stderr or "AppleScript de Reminders falhou sem explicação decente")
    payload = parse_applescript_output(completed.stdout)
    if str(payload.get("status") or "") == "error":
        return payload
    if payload.get("authorization_status") == "unknown":
        payload["authorization_status"] = "authorized"
    return payload


def run_apple_reminders_helper(workspace: Path, action: str, timezone_name: str) -> dict[str, Any]:
    from prumo_runtime.workspace import WorkspaceError

    try:
        payload = run_applescript_helper(workspace, action)
        return payload
    except WorkspaceError as exc:
        message = str(exc)
        if "ausente" not in message and "not found" not in message.lower():
            raise

    script = helper_script_path(workspace)
    if not script.exists():
        raise_workspace_error(f"helper Apple Reminders ausente: {script}")
    try:
        completed = subprocess.run(
            ["swift", str(script), action, "--timezone", timezone_name],
            capture_output=True,
            text=True,
            timeout=30,
            check=True,
        )
    except subprocess.CalledProcessError as exc:
        stderr = (exc.stderr or exc.stdout or "").strip()
        raise_workspace_error(stderr or "helper Apple Reminders falhou sem explicação decente")
    except subprocess.TimeoutExpired as exc:
        raise_workspace_error("helper Apple Reminders passou do limite; a Apple também sabe se atrasar")
    try:
        payload = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise_workspace_error("helper Apple Reminders respondeu lixo onde devia haver JSON")
    if not isinstance(payload, dict):
        raise_workspace_error("helper Apple Reminders respondeu formato inválido")
    return payload


def auth_apple_reminders(workspace: Path, timezone_name: str) -> dict:
    payload = run_apple_reminders_helper(workspace, "auth", timezone_name)
    status = str(payload.get("status") or "error")
    auth_status = str(payload.get("authorization_status") or "unknown")
    lists = [str(item) for item in payload.get("lists", []) if str(item).strip()]
    last_error = str(payload.get("error") or "")
    return update_apple_reminders_state(
        workspace,
        status=status,
        authorization_status=auth_status,
        timezone_name=timezone_name,
        lists=lists,
        last_error=last_error,
        authenticated=status == "connected",
    )


def fetch_apple_reminders_today(workspace: Path, timezone_name: str) -> dict[str, Any]:
    payload = run_apple_reminders_helper(workspace, "fetch", timezone_name)
    status = str(payload.get("status") or "error")
    auth_status = str(payload.get("authorization_status") or "unknown")
    lists = [str(item) for item in payload.get("lists", []) if str(item).strip()]
    last_error = str(payload.get("error") or "")
    state = update_apple_reminders_state(
        workspace,
        status="connected" if status == "ok" else status,
        authorization_status=auth_status,
        timezone_name=timezone_name,
        lists=lists,
        last_error=last_error,
        authenticated=False,
    )
    items = payload.get("today", [])
    rendered = [str(item.get("display") or "").strip() for item in items if isinstance(item, dict) and str(item.get("display") or "").strip()]
    note = str(payload.get("note") or "").strip()
    return {
        "status": status,
        "authorization_status": auth_status,
        "lists": lists,
        "items": rendered,
        "raw_items": items if isinstance(items, list) else [],
        "note": note,
        "state": state,
    }
