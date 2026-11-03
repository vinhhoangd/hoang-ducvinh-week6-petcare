#!/bin/bash
# Build Team3-Week6-4.zip from a copy of project-workspace/ (START-HERE "Submission Instructions").
# Run from anywhere:  ./make-submission-zip.sh [output-folder]
# Leaves out: .env, the Python environments, caches, and the ADI501-only templates (we are ADI201).
# Refuses to build if the Census key appears anywhere in the copy.
set -euo pipefail
cd "$(dirname "$0")"
OUT_DIR="${1:-$PWD}"
NAME=Team3-Week6-4
STAGE=$(mktemp -d)
trap 'rm -rf "$STAGE"' EXIT

rsync -a \
  --exclude '.env' --exclude '*.env' --exclude '.venv' --exclude '.venv/' \
  --exclude '.venv-offloaded-by-icloud/' --exclude '__pycache__/' --exclude '.DS_Store' \
  --exclude 'evidence/source-quality-adoption.md' --exclude 'evidence/governance-controls.md' \
  --exclude 'evidence/model-risk-note.md' --exclude 'evidence/pilot-recommendation.md' \
  project-workspace/ "$STAGE/project-workspace/"

KEY=$(grep -m1 '^CENSUS_API=' project-workspace/.env 2>/dev/null | cut -d= -f2- | tr -d '[:space:]' || true)
if [ -n "$KEY" ] && grep -rqF -- "$KEY" "$STAGE"; then
  echo "STOP: the Census key appears in the copy. Nothing was zipped."; exit 1
fi
if find "$STAGE" -name '.env' -o -name '*.env' | grep -q .; then
  echo "STOP: an .env file is in the copy. Nothing was zipped."; exit 1
fi

rm -f "$OUT_DIR/$NAME.zip"
(cd "$STAGE" && zip -r -X -q "$OUT_DIR/$NAME.zip" project-workspace)
echo "Created $OUT_DIR/$NAME.zip — key search: 0 hits, no .env"
unzip -l "$OUT_DIR/$NAME.zip" | tail -1
