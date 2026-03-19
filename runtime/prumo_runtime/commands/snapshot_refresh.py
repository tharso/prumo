from __future__ import annotations

import json
import os
from contextlib import contextmanager
from pathlib import Path

from prumo_runtime.commands.briefing import resolve_snapshot_data, snapshot_cache_path
from prumo_runtime.constants import repo_root_from
from prumo_runtime.workspace import build_config_from_existing


@contextmanager
def temporary_env(key: str, value: str):
    previous = os.environ.get(key)
    os.environ[key] = value
    try:
        yield
    finally:
        if previous is None:
            os.environ.pop(key, None)
        else:
            os.environ[key] = previous


def run_snapshot_refresh(args) -> int:
    workspace = Path(args.workspace).expanduser().resolve()
    build_config_from_existing(workspace)
    repo_root = repo_root_from(Path(__file__))
    if getattr(args, "profile", None):
        with temporary_env("PRUMO_GEMINI_PROFILES", args.profile):
            snapshot = resolve_snapshot_data(workspace, repo_root, refresh_snapshot=True)
    else:
        snapshot = resolve_snapshot_data(workspace, repo_root, refresh_snapshot=True)

    if args.format == "json":
        print(json.dumps(snapshot, ensure_ascii=True, indent=2))
        return 0

    print(f"Snapshot refresh: {workspace}")
    print(f"- status: {snapshot.get('status', 'desconhecido')}")
    print(f"- nota: {snapshot.get('note', 'sem observacao')}")
    print(f"- perfis ok: {snapshot.get('ok_profiles', 0)}")
    print(f"- cache: {snapshot_cache_path(workspace)}")
    for profile_name, profile in snapshot.get("profiles", {}).items():
        status = profile.get("status", "unknown")
        account = profile.get("account", "desconhecido")
        emails_total = profile.get("emails_total", 0)
        today = len(profile.get("agenda_today", []))
        print(
            f"  - {profile_name}: {status} | conta={account} | agenda_hoje={today} | emails={emails_total}"
        )
    return 0
