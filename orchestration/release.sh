#!/usr/bin/env bash
# Forwarder kept at this path because HARD_LIMITS.md (hash-pinned) names it.
# The implementation lives in plugins/ticket-loop/scripts/release.sh.
exec bash "$(cd "$(dirname "$0")" && pwd)/../plugins/ticket-loop/scripts/release.sh" "$@"
