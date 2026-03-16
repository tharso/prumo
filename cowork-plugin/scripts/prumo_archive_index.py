#!/usr/bin/env python3
"""Helpers para indice de archive do Prumo."""

from __future__ import annotations

import datetime as dt
import hashlib
import json
from pathlib import Path
from typing import Any

INDEX_VERSION = "1.0"
MD_RECENT_LIMIT = 80


def now_iso() -> str:
    return dt.datetime.now().astimezone().isoformat(timespec="seconds")


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return default


def text_fingerprint(text: str) -> str:
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:16]


def empty_archive_index() -> dict[str, Any]:
    return {
        "version": INDEX_VERSION,
        "updated_at": "",
        "entries": [],
    }


def load_archive_index(index_path: Path) -> dict[str, Any]:
    payload = load_json(index_path, default=empty_archive_index())
    if isinstance(payload, list):
        payload = {
            "version": INDEX_VERSION,
            "updated_at": "",
            "entries": payload,
        }

    if not isinstance(payload, dict):
        payload = empty_archive_index()

    entries = payload.get("entries")
    if not isinstance(entries, list):
        entries = []

    return {
        "version": str(payload.get("version") or INDEX_VERSION),
        "updated_at": str(payload.get("updated_at") or ""),
        "entries": [entry for entry in entries if isinstance(entry, dict)],
    }


def normalize_entry(entry: dict[str, Any]) -> dict[str, Any]:
    return {
        "run_at": str(entry.get("run_at") or now_iso()),
        "policy": str(entry.get("policy") or "unknown"),
        "source_path": str(entry.get("source_path") or ""),
        "destination_path": str(entry.get("destination_path") or ""),
        "reason": str(entry.get("reason") or ""),
        "size_bytes": int(entry.get("size_bytes") or 0),
        "mtime_iso": str(entry.get("mtime_iso") or ""),
        "fingerprint": str(entry.get("fingerprint") or ""),
    }


def render_archive_index_md(payload: dict[str, Any]) -> str:
    updated_at = str(payload.get("updated_at") or "")
    entries = payload.get("entries") or []
    recent_entries = list(reversed(entries[-MD_RECENT_LIMIT:]))

    lines = [
        "# Archive Index (Prumo)",
        "",
        "Indice humano do historico de archive automatico do Prumo.",
        "",
        f"Atualizado em: {updated_at or 'desconhecido'}",
        f"Entradas totais: {len(entries)}",
        "",
        "## Entradas recentes",
    ]

    if not recent_entries:
        lines.extend(["", "- Nenhuma entrada registrada."])
        return "\n".join(lines) + "\n"

    current_run = None
    for entry in recent_entries:
        run_at = str(entry.get("run_at") or "desconhecido")
        if run_at != current_run:
            current_run = run_at
            lines.extend(["", f"### Run {run_at}", ""])

        policy = str(entry.get("policy") or "unknown")
        source_path = str(entry.get("source_path") or "")
        destination_path = str(entry.get("destination_path") or "")
        reason = str(entry.get("reason") or "")
        size_bytes = int(entry.get("size_bytes") or 0)
        lines.append(
            f"- `{policy}` | `{source_path}` -> `{destination_path}` | motivo: {reason} | tamanho: {size_bytes} B"
        )

    lines.append("")
    return "\n".join(lines)


def append_archive_entries(
    index_path: Path,
    markdown_path: Path,
    new_entries: list[dict[str, Any]],
    max_entries: int = 1000,
) -> dict[str, int]:
    payload = load_archive_index(index_path)
    existing_count = len(payload["entries"])

    normalized = [normalize_entry(entry) for entry in new_entries if isinstance(entry, dict)]
    if normalized:
        payload["entries"].extend(normalized)
        if max_entries > 0:
            payload["entries"] = payload["entries"][-max_entries:]
        payload["updated_at"] = now_iso()

        index_path.parent.mkdir(parents=True, exist_ok=True)
        index_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        markdown_path.write_text(render_archive_index_md(payload), encoding="utf-8")

    return {
        "added": len(normalized),
        "before": existing_count,
        "after": len(payload["entries"]),
    }
