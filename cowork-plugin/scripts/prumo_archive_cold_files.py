#!/usr/bin/env python3
"""Arquiva arquivos frios e seguros do workspace do Prumo.

Escopo inicial e conservador:
- arquivos de `Inbox4Mobile/` marcados como processados em `_processed.json`
- apenas itens com idade acima do threshold configurado
- nunca apaga sem mover para archive
- sempre registra no indice global de archive
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from prumo_archive_index import append_archive_entries, now_iso

CONTROL_FILENAMES = {
    "_processed.json",
    "inbox-preview.html",
    "_preview-index.json",
}
PROCESSED_REGISTRY_RESERVED = {
    "version",
    "updated_at",
    "generated_at",
    "items",
    "processed_files",
    "meta",
}
NEGATIVE_STATUS = {
    "pending",
    "new",
    "open",
    "unprocessed",
    "todo",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Archive conservador de arquivos frios do Prumo.")
    parser.add_argument("--workspace", default=".", help="Workspace raiz (default: .)")
    parser.add_argument("--apply", action="store_true", help="Aplica mudancas em disco")
    parser.add_argument("--min-age-days", type=int, default=14, help="Idade minima do arquivo para archive")
    parser.add_argument(
        "--min-candidates",
        type=int,
        default=2,
        help="Quantidade minima de candidatos para disparar archive",
    )
    parser.add_argument(
        "--min-bytes",
        type=int,
        default=262144,
        help="Bytes minimos acumulados dos candidatos para disparar archive",
    )
    parser.add_argument(
        "--max-index-entries",
        type=int,
        default=1000,
        help="Quantidade maxima de entradas mantidas no indice global",
    )
    return parser.parse_args()


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return default


def file_fingerprint(path: Path) -> str:
    stat = path.stat()
    return f"{stat.st_mtime_ns}:{stat.st_size}"


def normalize_filename(raw: str | None) -> str | None:
    if not raw:
        return None
    text = str(raw).strip()
    if not text:
        return None
    return Path(text).name


def extract_name_from_item(item: Any, fallback_name: str | None = None) -> str | None:
    if isinstance(item, str):
        return normalize_filename(item)
    if not isinstance(item, dict):
        return normalize_filename(fallback_name)

    for key in ("filename", "name", "path", "absolute_path"):
        value = item.get(key)
        normalized = normalize_filename(value)
        if normalized:
            return normalized
    return normalize_filename(fallback_name)


def is_processed_marker(value: Any) -> bool:
    if value is False or value is None:
        return False
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return value != 0
    if isinstance(value, str):
        return value.strip().lower() not in NEGATIVE_STATUS and value.strip() != ""
    if isinstance(value, dict):
        if value.get("processed") is False:
            return False
        status = str(value.get("status") or "").strip().lower()
        if status and status in NEGATIVE_STATUS:
            return False
        return True
    return False


def parse_processed_payload(payload: Any) -> tuple[str, set[str]]:
    processed: set[str] = set()

    def add(item: Any, fallback_name: str | None = None) -> None:
        if not is_processed_marker(item):
            return
        name = extract_name_from_item(item, fallback_name=fallback_name)
        if name:
            processed.add(name)

    if payload is None:
        return "missing", processed

    if isinstance(payload, list):
        for item in payload:
            add(item)
        return "ok", processed

    if isinstance(payload, dict):
        if isinstance(payload.get("items"), list):
            for item in payload["items"]:
                add(item)
            return "ok", processed

        if isinstance(payload.get("processed_files"), list):
            for item in payload["processed_files"]:
                add(item)
            return "ok", processed

        for key, value in payload.items():
            if key in PROCESSED_REGISTRY_RESERVED:
                continue
            add(value, fallback_name=key)
        return "ok", processed

    return "unsupported_format", processed


def read_processed_registry(processed_path: Path) -> tuple[str, set[str]]:
    if not processed_path.exists():
        return "missing", set()

    try:
        payload = json.loads(processed_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return "invalid_json", set()

    return parse_processed_payload(payload)


def list_cold_inbox_candidates(workspace: Path, min_age_days: int) -> dict[str, Any]:
    inbox_dir = workspace / "Inbox4Mobile"
    processed_path = inbox_dir / "_processed.json"
    preview_path = inbox_dir / "inbox-preview.html"
    index_path = inbox_dir / "_preview-index.json"

    registry_status, processed_names = read_processed_registry(processed_path)
    if registry_status not in {"ok", "missing"}:
        return {
            "registry_status": registry_status,
            "processed_names": sorted(processed_names),
            "candidates": [],
        }

    if not inbox_dir.exists() or not inbox_dir.is_dir():
        return {
            "registry_status": registry_status,
            "processed_names": sorted(processed_names),
            "candidates": [],
        }

    now = dt.datetime.now().astimezone()
    preview_mtime = preview_path.stat().st_mtime if preview_path.exists() else 0.0
    index_mtime = index_path.stat().st_mtime if index_path.exists() else 0.0
    preview_guard_mtime = max(preview_mtime, index_mtime)
    candidates: list[dict[str, Any]] = []

    for path in sorted(inbox_dir.iterdir(), key=lambda p: p.name.lower()):
        if not path.is_file():
            continue
        if path.name in CONTROL_FILENAMES:
            continue
        if path.parent.name == "archive":
            continue
        if path.name not in processed_names:
            continue

        stat = path.stat()
        file_dt = dt.datetime.fromtimestamp(stat.st_mtime).astimezone()
        age_days = (now - file_dt).total_seconds() / 86400.0
        if age_days < min_age_days:
            continue

        candidates.append(
            {
                "path": path,
                "filename": path.name,
                "size_bytes": stat.st_size,
                "mtime_iso": file_dt.isoformat(timespec="seconds"),
                "fingerprint": file_fingerprint(path),
                "age_days": round(age_days, 2),
                "preview_guard_ok": preview_guard_mtime == 0.0 or stat.st_mtime <= preview_guard_mtime,
            }
        )

    return {
        "registry_status": registry_status,
        "processed_names": sorted(processed_names),
        "candidates": candidates,
    }


def ensure_unique_destination(path: Path) -> Path:
    if not path.exists():
        return path

    stem = path.stem
    suffix = path.suffix
    counter = 2
    while True:
        candidate = path.with_name(f"{stem}-{counter}{suffix}")
        if not candidate.exists():
            return candidate
        counter += 1


def refresh_preview(inbox_dir: Path) -> tuple[bool, str]:
    script_path = Path(__file__).with_name("generate_inbox_preview.py")
    if not script_path.exists():
        return False, "script_not_found"

    cmd = [
        sys.executable,
        str(script_path),
        "--inbox-dir",
        str(inbox_dir),
        "--output",
        str(inbox_dir / "inbox-preview.html"),
        "--index-output",
        str(inbox_dir / "_preview-index.json"),
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        detail = proc.stderr.strip() or proc.stdout.strip() or "preview_refresh_failed"
        return False, detail
    return True, proc.stdout.strip()


def main() -> int:
    args = parse_args()
    workspace = Path(args.workspace).resolve()
    inbox_dir = workspace / "Inbox4Mobile"
    archive_root = inbox_dir / "archive"
    state_archive_dir = workspace / "_state" / "archive"
    index_path = state_archive_dir / "ARCHIVE-INDEX.json"
    index_md_path = state_archive_dir / "ARCHIVE-INDEX.md"

    probe = list_cold_inbox_candidates(workspace, min_age_days=args.min_age_days)
    registry_status = str(probe["registry_status"])
    candidates = list(probe["candidates"])
    total_bytes = sum(int(item["size_bytes"]) for item in candidates)
    triggered = registry_status == "ok" and (
        len(candidates) >= args.min_candidates or total_bytes >= args.min_bytes
    )

    moved_entries: list[dict[str, Any]] = []
    preview_refreshed = False
    preview_status = "not_needed"

    if args.apply and triggered:
        for item in candidates:
            source_path = Path(item["path"])
            month_bucket = dt.datetime.fromisoformat(item["mtime_iso"]).strftime("%Y-%m")
            destination = ensure_unique_destination(archive_root / month_bucket / source_path.name)
            destination.parent.mkdir(parents=True, exist_ok=True)
            source_path.replace(destination)

            moved_entries.append(
                {
                    "run_at": now_iso(),
                    "policy": "inbox_processed_cold",
                    "source_path": str(source_path),
                    "destination_path": str(destination),
                    "reason": f"processed_marker + age>={args.min_age_days}d",
                    "size_bytes": int(item["size_bytes"]),
                    "mtime_iso": str(item["mtime_iso"]),
                    "fingerprint": str(item["fingerprint"]),
                }
            )

        preview_refreshed, preview_status = refresh_preview(inbox_dir)
        append_archive_entries(
            index_path,
            index_md_path,
            moved_entries,
            max_entries=args.max_index_entries,
        )

    print(f"workspace: {workspace}")
    print(f"processed_registry_status: {registry_status}")
    print(f"cold_candidates: {len(candidates)}")
    print(f"cold_candidate_bytes: {total_bytes}")
    print(f"threshold_min_age_days: {args.min_age_days}")
    print(f"threshold_min_candidates: {args.min_candidates}")
    print(f"threshold_min_bytes: {args.min_bytes}")
    print(f"triggered: {triggered}")
    print(f"apply_requested: {args.apply}")
    print(f"applied: {bool(args.apply and triggered)}")
    print(f"archive_moves: {len(moved_entries)}")
    print(f"archive_index_additions: {len(moved_entries)}")
    print(f"preview_refreshed: {preview_refreshed}")
    print(f"preview_status: {preview_status}")

    if registry_status not in {"ok", "missing"}:
        print("policy_abort_reason: processed_registry_invalid")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
