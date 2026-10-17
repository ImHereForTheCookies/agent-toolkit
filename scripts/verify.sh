#!/usr/bin/env bash
# Step runner for `make verify`. Steps run sequentially and fail fast.
# Later tickets extend this by appending steps at the bottom.
# Note: `claude plugin validate` exits 0 on "Validation passed with warnings"
# and non-zero on errors, so we rely on the exit code alone.
set -euo pipefail

cd "$(dirname "$0")/.."

step() { printf '\n== %s ==\n' "$1"; }

# --- Step 1: validate the marketplace ---
step "1. claude plugin validate ."
claude plugin validate .

# --- Step 2: validate each plugin directory ---
step "2. validate plugins/*"
for dir in plugins/*/; do
  [ -d "$dir" ] || continue
  echo "-- ${dir%/}"
  claude plugin validate "${dir%/}"
done

# --- Step 3: run tests, only if any test files exist ---
step "3. pytest (if tests/test_*.py exist)"
if find tests -name 'test_*.py' -print -quit 2>/dev/null | grep -q .; then
  python3 -m pytest -q tests
else
  echo "no tests/test_*.py files; skipping"
fi

# --- extra steps (added by later tickets) ---

# --- Step 4: lint every tickets/**/*.md against the ticket contract (ROB-6) ---
step "4. lint tickets (tickets/**/*.md)"
ticket_files=()
while IFS= read -r f; do
  ticket_files+=("$f")
done < <(find . \( -name .git -o -name node_modules \) -prune -o \
  -type f -name '*.md' -path '*/tickets/*' -print | sort)
if [ "${#ticket_files[@]}" -gt 0 ]; then
  python3 scripts/lint_ticket.py "${ticket_files[@]}"
  echo "linted ${#ticket_files[@]} ticket file(s)"
else
  echo "no tickets/ markdown files; skipping"
fi

step "verify: OK"
