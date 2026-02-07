#!/bin/bash

# PURPOSE: 
#   Run tests efficiently using 'uv' without redundant tool re-installation.
# WHY: 
#   Optimizes execution time by correctly checking all common local bin paths.

# 1. Step: Comprehensive check for 'uv' in common local paths
if ! command -v uv &> /dev/null && [ ! -f "$HOME/.local/bin/uv" ] && [ ! -f "$HOME/.cargo/bin/uv" ]; then
    echo "[LOG] 'uv' not found. Installing standalone manager..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
fi

# Ensure 'uv' is in the current PATH for this script execution
[[ -f "$HOME/.local/bin/env" ]] && source "$HOME/.local/bin/env"
[[ -f "$HOME/.cargo/env" ]] && source "$HOME/.cargo/env"

# 2. Step: Execute tests (uses cached python and packages automatically)
echo "[LOG] Executing tests..."
uv run --python 3.12 --with pytest-cov --with-requirements requirements.txt \
   python -m pytest --cov=lambda --cov-report=html

echo "--------------------------------------------------------"
echo "[SUCCESS] HTML report updated: htmlcov/index.html"
echo "--------------------------------------------------------"