#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
REPO_ROOT=$(cd "$SCRIPT_DIR/.." && pwd)

"$SCRIPT_DIR/bootstrap.sh"
if [[ -f "$REPO_ROOT/.venv/bin/activate" ]]; then
  # shellcheck disable=SC1090
  source "$REPO_ROOT/.venv/bin/activate"
fi

python -m unittest discover -s tests

python -m rf_research.cli generate
python -m rf_research.cli train
python -m rf_research.cli evaluate
python -m rf_research.cli spark
python -m rf_research.cli hadoop
python -m rf_research.cli collect
python -m rf_research.cli analyze

make -C core-os
./core-os/ai_integration secure
./core-os/ai_integration monitor 1 1

python "$SCRIPT_DIR/verify_outputs.py"
