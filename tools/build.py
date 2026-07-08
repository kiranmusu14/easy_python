"""
Build step: parse every reconstructed source file, attach syntax pointers
and a merged quiz to each chapter (a "topic"), group topics into named
modules, and serialize the whole result into one static data file the
frontend imports directly. No runtime parsing, no backend, no database.

Run:  python3 tools/build.py
Out:  web/data.js   (window.__COURSE_DATA__ = {...})
"""

import hashlib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from concepts import CONCEPTS  # noqa: E402
from quizzes import HAND_AUTHORED  # noqa: E402
from corpus import (  # noqa: E402
    BASE,
    parse_topic,
    raw_and_scan_corpus,
)

# ---------------------------------------------------------------------------
# 5. Modules: the ONE manually-curated step. Group chapter files into named
#    modules by simple course/numeric ranges, purely for sidebar order.
# ---------------------------------------------------------------------------
MODULES = [
    {
        "id": "foundations",
        "name": "Python Foundations",
        "blurb": "The core language: values, types, lists, functions and packages.",
        "dir": "basics/src",
    },
    {
        "id": "pandas",
        "name": "Data Manipulation with pandas",
        "blurb": "DataFrames, aggregation, indexing and building new data.",
        "dir": "Pandas/src",
    },
    {
        "id": "viz",
        "name": "Visualization with Matplotlib",
        "blurb": "Plots, time series, comparisons and sharing figures.",
        "dir": "Mathplotlib/src",
    },
    {
        "id": "eda",
        "name": "Exploratory Data Analysis",
        "blurb": "Cleaning, distributions, relationships and hypotheses.",
        "dir": "EDA/src",
    },
    {
        "id": "stats",
        "name": "Statistics in Python",
        "blurb": "Summary stats, probability, distributions and correlation.",
        "dir": "Stats In Python /src",
    },
]

COMPILED = [(c, re.compile(c["regex"], re.MULTILINE)) for c in CONCEPTS]


def stable_hash(s: str) -> int:
    return int(hashlib.sha256(s.encode("utf-8")).hexdigest(), 16)


# ---------------------------------------------------------------------------
# 3. Syntax pointers: scan a chapter's code against every concept, keep the
#    matches in dictionary order, with a real example line from the source.
# ---------------------------------------------------------------------------
def syntax_pointers_for(parsed_chapter):
    raw, scan = raw_and_scan_corpus([parsed_chapter])
    pointers = []
    for concept, rx in COMPILED:
        matches = list(rx.finditer(scan))
        if not matches:
            continue
        # Real example: the source line containing the first match (offsets
        # align because neutralization preserves length).
        start = matches[0].start()
        line_start = raw.rfind("\n", 0, start) + 1
        line_end = raw.find("\n", start)
        if line_end == -1:
            line_end = len(raw)
        example = raw[line_start:line_end].strip()
        pointers.append({
            "label": concept["label"],
            "explanation": concept["explanation"],
            "count": len(matches),
            "example": example,
        })
    return pointers


# ---------------------------------------------------------------------------
# 4b. Auto-generated "what does this snippet do?" questions.
# ---------------------------------------------------------------------------
def paraphrase_label(label: str) -> str:
    """Light, deterministic paraphrase of a step's comment label into an
    answer string. No LLM: just tidy the fragment."""
    text = label.strip()
    # Drop a trailing sentence-ending period for a cleaner option.
    text = re.sub(r"\.$", "", text)
    # Uppercase the first letter.
    if text and text[0].islower():
        text = text[0].upper() + text[1:]
    return text


def collect_step_candidates(parsed_chapter):
    """Steps with real code and a usable, distinctive label."""
    seen_labels = set()
    out = []
    for section in parsed_chapter["sections"]:
        for step in section["steps"]:
            code = step["code"].strip()
            label = step["label"].strip()
            if not code:
                continue
            if label in ("(untitled step)", ""):
                continue
            if len(label) < 12 or len(label) > 120:
                continue
            key = label.lower()
            if key in seen_labels:
                continue
            seen_labels.add(key)
            out.append({"label": label, "code": code})
    return out


def deterministic_shuffle(options, seed: str):
    """Order options deterministically by hashing seed+text (no Math.random)."""
    return sorted(options, key=lambda o: stable_hash(seed + "|" + o))


def auto_questions_for(topic_id, parsed_chapter, max_q=4):
    candidates = collect_step_candidates(parsed_chapter)
    if len(candidates) < 4:
        return []  # not enough distinct steps to form distractors

    # Deterministically pick which steps become question stems.
    ordered = sorted(candidates, key=lambda c: stable_hash(topic_id + "::" + c["code"]))
    stems = ordered[:max_q]

    questions = []
    for stem in stems:
        correct = paraphrase_label(stem["label"])
        # Distractors: other candidates' labels, deterministically chosen.
        others = [c for c in candidates if c["label"] != stem["label"]]
        others = sorted(others, key=lambda c: stable_hash(stem["code"] + "##" + c["label"]))
        distractors = []
        used = {correct}
        for o in others:
            para = paraphrase_label(o["label"])
            if para in used:
                continue
            distractors.append(para)
            used.add(para)
            if len(distractors) == 3:
                break
        if len(distractors) < 3:
            continue
        options = deterministic_shuffle([correct] + distractors, seed=stem["code"])
        answer = options.index(correct)
        questions.append({
            "question": "What does this snippet do?",
            "code": stem["code"],
            "options": options,
            "answer": answer,
            "explanation": f"This step is labelled: “{stem['label']}”.",
            "auto": True,
        })
    return questions


# ---------------------------------------------------------------------------
# 4. Merge hand-authored + auto-generated into each topic's quiz array.
# ---------------------------------------------------------------------------
def quiz_for(topic_id, parsed_chapter):
    quiz = []
    for q in HAND_AUTHORED.get(topic_id, []):
        quiz.append({**q, "auto": False})
    quiz.extend(auto_questions_for(topic_id, parsed_chapter))
    return quiz


# ---------------------------------------------------------------------------
# 6. Serialize.
# ---------------------------------------------------------------------------
def build():
    modules_out = []
    topics_out = []
    topic_order = []

    for module in MODULES:
        parsed_chapters = parse_topic(module["dir"])
        chapter_ids = []
        for parsed in parsed_chapters:
            topic_id = parsed["id"]
            intro = parsed["intro"]
            pointers = syntax_pointers_for(parsed)
            quiz = quiz_for(topic_id, parsed)
            n_steps = sum(len(s["steps"]) for s in parsed["sections"])
            topics_out.append({
                "id": topic_id,
                "moduleId": module["id"],
                "title": intro["title"] or topic_id,
                "description": intro["description"],
                "toc": intro["toc"],
                "sections": parsed["sections"],
                "syntaxPointers": pointers,
                "quiz": quiz,
                "meta": {
                    "sections": len(parsed["sections"]),
                    "steps": n_steps,
                    "pointers": len(pointers),
                    "quizQuestions": len(quiz),
                    "sourceFile": parsed["sourceFile"],
                },
            })
            chapter_ids.append(topic_id)
            topic_order.append(topic_id)
        modules_out.append({
            "id": module["id"],
            "name": module["name"],
            "blurb": module["blurb"],
            "topicIds": chapter_ids,
        })

    data = {
        "generatedBy": "tools/build.py",
        "modules": modules_out,
        "topics": topics_out,
        "topicOrder": topic_order,
        "totalTopics": len(topics_out),
    }
    return data


def main():
    data = build()
    out_dir = BASE / "web"
    out_dir.mkdir(exist_ok=True)
    payload = json.dumps(data, ensure_ascii=False, indent=2)
    (out_dir / "data.js").write_text(
        "// AUTO-GENERATED by tools/build.py — do not edit by hand.\n"
        "window.__COURSE_DATA__ = " + payload + ";\n",
        encoding="utf-8",
    )
    # Also emit raw JSON for the serverless function / debugging.
    (out_dir / "data.json").write_text(payload, encoding="utf-8")

    # Build summary.
    total_q = sum(len(t["quiz"]) for t in data["topics"])
    total_auto = sum(sum(1 for q in t["quiz"] if q.get("auto")) for t in data["topics"])
    print(f"Modules: {len(data['modules'])}   Topics: {len(data['topics'])}")
    print(f"Quiz questions: {total_q}  (auto {total_auto}, hand {total_q - total_auto})")
    print(f"Wrote {out_dir/'data.js'} ({len(payload)} bytes)")


if __name__ == "__main__":
    main()
