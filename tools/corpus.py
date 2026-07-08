"""
Shared helpers: discover topic source files and build the code-only text
that concept detection scans. Concept detection must ignore comment/doc
prose (otherwise English words like "is", "in", "and" and URL "//" match),
so the scan corpus is the concatenation of the parser's verbatim `code`
fields — real code only, no comments, no docstrings.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from parse_lessons import parse_file  # noqa: E402

BASE = Path(__file__).resolve().parent.parent

# (topic id, display name, source dir relative to BASE, module range key)
TOPIC_DIRS = [
    ("basics", "Introduction to Python", "basics/src"),
    ("eda", "Exploratory Data Analysis", "EDA/src"),
    ("mathplotlib", "Data Visualization (Matplotlib)", "Mathplotlib/src"),
    ("pandas", "Data Manipulation (pandas)", "Pandas/src"),
    ("stats", "Statistics in Python", "Stats In Python /src"),
]

# Strip trailing inline comments from a code line without breaking any #
# that lives inside a string literal.
_INLINE_COMMENT = re.compile(
    r"""
    (?P<code>
        (?: [^#'"] | '(?:\\.|[^'\\])*' | "(?:\\.|[^"\\])*" )*
    )
    \s\#.*$
    """,
    re.VERBOSE,
)


def strip_inline_comment(line: str) -> str:
    m = _INLINE_COMMENT.match(line)
    return m.group("code").rstrip() if m else line


# Match string literals (triple-quoted first, then single-line), keeping the
# opening prefix+quote and closing quote but neutralizing the interior so
# English words / operators *inside* strings don't match code-syntax regexes.
_STRING_LITERAL = re.compile(
    r"""
      (?P<prefix>[rRbBfFuU]{0,2})
      (?P<q>\"\"\"|'''|\"|')
      (?P<body>(?:\\.|(?!(?P=q)).)*)
      (?P=q)
    """,
    re.VERBOSE | re.DOTALL,
)


def neutralize_strings(code: str) -> str:
    """Replace the interior of every string literal with dots (letters/spaces
    removed), preserving delimiters, prefixes, and newline count so line
    numbers and quote-based detectors still work."""
    def repl(m):
        body = m.group("body")
        neutral = "".join("\n" if ch == "\n" else "." for ch in body)
        return f'{m.group("prefix")}{m.group("q")}{neutral}{m.group("q")}'

    return _STRING_LITERAL.sub(repl, code)


def topic_source_files(rel_dir: str):
    return sorted((BASE / rel_dir).glob("*.py"))


def parse_topic(rel_dir: str):
    """Return list of parsed chapter dicts for a topic directory."""
    return [parse_file(p) for p in topic_source_files(rel_dir)]


def raw_code_lines(parsed_chapters):
    """Every step's verbatim code line across all chapters, with whole-line
    comments dropped and inline trailing comments stripped."""
    lines = []
    for chapter in parsed_chapters:
        for section in chapter["sections"]:
            for step in section["steps"]:
                for line in step["code"].split("\n"):
                    if line.lstrip().startswith("#"):
                        continue
                    lines.append(strip_inline_comment(line))
    return lines


def code_corpus_for_topic(parsed_chapters) -> str:
    """Scan corpus (string interiors neutralized) for one topic/chapter."""
    return neutralize_strings("\n".join(raw_code_lines(parsed_chapters)))


def raw_and_scan_corpus(parsed_chapters):
    """Return (raw_corpus, scan_corpus). Neutralization preserves length and
    newlines exactly, so a match offset in scan_corpus maps to the same
    offset in raw_corpus — letting us match on scan but display the real
    (string-intact) source line."""
    raw = "\n".join(raw_code_lines(parsed_chapters))
    return raw, neutralize_strings(raw)


def all_topics():
    """Yield (id, name, rel_dir, parsed_chapters, code_corpus)."""
    out = []
    for tid, name, rel, in [(a, b, c) for (a, b, c) in TOPIC_DIRS]:
        parsed = parse_topic(rel)
        corpus = code_corpus_for_topic(parsed)
        out.append((tid, name, rel, parsed, corpus))
    return out
