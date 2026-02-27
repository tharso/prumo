#!/usr/bin/env bash
set -euo pipefail

# Idempotently syncs Project v2 schema used by Prumo workflow.
# - Ensures required fields exist
# - Optionally syncs field values from issue labels

OWNER="${1:-$(gh repo view --json owner -q '.owner.login')}"
PROJECT_NUMBER="${2:-6}"
SYNC_VALUES="${3:-true}" # true|false

require_bin() {
  command -v "$1" >/dev/null 2>&1 || {
    echo "Erro: comando '$1' não encontrado." >&2
    exit 1
  }
}

require_bin gh
require_bin jq

project_json="$(gh project view "$PROJECT_NUMBER" --owner "$OWNER" --format json)"
project_id="$(jq -r '.id' <<<"$project_json")"
if [[ -z "$project_id" || "$project_id" == "null" ]]; then
  echo "Erro: projeto não encontrado (owner=$OWNER, number=$PROJECT_NUMBER)." >&2
  exit 1
fi

echo "Projeto: $(jq -r '.title' <<<"$project_json") ($project_id)"

ensure_field() {
  local name="$1"
  local data_type="$2"
  local options="${3:-}"

  local existing
  existing="$(gh project field-list "$PROJECT_NUMBER" --owner "$OWNER" --format json | jq -r --arg name "$name" '.fields[] | select(.name == $name) | .id' | head -n1)"

  if [[ -n "$existing" ]]; then
    echo "Campo existente: $name"
    return 0
  fi

  if [[ "$data_type" == "SINGLE_SELECT" ]]; then
    gh project field-create "$PROJECT_NUMBER" \
      --owner "$OWNER" \
      --name "$name" \
      --data-type "$data_type" \
      --single-select-options "$options" >/dev/null
  else
    gh project field-create "$PROJECT_NUMBER" \
      --owner "$OWNER" \
      --name "$name" \
      --data-type "$data_type" >/dev/null
  fi

  echo "Campo criado: $name"
}

# Status já existe por padrão (Todo/In Progress/Done)
ensure_field "Priority" "SINGLE_SELECT" "p0,p1,p2,p3"
ensure_field "Area" "SINGLE_SELECT" "core,briefing,setup,landing,docs,infra"
ensure_field "Size" "SINGLE_SELECT" "xs,s,m,l,xl"
ensure_field "Target Version" "TEXT"
ensure_field "Agent" "SINGLE_SELECT" "codex,cowork,gemini"
ensure_field "Blocked By" "TEXT"

if [[ "$SYNC_VALUES" != "true" ]]; then
  echo "SYNC_VALUES=false: sincronização de valores pulada."
  exit 0
fi

fields_json="$(gh project field-list "$PROJECT_NUMBER" --owner "$OWNER" --format json)"
items_json="$(gh project item-list "$PROJECT_NUMBER" --owner "$OWNER" --format json --limit 500)"

get_field_id() {
  local fname="$1"
  jq -r --arg n "$fname" '.fields[] | select(.name == $n) | .id' <<<"$fields_json" | head -n1
}

get_option_id() {
  local fname="$1"
  local opt="$2"
  local opt_lc
  opt_lc="$(printf '%s' "$opt" | tr '[:upper:]' '[:lower:]')"
  jq -r --arg n "$fname" --arg o "$opt_lc" '
    .fields[] | select(.name == $n) | .options[]? | select((.name | ascii_downcase) == $o) | .id
  ' <<<"$fields_json" | head -n1
}

set_single_select() {
  local item_id="$1"
  local field_id="$2"
  local option_id="$3"
  if [[ -z "$field_id" || -z "$option_id" ]]; then
    return 0
  fi
  gh project item-edit --id "$item_id" --project-id "$project_id" --field-id "$field_id" --single-select-option-id "$option_id" >/dev/null
}

priority_field_id="$(get_field_id "Priority")"
area_field_id="$(get_field_id "Area")"
agent_field_id="$(get_field_id "Agent")"
status_field_id="$(get_field_id "Status")"

priority_opt() { get_option_id "Priority" "$1"; }
area_opt() { get_option_id "Area" "$1"; }
agent_opt() { get_option_id "Agent" "$1"; }
status_opt() { get_option_id "Status" "$1"; }

while IFS= read -r row; do
  item_id="$(jq -r '.id' <<<"$row")"
  labels_csv="$(jq -r '.labels | join(",")' <<<"$row")"

  # Priority from label priority/pX
  prio="$(awk -F',' '{for(i=1;i<=NF;i++){if($i ~ /^priority\//){split($i,a,"/");print tolower(a[2]);exit}}}' <<<"$labels_csv")"
  if [[ -n "$prio" ]]; then
    set_single_select "$item_id" "$priority_field_id" "$(priority_opt "$prio")"
  fi

  # Area from label area/*
  area="$(awk -F',' '{for(i=1;i<=NF;i++){if($i ~ /^area\//){split($i,a,"/");print tolower(a[2]);exit}}}' <<<"$labels_csv")"
  if [[ -n "$area" ]]; then
    set_single_select "$item_id" "$area_field_id" "$(area_opt "$area")"
  fi

  # Agent from label agent/*
  agent="$(awk -F',' '{for(i=1;i<=NF;i++){if($i ~ /^agent\//){split($i,a,"/");print tolower(a[2]);exit}}}' <<<"$labels_csv")"
  if [[ -n "$agent" ]]; then
    set_single_select "$item_id" "$agent_field_id" "$(agent_opt "$agent")"
  fi

  # Status mapping from status/* labels to default project status options
  stat_label="$(awk -F',' '{for(i=1;i<=NF;i++){if($i ~ /^status\//){split($i,a,"/");print tolower(a[2]);exit}}}' <<<"$labels_csv")"
  status_name=""
  case "$stat_label" in
    done) status_name="Done" ;;
    in-progress|review) status_name="In Progress" ;;
    triage|ready|blocked|"") status_name="Todo" ;;
    *) status_name="Todo" ;;
  esac
  if [[ -n "$status_name" ]]; then
    set_single_select "$item_id" "$status_field_id" "$(status_opt "$status_name")"
  fi

done < <(jq -c '.items[] | {id, labels}' <<<"$items_json")

echo "Schema sincronizado para o Project #$PROJECT_NUMBER (owner: $OWNER)."
