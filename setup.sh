#!/bin/bash
# setup.sh — prepare the davinci-resolve MCP server environment for the Kimi plugin.
#
# Creates server/venv with --copies (Kimi's plugin safety scan rejects symlinked
# interpreters, so a plain `python3 -m venv` will NOT register) and installs the
# Python dependencies. Requires Python 3.10+ on PATH (3.10–3.12 recommended).
set -euo pipefail

cd "$(dirname "$0")"

PYTHON_BIN="${PYTHON_BIN:-python3}"
if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
    echo "Error: python3 not found on PATH. Install Python 3.10+ first." >&2
    exit 1
fi

PY_VER="$("$PYTHON_BIN" -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"
echo "Using $PYTHON_BIN (Python $PY_VER)"

if [ -d server/venv ]; then
    echo "server/venv already exists — remove it first if you want a clean rebuild."
else
    "$PYTHON_BIN" -m venv --copies server/venv
fi

./server/venv/bin/pip install --upgrade pip -q
./server/venv/bin/pip install -q -r server/requirements.txt

echo
echo "Done. Sanity check:"
./server/venv/bin/python -c "import mcp; print('  mcp SDK OK')" && echo "  environment ready"
echo
echo "Next: register the plugin folder in Kimi (Plugins → Personal → +),"
echo "and make sure DaVinci Resolve Studio is installed with external scripting enabled"
echo "(Preferences → General → External scripting using: Local)."
