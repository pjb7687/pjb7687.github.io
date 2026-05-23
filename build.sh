#!/usr/bin/env bash
# Build the SvelteKit site from the existing cache.
#
# To refresh citations from Google Scholar, run separately:
#   uv run cache/get_citations.py
#
# Outputs:
#   build/   — static site, ready to publish on the gh-pages branch.
set -euo pipefail

cd "$(dirname "$0")"

ts() { date -u +"%Y-%m-%dT%H:%M:%SZ"; }
log() { printf '[%s] %s\n' "$(ts)" "$*"; }

log "Installing node dependencies"
pnpm install -y

log "Building SvelteKit site"
pnpm build

log "Writing CNAME"
echo "jeongbinpark.com" > build/CNAME
touch build/.nojekyll

log "Build complete — output in ./build"
