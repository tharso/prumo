#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ge 1 ]]; then
  OWNER="$1"
else
  OWNER="$(gh repo view --json owner -q '.owner.login')"
fi
TITLE="${2:-Prumo Product OS}"

PROJECT_URL=$(gh project create --owner "$OWNER" --title "$TITLE" --format json | jq -r '.url')

echo "Project criado: $PROJECT_URL"
echo "Sugestão: configure os campos Status, Priority, Area, Size, Target Version, Agent e Blocked By na UI do Project."
