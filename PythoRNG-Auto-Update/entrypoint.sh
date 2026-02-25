#!/bin/bash
set -e

echo "Starting auto-update application..."
echo ""

cd /app || exit 1

if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs) || true
fi

if [ -z "$WEBHOOK_URL" ]; then
    echo "Enter Discord webhook URL (or leave blank to skip):"
    read -r WEBHOOK_URL_INPUT
    if [ -n "$WEBHOOK_URL_INPUT" ]; then
        echo "WEBHOOK_URL=$WEBHOOK_URL_INPUT" >> .env
        export WEBHOOK_URL="$WEBHOOK_URL_INPUT"
    fi
fi

if [ -z "$GITHUB_USERNAME" ] || [ -z "$GITHUB_REPO" ]; then
    echo "ERROR: Set GITHUB_USERNAME and GITHUB_REPO in .env"
    exit 1
fi

GITHUB_REPO_URL="https://github.com/${GITHUB_USERNAME}/${GITHUB_REPO}.git"
BRANCH=${GITHUB_BRANCH:-main}
UPDATE_INTERVAL=${UPDATE_CHECK_INTERVAL:-0}

pull_repo(){
    if [ -d ".git" ]; then
        git fetch origin
        git checkout "$BRANCH" || true
        git pull origin "$BRANCH" || true
    else
        git clone --branch "$BRANCH" "$GITHUB_REPO_URL" .
    fi
}

pull_repo

start_apps(){
    cd /app || return
    python main.py &
    MAIN_PID=$!

    cd /app/Macro || return
    python PythoRNG.py &
    LAUNCHER_PID=$!
}

stop_apps(){
    kill ${MAIN_PID:-0} ${LAUNCHER_PID:-0} 2>/dev/null || true
    wait ${MAIN_PID:-0} ${LAUNCHER_PID:-0} 2>/dev/null || true
}

start_apps

if [ "$UPDATE_INTERVAL" -gt 0 ]; then
    while true; do
        sleep "$UPDATE_INTERVAL"
        cd /app || continue
        git fetch origin || continue
        LOCAL=$(git rev-parse @ 2>/dev/null || echo)
        REMOTE=$(git rev-parse origin/"$BRANCH" 2>/dev/null || echo)
        if [ "$LOCAL" != "$REMOTE" ]; then
            stop_apps
            pull_repo
            start_apps
        fi
    done
else
    wait ${MAIN_PID:-0} ${LAUNCHER_PID:-0}
fi