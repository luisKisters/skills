#!/usr/bin/env python3

import argparse
import json
import os
from pathlib import Path
import stat
import tempfile


def write_atomic(path: Path, data: bytes, mode: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        temporary.chmod(mode)
        temporary.replace(path)
    except BaseException:
        temporary.unlink(missing_ok=True)
        raise


def main() -> int:
    parser = argparse.ArgumentParser(description="Install the Claude Code block-rm hook")
    parser.add_argument("--home", type=Path, default=Path.home())
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    home = args.home.expanduser().resolve()
    source_hook = Path(__file__).with_name("block-rm.sh")
    claude_dir = home / ".claude"
    target_hook = claude_dir / "hooks" / "block-rm.sh"
    settings_path = claude_dir / "settings.json"

    if settings_path.exists():
        settings = json.loads(settings_path.read_text())
        if not isinstance(settings, dict):
            raise ValueError(f"{settings_path} must contain a JSON object")
    else:
        settings = {}

    command = str(target_hook)
    hook = {
        "matcher": "Bash",
        "hooks": [
            {
                "type": "command",
                "command": command,
            }
        ],
    }
    hooks = settings.setdefault("hooks", {})
    if not isinstance(hooks, dict):
        raise ValueError(f"{settings_path}: hooks must be a JSON object")
    pre_tool_use = hooks.setdefault("PreToolUse", [])
    if not isinstance(pre_tool_use, list):
        raise ValueError(f"{settings_path}: hooks.PreToolUse must be a JSON array")

    already_configured = any(
        isinstance(group, dict)
        and group.get("matcher") == "Bash"
        and any(
            isinstance(handler, dict) and handler.get("command") == command
            for handler in group.get("hooks", [])
        )
        for group in pre_tool_use
    )
    if not already_configured:
        pre_tool_use.append(hook)

    settings_data = (json.dumps(settings, indent=2) + "\n").encode()
    hook_data = source_hook.read_bytes()

    if args.dry_run:
        print(f"Would install {target_hook}")
        print(f"Would update {settings_path}")
        return 0

    hook_mode = stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH
    write_atomic(target_hook, hook_data, hook_mode)
    settings_mode = stat.S_IMODE(settings_path.stat().st_mode) if settings_path.exists() else 0o600
    write_atomic(settings_path, settings_data, settings_mode)

    print(f"Installed {target_hook}")
    print(f"Updated {settings_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
