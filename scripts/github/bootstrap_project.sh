#!/usr/bin/env bash
set -euo pipefail

OWNER="${1:-tharso}"
TITLE="${2:-Prumo Product OS}"

PROJECT_URL=$(gh project create --owner "$OWNER" --title "$TITLE" --format json | jq -r '.url')

echo "Project criado: $PROJECT_URL"
echo "Sugestão: configure os campos Status, Priority, Area, Size, Target Version, Agent e Blocked By na UI do Project."
