#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
REPO_ROOT=$(cd "$SCRIPT_DIR/.." && pwd)

"$SCRIPT_DIR/bootstrap.sh"
source "$REPO_ROOT/.venv/bin/activate"

python -m rf_research.cli generate
python -m rf_research.cli train
python -m rf_research.cli evaluate
python -m rf_research.cli spark
python -m rf_research.cli hadoop
python -m rf_research.cli collect
python -m rf_research.cli analyze

make -C core-os
./core-os/ai_integration secure
