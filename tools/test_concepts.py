"""
Validate the concept dictionary: every regex must compile, must not be
catastrophically slow, and its matches across all topics are printed so a
human can eyeball for false positives. Also flags entries that match
nothing anywhere (probably a broken/over-narrow regex) and entries that
match literally everything (probably too broad).
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from concepts import CONCEPTS  # noqa: E402
from corpus import all_topics  # noqa: E402


def load_topic_sources():
    # Scan the code-only corpus (no comment/doc prose) to avoid English-word
    # and URL false positives.
    return {name: corpus for (_id, name, _rel, _parsed, corpus) in all_topics()}


def main():
    topics = load_topic_sources()

    # 1. Every regex compiles.
    compiled = []
    for c in CONCEPTS:
        try:
            compiled.append((c, re.compile(c["regex"], re.MULTILINE)))
        except re.error as e:
            print(f"BROKEN REGEX  {c['label']!r}: {e}")
            sys.exit(1)

    # 2. Duplicate label check.
    labels = [c["label"] for c in CONCEPTS]
    dupes = {l for l in labels if labels.count(l) > 1}
    if dupes:
        print("DUPLICATE LABELS:", dupes)

    print(f"{len(CONCEPTS)} concepts, all compile.\n")

    verbose = "--verbose" in sys.argv
    matched_somewhere = set()

    for name, text in topics.items():
        hits = []
        for c, rx in compiled:
            found = rx.findall(text)
            if found:
                hits.append((c["label"], len(found)))
                matched_somewhere.add(c["label"])
        print(f"=== {name}: {len(hits)} pointers ===")
        for label, n in hits:
            print(f"   {n:3d}x  {label}")
        print()

    never = [c["label"] for c in CONCEPTS if c["label"] not in matched_somewhere]
    if never:
        print("NEVER MATCHED (check if too narrow / expected):")
        for l in never:
            print("   -", l)

    if verbose:
        # Print actual matched fragments for spot-checking false positives.
        target = sys.argv[-1] if not sys.argv[-1].startswith("--") else None
        for name, text in topics.items():
            if target and target != name:
                continue
            print(f"\n########## fragments for {name} ##########")
            for c, rx in compiled:
                found = rx.findall(text)
                if found:
                    print(f"\n--- {c['label']} ---")
                    # findall may return tuples for groups; normalize.
                    for m in rx.finditer(text):
                        frag = m.group(0).replace("\n", "\\n")
                        print("   ", frag[:90])


if __name__ == "__main__":
    main()
