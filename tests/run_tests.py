#!/usr/bin/env python3
"""Black-box tests: run the binary, feed commands to stdin, compare stdout."""
import subprocess
import sys

BIN = "build/db"
PROMPT = "db > "


def run(commands):
    proc = subprocess.run(
        [BIN],
        input="\n".join(commands) + "\n",
        capture_output=True,
        text=True,
        timeout=5,
    )
    return proc.stdout.split("\n")


def check(name, commands, expected):
    out = run(commands)
    if out == expected:
        print(f"PASS  {name}")
        return True
    print(f"FAIL  {name}\n  expected: {expected!r}\n  got:      {out!r}")
    return False


def stage_01():
    return [
        check(
            "exit command terminates the REPL",
            [".exit"],
            [PROMPT],
        ),
        check(
            "unknown meta-command is reported",
            [".foo", ".exit"],
            [PROMPT + "Unrecognized command '.foo'.", PROMPT],
        ),
        check(
            "insert and select are recognised",
            ["insert 1 user1 a@b.c", "select", ".exit"],
            [
                PROMPT + "Executed.",
                PROMPT + "Executed.",
                PROMPT,
            ],
        ),
        check(
            "unknown statement is reported",
            ["foo bar", ".exit"],
            [PROMPT + "Unrecognized keyword at start of 'foo bar'.", PROMPT],
        ),
    ]


if __name__ == "__main__":
    results = stage_01()
    sys.exit(0 if all(results) else 1)
