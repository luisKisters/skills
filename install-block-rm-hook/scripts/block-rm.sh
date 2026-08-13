#!/bin/sh

set -eu

python3 -c '
import json
import os
import re
import shlex
import sys


def tokens(command):
    lexer = shlex.shlex(command, posix=True, punctuation_chars=";&|()<>\n")
    lexer.whitespace = " \t\r"
    lexer.whitespace_split = True
    lexer.commenters = ""
    return list(lexer)


def invokes_rm(command):
    try:
        words = tokens(command)
    except ValueError:
        return False

    separators = {";", ";;", ";&", ";;&", "&&", "||", "|", "|&", "&", "\n", "(", ")"}
    command_keywords = {"if", "then", "elif", "else", "while", "until", "do", "!", "{"}
    prefixes = {"command", "builtin", "exec", "env", "nohup", "sudo", "time", "nice", "noglob"}
    prefix_options_with_values = {
        "env": {"-C", "-S", "-u", "--chdir", "--split-string", "--unset"},
        "nice": {"-n", "--adjustment"},
        "sudo": {"-C", "-g", "-h", "-p", "-R", "-T", "-u", "--chdir", "--chroot", "--command-timeout", "--group", "--host", "--prompt", "--user"},
        "time": {"-f", "-o", "--format", "--output"},
    }
    shells = {"bash", "dash", "ksh", "sh", "zsh"}
    expect_command = True
    command_name = None
    prefix_value_pending = False
    previous = None

    for word in words:
        if word in separators:
            expect_command = True
            command_name = None
            prefix_value_pending = False
            previous = word
            continue

        if word in command_keywords:
            expect_command = True
            command_name = None
            prefix_value_pending = False
            previous = word
            continue

        if expect_command:
            if prefix_value_pending:
                prefix_value_pending = False
                previous = word
                continue
            if re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", word):
                previous = word
                continue
            if word.startswith("-") and command_name in prefixes:
                if command_name == "command" and word in {"-v", "-V"}:
                    expect_command = False
                if word in prefix_options_with_values.get(command_name, set()):
                    prefix_value_pending = True
                previous = word
                continue

            name = os.path.basename(word)
            if name == "rm":
                return True
            if name in prefixes:
                command_name = name
                previous = word
                continue

            command_name = name
            expect_command = False
            previous = word
            continue

        name = os.path.basename(word)
        if command_name == "xargs" and name == "rm":
            return True
        if command_name == "find" and previous in {"-exec", "-execdir"} and name == "rm":
            return True
        if command_name in shells and previous == "-c" and invokes_rm(word):
            return True
        previous = word

    return False


try:
    payload = json.load(sys.stdin)
except (json.JSONDecodeError, OSError):
    sys.exit(0)

command = payload.get("tool_input", {}).get("command", "")
if isinstance(command, str) and invokes_rm(command):
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": "Direct rm is blocked. Use trash <path> instead."
        }
    }))
'
