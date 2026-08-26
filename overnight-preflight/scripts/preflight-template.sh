#!/usr/bin/env bash
# Unattended-run preflight. Copy into <repo>/scripts/preflight.sh and adapt the
# PROJECT SPECIFIC blocks. The mechanics above them are the part worth keeping.
#
# Answers one question: can an agent run this repo for hours with nobody at the
# keyboard? It never asks anything, never runs sudo, never opens a GUI, and puts
# a timeout on every command so a hung tool cannot swallow the night.
#
# Exit 0  ready to walk away (possibly degraded, always with a documented workaround)
# Exit 1  a human is needed first; the decisions are listed at the bottom
set -uo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

DEVELOPER_DIR="${DEVELOPER_DIR:-/Applications/Xcode.app/Contents/Developer}"
export DEVELOPER_DIR
export CLANG_MODULE_CACHE_PATH="$REPO_ROOT/.build/clang-module-cache"
export SWIFTPM_MODULECACHE_OVERRIDE="$REPO_ROOT/.build/swiftpm-module-cache"

BLOCKERS=()   # a human must act
DEGRADED=()   # works around it and keeps running
DECISIONS=()  # needs a yes/no from the owner before they sleep

ok()       { echo "[preflight] OK        $*"; }
degrade()  { echo "[preflight] DEGRADED  $*"; DEGRADED+=("$*"); }
block()    { echo "[preflight] BLOCKED   $*"; BLOCKERS+=("$*"); }
decide()   { DECISIONS+=("$*"); }

# run_with_timeout <seconds> <command...>
# macOS ships no coreutils `timeout`. Exit 124 means it was killed.
run_with_timeout() {
    local seconds="$1"; shift
    "$@" >/tmp/preflight-last.txt 2>&1 &
    local pid=$!
    ( sleep "$seconds"; kill -9 "$pid" 2>/dev/null ) >/dev/null 2>&1 &
    local watchdog=$!
    disown "$watchdog" 2>/dev/null
    wait "$pid"; local status=$?
    kill "$watchdog" 2>/dev/null
    if [[ $status -ge 128 ]]; then return 124; fi
    return $status
}

echo "[preflight] == Toolchain =="

if [[ -d "$DEVELOPER_DIR" ]]; then
    ok "Xcode toolchain at $DEVELOPER_DIR"
else
    block "No Xcode at $DEVELOPER_DIR. XCTest does not ship with the Command Line Tools, so no test can run. Install Xcode."
fi

if run_with_timeout 600 xcrun swift build --disable-sandbox; then
    ok "swift build"
else
    block "swift build fails. Nothing can proceed. Last output: $(tail -3 /tmp/preflight-last.txt | tr '\n' ' ')"
fi

# Anything needing a password stops an unattended run dead. Nothing here may use it.
if sudo -n true 2>/dev/null; then
    ok "sudo is passwordless (unused anyway)"
else
    ok "sudo would prompt; no step in this repo uses it"
fi

FREE_GB=$(df -g "$REPO_ROOT" | awk 'NR==2 {print $4}')
if [[ "${FREE_GB:-0}" -ge 5 ]]; then
    ok "disk ${FREE_GB} GB free"
else
    block "Only ${FREE_GB} GB free. Builds and snapshots will fail overnight."
fi

echo "[preflight] == Model access =="

# The decisive check: one real round trip. A key that is missing, revoked or out of
# credit fails every single classification, and nothing else in the run would notice.
KEY="${OPENROUTER_API_KEY:-}"
if [[ -z "$KEY" && -f "$HOME/Library/Application Support/Anchr/openrouter-key" ]]; then
    KEY="$(tr -d '[:space:]' < "$HOME/Library/Application Support/Anchr/openrouter-key")"
fi
if [[ -z "$KEY" ]] && command -v op >/dev/null 2>&1; then
    # Best effort only: op needs an interactive unlock, so a failure here is normal
    # in an unattended shell and must never block.
    if run_with_timeout 20 op read "op://Personal/Anchr OpenRouter API Key/credential"; then
        CANDIDATE="$(tr -d '[:space:]' < /tmp/preflight-last.txt)"
        [[ "$CANDIDATE" == sk-or-* ]] && KEY="$CANDIDATE"
    fi
fi

if [[ -z "$KEY" ]]; then
    block "No OpenRouter key. Set OPENROUTER_API_KEY, or paste one into onboarding, or store it at ~/Library/Application Support/Anchr/openrouter-key. Every classification fails without it."
else
    MODEL="${ANCHR_OPENROUTER_MODEL:-google/gemini-2.5-flash}"
    PROBE=/tmp/preflight-model.json
    if run_with_timeout 60 curl -sS --max-time 45 https://openrouter.ai/api/v1/chat/completions \
        -H "Authorization: Bearer $KEY" -H "Content-Type: application/json" \
        -d "{\"model\":\"$MODEL\",\"messages\":[{\"role\":\"user\",\"content\":\"Reply with ok\"}],\"max_tokens\":16}"
    then
        cp /tmp/preflight-last.txt "$PROBE" 2>/dev/null
        if grep -q '"error"' "$PROBE" 2>/dev/null; then
            REASON="$(python3 -c "
import json,sys
try:
    print(json.load(open('$PROBE'))['error'].get('message','unknown'))
except Exception:
    print('unparsable error')" 2>/dev/null)"
            block "OpenRouter rejected the request: $REASON"
        else
            ok "OpenRouter round trip with $MODEL"
        fi
    else
        degrade "OpenRouter did not answer in time. Offline work continues; live-model tests will fail."
    fi
fi

echo "[preflight] == Accessibility =="

if run_with_timeout 300 xcrun swift run --disable-sandbox ax-probe --front; then
    CHARS=$(grep -oE 'chars: [0-9]+' /tmp/preflight-last.txt | head -1)
    ok "accessibility read works (${CHARS:-unknown})"
else
    # Not a blocker: every live-AX test is opt-in and skips itself. Kit work continues.
    degrade "Accessibility read failed (sandboxed shell, or the grant was reset). ANCHR_LIVE_AX tests will skip; all Kit and headless work still runs. Grant it in System Settings > Privacy & Security > Accessibility."
fi

echo "[preflight] == GUI tests =="

if command -v xcodegen >/dev/null 2>&1; then
    ok "xcodegen present; XCUITest project can be generated"
else
    degrade "xcodegen is missing, so the GUI smoke cannot run. Headless suites are unaffected. Install with: brew install xcodegen"
fi

echo "[preflight] == Staying awake =="

if [[ -x /usr/bin/caffeinate ]]; then
    ok "caffeinate present (wrap long runs in: caffeinate -dimsu <command>)"
else
    degrade "No caffeinate. The machine may sleep mid-run."
fi

echo "[preflight] == Git =="

if run_with_timeout 30 git ls-remote --exit-code origin HEAD; then
    ok "origin reachable without a prompt"
else
    degrade "Cannot reach origin non-interactively. Work stays local; commits are not pushed."
fi

echo "[preflight] == Decisions only the owner can make =="

# Design snapshot baselines are approved once, by a human, against the prototype.
# An agent must never approve its own baseline.
SNAPSHOT_DIR="$REPO_ROOT/design/snapshots"
APPROVAL="$SNAPSHOT_DIR/APPROVED"
if [[ -d "$SNAPSHOT_DIR" ]]; then
    UNAPPROVED=()
    for png in "$SNAPSHOT_DIR"/*.png; do
        [[ -e "$png" ]] || continue
        name="$(basename "$png")"
        if [[ ! -f "$APPROVAL" ]] || ! grep -qxF "$name" "$APPROVAL"; then
            UNAPPROVED+=("$name")
        fi
    done
    if [[ ${#UNAPPROVED[@]} -gt 0 ]]; then
        decide "Approve ${#UNAPPROVED[@]} design snapshot baseline(s) against design/mockups/v2/interactive.html, then list them in design/snapshots/APPROVED: ${UNAPPROVED[*]}"
    else
        ok "all design snapshot baselines approved"
    fi
fi

# Tasks that need the owner at the keyboard cannot run overnight, by definition.
# Everything else, including the GUI suite, is fair game for an unattended run.
decide "The corpus task and the full product run need you present (30 real work snapshots; a live 20-minute drift session). An unattended run must stop before those and report."

echo
echo "──────────────────────────────────────────────"
if [[ ${#DEGRADED[@]} -gt 0 ]]; then
    echo "Degraded, with a workaround in place:"
    for d in "${DEGRADED[@]}"; do echo "  - $d"; done
    echo
fi
if [[ ${#DECISIONS[@]} -gt 0 ]]; then
    echo "Decide before you sleep:"
    for d in "${DECISIONS[@]}"; do echo "  - $d"; done
    echo
fi
if [[ ${#BLOCKERS[@]} -gt 0 ]]; then
    echo "BLOCKED. A human must act first:"
    for b in "${BLOCKERS[@]}"; do echo "  - $b"; done
    exit 1
fi
echo "Ready to run unattended."
exit 0
