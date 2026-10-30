#!/usr/bin/env bash
# Cut a release of one project folder: verify, build, create the frozen branch
# release/<slug>-vN at that commit, and move the release/<slug> branch forward to it.
# Releases are branches, not tags: cloud sessions may only push branches (their
# GitHub proxy refuses tag pushes), so a version is a branch that is never moved again.
# Never force-pushes, never moves a release backward, never deploys (a host the owner
# configures may watch release/<slug>).
#
# Usage (from anywhere):  release.sh <repo> <folder> <slug> [--notes FILE]
#   <repo>    checkout of the repo (main is checked out at origin/main by the script)
#   <folder>  project folder relative to the repo ("." for the repo root project)
#   <slug>    release name prefix, e.g. "cajunt" -> release/cajunt-v1, release/cajunt-v2 ...
# Exit codes: 0 released, 3 nothing to release (no changes since the last version),
#             1 failure (verify/build failed, or a push was rejected).
# Env: RELEASE_SKIP_FETCH=1 skips fetching main (tests).
set -euo pipefail

repo=$1 folder=$2 slug=$3
notes_out=""
if [ "${4:-}" = "--notes" ]; then notes_out=$5; fi
cd "$repo"

if [ -z "${RELEASE_SKIP_FETCH:-}" ]; then
  git fetch -q origin main
  git checkout -q -B main origin/main
fi
[ -z "$(git status --porcelain)" ] || { echo "release: working tree not clean" >&2; exit 1; }

# The root project excludes the pocs/ folders (they release on their own).
if [ "$folder" = "." ]; then paths=(. ':(exclude)pocs'); else paths=("$folder"); fi

# Versions live on the remote as release/<slug>-v<N> branches.
remote_heads=$(git ls-remote --heads origin "refs/heads/release/${slug}*")
remote_sha() { printf '%s\n' "$remote_heads" | awk -v r="refs/heads/$1" '$2 == r {print $1}'; }
last=$(printf '%s\n' "$remote_heads" | awk '{print $2}' \
  | sed -n "s|^refs/heads/release/${slug}-v\([0-9][0-9]*\)$|\1|p" | sort -n | tail -1)

# Make sure a commit from the remote is present locally (shallow clones may lack it).
have_commit() {
  git cat-file -e "$1^{commit}" 2>/dev/null && return 0
  git fetch -q origin "refs/heads/$2" && git cat-file -e "$1^{commit}"
}

if [ -n "$last" ]; then
  last_branch="release/${slug}-v${last}"
  last_sha=$(remote_sha "$last_branch")
  have_commit "$last_sha" "$last_branch"
  if git diff --quiet "$last_sha" HEAD -- "${paths[@]}"; then
    # Repair a cut whose second push failed: point release/<slug> at the last version.
    if [ "$(remote_sha "release/$slug")" != "$last_sha" ]; then
      git push -q origin "$last_sha:refs/heads/release/$slug"
      echo "release: release/$slug moved to ${last_branch} ($last_sha)"
      exit 0
    fi
    echo "release: nothing to release for $slug since ${last_branch}"
    exit 3
  fi
  range="${last_sha}..HEAD"
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

version="${slug}-v${next}"
sha=$(git rev-parse HEAD)
changes=$(git log --no-merges --format='- %s' $range -- "${paths[@]}" | head -50)
msg="$version (branch release/$version)

Verified with make verify${built} at $sha.

Changes since ${last:+${slug}-v${last}}${last:-the start}:
$changes"

# vN is one past the highest version on the remote, so this push creates a new branch.
git push -q origin "$sha:refs/heads/release/$version"
# Fast-forward only: a plain push is rejected if release/<slug> isn't an ancestor of $sha.
git push -q origin "$sha:refs/heads/release/$slug"

if [ -n "$notes_out" ]; then printf '%s\n' "$msg" > "$notes_out"; fi
echo "release: $version at $sha (release/$version created, release/$slug updated)"
