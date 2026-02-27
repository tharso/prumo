#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ge 1 ]]; then
  OWNER="$1"
else
  OWNER="$(gh repo view --json owner -q '.owner.login')"
fi
TITLE="${2:-Prumo Product OS}"

PROJECT_JSON=$(gh project create --owner "$OWNER" --title "$TITLE" --format json)
PROJECT_URL=$(jq -r '.url' <<<"$PROJECT_JSON")
PROJECT_NUMBER=$(jq -r '.number' <<<"$PROJECT_JSON")

echo "Project criado: $PROJECT_URL"

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
"$SCRIPT_DIR/sync_project_schema.sh" "$OWNER" "$PROJECT_NUMBER" true

README_CONTENT=$'## Views recomendadas\n- Backlog (table)\n- Next (table)\n- In Progress (board)\n- Review/Validation (table)\n- Done (table)\n\n## Campos obrigatórios\n- Status\n- Priority\n- Area\n- Size\n- Target Version\n- Agent\n- Blocked By\n\nObservação: criação/edição de views ainda depende da UI do GitHub Project.'
gh project edit "$PROJECT_NUMBER" --owner "$OWNER" --readme "$README_CONTENT" >/dev/null

echo "Schema de campos aplicado e readme do project atualizado."
echo "Views: configurar na UI conforme checklist do readme (limitação atual da API/CLI)."
