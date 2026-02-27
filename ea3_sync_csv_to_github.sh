# sync_csv_to_github.sh
#!/usr/bin/env bash
#
# sync_csv_to_github.sh
#
# Copy CSV files into a local GitHub repo's data/ directory, commit, and push.
# Intended to run ON EACH PI (Option 1).
#
# Usage example:
#   ./sync_csv_to_github.sh \
#     --src "/home/pi/EJnPi/PiZ*_ea30_sp26_v05.csv" \
#     --repo "/home/pi/EJnPiRepo" \
#     --branch "main" \
#     --message "Pi data upload" \
#     --tag-with host
#
# Exit codes:
#   0 = success or nothing to do
#   1 = usage or fatal error
#
# Notes:
#   - Requires a local git repo at --repo, with 'origin' remote set to GitHub.
#   - Requires SSH key set up for passwordless push.
#   - Safe to schedule via cron; includes basic retry logic for flaky networks.

set -euo pipefail

# Defaults
BRANCH="main"
COMMIT_MESSAGE="Add CSV data"
TAG_WITH="none"  # none|host|time|both
RETRIES=3
SLEEP_BETWEEN=10

# Parse args
while [[ $# -gt 0 ]]; do
  case "$1" in
    --src) SRC_PATTERN="$2"; shift 2 ;;
    --repo) REPO_PATH="$2"; shift 2 ;;
    --branch) BRANCH="$2"; shift 2 ;;
    --message) COMMIT_MESSAGE="$2"; shift 2 ;;
    --tag-with) TAG_WITH="$2"; shift 2 ;;
    --retries) RETRIES="$2"; shift 2 ;;
    --sleep) SLEEP_BETWEEN="$2"; shift 2 ;;
    -h|--help)
      sed -n '1,120p' "$0"; exit 0 ;;
    *)
      echo "Unknown argument: $1" >&2; exit 1 ;;
  esac
done

# Validate
if [[ -z "${SRC_PATTERN:-}" ]]; then
  echo "ERROR: --src is required (e.g., /home/pi/EJnPi/*.csv)" >&2; exit 1
fi
if [[ -z "${REPO_PATH:-}" ]]; then
  echo "ERROR: --repo is required (e.g., /home/pi/EJnPiRepo)" >&2; exit 1
fi
if [[ ! -d "$REPO_PATH" ]]; then
  echo "ERROR: repo path not found: $REPO_PATH" >&2; exit 1
fi

# Resolve files
shopt -s nullglob
FILES=( $SRC_PATTERN )
shopt -u nullglob

if [[ ${#FILES[@]} -eq 0 ]]; then
  echo "No files matched pattern: $SRC_PATTERN"
  exit 0
fi

# Prepare repo
cd "$REPO_PATH"
if [[ ! -d ".git" ]]; then
  echo "ERROR: $REPO_PATH is not a git repository." >&2; exit 1
fi

# Ensure branch is present locally
git fetch --all --prune >/dev/null 2>&1 || true
if ! git rev-parse --verify "$BRANCH" >/dev/null 2>&1; then
  git switch -c "$BRANCH"
else
  git switch "$BRANCH"
fi

# Ensure data/ exists
mkdir -p data

# Build tag suffix
HOST="$(hostname -s 2>/dev/null || echo pi)"
TIMESTAMP="$(date -u +'%Y%m%dT%H%M%SZ')"
SUFFIX=""
case "$TAG_WITH" in
  host) SUFFIX="__${HOST}" ;;
  time) SUFFIX="__${TIMESTAMP}" ;;
  both) SUFFIX="__${HOST}__${TIMESTAMP}" ;;
  none) SUFFIX="" ;;
  *) echo "Invalid --tag-with option. Use: none|host|time|both" >&2; exit 1 ;;
fi

# Copy files (optionally rename with suffix)
COPIED=0
for f in "${FILES[@]}"; do
  [[ -f "$f" ]] || continue
  base="$(basename "$f")"
  if [[ -n "$SUFFIX" && "$base" == *.* ]]; then
    name="${base%.*}"
    ext="${base##*.}"
    dest="data/${name}${SUFFIX}.${ext}"
  else
    dest="data/${base}"
  fi
  install -m 0644 "$f" "$dest"
  echo "Copied: $f -> $dest"
  ((COPIED++))
done

if [[ $COPIED -eq 0 ]]; then
  echo "Nothing copied; exiting."
  exit 0
fi

# Git add/commit/push (retry on push)
git add data/
if git diff --cached --quiet; then
  echo "No changes to commit."
  exit 0
fi

git commit -m "$COMMIT_MESSAGE"

attempt=1
while :; do
  if git push -u origin "$BRANCH"; then
    echo "✅ Push succeeded on attempt $attempt"
    break
  fi
  if (( attempt >= RETRIES )); then
    echo "❌ Push failed after $RETRIES attempts."
    exit 1
  fi
  echo "⚠️ Push failed; retrying in $SLEEP_BETWEEN sec (attempt $((attempt+1))/$RETRIES)..."
  sleep "$SLEEP_BETWEEN"
  ((attempt++))
done

echo "✅ Done: pushed $COPIED file(s) to branch '$BRANCH' in $(basename "$REPO_PATH")"
