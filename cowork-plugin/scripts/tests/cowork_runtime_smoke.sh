#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../../.." && pwd)"
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
    rg -q -- "$pattern" "$file" || fail "$label (arquivo: $file)"
    return 0
  fi
  grep -Eq -- "$pattern" "$file" || fail "$label (arquivo: $file)"
}

TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

ORIGIN_REPO="$TMP_DIR/origin-repo"
SESSIONS_ROOT="$TMP_DIR/sessions"
STORE_ROOT="$SESSIONS_ROOT/session-a/chat-a/cowork_plugins"
MARKET_DIR="$STORE_ROOT/marketplaces/prumo-marketplace"

mkdir -p "$ORIGIN_REPO" "$STORE_ROOT/marketplaces"
git -C "$ORIGIN_REPO" init >/dev/null
git -C "$ORIGIN_REPO" config user.name "Prumo Test"
git -C "$ORIGIN_REPO" config user.email "test@example.com"

cat > "$ORIGIN_REPO/VERSION" <<'EOF'
1.2.0
EOF

cat > "$ORIGIN_REPO/marketplace.json" <<EOF
{
  "name": "prumo-marketplace",
  "plugins": [
    {
      "name": "prumo",
      "version": "1.2.0"
    }
  ]
}
EOF

git -C "$ORIGIN_REPO" add VERSION marketplace.json
git -C "$ORIGIN_REPO" commit -m "v1.2.0" >/dev/null

git clone "$ORIGIN_REPO" "$MARKET_DIR" >/dev/null 2>&1

mkdir -p "$STORE_ROOT/cache/prumo-marketplace/prumo/1.2.0"

cat > "$STORE_ROOT/known_marketplaces.json" <<EOF
{
  "prumo-marketplace": {
    "source": {
      "source": "git",
      "url": "$ORIGIN_REPO"
    },
    "installLocation": "$MARKET_DIR",
    "lastUpdated": "2026-03-18T10:00:00Z"
  }
}
EOF

cat > "$STORE_ROOT/installed_plugins.json" <<EOF
{
  "version": 2,
  "plugins": {
    "prumo@prumo-marketplace": [
      {
        "scope": "user",
        "installPath": "$STORE_ROOT/cache/prumo-marketplace/prumo/1.2.0",
        "version": "1.2.0",
        "installedAt": "2026-03-18T10:00:00Z",
        "lastUpdated": "2026-03-18T10:00:00Z",
        "gitCommitSha": "$(git -C "$MARKET_DIR" rev-parse HEAD)"
      }
    ]
  }
}
EOF

cat > "$ORIGIN_REPO/VERSION" <<'EOF'
1.3.0
EOF

cat > "$ORIGIN_REPO/marketplace.json" <<EOF
{
  "name": "prumo-marketplace",
  "plugins": [
    {
      "name": "prumo",
      "version": "1.3.0"
    }
  ]
}
EOF

git -C "$ORIGIN_REPO" add VERSION marketplace.json
git -C "$ORIGIN_REPO" commit -m "v1.3.0" >/dev/null

bash "$ROOT_DIR/scripts/prumo_cowork_doctor.sh" --sessions-root "$SESSIONS_ROOT" --json > "$TMP_DIR/doctor-before.json"

assert_contains "$TMP_DIR/doctor-before.json" "\"marketplace_checkout_stale\": true" "Doctor nao detectou checkout defasado"
assert_contains "$TMP_DIR/doctor-before.json" "\"marketplace_checkout_version\": \"1.2.0\"" "Doctor nao leu versao do checkout antes do update"

bash "$ROOT_DIR/scripts/prumo_cowork_update.sh" --sessions-root "$SESSIONS_ROOT" --json > "$TMP_DIR/update.json"

assert_contains "$TMP_DIR/update.json" "\"after_version\": \"1.3.0\"" "Updater nao trouxe checkout para a nova versao"

bash "$ROOT_DIR/scripts/prumo_cowork_doctor.sh" --sessions-root "$SESSIONS_ROOT" --json > "$TMP_DIR/doctor-after.json"

assert_contains "$TMP_DIR/doctor-after.json" "\"marketplace_checkout_stale\": false" "Doctor nao reconheceu checkout alinhado apos update"
assert_contains "$TMP_DIR/doctor-after.json" "\"marketplace_declared_plugin_version\": \"1.3.0\"" "Doctor nao leu nova versao anunciada"
assert_contains "$TMP_DIR/doctor-after.json" "\"plugin_update_recommended\": true" "Doctor nao sugeriu reinstall/update do plugin apos atualizar marketplace"

echo "[OK] Cowork runtime smoke checks passaram."
