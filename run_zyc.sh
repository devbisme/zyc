#!/usr/bin/env bash

set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON="${ZYC_PYTHON:-/Users/andres/Skidl_KiCAD10_Test/.venv/bin/python}"
KICAD_APP="${KICAD_APP:-/Applications/KiCad/KiCad.app}"

if [[ ! -x "$PYTHON" ]]; then
    printf 'Python environment not found: %s\n' "$PYTHON" >&2
    exit 1
fi

if [[ ! -d "$KICAD_APP/Contents/SharedSupport" ]]; then
    printf 'KiCad 10 installation not found: %s\n' "$KICAD_APP" >&2
    exit 1
fi

export KICAD10_SYMBOL_DIR="$KICAD_APP/Contents/SharedSupport/symbols"
export KICAD10_FOOTPRINT_DIR="$KICAD_APP/Contents/SharedSupport/footprints"

cd "$PROJECT_DIR"
exec "$PYTHON" -c "from zyc.zyc import main; main()"
