from __future__ import annotations

import os
from pathlib import Path

from prumo_runtime.workspace import extract_section, read_text, load_json


DEFAULT_GOOGLE_CLIENT_SECRETS = Path("~/Documents/_secrets/prumo/google-oauth-client.json").expanduser()


def shell_action(
    action_id: str,
    label: str,
    shell_command: str,
    *,
    category: str,
    documentation_targets: list[str] | None = None,
    outcome: str | None = None,
) -> dict[str, object]:
    payload: dict[str, object] = {
        "id": action_id,
        "label": label,
        "kind": "shell",
        "category": category,
        "command": shell_command,
        "shell_command": shell_command,
    }
    if documentation_targets:
        payload["documentation_targets"] = documentation_targets
    if outcome:
        payload["outcome"] = outcome
    return payload


def host_prompt_action(
    action_id: str,
    label: str,
    host_prompt: str,
    *,
    category: str,
    documentation_targets: list[str] | None = None,
    outcome: str | None = None,
) -> dict[str, object]:
    payload: dict[str, object] = {
        "id": action_id,
        "label": label,
        "kind": "host-prompt",
        "category": category,
        "command": host_prompt,
        "host_prompt": host_prompt,
    }
    if documentation_targets:
        payload["documentation_targets"] = documentation_targets
    if outcome:
        payload["outcome"] = outcome
    return payload


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


def documentation_targets(workspace: Path) -> dict[str, str]:
    return {
        "pauta": str((workspace / "PAUTA.md").resolve()),
        "inbox": str((workspace / "INBOX.md").resolve()),
        "registro": str((workspace / "REGISTRO.md").resolve()),
        "workflow_registry": str((workspace / "Referencias" / "WORKFLOWS.md").resolve()),
    }


def count_markdown_items(markdown: str) -> int:
    count = 0
    for raw_line in markdown.splitlines():
        stripped = raw_line.strip()
        if not stripped or stripped.startswith(">") or stripped.startswith("_"):
            continue
        if stripped.startswith(("- ", "* ")):
            count += 1
        elif len(stripped) >= 4 and stripped[:2].isdigit() and stripped[2:4] == ". ":
            count += 1
    return count


def inbox_item_count(workspace: Path) -> int:
    preview_payload = load_json(workspace / "Inbox4Mobile" / "_preview-index.json")
    preview_items = preview_payload.get("items")
    if isinstance(preview_items, list) and preview_items:
        return len(preview_items)
    return count_markdown_items(read_text(workspace / "INBOX.md"))


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
    docs = documentation_targets(workspace)
    return {
        "mode": "daily-operator",
        "supports": [
            "briefing",
            "continuation",
            "inbox-triage",
            "documentation",
            "workflow-scaffolding",
        ],
        "documentation_targets": list(docs.values())[:3],
        "workflow_registry_path": docs["workflow_registry"],
        "documentation_contract": {
            "update_pauta": docs["pauta"],
            "update_inbox": docs["inbox"],
            "append_registro": docs["registro"],
            "register_workflows": docs["workflow_registry"],
        },
        "quality_bar": {
            "briefing_is_not_enough": True,
            "must_support_continuation": True,
            "must_leave_useful_documentation": True,
        },
    }


def build_daily_actions(
    workspace: Path,
    overview: dict,
    *,
    has_briefed_today: bool,
) -> list[dict[str, object]]:
    workspace_str = str(workspace)
    missing = overview["missing"]
    continue_item = clean_pauta_item(choose_continue_item(workspace))
    google_connected = overview["google_integration"]["active_profile_status"] == "connected"
    docs = documentation_targets(workspace)
    inbox_count = inbox_item_count(workspace)

    actions: list[dict[str, object]] = []
    if missing["generated"] or missing["derived"]:
        actions.append(
            shell_action(
                "repair",
                "Consertar a estrutura antes de brincar de produtividade",
                f"prumo repair --workspace {workspace_str}",
                category="repair",
                documentation_targets=[docs["pauta"], docs["inbox"], docs["registro"]],
                outcome="Workspace consistente o bastante para o Prumo não tropeçar na própria sandália.",
            )
        )

    actions.append(
        shell_action(
            "briefing",
            "Rodar o briefing agora" if not has_briefed_today else "Rodar o briefing de novo",
            f"prumo briefing --workspace {workspace_str} --refresh-snapshot",
            category="briefing",
            documentation_targets=[docs["pauta"], docs["inbox"], docs["registro"]],
            outcome="Panorama atualizado com proposta do dia e contexto suficiente para seguir trabalhando.",
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
                    f"em `{docs['pauta']}` e `{docs['registro']}` sem inventar contexto."
                ),
                category="continuation",
                documentation_targets=[docs["pauta"], docs["registro"]],
                outcome="Trabalho retomado com próximos passos e decisão registrada em documentação viva.",
            )
        )

    if inbox_count:
        actions.append(
            host_prompt_action(
                "process-inbox",
                f"Processar a fila que está encostada ({inbox_count} item(ns))",
                (
                    f"Processe a fila atual do workspace. Triague itens de `{docs['inbox']}` "
                    "e, se houver preview de Inbox4Mobile, use isso para priorizar. "
                    f"Atualize `{docs['pauta']}` com próximos passos, limpe o que for resolvido de `{docs['inbox']}` "
                    f"e registre decisões em `{docs['registro']}`."
                ),
                category="inbox-triage",
                documentation_targets=[docs["pauta"], docs["inbox"], docs["registro"]],
                outcome="Inbox menor, pauta mais clara e rastro do que foi decidido.",
            )
        )

    actions.append(
        host_prompt_action(
            "organize-day",
            "Organizar o dia e a documentação viva",
            (
                f"Organize o dia a partir de `{docs['pauta']}`, `{docs['inbox']}` e `{docs['registro']}`. "
                "Atualize próximos passos, pendências, decisões e pontos de bloqueio sem inventar contexto."
            ),
            category="documentation",
            documentation_targets=[docs["pauta"], docs["inbox"], docs["registro"]],
            outcome="Workspace mais respirável, com pendências, decisões e foco do dia explicitados.",
        )
    )

    if not google_connected:
        actions.append(suggest_google_auth_action(workspace))

    actions.append(
        host_prompt_action(
            "workflow-scaffold",
            "Preparar candidatos a workflow sem fechar nada à força",
            (
                f"Revise o trabalho atual e registre em `{docs['workflow_registry']}` padrões repetíveis, gatilhos, "
                "documentação necessária e pontos de proatividade que pareçam bons candidatos a workflow do Prumo. "
                "Não transforme isso em workflow fechado ainda."
            ),
            category="workflow-scaffolding",
            documentation_targets=[docs["workflow_registry"], docs["registro"]],
            outcome="Candidatos a workflow registrados sem vender promessa de automação antes da hora.",
        )
    )

    actions.append(
        shell_action(
            "context",
            "Ver o estado técnico sem poesia",
            f"prumo context-dump --workspace {workspace_str} --format json",
            category="diagnostics",
            documentation_targets=[docs["pauta"], docs["inbox"], docs["registro"]],
            outcome="Estado técnico explícito para host ou diagnóstico humano sem telepatia.",
        )
    )

    ordered: list[dict[str, object]] = []
    seen: set[str] = set()
    for action in actions:
        if action["id"] in seen:
            continue
        ordered.append(action)
        seen.add(action["id"])
    return ordered[:8]
