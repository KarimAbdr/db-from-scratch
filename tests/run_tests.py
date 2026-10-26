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


def stage_02():
    results = []
    results.append(
        check(
            "insert then select prints the row",
            ["insert 1 user1 person1@example.com", "select", ".exit"],
            [
                PROMPT + "Executed.",
                PROMPT + "(1, user1, person1@example.com)",
                "Executed.",
                PROMPT,
            ],
        )
    )

    # 32 / 255 chars is the maximum that must still fit (see ROW layout in docs)
    user, email = "a" * 32, "b" * 255
    results.append(
        check(
            "maximum length strings are accepted",
            [f"insert 1 {user} {email}", "select", ".exit"],
            [
                PROMPT + "Executed.",
                PROMPT + f"(1, {user}, {email})",
                "Executed.",
                PROMPT,
            ],
        )
    )

    results.append(
        check(
            "strings that are too long are rejected",
            [f"insert 1 {'a' * 33} {email}", "select", ".exit"],
            [
                PROMPT + "String is too long.",
                PROMPT + "Executed.",
                PROMPT,
            ],
        )
    )

    results.append(
        check(
            "negative id is rejected",
            ["insert -1 cstack foo@bar.com", "select", ".exit"],
            [
                PROMPT + "ID must be positive.",
                PROMPT + "Executed.",
                PROMPT,
            ],
        )
    )

    results.append(
        check(
            "malformed insert is a syntax error",
            ["insert 1", ".exit"],
            [PROMPT + "Syntax error. Could not parse statement.", PROMPT],
        )
    )

    # With ROW_SIZE = 293 and 4096-byte pages: 13 rows/page * 100 pages = 1300.
    script = [f"insert {i} user{i} person{i}@example.com" for i in range(1, 1302)]
    out = run(script + [".exit"])
    full = out[-3:-1] == [PROMPT + "Error: Table full.", PROMPT] or (
        out[-2] == PROMPT + "Error: Table full."
    )
    print(("PASS  " if full else "FAIL  ") + "table reports full after 1300 rows")
    results.append(full)
    return results


if __name__ == "__main__":
    results = stage_01() + stage_02()
    sys.exit(0 if all(results) else 1)
