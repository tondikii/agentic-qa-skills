"""Validate scenario markdown files against the five BDD convertibility rules.

Usage:
    python bddcheck.py <scope>.scenario.md [<scope>.scenario.md ...]

Checks: unique titles, valid non-reserved tags, no markdown formatting
inside steps, no secrets or URLs in steps, no imperative click-type
chains, and a Then in every scenario. Exits 1 on any violation.
"""

import argparse
import re
import sys

TITLE = re.compile(r"^###\s+\S+:\s+(.+)$", re.M)
TAG_LINE = re.compile(r"^@(\S+(?:\s+@\S+)*)$", re.M)
TAG = re.compile(r"@[A-Za-z0-9_-]+")
RESERVED = re.compile(r"@(only|skip|fixme|fail|slow|mode:[a-z]+|timeout:\d+|retries:\d+)", re.I)
FENCED_GHERKIN = re.compile(r"```gherkin(.*?)```", re.S)
MARKDOWN_FMT = re.compile(r"\*\*|__|\[.+?\]\(.+?\)|<br")
SECRET_OR_URL = re.compile(r"https?://|password\s*=|secret\s*=|token\s*=", re.I)
IMPERATIVE = re.compile(r"\b(click|type|fill|press)\b.*\b(e\d+|button|textbox|field)\b", re.I)


def check_file(path):
    text = open(path, encoding="utf-8").read()
    errors = []

    titles = TITLE.findall(text)
    if len(titles) != len(set(titles)):
        errors.append("duplicate titles")

    for tag_line in TAG_LINE.findall(text):
        for piece in tag_line.split():
            tag = piece if piece.startswith("@") else "@" + piece
            if not TAG.fullmatch(tag):
                errors.append(f"bad tag: {tag}")
            if RESERVED.fullmatch(tag):
                errors.append(f"reserved tag: {tag}")

    for block in FENCED_GHERKIN.findall(text):
        for line in block.splitlines():
            s = line.strip()
            if not s or s.startswith("@") or s.startswith("Scenario:"):
                continue
            if MARKDOWN_FMT.search(s):
                errors.append(f"markdown formatting in step: {s}")
            if SECRET_OR_URL.search(s):
                errors.append(f"secret/url in step: {s}")
            if IMPERATIVE.search(s):
                errors.append(f"imperative click-type chain: {s}")
        if not [line for line in block.splitlines() if line.strip().startswith("Then")]:
            errors.append("scenario without Then")

    return errors


def main(argv=None):
    parser = argparse.ArgumentParser(description="Validate scenario files against BDD rules.")
    parser.add_argument("files", nargs="+", help="Scenario markdown files to check")
    args = parser.parse_args(argv)
    failed = False
    for path in args.files:
        errors = check_file(path)
        status = "PASS" if not errors else f"FAIL {errors}"
        print(f"{path}: {status}")
        failed = failed or bool(errors)
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
