#!/usr/bin/env bash
# Régénère la présentation PowerPoint de soutenance CIA
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
VENV="$ROOT/.venv-presentation"

if [[ ! -d "$VENV" ]]; then
  echo "Création de l'environnement Python..."
  python3 -m venv "$VENV"
  "$VENV/bin/pip" install -q -r "$ROOT/scripts/presentation/requirements.txt"
fi

"$VENV/bin/python" "$ROOT/scripts/presentation/generate_presentation.py"
