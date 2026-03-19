#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
TMP_DIR="$(mktemp -d)"
WORKSPACE="$TMP_DIR/ws"
SERVICE_PREFIX="prumo.test.$RANDOM.$RANDOM"
PROVIDER_PID=""
AUTH_PID=""

cleanup() {
  if [[ -n "$AUTH_PID" ]]; then
    kill "$AUTH_PID" >/dev/null 2>&1 || true
    wait "$AUTH_PID" >/dev/null 2>&1 || true
  fi
  if [[ -n "$PROVIDER_PID" ]]; then
    kill "$PROVIDER_PID" >/dev/null 2>&1 || true
    wait "$PROVIDER_PID" >/dev/null 2>&1 || true
  fi
  if [[ -f "$WORKSPACE/_state/google-integration.json" ]]; then
    SERVICE="$(python3 - <<'PY' "$WORKSPACE/_state/google-integration.json"
import json, sys
payload = json.load(open(sys.argv[1], encoding="utf-8"))
profile = payload["profiles"]["pessoal"]
print(profile["token_storage"]["service"])
print(profile["token_storage"]["account"])
PY
)"
    if [[ -n "$SERVICE" ]]; then
      SERVICE_NAME="$(echo "$SERVICE" | sed -n '1p')"
      ACCOUNT_NAME="$(echo "$SERVICE" | sed -n '2p')"
      security delete-generic-password -a "$ACCOUNT_NAME" -s "$SERVICE_NAME" >/dev/null 2>&1 || true
    fi
  fi
  rm -rf "$TMP_DIR"
}
trap cleanup EXIT

fail() {
  echo "FAIL: $1" >&2
  exit 1
}

mkdir -p "$WORKSPACE"

PYTHONPATH="$ROOT_DIR/runtime" python3 -m prumo_runtime setup \
  --workspace "$WORKSPACE" \
  --user-name "Batata" \
  --agent-name "Prumo" \
  --timezone "America/Sao_Paulo" \
  --briefing-time "09:00" >/dev/null

cat >"$TMP_DIR/fake_google_oauth.py" <<'PY'
import base64
import json
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlencode, urlparse


def b64(payload: bytes) -> str:
    return base64.urlsafe_b64encode(payload).rstrip(b"=").decode("ascii")


ID_TOKEN = ".".join(
    [
        b64(json.dumps({"alg": "none", "typ": "JWT"}).encode("utf-8")),
        b64(json.dumps({"email": "batata@example.com"}).encode("utf-8")),
        "",
    ]
)


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        return

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path != "/auth":
            self.send_response(404)
            self.end_headers()
            return
        params = parse_qs(parsed.query)
        redirect_uri = params["redirect_uri"][0]
        state = params["state"][0]
        location = f"{redirect_uri}?{urlencode({'code': 'fake-code', 'state': state})}"
        self.send_response(302)
        self.send_header("Location", location)
        self.end_headers()

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path != "/token":
            self.send_response(404)
            self.end_headers()
            return
        body = json.dumps(
            {
                "access_token": "ya29.fake-access-token",
                "refresh_token": "1//fake-refresh-token",
                "expires_in": 3600,
                "token_type": "Bearer",
                "scope": "openid email https://www.googleapis.com/auth/calendar.readonly https://www.googleapis.com/auth/gmail.readonly",
                "id_token": ID_TOKEN,
            }
        ).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
print(server.server_port, flush=True)
server.serve_forever()
PY

python3 "$TMP_DIR/fake_google_oauth.py" >"$TMP_DIR/provider.port" 2>"$TMP_DIR/provider.log" &
PROVIDER_PID="$!"

for _ in $(seq 1 50); do
  [[ -s "$TMP_DIR/provider.port" ]] && break
  sleep 0.1
done
[[ -s "$TMP_DIR/provider.port" ]] || fail "provedor OAuth fake nao subiu"
PROVIDER_PORT="$(head -n1 "$TMP_DIR/provider.port" | tr -d '[:space:]')"

cat >"$TMP_DIR/client_secret.json" <<EOF
{
  "installed": {
    "client_id": "fake-client-id.apps.googleusercontent.com",
    "client_secret": "fake-client-secret",
    "auth_uri": "http://127.0.0.1:${PROVIDER_PORT}/auth",
    "token_uri": "http://127.0.0.1:${PROVIDER_PORT}/token"
  }
}
EOF

PRUMO_GOOGLE_KEYCHAIN_SERVICE_PREFIX="$SERVICE_PREFIX" \
PYTHONPATH="$ROOT_DIR/runtime" python3 -u -m prumo_runtime auth google \
  --workspace "$WORKSPACE" \
  --client-secrets "$TMP_DIR/client_secret.json" \
  --no-open >"$TMP_DIR/auth.out" &
AUTH_PID="$!"

for _ in $(seq 1 80); do
  if grep -Fq "URL de autorizacao:" "$TMP_DIR/auth.out"; then
    break
  fi
  sleep 0.1
done

grep -Fq "URL de autorizacao:" "$TMP_DIR/auth.out" || fail "auth google nao imprimiu a URL de autorizacao"
AUTH_URL="$(python3 - <<'PY' "$TMP_DIR/auth.out"
import sys
for line in open(sys.argv[1], encoding="utf-8"):
    if line.startswith("URL de autorizacao: "):
        print(line.split(": ", 1)[1].strip())
        break
PY
)"
[[ -n "$AUTH_URL" ]] || fail "nao consegui extrair a URL de autorizacao"
sleep 0.2
curl -Ls "$AUTH_URL" >/dev/null
wait "$AUTH_PID"
AUTH_PID=""

[[ -f "$WORKSPACE/_state/google-integration.json" ]] || fail "google-integration.json nao foi criado"

python3 - <<'PY' "$WORKSPACE/_state/google-integration.json"
import json, sys
payload = json.load(open(sys.argv[1], encoding="utf-8"))
profile = payload["profiles"]["pessoal"]
assert payload["status"] == "connected"
assert payload["active_profile"] == "pessoal"
assert profile["status"] == "connected"
assert profile["account_email"] == "batata@example.com"
assert profile["token_storage"]["type"] == "macos-keychain"
PY

PYTHONPATH="$ROOT_DIR/runtime" python3 -m prumo_runtime context-dump \
  --workspace "$WORKSPACE" \
  --format json >"$TMP_DIR/context.json"

grep -Fq '"connected_profiles": [' "$TMP_DIR/context.json" || fail "context-dump nao mostrou perfis conectados"
grep -Fq '"pessoal"' "$TMP_DIR/context.json" || fail "context-dump nao mostrou perfil pessoal conectado"

echo "ok: local runtime google auth smoke"
