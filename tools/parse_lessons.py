"""
Parser: turns a reconstructed .py source file into structured lesson data.

Tokenizes a file into comment blocks, line comments, and code; normalizes
whatever banner style is used (====, ----, ####, etc.) into one canonical
"section" marker; treats the first comment block as the intro (title,
description, TOC) if it contains a table of contents; and walks the rest
of the file turning each (comment, code) pair into a step grouped under
its section. Output is byte-for-byte verbatim on code — no rewriting.
"""

import ast
import json
import re
import sys
from pathlib import Path

BANNER_RE = re.compile(r"^\s*#\s*[=\-#*~]{5,}\s*$")
TOC_HEADER_RE = re.compile(r"table of contents", re.IGNORECASE)
TOC_ITEM_RE = re.compile(r"^\s*(\d+)\.\s+(.+?)\s*$")
SECTION_TITLE_RE = re.compile(r"^\s*#\s*(\d+)\.\s+(.+?)\s*$")


def read_lines(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8").splitlines(keepends=True)


def leading_docstring_span(source: str):
    """Return (start_line, end_line, text) of the module's leading docstring, 0-indexed, end exclusive."""
    tree = ast.parse(source)
    if not tree.body:
        return None
    first = tree.body[0]
    if isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant) and isinstance(first.value.value, str):
        return (first.lineno - 1, first.end_lineno, first.value.value)
    return None


def parse_intro(docstring_text: str):
    """Split a docstring into title, description, and TOC entries."""
    lines = docstring_text.strip("\n").split("\n")
    toc_start = None
    for i, line in enumerate(lines):
        if TOC_HEADER_RE.search(line):
            toc_start = i
            break

    if toc_start is None:
        title = lines[0].strip() if lines else ""
        description = "\n".join(l.strip() for l in lines[1:] if l.strip() and not BANNER_RE.match(l)).strip()
        return {"title": title, "description": description, "toc": []}

    header_lines = lines[:toc_start]
    # Drop a "----" underline directly under the title, if present.
    body = [l for l in header_lines if l.strip() and not re.match(r"^[\-=]{3,}$", l.strip())]
    title = body[0].strip() if body else ""
    description = " ".join(l.strip() for l in body[1:]).strip()

    toc = []
    for line in lines[toc_start + 1:]:
        m = TOC_ITEM_RE.match(line)
        if m:
            toc.append({"number": int(m.group(1)), "label": m.group(2).strip()})

    return {"title": title, "description": description, "toc": toc}


def is_banner(line: str) -> bool:
    return bool(BANNER_RE.match(line))


def section_title_from_banner_block(lines: list[str], banner_idx: int):
    """Given the index of a banner line, find the section title line between
    this banner and its matching closing banner (canonical 3-line block:
    banner / '# N. Title' / banner)."""
    if banner_idx + 1 < len(lines):
        m = SECTION_TITLE_RE.match(lines[banner_idx + 1])
        if m:
            return int(m.group(1)), m.group(2).strip()
    return None, None


def strip_comment_marker(line: str) -> str:
    stripped = line.lstrip()
    if stripped.startswith("#"):
        stripped = stripped[1:]
        if stripped.startswith(" "):
            stripped = stripped[1:]
        return stripped.rstrip("\n")
    return line.rstrip("\n")


def parse_file(path: Path) -> dict:
    raw = path.read_text(encoding="utf-8")
    lines = read_lines(path)

    docspan = leading_docstring_span(raw)
    intro = {"title": path.stem, "description": "", "toc": []}
    body_start = 0
    if docspan:
        start, end, text = docspan
        intro = parse_intro(text)
        body_start = end

    sections = []
    current_section = None
    pending_comment_lines: list[str] = []
    i = body_start

    def flush_step(code_lines: list[str]):
        nonlocal pending_comment_lines
        note = "\n".join(strip_comment_marker(l).strip() for l in pending_comment_lines).strip()
        label_source = pending_comment_lines[0].strip() if pending_comment_lines else ""
        label = strip_comment_marker(label_source).strip() if label_source else ""
        code = "".join(code_lines).rstrip("\n")
        step = {
            "label": label if label else (note[:80] if note else "(untitled step)"),
            "note": note,
            "code": code,
        }
        pending_comment_lines = []
        if current_section is not None:
            current_section["steps"].append(step)
        return step

    n = len(lines)
    current_code_lines: list[str] = []
    blank_buffer: list[str] = []  # verbatim blank lines pending a decision

    while i < n:
        line = lines[i]

        if is_banner(line):
            number, title = section_title_from_banner_block(lines, i)
            if title:
                if current_code_lines or pending_comment_lines:
                    flush_step(current_code_lines)
                    current_code_lines = []
                blank_buffer = []
                current_section = {"number": number, "title": title, "steps": []}
                sections.append(current_section)
                i += 3  # banner, title line, closing banner
                if i < n and lines[i].strip() == "":
                    i += 1
                continue
            i += 1
            continue

        stripped = line.strip()

        if stripped == "":
            blank_buffer.append(line)
            i += 1
            continue

        if stripped.startswith("#"):
            if not current_code_lines:
                # Still accumulating the leading comment/label for the
                # upcoming step.
                pending_comment_lines.append(line)
            elif blank_buffer:
                # A genuine new paragraph: close out the current step and
                # start the next one's label.
                flush_step(current_code_lines)
                current_code_lines = []
                pending_comment_lines = [line]
            else:
                # A comment directly attached to the code above it (no
                # blank line in between) — keep it as part of that code,
                # verbatim.
                current_code_lines.append(line)
            blank_buffer = []
            i += 1
            continue

        # A code line. Blank-line gaps between code lines of the same
        # example (e.g. a multi-line function body, a multi-call plotting
        # block) do NOT start a new step — only a fresh comment paragraph
        # does. Reproduce the exact blank lines verbatim when committing.
        if current_code_lines:
            current_code_lines.extend(blank_buffer)
        blank_buffer = []
        current_code_lines.append(line)
        i += 1

    if current_code_lines or pending_comment_lines:
        flush_step(current_code_lines)

    return {
        "id": path.stem,
        "sourceFile": path.name,
        "intro": intro,
        "sections": sections,
    }


def main():
    if len(sys.argv) < 2:
        print("usage: parse_lessons.py <file.py> [more files...]", file=sys.stderr)
        sys.exit(1)

    results = []
    for arg in sys.argv[1:]:
        path = Path(arg)
        results.append(parse_file(path))

    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
