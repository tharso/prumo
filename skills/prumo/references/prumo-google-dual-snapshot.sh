#!/usr/bin/env bash
set -euo pipefail

TZ_NAME="${TZ_NAME:-America/Sao_Paulo}"
PROFILE_BASE="${GEMINI_PROFILE_BASE:-$HOME/.gemini-profiles}"
MAX_EMAILS="${MAX_EMAILS:-20}"
FALLBACK_HOURS="${FALLBACK_HOURS:-24}"
STATE_FILE="${STATE_FILE:-_state/briefing-state.json}"
GEMINI_TIMEOUT_SEC="${GEMINI_TIMEOUT_SEC:-120}"

PROFILES=("pessoal" "trabalho")
MCP_NAME="google-workspace"
MODE="${1:-snapshot}"

require_cmd() {
  local cmd="$1"
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo "ERRO: comando '$cmd' nao encontrado."
    exit 1
  fi
}

run_gemini_query() {
  if command -v gtimeout >/dev/null 2>&1; then
    gtimeout "$GEMINI_TIMEOUT_SEC" gemini "$@"
    return
  fi
  if command -v timeout >/dev/null 2>&1; then
    timeout "$GEMINI_TIMEOUT_SEC" gemini "$@"
    return
  fi
  if command -v perl >/dev/null 2>&1; then
    perl -e 'my $t=shift @ARGV; alarm($t); exec @ARGV;' "$GEMINI_TIMEOUT_SEC" gemini "$@"
    return
  fi
  gemini "$@"
}

today_ymd() {
  TZ="$TZ_NAME" date "+%Y-%m-%d"
}

now_iso() {
  TZ="$TZ_NAME" date "+%Y-%m-%dT%H:%M:%S%z" | sed 's/\(..\)$/:\1/'
}

tomorrow_ymd() {
  if TZ="$TZ_NAME" date -v+1d "+%Y-%m-%d" >/dev/null 2>&1; then
    TZ="$TZ_NAME" date -v+1d "+%Y-%m-%d"
  else
    TZ="$TZ_NAME" date -d "+1 day" "+%Y-%m-%d"
  fi
}

hours_ago_iso() {
  local hours="$1"
  if TZ="$TZ_NAME" date -v-"${hours}"H "+%Y-%m-%dT%H:%M:%S%z" >/dev/null 2>&1; then
    TZ="$TZ_NAME" date -v-"${hours}"H "+%Y-%m-%dT%H:%M:%S%z" | sed 's/\(..\)$/:\1/'
  else
    TZ="$TZ_NAME" date -d "-${hours} hours" "+%Y-%m-%dT%H:%M:%S%z" | sed 's/\(..\)$/:\1/'
  fi
}

read_last_briefing_at() {
  local found
  if [[ ! -f "$STATE_FILE" ]]; then
    echo ""
    return
  fi
  found="$(grep -Eo '"last_briefing_at"[[:space:]]*:[[:space:]]*"[^"]+"' "$STATE_FILE" 2>/dev/null | head -n1 || true)"
  if [[ -z "$found" ]]; then
    echo ""
    return
  fi
  printf "%s\n" "$found" | sed -E 's/.*"([^"]+)"$/\1/'
}

build_prompt() {
  cat <<EOF
Use apenas ferramentas MCP do servidor ${MCP_NAME}.
Fuso horario: ${TZ_NAME}
Datas de referencia:
- hoje: ${TODAY}
- amanha: ${TOMORROW}
- desde_ultimo_briefing: ${SINCE}

Objetivo:
1) Agenda de hoje (${TODAY}) com hora inicio, hora fim, titulo e calendario.
2) Agenda de amanha (${TOMORROW}) com hora inicio, hora fim, titulo e calendario.
3) Analisar emails recebidos desde ${SINCE} (nao apenas nao lidos), limite ${MAX_EMAILS}, e fazer curadoria por importancia/acao.
4) Conta principal identificada (se possivel).

Responda SOMENTE no formato abaixo (texto puro, sem markdown):
CONTA: <email-ou-desconhecido>
AGENDA_HOJE:
- <HH:MM-HH:MM> | <calendario> | <titulo>
AGENDA_AMANHA:
- <HH:MM-HH:MM> | <calendario> | <titulo>
EMAILS_DESDE_ULTIMO_BRIEFING_TOTAL: <numero>
TRIAGEM_RESPONDER:
- <P1|P2|P3> | <HH:MM> | <remetente> | <assunto> | <motivo objetivo>
TRIAGEM_VER:
- <P1|P2|P3> | <HH:MM> | <remetente> | <assunto> | <motivo objetivo>
TRIAGEM_SEM_ACAO:
- <P1|P2|P3> | <HH:MM> | <remetente> | <assunto> | <motivo objetivo>
ERROS:
- <erro ou "nenhum">
EOF
}

mark_briefing_complete() {
  local ts
  ts="$(now_iso)"
  mkdir -p "$(dirname "$STATE_FILE")"
  cat >"$STATE_FILE" <<EOF
{
  "last_briefing_at": "$ts"
}
EOF
  echo "OK: briefing marcado como concluido em $ts"
  echo "Arquivo: $STATE_FILE"
}

run_for_profile() {
  local profile="$1"
  local profile_home="${PROFILE_BASE}/${profile}"
  local prompt
  local output
  local cleaned_output
  local cmd_status
  local auth_output

  echo "## Perfil: ${profile}"
  echo "- GEMINI_CLI_HOME: ${profile_home}"

  if [[ ! -d "$profile_home" ]]; then
    echo "- Status: ERRO (perfil nao existe)"
    echo
    return
  fi

  set +e
  auth_output="$(GEMINI_CLI_HOME="$profile_home" run_gemini_query -p "Diga apenas OK" --output-format text 2>&1)"
  cmd_status=$?
  set -e
  if [[ $cmd_status -ne 0 ]] || ! printf "%s\n" "$auth_output" | grep -q "OK"; then
    echo "- Status: ERRO (auth pendente/falha, codigo ${cmd_status})"
    echo "- Acao: GEMINI_CLI_HOME=\"${profile_home}\" gemini"
    echo
    return
  fi

  if ! GEMINI_CLI_HOME="$profile_home" gemini mcp list 2>&1 | grep -q "${MCP_NAME}:"; then
    echo "- Status: ERRO (MCP '${MCP_NAME}' nao configurado)"
    echo "- Acao: GEMINI_CLI_HOME=\"${profile_home}\" gemini mcp add -s user -e GEMINI_CLI_WORKSPACE_FORCE_FILE_STORAGE=true ${MCP_NAME} npx -y @presto-ai/google-workspace-mcp"
    echo
    return
  fi

  prompt="$(build_prompt)"

  set +e
  output="$(GEMINI_CLI_HOME="$profile_home" run_gemini_query -y --allowed-mcp-server-names "$MCP_NAME" -p "$prompt" --output-format text 2>&1)"
  cmd_status=$?
  set -e
  cleaned_output="$(printf "%s\n" "$output" \
    | sed '/^YOLO mode is enabled\./d' \
    | sed '/^Loaded cached credentials\./d' \
    | sed "/^Server '${MCP_NAME}' supports tool updates\. Listening for changes\.\.\./d")"
  if [[ $cmd_status -ne 0 ]]; then
    if printf "%s\n" "$cleaned_output" | grep -q '^CONTA:'; then
      echo "- Status: AVISO (timeout parcial, codigo ${cmd_status}; usando resultado parcial)"
    else
      echo "- Status: ERRO (falha/timeout na consulta, codigo ${cmd_status})"
      if [[ -n "$cleaned_output" ]]; then
        printf "%s\n" "$cleaned_output"
      fi
      echo
      return
    fi
  fi
  if printf "%s\n" "$cleaned_output" | grep -q '^CONTA:'; then
    cleaned_output="$(printf "%s\n" "$cleaned_output" | awk 'found || /^CONTA:/{found=1; print}')"
  fi

  echo "- Status: OK"
  printf "%s\n" "$cleaned_output"
  echo
}

main() {
  local i
  require_cmd gemini

  if [[ "$MODE" == "--mark-briefing-complete" ]]; then
    mark_briefing_complete
    exit 0
  fi

  if [[ "$MODE" != "snapshot" ]]; then
    echo "Uso:"
    echo "  $0                 # gera snapshot dual para briefing"
    echo "  $0 --mark-briefing-complete"
    exit 1
  fi

  TODAY="$(today_ymd)"
  TOMORROW="$(tomorrow_ymd)"
  LAST_BRIEFING_AT="$(read_last_briefing_at)"
  if [[ -z "$LAST_BRIEFING_AT" ]]; then
    SINCE="$(hours_ago_iso "$FALLBACK_HOURS")"
    SINCE_SOURCE="fallback_${FALLBACK_HOURS}h"
  else
    SINCE="$LAST_BRIEFING_AT"
    SINCE_SOURCE="state_file"
  fi
  export TODAY TOMORROW SINCE

  echo "# Snapshot Google (Prumo Briefing)"
  echo "- Gerado em: $(TZ="$TZ_NAME" date '+%Y-%m-%d %H:%M:%S %Z')"
  echo "- Hoje: ${TODAY}"
  echo "- Amanha: ${TOMORROW}"
  echo "- Janela email: desde ${SINCE} (${SINCE_SOURCE})"
  echo "- Estado briefing: ${STATE_FILE}"
  echo

  for i in "${!PROFILES[@]}"; do
    run_for_profile "${PROFILES[$i]}"
  done

  echo "Proximo passo: apos finalizar o briefing, rode:"
  echo "  $0 --mark-briefing-complete"
}

main "$@"
