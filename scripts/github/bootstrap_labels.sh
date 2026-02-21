#!/usr/bin/env bash
set -euo pipefail

OWNER="${1:-tharso}"
REPO="${2:-prumo}"

create_or_update_label() {
  local name="$1"
  local color="$2"
  local description="$3"
  gh label create "$name" --repo "$OWNER/$REPO" --color "$color" --description "$description" --force >/dev/null
  echo "ok: $name"
}

create_or_update_label "type/feature" "0E8A16" "Nova funcionalidade"
create_or_update_label "type/bug" "D73A4A" "Defeito ou regressão"
create_or_update_label "type/debt" "B60205" "Dívida técnica"
create_or_update_label "type/spike" "5319E7" "Investigação timeboxed"
create_or_update_label "type/chore" "1D76DB" "Manutenção"

create_or_update_label "priority/p0" "B60205" "Crítico"
create_or_update_label "priority/p1" "D93F0B" "Alta"
create_or_update_label "priority/p2" "FBCA04" "Média"
create_or_update_label "priority/p3" "0E8A16" "Baixa"

create_or_update_label "status/triage" "BFDADC" "Aguardando refinamento"
create_or_update_label "status/ready" "0E8A16" "Pronta para execução"
create_or_update_label "status/in-progress" "1D76DB" "Em execução"
create_or_update_label "status/review" "5319E7" "Em revisão"
create_or_update_label "status/done" "0E8A16" "Concluída"
create_or_update_label "status/blocked" "D73A4A" "Bloqueada"

create_or_update_label "area/core" "0052CC" "Motor e regras do sistema"
create_or_update_label "area/briefing" "006B75" "Fluxo de briefing"
create_or_update_label "area/setup" "5319E7" "Onboarding e setup"
create_or_update_label "area/landing" "C5DEF5" "Landing e posicionamento"
create_or_update_label "area/docs" "A2EEEF" "Documentação"
create_or_update_label "area/infra" "BFD4F2" "Infraestrutura e automação"

create_or_update_label "agent/codex" "0366D6" "Execução principal pelo Codex"
create_or_update_label "agent/cowork" "8250DF" "Execução principal pelo Cowork"

echo "Labels atualizadas em $OWNER/$REPO"
