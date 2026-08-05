#!/bin/sh
set -eu

install_dir=${INSTALL_DIR:-"$HOME/.local/bin"}
mkdir -p "$install_dir"

cla_tmp="$install_dir/.cla.$$"
coa_tmp="$install_dir/.coa.$$"
trap 'rm -f "$cla_tmp" "$coa_tmp"' EXIT HUP INT TERM

printf '%s\n' \
  '#!/bin/sh' \
  'if ! command -v claude >/dev/null 2>&1; then' \
  '  echo "cla: Claude Code is not installed or is not on PATH" >&2' \
  '  exit 127' \
  'fi' \
  'exec claude --permission-mode auto "$@"' >"$cla_tmp"

printf '%s\n' \
  '#!/bin/sh' \
  'if ! command -v codex >/dev/null 2>&1; then' \
  '  echo "coa: Codex CLI is not installed or is not on PATH" >&2' \
  '  exit 127' \
  'fi' \
  'exec codex --ask-for-approval never --sandbox workspace-write "$@"' >"$coa_tmp"

chmod 755 "$cla_tmp" "$coa_tmp"
mv "$cla_tmp" "$install_dir/cla"
mv "$coa_tmp" "$install_dir/coa"
trap - EXIT HUP INT TERM

printf 'Installed cla and coa in %s\n' "$install_dir"
case ":$PATH:" in
  *":$install_dir:"*) ;;
  *) printf 'Add %s to PATH to use cla and coa directly.\n' "$install_dir" ;;
esac
