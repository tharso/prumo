from __future__ import annotations

from pathlib import Path

from prumo_runtime.apple_reminders import load_apple_reminders, set_observed_apple_reminders_lists
from prumo_runtime.workspace import build_config_from_existing


def render_visible_lists(payload: dict) -> str:
    lists = [str(item).strip() for item in payload.get("lists") or [] if str(item).strip()]
    if not lists:
        return "nenhuma lista visível ainda"
    return ", ".join(lists[:10]) + (" ..." if len(lists) > 10 else "")


def render_observed_lists(payload: dict) -> str:
    observed = [str(item).strip() for item in payload.get("observed_lists") or [] if str(item).strip()]
    if not observed:
        return "todas"
    return ", ".join(observed)


def run_config_apple_reminders(args) -> int:
    workspace = Path(args.workspace).expanduser().resolve()
    config = build_config_from_existing(workspace)

    requested_lists = [str(item).strip() for item in (getattr(args, "observe_lists", None) or []) if str(item).strip()]
    clear_all = bool(getattr(args, "all_lists", False))

    if clear_all:
        payload = set_observed_apple_reminders_lists(workspace, config.timezone_name, [])
        print("Apple Reminders reconfigurado.")
        print(f"- Workspace: {workspace}")
        print("- Listas observadas: todas")
        print(f"- Listas visíveis: {render_visible_lists(payload)}")
        return 0

    if requested_lists:
        payload = set_observed_apple_reminders_lists(workspace, config.timezone_name, requested_lists)
        print("Apple Reminders reconfigurado.")
        print(f"- Workspace: {workspace}")
        print(f"- Listas observadas: {render_observed_lists(payload)}")
        print(f"- Listas visíveis: {render_visible_lists(payload)}")
        return 0

    payload = load_apple_reminders(workspace)
    print("Apple Reminders configurado assim:")
    print(f"- Workspace: {workspace}")
    print(f"- Status: {payload.get('status') or 'desconhecido'}")
    print(f"- Strategy: {payload.get('strategy') or 'desconhecida'}")
    print(f"- Listas observadas: {render_observed_lists(payload)}")
    print(f"- Listas visíveis: {render_visible_lists(payload)}")
    print("Se quiser afunilar, use `prumo config apple-reminders --workspace ... --list \"A vida...\"`.")
    print("Se quiser voltar a observar tudo, use `prumo config apple-reminders --workspace ... --all`.")
    return 0
