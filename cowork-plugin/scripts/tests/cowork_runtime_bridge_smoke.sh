#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
TMP_DIR="$(mktemp -d)"
WORKSPACE_OK="$TMP_DIR/ws-ok"
WORKSPACE_OLD="$TMP_DIR/ws-old"

cleanup() {
  rm -rf "$TMP_DIR"
}
trap cleanup EXIT

fail() {
  echo "FAIL: $1" >&2
  exit 1
}

assert_contains() {
  local file="$1"
  local needle="$2"
  local message="$3"
  grep -Fq "$needle" "$file" || fail "$message"
}

mkdir -p "$WORKSPACE_OK" "$WORKSPACE_OLD"

PYTHONPATH="$ROOT_DIR/runtime" python3 -m prumo_runtime setup \
  --workspace "$WORKSPACE_OK" \
  --user-name "Tharso" \
  --agent-name "Prumo" \
  --timezone "America/Sao_Paulo" \
  --briefing-time "09:00" >/dev/null

cat >"$WORKSPACE_OK/PAUTA.md" <<'EOF'
# Pauta

## Quente (precisa de atenção agora)

- [Produto] Fechar o bridge do Cowork.

## Em andamento

- [Produto] Validar runtime local.

## Agendado / Lembretes

- **21/03**: [Saúde] Agendar exame.
EOF

cat >"$WORKSPACE_OK/INBOX.md" <<'EOF'
# Inbox

- [Email] Responder contador.
EOF

python3 "$ROOT_DIR/scripts/prumo_cowork_bridge.py" \
  --workspace "$WORKSPACE_OK" \
  --command briefing >"$TMP_DIR/bridge-ok.out"

assert_contains "$TMP_DIR/bridge-ok.out" "1. Preflight:" "bridge nao devolveu saida do runtime"
assert_contains "$TMP_DIR/bridge-ok.out" "2. Google:" "bridge nao trouxe status da integracao Google"
assert_contains "$TMP_DIR/bridge-ok.out" "7. Proposta do dia:" "bridge nao manteve briefing completo"

set +e
python3 "$ROOT_DIR/scripts/prumo_cowork_bridge.py" \
  --workspace "$WORKSPACE_OLD" \
  --command briefing >"$TMP_DIR/bridge-old.out" 2>"$TMP_DIR/bridge-old.err"
STATUS="$?"
set -e

[[ "$STATUS" -eq 12 ]] || fail "bridge deveria cair com codigo 12 em workspace antigo"
assert_contains "$TMP_DIR/bridge-old.err" "bridge-disabled:" "bridge nao explicou fallback legado"

echo "ok: cowork runtime bridge smoke"
