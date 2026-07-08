# Python Revision Workspace

A self-hosted, offline-first revision site built **from the course's own
Python source files** — parsed, not LLM-summarised. Five modules
(Foundations, pandas, Matplotlib, EDA, Statistics) across 19 chapter
"topics", each with a verbatim lesson, detected syntax pointers, and a
practice quiz. The whole thing is static HTML/CSS/JS plus one optional
serverless function.

## Layout

```
basics/  Pandas/  Mathplotlib/  EDA/  "Stats In Python"/
  └── src/*.py         reconstructed, verbatim course source (the source of truth)
tools/
  parse_lessons.py     tokenizes a .py file into sections + {label, code} steps
  concepts.py          the 97-entry concept dictionary (label, regex, explanation)
  test_concepts.py     validates every regex against every topic (no false positives)
  corpus.py            builds the code-only scan corpus (strings/comments neutralized)
  quizzes.py           hand-authored "why" MCQs, keyed by topic
  build.py             parse → pointers → quiz → modules → web/data.js
web/
  index.html styles.css app.js   the single-page frontend (no framework, no CDN)
  data.js              AUTO-GENERATED — the whole workspace serialized
api/
  ask.js               optional Ask-a-Doubt serverless function (Groq)
```

## Rebuild the data

Any time you edit a `src/*.py`, the dictionary, or the quizzes:

```bash
python3 tools/test_concepts.py     # sanity-check regexes (optional)
python3 tools/build.py             # regenerates web/data.js and web/data.json
```

`build.py` output is **deterministic** — the same inputs always produce a
byte-identical `data.js` (quiz shuffling uses a stable hash, not random).

## Run locally

Pure static (Ask-a-Doubt shows a graceful "not deployed" note):

```bash
cd web && python3 -m http.server 8000
# open http://localhost:8000
```

With the AI function, use your platform's dev server (e.g. `vercel dev`
from the project root) and put `GROQ_API_KEY=...` in a root `.env`
(git-ignored — see `.env.example`).

## Deploy

- **Static bundle:** deploy `web/` to any static host (Vercel, Netlify,
  Cloudflare Pages, GitHub Pages). No backend or database required.
- **AI function:** `api/ask.js` deploys as one serverless/edge endpoint at
  `/api/ask`. It uses only the Web Fetch API, so it runs unmodified on
  Vercel Edge, Cloudflare Workers, Netlify Edge, and Deno Deploy.
- **Secret:** set `GROQ_API_KEY` as a **platform secret** (never in a
  shipped file). Optionally `GROQ_MODEL` (default `llama-3.3-70b-versatile`).

The frontend works fully with the function switched off; only the
"Ask a Doubt" card degrades to an inline notice.

## Keyboard shortcuts

`j` / `k` next / previous topic · `/` focus search · `[` toggle sidebar ·
`t` toggle theme.

## How grounding works (Ask a Doubt)

The frontend sends the question plus the **current topic's already-parsed
lesson text** as the only context. There is no separate retrieval index or
embedding store — the parsed lesson text already is the correct grounding.
The system prompt instructs the model to answer only from that material.

## Notes on the source files

The `src/*.py` files were reconstructed from the course's slide PDFs (the
original scripts weren't available). Code is kept verbatim to what the
slides show; a few spots where the *original slides* were internally
inconsistent are flagged in code comments (e.g. an EDA `.fillna` without
reassignment, and differing `dogs` weights between pandas chapters) rather
than silently "fixed". `Machine learning`, `Numpy`, and `Seaborn` folders
had no source material and are intentionally omitted.
