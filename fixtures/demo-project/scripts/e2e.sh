#!/usr/bin/env bash
# HTTP smoke test: start uvicorn on a free port, hit /health and a create+list round trip.
set -euo pipefail
cd "$(dirname "$0")/.."

TMP="$(mktemp -d)"
SERVER_PID=""
cleanup() {
  [ -n "$SERVER_PID" ] && kill "$SERVER_PID" 2>/dev/null || true
  rm -rf "$TMP"
}
trap cleanup EXIT

PORT="$(python3 -c 'import socket; s=socket.socket(); s.bind(("127.0.0.1",0)); print(s.getsockname()[1])')"
BASE="http://127.0.0.1:$PORT"

PANTRY_DB="$TMP/e2e.db" python3 -m uvicorn app.server:app \
  --host 127.0.0.1 --port "$PORT" --log-level warning >"$TMP/server.log" 2>&1 &
SERVER_PID=$!

for _ in $(seq 1 50); do
  curl -fsS "$BASE/health" >/dev/null 2>&1 && break
  kill -0 "$SERVER_PID" 2>/dev/null || { echo "e2e: server died"; cat "$TMP/server.log"; exit 1; }
  sleep 0.2
done

fail() { echo "e2e FAIL: $1"; cat "$TMP/server.log"; exit 1; }

curl -fsS "$BASE/health" | grep -q '"status":"ok"' || fail "/health"
echo "ok  GET /health"

created="$(curl -fsS -X POST "$BASE/items" -H 'content-type: application/json' \
  -d '{"name":"e2e flour","quantity":3,"unit":"kg"}')"
echo "$created" | grep -q '"name":"e2e flour"' || fail "POST /items: $created"
echo "ok  POST /items"

curl -fsS "$BASE/items" | grep -q '"name":"e2e flour"' || fail "GET /items missing created item"
echo "ok  GET /items (round trip)"

echo "e2e: OK"
