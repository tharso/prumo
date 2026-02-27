#!/usr/bin/env python3
"""Sanitiza estado operacional do Prumo sem perder historico.

Escopo atual:
- Compacta `_state/HANDOVER.md` (arquiva fechados antigos)
- Gera `_state/HANDOVER.summary.md` para leitura leve no briefing
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
from dataclasses import dataclass
from pathlib import Path

ID_RE = re.compile(r"^###\s+ID:\s*(.+)$", re.MULTILINE)
STATUS_RE = re.compile(r"^-\s+Status:\s*([A-Z_]+)", re.MULTILINE)
DATE_RE = re.compile(r"^-\s+Data:\s*(.+)$", re.MULTILINE)
FROM_RE = re.compile(r"^-\s+De:\s*(.+)$", re.MULTILINE)
TO_RE = re.compile(r"^-\s+Para:\s*(.+)$", re.MULTILINE)


@dataclass
class Section:
    raw: str
    ident: str
    status: str
    date: str
    owner_from: str
    owner_to: str


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Sanitiza estado operacional do Prumo.")
    p.add_argument("--workspace", default=".", help="Workspace raiz (default: .)")
    p.add_argument(
        "--keep-closed",
        type=int,
        default=8,
        help="Quantidade de handovers CLOSED mantidos no arquivo ativo.",
    )
    p.add_argument(
        "--summary-closed",
        type=int,
        default=5,
        help="Quantidade de handovers CLOSED recentes no resumo leve.",
    )
    p.add_argument(
        "--apply",
        action="store_true",
        help="Aplica alteracoes em disco. Sem essa flag, roda em dry-run.",
    )
    return p.parse_args()


def split_sections(content: str) -> tuple[str, list[str]]:
    matches = list(ID_RE.finditer(content))
    if not matches:
        return content, []

    prefix = content[: matches[0].start()].rstrip() + "\n\n"
    blocks: list[str] = []

    for i, m in enumerate(matches):
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(content)
        blocks.append(content[start:end].strip())
    return prefix, blocks


def get_match(pattern: re.Pattern[str], text: str, default: str) -> str:
    m = pattern.search(text)
    if not m:
        return default
    return m.group(1).strip()


def parse_section(block: str) -> Section:
    return Section(
        raw=block.strip(),
        ident=get_match(ID_RE, block, "SEM-ID"),
        status=get_match(STATUS_RE, block, "UNKNOWN"),
        date=get_match(DATE_RE, block, ""),
        owner_from=get_match(FROM_RE, block, ""),
        owner_to=get_match(TO_RE, block, ""),
    )


def join_sections(prefix: str, sections: list[Section]) -> str:
    if not sections:
        return prefix.rstrip() + "\n"
    body = "\n\n---\n\n".join(s.raw for s in sections)
    return prefix.rstrip() + "\n\n" + body + "\n"


def append_archive(archive_path: Path, moved: list[Section], source_file: Path) -> None:
    archive_path.parent.mkdir(parents=True, exist_ok=True)
    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if not archive_path.exists():
        header = (
            "# Handover Archive (Prumo)\n\n"
            "Arquivo de historico de handovers compactados automaticamente.\n"
            "Nao editar manualmente, exceto para consulta.\n\n"
        )
        archive_path.write_text(header, encoding="utf-8")

    batch_header = (
        f"\n## Lote {now}\n"
        f"- Origem: `{source_file}`\n"
        f"- Itens movidos: {len(moved)}\n\n"
    )
    batch_body = "\n\n---\n\n".join(s.raw for s in moved)

    with archive_path.open("a", encoding="utf-8") as f:
        f.write(batch_header)
        f.write(batch_body)
        f.write("\n")


def build_summary(summary_path: Path, active: list[Section], summary_closed: int) -> None:
    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    pending = [s for s in active if s.status == "PENDING_VALIDATION"]
    rejected = [s for s in active if s.status == "REJECTED"]
    closed = [s for s in active if s.status == "CLOSED"]
    closed_recent = closed[-summary_closed:] if summary_closed > 0 else []

    lines: list[str] = [
        "# Handover Summary (Prumo)",
        "",
        f"Gerado em: {now}",
        f"Total no arquivo ativo: {len(active)}",
        "",
        "## Pendentes de validacao",
    ]

    if pending:
        for s in pending:
            lines.append(f"- {s.ident} | de: {s.owner_from} | para: {s.owner_to} | data: {s.date}")
    else:
        lines.append("- Nenhum.")

    lines.extend(["", "## Rejeitados (bloqueio)"])
    if rejected:
        for s in rejected:
            lines.append(f"- {s.ident} | de: {s.owner_from} | para: {s.owner_to} | data: {s.date}")
    else:
        lines.append("- Nenhum.")

    lines.extend(["", "## Fechados recentes (referencia)"])
    if closed_recent:
        for s in closed_recent:
            lines.append(f"- {s.ident} | de: {s.owner_from} | para: {s.owner_to} | data: {s.date}")
    else:
        lines.append("- Nenhum.")

    lines.append("")
    summary_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    args = parse_args()
    ws = Path(args.workspace).resolve()

    handover_path = ws / "_state" / "HANDOVER.md"
    if not handover_path.exists():
        print(f"skip: {handover_path} nao encontrado")
        return 0

    content = handover_path.read_text(encoding="utf-8")
    prefix, blocks = split_sections(content)
    if not blocks:
        print("skip: nenhum bloco de handover encontrado")
        return 0

    sections = [parse_section(b) for b in blocks]

    closed = [s for s in sections if s.status == "CLOSED"]
    open_or_review = [s for s in sections if s.status != "CLOSED"]

    keep_closed = max(args.keep_closed, 0)
    keep_tail = closed[-keep_closed:] if keep_closed > 0 else []
    moved = closed[:-keep_closed] if keep_closed > 0 else closed

    active_sections = open_or_review + keep_tail

    print(f"handover_total: {len(sections)}")
    print(f"handover_closed: {len(closed)}")
    print(f"handover_keep_closed: {len(keep_tail)}")
    print(f"handover_move_archive: {len(moved)}")

    if args.apply:
        archive_dir = ws / "_state" / "archive"
        backup_dir = archive_dir / "backups"
        backup_dir.mkdir(parents=True, exist_ok=True)

        stamp = dt.datetime.now().strftime("%Y-%m-%d-%H%M%S")
        backup_file = backup_dir / f"HANDOVER.md.{stamp}"
        backup_file.write_text(content, encoding="utf-8")

        if moved:
            append_archive(archive_dir / "HANDOVER-ARCHIVE.md", moved, handover_path)

        new_content = join_sections(prefix, active_sections)
        handover_path.write_text(new_content, encoding="utf-8")

        summary_path = ws / "_state" / "HANDOVER.summary.md"
        build_summary(summary_path, active_sections, args.summary_closed)

        print(f"apply: backup={backup_file}")
        print(f"apply: handover={handover_path}")
        print(f"apply: summary={summary_path}")
    else:
        print("dry_run: sem alteracoes")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
