from __future__ import annotations

import json
import os
from contextlib import contextmanager
from pathlib import Path

from prumo_runtime.commands.briefing import (
    infer_timezone_name,
    resolve_snapshot_data,
    snapshot_cache_path,
    write_snapshot_cache,
)
from prumo_runtime.constants import repo_root_from
from prumo_runtime.workspace import build_config_from_existing


PROFILE_NAMES = ("pessoal", "trabalho")


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


def try_profile_rescue(workspace: Path, repo_root: Path) -> dict | None:
    merged_profiles: dict[str, dict] = {}
    notes: list[str] = []

    for profile_name in PROFILE_NAMES:
        with temporary_env("PRUMO_GEMINI_PROFILES", profile_name):
            snapshot = resolve_snapshot_data(workspace, repo_root, refresh_snapshot=True)
        if snapshot.get("note"):
            notes.append(f"{profile_name}: {snapshot['note']}")
        if snapshot.get("ok_profiles", 0) == 0:
            continue
        merged_profiles.update(snapshot.get("profiles", {}))

    if not merged_profiles:
        return None

    rescued = {
        "status": "partial",
        "note": "refresh conjunto falhou; usei o que deu para salvar por perfil. " + " ".join(notes).strip(),
        "ok_profiles": sum(
            1
            for profile in merged_profiles.values()
            if str(profile.get("status", "")).startswith(("OK", "AVISO"))
        ),
        "profiles": merged_profiles,
    }
    write_snapshot_cache(workspace, infer_timezone_name(workspace), rescued)
    return rescued


def run_snapshot_refresh(args) -> int:
    workspace = Path(args.workspace).expanduser().resolve()
    build_config_from_existing(workspace)
    repo_root = repo_root_from(Path(__file__))
    snapshot = resolve_snapshot_data(workspace, repo_root, refresh_snapshot=True)
    if snapshot.get("ok_profiles", 0) == 0 and snapshot.get("status") in {"timeout", "error", "empty"}:
        rescued = try_profile_rescue(workspace, repo_root)
        if rescued is not None:
            snapshot = rescued

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
