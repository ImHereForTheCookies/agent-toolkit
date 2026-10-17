#!/usr/bin/env bash
# Prove the fixture can detect a regression: apply fixtures/seeded-bug.patch to a
# temp copy of fixtures/demo-project and assert that exactly one test fails,
# test_quantity_cannot_go_negative. Exits non-zero otherwise.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

cp -R "$ROOT/fixtures/demo-project" "$TMP/demo-project"
cd "$TMP/demo-project"

# The patch uses paths relative to the fixture root (a/app/main.py).
patch -p1 --quiet < "$ROOT/fixtures/seeded-bug.patch"

set +e
out="$(python3 -m pytest -q -rf tests 2>&1)"
set -e

failed="$(printf '%s\n' "$out" | grep '^FAILED ' || true)"
count="$(printf '%s' "$failed" | grep -c . || true)"

if [ "$count" -eq 1 ] && printf '%s' "$failed" | grep -q 'test_quantity_cannot_go_negative'; then
  echo "seeded bug: OK (only test_quantity_cannot_go_negative fails)"
  exit 0
fi

echo "seeded bug: FAIL - expected exactly one failure, test_quantity_cannot_go_negative; got $count:"
printf '%s\n' "$out" | tail -20
exit 1
