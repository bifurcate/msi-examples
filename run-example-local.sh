#!/usr/bin/env bash
set -euo pipefail

if [ $# -lt 1 ]; then
  echo "Usage: $0 <project_directory> [distribute args...]"
  echo "Example: $0 my-run --max-n 5000 --partition-size 500"
  exit 1
fi

PROJECT_DIR="$1"
shift

# Clean existing project data
if [ -d "$PROJECT_DIR" ]; then
  echo "Cleaning existing project directory: $PROJECT_DIR"
  rm -rf "$PROJECT_DIR"
fi

echo "=== Distribute ==="
poetry run python distribute.py "$@" "$PROJECT_DIR"

echo "=== Worker ==="
poetry run python worker.py "$PROJECT_DIR"

echo "=== Aggregate ==="
poetry run python aggregate.py "$PROJECT_DIR"

echo "=== Done ==="
