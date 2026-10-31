#!/usr/bin/env bash
# REST-only PR helper. `gh pr create/merge` use GraphQL, which is blocked in Claude cloud sessions.
# Run from inside the target repo checkout (repo is read from `origin`), or set REPO=owner/name.
# Usage:
#   ghpr.sh open  <head> <base> <title> <body-file>   -> prints PR URL (reuses an open PR for the same head)
#   ghpr.sh merge <head>                              -> merges the open PR for <head> with a merge commit
#   ghpr.sh url   <head>                              -> prints the open PR URL for <head>, if any
#   ghpr.sh comment <head> <body-file>                -> comments on the open PR for <head>
set -euo pipefail
if [ -z "${REPO:-}" ]; then
  url=$(git remote get-url origin)
  REPO=$(printf '%s' "$url" | sed -E 's#(git@github.com:|https://github.com/)##; s#\.git$##')
fi
OWNER=${REPO%%/*}
FOOT=${PR_FOOTER:-$'\n\n🤖 Generated with [Claude Code](https://claude.com/claude-code)'}

pr_number() { gh api "repos/$REPO/pulls?head=$OWNER:$1&state=open" --jq '.[0].number // empty'; }

case "${1:-}" in
  open)
    head=$2 base=$3 title=$4 bodyfile=$5
    n=$(pr_number "$head")
    if [ -n "$n" ]; then gh api "repos/$REPO/pulls/$n" --jq .html_url; exit 0; fi
    body="$(cat "$bodyfile")$FOOT"
    gh api "repos/$REPO/pulls" -f head="$head" -f base="$base" -f title="$title" -f body="$body" --jq .html_url ;;
  merge)
    n=$(pr_number "$2"); [ -n "$n" ] || { echo "no open PR for $2" >&2; exit 1; }
    gh api -X PUT "repos/$REPO/pulls/$n/merge" -f merge_method=merge --jq '.sha + " " + .message' ;;
  url)
    n=$(pr_number "$2"); [ -n "$n" ] && gh api "repos/$REPO/pulls/$n" --jq .html_url ;;
  comment)
    n=$(pr_number "$2"); [ -n "$n" ] || { echo "no open PR for $2" >&2; exit 1; }
    gh api "repos/$REPO/issues/$n/comments" -f body="$(cat "$3")" --jq .html_url ;;
  *) echo "usage: ghpr.sh open|merge|url|comment ..." >&2; exit 2 ;;
esac
