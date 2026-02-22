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
  if ! rg -q --pcre2 "$pattern" "$file"; then
    fail "$label (arquivo: $file)"
  fi
}

CORE_FILE="references/prumo-core.md"
SKILL_FILE="skills/briefing/SKILL.md"
SKILL_MIRROR_FILE="skills-briefing-SKILL.md"

for file in "$CORE_FILE" "$SKILL_FILE" "$SKILL_MIRROR_FILE"; do
  [[ -f "$file" ]] || fail "Arquivo obrigatório ausente: $file"
done

for file in "$CORE_FILE" "$SKILL_FILE" "$SKILL_MIRROR_FILE"; do
  assert_contains "$file" "Responder" "Taxonomia: ausência de 'Responder'"
  assert_contains "$file" "Ver" "Taxonomia: ausência de 'Ver'"
  assert_contains "$file" "Sem ação|Sem acao" "Taxonomia: ausência de 'Sem ação'"
  assert_contains "$file" "P1/P2/P3|P1.*P2.*P3" "Prioridade P1/P2/P3 ausente"
done

for file in "$CORE_FILE" "$SKILL_FILE" "$SKILL_MIRROR_FILE"; do
  assert_contains "$file" "last_briefing_at" "Janela temporal: falta referência a last_briefing_at"
  assert_contains "$file" "24h|24 h|24 horas" "Janela temporal: falta fallback de 24h"
done

assert_contains "$SKILL_FILE" "Google dual via Gemini CLI|script dual" "Modo com shell não descrito na skill principal"
assert_contains "$SKILL_FILE" "Fallback sem shell" "Fallback sem shell não descrito na skill principal"
assert_contains "$SKILL_MIRROR_FILE" "Google dual via Gemini CLI|script dual" "Modo com shell não descrito na skill espelhada"
assert_contains "$SKILL_MIRROR_FILE" "Fallback sem shell" "Fallback sem shell não descrito na skill espelhada"

assert_contains "$CORE_FILE" "com shell" "Modo com shell não descrito no core"
assert_contains "$CORE_FILE" "sem shell" "Modo sem shell não descrito no core"

echo "[OK] Briefing smoke checks passaram."
