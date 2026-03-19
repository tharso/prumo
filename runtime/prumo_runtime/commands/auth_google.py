from __future__ import annotations

import base64
import hashlib
import json
import secrets
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from prumo_runtime.google_integration import (
    DEFAULT_GOOGLE_PROFILE,
    DEFAULT_GOOGLE_SCOPES,
    default_profile_state,
    store_oauth_bundle_in_keychain,
    update_profile_state,
    write_google_integration,
)
from prumo_runtime.workspace import WorkspaceError, build_config_from_existing, now_iso

DEFAULT_AUTH_URI = "https://accounts.google.com/o/oauth2/v2/auth"
DEFAULT_TOKEN_URI = "https://oauth2.googleapis.com/token"


def _base64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _decode_jwt_payload(token: str) -> dict:
    parts = token.split(".")
    if len(parts) != 3:
        return {}
    padded = parts[1] + "=" * (-len(parts[1]) % 4)
    try:
        payload = base64.urlsafe_b64decode(padded.encode("ascii"))
        return json.loads(payload.decode("utf-8"))
    except Exception:
        return {}


def load_client_secrets(path: Path) -> dict:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise WorkspaceError(f"client secrets nao encontrado: {path}") from exc
    except json.JSONDecodeError as exc:
        raise WorkspaceError(f"client secrets invalido: {path}") from exc

    block = payload.get("installed") or payload.get("web")
    if not isinstance(block, dict):
        raise WorkspaceError("client secrets sem bloco `installed` ou `web`")

    client_id = str(block.get("client_id") or "").strip()
    client_secret = str(block.get("client_secret") or "").strip()
    auth_uri = str(block.get("auth_uri") or DEFAULT_AUTH_URI).strip()
    token_uri = str(block.get("token_uri") or DEFAULT_TOKEN_URI).strip()
    if not client_id:
        raise WorkspaceError("client secrets sem client_id")
    if not token_uri:
        raise WorkspaceError("client secrets sem token_uri")
    return {
        "client_id": client_id,
        "client_secret": client_secret,
        "auth_uri": auth_uri,
        "token_uri": token_uri,
        "project_id": str(block.get("project_id") or "").strip(),
        "source_path": str(path),
    }


def resolve_client_config(args) -> dict:
    if args.client_id:
        client_id = str(args.client_id).strip()
        client_secret = str(args.client_secret or "").strip()
        if not client_secret:
            raise WorkspaceError("faltou --client-secret; so o client_id nao abre porta nenhuma")
        return {
            "client_id": client_id,
            "client_secret": client_secret,
            "auth_uri": str(args.auth_uri or DEFAULT_AUTH_URI).strip(),
            "token_uri": str(args.token_uri or DEFAULT_TOKEN_URI).strip(),
            "project_id": str(args.project_id or "").strip(),
            "source_path": "inline-flags",
        }

    if not args.client_secrets:
        raise WorkspaceError(
            "informe --client-secrets ou o par --client-id/--client-secret; adivinhacao OAuth nao entrou no roadmap"
        )

    client_secrets_path = Path(args.client_secrets).expanduser().resolve()
    client = load_client_secrets(client_secrets_path)
    if args.project_id:
        client["project_id"] = str(args.project_id).strip()
    return client


class OAuthCallbackServer(ThreadingHTTPServer):
    auth_code: str | None = None
    auth_error: str | None = None
    auth_state: str | None = None


class OAuthCallbackHandler(BaseHTTPRequestHandler):
    def log_message(self, fmt: str, *args) -> None:  # pragma: no cover
        return

    def do_GET(self) -> None:  # noqa: N802
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)
        code = params.get("code", [None])[0]
        error = params.get("error", [None])[0]
        state = params.get("state", [None])[0]
        if code or error or state:
            self.server.auth_code = code
            self.server.auth_error = error
            self.server.auth_state = state
        status_code = 200 if code else 400
        body = (
            "<html><body><h1>Prumo</h1><p>Autenticacao recebida. Pode fechar esta aba.</p></body></html>"
            if code
            else "<html><body><h1>Prumo</h1><p>Callback incompleto. Volte para o terminal.</p></body></html>"
        )
        self.send_response(status_code)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(body.encode("utf-8"))


def wait_for_callback(server: OAuthCallbackServer, timeout_seconds: int) -> tuple[str, str]:
    deadline = time.monotonic() + timeout_seconds
    while time.monotonic() < deadline:
        remaining = max(0.1, deadline - time.monotonic())
        server.timeout = min(0.5, remaining)
        thread = threading.Thread(target=server.handle_request, daemon=True)
        thread.start()
        thread.join(server.timeout + 0.1)
        if server.auth_error:
            raise WorkspaceError(f"google respondeu com erro: {server.auth_error}")
        if server.auth_code and server.auth_state:
            return server.auth_code, server.auth_state
    raise WorkspaceError("timeout esperando callback do navegador")


def exchange_code_for_token(
    *,
    token_uri: str,
    client_id: str,
    client_secret: str,
    code: str,
    code_verifier: str,
    redirect_uri: str,
) -> dict:
    form = {
        "client_id": client_id,
        "code": code,
        "code_verifier": code_verifier,
        "grant_type": "authorization_code",
        "redirect_uri": redirect_uri,
    }
    if client_secret:
        form["client_secret"] = client_secret
    request = urllib.request.Request(
        token_uri,
        data=urllib.parse.urlencode(form).encode("utf-8"),
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise WorkspaceError(f"falha trocando code por token: HTTP {exc.code} {body}") from exc


def build_auth_url(
    *,
    auth_uri: str,
    client_id: str,
    redirect_uri: str,
    scopes: list[str],
    state: str,
    code_challenge: str,
) -> str:
    params = {
        "access_type": "offline",
        "client_id": client_id,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
        "include_granted_scopes": "true",
        "prompt": "consent",
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": " ".join(scopes),
        "state": state,
    }
    return f"{auth_uri}?{urllib.parse.urlencode(params)}"


def run_auth_google(args) -> int:
    workspace = Path(args.workspace).expanduser().resolve()
    config = build_config_from_existing(workspace)

    client = resolve_client_config(args)
    profile = args.profile or DEFAULT_GOOGLE_PROFILE
    profile_state = default_profile_state(workspace, profile)
    scopes = list(profile_state["scopes"] or DEFAULT_GOOGLE_SCOPES)

    code_verifier = _base64url(secrets.token_bytes(48))
    code_challenge = _base64url(hashlib.sha256(code_verifier.encode("ascii")).digest())
    state = secrets.token_urlsafe(24)

    callback_server = OAuthCallbackServer(("127.0.0.1", 0), OAuthCallbackHandler)
    redirect_uri = f"http://127.0.0.1:{callback_server.server_port}/oauth2callback"
    auth_url = build_auth_url(
        auth_uri=args.auth_uri or client["auth_uri"],
        client_id=client["client_id"],
        redirect_uri=redirect_uri,
        scopes=scopes,
        state=state,
        code_challenge=code_challenge,
    )

    print(f"{config.user_name}, vamos conectar a conta Google do perfil `{profile}`.", flush=True)
    print(
        "Nada sensivel vai para o workspace em texto puro. O state guarda metadado; token vai para o Keychain.",
        flush=True,
    )
    print(f"URL de autorizacao: {auth_url}", flush=True)
    if not args.no_open:
        if webbrowser.open(auth_url):
            print(
                "Abri o navegador. Se ele fingir demencia, copie a URL acima e cole manualmente.",
                flush=True,
            )
        else:
            print(
                "Nao consegui abrir o navegador sozinho. Copie a URL acima e siga por conta propria.",
                flush=True,
            )

    try:
        code, returned_state = wait_for_callback(callback_server, timeout_seconds=args.timeout)
    finally:
        callback_server.server_close()
    if returned_state != state:
        raise WorkspaceError("state OAuth nao confere; melhor parar do que aceitar truque barato")

    token_payload = exchange_code_for_token(
        token_uri=args.token_uri or client["token_uri"],
        client_id=client["client_id"],
        client_secret=client["client_secret"],
        code=code,
        code_verifier=code_verifier,
        redirect_uri=redirect_uri,
    )
    if "refresh_token" not in token_payload:
        raise WorkspaceError(
            "Google nao devolveu refresh_token. Sem isso, a integracao nasce com perna curta."
        )

    id_claims = _decode_jwt_payload(str(token_payload.get("id_token") or ""))
    account_email = str(id_claims.get("email") or "").strip()
    oauth_bundle = {
        "oauth_client": {
            "client_id": client["client_id"],
            "client_secret": client["client_secret"],
            "auth_uri": args.auth_uri or client["auth_uri"],
            "token_uri": args.token_uri or client["token_uri"],
        },
        "token_payload": token_payload,
    }
    stored = store_oauth_bundle_in_keychain(workspace, profile, oauth_bundle)
    payload = update_profile_state(
        workspace,
        profile,
        status="connected",
        account_email=account_email,
        scopes=scopes,
        last_authenticated_at=now_iso(config.timezone_name),
    )
    payload["profiles"][profile]["token_storage"] = stored
    payload["status"] = "connected"
    write_google_integration(workspace, payload)

    print("")
    print("Conta Google conectada.")
    print(f"- Workspace: {workspace}")
    print(f"- Perfil: {profile}")
    print(f"- Conta: {account_email or 'nao foi possivel extrair email do id_token'}")
    print(f"- Escopos: {len(scopes)}")
    print(f"- Token storage: {stored['type']} ({stored['service']} / {stored['account']})")
    print(f"- Credencial: {client['source_path']}")
    print("")
    print("Próximos passos:")
    print("1. Rode `prumo context-dump --workspace ... --format json` para conferir o estado da integração.")
    print("2. Só depois mexa no briefing. Integração sem estado explícito é só ansiedade com credencial.")
    return 0
