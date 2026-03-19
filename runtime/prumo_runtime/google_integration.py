from __future__ import annotations

import hashlib
import json
import os
import platform
import subprocess
from pathlib import Path

GOOGLE_INTEGRATION_RELATIVE = "_state/google-integration.json"
DEFAULT_GOOGLE_PROFILE = "pessoal"
DEFAULT_GOOGLE_SCOPES = (
    "openid",
    "email",
    "https://www.googleapis.com/auth/calendar.readonly",
    "https://www.googleapis.com/auth/gmail.readonly",
)
KEYCHAIN_SERVICE_PREFIX = "me.prumo.google.oauth"


def keychain_supported() -> bool:
    return platform.system() == "Darwin"


def keychain_service_name() -> str:
    prefix = os.environ.get("PRUMO_GOOGLE_KEYCHAIN_SERVICE_PREFIX", KEYCHAIN_SERVICE_PREFIX).strip()
    return prefix or KEYCHAIN_SERVICE_PREFIX


def keychain_account_name(workspace: Path, profile: str) -> str:
    digest = hashlib.sha256(str(workspace.resolve()).encode("utf-8")).hexdigest()[:16]
    return f"{digest}:{profile}"


def default_profile_state(workspace: Path, profile: str = DEFAULT_GOOGLE_PROFILE) -> dict:
    return {
        "label": "Conta pessoal" if profile == "pessoal" else f"Conta {profile}",
        "status": "disconnected",
        "account_email": "",
        "scopes": list(DEFAULT_GOOGLE_SCOPES),
        "last_authenticated_at": "",
        "last_refresh_at": "",
        "source": "browser-oauth",
        "token_storage": {
            "type": "macos-keychain" if keychain_supported() else "unsupported",
            "service": keychain_service_name(),
            "account": keychain_account_name(workspace, profile),
        },
    }


def default_google_integration_payload(workspace: Path) -> dict:
    return {
        "provider": "google",
        "strategy": "direct-google-api",
        "status": "disconnected",
        "active_profile": DEFAULT_GOOGLE_PROFILE,
        "profiles": {
            DEFAULT_GOOGLE_PROFILE: default_profile_state(workspace, DEFAULT_GOOGLE_PROFILE),
        },
    }


def render_google_integration_json(workspace: Path) -> str:
    return json.dumps(default_google_integration_payload(workspace), ensure_ascii=True, indent=2) + "\n"


def load_google_integration(workspace: Path) -> dict:
    target = workspace / GOOGLE_INTEGRATION_RELATIVE
    if not target.exists():
        return default_google_integration_payload(workspace)
    try:
        payload = json.loads(target.read_text(encoding="utf-8"))
    except Exception:
        return default_google_integration_payload(workspace)

    default_payload = default_google_integration_payload(workspace)
    profiles = payload.get("profiles") if isinstance(payload.get("profiles"), dict) else {}
    merged_profiles = dict(default_payload["profiles"])
    for name, profile_payload in profiles.items():
        base = default_profile_state(workspace, name)
        if isinstance(profile_payload, dict):
            merged = {**base, **profile_payload}
            token_storage = {**base["token_storage"], **(profile_payload.get("token_storage") or {})}
            merged["token_storage"] = token_storage
            merged_profiles[name] = merged

    return {
        "provider": str(payload.get("provider") or default_payload["provider"]),
        "strategy": str(payload.get("strategy") or default_payload["strategy"]),
        "status": str(payload.get("status") or default_payload["status"]),
        "active_profile": str(payload.get("active_profile") or default_payload["active_profile"]),
        "profiles": merged_profiles,
    }


def write_google_integration(workspace: Path, payload: dict) -> None:
    target = workspace / GOOGLE_INTEGRATION_RELATIVE
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def update_profile_state(
    workspace: Path,
    profile: str,
    *,
    status: str,
    account_email: str = "",
    scopes: list[str] | None = None,
    last_authenticated_at: str = "",
    last_refresh_at: str = "",
) -> dict:
    payload = load_google_integration(workspace)
    profile_payload = payload["profiles"].get(profile, default_profile_state(workspace, profile))
    profile_payload.update(
        {
            "status": status,
            "account_email": account_email,
            "scopes": scopes or profile_payload.get("scopes") or list(DEFAULT_GOOGLE_SCOPES),
            "last_authenticated_at": last_authenticated_at or profile_payload.get("last_authenticated_at", ""),
            "last_refresh_at": last_refresh_at or profile_payload.get("last_refresh_at", ""),
            "source": "browser-oauth",
        }
    )
    payload["profiles"][profile] = profile_payload
    payload["active_profile"] = profile
    payload["status"] = "connected" if any(
        item.get("status") == "connected" for item in payload["profiles"].values()
    ) else status
    write_google_integration(workspace, payload)
    return payload


def google_integration_summary(workspace: Path) -> dict:
    payload = load_google_integration(workspace)
    profiles = payload.get("profiles") or {}
    connected_profiles = [
        name
        for name, profile_payload in profiles.items()
        if isinstance(profile_payload, dict) and profile_payload.get("status") == "connected"
    ]
    return {
        "provider": payload.get("provider", "google"),
        "strategy": payload.get("strategy", "direct-google-api"),
        "status": payload.get("status", "disconnected"),
        "active_profile": payload.get("active_profile", DEFAULT_GOOGLE_PROFILE),
        "connected_profiles": connected_profiles,
        "profiles": profiles,
        "token_storage_supported": keychain_supported(),
    }


def store_token_in_keychain(workspace: Path, profile: str, secret: str) -> dict:
    if not keychain_supported():
        raise RuntimeError("token storage seguro no runtime ainda so esta implementado no macOS")
    service = keychain_service_name()
    account = keychain_account_name(workspace, profile)
    command = [
        "security",
        "add-generic-password",
        "-a",
        account,
        "-s",
        service,
        "-w",
        secret,
        "-U",
    ]
    try:
        completed = subprocess.run(command, capture_output=True, text=True)
    except FileNotFoundError as exc:
        raise RuntimeError("comando `security` indisponivel; sem isso o Keychain nao entra em cena") from exc
    if completed.returncode != 0:
        stderr = (completed.stderr or completed.stdout or "").strip()
        raise RuntimeError(stderr or "nao foi possivel gravar token no Keychain")
    return {"type": "macos-keychain", "service": service, "account": account}
