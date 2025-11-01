#!/bin/bash

# Usage: ./run_tests.sh [-a] [-l] [-n]
# -a: Run AnythingLLM tests only
# -l: Run LMStudio tests only
# -n: Run Nexa tests only

set -e

# Prompt user to start backend servers
cat <<EOF
Please start the required backend servers (AnythingLLM, LMStudio, Nexa) manually.
Press Enter when complete.
EOF
read

# Move to project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/.."

# Parse arguments
a_flag=false
l_flag=false
n_flag=false
while getopts "aln" opt; do
  case $opt in
    a) a_flag=true ;;
    l) l_flag=true ;;
    n) n_flag=true ;;
    *) ;;
  esac
done

# Determine tests to run
tests=()
if $a_flag || (! $l_flag && ! $n_flag && ! $a_flag); then tests+=("tests/test_anythingllm.py"); fi
if $l_flag || (! $a_flag && ! $n_flag && ! $l_flag); then tests+=("tests/test_lmstudio.py"); fi
if $n_flag || (! $a_flag && ! $l_flag && ! $n_flag); then tests+=("tests/test_nexa.py"); fi

if [ ${#tests[@]} -eq 0 ]; then
  tests=("tests/test_anythingllm.py" "tests/test_lmstudio.py" "tests/test_nexa.py")
fi

echo "Running pytest for: ${tests[*]}"

# Activate venv if not already active
if [ -z "$VIRTUAL_ENV" ]; then
  if [ -f "venv/bin/activate" ]; then
    echo "Activating virtual environment..."
    source "venv/bin/activate"
  fi
fi

# Run pytest
pytest "${tests[@]}"
