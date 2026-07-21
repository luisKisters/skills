---
name: hyperkey-setup
description: Set up Karabiner-Elements on macOS with bundled Caps Lock Hyperkey and right Shift launcher shortcuts, including installation, permissions, rule activation, and verification. Use when a user asks to install or configure Karabiner-Elements, set up a Hyperkey, map a tapped Caps Lock to Cmd+Tab, map a tapped right Shift to Cmd+Space or Raycast, or restore this specific keyboard configuration.
---

# Hyperkey Setup

Follow this workflow in order. Prefer shell commands for every action they can perform, and use computer control only for required Karabiner or macOS UI interactions that have no command-line path. Stop only for required user confirmations or macOS permission dialogs.

## Safety

- Always ask before installing software or overwriting a file.
- Never modify `~/.config/karabiner/karabiner.json` directly. Only write to `~/.config/karabiner/assets/complex_modifications/`.
- Copy the bundled `hyperkey.json`; do not regenerate or rewrite its contents.

## 1. Check Karabiner-Elements

Run both checks:

```sh
ls /Applications
brew list --cask karabiner-elements
```

Treat `/Applications/Karabiner-Elements.app` or a successful Homebrew cask lookup as installed. If `brew` is unavailable, continue to the Homebrew-missing branch below rather than treating that command failure as an installation failure by itself.

## 2. Install When Missing

Check for Homebrew:

```sh
command -v brew
```

If Homebrew exists, ask the user to confirm installing Karabiner-Elements. Only after confirmation, run:

```sh
brew install --cask karabiner-elements
```

If Homebrew is missing, do not install it automatically. Ask whether the user wants to install Homebrew or download Karabiner-Elements manually from `https://karabiner-elements.pqrs.org`, then wait for their choice and for the selected installation to finish.

## 3. Copy the Bundled Configuration

Resolve `<skill-dir>` to the directory containing this `SKILL.md`. Check whether the destination already exists:

```sh
test -e "$HOME/.config/karabiner/assets/complex_modifications/hyperkey.json"
```

If it exists, ask before overwriting and stop unless the user confirms. Then create the assets directory and copy the bundled file:

```sh
mkdir -p "$HOME/.config/karabiner/assets/complex_modifications"
cp "<skill-dir>/hyperkey.json" "$HOME/.config/karabiner/assets/complex_modifications/hyperkey.json"
```

Do not use a heredoc or generate a replacement file.

## 4. Grant Permissions and Enable Rules

Karabiner-Elements needs Input Monitoring permission, and both bundled rules must be enabled.

If a computer-use tool is available, use it only where the UI is unavoidable:

1. Run `open -a "Karabiner-Elements"` in the shell. Do not use computer control to perform checks, installation, file copying, or application launching that commands can handle.
2. Use computer control to navigate Karabiner's initial setup to the screen that requests Input Monitoring or other macOS security permissions.
3. Ask the user to approve the macOS permission dialogs. Do not attempt to automate those dialogs; wait until the user confirms completion.
4. Use computer control to navigate to Karabiner-Elements Settings -> Complex Modifications -> Add predefined rule because enabling rules cannot be done through the assets-file copy and this skill must not edit `karabiner.json`.
5. Find `Hyperkey setup (Caps Lock -> Hyper / Cmd+Tab, Right Shift -> Raycast)`, enable both rules, and confirm they appear under Complex Modifications.

If no computer-use tool is available, print these instructions and wait for confirmation after each numbered step before continuing:

1. Open Karabiner-Elements and complete its initial setup prompts. Confirm when done.
2. Open System Settings -> Privacy & Security -> Input Monitoring, enable every Karabiner component requested by macOS, and approve any restart prompts. Confirm when done.
3. Open Karabiner-Elements Settings -> Complex Modifications -> Add predefined rule. Confirm when the predefined-rule list is visible.
4. Find `Hyperkey setup (Caps Lock -> Hyper / Cmd+Tab, Right Shift -> Raycast)` and enable `Caps Lock -> Hyper (held + key) / Cmd+Tab (tap)`. Confirm when enabled.
5. Enable `Right Shift -> Cmd+Space (tap) / normal shift (held)`. Confirm when enabled.

## 5. Verify

Ask the user to perform both tests:

1. Tap Caps Lock. It should trigger the Cmd+Tab app switcher.
2. Tap right Shift. It should trigger Cmd+Space.

If the user uses Raycast, remind them to set Raycast's hotkey to Cmd+Space and disable Spotlight's Cmd+Space shortcut so the two do not conflict.
