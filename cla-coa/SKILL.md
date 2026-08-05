---
name: cla-coa
description: Install and verify the portable `cla` and `coa` shell launchers for Claude Code automatic permission mode and Codex no-prompt approval mode on macOS or Linux. Use when a user asks for Claude Auto, Codex Auto, shorter commands for either CLI, automatic approval launchers, `cla` or `coa`, or wants these wrappers installed, repaired, updated, or checked.
---

# Claude and Codex Auto Launchers

Install both launchers with the bundled script and verify the underlying CLIs when available.

## Safety

- Explain that `cla` reduces Claude permission prompts and `coa` disables Codex approval prompts.
- Keep Codex in `workspace-write` sandbox mode. Do not replace it with `danger-full-access` or the dangerous bypass flag.
- Do not install Claude Code or Codex itself unless the user separately requests it.

## Install

Resolve `<skill-dir>` to the directory containing this `SKILL.md`, then run:

```sh
sh "<skill-dir>/scripts/install.sh"
```

The script installs into `$INSTALL_DIR` when set, otherwise `$HOME/.local/bin`. It safely replaces only the `cla` and `coa` files in that directory.

## Verify

Confirm the files are executable:

```sh
test -x "${INSTALL_DIR:-$HOME/.local/bin}/cla"
test -x "${INSTALL_DIR:-$HOME/.local/bin}/coa"
```

If `claude` is installed, run `cla --version`. If `codex` is installed, run `coa --version`. If the install directory is not on `PATH`, report the exact directory and tell the user to add it.

## Behavior

- `cla` executes `claude --permission-mode auto` and forwards every supplied argument.
- `coa` executes `codex --ask-for-approval never --sandbox workspace-write` and forwards every supplied argument.
