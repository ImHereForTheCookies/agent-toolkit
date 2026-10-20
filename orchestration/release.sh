#!/usr/bin/env bash
# Cut a release of one project folder: verify, build, tag <slug>-vN, and move the
# release/<slug> branch forward to that commit. Never force-pushes, never moves a
# release backward, never deploys (a host Robert configures may watch the branch).
#
# Usage (from anywhere):  release.sh <repo> <folder> <slug> [--notes FILE]
#   <repo>    checkout of the repo (main is checked out at origin/main by the script)
#   <folder>  project folder relative to the repo ("." for the repo root project)
#   <slug>    release name prefix, e.g. "cajunt" -> tags cajunt-v1, cajunt-v2 ...
# Exit codes: 0 released, 3 nothing to release (no changes since the last tag),
#             1 failure (verify/build failed, or a push was rejected).
# Env: RELEASE_SKIP_FETCH=1 skips the initial fetch (tests).
set -euo pipefail

repo=$1 folder=$2 slug=$3
notes_out=""
if [ "${4:-}" = "--notes" ]; then notes_out=$5; fi
cd "$repo"

if [ -z "${RELEASE_SKIP_FETCH:-}" ]; then
  git fetch -q origin main
  git fetch -q --tags origin
  git checkout -q -B main origin/main
fi
[ -z "$(git status --porcelain)" ] || { echo "release: working tree not clean" >&2; exit 1; }

# The root project excludes the pocs/ folders (they release on their own).
if [ "$folder" = "." ]; then paths=(. ':(exclude)pocs'); else paths=("$folder"); fi

last=$(git tag -l "${slug}-v*" | sed "s/^${slug}-v//" | grep -E '^[0-9]+$' | sort -n | tail -1 || true)
if [ -n "$last" ]; then
  if git diff --quiet "${slug}-v${last}" HEAD -- "${paths[@]}"; then
    echo "release: nothing to release for $slug since ${slug}-v${last}"
    exit 3
  fi
  range="${slug}-v${last}..HEAD"
  next=$((last + 1))
else
  range="HEAD"
  next=1
fi

has_target() { make -C "$folder" -n "$1" >/dev/null 2>&1; }
if has_target setup; then make -C "$folder" setup; fi
make -C "$folder" verify
built=""
if has_target build; then make -C "$folder" build; built=" and make build"; fi

tag="${slug}-v${next}"
sha=$(git rev-parse HEAD)
changes=$(git log --no-merges --format='- %s' $range -- "${paths[@]}" | head -50)
msg="$tag

Verified with make verify${built} at $sha.

Changes since ${last:+${slug}-v${last}}${last:-the start}:
$changes"

git tag -a "$tag" -m "$msg" "$sha"
git push -q origin "refs/tags/$tag"
# Fast-forward only: a plain push is rejected if release/<slug> isn't an ancestor of $sha.
git push -q origin "$sha:refs/heads/release/$slug"

if [ -n "$notes_out" ]; then printf '%s\n' "$msg" > "$notes_out"; fi
echo "release: $tag at $sha (release/$slug updated)"
