from __future__ import annotations

import os
from pathlib import Path

from prumo_runtime.workspace import extract_section, read_text, load_json


DEFAULT_GOOGLE_CLIENT_SECRETS = Path("~/Documents/_secrets/prumo/google-oauth-client.json").expanduser()


def shell_action(action_id: str, label: str, shell_command: str, *, category: str) -> dict[str, str]:
    return {
        "id": action_id,
        "label": label,
        "kind": "shell",
        "category": category,
        "command": shell_command,
        "shell_command": shell_command,
    }


def host_prompt_action(action_id: str, label: str, host_prompt: str, *, category: str) -> dict[str, str]:
    return {
        "id": action_id,
        "label": label,
        "kind": "host-prompt",
        "category": category,
        "command": host_prompt,
        "host_prompt": host_prompt,
    }


def pauta_candidates(workspace: Path) -> tuple[list[str], list[str]]:
    pauta = read_text(workspace / "PAUTA.md")
    hot = extract_section(pauta, "Quente (precisa de atenção agora)")
    ongoing = extract_section(pauta, "Em andamento")
    clean_hot = [item for item in hot if "_Nada ainda._" not in item and "Nada ainda." not in item]
    clean_ongoing = [item for item in ongoing if "_Nada ainda._" not in item and "Nada ainda." not in item]
    return clean_hot, clean_ongoing


def clean_pauta_item(value: str | None) -> str:
    text = str(value or "").strip()
    if text.startswith("- "):
        text = text[2:].strip()
    return text


def choose_continue_item(workspace: Path) -> str | None:
    hot, ongoing = pauta_candidates(workspace)
    if hot:
        return hot[0]
    if ongoing:
        return ongoing[0]
    return None


def suggest_google_auth_action(workspace: Path) -> dict[str, str]:
    workspace_str = str(workspace)
    client_secrets_env = str(os.environ.get("PRUMO_GOOGLE_CLIENT_SECRETS") or "").strip()
    client_id = str(os.environ.get("PRUMO_GOOGLE_CLIENT_ID") or "").strip()
    client_secret = str(os.environ.get("PRUMO_GOOGLE_CLIENT_SECRET") or "").strip()
    if client_secrets_env:
        candidate = Path(client_secrets_env).expanduser()
        if candidate.exists():
            return shell_action(
                "auth-google",
                "Conectar Google",
                f"prumo auth google --workspace {workspace_str} --client-secrets {candidate}",
                category="integration",
            )
    if DEFAULT_GOOGLE_CLIENT_SECRETS.exists():
        return shell_action(
            "auth-google",
            "Conectar Google",
            f"prumo auth google --workspace {workspace_str} --client-secrets {DEFAULT_GOOGLE_CLIENT_SECRETS}",
            category="integration",
        )
    if client_id and client_secret:
        return shell_action(
            "auth-google",
            "Conectar Google",
            (
                f'prumo auth google --workspace {workspace_str} --client-id "{client_id}" '
                f'--client-secret "{client_secret}"'
            ),
            category="integration",
        )
    return shell_action(
        "auth-google-help",
        "Ver como conectar Google sem chute cego",
        f"prumo auth google --workspace {workspace_str} --help",
        category="integration",
    )


def daily_operation_payload(workspace: Path) -> dict[str, object]:
    registry = workspace / "Referencias" / "WORKFLOWS.md"
    return {
        "mode": "daily-operator",
        "supports": [
            "briefing",
            "continuation",
            "documentation",
            "workflow-scaffolding",
        ],
        "documentation_targets": [
            str((workspace / "PAUTA.md").resolve()),
            str((workspace / "INBOX.md").resolve()),
            str((workspace / "REGISTRO.md").resolve()),
        ],
        "workflow_registry_path": str(registry.resolve()),
    }


def build_daily_actions(
    workspace: Path,
    overview: dict,
    *,
    has_briefed_today: bool,
) -> list[dict[str, str]]:
    workspace_str = str(workspace)
    missing = overview["missing"]
    continue_item = clean_pauta_item(choose_continue_item(workspace))
    google_connected = overview["google_integration"]["active_profile_status"] == "connected"

    actions: list[dict[str, str]] = []
    if missing["generated"] or missing["derived"]:
        actions.append(
            shell_action(
                "repair",
                "Consertar a estrutura antes de brincar de produtividade",
                f"prumo repair --workspace {workspace_str}",
                category="repair",
            )
        )

    actions.append(
        shell_action(
            "briefing",
            "Rodar o briefing agora" if not has_briefed_today else "Rodar o briefing de novo",
            f"prumo briefing --workspace {workspace_str} --refresh-snapshot",
            category="briefing",
        )
    )

    if continue_item:
        actions.append(
            host_prompt_action(
                "continue",
                f"Retomar o que já estava quente: {continue_item}",
                (
                    "Continue pelo item da pauta: "
                    f"{continue_item}. Enquanto avança, registre decisões, próximos passos e pendências "
                    "na documentação viva do workspace sem inventar contexto."
                ),
                category="continuation",
            )
        )

    actions.append(
        host_prompt_action(
            "organize-day",
            "Organizar o dia e a documentação viva",
            (
                "Organize o dia a partir de PAUTA.md, INBOX.md e REGISTRO.md. "
                "Atualize a documentação viva com próximos passos, pendências e decisões, sem inventar contexto."
            ),
            category="documentation",
        )
    )

    if not google_connected:
        actions.append(suggest_google_auth_action(workspace))

    actions.append(
        host_prompt_action(
            "workflow-scaffold",
            "Preparar candidatos a workflow sem fechar nada à força",
            (
                "Revise o trabalho atual e registre em Referencias/WORKFLOWS.md padrões repetíveis, gatilhos, "
                "documentação necessária e pontos de proatividade que pareçam bons candidatos a workflow do Prumo. "
                "Não transforme isso em workflow fechado ainda."
            ),
            category="workflow-scaffolding",
        )
    )

    actions.append(
        shell_action(
            "context",
            "Ver o estado técnico sem poesia",
            f"prumo context-dump --workspace {workspace_str} --format json",
            category="diagnostics",
        )
    )

    ordered: list[dict[str, str]] = []
    seen: set[str] = set()
    for action in actions:
        if action["id"] in seen:
            continue
        ordered.append(action)
        seen.add(action["id"])
    return ordered[:7]
