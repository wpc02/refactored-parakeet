#!/bin/sh
# Auto add/commit/push when triggered by git status via core.fsmonitor
cd "/c/git repository" || exit 0

if [ -f ".git/pushing" ]; then
    exit 0
fi

touch ".git/pushing"

git add .
git commit -m "Initial commit" 2>/dev/null || true
git push -u origin main 2>/dev/null || true

rm -f ".git/pushing"
exit 0
