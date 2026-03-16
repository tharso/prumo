#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT_DIR"

fail() {
  echo "[FAIL] $1" >&2
  exit 1
}

assert_contains() {
  local file="$1"
  local pattern="$2"
  local label="$3"
  if command -v rg >/dev/null 2>&1; then
    rg -q --pcre2 -- "$pattern" "$file" || fail "$label (arquivo: $file)"
    return 0
  fi

  if ! grep -Eq -- "$pattern" "$file"; then
    fail "$label (arquivo: $file)"
  fi
}

TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

HANDOVER_WS="$TMP_DIR/handover"
mkdir -p "$HANDOVER_WS/_state"
cat > "$HANDOVER_WS/_state/HANDOVER.md" <<'EOF'
# Handover

### ID: HO-TEST-001
- Status: CLOSED
- Data: 2026-03-10
- De: Codex
- Para: Cowork

Primeiro bloco fechado.

---

### ID: HO-TEST-002
- Status: CLOSED
- Data: 2026-03-11
- De: Codex
- Para: Gemini

Segundo bloco fechado.

---

### ID: HO-TEST-003
- Status: PENDING_VALIDATION
- Data: 2026-03-12
- De: Codex
- Para: Usuario

Bloco ainda quente.
EOF

python3 "$ROOT_DIR/scripts/prumo_sanitize_state.py" \
  --workspace "$HANDOVER_WS" \
  --keep-closed 1 \
  --summary-closed 1 \
  --apply >/dev/null

[[ -f "$HANDOVER_WS/_state/archive/HANDOVER-ARCHIVE.md" ]] || fail "Archive de handover nao foi gerado"
[[ -f "$HANDOVER_WS/_state/archive/ARCHIVE-INDEX.json" ]] || fail "Indice global nao foi gerado para handover"
assert_contains "$HANDOVER_WS/_state/archive/ARCHIVE-INDEX.json" "handover_closed_compaction" "Indice global nao registrou compactacao de handover"
assert_contains "$HANDOVER_WS/_state/archive/ARCHIVE-INDEX.json" "HO-TEST-001" "Indice global nao preservou origem do handover arquivado"

INBOX_WS="$TMP_DIR/inbox"
mkdir -p "$INBOX_WS/Inbox4Mobile" "$INBOX_WS/_state"
cat > "$INBOX_WS/Inbox4Mobile/item-frio.txt" <<'EOF'
arquivo frio para archive
EOF
cat > "$INBOX_WS/Inbox4Mobile/_processed.json" <<'EOF'
{
  "version": "1.0",
  "items": [
    {
      "filename": "item-frio.txt",
      "processed_at": "2026-03-01T10:00:00-03:00",
      "status": "processed"
    }
  ]
}
EOF

python3 - <<PY
from pathlib import Path
import os
import time

path = Path("$INBOX_WS/Inbox4Mobile/item-frio.txt")
old = time.time() - (20 * 86400)
os.utime(path, (old, old))
PY

python3 "$ROOT_DIR/scripts/prumo_archive_cold_files.py" \
  --workspace "$INBOX_WS" \
  --min-age-days 7 \
  --min-candidates 1 \
  --min-bytes 1 >/dev/null

[[ -f "$INBOX_WS/Inbox4Mobile/item-frio.txt" ]] || fail "Dry-run moveu arquivo frio"
[[ ! -f "$INBOX_WS/_state/archive/ARCHIVE-INDEX.json" ]] || fail "Dry-run gerou indice em disco"

python3 "$ROOT_DIR/scripts/prumo_archive_cold_files.py" \
  --workspace "$INBOX_WS" \
  --min-age-days 7 \
  --min-candidates 1 \
  --min-bytes 1 \
  --apply >/dev/null

ARCHIVED_FILE="$(find "$INBOX_WS/Inbox4Mobile/archive" -type f -name 'item-frio.txt' | head -n1)"
[[ -n "$ARCHIVED_FILE" ]] || fail "Arquivo frio nao foi movido para archive"
[[ ! -f "$INBOX_WS/Inbox4Mobile/item-frio.txt" ]] || fail "Arquivo frio permaneceu no inbox apos apply"
[[ -f "$INBOX_WS/Inbox4Mobile/_preview-index.json" ]] || fail "Preview nao foi regenerado apos archive frio"
assert_contains "$INBOX_WS/_state/archive/ARCHIVE-INDEX.json" "inbox_processed_cold" "Indice global nao registrou archive frio do inbox"

AUTO_WS="$TMP_DIR/auto"
mkdir -p "$AUTO_WS/Inbox4Mobile" "$AUTO_WS/_state"
cat > "$AUTO_WS/Inbox4Mobile/item-auto.txt" <<'EOF'
arquivo frio do autosanitize
EOF
cat > "$AUTO_WS/Inbox4Mobile/_processed.json" <<'EOF'
{
  "version": "1.0",
  "items": [
    {
      "filename": "item-auto.txt",
      "processed_at": "2026-03-01T10:00:00-03:00",
      "status": "processed"
    }
  ]
}
EOF

python3 - <<PY
from pathlib import Path
import os
import time

path = Path("$AUTO_WS/Inbox4Mobile/item-auto.txt")
old = time.time() - (20 * 86400)
os.utime(path, (old, old))
PY

python3 "$ROOT_DIR/scripts/prumo_auto_sanitize.py" \
  --workspace "$AUTO_WS" \
  --apply \
  --force \
  --cold-inbox-min-candidates 1 \
  --cold-inbox-min-bytes 1 \
  --cold-inbox-min-age-days 7 >/dev/null

AUTO_ARCHIVED="$(find "$AUTO_WS/Inbox4Mobile/archive" -type f -name 'item-auto.txt' | head -n1)"
[[ -n "$AUTO_ARCHIVED" ]] || fail "Autosanitize nao arquivou item frio"
[[ -f "$AUTO_WS/_state/auto-sanitize-state.json" ]] || fail "Autosanitize nao gravou estado"
assert_contains "$AUTO_WS/_state/auto-sanitize-state.json" "\"cold_inbox_candidates\": 1" "Autosanitize nao registrou metricas de archive frio"
assert_contains "$AUTO_WS/_state/auto-sanitize-state.json" "archive_cold_files" "Autosanitize nao registrou acao de archive frio"

echo "[OK] Sanitization/archive smoke checks passaram."
