from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from prumo_runtime.workspace import (
    WorkspaceError,
    extract_section,
    load_json,
    read_text,
    workspace_overview,
)


def _parse_iso(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return None


def _same_local_day(value: str | None, timezone_name: str) -> bool:
    dt_value = _parse_iso(value)
    if dt_value is None:
        return False
    now = datetime.now(ZoneInfo(timezone_name))
    return dt_value.astimezone(ZoneInfo(timezone_name)).date() == now.date()


def _short_clock(value: str | None, timezone_name: str) -> str | None:
    dt_value = _parse_iso(value)
    if dt_value is None:
        return None
    return dt_value.astimezone(ZoneInfo(timezone_name)).strftime("%H:%M")


def _looks_legacy(workspace: Path) -> bool:
    return any(
        (workspace / relative).exists()
        for relative in ("CLAUDE.md", "PRUMO-CORE.md", "PAUTA.md", "INBOX.md", "REGISTRO.md")
    )


def _pauta_candidates(workspace: Path) -> tuple[list[str], list[str]]:
    pauta = read_text(workspace / "PAUTA.md")
    hot = extract_section(pauta, "Quente (precisa de atenção agora)")
    ongoing = extract_section(pauta, "Em andamento")
    clean_hot = [item for item in hot if "_Nada ainda._" not in item and "Nada ainda." not in item]
    clean_ongoing = [item for item in ongoing if "_Nada ainda._" not in item and "Nada ainda." not in item]
    return clean_hot, clean_ongoing


def _clean_pauta_item(value: str | None) -> str:
    text = str(value or "").strip()
    if text.startswith("- "):
        text = text[2:].strip()
    return text


def _choose_continue_item(workspace: Path) -> str | None:
    hot, ongoing = _pauta_candidates(workspace)
    if hot:
        return hot[0]
    if ongoing:
        return ongoing[0]
    return None


def _build_actions(workspace: Path, overview: dict) -> list[dict[str, str]]:
    workspace_str = str(workspace)
    missing = overview["missing"]
    briefing_state = load_json(workspace / "_state" / "briefing-state.json")
    last_briefing_at = str(briefing_state.get("last_briefing_at") or "").strip()
    has_briefed_today = _same_local_day(last_briefing_at, overview["timezone"])
    continue_item = _clean_pauta_item(_choose_continue_item(workspace))
    google_connected = overview["google_integration"]["active_profile_status"] == "connected"
    apple_connected = overview["apple_reminders"]["status"] == "connected"

    actions: list[dict[str, str]] = []
    if missing["generated"] or missing["derived"]:
        actions.append(
            {
                "id": "repair",
                "label": "Consertar a estrutura antes de brincar de produtividade",
                "command": f"prumo repair --workspace {workspace_str}",
            }
        )

    actions.append(
        {
            "id": "briefing",
            "label": "Rodar o briefing agora" if not has_briefed_today else "Rodar o briefing de novo",
            "command": f"prumo briefing --workspace {workspace_str} --refresh-snapshot",
        }
    )

    if continue_item:
        actions.append(
            {
                "id": "continue",
                "label": f"Retomar o que já estava quente: {continue_item}",
                "command": f"Continue pelo item da pauta: {continue_item}",
            }
        )

    if not google_connected:
        actions.append(
            {
                "id": "auth-google",
                "label": "Conectar Google",
                "command": f"prumo auth google --workspace {workspace_str} --client-secrets /caminho/do/client_secret.json",
            }
        )

    if not apple_connected:
        actions.append(
            {
                "id": "auth-apple-reminders",
                "label": "Conectar Apple Reminders",
                "command": f"prumo auth apple-reminders --workspace {workspace_str}",
            }
        )

    actions.append(
        {
            "id": "context",
            "label": "Ver o estado técnico sem poesia",
            "command": f"prumo context-dump --workspace {workspace_str} --format json",
        }
    )

    ordered: list[dict[str, str]] = []
    seen: set[str] = set()
    for action in actions:
        if action["id"] in seen:
            continue
        ordered.append(action)
        seen.add(action["id"])
    return ordered[:4]


def _render_text_for_missing_workspace(workspace: Path) -> str:
    workspace_str = str(workspace)
    return "\n".join(
        [
            f"1. Não achei o workspace `{workspace_str}`.",
            "2. Então não faz sentido fingir briefing. Primeiro precisamos de chão.",
            "3. Minha sugestão: criar o workspace com `prumo setup`.",
            "a) Rodar `prumo setup --workspace "
            f"{workspace_str}`",
            "b) Escolher outro caminho de workspace",
        ]
    )


def _render_text_for_legacy_workspace(workspace: Path) -> str:
    workspace_str = str(workspace)
    return "\n".join(
        [
            f"1. Achei um workspace em `{workspace_str}`, mas ele ainda não tem identidade canônica do runtime.",
            "2. Em português simples: parece casa antiga. Não é caso de `setup`; é caso de `migrate`.",
            "3. Minha sugestão: adotar o workspace legado antes de pedir briefing.",
            f"a) Rodar `prumo migrate --workspace {workspace_str}`",
            f"b) Ver estado cru com `prumo context-dump --workspace {workspace_str} --format json`",
        ]
    )


def _render_start_text(workspace: Path, overview: dict) -> str:
    timezone_name = overview["timezone"]
    missing = overview["missing"]
    google = overview["google_integration"]
    apple = overview["apple_reminders"]
    briefing_state = load_json(workspace / "_state" / "briefing-state.json")
    last_briefing_at = str(briefing_state.get("last_briefing_at") or "").strip()
    has_briefed_today = _same_local_day(last_briefing_at, timezone_name)
    last_briefing_clock = _short_clock(last_briefing_at, timezone_name)
    actions = _build_actions(workspace, overview)

    if missing["generated"] or missing["derived"]:
        suggestion = "consertar a estrutura antes de brincar de produtividade."
    elif not has_briefed_today:
        suggestion = "rodar o briefing agora."
    elif _choose_continue_item(workspace):
        suggestion = "retomar a frente mais quente em vez de pedir outro mapa da cidade."
    else:
        suggestion = "rodar o briefing de novo ou abrir o contexto técnico, porque o terreno parece relativamente calmo."

    lines = [
        f"1. {overview['user_name']}, o Prumo está de pé no workspace `{workspace}`.",
        (
            "2. Estado rápido: "
            f"Google `{google['active_profile_status']}`, "
            f"Apple Reminders `{apple['status']}`, "
            f"core `{overview['core_version'] or 'ausente'}`."
        ),
    ]

    if missing["generated"] or missing["derived"] or missing["authorial"]:
        missing_parts: list[str] = []
        if missing["generated"] or missing["derived"]:
            missing_parts.append(
                f"faltam arquivos recriáveis ({len(missing['generated']) + len(missing['derived'])})"
            )
        if missing["authorial"]:
            missing_parts.append(f"faltam arquivos autorais ({len(missing['authorial'])})")
        lines.append("3. O workspace não está 100% inteiro: " + "; ".join(missing_parts) + ".")
        suggestion_index = 4
    else:
        if has_briefed_today and last_briefing_clock:
            lines.append(f"3. Você já passou pelo briefing hoje, às {last_briefing_clock}.")
        else:
            lines.append("3. Ainda não há briefing registrado hoje neste workspace.")
        suggestion_index = 4

    lines.append(f"{suggestion_index}. Minha sugestão: {suggestion}")

    option_labels = ["a", "b", "c", "d"]
    for label, action in zip(option_labels, actions):
        lines.append(f"{label}) {action['label']}")
        lines.append(f"   `{action['command']}`")

    return "\n".join(lines)


def run_start(args) -> int:
    workspace = Path(args.workspace).expanduser().resolve()
    if not workspace.exists():
        print(_render_text_for_missing_workspace(workspace))
        return 0
    if not workspace.is_dir():
        raise WorkspaceError(f"workspace não é diretório: {workspace}")

    try:
        overview = workspace_overview(workspace)
    except WorkspaceError:
        if _looks_legacy(workspace):
            print(_render_text_for_legacy_workspace(workspace))
            return 0
        raise

    payload = {
        "workspace_path": str(workspace),
        "user_name": overview["user_name"],
        "runtime_version": overview["runtime_version"],
        "core_version": overview["core_version"],
        "google_status": overview["google_integration"]["active_profile_status"],
        "apple_reminders_status": overview["apple_reminders"]["status"],
        "missing": overview["missing"],
        "actions": _build_actions(workspace, overview),
        "message": _render_start_text(workspace, overview),
    }

    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=True, indent=2))
        return 0

    print(payload["message"])
    return 0
