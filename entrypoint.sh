#!/usr/bin/env bash
# Container entrypoint.
#
#   build      one-shot: build SvelteKit from existing cache, then exit
#   scheduler  long-running: refreshes cache + builds + pushes every Wednesday at 03:00 (TZ-local)
#
# Output goes to stdout/stderr so `docker compose logs -f` works without extra plumbing.
set -euo pipefail
cd /app

mode="${1:-build}"

log() { printf '[%s] %s\n' "$(date -u +%FT%TZ)" "$*"; }

setup_git() {
  git config --global --add safe.directory /app
  git config --global user.email "${GIT_EMAIL:-jeongbin.park@pusan.ac.kr}"
  git config --global user.name "${GIT_NAME:-Jeongbin Park}"
}

push_changes() {
  log "pushing cache changes to svelte branch"
  git add cache/gscache.txt cache/cofirsts_cocorrespondence_cache.txt cache/stats.json
  git diff --cached --quiet || git commit -m "Update cache files" && git push origin svelte || log "cache push failed (non-fatal)"

  log "pushing build to gh-pages branch"
  # clean up any previous worktree
  rm -rf /tmp/gh-pages
  git worktree add /tmp/gh-pages gh-pages 2>/dev/null || {
    git fetch origin gh-pages
    git worktree add /tmp/gh-pages gh-pages
  }
  cp -r build/* /tmp/gh-pages/
  cd /tmp/gh-pages
  git add .
  git diff --cached --quiet || {
    git commit -m "Update website"
    git push origin gh-pages
  }
  cd /app
  git worktree remove /tmp/gh-pages 2>/dev/null || true
  log "push complete"
}

full_build() {
  log "refreshing citations from Google Scholar"
  uv run cache/get_citations.py
  log "building SvelteKit site"
  /app/build.sh
  setup_git
  push_changes
}

case "$mode" in
  build)
    exec /app/build.sh
    ;;

  scheduler)
    TARGET_DOW="${BUILD_DOW:-3}"      # 1=Mon..7=Sun (Wed=3)
    TARGET_HOUR="${BUILD_HOUR:-03}"
    LAST_RUN=/app/cache/.last-scheduled-run

    ran_today() {
      [ -f "$LAST_RUN" ] || return 1
      [ "$(cat "$LAST_RUN")" = "$(date -I)" ]
    }
    mark_ran() { date -I > "$LAST_RUN"; }

    log "scheduler started — building every week on DOW=${TARGET_DOW} at ${TARGET_HOUR}:00 (TZ=${TZ:-UTC})"
    log "scheduler PID=$$ — Ctrl-C / docker stop will terminate"

    # Initial build on first run
    log "initial run"
    full_build && mark_ran || log "initial build FAILED"

    while true; do
      dow=$(date +%u)
      hr=$(date +%H)
      if [ "$dow" = "$TARGET_DOW" ] && [ "$hr" = "$TARGET_HOUR" ] && ! ran_today; then
        log "weekly trigger fired"
        if full_build; then
          mark_ran
          log "weekly build complete"
        else
          log "build FAILED — will retry next week"
        fi
      fi
      sleep 60
    done
    ;;

  *)
    log "unknown mode: $mode (use 'build' or 'scheduler')"
    exit 64
    ;;
esac
