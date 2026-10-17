#!/usr/bin/env bash
# Smoke test: add this repo as a marketplace and install every plugin,
# using a throwaway CLAUDE_CONFIG_DIR. Slower than `make verify`; run via `make smoke`.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
CLAUDE_CONFIG_DIR="$(mktemp -d)"
export CLAUDE_CONFIG_DIR
trap 'rm -rf "$CLAUDE_CONFIG_DIR"' EXIT

claude plugin marketplace add "$ROOT"
for name in agentic-workflow code-navigation linear-workflow project-template; do
  claude plugin install "$name@agent-toolkit"
done
echo "smoke: OK"
