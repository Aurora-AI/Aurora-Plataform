#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
poetry run pytest --disable-warnings -q
