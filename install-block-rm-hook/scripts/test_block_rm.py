#!/usr/bin/env python3

import json
from pathlib import Path
import subprocess
import sys


BLOCKED = [
    "rm -rf /tmp/example",
    "echo ready && rm file.txt",
    "sudo rm -f file.txt",
    "sudo -u root rm -f file.txt",
    "nice -n 5 rm -f file.txt",
    "env -u TMPDIR rm -f file.txt",
    "/bin/rm file.txt",
    "find . -name junk -exec rm {} ;",
    "xargs rm < files.txt",
    "bash -c 'rm -f file.txt'",
]

ALLOWED = [
    "git rm file.txt",
    "npm rm package-name",
    "yarn rm package-name",
    "pnpm rm package-name",
    "cat rm-notes.txt",
    "printf '%s\\n' rm",
    "echo 'rm -rf is dangerous'",
    "command -v rm",
]


def denied(hook: Path, command: str) -> bool:
    payload = json.dumps({"tool_name": "Bash", "tool_input": {"command": command}})
    result = subprocess.run(
        [str(hook)],
        input=payload,
        text=True,
        capture_output=True,
        check=True,
    )
    if not result.stdout.strip():
        return False
    output = json.loads(result.stdout)
    return output.get("hookSpecificOutput", {}).get("permissionDecision") == "deny"


def main() -> int:
    hook = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name("block-rm.sh")
    failures = []
    for command in BLOCKED:
        if not denied(hook, command):
            failures.append(f"expected deny: {command}")
    for command in ALLOWED:
        if denied(hook, command):
            failures.append(f"expected allow: {command}")

    if failures:
        print("FAIL")
        print("\n".join(failures))
        return 1
    print(f"PASS: {len(BLOCKED)} blocked and {len(ALLOWED)} allowed cases")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
