#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VERSION="$(cat "$ROOT_DIR/VERSION")"

find_uv() {
  if command -v uv >/dev/null 2>&1; then
    command -v uv
    return 0
  fi
  if [ -x "$HOME/.local/bin/uv" ]; then
    echo "$HOME/.local/bin/uv"
    return 0
  fi
  return 1
}

find_python() {
  local candidate
  for candidate in python3.13 python3.12 python3.11; do
    if command -v "$candidate" >/dev/null 2>&1; then
      command -v "$candidate"
      return 0
    fi
  done
  return 1
}

echo "==> Instalando runtime local do Prumo"
echo "Repo: $ROOT_DIR"

if UV_BIN="$(find_uv)"; then
  echo "Usando uv: $UV_BIN"
  "$UV_BIN" tool install --editable --force --python 3.11 "$ROOT_DIR"
elif PYTHON_BIN="$(find_python)"; then
  echo "uv nao encontrado. Vou de pip com $PYTHON_BIN"
  "$PYTHON_BIN" -m pip install --user -e "$ROOT_DIR"
else
  echo "erro: preciso de uv ou Python 3.11+ para instalar o runtime." >&2
  echo "Instale uv (https://docs.astral.sh/uv/) ou um Python 3.11+ e tente de novo." >&2
  exit 1
fi

echo ""
echo "Runtime instalado. Versao: $VERSION"
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
  echo "Obs: \$HOME/.local/bin nao esta no PATH desta sessao."
  echo "Se o comando \`prumo\` nao responder, rode: export PATH=\"\$HOME/.local/bin:\$PATH\""
fi
echo "Teste rapido:"
echo "1. prumo --version"
echo "2. prumo setup --workspace /caminho/do/workspace"
