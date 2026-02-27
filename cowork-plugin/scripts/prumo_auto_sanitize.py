#!/usr/bin/env python3
"""Autosanitizacao do estado operacional do Prumo.

Executa manutencao preventiva por gatilhos objetivos:
1) Compacta handovers antigos quando HANDOVER.md cresce demais.
2) Regenera preview/index do Inbox4Mobile quando volume/defasagem exigirem.

Ajuste de thresholds e por workspace (usuario) via historico local:
- _state/auto-sanitize-history.json

Sem --apply, roda em dry-run.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

MEDIA_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".webp",
    ".bmp",
    ".svg",
    ".heic",
    ".heif",
    ".pdf",
    ".mp4",
    ".mov",
    ".m4v",
    ".avi",
    ".mkv",
    ".webm",
}

IGNORE_NAMES = {
    "_processed.json",
    "inbox-preview.html",
    "_preview-index.json",
}

THRESHOLD_KEYS = [
    "handover_max_bytes",
    "handover_max_lines",
    "handover_keep_closed",
    "inbox_min_total",
    "inbox_min_media",
]

BASE_THRESHOLDS = {
    "handover_max_bytes": 120_000,
    "handover_max_lines": 350,
    "handover_keep_closed": 8,
    "inbox_min_total": 8,
    "inbox_min_media": 4,
}


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Autosanitizacao do Prumo por gatilhos.")
    p.add_argument("--workspace", default=".", help="Workspace raiz (default: .)")
    p.add_argument("--apply", action="store_true", help="Aplica mudancas em disco")
    p.add_argument("--force", action="store_true", help="Ignora cooldown e força execução")
    p.add_argument("--cooldown-hours", type=int, default=6, help="Cooldown entre execucoes")

    p.add_argument("--adaptive", choices=["auto", "off"], default="auto")
    p.add_argument("--adaptive-min-samples", type=int, default=12)
    p.add_argument("--history-max-samples", type=int, default=400)

    p.add_argument("--handover-max-bytes", type=int, default=None)
    p.add_argument("--handover-max-lines", type=int, default=None)
    p.add_argument("--handover-keep-closed", type=int, default=None)

    p.add_argument("--inbox-min-total", type=int, default=None)
    p.add_argument("--inbox-min-media", type=int, default=None)
    return p.parse_args()


def now_iso() -> str:
    return dt.datetime.now().astimezone().isoformat()


def find_script(ws: Path, candidates: list[str]) -> Path | None:
    for rel in candidates:
        path = (ws / rel).resolve()
        if path.exists() and path.is_file():
            return path
    return None


def parse_iso(raw: str | None) -> dt.datetime | None:
    if not raw:
        return None
    try:
        return dt.datetime.fromisoformat(raw)
    except ValueError:
        return None


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return default


def save_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def list_inbox_files(inbox_dir: Path) -> list[Path]:
    if not inbox_dir.exists() or not inbox_dir.is_dir():
        return []
    files: list[Path] = []
    for path in inbox_dir.iterdir():
        if not path.is_file():
            continue
        if path.name in IGNORE_NAMES:
            continue
        files.append(path)
    return files


def count_media(files: list[Path]) -> int:
    return sum(1 for f in files if f.suffix.lower() in MEDIA_EXTENSIONS)


def count_handover_closed(handover_path: Path) -> int:
    if not handover_path.exists():
        return 0
    text = handover_path.read_text(encoding="utf-8")
    status_re = re.compile(r"^-\s+Status:\s*([A-Z_]+)", re.MULTILINE)
    statuses = status_re.findall(text)
    return sum(1 for s in statuses if s == "CLOSED")


def run_cmd(cmd: list[str]) -> tuple[int, str, str]:
    proc = subprocess.run(cmd, capture_output=True, text=True)
    return proc.returncode, proc.stdout.strip(), proc.stderr.strip()


def clamp(value: int, lo: int, hi: int) -> int:
    return max(lo, min(hi, value))


def percentile(values: list[float], pct: float) -> float:
    if not values:
        return 0.0
    if pct <= 0:
        return min(values)
    if pct >= 100:
        return max(values)

    ordered = sorted(values)
    idx = (len(ordered) - 1) * (pct / 100.0)
    lo = int(idx)
    hi = min(lo + 1, len(ordered) - 1)
    if lo == hi:
        return ordered[lo]
    weight = idx - lo
    return ordered[lo] * (1 - weight) + ordered[hi] * weight


def numeric_series(history: list[dict[str, Any]], key: str) -> list[float]:
    out: list[float] = []
    for row in history:
        metrics = row.get("metrics")
        if not isinstance(metrics, dict):
            continue
        raw = metrics.get(key)
        if isinstance(raw, (int, float)):
            out.append(float(raw))
    return out


def compute_adaptive_thresholds(
    history: list[dict[str, Any]],
    base: dict[str, int],
    min_samples: int,
) -> tuple[dict[str, int] | None, dict[str, Any]]:
    sample_size = len(history)
    if sample_size < min_samples:
        return None, {
            "status": "insufficient_history",
            "sample_size": sample_size,
            "min_samples": min_samples,
        }

    lines = numeric_series(history, "handover_lines")
    sizes = numeric_series(history, "handover_size_bytes")
    closed = numeric_series(history, "handover_closed")
    inbox_total = numeric_series(history, "inbox_total_files")
    inbox_media = numeric_series(history, "inbox_media_files")

    if not lines or not sizes:
        return None, {
            "status": "insufficient_metrics",
            "sample_size": sample_size,
            "min_samples": min_samples,
        }

    p75_lines = percentile(lines, 75)
    p90_lines = percentile(lines, 90)
    p75_size = percentile(sizes, 75)
    p75_closed = percentile(closed, 75) if closed else float(base["handover_keep_closed"])
    p75_total = percentile(inbox_total, 75) if inbox_total else float(base["inbox_min_total"])
    p75_media = percentile(inbox_media, 75) if inbox_media else float(base["inbox_min_media"])

    bytes_per_line = p75_size / max(p75_lines, 1)

    target_handover_lines = clamp(
        int(max(base["handover_max_lines"] * 0.85, p90_lines * 1.15, p75_lines + 60)),
        240,
        1400,
    )
    target_handover_bytes = clamp(
        int(max(base["handover_max_bytes"] * 0.85, target_handover_lines * bytes_per_line * 1.15)),
        90_000,
        1_100_000,
    )

    target_keep_closed = clamp(int(round(max(base["handover_keep_closed"], p75_closed + 1))), 6, 24)
    target_inbox_total = clamp(int(round(max(base["inbox_min_total"], p75_total * 1.35))), 6, 36)
    target_inbox_media = clamp(int(round(max(base["inbox_min_media"], p75_media * 1.35))), 3, 16)

    result = {
        "handover_max_bytes": target_handover_bytes,
        "handover_max_lines": target_handover_lines,
        "handover_keep_closed": target_keep_closed,
        "inbox_min_total": target_inbox_total,
        "inbox_min_media": target_inbox_media,
    }

    debug = {
        "status": "applied",
        "sample_size": sample_size,
        "min_samples": min_samples,
        "stats": {
            "p75_handover_lines": round(p75_lines, 2),
            "p90_handover_lines": round(p90_lines, 2),
            "p75_handover_size_bytes": round(p75_size, 2),
            "p75_handover_closed": round(p75_closed, 2),
            "p75_inbox_total": round(p75_total, 2),
            "p75_inbox_media": round(p75_media, 2),
            "bytes_per_line_p75": round(bytes_per_line, 2),
        },
    }
    return result, debug


def resolve_thresholds(
    args: argparse.Namespace,
    history: list[dict[str, Any]],
) -> tuple[dict[str, int], dict[str, Any]]:
    effective = dict(BASE_THRESHOLDS)
    manual_overrides: dict[str, int] = {}

    adaptive_meta: dict[str, Any] = {
        "mode": args.adaptive,
        "sample_size": len(history),
        "min_samples": args.adaptive_min_samples,
    }

    if args.adaptive == "auto":
        adaptive, debug = compute_adaptive_thresholds(history, BASE_THRESHOLDS, args.adaptive_min_samples)
        adaptive_meta.update(debug)
        if adaptive:
            for k, v in adaptive.items():
                effective[k] = v
            adaptive_meta["recommended"] = adaptive
    else:
        adaptive_meta["status"] = "disabled"

    for k in THRESHOLD_KEYS:
        raw = getattr(args, k)
        if raw is not None:
            manual_overrides[k] = int(raw)
            effective[k] = int(raw)

    adaptive_meta["manual_overrides"] = manual_overrides
    return effective, adaptive_meta


def trim_history(history: list[dict[str, Any]], max_samples: int) -> list[dict[str, Any]]:
    if max_samples <= 0:
        return history
    return history[-max_samples:]


def main() -> int:
    args = parse_args()
    ws = Path(args.workspace).resolve()

    state_dir = ws / "_state"
    state_dir.mkdir(parents=True, exist_ok=True)
    state_path = state_dir / "auto-sanitize-state.json"
    history_path = state_dir / "auto-sanitize-history.json"

    handover_path = state_dir / "HANDOVER.md"
    handover_summary_path = state_dir / "HANDOVER.summary.md"

    inbox_dir = ws / "Inbox4Mobile"
    preview_path = inbox_dir / "inbox-preview.html"
    index_path = inbox_dir / "_preview-index.json"

    state = load_json(state_path, default={})
    history = load_json(history_path, default=[])
    if not isinstance(history, list):
        history = []

    effective_thresholds, adaptive_meta = resolve_thresholds(args, history)

    last_apply_at = parse_iso(state.get("last_apply_at") if isinstance(state, dict) else None)
    cooldown_ok = True
    skipped_by_cooldown = False
    if not args.force and last_apply_at:
        elapsed = dt.datetime.now().astimezone() - last_apply_at
        cooldown_ok = elapsed.total_seconds() >= args.cooldown_hours * 3600
        skipped_by_cooldown = not cooldown_ok

    handover_exists = handover_path.exists()
    handover_size = handover_path.stat().st_size if handover_exists else 0
    handover_lines = 0
    if handover_exists:
        try:
            handover_lines = sum(1 for _ in handover_path.open("r", encoding="utf-8"))
        except OSError:
            handover_lines = 0

    handover_closed = count_handover_closed(handover_path)
    handover_over_limit = (
        handover_size >= effective_thresholds["handover_max_bytes"]
        or handover_lines >= effective_thresholds["handover_max_lines"]
    )
    handover_summary_missing = not handover_summary_path.exists()
    handover_trigger = handover_exists and (
        (handover_over_limit and handover_closed > effective_thresholds["handover_keep_closed"])
        or handover_summary_missing
    )

    inbox_files = list_inbox_files(inbox_dir)
    inbox_total = len(inbox_files)
    inbox_media = count_media(inbox_files)

    preview_exists = preview_path.exists()
    index_exists = index_path.exists()

    newest_inbox_mtime = max((p.stat().st_mtime for p in inbox_files), default=0.0)
    preview_mtime = preview_path.stat().st_mtime if preview_exists else 0.0
    index_mtime = index_path.stat().st_mtime if index_exists else 0.0

    preview_stale = bool(inbox_files) and (
        not preview_exists
        or not index_exists
        or preview_mtime < newest_inbox_mtime
        or index_mtime < newest_inbox_mtime
    )

    inbox_trigger = bool(inbox_files) and (
        inbox_total >= effective_thresholds["inbox_min_total"]
        or inbox_media >= effective_thresholds["inbox_min_media"]
        or preview_stale
    )

    triggers: list[str] = []
    if handover_trigger:
        triggers.append("handover")
    if inbox_trigger:
        triggers.append("inbox")

    should_apply = args.apply and cooldown_ok and bool(triggers)

    actions: list[dict[str, Any]] = []

    if should_apply:
        if handover_trigger:
            sanitize_script = find_script(
                ws,
                [
                    "scripts/prumo_sanitize_state.py",
                    "Prumo/scripts/prumo_sanitize_state.py",
                ],
            )
            if sanitize_script is None:
                actions.append({"name": "sanitize_handover", "ok": False, "reason": "script_not_found"})
            else:
                cmd = [
                    sys.executable,
                    str(sanitize_script),
                    "--workspace",
                    str(ws),
                    "--keep-closed",
                    str(effective_thresholds["handover_keep_closed"]),
                    "--apply",
                ]
                code, out, err = run_cmd(cmd)
                actions.append(
                    {
                        "name": "sanitize_handover",
                        "ok": code == 0,
                        "exit_code": code,
                        "stdout": out,
                        "stderr": err,
                    }
                )

        if inbox_trigger:
            preview_script = find_script(
                ws,
                [
                    "scripts/generate_inbox_preview.py",
                    "Prumo/scripts/generate_inbox_preview.py",
                ],
            )
            if preview_script is None:
                actions.append({"name": "refresh_inbox_preview", "ok": False, "reason": "script_not_found"})
            else:
                cmd = [
                    sys.executable,
                    str(preview_script),
                    "--inbox-dir",
                    str(inbox_dir),
                    "--output",
                    str(preview_path),
                    "--index-output",
                    str(index_path),
                ]
                code, out, err = run_cmd(cmd)
                actions.append(
                    {
                        "name": "refresh_inbox_preview",
                        "ok": code == 0,
                        "exit_code": code,
                        "stdout": out,
                        "stderr": err,
                    }
                )

    metrics = {
        "handover_exists": handover_exists,
        "handover_size_bytes": handover_size,
        "handover_lines": handover_lines,
        "handover_closed": handover_closed,
        "handover_summary_exists": handover_summary_path.exists(),
        "inbox_total_files": inbox_total,
        "inbox_media_files": inbox_media,
        "preview_exists": preview_exists,
        "index_exists": index_exists,
        "preview_stale": preview_stale,
    }

    decision = {
        "apply_requested": args.apply,
        "force": args.force,
        "cooldown_ok": cooldown_ok,
        "skipped_by_cooldown": skipped_by_cooldown,
        "triggers": triggers,
        "will_apply": should_apply,
    }

    state_payload = {
        "last_run_at": now_iso(),
        "last_apply_at": now_iso() if should_apply else (state.get("last_apply_at", "") if isinstance(state, dict) else ""),
        "cooldown_hours": args.cooldown_hours,
        "adaptive": adaptive_meta,
        "metrics": metrics,
        "thresholds_base": BASE_THRESHOLDS,
        "thresholds_effective": effective_thresholds,
        "decision": decision,
        "actions": actions,
        "history": {
            "path": str(history_path),
            "max_samples": args.history_max_samples,
            "samples_before": len(history),
            "samples_after": None,
        },
        "paths": {
            "workspace": str(ws),
            "handover": str(handover_path),
            "handover_summary": str(handover_summary_path),
            "inbox_preview": str(preview_path),
            "inbox_index": str(index_path),
        },
    }

    history_entry = {
        "run_at": now_iso(),
        "metrics": metrics,
        "thresholds_effective": effective_thresholds,
        "decision": {
            "triggers": triggers,
            "will_apply": should_apply,
            "cooldown_ok": cooldown_ok,
        },
    }
    history.append(history_entry)
    history = trim_history(history, args.history_max_samples)
    state_payload["history"]["samples_after"] = len(history)

    save_json(history_path, history)
    save_json(state_path, state_payload)

    print(f"state: {state_path}")
    print(f"history: {history_path}")
    print(f"adaptive_mode: {args.adaptive}")
    print(f"adaptive_status: {adaptive_meta.get('status', 'unknown')}")
    print(f"triggers: {','.join(triggers) if triggers else 'none'}")
    print(f"cooldown_ok: {cooldown_ok}")
    print(f"apply_requested: {args.apply}")
    print(f"applied: {should_apply}")

    for action in actions:
        name = action.get("name", "unknown")
        ok = action.get("ok", False)
        print(f"action:{name}:{'ok' if ok else 'fail'}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
