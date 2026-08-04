# Hyperkey Setup

This skill installs or configures Karabiner-Elements with bundled Caps Lock Hyperkey and right Shift launcher shortcuts. An agent triggers it when a user asks for this keyboard setup or asks to restore its specific mappings.

## Install

```sh
npx skills add github.com/luisKisters/skills --skill hyperkey-setup
```

If the CLI is unavailable, clone or download the repository and copy the skill directory into the agent's skills directory, for example `cp -R hyperkey ~/.codex/skills/hyperkey-setup`.
